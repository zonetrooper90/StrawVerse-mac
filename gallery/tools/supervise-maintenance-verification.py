#!/usr/bin/env python3
"""One-package, exact-commit, bounded Actions retry supervisor. Never publishes."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request

BRANCH = "gallery/development-clean"
PLAN = "gallery/queues/2026-11-19-maintenance-documentation.json"
BASE = "4e7f4eeeed62114b844bf65b057a95bd707f24ba"
ALLOWED = frozenset(json.loads("[\".github/workflows/gallery-maintenance-verification-supervisor.yml\",\"gallery/APPROVED-DECISIONS.md\",\"gallery/DEVELOPMENT-STATE.md\",\"gallery/MAINTENANCE-GUIDE.md\",\"gallery/README-WORKING.md\",\"gallery/WORKFLOW.md\",\"gallery/queues/2026-11-19-maintenance-documentation.json\",\"gallery/tests/test_maintenance_verification_supervisor.py\",\"gallery/tools/supervise-maintenance-verification.py\"]"))
INTEGRITY = "gallery-checkpoint-integrity.yml"
BROWSER = "gallery-transition-ui.yml"
EXPECTED = {
    INTEGRITY: {"integrity"},
    BROWSER: {"browser-routes (full)", "browser-routes (lightweight)", "browser-routes (subtitle-preview-modes)"},
}
CHECKS = {
    INTEGRITY: ("Verify current HTML exactly matches immutable checkpoint",
                "Restore immutable backup as recovery smoke test",
                "Dry-run complete HTML editing and immutable checkpoint creation",
                "Verify deterministic Gallery source assembly and asset build modes",
                "Verify complete publisher comparison matrices and original gate preservation"),
    BROWSER: ("Verify checkpoint and canonical working file",),
}
SETUP = {
    INTEGRITY: {"Set up job", "Check out committed Gallery source", "Set up Python"},
    BROWSER: {"Set up job", "Check out exact Gallery commit", "Set up Python"},
}
BROWSER_SETUP = "Install pinned Chromium test runner"
ROUTE_TEST = "Test navigation, coordinated fades, Watch History, Player and Settings"
ASSET_TEST = "Test both subtitle preview asset modes and geometry parity"

def required_steps(workflow, name):
    if workflow == INTEGRITY:
        return CHECKS[workflow]
    return CHECKS[workflow] + (BROWSER_SETUP, ASSET_TEST if name.endswith("(subtitle-preview-modes)") else ROUTE_TEST)

def step_map(job):
    steps = job.get("steps") or []
    if len({s["name"] for s in steps}) != len(steps):
        raise RuntimeError("Duplicate job steps")
    return {s["name"]: s.get("conclusion") for s in steps}

def classify(workflow, run, jobs):
    """Return pass, wait, retry, or stop; unknown states fail closed.
    A retry never permits a validation failure or user cancellation.
    jobs are latest effective jobs, merged by name across run attempts.
    """
    attempt = run.get("run_attempt")
    if type(attempt) is not int or not 1 <= attempt <= 2:
        return "stop", "Unexpected/exhausted run attempt"
    names = [j["name"] for j in jobs]
    if len(names) != len(set(names)) or not set(names) <= EXPECTED[workflow]:
        return "stop", "Unexpected job matrix"
    # Fail closed on validation failure even if another matrix job is running.
    for j in jobs:
        steps = step_map(j)
        if any(steps.get(s) in ("failure", "timed_out", "cancelled", "action_required", "neutral") for s in CHECKS[workflow]):
            return "stop", "Integrity/assembly validation did not pass: " + j["name"]
    if run.get("status") != "completed":
        return "wait", "Run not completed"
    if set(names) != EXPECTED[workflow] or any(j.get("status") != "completed" for j in jobs):
        return "stop", "Missing or unfinished required jobs"
    if run.get("conclusion") == "success":
        if all(j.get("conclusion") == "success" and all(step_map(j).get(s) == "success" for s in required_steps(workflow, j["name"])) for j in jobs):
            return "pass", "All required jobs and steps passed"
        return "stop", "Run success inconsistent with required jobs/steps"
    if run.get("conclusion") not in ("failure", "timed_out", "startup_failure"):
        return "stop", "Non-retryable workflow conclusion: " + str(run.get("conclusion"))
    if attempt == 2:
        return "stop", "Retry exhausted"
    failures = [j for j in jobs if j.get("conclusion") != "success"]
    if not failures:
        return "stop", "Run/job conclusions inconsistent"
    for j in failures:
        steps = step_map(j)
        conclusion = j.get("conclusion")
        if conclusion not in ("failure", "timed_out", "startup_failure"):
            # A timeout labelled cancelled by GitHub is ambiguous; never
            # automatically undo cancellation without explicit timeout evidence.
            if not (conclusion == "cancelled" and run.get("conclusion") == "timed_out"):
                return "stop", "Cancellation/unknown job result: " + j["name"]
        bad = {name for name, result in steps.items() if result in ("failure", "timed_out", "cancelled")}
        # Checkout/setup failures are retryable if no validation step failed.
        if bad and bad <= SETUP[workflow]:
            continue
        if workflow == BROWSER and all(steps.get(s) == "success" for s in CHECKS[BROWSER]):
            permitted = {BROWSER_SETUP, ASSET_TEST if j["name"].endswith("(subtitle-preview-modes)") else ROUTE_TEST}
            if bad and bad <= permitted:
                continue
            if conclusion == "timed_out" and not bad:
                continue
        return "stop", "Unclassified failure; inspect original logs: " + j["name"]
    return "retry", "Eligible failed jobs; retry same run once"

def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()

def digest(path):
    raw = Path(path).read_bytes()
    return len(raw), hashlib.sha256(raw).hexdigest()

def verify_scope(sha):
    plan = json.loads(Path(PLAN).read_text())
    assert plan["schema"] == 1 and plan["baseline"] == BASE and plan["branch"] == BRANCH
    assert plan["max_attempts"] == 2 and set(plan["workflow_files"]) == set(EXPECTED)
    assert os.environ["GITHUB_REF"] == "refs/heads/" + BRANCH
    assert git("rev-parse", "HEAD") == sha and git("rev-parse", "HEAD^") == BASE
    paths = set(git("diff", "--name-only", "--no-renames", BASE, sha).splitlines())
    assert paths == set(plan["changed_paths"]) == ALLOWED, paths
    pointer = json.loads(Path("gallery/checkpoints/current.json").read_text())
    p = plan["checkpoint"]
    assert (pointer["folder"], pointer["bytes"], pointer["sha256"]) == (p["folder"], p["full_bytes"], p["full_sha256"])
    assert digest("gallery/Gallery-current.html") == (p["full_bytes"], p["full_sha256"])
    assert digest("gallery/Gallery-development.html") == (p["light_bytes"], p["light_sha256"])
    subprocess.run(["python3", "gallery/tools/restore-checkpoint.py", "--verify-only"], check=True)
    subprocess.run(["python3", "gallery/tools/build-gallery.py", "--check"], check=True)
    assert not git("status", "--porcelain"), "Dirty supervisor checkout"

class API:
    def __init__(self):
        self.repo = os.environ["GITHUB_REPOSITORY"]
        assert self.repo == "zonetrooper90/StrawVerse-mac"
        self.prefix = "https://api.github.com/repos/" + self.repo
        self.token = os.environ["GH_TOKEN"]

    def call(self, path, post=False):
        # Only fixed GitHub REST endpoints; token is never logged. Reads have
        # bounded transient retries. Never blindly retry a POST with ambiguous outcome.
        req = urllib.request.Request(self.prefix + path,
            data=b"{}" if post else None,
            method="POST" if post else "GET",
            headers={"Authorization": "Bearer " + self.token,
                     "Accept": "application/vnd.github+json",
                     "X-GitHub-Api-Version": "2022-11-28",
                     "Content-Type": "application/json",
                     "User-Agent": "gallery-maintenance-supervisor"})
        for attempt in range(1 if post else 3):
            try:
                with urllib.request.urlopen(req, timeout=25) as response:
                    data = response.read()
                    if post:
                        if response.status not in (201, 202):
                            raise RuntimeError("Unexpected rerun response " + str(response.status))
                        return None
                    return json.loads(data)
            except (urllib.error.URLError, TimeoutError) as exc:
                if post or attempt == 2 or isinstance(exc, urllib.error.HTTPError) and exc.code not in (429, 500, 502, 503, 504):
                    raise
                time.sleep(5 * (attempt + 1))

    def assert_head(self, sha):
        ref = self.call("/git/ref/heads/" + BRANCH)
        assert ref["object"]["sha"] == sha, "Active branch advanced; stop rather than retry"

    def discover(self, workflow, sha):
        query = urllib.parse.urlencode({"head_sha": sha, "branch": BRANCH, "event": "push", "per_page": 100})
        data = self.call("/actions/workflows/" + workflow + "/runs?" + query)
        matches = [r for r in data["workflow_runs"] if r["head_sha"] == sha and r["head_branch"] == BRANCH and r["event"] == "push"]
        assert len(matches) <= 1, "Ambiguous exact-commit workflow runs"
        return matches[0]["id"] if matches else None

    def snapshot(self, run_id, sha):
        run = self.call(f"/actions/runs/{run_id}")
        assert run["id"] == run_id and run["head_sha"] == sha and run["head_branch"] == BRANCH and run["event"] == "push"
        attempt = run["run_attempt"]
        assert type(attempt) is int and 1 <= attempt <= 2, "Unexpected retry count"
        # Failed-job rerun may contain only rerun jobs in attempt 2; retain
        # attempt-1 successful jobs, supersede failed ones by exact name.
        effective = {}
        for n in range(1, attempt + 1):
            data = self.call(f"/actions/runs/{run_id}/attempts/{n}/jobs?per_page=100")
            assert data["total_count"] <= 100
            names = set()
            for j in data["jobs"]:
                assert j["run_id"] == run_id and j["head_sha"] == sha and j["name"] not in names
                names.add(j["name"])
                effective[j["name"]] = j
        return run, list(effective.values())

def main():
    sha = os.environ["GITHUB_SHA"]
    verify_scope(sha)
    api = API()
    api.assert_head(sha)
    summary = Path(os.environ["GITHUB_STEP_SUMMARY"])
    def record(message):
        print(message, flush=True)
        with summary.open("a", encoding="utf-8") as f:
            f.write(message + "\n\n")
    record("## A3.3 / A6 / A7 verification — exact commit " + sha)
    ids = {}
    requested = {}
    deadline = time.monotonic() + 110 * 60
    discovery = time.monotonic() + 8 * 60
    last = {}
    while time.monotonic() < deadline:
        for workflow in EXPECTED:
            if workflow not in ids:
                rid = api.discover(workflow, sha)
                if rid is not None:
                    ids[workflow] = rid
                    record(f"- {workflow}: https://github.com/{api.repo}/actions/runs/{rid}")
        if set(ids) != set(EXPECTED):
            if time.monotonic() > discovery:
                raise RuntimeError("Required exact-commit runs not found")
            time.sleep(20)
            continue
        decisions = {}
        for workflow, rid in ids.items():
            run, jobs = api.snapshot(rid, sha)
            if workflow in requested and run["run_attempt"] == 1:
                if time.monotonic() - requested[workflow] > 300:
                    raise RuntimeError("Rerun request not confirmed; inspect before retry")
                decision = ("wait", "Awaiting confirmed attempt 2")
            else:
                decision = classify(workflow, run, jobs)
            decisions[workflow] = (run, decision)
            state = (run["run_attempt"], *decision)
            if last.get(workflow) != state:
                record(f"- {workflow} attempt {state[0]}: {state[1]} — {state[2]}")
                last[workflow] = state
        # Never initiate any retry if either workflow reported a hard failure.
        stops = [f"{w}: {d[1]}" for w, (_, d) in decisions.items() if d[0] == "stop"]
        if stops:
            record("**STOP — manual investigation required:** " + "; ".join(stops))
            raise RuntimeError("Verification stopped")
        if all(d[0] == "pass" for _, d in decisions.values()):
            api.assert_head(sha)
            record("**PASS — both independent workflows succeeded on exact unchanged application.**")
            return
        for workflow, (run, decision) in decisions.items():
            if decision[0] != "retry":
                continue
            # Browser retry requires the independent integrity workflow to pass.
            if workflow == BROWSER and decisions[INTEGRITY][1][0] != "pass":
                continue
            assert workflow not in requested and run["run_attempt"] == 1
            api.assert_head(sha)
            # Re-read immediately before mutation; avoid double dispatch if
            # somebody manually reran this exact run since the last poll.
            latest, jobs = api.snapshot(ids[workflow], sha)
            assert latest["run_attempt"] == 1 and classify(workflow, latest, jobs)[0] == "retry"
            record(f"- Requesting one failed-jobs rerun of {workflow}, run {ids[workflow]}, attempt 1. Original logs retained.")
            api.call(f"/actions/runs/{ids[workflow]}/rerun-failed-jobs", post=True)
            requested[workflow] = time.monotonic()
        time.sleep(30)
    raise RuntimeError("Bounded supervisor deadline exceeded; inspect runs manually")

if __name__ == "__main__":
    main()
