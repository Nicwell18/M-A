"""Pruebas de las capas 2, 3 y 4 que NO llaman a la API.

Las respuestas "del modelo" de este archivo están escritas a mano: sirven para
probar el código que las comprueba y califica, no al modelo.
"""

from datetime import date

import yaml

from deal_analyzer.extract import Excerpt, Finding, build_prompt, select_excerpts, verify_quotes
from deal_analyzer.flag import METRICS, apply_bands, flag_findings
from deal_analyzer.ingest import Chunk
from deal_analyzer.report import build_rows

CLAUSES = yaml.safe_load(open("config/merger_agreement/clauses.yaml", encoding="utf-8"))["clauses"]
STANDARDS = yaml.safe_load(open("config/merger_agreement/playbook.yaml", encoding="utf-8"))["standards"]
CLAUSE = {c["id"]: c for c in CLAUSES}
STANDARD = {(s["clause"], s["field"]): s for s in STANDARDS}
DEAL = {"signing_date": date(2025, 12, 18), "equity_value_usd_m": {"company": 3000, "parent": 3000}}


def section(number, title, text):
    return Chunk("section", "ARTICLE X", "", number, title, text, 1, 1)


CHUNKS = [
    section("1.1", "Definitions",
            "Section 1.1 Definitions.\n"
            "“Company Material Adverse Effect” means any change that\nis materially adverse.\n"
            "“Company Termination Fee” means an amount equal to\n$90,000,000.\n"
            "“Law” means any statute."),
    section("6.5", "No Solicitation", "The Company Termination Fee is mentioned here."),
    section("8.3", "Termination Fee", "Section 8.3 Termination Fee.\n(a) In the event that..."),
]


def finding(clause, field, value, party="", verified=True):
    return Finding(clause, field, party, value, "cita", "Section 1.1", verified)


# --- Configuración: clauses.yaml y playbook.yaml deben encajar ---------------

def test_every_standard_points_to_an_existing_field():
    for standard in STANDARDS:
        fields = {f["field"]: f for f in CLAUSE[standard["clause"]]["extract"]}
        assert standard["field"] in fields


def test_every_choice_option_has_a_verdict_and_every_metric_exists():
    for standard in STANDARDS:
        field = next(f for f in CLAUSE[standard["clause"]]["extract"] if f["field"] == standard["field"])
        if field["type"] == "choice":
            assert set(standard["mapping"]) == set(field["options"])
        else:
            assert standard["metric"] in METRICS
            assert "up_to" not in standard["bands"][-1]


# --- Capa 2 -------------------------------------------------------------------

def test_select_excerpts_picks_section_and_definition():
    excerpts = select_excerpts(CHUNKS, CLAUSE["termination_fee"])
    assert [e.location for e in excerpts] == [
        "Section 1.1, definition of “Company Termination Fee”",
        "Section 8.3 (p. 1)",
    ]
    # La definición incluye su segunda línea y no se come la siguiente definición
    assert excerpts[0].text.endswith("$90,000,000.")


def test_prompt_lists_the_options_of_choice_fields():
    prompt = build_prompt(CLAUSE["no_shop"], [Excerpt("E1", "Section 6.5", "texto")])
    assert "option terminate_for_superior_proposal:" in prompt
    assert '<excerpt id="E1" location="Section 6.5">' in prompt


def test_verify_quotes_accepts_literal_and_rejects_invented():
    excerpts = [Excerpt("E1", "Section 1.1", "“Company Termination Fee” means an amount equal to\n$90,000,000.")]
    raw = [
        {"field": "amount_usd", "party": "Company", "value": "90000000", "excerpt_id": "E1",
         "quote": '"Company Termination Fee" means an amount equal to $90,000,000.'},
        {"field": "amount_usd", "party": "Parent", "value": "95000000", "excerpt_id": "E1",
         "quote": "Parent Termination Fee means $95,000,000"},
        # Dato manual, sin excerpt_id: se busca la cita en todos los trozos
        {"field": "amount_usd", "value": 90000000, "quote": "an amount equal to $90,000,000"},
    ]
    findings = verify_quotes("termination_fee", raw, excerpts)
    assert [f.verified for f in findings] == [True, False, True]
    assert findings[2].location == "Section 1.1"


# --- Capa 3 -------------------------------------------------------------------

def test_bands_boundaries():
    bands = STANDARD[("termination_fee", "amount_usd")]["bands"]
    verdicts = [apply_bands(v, bands)["verdict"] for v in (1.5, 2.0, 3.0, 3.5, 3.8, 4.0, 4.5)]
    assert verdicts == ["off-market", "off-market", "market", "market", "off-market", "off-market", "aggressive"]


def test_flag_findings():
    findings = [
        finding("termination_fee", "amount_usd", "90000000", "Company"),
        finding("termination_fee", "amount_usd", "150000000", "Parent"),
        finding("termination_fee", "amount_usd", "90000000", "Company", verified=False),
        finding("termination_fee", "amount_usd", "90000000", "Buyer"),      # parte desconocida
        finding("termination_fee", "triggers", "resumen", "Company"),       # sin estándar
        finding("outside_date", "end_date", "2026-12-18"),
        finding("outside_date", "end_date", "2027-12-18"),
        finding("specific_performance", "availability", "none"),
        finding("specific_performance", "availability", "opcion_inventada"),
        finding("no_shop", "match_right_business_days", "7", "Company"),
    ]
    verdicts = flag_findings(STANDARDS, findings, DEAL)
    assert [(v.verdict, v.metric_value) for v in verdicts] == [
        ("market", 3.0),
        ("aggressive", 5.0),
        ("sin calificar", None),
        ("sin calificar", None),
        ("market", 12.0),
        ("aggressive", 24.0),
        ("aggressive", None),
        ("sin calificar", None),
        ("off-market", 7.0),
    ]


# --- Capa 4 -------------------------------------------------------------------

def test_report_rows():
    findings = [
        finding("termination_fee", "amount_usd", "90000000", "Company"),
        finding("termination_fee", "triggers", "resumen", "Company"),
    ]
    rows = build_rows(CLAUSES, findings, flag_findings(STANDARDS, findings, DEAL))
    assert rows[0]["Qué dice el contrato"] == "[Company] Importe de la fee (USD): 90.000.000 (3.0 % del equity value de quien paga)"
    assert rows[0]["Veredicto"] == "market"
    assert rows[1]["Veredicto"] == "informativo"
    # Las cláusulas sin datos aparecen como no encontradas
    assert [r["Qué dice el contrato"] for r in rows[2:]] == ["No encontrada"] * 5
