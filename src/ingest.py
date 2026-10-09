"""
ENTSO-E data ingestion for GridForecast.

For a given country and time window, downloads three data families from the
ENTSO-E Transparency Platform and saves them as Parquet in a "raw" (bronze)
layer following a medallion architecture:

    data/raw/<country>/<type>/<type>_<start>_<end>.parquet

  - Actual total load              -> type "load"
  - Generation by technology type  -> type "generation"
  - Wind and solar forecast        -> type "wind_solar_forecast"

This layer stores the raw data as it arrives from the source; cleaning and
modeling happen later on downstream layers.

Usage:
    python src/ingest.py

Requires:
    - A .env file at the project root with ENTSOE_API_TOKEN=<your_token>
    - The dependencies in requirements.txt installed
"""

import os
from pathlib import Path

import pandas as pd
from dotenv import find_dotenv, load_dotenv
from entsoe import EntsoePandasClient

# --- Configuration ---
COUNTRY_CODE = "ES"           # Spain
TIMEZONE = "Europe/Madrid"    # timezone of the Spanish electricity market
DAYS_BACK = 7                 # how many days back to download
RAW_DIR = Path("data/raw")    # raw (bronze) layer of the medallion architecture


def get_client() -> EntsoePandasClient:
    """Load the token from .env and create the ENTSO-E client."""
    load_dotenv(find_dotenv())
    token = os.getenv("ENTSOE_API_TOKEN")
    if not token or token == "your_token_here":
        raise SystemExit(
            "ERROR: ENTSOE_API_TOKEN not found. "
            "Copy .env.example to .env and paste your token."
        )
    return EntsoePandasClient(api_key=token)


def date_range():
    """Return (start, end) for the last DAYS_BACK days, timezone-aware."""
    end = pd.Timestamp.now(tz=TIMEZONE)
    start = end - pd.Timedelta(days=DAYS_BACK)
    return start, end


def save(df: pd.DataFrame, data_type: str, start, end) -> Path:
    """Save a DataFrame to the raw layer as Parquet.

    Path: data/raw/<country>/<type>/<type>_<start>_<end>.parquet
    Including the date range in the filename avoids overwriting previous
    downloads and keeps traceability of which period each file covers.

    Parquet needs string column names. Generation by technology arrives with
    multi-level (MultiIndex) columns, so we flatten them to a single level
    before saving.
    """
    df = df.copy()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [" - ".join(str(x) for x in col).strip(" -")
                      for col in df.columns]
    else:
        df.columns = [str(c) for c in df.columns]

    out_dir = RAW_DIR / COUNTRY_CODE.lower() / data_type
    out_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{data_type}_{start.date()}_{end.date()}.parquet"
    path = out_dir / filename
    df.to_parquet(path)
    return path


# --- Download functions (one per data family) ---

def fetch_load(client, start, end):
    """Actual total load."""
    data = client.query_load(COUNTRY_CODE, start=start, end=end)
    if isinstance(data, pd.Series):
        data = data.to_frame(name="actual_load")
    return data


def fetch_generation(client, start, end):
    """Generation by technology type."""
    return client.query_generation(COUNTRY_CODE, start=start, end=end, psr_type=None)


def fetch_wind_solar_forecast(client, start, end):
    """Wind and solar generation forecast."""
    return client.query_wind_and_solar_forecast(
        COUNTRY_CODE, start=start, end=end, psr_type=None
    )


def main() -> None:
    client = get_client()
    start, end = date_range()
    print(f"Country: {COUNTRY_CODE} | Window: {start.date()} -> {end.date()}\n")

    # (label, function, data type for the output path)
    jobs = [
        ("load", fetch_load, "load"),
        ("generation by technology", fetch_generation, "generation"),
        ("wind/solar forecast", fetch_wind_solar_forecast, "wind_solar_forecast"),
    ]

    for label, fn, data_type in jobs:
        print(f"Downloading {label} ...")
        try:
            df = fn(client, start, end)
            path = save(df, data_type, start, end)
            rel = path.relative_to(RAW_DIR.parent)
            print(f"  OK  {len(df)} rows, {df.shape[1]} column(s)  ->  {rel}")
        except Exception as e:  # noqa: BLE001
            # Intentionally catch failures per job so other downloads can continue.
            print(f"  ERROR downloading {label}: {e}")

    print("\nIngestion complete.")


if __name__ == "__main__":
    main()
