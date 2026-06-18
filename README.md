📂 Peer Lending

Peer Lending is an umbrella project for community‑driven peer‑to‑peer lending applications. It provides a modular foundation for building micro‑credit engines that combine trust, transparency, and startup speed.

Current branch focus:
Peer_Lending_Pulse

Current flagship apps under this repo:
Pulse Lending
Accesso Ancla

🌐 Vision

The Peer Lending initiative aims to deliver accessible micro‑credit through:
Community signals and social trust
Machine‑driven risk models
Flexible collateral and repayment frameworks
Transparent borrower/lender dashboards
Automated notifications (email + Telegram)

🏛️ Brand Segments

🔵 Pulse Lending
Identity: A community‑driven micro‑credit engine designed for everyday borrowers and lenders.
Tagline: “Finance with community at its core.”
Focus: Building trust networks and shared growth through transparent lending.
Use Case: Empowering individuals to borrow and lend within their social or professional circles.

🟠 Accesso Ancla

Identity: A neighborhood‑focused lending platform emphasizing local solidarity.
Tagline: “Credit built on community roots.”
Focus: Strengthening financial inclusion at the grassroots level.
Use Case: Supporting small businesses, gig workers, and families through localized peer lending.

🛠️ Development Tracks

Both apps currently share the same technical objectives and roadmap:

Borrower Risk Scoring
  Machine‑driven PD/LTV models
  Community trust signals
  Collateralization Framework

Digital asset escrow contracts
  Payroll deduction modules
  Payback Simulation Engine

Payback Simulation Engine
  Flexible repayment schedules
  Revenue‑share integrations

📑 Repo Structure

peer-lending/
│
├── Pulse/                # Pulse Lending app
├── Ancla/                # Accesso Ancla app
├── api/                  # FastAPI routes (identity, collateral, loan)
├── db/                   # Database migrations & schema
├── docs/                 # Scope of work, compliance notes
└── roadmap/              # GitHub Project boards (Roadmap + Kanban)

Published page entry points:

- Root: index.html
- Accesso Ancla: Ancla/index.html

⚙️ Developer Setup

**Branch:** `Peer_Lending_Pulse`

```bash
git checkout Peer_Lending_Pulse
```

**Install dependencies**

Requires [Poetry](https://python-poetry.org/docs/#installation) and Python 3.11.

```bash
poetry install
```

**Run the API server**

```bash
# Shorthand script (hot-reload, port 8001)
poetry run start

# Or explicitly with uvicorn
poetry run uvicorn src.api:app --reload --host 127.0.0.1 --port 8001
```

API will be available at `http://127.0.0.1:8001`.
Interactive docs: `http://127.0.0.1:8001/docs`

**Run tests**

```bash
poetry run pytest
```

🚀 Roadmap Milestones
MVP → Account creation, loan request, approval, fund distribution
Pilot → Risk scoring + collateral modules live
Compliance → Regulatory alignment + reporting
Production → Fully responsive dashboards + notifications
