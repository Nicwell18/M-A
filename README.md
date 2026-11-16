# Deal Term Analyzer

Herramienta en Python que lee contratos de M&A (merger agreements de empresas
cotizadas), extrae las cláusulas que mueven valor y riesgo, y las compara con
un estándar de mercado definido por el usuario. Cada veredicto
(*market / off-market / aggressive*) cita el texto exacto del contrato.

Es un proyecto de aprendizaje: la prioridad es que cada paso sea claro y
trazable, no la escala.

## Estado

| Capa | Qué hace | Estado |
|---|---|---|
| 1. Ingesta | HTML o PDF → una pieza por cada Section del contrato | Hecha. En el contrato real encuentra las 112 Sections de su índice |
| 2. Extracción | Localiza las cláusulas objetivo, con cita y ubicación | Escrita. La selección de trozos y la verificación de citas están probadas; **la llamada al modelo aún no se ha ejecutado** |
| 3. Red flags | Compara cada dato con el playbook | Hecha, para seis cláusulas |
| 4. Output | Tabla en CSV y Markdown | Hecha |

El análisis completo se ha ejecutado sobre el contrato real con datos extraídos
a mano (`--findings`), no con el modelo. El resultado está en
[`docs/ejemplo-informe.md`](docs/ejemplo-informe.md).

Cláusulas cubiertas: termination fee, no-shop y fiduciary out, Material Adverse
Effect, efforts regulatorios, outside date y specific performance. La
explicación de cada una está en
[`docs/guia-de-clausulas.md`](docs/guia-de-clausulas.md).

## Idea de diseño: motor y conocimiento separados

- `deal_analyzer/` es **el motor**. No contiene nada jurídico.
- `config/<tipo de contrato>/` es **el conocimiento**, en dos archivos:
  `clauses.yaml` (qué buscar) y `playbook.yaml` (cómo calificarlo, con sus
  fuentes y sus salvedades).
- `docs/guia-de-clausulas.md` explica cada cláusula: qué es, por qué importa
  y cómo se califica.

Añadir otro tipo de contrato (p. ej. credit agreements) debe ser añadir dos
archivos de configuración, sin tocar el motor.

## Uso

```bash
pip install -r requirements.txt

python main.py data/contracts/contrato.htm              # tabla con todas las sections
python main.py data/contracts/contrato.htm --show 5.3   # texto literal de una section
python main.py data/contracts/contrato.htm --json       # guarda los chunks en output/
```

Acepta `.htm` / `.html` (el formato nativo de EDGAR) y `.pdf`. Para descargar
un contrato de EDGAR a `data/contracts/`:

```bash
export SEC_USER_AGENT="Nombre Apellido nombre@email.com"   # la SEC lo exige
python fetch_edgar.py https://www.sec.gov/Archives/edgar/data/.../ex2-1.htm
```

Para analizar un contrato (necesita una API key de Anthropic):

```bash
export ANTHROPIC_API_KEY="..."
python analyze.py data/contracts/contrato.pdf --dry-run   # qué se enviaría, sin llamar a la API
python analyze.py data/contracts/contrato.pdf             # extracción y veredictos
```

Sin API key, con datos extraídos a mano (las citas se verifican igual):

```bash
python analyze.py data/contracts/tmtg_tae_merger_agreement.pdf \
       --findings data/reference/tmtg_tae_manual_findings.yaml
```

El resultado se guarda en `output/` como CSV y Markdown. Junto a cada contrato
hace falta un `.yaml` con los datos del deal que el contrato no contiene
(valor, partes, fecha de firma).

## Capas 2 y 3: extracción y veredicto

1. **Selección (reglas).** `clauses.yaml` dice dónde suele estar cada cláusula.
   El motor elige esas Sections y definiciones; solo eso se envía al modelo.
2. **Extracción (modelo).** El modelo devuelve cada dato con una cita literal y
   el trozo del que la saca, en un formato JSON fijo.
3. **Verificación (código).** Se comprueba que cada cita aparece literalmente
   en el contrato. Si no, el dato queda marcado y no se califica.
