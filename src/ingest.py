"""
Ingesta de datos de ENTSO-E para GridForecast.

Descarga, para un pais y una ventana de tiempo, tres familias de datos
de la ENTSO-E Transparency Platform y las guarda en data/ como Parquet:
  - Demanda real (actual total load)
  - Generacion por tipo de tecnologia
  - Pronostico de eolica y solar

Uso:
    python src/ingest.py

Requiere:
    - Un archivo .env en la raiz con ENTSOE_API_TOKEN=<tu_token>
    - Las dependencias de requirements.txt instaladas
"""

import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv, find_dotenv
from entsoe import EntsoePandasClient

# --- Configuracion ---
COUNTRY_CODE = "ES"           # Espana
TIMEZONE = "Europe/Madrid"    # zona horaria del mercado electrico espanol
DAYS_BACK = 7                 # cuantos dias hacia atras descargar
OUTPUT_DIR = Path("data")


def get_client() -> EntsoePandasClient:
    """Carga el token desde .env y crea el cliente de ENTSO-E."""
    load_dotenv(find_dotenv())
    token = os.getenv("ENTSOE_API_TOKEN")
    if not token or token == "your_token_here":
        raise SystemExit(
            "ERROR: no se encontro ENTSOE_API_TOKEN. "
            "Copia .env.example a .env y pega tu token."
        )
    return EntsoePandasClient(api_key=token)


def date_range():
    """Devuelve (start, end) para los ultimos DAYS_BACK dias, con zona horaria."""
    end = pd.Timestamp.now(tz=TIMEZONE)
    start = end - pd.Timedelta(days=DAYS_BACK)
    return start, end


def save(df: pd.DataFrame, filename: str) -> Path:
    """Guarda un DataFrame en data/ como Parquet.

    Parquet necesita nombres de columna de tipo texto. La generacion por
    tecnologia llega con columnas de varios niveles (MultiIndex), asi que
    las aplanamos a un solo nivel antes de guardar.
    """
    df = df.copy()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [" - ".join(str(x) for x in col).strip(" -")
                      for col in df.columns]
    else:
        df.columns = [str(c) for c in df.columns]

    OUTPUT_DIR.mkdir(exist_ok=True)
    path = OUTPUT_DIR / filename
    df.to_parquet(path)
    return path


# --- Funciones de descarga (una por familia de datos) ---

def fetch_load(client, start, end):
    """Demanda real (actual total load)."""
    data = client.query_load(COUNTRY_CODE, start=start, end=end)
    if isinstance(data, pd.Series):
        data = data.to_frame(name="actual_load")
    return data


def fetch_generation(client, start, end):
    """Generacion por tipo de tecnologia."""
    return client.query_generation(COUNTRY_CODE, start=start, end=end, psr_type=None)


def fetch_wind_solar_forecast(client, start, end):
    """Pronostico de generacion eolica y solar."""
    return client.query_wind_and_solar_forecast(
        COUNTRY_CODE, start=start, end=end, psr_type=None
    )


def main() -> None:
    client = get_client()
    start, end = date_range()
    print(f"Pais: {COUNTRY_CODE} | Ventana: {start.date()} -> {end.date()}\n")

    # (etiqueta, funcion, nombre del archivo de salida)
    jobs = [
        ("demanda", fetch_load,
         f"{COUNTRY_CODE.lower()}_load_ultimos_{DAYS_BACK}d.parquet"),
        ("generacion por tecnologia", fetch_generation,
         f"{COUNTRY_CODE.lower()}_generation_ultimos_{DAYS_BACK}d.parquet"),
        ("pronostico eolico/solar", fetch_wind_solar_forecast,
         f"{COUNTRY_CODE.lower()}_wind_solar_forecast_ultimos_{DAYS_BACK}d.parquet"),
    ]

    for label, fn, filename in jobs:
        print(f"Descargando {label} ...")
        try:
            df = fn(client, start, end)
            path = save(df, filename)
            print(f"  OK  {len(df)} registros, {df.shape[1]} columna(s)  ->  {path.name}")
        except Exception as e:
            # Si una familia falla, seguimos con las demas en vez de abortar todo.
            print(f"  ERROR al descargar {label}: {e}")

    print("\nIngesta completada.")


if __name__ == "__main__":
    main()
