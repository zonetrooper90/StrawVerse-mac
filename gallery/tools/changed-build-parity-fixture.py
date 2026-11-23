#!/usr/bin/env python3
"""Build a NONPUBLISHED dual-HTML Gallery parity fixture in an isolated worktree.

The fixture is a deterministic LOCAL detached commit derived from an exact
approved development HEAD. It only appends an inert CSS comment, reconstructs
both HTML deliverables and an experimental checkpoint in the isolated worktree.
No original source, checkpoint, publishing workflow or remote branch is edited.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
PROBE = "gallery/development/preview-scripts/2026-11-23-stage7-source-probe.py"
CSS = "gallery/src/styles/28-unified-headers-and-history-frame.css"
FULL = "gallery/Gallery-current.html"
LIGHT = "gallery/Gallery-development.html"
POINTER = "gallery/checkpoints/current.json"
FIXTURE_ID = "2026-11-23-dynamic-regression-scratch-parity"
BASE_FULL_SHA = "2e01412a4da6874398af9e3373346208508e66be15ca3113c4c17023c05dff50"
BASE_LIGHT_SHA = "e9fa6ac3816f50c25b98c3f49e9332c9241cd6437e5005a5c98be80481602e93"
PROBE_BLOB = "1aec46b0807562bf7b6bb746e22f0e9a53ea0c01"
CANDIDATE_CSS_BLOB = "8fbefc98cba2123482963db830de36289a591ef1"
NOTE = b"/* Stage 7 source-only preview probe: HTML bytes change; visual behavior stays G3.1. */\n"
BASE_RUNS = ("45240712823", "45240712774", "45240713010")
FIXED_DATE = "2026-11-23T12:00:00+01:00"

def require(ok, reason):
    if not ok:
        raise AssertionError("Nonpublishing Gallery parity fixture: " + reason)

def git(cwd, *args, env=None):
    return subprocess.check_output(
        ["git", "-C", str(cwd), *args], text=True, env=env
    ).strip()

def run(cwd, *args):
    subprocess.run(args, cwd=cwd, check=True)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def verify_base(base):
    require(re.fullmatch(r"[0-9a-f]{40}", base) is not None, "base SHA not exact")
    require(git(ROOT, "rev-parse", "HEAD") == base, "triggering branch HEAD mismatch")
    require(git(ROOT, "status", "--porcelain") == "", "base checkout is dirty")
    pointer = json.loads((ROOT / POINTER).read_text(encoding="utf-8"))
    require(pointer["sha256"] == BASE_FULL_SHA,
            "not the unchanged approved G3.1 full checkpoint")
    require(sha((ROOT / FULL).read_bytes()) == BASE_FULL_SHA,
            "base full HTML differs from verified G3.1")
    require(sha((ROOT / LIGHT).read_bytes()) == BASE_LIGHT_SHA,
            "base lightweight HTML differs from verified G3.1")
    require(git(ROOT, "hash-object", PROBE) == PROBE_BLOB,
            "inert source probe is not the immutable approved script")
    require(NOTE not in (ROOT / CSS).read_bytes(),
            "source is already changed")
    return pointer

def make_fixture(base, output):
    old_ptr = verify_base(base)
    require(output.is_absolute(), "fixture must be an absolute scratch path")
    require(not output.exists(), "scratch candidate location must not already exist")
    require(not output.is_relative_to(ROOT), "scratch candidate may not be inside repository")
    output.parent.mkdir(parents=True, exist_ok=True)
    run(ROOT, "git", "-C", str(ROOT), "worktree", "add", "--detach", str(output), base)
    require(git(output, "rev-parse", "HEAD") == base, "worktree did not checkout approved commit")
    run(output, sys.executable, "-B", PROBE)
    require(git(output, "hash-object", CSS) == CANDIDATE_CSS_BLOB,
            "source patch differs from immutable nonvisual candidate")
    require((output / CSS).read_bytes().endswith(NOTE),
            "source probe unexpectedly changed runtime CSS")
    run(output, sys.executable, "-B", "gallery/tools/build-gallery.py", "--write-deliverables")
    new_full = (output / FULL).read_bytes()
    new_light = (output / LIGHT).read_bytes()
    require(sha(new_full) != BASE_FULL_SHA and sha(new_light) != BASE_LIGHT_SHA,
            "both generated HTML builds must change for this test")
    require(len(new_full) - old_ptr["bytes"] == len(NOTE) and
            len(new_light) > 0, "not an inert exact-size CSS-only build change")
    run(output, sys.executable, "-B", "gallery/tools/stage-checkpoint.py",
        "--input", FULL, "--id", FIXTURE_ID, "--status", "experiment")
    ptr = json.loads((output / POINTER).read_text(encoding="utf-8"))
    require(ptr["folder"] == FIXTURE_ID and ptr["status"] == "experiment" and
            ptr["sha256"] == sha(new_full) and ptr["bytes"] == len(new_full),
            "experimental isolated archive/pointer inconsistent")
    checkpoint_dir = "gallery/checkpoints/" + FIXTURE_ID
    stage_paths = [CSS, FULL, LIGHT, POINTER, checkpoint_dir]
    run(output, "git", "-C", str(output), "add", "--", *stage_paths)
    staged = set(filter(None, git(output, "diff", "--cached", "--name-only").splitlines()))
    required = {CSS, FULL, LIGHT, POINTER}
    require(required <= staged and
            all(p in required or p.startswith(checkpoint_dir + "/") for p in staged) and
            any(p.startswith(checkpoint_dir + "/parts/") for p in staged),
            "unexpected staged file or missing checkpoint chunk in candidate")
    tree = git(output, "write-tree")
    env = dict(os.environ, GIT_AUTHOR_NAME="Gallery Scratch Fixture",
               GIT_AUTHOR_EMAIL="gallery-fixture@example.invalid",
               GIT_COMMITTER_NAME="Gallery Scratch Fixture",
               GIT_COMMITTER_EMAIL="gallery-fixture@example.invalid",
               GIT_AUTHOR_DATE=FIXED_DATE, GIT_COMMITTER_DATE=FIXED_DATE)
    commit = subprocess.check_output(
        ["git", "-C", str(output), "commit-tree", tree, "-p", base],
        input="Gallery disposable changed dual-build fixture (NOT published)\n",
        text=True, env=env).strip()
    run(output, "git", "-C", str(output), "reset", "--hard", commit)
    require(git(output, "rev-parse", "HEAD") == commit and
            git(output, "show", "-s", "--format=%P", "HEAD") == base and
            git(output, "status", "--porcelain") == "",
            "synthetic detached fixture commit not clean and exact")
    require(git(ROOT, "rev-parse", "HEAD") == base and
            git(ROOT, "status", "--porcelain") == "" and
            (ROOT / POINTER).read_text(encoding="utf-8") ==
                json.dumps(old_ptr, indent=2) + "\n",
            "approved repository or checkpoint was modified")
    summary = {
        "status": "scratch-only-changed-source-dual-build-not-release",
        "base_commit": base, "scratch_commit": commit, "scratch_tree": tree,
        "source_blob": git(output, "hash-object", CSS),
        "full_sha256": sha(new_full), "full_bytes": len(new_full),
        "lightweight_sha256": sha(new_light), "lightweight_bytes": len(new_light),
        "checkpoint_id": FIXTURE_ID, "checkpoint_sha256": ptr["sha256"],
        "published": False, "experimental": True,
    }
    print(json.dumps(summary, sort_keys=True), flush=True)
    return summary

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--base", required=True)
    ap.add_argument("--scratch", type=Path, required=True)
    ap.add_argument("--summary", type=Path)
    a = ap.parse_args()
    data = make_fixture(a.base, a.scratch.resolve())
    if a.summary:
        dest = a.summary.resolve()
        require(not dest.is_relative_to(ROOT) and not dest.is_relative_to(a.scratch.resolve()),
                "summary must live outside all checkouts")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(data, sort_keys=True) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
