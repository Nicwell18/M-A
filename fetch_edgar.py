"""Descarga un contrato de EDGAR (SEC) a data/contracts/.

Uso:
    python fetch_edgar.py https://www.sec.gov/Archives/edgar/data/.../ex2-1.htm

La SEC exige que los programas se identifiquen con un nombre y un email de
contacto en la cabecera "User-Agent"; si no, responde 403. Ese dato NO se
escribe en el código (el repo es público): se lee de la variable de entorno
SEC_USER_AGENT, por ejemplo:

    export SEC_USER_AGENT="Nombre Apellido nombre@email.com"
"""

import os
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

CONTRACTS_DIR = Path("data/contracts")


def fetch(url: str) -> Path:
    """Descarga la URL y devuelve la ruta del archivo guardado."""
    user_agent = os.environ.get("SEC_USER_AGENT")
    if not user_agent:
        sys.exit("Falta la variable de entorno SEC_USER_AGENT (nombre y email de contacto).")

    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname != "www.sec.gov":
        sys.exit("Solo se admiten direcciones https://www.sec.gov/...")

    request = urllib.request.Request(url, headers={"User-Agent": user_agent})
    with urllib.request.urlopen(request, timeout=60) as response:
        content = response.read()

    CONTRACTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = CONTRACTS_DIR / Path(parsed.path).name
    out_path.write_bytes(content)
    return out_path


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Uso: python fetch_edgar.py <url de sec.gov>")
    saved = fetch(sys.argv[1])
    print(f"Guardado en {saved} ({saved.stat().st_size:,} bytes)")
