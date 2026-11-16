"""Capa 3 - Motor de red flags.

Compara lo extraído con el playbook y devuelve un veredicto. Aquí no hay IA:
es aritmética y una tabla de tramos, así que el mismo dato da siempre el
mismo veredicto y se puede explicar paso a paso.

Los umbrales NO están aquí: están en playbook.yaml. Lo único que sabe este
archivo es cómo calcular cada métrica.
"""

from dataclasses import dataclass

from deal_analyzer.extract import Finding


@dataclass
class Verdict:
    clause: str
    party: str
    metric_value: float | None  # p. ej. 3.0 (por ciento); None si no se pudo calcular
    verdict: str                # "market", "off-market", "aggressive" o "sin calificar"
    reason: str
    finding: Finding | None     # el dato del contrato en el que se apoya


# ---------------------------------------------------------------------------
# Métricas: cómo convertir un dato del contrato en un número comparable
# ---------------------------------------------------------------------------

def fee_pct_of_payer_equity_value(finding: Finding, deal: dict) -> float:
    """Fee / equity value de la parte que paga, en porcentaje."""
    amount_usd = float(finding.value)
    equity_usd_m = deal["equity_value_usd_m"][finding.party.lower()]
    return amount_usd / (equity_usd_m * 1_000_000) * 100


# nombre de la métrica en playbook.yaml -> (campo del que parte, función)
METRICS = {
    "fee_pct_of_payer_equity_value": ("amount_usd", fee_pct_of_payer_equity_value),
}


# ---------------------------------------------------------------------------
# Tramos
# ---------------------------------------------------------------------------

def apply_bands(value: float, bands: list[dict]) -> dict:
    """Devuelve el primer tramo cuyo límite superior no se supera.

    El último tramo no tiene 'up_to': recoge todo lo que quede por encima.
    """
    for band in bands:
        if "up_to" not in band or value <= band["up_to"]:
            return band
    raise ValueError("El último tramo del playbook no debe tener 'up_to'")


def flag_clause(standard: dict, findings: list[Finding], deal: dict) -> list[Verdict]:
    """Califica una cláusula: un veredicto por cada parte a la que se aplica."""
    field, compute = METRICS[standard["metric"]]
    verdicts = []
    for finding in findings:
        if finding.field != field:
            continue
        if not finding.verified:
            verdicts.append(Verdict(standard["clause"], finding.party, None, "sin calificar",
                                    "La cita no se ha podido verificar en el contrato.", finding))
            continue
        try:
            value = compute(finding, deal)
        except (KeyError, ValueError) as error:
            verdicts.append(Verdict(standard["clause"], finding.party, None, "sin calificar",
                                    f"No se pudo calcular la métrica: falta o no es válido {error}.", finding))
            continue
        band = apply_bands(value, standard["bands"])
        verdicts.append(Verdict(standard["clause"], finding.party, round(value, 2),
                                band["verdict"], band["reason"], finding))
    return verdicts
