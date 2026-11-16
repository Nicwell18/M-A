"""Capa 4 - Output.

Convierte datos y veredictos en la tabla final:

    cláusula | qué dice el contrato | cita exacta | ubicación | veredicto | justificación

y la guarda como CSV (para Excel) y como Markdown (para leer o enseñar).
"""

import csv
from pathlib import Path

from deal_analyzer.extract import Finding
from deal_analyzer.flag import Verdict

COLUMNS = ["Cláusula", "Qué dice el contrato", "Cita exacta", "Ubicación", "Veredicto", "Justificación"]


def format_number(text: str) -> str:
    """'90000000' -> '90.000.000'. Si no es un número, lo deja igual."""
    try:
        return f"{float(text):,.0f}".replace(",", ".")
    except ValueError:
        return text


def build_rows(clauses: list[dict], findings: list[Finding], verdicts: list[Verdict]) -> list[dict]:
    """Una fila por dato extraído, en el orden de clauses.yaml."""
    verdict_of = {id(v.finding): v for v in verdicts}
    rows = []
    for clause in clauses:
        fields = {f["field"]: f for f in clause["extract"]}
        clause_findings = [f for f in findings if f.clause == clause["id"]]

        if not clause_findings:
            rows.append(dict(zip(COLUMNS, [clause["name"], "No encontrada", "", "", "sin calificar",
                                           "No se localizó la cláusula en el contrato."])))
            continue

        for finding in clause_findings:
            field = fields.get(finding.field, {"label": finding.field, "type": "text"})
            value = format_number(finding.value) if field["type"] == "number" else finding.value
            says = f"{field['label']}: {value}"
            if finding.party:
                says = f"[{finding.party}] {says}"

            verdict = verdict_of.get(id(finding))
            if verdict is None:
                label, reason = "informativo", "Dato descriptivo; no se califica."
            else:
                label, reason = verdict.verdict, verdict.reason
                # Se añade la métrica calculada, salvo que sea el propio dato (p. ej. días).
                same_as_value = field["type"] == "number" and float(finding.value) == verdict.metric_value
                if verdict.metric_value is not None and not same_as_value:
                    says += f" ({verdict.metric_value} {verdict.unit})"
            if not finding.verified:
                says += " - CITA NO VERIFICADA"

            rows.append(dict(zip(COLUMNS, [clause["name"], says, finding.quote, finding.location, label, reason])))
    return rows


def write_csv(rows: list[dict], path: Path) -> None:
    # utf-8-sig hace que Excel reconozca los acentos al abrir el archivo
    with open(path, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict], path: Path, title: str, note: str = "") -> None:
    def cell(text: str) -> str:
        return " ".join(str(text).split()).replace("|", "\\|")  # una línea, sin romper la tabla

    lines = [f"# {title}", ""]
    if note:
        lines += [note, ""]
    lines.append("| " + " | ".join(COLUMNS) + " |")
    lines.append("|" + "---|" * len(COLUMNS))
    for row in rows:
        lines.append("| " + " | ".join(cell(row[c]) for c in COLUMNS) + " |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
