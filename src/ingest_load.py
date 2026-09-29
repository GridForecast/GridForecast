"""
Ingesta de demanda electrica desde ENTSO-E.

Descarga la demanda real (actual total load) de Espana para los ultimos
7 dias desde la ENTSO-E Transparency Platform y la guarda en Parquet
dentro de la carpeta data/.

Uso:
    python src/ingest_load.py

Requiere:
    - Un archivo .env en la raiz con ENTSOE_API_TOKEN=<tu_token>
    - Las dependencias de requirements.txt instaladas
"""

import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from entsoe import EntsoePandasClient

# --- Configuracion ---
COUNTRY_CODE = "ES"           # Espana
TIMEZONE = "Europe/Madrid"    # zona horaria del mercado electrico espanol
DAYS_BACK = 7                 # cuantos dias hacia atras descargar
OUTPUT_DIR = Path("data")
OUTPUT_FILE = OUTPUT_DIR / "es_load_ultimos_7d.parquet"


def get_client() -> EntsoePandasClient:
    """Carga el token desde .env y crea el cliente de ENTSO-E."""
    load_dotenv()  # lee el archivo .env de la raiz del proyecto
    token = os.getenv("ENTSOE_API_TOKEN")
    if not token or token == "your_token_here":
        raise SystemExit(
            "ERROR: no se encontro ENTSOE_API_TOKEN. "
            "Copia .env.example a .env y pega tu token."
        )
    return EntsoePandasClient(api_key=token)


def fetch_load(client: EntsoePandasClient) -> pd.DataFrame:
    """Descarga la demanda real de los ultimos DAYS_BACK dias."""
    end = pd.Timestamp.now(tz=TIMEZONE)
    start = end - pd.Timedelta(days=DAYS_BACK)
    print(f"Descargando demanda de {COUNTRY_CODE} "
          f"de {start.date()} a {end.date()} ...")

    data = client.query_load(COUNTRY_CODE, start=start, end=end)

    # Segun la version de entsoe-py puede devolver Series o DataFrame;
    # normalizamos a DataFrame para poder guardar en Parquet.
    if isinstance(data, pd.Series):
        data = data.to_frame(name="actual_load")
    return data


def main() -> None:
    client = get_client()
    df = fetch_load(client)

    print("\n=== Primeras filas ===")
    print(df.head())

    print("\n=== Resumen ===")
    print(f"Registros: {len(df)}")
    print(f"Rango: {df.index.min()}  ->  {df.index.max()}")

    OUTPUT_DIR.mkdir(exist_ok=True)
    df.to_parquet(OUTPUT_FILE)
    print(f"\nGuardado en: {OUTPUT_FILE.resolve()}")


if __name__ == "__main__":
    main()
