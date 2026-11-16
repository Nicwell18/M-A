"""Pruebas de las partes de las capas 2 y 3 que NO llaman a la API.

Las respuestas "del modelo" de este archivo están escritas a mano: sirven para
probar el código que las comprueba y califica, no al modelo.
"""

import yaml

from deal_analyzer.extract import Excerpt, Finding, select_excerpts, verify_quotes
from deal_analyzer.flag import apply_bands, flag_clause
from deal_analyzer.ingest import Chunk

CLAUSE = yaml.safe_load(open("config/merger_agreement/clauses.yaml", encoding="utf-8"))["clauses"][0]
STANDARD = yaml.safe_load(open("config/merger_agreement/playbook.yaml", encoding="utf-8"))["standards"][0]
DEAL = {"equity_value_usd_m": {"company": 3000, "parent": 3000}}


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


def test_select_excerpts_picks_section_and_definition():
    excerpts = select_excerpts(CHUNKS, CLAUSE)
    assert [e.location for e in excerpts] == [
        "Section 1.1, definition of “Company Termination Fee”",
        "Section 8.3 (p. 1)",
    ]
    # La definición incluye su segunda línea y no se come la siguiente definición
    assert excerpts[0].text.endswith("$90,000,000.")


def test_verify_quotes_accepts_literal_and_rejects_invented():
    excerpts = [Excerpt("E1", "Section 1.1", "“Company Termination Fee” means an amount equal to\n$90,000,000.")]
    raw = [
        {"field": "amount_usd", "party": "Company", "value": "90000000", "excerpt_id": "E1",
         "quote": '"Company Termination Fee" means an amount equal to $90,000,000.'},
        {"field": "amount_usd", "party": "Parent", "value": "95000000", "excerpt_id": "E1",
         "quote": "Parent Termination Fee means $95,000,000"},
    ]
    findings = verify_quotes("termination_fee", raw, excerpts)
    assert [f.verified for f in findings] == [True, False]


def test_bands_boundaries():
    verdicts = [apply_bands(v, STANDARD["bands"])["verdict"] for v in (1.5, 2.0, 3.0, 3.5, 3.8, 4.0, 4.5)]
    assert verdicts == ["off-market", "off-market", "market", "market", "off-market", "off-market", "aggressive"]


def finding(party, value, verified=True):
    return Finding("termination_fee", "amount_usd", party, value, "cita", "Section 1.1", verified)


def test_flag_clause():
    market, aggressive, unverified, unknown_party = flag_clause(
        STANDARD,
        [finding("Company", "90000000"), finding("Parent", "150000000"),
         finding("Company", "90000000", verified=False), finding("Buyer", "90000000")],
        DEAL,
    )
    assert (market.verdict, market.metric_value) == ("market", 3.0)
    assert (aggressive.verdict, aggressive.metric_value) == ("aggressive", 5.0)
    assert unverified.verdict == "sin calificar"
    assert unknown_party.verdict == "sin calificar"
