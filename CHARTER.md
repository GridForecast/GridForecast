# GridForecast — Project Charter

### Probabilistic Forecasting Platform for the Electricity System

> **Single source of truth:** this repository. If an important decision isn't here, in an Issue, or in a PR, it doesn't exist.

---

## 1. Vision

Build a **production forecasting system** that predicts electricity demand and renewable generation in real time, with well-calibrated uncertainty, drift monitoring, and automatic retraining, plus a natural-language reporting layer.

The goal is **not** academic research or an isolated notebook, but a running system that anyone can open at a URL and that demonstrates the full lifecycle of a modern data scientist.

## 2. Real objective

Employability and portfolio. Success is measured by what a recruiter or hiring manager can see running and verify, not by accuracy metrics in a vacuum. The differentiator is the **engineering and operation around the model**, not the model itself.

By the end, each member should be able to show: a live data pipeline, a calibrated probabilistic model, deployment and monitoring, tests and CI/CD, purposeful LLM integration, and a public dashboard.

## 3. Scope

**In:**
- Live ingestion of grid data (ENTSO-E or a public operator) + open weather data.
- Versioned storage in Parquet.
- Probabilistic forecasting with uncertainty quantification (conformal prediction / calibrated intervals).
- Backtesting and honest out-of-sample validation.
- Model deployment + dashboard.
- Data drift and calibration monitoring; scheduled retraining.
- LLM layer that turns the forecast into a readable report.

**Out (for now):**
- Trading or investment recommendations.
- Expensive managed databases.
- GPUs and premium tiers without a milestone that justifies them.
- Any idle always-on cloud resource.

## 4. Team and roles

Each role has an owner; the **reviewer hat rotates every sprint** so everyone touches everything.

| Role | Owner | Main responsibility |
|------|-------|---------------------|
| **Data & Infra + Modeling** | Jalil | Live ingestion, storage, cloud, **budget owner** + probabilistic forecasting, uncertainty, and calibration |
| **MLOps & Monitoring** | Eliseo | Deployment, drift detection, retraining, CI/CD; co-reviewer of the modeling |
| **Product & GenAI** | David | Dashboard, visible evaluation/backtesting, documentation, narrative + LLM layer (stretch goal) |

> **Note (team of 3).** Willy left the project, so the Modeling role is absorbed. Jalil takes it on alongside Infra: the load is manageable because ingestion and modeling happen **in sequence, not in parallel** (pipeline first, then models). Drift and calibration monitoring is statistically adjacent to modeling, so Eliseo is the natural co-reviewer for that part. The LLM layer becomes a **stretch goal**, not a requirement: if time gets tight, it can be cut without harming the project.

## 5. Methodology

**Kanban with 2-week sprints, everything anchored to GitHub.**

- Every task (feature, model, bug) is an **Issue**.
- Board columns: `Backlog → In progress → In review → Done`.
- Every task goes on its **own branch** → **Pull Request** → **mandatory peer review** → merge.
- **Nobody** pushes directly to `main`.
- Biweekly demo at the end of each sprint.

**Cadence:**
- **Daily async standup** in chat (3 lines: what I did, what I'll do, what's blocking me).
- **Weekly 30-min sync**: board review + cloud cost snapshot.
- **Retro** at the end of each sprint (what worked, what didn't, one adjustment).

## 6. Tooling stack

| Need | Tool | Cost | When adopted |
|------|------|------|--------------|
| Code, tasks, docs | **GitHub** (repo + Projects + Wiki) | Free | Week 0 |
| Communication | **Discord / Slack** (async by default) | Free | Week 0 |
| Video call | **Google Meet / Discord** | Free | Week 0 |
| Experiment tracking | **MLflow** (local/self-hosted) | Free | Week ~4 |
| Dashboard | **Streamlit** | Free locally | When there's something to show |
| Cloud | **Azure** (serverless, scale-to-zero) | ~5–20 USD/mo austere | Deployment phase |

> **Rule:** don't adopt a tool until you actually need it. Start with just GitHub and chat.

## 7. Definition of Done

A task is *done* only if it meets **all** of:

- [ ] Code/notebook reproducible from scratch.
- [ ] Out-of-sample check where applicable.
- [ ] Code review approved by a teammate.
- [ ] Documentation entry.
- [ ] **Cost gate**: if it creates a cloud resource, the price was checked in the Azure calculator *before* creating it.

## 8. Cost control (surprise-proofing)

- **Azure Budgets with alerts at 50 / 80 / 100 %** — protection number one.
- Student-credit subscription with the spending limit enabled.
- Everything serverless / scale-to-zero; auto-shutdown on any VM.
- A single resource group, everything tagged.
- 5-minute cost review at each weekly sync.

**Estimate:** ~5–20 USD/mo in austere mode; probably **0 USD** for the first months with Azure for Students (100 USD credit) + GitHub Student Pack.

## 9. Timeline (~14 weeks)

| Phase | Weeks | Deliverable |
|-------|-------|-------------|
| Setup | 0 | Repo, roles, budget with alerts, data source chosen |
| Ingestion | 1–3 | Clean data flowing (local/serverless) |
| Modeling | 4–7 | Probabilistic forecasting + rigorous evaluation |
| Monitoring | 8–10 | Drift detection + retraining |
| Deployment | 11–13 | Dashboard + backtesting with honest validation |
| Wrap-up | 14+ | Documentation, portfolio write-up, LLM layer |

## 10. Sprint 0 backlog (setup)

Turn each item into an Issue and assign it:

1. Create the GitHub organization/repo and invite the four members.
2. Configure branch protection on `main` (PR + 1 mandatory review).
3. Create the board in GitHub Projects with the four columns.
4. Set up the Discord/Slack server and connect GitHub notifications.
5. Assign the four roles (use the team's skills assessment).
6. Create the Azure for Students subscription and configure Budgets + alerts.
7. Research and decide the grid data source (ENTSO-E vs local operator).
8. Write the `README.md` with environment setup (Python, dependencies).

## 11. Working norms

- **Async by default.** Chat is for quick unblocking; decisions go to GitHub.
- **Reviewing each other's code is learning**, not policing.
- No new tool without a real need.
- The project's framing is **research and education**, never investment advice.
