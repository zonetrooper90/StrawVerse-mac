#!/usr/bin/env python3
"""Fail-closed invocation guard for NON-REQUIRED Gallery exact-commit browser shadow.

This does not publish, promote, mutate branches/checkpoints or replace the
original independent postpublication browser and integrity verification gates.
"""
import argparse
import re

EXPECTED_REPO = "zonetrooper90/StrawVerse-mac"
EXPECTED_REF = "refs/heads/gallery/development-clean"
SHA40 = re.compile(r"[0-9a-f]{40}\Z")

def validate(event, repository, ref, sha, expected):
    def require(ok, reason):
        if not ok:
            raise AssertionError("Gallery nonpublishing shadow invocation: " + reason)
    require(repository == EXPECTED_REPO, "wrong repository")
    require(ref == EXPECTED_REF, "wrong branch or tag")
    require(isinstance(sha, str) and SHA40.fullmatch(sha), "invalid triggering SHA")
    require(event in ("push", "workflow_dispatch"), "wrong event")
    if event == "push":
        require(expected in (None, ""), "unexpected push SHA override")
    else:
        require(isinstance(expected, str) and SHA40.fullmatch(expected),
                "manual invocation requires a complete exact commit SHA")
        require(expected == sha, "requested commit differs from exact GitHub run SHA")
    return sha

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--event", required=True)
    p.add_argument("--repository", required=True)
    p.add_argument("--ref", required=True)
    p.add_argument("--sha", required=True)
    p.add_argument("--expected", default="")
    a = p.parse_args()
    exact = validate(a.event, a.repository, a.ref, a.sha, a.expected)
    print("PASS read-only shadow invocation, same exact GitHub triggering SHA:", exact)
    print("NO release, NO new checkpoint, NO required-check substitution.")

if __name__ == "__main__":
    main()
