"""Analiza un contrato: extrae las cláusulas objetivo y las califica.

Uso:
    python analyze.py data/contracts/contrato.pdf             análisis completo (llama a la API)
    python analyze.py data/contracts/contrato.pdf --dry-run   enseña qué se enviaría, sin llamar

Necesita, junto al contrato, un archivo con el mismo nombre y extensión .yaml
con los datos del deal (tipo de contrato, valor, partes).
"""

import argparse
from pathlib import Path

import yaml

from deal_analyzer.extract import build_prompt, extract_clause, select_excerpts
from deal_analyzer.flag import flag_clause
from deal_analyzer.ingest import ingest


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description="Extrae y califica las cláusulas de un contrato.")
    parser.add_argument("contract", help="ruta al contrato (.htm, .html o .pdf)")
    parser.add_argument("--dry-run", action="store_true",
                        help="enseña los trozos seleccionados y el mensaje, sin llamar a la API")
    args = parser.parse_args()

    contract_path = Path(args.contract)
    deal = load_yaml(contract_path.with_suffix(".yaml"))

    # El tipo de contrato decide qué carpeta de configuración se usa.
    config_dir = Path("config") / deal["contract_type"]
    clauses = load_yaml(config_dir / "clauses.yaml")["clauses"]
    standards = {s["clause"]: s for s in load_yaml(config_dir / "playbook.yaml")["standards"]}

    chunks = ingest(str(contract_path))

    for clause in clauses:
        print(f"\n=== {clause['name']} ===")

        if args.dry_run:
            excerpts = select_excerpts(chunks, clause)
            for excerpt in excerpts:
                print(f"  {excerpt.id}  {excerpt.location}  ({len(excerpt.text):,} caracteres)")
            print("\n--- Mensaje que se enviaría al modelo (primeros 1.500 caracteres) ---")
            print(build_prompt(clause, excerpts)[:1500])
            continue

        findings = extract_clause(chunks, clause)
        if not findings:
            print("  No encontrada en el contrato.")
            continue

        for finding in findings:
            mark = "cita verificada" if finding.verified else "CITA NO VERIFICADA"
            print(f"  {finding.field} [{finding.party}] = {finding.value}")
            print(f"      «{finding.quote}»")
            print(f"      {finding.location} - {mark}")

        for verdict in flag_clause(standards[clause["id"]], findings, deal):
            value = f"{verdict.metric_value}%" if verdict.metric_value is not None else "n/d"
            print(f"\n  VEREDICTO [{verdict.party}]: {verdict.verdict.upper()} ({value})")
            print(f"      {verdict.reason}")


if __name__ == "__main__":
    main()
