"""
CI/CD Pipeline Dashboard — FastAPI backend.
Reads Jenkins data and serves it via REST API + HTML dashboard.
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import jenkins
import json
from datetime import datetime
from pathlib import Path


app = FastAPI(title="CI/CD Pipeline Dashboard")

# Serve static files (CSS/JS) and HTML templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Jenkins connection config
JENKINS_URL = "http://localhost:8080"
JENKINS_USER = "admin"
JENKINS_PASS = "admin123"
JOB_NAME = "sample-python-pipeline"


def get_jenkins() -> jenkins.Jenkins:
    """Create Jenkins connection."""
    return jenkins.Jenkins(JENKINS_URL, JENKINS_USER, JENKINS_PASS)


def fetch_builds() -> list[dict]:
    """Fetch all builds with details from Jenkins."""
    server = get_jenkins()
    job_info = server.get_job_info(JOB_NAME)

    builds = []
    for build_ref in job_info["builds"]:
        build_num = build_ref["number"]
        build_info = server.get_build_info(JOB_NAME, build_num)

        build = {
            "number": build_num,
            "result": build_info.get("result", "IN_PROGRESS"),
            "duration_ms": build_info["duration"],
            "duration_sec": round(build_info["duration"] / 1000, 2),
            "timestamp": datetime.fromtimestamp(
                build_info["timestamp"] / 1000
            ).strftime("%Y-%m-%d %H:%M:%S"),
            "url": build_info["url"],
        }
        builds.append(build)

    return builds


def compute_metrics(builds: list[dict]) -> dict:
    """Compute DORA-style pipeline metrics."""
    total = len(builds)
    if total == 0:
        return {}

    passed = sum(1 for b in builds if b["result"] == "SUCCESS")
    failed = sum(1 for b in builds if b["result"] == "FAILURE")
    durations = [b["duration_sec"] for b in builds if b["result"] == "SUCCESS"]

    avg_duration = round(sum(durations) / len(durations), 2) if durations else 0
    fastest = round(min(durations), 2) if durations else 0
    slowest = round(max(durations), 2) if durations else 0

    return {
        "total_builds": total,
        "passed": passed,
        "failed": failed,
        "pass_rate": round(passed / total * 100, 1),
        "fail_rate": round(failed / total * 100, 1),
        "avg_duration_sec": avg_duration,
        "fastest_build_sec": fastest,
        "slowest_build_sec": slowest,
    }


# ---- API Routes ----

@app.get("/api/builds")
def api_builds():
    """REST API: return all builds as JSON."""
    return fetch_builds()


@app.get("/api/metrics")
def api_metrics():
    """REST API: return computed metrics as JSON."""
    builds = fetch_builds()
    return compute_metrics(builds)


# ---- Dashboard HTML Route ----

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    """Serve the main dashboard page."""
    builds = fetch_builds()
    metrics = compute_metrics(builds)
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "builds": builds,
            "metrics": metrics,
            "job_name": JOB_NAME,
        },
    ) 
