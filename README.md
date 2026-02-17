# Section 8 Sentinel

Section 8 Sentinel is a lightweight DevSecOps security dashboard that ingests scan results from CI pipelines and displays the latest findings per repository.

It currently supports:
- **Trivy** (vulnerability scanning)
- **Gitleaks** (secret scanning)

Findings are ingested via token-protected API endpoints and stored in a local SQLite database for MVP use.

---

## Features

- User registration + login
- Add repositories and generate **per-repo ingestion tokens**
- Token-authenticated ingestion API:
  - `POST /api/ingest/trivy`
  - `POST /api/ingest/gitleaks`
- Stores scans + findings in a database
- Dashboard shows:
  - onboarded repositories
  - latest findings across all repos

---

## Tech Stack

- Python 3
- Flask
- Flask-Login
- Flask-WTF
- SQLAlchemy (Flask-SQLAlchemy)
- SQLite (MVP)

---

## Getting Started (Local)

### 1) Clone
```bash
git clone git@github.com:ApacheSBC/section8-sentinel.git
cd section8-sentinel
