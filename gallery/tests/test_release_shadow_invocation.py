#!/usr/bin/env python3
"""Negative cases for the optional exact-commit shadow workflow input guard."""
import runpy

api = runpy.run_path("gallery/tools/release-shadow-invocation.py")
validate = api["validate"]
repo = api["EXPECTED_REPO"]
ref = api["EXPECTED_REF"]
sha = "a" * 40
assert validate("push", repo, ref, sha, "") == sha
assert validate("workflow_dispatch", repo, ref, sha, sha) == sha

def reject(*args):
    try:
        validate(*args)
    except AssertionError:
        return
    raise AssertionError("unsafe shadow invocation accepted")

reject("workflow_dispatch", repo, ref, sha, "")
reject("workflow_dispatch", repo, ref, sha, "b" * 40)
reject("workflow_dispatch", repo, ref, sha, "HEAD")
reject("push", repo, ref, sha, sha)
reject("pull_request", repo, ref, sha, "")
reject("push", "other/repo", ref, sha, "")
reject("push", repo, "refs/heads/main", sha, "")
reject("push", repo, "refs/tags/2026", sha, "")
reject("push", repo, ref, "not-a-sha", "")
reject("push", repo, ref, sha.upper(), "")
print("PASS shadow exact-commit/manual-dispatch provenance and reject unsafe contexts.")
