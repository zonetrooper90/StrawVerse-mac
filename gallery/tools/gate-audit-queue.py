#!/usr/bin/env python3
"""Fail-closed, exact-commit gate for the explicitly approved read-only audit."""
import json
import os
import sys
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BRANCH = "gallery/development-clean"
WORKFLOWS = ("gallery-checkpoint-integrity.yml", "gallery-transition-ui.yml")
TASKS = ["verify-independent-workflows", "design-system-inventory", "search-syntax-investigation"]

def main():
    plan = json.loads(Path(sys.argv[1]).read_text())
    expected = {"schema": 1, "id": "2026-11-13-infrastructure-audit",
                "branch": BRANCH, "tasks": TASKS, "mode": "read-only", "stop": "human-review"}
    if plan != expected or os.environ["GITHUB_REF"] != "refs/heads/" + BRANCH:
        raise SystemExit("Unapproved plan or branch; stopping.")
    sha = os.environ["GITHUB_SHA"]
    repo = os.environ["GITHUB_REPOSITORY"]
    api = os.environ["GITHUB_API_URL"]
    token = os.environ["GH_TOKEN"]
    deadline = time.monotonic() + 35 * 60
    query = urlencode({"head_sha": sha, "branch": BRANCH, "event": "push", "per_page": 100})
    print("Waiting for both independent push checks on " + sha, flush=True)
    previous = None
    while time.monotonic() < deadline:
        successes = []
        observations = []
        for filename in WORKFLOWS:
            url = f"{api}/repos/{repo}/actions/workflows/{filename}/runs?{query}"
            req = Request(url, headers={"Authorization": "Bearer " + token,
                          "Accept": "application/vnd.github+json",
                          "X-GitHub-Api-Version": "2022-11-28"})
            with urlopen(req, timeout=30) as response:
                payload = json.load(response)
            runs = [r for r in payload["workflow_runs"]
                    if r["head_sha"] == sha and r["head_branch"] == BRANCH and r["event"] == "push"]
            if not runs:
                observations.append((filename, "not yet visible"))
                continue
            run = max(runs, key=lambda r: (r["run_number"], r["run_attempt"]))
            observations.append((filename, run["id"], run["status"], run["conclusion"]))
            if run["status"] == "completed":
                if run["conclusion"] != "success":
                    raise SystemExit(f"STOP: {filename} {run['conclusion']}: {run['html_url']}")
                successes.append(run)
        if observations != previous:
            print(observations, flush=True)
            previous = observations
        if len(successes) == len(WORKFLOWS):
            with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as out:
                out.write("## Independent checks passed\n\nExact commit: " + sha + "\n\n")
                for run in successes:
                    out.write(f"- [{run['name']}]({run['html_url']}) — success\n")
                out.write("\nOnly read-only investigation is authorized.\n")
            print("PASS: both independent checks succeeded; audit may proceed.", flush=True)
            return
        time.sleep(15)
    raise SystemExit("STOP: timed out waiting for both exact-commit checks.")

if __name__ == "__main__":
    main()
