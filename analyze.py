"""Analiza un contrato: extrae las cláusulas objetivo, las califica y guarda la tabla.

Uso:
    python analyze.py data/contracts/contrato.pdf
        análisis completo; la extracción llama a la API de Anthropic

    python analyze.py data/contracts/contrato.pdf --dry-run
        enseña qué trozos se enviarían al modelo, sin llamar a la API

    python analyze.py data/contracts/contrato.pdf --findings datos.yaml
        usa datos extraídos a mano en vez del modelo (las citas se verifican igual)

Necesita, junto al contrato, un archivo con el mismo nombre y extensión .yaml
con los datos del deal (tipo de contrato, valor, partes, fecha de firma).
El resultado se guarda en output/<nombre>.csv y output/<nombre>.md.
"""

import argparse
from pathlib import Path

import yaml

from deal_analyzer.extract import ask_model, select_excerpts, verify_quotes
from deal_analyzer.flag import flag_findings
from deal_analyzer.ingest import ingest
from deal_analyzer.report import build_rows, write_csv, write_markdown


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description="Extrae y califica las cláusulas de un contrato.")
    parser.add_argument("contract", help="ruta al contrato (.htm, .html o .pdf)")
    parser.add_argument("--dry-run", action="store_true",
                        help="enseña los trozos seleccionados, sin llamar a la API")
    parser.add_argument("--findings", metavar="YAML",
                        help="archivo con datos extraídos a mano, en vez de usar el modelo")
    args = parser.parse_args()

    contract_path = Path(args.contract)
    deal = load_yaml(contract_path.with_suffix(".yaml"))

    # El tipo de contrato decide qué carpeta de configuración se usa.
    config_dir = Path("config") / deal["contract_type"]
    clauses = load_yaml(config_dir / "clauses.yaml")["clauses"]
    standards = load_yaml(config_dir / "playbook.yaml")["standards"]

    manual = load_yaml(Path(args.findings)) if args.findings else None
    chunks = ingest(str(contract_path))

    findings = []
    for clause in clauses:
        excerpts = select_excerpts(chunks, clause)
        print(f"\n{clause['name']}: {len(excerpts)} trozos seleccionados")
        for excerpt in excerpts:
            print(f"    {excerpt.id}  {excerpt.location}  ({len(excerpt.text):,} caracteres)")
        if args.dry_run or not excerpts:
            continue

        if manual is not None:
            raw = [f for f in manual["findings"] if f["clause"] == clause["id"]]
        else:
            raw = ask_model(clause, excerpts)
        findings += verify_quotes(clause["id"], raw, excerpts)

    if args.dry_run:
        return

    verdicts = flag_findings(standards, findings, deal)
    rows = build_rows(clauses, findings, verdicts)

    print()
    for row in rows:
        print(f"{row['Veredicto'].upper():<14} {row['Cláusula']}: {row['Qué dice el contrato']}")

    origin = "extracción manual" if manual is not None else "extracción con modelo"
    note = f"Contrato: `{contract_path.name}`. Origen de los datos: {origin}."
    if manual is not None and manual.get("note"):
        note += " " + manual["note"]

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    write_csv(rows, output_dir / f"{contract_path.stem}.csv")
    write_markdown(rows, output_dir / f"{contract_path.stem}.md",
                   f"{deal['parties']['parent']} / {deal['parties']['company']}", note)
    print(f"\nGuardado en output/{contract_path.stem}.csv y .md")


if __name__ == "__main__":
    main()
