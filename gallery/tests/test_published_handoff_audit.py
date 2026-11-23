#!/usr/bin/env python3
"""Negative exact-published-SHA handoff tests (no network or publication)."""
from pathlib import Path
import copy
import runpy

audit = runpy.run_path(str(Path(__file__).resolve().parents[1] /
                          "tools/published-handoff-audit.py"))["audit"]
REQUEST = "ec5242eaf4bbf98ff96cadbb9c39e8214abd9698"
BUILD = "50bf289581c713fea36cf00e5eb6eed5b9619a5b"
IDS = {"publisher": 45046653548, "integrity": 45050371208, "browser": 45050373490}
R = "zonetrooper90/StrawVerse-mac"

def run(name, sha, event):
    return {"id": IDS[name], "head_sha": sha,
            "path": ".github/workflows/gallery-" +
                    {"publisher": "controlled-publish.yml",
                     "integrity": "checkpoint-integrity.yml",
                     "browser": "transition-ui.yml"}[name],
            "event": event, "repository": {"full_name": R},
            "head_branch": "gallery/development-clean", "status": "completed",
            "conclusion": "success", "run_attempt": 1}

def listing(name, names):
    return {"total_count": len(names),
            "jobs": [{"name": n, "run_id": IDS[name], "head_sha": BUILD,
                      "status": "completed", "conclusion": "success"} for n in names]}

def fixture():
    return {
        "publisher": run("publisher", REQUEST, "push"),
        "integrity": run("integrity", BUILD, "workflow_dispatch"),
        "browser": run("browser", BUILD, "workflow_dispatch"),
        "commit": {"sha": BUILD, "parents": [{"sha": REQUEST}],
                   "html_url": "https://github.com/" + R + "/commit/" + BUILD},
        "integrity_jobs": listing("integrity", ["integrity"]),
        "browser_jobs": listing("browser", ["browser-routes (full)",
                                          "browser-routes (lightweight)",
                                          "browser-routes (subtitle-preview-modes)"]),
    }

def reject(label, alter):
    data = copy.deepcopy(fixture())
    alter(data)
    try:
        audit(data, REQUEST, BUILD, IDS)
    except AssertionError:
        return
    raise AssertionError("accepted unsafe handoff: " + label)

def main():
    good = audit(fixture(), REQUEST, BUILD, IDS)
    assert good["shadow_dispatch_performed"] is False
    reject("wrong published commit", lambda d: d["commit"].update(sha=REQUEST))
    reject("wrong parent", lambda d: d["commit"]["parents"][0].update(sha=BUILD))
    reject("wrong browser sha", lambda d: d["browser"].update(head_sha=REQUEST))
    reject("wrong workflow", lambda d: d["browser"].update(path="shadow.yml"))
    reject("wrong event", lambda d: d["integrity"].update(event="push"))
    reject("failed original check", lambda d: d["browser"].update(conclusion="failure"))
    reject("retry", lambda d: d["browser"].update(run_attempt=2))
    reject("wrong branch", lambda d: d["integrity"].update(head_branch="main"))
    reject("wrong repo", lambda d: d["publisher"]["repository"].update(full_name="other/repo"))
    reject("missing job", lambda d: d["browser_jobs"]["jobs"].pop())
    reject("skipped job", lambda d: d["browser_jobs"]["jobs"][0].update(conclusion="skipped"))
    reject("wrong job sha", lambda d: d["browser_jobs"]["jobs"][0].update(head_sha=REQUEST))
    reject("wrong job run", lambda d: d["browser_jobs"]["jobs"][0].update(run_id=IDS["publisher"]))
    reject("duplicate job", lambda d: d["browser_jobs"]["jobs"][0].update(name="browser-routes (lightweight)"))
    print("PASS historical handoff and 14 fail-closed negative contracts")

if __name__ == "__main__":
    main()
