# GridForecast

> Real-time probabilistic forecasting platform for electricity demand and renewable generation, with drift monitoring and automated retraining.

## Overview

GridForecast ingests live grid data (from the [ENTSO-E Transparency Platform](https://transparency.entsoe.eu/)), forecasts electricity demand and renewable generation with **calibrated uncertainty**, monitors data drift, retrains automatically, and exposes a dashboard plus a natural-language reporting layer.

This repository is the single source of truth for the project. Before contributing, read [`CHARTER.md`](./CHARTER.md) for the vision, roles, methodology, and Definition of Done.

## Prerequisites

- **Python 3.11 or newer**
- **Git**
- An **ENTSO-E API token** — free, but takes ~3 working days to obtain. See [Data source](#data-source) below.

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/GridForecast/GridForecast.git
cd GridForecast
```

### 2. Create and activate a virtual environment

A virtual environment keeps this project's dependencies isolated from the rest of your system.

**macOS / Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

When active, your terminal prompt shows `(.venv)`. Run `deactivate` to exit.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Secrets (like the API token) never go in the code or in Git. They live in a local `.env` file that is ignored by version control.

```bash
cp .env.example .env
```

Then open `.env` and paste your ENTSO-E token:

```
ENTSOE_API_TOKEN=your_token_here
```

> **Never commit `.env`.** It contains your personal token. The `.gitignore` already excludes it — keep it that way.

### 5. Verify the setup

```bash
python -c "import entsoe, pandas, dotenv; print('Environment OK')"
```

If you see `Environment OK`, you're ready to work.

## Project structure

```
GridForecast/
├── CHARTER.md          # Vision, roles, methodology, Definition of Done
├── README.md           # This file
├── requirements.txt    # Python dependencies
├── .env.example        # Template for environment variables (copy to .env)
├── .gitignore          # Files Git should ignore
├── src/                # Source code (added as the project grows)
├── data/               # Local data (ignored by Git)
└── notebooks/          # Exploratory notebooks
```

Directories like `src/`, `data/`, and `notebooks/` are created as work begins; they may not all exist yet.

## Data source

GridForecast uses the **ENTSO-E Transparency Platform**, the official open dataset of the European electricity grid, published under EU Regulation 543/2013. Data is free to use, including commercially, provided ENTSO-E is credited as the source.

To get API access:

1. Register a free account at [transparency.entsoe.eu](https://transparency.entsoe.eu/).
2. Email `transparency@entsoe.eu` with the subject `RESTful API access` and your registered email in the body. Access is granted within ~3 working days.
3. Sign in, go to **My Account**, and generate a token. **Copy it immediately** — it is shown only once.
4. Paste the token into your local `.env` file (step 4 above).

## Development workflow

We work on GitHub with two-week sprints and a Kanban board. In short:

- Every task is a GitHub **Issue** on the project board.
- Work happens on a **branch**, never directly on `main`.
- Changes are merged via **Pull Request** with **at least one peer review**.
- A task is done only if it meets the Definition of Done in [`CHARTER.md`](./CHARTER.md).

## Dependencies

Dependencies are intentionally minimal for now — just what the data ingestion phase needs. Modeling, MLOps, and dashboard libraries (scikit-learn, MLflow, Streamlit, etc.) will be added at their defined milestones, not up front.

Once your environment works, lock exact versions for reproducibility:

```bash
pip freeze > requirements.txt
```

## License & attribution

Data © ENTSO-E, used under EU Regulation 543/2013. Attribution to ENTSO-E as the source is required.
