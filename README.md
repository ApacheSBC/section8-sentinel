# Section 8 Sentinel

# Section 8 Sentinel

## Overview

Section 8 Sentinel is a lightweight DevSecOps-style security dashboard designed to track repositories and surface security findings in a simple, centralised interface.

The goal of this project was to build a working security tool from the ground up, deploy it to the cloud, connect it to a live database, and demonstrate the full lifecycle of a modern web application in a DevSecOps context.

This project was built as part of my transition into cybersecurity and DevSecOps after over 20 years working in electrical construction and site management.

---

## Live Demo

https://section8-sentinel.onrender.com

---

## Core Features (v1.0)

* User registration and login
* Repository tracking per user
* Security findings ingestion
* Severity classification (High, etc.)
* PostgreSQL-backed data storage
* Cloud deployment on Render
* Simple security dashboard UI

---

## Tech Stack

**Backend**

* Python
* Flask
* SQLAlchemy
* PostgreSQL

**Frontend**

* HTML
* CSS
* Jinja templates

**Infrastructure**

* Render (cloud hosting)
* Managed PostgreSQL database

---

## Architecture Overview

User → Web App (Flask) → PostgreSQL Database
↓
Security Findings Ingestion

The application handles authentication, stores repository data, and displays findings through a simple dashboard interface.

---

## How It Works

1. User registers and logs into the application.
2. User adds a repository to track.
3. Security findings are ingested into the system.
4. Findings are stored in PostgreSQL.
5. Dashboard displays the latest findings with severity levels.

---

## Local Setup

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/section8-sentinel.git
cd section8-sentinel
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Set environment variables:

```bash
export DATABASE_URL=your_postgres_url
export SECRET_KEY=your_secret_key
```

Run the app:

```bash
flask run
```

---

## Deployment

The application is deployed on Render using:

* A web service for the Flask app
* A managed PostgreSQL instance

Environment variables are configured in the Render dashboard.

---

## Future Improvements

Planned features:

* GitHub webhook ingestion
* Finding status (open, fixed, ignored)
* Risk scoring per repository
* Automated scans
* CI/CD security pipeline

---

## Author

Aaron Doran
Aspiring DevSecOps Engineer
Currently training in a DevSecOps Boot Camp.

### 1) Clone
```bash
git clone git@github.com:ApacheSBC/section8-sentinel.git
cd section8-sentinel
