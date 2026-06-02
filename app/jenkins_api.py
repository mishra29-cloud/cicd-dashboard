"""
Fetch pipeline data from Jenkins API.
This is the data source for our CI/CD dashboard.
"""

import jenkins
import json
from datetime import datetime
from pprint import pprint


def connect(url: str = "http://localhost:8080",
            username: str = "admin",
            password: str = "admin123") -> jenkins.Jenkins:
    """Connect to Jenkins and verify."""
    server = jenkins.Jenkins(url, username=username, password=password)
    user = server.get_whoami()
    print(f"Connected as: {user['fullName']}")
    print(f"Jenkins version: {server.get_version()}")
    return server


def get_all_builds(server: jenkins.Jenkins,
                   job_name: str = "sample-python-pipeline") -> list[dict]:
    """Fetch all builds for a job with details."""
    job_info = server.get_job_info(job_name)

    builds = []
    for build_ref in job_info["builds"]:
        build_num = build_ref["number"]
        build_info = server.get_build_info(job_name, build_num)

        build = {
            "number": build_num,
            "result": build_info.get("result", "IN_PROGRESS"),
            "duration_ms": build_info["duration"],
            "duration_sec": round(build_info["duration"] / 1000, 2),
            "timestamp": datetime.fromtimestamp(
                build_info["timestamp"] / 1000
            ).isoformat(),
            "url": build_info["url"],
        }
        builds.append(build)

    return builds


def print_build_summary(builds: list[dict]) -> None:
    """Print a readable summary of all builds."""
    print(f"\n{'='*60}")
    print(f"{'#':<5} {'Status':<12} {'Duration':<12} {'Timestamp'}")
    print(f"{'='*60}")

    for b in builds:
        status = b["result"] or "RUNNING"
        duration = f"{b['duration_sec']}s"
        print(f"#{b['number']:<4} {status:<12} {duration:<12} {b['timestamp']}")

    total = len(builds)
    passed = sum(1 for b in builds if b["result"] == "SUCCESS")
    failed = sum(1 for b in builds if b["result"] == "FAILURE")
    print(f"\nTotal: {total} | Passed: {passed} | Failed: {failed}")
    print(f"Pass rate: {passed/total*100:.1f}%")


if __name__ == "__main__":
    server = connect()
    builds = get_all_builds(server)
    print_build_summary(builds)
    
    # Also save raw data for inspection
    with open("data/builds.json", "w") as f:
        json.dump(builds, f, indent=2)
    print(f"\nRaw data saved to data/builds.json")
