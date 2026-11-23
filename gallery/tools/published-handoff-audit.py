#!/usr/bin/env python3
"""Fail-closed historical actual-published-SHA handoff audit; read-only, never a release."""
import argparse
import json
from pathlib import Path
import re

REPO = "zonetrooper90/StrawVerse-mac"
BRANCH = "gallery/development-clean"
SHA = re.compile(r"[0-9a-f]{40}\Z")
EXPECTED = {
    "publisher": (".github/workflows/gallery-controlled-publish.yml", "push"),
    "integrity": (".github/workflows/gallery-checkpoint-integrity.yml", "workflow_dispatch"),
    "browser": (".github/workflows/gallery-transition-ui.yml", "workflow_dispatch"),
}
BROWSER_JOBS = {"browser-routes (full)", "browser-routes (lightweight)",
                "browser-routes (subtitle-preview-modes)"}

def require(ok, message):
    if not ok:
        raise AssertionError("Gallery published handoff: " + message)

def audit(data, request, published, ids):
    require(all(isinstance(s, str) and SHA.fullmatch(s) for s in (request, published))
            and request != published, "invalid or equal request and published SHAs")
    require(set(ids) == set(EXPECTED) and all(type(v) is int and v > 0 for v in ids.values())
            and len(set(ids.values())) == 3, "run identity set")
    commit = data["commit"]
    require(commit.get("sha") == published and
            [p.get("sha") for p in commit.get("parents", [])] == [request],
            "published commit must be the direct child of publisher request")
    require(commit.get("html_url") == "https://github.com/" + REPO + "/commit/" + published,
            "published commit URL")

    for name, (path, event) in EXPECTED.items():
        r = data[name]
        sha = request if name == "publisher" else published
        require(r.get("id") == ids[name] and r.get("head_sha") == sha,
                name + " run ID / SHA mismatch")
        require(r.get("path") == path and r.get("event") == event,
                name + " workflow / event mismatch")
        require(r.get("repository", {}).get("full_name") == REPO and
                r.get("head_branch") == BRANCH, name + " repo / branch mismatch")
        require(r.get("status") == "completed" and r.get("conclusion") == "success"
                and r.get("run_attempt") == 1, name + " run must pass on attempt 1")

    for key, run_name, expected in (
        ("integrity_jobs", "integrity", {"integrity"}),
        ("browser_jobs", "browser", BROWSER_JOBS),
    ):
        info = data[key]
        jobs = info.get("jobs", [])
        require(info.get("total_count") == len(expected) and len(jobs) == len(expected),
                key + " missing or extra jobs")
        require({job.get("name") for job in jobs} == expected,
                key + " missing, duplicated or wrong job identities")
        for job in jobs:
            require(job.get("run_id") == ids[run_name] and
                    job.get("head_sha") == published and
                    job.get("status") == "completed" and
                    job.get("conclusion") == "success", key + " job did not pass at published SHA")

    return {"result": "PASS exact historical published-Gallery-SHA handoff",
            "published_sha": published, "publisher_request_sha": request,
            "original_independent_workflows": [ids["integrity"], ids["browser"]],
            "shadow_dispatch_performed": False, "release_authorized": False}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--directory", type=Path, required=True)
    args = p.parse_args()
    data = {name: json.loads((args.directory / (name + ".json")).read_text())
            for name in (*EXPECTED, "commit", "integrity_jobs", "browser_jobs")}
    result = audit(data, "ec5242eaf4bbf98ff96cadbb9c39e8214abd9698",
                   "50bf289581c713fea36cf00e5eb6eed5b9619a5b",
                   {"publisher": 45046653548, "integrity": 45050371208, "browser": 45050373490})
    print(json.dumps(result, sort_keys=True, indent=2))

if __name__ == "__main__":
    main()
