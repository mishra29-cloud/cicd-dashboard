cat > README.md << 'READMEEOF'
# CI/CD Pipeline Dashboard

> Real-time pipeline health metrics from Jenkins — pass rates, duration trends, and failure tracking in one dashboard.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![Jenkins](https://img.shields.io/badge/Jenkins-LTS-red)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow)

![Dashboard Screenshot](docs/screenshot-dashboard.png)

## What it does

Connects to Jenkins via REST API, fetches real pipeline build data, computes health metrics (pass rate, duration trends, fastest/slowest builds), and displays everything in an interactive dark-themed dashboard. Built on patterns from 7+ years of CI/CD automation experience in a product-based company.

## Run it in 60 seconds

```bash
git clone https://github.com/Sakshi \ Dwivedi/cicd-dashboard.git
cd cicd-dashboard
docker compose up -d --build
# Open http://localhost:9000 for dashboard
# Open http://localhost:8080 for Jenkins
```

## Architecture

Browser ──→ FastAPI (port 9000)
│
├── GET /          → Jinja2 HTML + Chart.js
├── GET /api/builds  → JSON (all builds)
└── GET /api/metrics → JSON (computed metrics)
│
▼
python-jenkins
│
▼
Jenkins REST API (port 8080)
(Dockerized, Python-enabled)



**Data flow:** Browser requests dashboard → FastAPI calls Jenkins API → Normalizes raw build data into clean schema → Computes metrics (pass rate, duration percentiles) → Renders HTML with Chart.js bar chart → Browser displays interactive dashboard.

## API Endpoints

| Endpoint | Response | Description |
|----------|----------|-------------|
| `GET /` | HTML | Dashboard with metrics cards, chart, and build table |
| `GET /api/builds` | JSON | All builds with status, duration, timestamp |
| `GET /api/metrics` | JSON | Computed metrics: pass rate, avg duration, etc. |
| `GET /docs` | HTML | Auto-generated FastAPI OpenAPI documentation |

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Backend | Python 3.13 + FastAPI | Async-ready, auto OpenAPI docs, Pydantic validation |
| CI Integration | python-jenkins | Official SDK, handles auth and API versioning |
| Templates | Jinja2 | Server-side rendering, no JS build step |
| Charts | Chart.js (CDN) | Lightweight (200KB), sufficient for bar/line |
| Styling | Custom CSS (dark theme) | No framework dependency |
| CI Server | Jenkins LTS (Docker) | Custom image with Python |
| Testing | pytest + JUnit XML | 100% coverage, Jenkins-native reporting |
| Containers | Docker + docker-compose | One-command local setup |

## Design Decisions

**FastAPI over Flask:** Automatic OpenAPI docs, Pydantic validation, async-ready foundation for future real-time features.

**Jenkins API polling over webhooks:** Simpler for portfolio scope. Production approach: webhook receivers with polling reconciler as fallback.

**Server-side rendering over React SPA:** Dashboard is read-heavy with infrequent updates — SSR is the right fit. React would be overengineering.

**Dual interface (API + HTML):** Same backend serves both the dashboard UI and programmatic consumers (Slack bots, CI gates, other tools).

## What I'd Do Next

- [ ] **Database caching** — SQLite/Postgres to avoid hitting Jenkins API on every page load
- [ ] **LLM failure analysis** — Send failed build logs to an LLM, categorize failures automatically
- [ ] **Multi-CI support** — GitHub Actions and GitLab CI collectors behind a pluggable interface
- [ ] **DORA metrics** — Deployment Frequency, Lead Time, Change Failure Rate, MTTR
- [ ] **Slack notifications** — Alert on anomalous builds (duration 2x average)
- [ ] **Cloud deployment** — Containerize dashboard and deploy to Fly.io with live demo

## Run Tests

```bash
# Activate virtual environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run tests with coverage
python -m pytest tests/ -v --cov=app --cov-report=term-missing
```

## Project Structure

cicd-dashboard/
├── app/
│   ├── calculator.py        # Sample Python app (Jenkins builds this)
│   ├── jenkins_api.py       # Jenkins API client + data fetching
│   └── dashboard.py         # FastAPI backend + routes
├── templates/
│   └── dashboard.html       # Jinja2 template with Chart.js
├── static/
│   └── style.css            # Dark-themed dashboard styling
├── tests/
│   └── test_calculator.py   # pytest with 100% coverage
├── data/
│   └── builds.json          # Sample data for demo without Jenkins
├── docs/
│   └── screenshot-dashboard.png
├── docker-compose.yml       # Jenkins + Dashboard services
├── Dockerfile.jenkins       # Custom Jenkins image with Python
├── Jenkinsfile              # 4-stage pipeline definition
└── requirements.txt

## License

MIT — [Sakshi Dwivedi](https://www.linkedin.com/in/YOUR_LINKEDIN/)
READMEEOF
