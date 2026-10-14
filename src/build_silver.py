"""
Build the silver layer for GridForecast.

Reads the raw (bronze) layer produced by src/ingest.py, cleans and combines
the three data families (demand, generation, wind/solar forecast) into a
single model-ready table, and saves it to data/silver/ as Parquet.

All values are in MW. Cleaning steps:
  - Drop generation columns that are all zero for the country/window.
  - Give every column a tidy snake_case name, prefixed by source
    (demand, gen_*, fcst_*).
  - Align the three sources on a shared 15-min timestamp index (inner join)
    so every row is complete.

Usage:
    python src/build_silver.py

Requires the raw layer to exist (run src/ingest.py first).
"""

import re
from pathlib import Path

import pandas as pd

COUNTRY_CODE = "ES"
RAW_DIR = Path("data/raw") / COUNTRY_CODE.lower()
SILVER_DIR = Path("data/silver")


def _slug(text: str) -> str:
    """Lowercase snake_case slug (letters, digits and underscores only)."""
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def latest(subdir: str) -> pd.DataFrame:
    """Read the most recent Parquet file from a raw subfolder."""
    files = sorted((RAW_DIR / subdir).glob("*.parquet"))
    if not files:
        raise SystemExit(
            f"No parquet in {RAW_DIR / subdir}. Run `python src/ingest.py` first."
        )
    return pd.read_parquet(files[-1])


def clean_load(df: pd.DataFrame) -> pd.DataFrame:
    """Demand: keep the actual load column, renamed to `demand`."""
    return df.rename(columns={"Actual Load": "demand"})[["demand"]]


def clean_generation(df: pd.DataFrame) -> pd.DataFrame:
    """Generation: drop all-zero technologies and tidy the column names."""
    df = df.loc[:, (df != 0).any()]

    def rename(col: str) -> str:
        col = col.replace(" - Actual Aggregated", "")
        col = col.replace(" - Actual Consumption", " consumption")
        return "gen_" + _slug(col)

    return df.rename(columns=rename)


def clean_forecast(df: pd.DataFrame) -> pd.DataFrame:
    """Wind/solar forecast: prefix columns with `fcst_`."""
    return df.rename(columns=lambda c: "fcst_" + _slug(c))


def main() -> None:
    silver = (
        clean_load(latest("load"))
        .join(clean_generation(latest("generation")), how="inner")
        .join(clean_forecast(latest("wind_solar_forecast")), how="inner")
        .sort_index()
    )
    silver.index.name = "timestamp"

    SILVER_DIR.mkdir(parents=True, exist_ok=True)
    start, end = silver.index.min().date(), silver.index.max().date()
    out = SILVER_DIR / f"{COUNTRY_CODE.lower()}_silver_{start}_{end}.parquet"
    silver.to_parquet(out)

    print(f"Silver table: {silver.shape[0]} rows x {silver.shape[1]} columns")
    print(f"Range: {silver.index.min()} -> {silver.index.max()}")
    print(f"Nulls: {int(silver.isna().sum().sum())}")
    print(f"Columns: {list(silver.columns)}")
    print(f"Saved to: {out}")


if __name__ == "__main__":
    main()
