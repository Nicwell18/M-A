"""Capa 2 - Extracción.

Para cada cláusula objetivo de clauses.yaml:

    select_excerpts()   elige los trozos del contrato donde puede estar (reglas)
    ask_model()         pide al modelo los datos, cada uno con su cita literal
    verify_quotes()     comprueba que cada cita existe de verdad en el contrato

El modelo solo ve los trozos seleccionados, no las 200 páginas: es más barato
y deja menos margen para que se confunda. Y nunca nos fiamos de su cita:
la comprobamos con código.

Este archivo no sabe nada de termination fees: todo lo que busca viene de
clauses.yaml.
"""

import json
import re
from dataclasses import dataclass

import anthropic

from deal_analyzer.ingest import Chunk

MODEL = "claude-opus-5-5"


@dataclass
class Excerpt:
    """Un trozo del contrato que se enseña al modelo."""
    id: str        # "E1", "E2"... para que el modelo diga de dónde sale cada cita
    location: str  # "Section 8.3 (pp. 121-123)"
    text: str


@dataclass
class Finding:
    """Un dato extraído del contrato."""
    clause: str     # id de la cláusula: "termination_fee"
    field: str      # "amount_usd"
    party: str      # parte a la que se refiere: "Company", "Parent" o ""
    value: str      # "90000000"
    quote: str      # cita literal del contrato que lo justifica
    location: str   # dónde está la cita
    verified: bool  # True si la cita aparece literalmente en ese trozo


# ---------------------------------------------------------------------------
# Paso 1: elegir los trozos relevantes (sin IA)
# ---------------------------------------------------------------------------

# Una definición empieza con el término entre comillas: “Company Termination Fee” means...
DEFINED_TERM_RE = re.compile(r"^[“\"]([^”\"]+)[”\"]")


def split_definitions(chunk: Chunk) -> dict[str, str]:
    """Parte la Section de Definitions en {término: texto de su definición}.

    Cada definición va desde la línea que abre con un término entre comillas
    hasta la siguiente línea que abre con otro.
    """
    definitions: dict[str, str] = {}
    term = None
    for line in chunk.text.splitlines():
        match = DEFINED_TERM_RE.match(line)
        if match:
            term = match.group(1)
            definitions[term] = line
        elif term:
            definitions[term] += "\n" + line
    return definitions


def select_excerpts(chunks: list[Chunk], clause: dict) -> list[Excerpt]:
    """Devuelve los trozos del contrato donde buscar la cláusula."""
    where = clause["where_to_look"]
    title_keys = [k.lower() for k in where.get("section_titles", [])]
    term_keys = [k.lower() for k in where.get("defined_terms", [])]

    selected: list[tuple[str, str]] = []  # (ubicación, texto)
    for chunk in chunks:
        if chunk.kind != "section":
            continue
        title = chunk.title.lower()
        if any(key in title for key in title_keys):
            selected.append((chunk.location, chunk.text))
        if "definitions" in title:
            for term, text in split_definitions(chunk).items():
                if any(key in term.lower() for key in term_keys):
                    selected.append((f"Section {chunk.number}, definition of “{term}”", text))

    return [Excerpt(f"E{i}", location, text) for i, (location, text) in enumerate(selected, start=1)]


# ---------------------------------------------------------------------------
# Paso 2: preguntar al modelo
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You extract facts from M&A contracts for a legal analyst.

You are given excerpts from one contract and a list of fields to extract.
Rules:
- Use only the excerpts. If a field is not stated in them, do not return it.
- Every finding needs a quote: a short passage copied character for character
  from one excerpt, enough to prove the value. Do not paraphrase, correct or
  join separate passages.
- If a field applies separately to more than one party, return one finding per
  party and name the party as the contract does (e.g. "Company", "Parent").
- For fields of type number, the value is digits only (e.g. 90000000)."""

# Forma exacta de la respuesta. La API garantiza que el JSON la cumple.
OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "field": {"type": "string"},
                    "party": {"type": "string"},
                    "value": {"type": "string"},
                    "quote": {"type": "string"},
                    "excerpt_id": {"type": "string"},
                },
                "required": ["field", "party", "value", "quote", "excerpt_id"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["findings"],
    "additionalProperties": False,
}


def build_prompt(clause: dict, excerpts: list[Excerpt]) -> str:
    """Monta el mensaje: qué cláusula, qué campos y los trozos del contrato."""
    fields = "\n".join(
        f"- {f['field']} (type: {f['type']}): {f['description']}" for f in clause["extract"]
    )
    documents = "\n\n".join(
        f'<excerpt id="{e.id}" location="{e.location}">\n{e.text}\n</excerpt>' for e in excerpts
    )
    return (
        f"Clause: {clause['name']}\n{clause['summary']}\n\n"
        f"Fields to extract:\n{fields}\n\n"
        f"Contract excerpts:\n\n{documents}"
    )


def ask_model(clause: dict, excerpts: list[Excerpt]) -> list[dict]:
    """Llama a la API y devuelve la lista de findings tal como la da el modelo."""
    client = anthropic.Anthropic()  # lee la clave de la variable ANTHROPIC_API_KEY
    response = client.messages.create(
        model=MODEL,
        max_tokens=16000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_prompt(clause, excerpts)}],
        output_config={
            "effort": "medium",
            "format": {"type": "json_schema", "schema": OUTPUT_SCHEMA},
        },
    )
    if response.stop_reason != "end_turn":
        raise RuntimeError(f"El modelo no terminó la respuesta (stop_reason={response.stop_reason})")
    text = next(block.text for block in response.content if block.type == "text")
    return json.loads(text)["findings"]


# ---------------------------------------------------------------------------
# Paso 3: comprobar las citas (sin IA)
# ---------------------------------------------------------------------------

def normalize(text: str) -> str:
    """Iguala espacios, saltos de línea y tipos de comillas antes de comparar."""
    text = text.replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'")
    return " ".join(text.split())


def verify_quotes(clause_id: str, raw_findings: list[dict], excerpts: list[Excerpt]) -> list[Finding]:
    """Convierte la respuesta del modelo en Findings y marca si la cita es real.

    Una cita es válida si aparece literalmente en el trozo que el modelo dice.
    Si no aparece, el dato se conserva pero queda marcado como NO verificado.
    """
    by_id = {e.id: e for e in excerpts}
    findings = []
    for raw in raw_findings:
        excerpt = by_id.get(raw["excerpt_id"])
        verified = excerpt is not None and normalize(raw["quote"]) in normalize(excerpt.text)
        findings.append(Finding(
            clause=clause_id,
            field=raw["field"],
            party=raw["party"],
            value=raw["value"],
            quote=raw["quote"],
            location=excerpt.location if excerpt else "desconocida",
            verified=verified,
        ))
    return findings


def extract_clause(chunks: list[Chunk], clause: dict) -> list[Finding]:
    """Los tres pasos seguidos para una cláusula."""
    excerpts = select_excerpts(chunks, clause)
    if not excerpts:
        return []
    return verify_quotes(clause["id"], ask_model(clause, excerpts), excerpts)