4. **Veredicto (código).** Según el tipo de dato: un número se convierte en
   una métrica y se busca su tramo; una opción se busca en una tabla. Todo
   sale de `playbook.yaml`. Sin IA: el mismo dato da siempre el mismo veredicto.

### Limitaciones del playbook

- Solo la termination fee tiene fuentes citadas. El resto de umbrales son
  criterio propio, pendientes de contrastar (p. ej. con el ABA Deal Points
  Study). Cada estándar lo indica en su campo `caveats`.
- El valor del deal por parte (necesario para el porcentaje de la fee) es una
  hipótesis sin verificar; ver el `.yaml` del contrato.
- Los estándares están pensados para deals de cotizadas en EE. UU.

El modelo solo interviene en el paso 2. Lo que decide el veredicto es
aritmética sobre un dato cuya cita se ha comprobado.

## Capa 1: cómo funciona la ingesta

Todo está en `deal_analyzer/ingest.py`, en tres pasos:

1. **`load_html`** o **`load_pdf`**: convierten el archivo en líneas de texto.
   El HTML da un párrafo por línea y es más limpio; el PDF guarda además la
   página de cada línea (para citar "p. 41").
2. **`clean_lines`** (solo PDF): quita cabeceras, pies y números de página.
   Una línea es cabecera o pie si está en el borde de la página y se repite en
   más de la mitad de las páginas.
3. **`split_into_chunks`**: abre una pieza nueva en cada encabezado
   `Section N.M`. No sabe de qué formato vinieron las líneas.

### Por qué trocear por Section y no por tamaño

Un troceado por tamaño fijo (cada 1.000 caracteres) corta las cláusulas por la
mitad y pierde la ubicación. En un contrato, la Section es la unidad con
sentido jurídico y es como se cita. Si la pieza es la Section, la cita y la
ubicación salen gratis.

### Los tres problemas y cómo se resuelven

| Problema | Solución |
|---|---|
| El índice repite todos los encabezados | El cuerpo empieza en el último `ARTICLE I` antes de las firmas |
| Los anexos tienen sus propios `ARTICLE I` | El cuerpo termina en `IN WITNESS WHEREOF`; el resto es `back_matter` |
| Referencias cruzadas a principio de línea ("Section 5.3 of this Agreement") | Un encabezado solo vale si su número es mayor que el anterior, está en el artículo actual y va seguido de un título en mayúscula |

Además, `check_numbering` avisa si falta algún número (5.1, 5.2, 5.4): un hueco
casi siempre es un encabezado que se ha escapado.

### Limitaciones conocidas

- Los PDF deben tener texto (no escaneados). El HTML no tiene números de página.
- Asume la estructura `ARTICLE` + `Section N.M`. Un contrato que numere de otra
  forma (solo "1.", "2.") no se trocea.
- Una referencia a la section *inmediatamente siguiente*, a principio de línea
  y seguida de palabras en mayúscula, se confundiría con su encabezado.
- Las Sections muy largas (p. ej. Definitions) quedan como una sola pieza.

## Estructura

```
deal_analyzer/ingest.py   capa 1: trocear el contrato
deal_analyzer/extract.py  capa 2: seleccionar, extraer y verificar citas
deal_analyzer/flag.py     capa 3: métrica y veredicto
deal_analyzer/report.py   capa 4: tabla en CSV y Markdown
analyze.py                analiza un contrato de principio a fin
main.py                   enseña el troceado de un contrato
fetch_edgar.py            descarga un contrato de EDGAR
config/merger_agreement/  cláusulas objetivo y playbook de M&A
docs/guia-de-clausulas.md guía explicativa de las cláusulas
data/contracts/           contratos (.htm o .pdf) y los datos de cada deal (.yaml)
data/reference/           datos extraídos a mano, como referencia
docs/ejemplo-informe.md   resultado del análisis del contrato de prueba
tests/                    pruebas con un contrato sintético
```

## Dependencias

- `pdfplumber`: extrae el texto de los PDF conservando el orden de lectura.
  El HTML se lee con la librería estándar de Python, sin dependencias.
- `pyyaml`: lee los archivos de configuración.
- `anthropic`: cliente oficial de la API, para la extracción.
- `pytest` (solo para las pruebas): `python -m pytest`.
