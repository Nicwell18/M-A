"""Capa 3 - Motor de red flags.

Compara lo extraído con el playbook y devuelve un veredicto. Aquí no hay IA:
es aritmética y tablas, así que el mismo dato da siempre el mismo veredicto y
se puede explicar paso a paso.

Los umbrales NO están aquí: están en playbook.yaml. Lo único que sabe este
archivo es cómo calcular cada métrica y cómo leer los dos tipos de estándar:

    metric + bands   dato numérico -> número -> tramo
    mapping          opción elegida -> veredicto
"""

from dataclasses import dataclass
from datetime import date

from deal_analyzer.extract import Finding


@dataclass
class Verdict:
    finding: Finding            # el dato del contrato en el que se apoya
    verdict: str                # "market", "off-market", "aggressive" o "sin calificar"
    reason: str
    metric_value: float | None = None  # p. ej. 3.0; None si el estándar no es numérico
    unit: str = ""                     # p. ej. "% del equity value de quien paga"


# ---------------------------------------------------------------------------
# Métricas: cómo convertir un dato del contrato en un número comparable
# ---------------------------------------------------------------------------

def fee_pct_of_payer_equity_value(finding: Finding, deal: dict) -> float:
    """Fee / equity value de la parte que paga, en porcentaje."""
    amount_usd = float(finding.value)
    equity_usd_m = deal["equity_value_usd_m"][finding.party.lower()]
    return amount_usd / (equity_usd_m * 1_000_000) * 100


def months_from_signing(finding: Finding, deal: dict) -> float:
    """Meses entre la firma del contrato y la fecha extraída."""
    signing = deal["signing_date"]  # PyYAML ya lo lee como fecha
    days = (date.fromisoformat(finding.value) - signing).days
    return days / 30.44  # duración media de un mes


def number(finding: Finding, deal: dict) -> float:
    """El dato ya es el número que se compara."""
    return float(finding.value)


# nombre de la métrica en playbook.yaml -> función que la calcula
METRICS = {
    "fee_pct_of_payer_equity_value": fee_pct_of_payer_equity_value,
    "months_from_signing": months_from_signing,
    "number": number,
}


# ---------------------------------------------------------------------------
# Veredictos
# ---------------------------------------------------------------------------

def apply_bands(value: float, bands: list[dict]) -> dict:
    """Devuelve el primer tramo cuyo límite superior no se supera.

    El último tramo no tiene 'up_to': recoge todo lo que quede por encima.
    """
    for band in bands:
        if "up_to" not in band or value <= band["up_to"]:
            return band
    raise ValueError("El último tramo del playbook no debe tener 'up_to'")


def judge(standard: dict, finding: Finding, deal: dict) -> Verdict:
    """Califica un dato con su estándar."""
    if not finding.verified:
        return Verdict(finding, "sin calificar", "La cita no se ha podido verificar en el contrato.")

    if "mapping" in standard:
        entry = standard["mapping"].get(finding.value)
        if entry is None:
            return Verdict(finding, "sin calificar", f"'{finding.value}' no es una opción prevista en el playbook.")
        return Verdict(finding, entry["verdict"], entry["reason"])

    try:
        value = METRICS[standard["metric"]](finding, deal)
    except (KeyError, ValueError) as error:
        return Verdict(finding, "sin calificar", f"No se pudo calcular la métrica: falta o no es válido {error}.")
    band = apply_bands(value, standard["bands"])
    # Se compara el valor exacto; el redondeo es solo para mostrarlo.
    return Verdict(finding, band["verdict"], band["reason"], round(value, 1), standard.get("unit", ""))


def flag_findings(standards: list[dict], findings: list[Finding], deal: dict) -> list[Verdict]:
    """Un veredicto por cada dato que tenga estándar en el playbook.

    Los datos sin estándar (p. ej. un resumen de texto) son informativos y no
    se califican.
    """
    by_field = {(s["clause"], s["field"]): s for s in standards}
    verdicts = []
    for finding in findings:
        standard = by_field.get((finding.clause, finding.field))
        if standard:
            verdicts.append(judge(standard, finding, deal))
    return verdicts
