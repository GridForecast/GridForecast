# CLAUDE.md

Guidance for Claude Code when working in the GridForecast repository.

## Project

GridForecast is a real-time **probabilistic forecasting platform** for electricity
demand and renewable generation. It is a portfolio project: the goal is a running,
production-grade system that demonstrates the full data-science lifecycle — not a
one-off notebook. See `CHARTER.md` for the full vision, roles, and methodology.

## Tech stack

- **Python 3.11+**
- **Data:** ENTSO-E Transparency Platform via the `entsoe-py` client; `pandas`;
  `pyarrow` for Parquet storage.
- **Secrets:** `python-dotenv` (`.env` file).
- **Later milestones:** MLflow (experiment tracking), Streamlit (dashboard), Azure (cloud).

## Environment

- Virtual environment lives in `.venv/`; dependencies in `requirements.txt`.
- The ENTSO-E token is read from the environment variable `ENTSOE_API_TOKEN`,
  loaded from a local `.env` file with `python-dotenv`.
- Data files live in `data/` (gitignored) — never committed.

## Critical rules

- **NEVER commit `.env` or any secret/token.** It is gitignored; keep it that way.
- **NEVER hardcode the API token** in code. Always read it from the environment:
  `os.getenv("ENTSOE_API_TOKEN")`.
- **NEVER push directly to `main`.** Work on a branch → open a Pull Request →
  get one peer review → merge.
- **Keep dependencies minimal.** Add a library only when its milestone arrives,
  and update `requirements.txt` when you do.

## Conventions

- Small, focused commits with clear messages.
- Readable, documented code — this is a portfolio repo that others will read and review.
- Add a short comment or docstring for any non-obvious logic.
- Reproducibility matters: code must run from a clean clone by following the README.

## Definition of Done (see CHARTER.md)

A task is done only when it is reproducible, checked out-of-sample where applicable,
peer-reviewed, documented, and — for any cloud resource — passed the cost gate.

## Working style

- This is a learning project for the team. Explain your reasoning as you go.
- When a design choice is non-trivial, propose options with trade-offs rather than
  silently assuming one.
- The team communicates in Spanish; feel free to explain in Spanish when asked.
