#!/usr/bin/env python3
"""G3.1-anchored source-only iteration rehearsal. No release/promotion writes.

The committed contract currently contains zero source changes. Any later source
replay must be separately approved, exact Git-blob pinned, and tested. Operates
on a disposable exact-commit checkout with output outside the repository.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import runpy
import subprocess
import sys
import time

ROOT = Path.cwd().resolve()
CONTRACT = Path("gallery/development/g31-iterations.json")
BASELINE = Path("gallery/development/verified-baseline.json")
POINTER = Path("gallery/checkpoints/current.json")
FULL = Path("gallery/Gallery-current.html")
LIGHT = Path("gallery/Gallery-development.html")
SHA40 = re.compile(r"[0-9a-f]{40}\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")
SLUG = re.compile(r"20[0-9]{2}-[0-9]{2}-[0-9]{2}-[a-z0-9-]+\Z")


def require(condition, why):
    if not condition:
        raise AssertionError("G3.1 iteration rehearsal: " + why)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()


def validate(state):
    require(isinstance(state, dict) and set(state) ==
            {"schema", "status", "baseline_ref", "baseline_git_blob",
             "mode", "iterations", "promotion"}, "unexpected schema")
    require(type(state["schema"]) is int and state["schema"] == 1 and
            state["status"] == "g31-iteration-rehearsal-not-release",
            "contract version/status")
    require(state["baseline_ref"] == str(BASELINE) and
            isinstance(state["baseline_git_blob"], str) and
            SHA40.fullmatch(state["baseline_git_blob"]), "G3.1 reference/identity")
    require(state["promotion"] ==
            {"status": "not-authorized", "published_commit": None},
            "release promotion is forbidden")
    steps = state["iterations"]
    require(isinstance(steps, list) and len(steps) <= 8,
            "up to eight separately approved iterations")
    mode = state["mode"]
    require((mode == "baseline-only-no-source-changes" and not steps) or
            (mode == "approved-source-only-steps" and bool(steps)),
            "no implicit application changes or unapproved iteration mode")
    slugs = set()
    for step in steps:
        require(isinstance(step, dict) and set(step) ==
                {"slug", "preview_script", "preview_script_blob",
                 "approved_script", "approved_script_blob", "source_blobs",
                 "lightweight_sha256", "lightweight_bytes"}, "step schema")
        slug = step["slug"]
        require(isinstance(slug, str) and SLUG.fullmatch(slug) and
                slug not in slugs, "unique date-prefixed iteration slug")
        slugs.add(slug)
        for k, prefix in (("preview_script", "gallery/changes/previews/"),
                          ("approved_script", "gallery/changes/pending/")):
            require(step[k] == prefix + slug + ".py", "immutable approved script path")
            require(isinstance(step[k + "_blob"], str) and
                    SHA40.fullmatch(step[k + "_blob"]), "script Git blob")
        sources = step["source_blobs"]
        require(isinstance(sources, dict) and 1 <= len(sources) <= 128,
                "exact cumulative source snapshot required")
        for path, expected in sources.items():
            p = Path(path)
            require(type(path) is str and p.is_relative_to(Path("gallery/src")) and
                    ".." not in p.parts and p.suffix in (".css", ".js", ".html", ".json")
                    and type(expected) is str and SHA40.fullmatch(expected),
                    "allowed source path and SHA")
        require(isinstance(step["lightweight_sha256"], str) and
                SHA256.fullmatch(step["lightweight_sha256"]) and
                type(step["lightweight_bytes"]) is int and
                step["lightweight_bytes"] > 0, "exact candidate SHA/bytes")
    return steps


def baseline_check(state):
    require(blob(BASELINE.read_bytes()) == state["baseline_git_blob"],
            "verified G3.1 baseline contract changed")
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    api = runpy.run_path("gallery/tools/verify-development-baseline.py")
    api["verify"](baseline)
    return baseline["baseline"]


def check_artifact(path, manifest_path, state, commit):
    validate(state)
    require(SHA40.fullmatch(commit) and git("rev-parse", "HEAD") == commit,
            "artifact verification must use exact GitHub commit")
    base = baseline_check(state)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    raw = path.read_bytes()
    expected = state["iterations"][-1] if state["iterations"] else {
        "lightweight_sha256": base["lightweight_sha256"],
        "lightweight_bytes": base["lightweight_bytes"]
    }
    require(set(manifest) ==
            {"status", "exact_commit", "verified_build_commit",
             "baseline_sha256", "baseline_checkpoint", "mode", "iterations",
             "lightweight_bytes", "lightweight_sha256",
             "promotion_authorized", "release_changed",
             "preflight_seconds"}, "manifest schema")
    require(manifest["status"] == "Development Preview — Not a Verified Release" and
            manifest["exact_commit"] == commit and
            manifest["verified_build_commit"] == base["verified_build_commit"] and
            manifest["baseline_sha256"] == base["full_sha256"] and
            manifest["baseline_checkpoint"] == base["checkpoint_folder"] and
            manifest["mode"] == state["mode"] and
            manifest["promotion_authorized"] is False and
            manifest["release_changed"] is False and
            type(manifest["preflight_seconds"]) in (int, float) and
            manifest["preflight_seconds"] >= 0 and
            manifest["lightweight_bytes"] == len(raw) == expected["lightweight_bytes"] and
            manifest["lightweight_sha256"] == digest(raw) == expected["lightweight_sha256"],
            "artifact provenance, sha or size differs")
    stages = state["iterations"]
    require(manifest["iterations"] ==
            [{"slug": step["slug"], "lightweight_sha256": step["lightweight_sha256"]}
             for step in stages], "approved stage provenance mismatch")
    require(b"data:image/png;base64," not in raw,
            "lightweight preview must not embed large artwork")
    return manifest


def generate(state, commit, output):
    started = time.perf_counter()
    steps = validate(state)
    require(SHA40.fullmatch(commit) and git("rev-parse", "HEAD") == commit,
            "must be exact triggering SHA")
    require(not git("status", "--porcelain"), "rehearsal worktree must be clean")
    require(not output.resolve().is_relative_to(ROOT),
            "artifact cannot be inside a repository")
    base = baseline_check(state)
    old_ptr, old_full, old_light = (POINTER.read_bytes(), FULL.read_bytes(),
                                   LIGHT.read_bytes())
    builder = runpy.run_path("gallery/tools/build-gallery.py")
    prior_sha = base["lightweight_sha256"]
    for step in steps:
        for name in ("preview_script", "approved_script"):
            p = Path(step[name])
            raw = p.read_bytes()
            require(blob(raw) == step[name + "_blob"],
                    "unapproved/tampered script: " + name)
            compile(raw, str(p), "exec")
        # Worktree only; scripts can modify approved src, never a release checkout.
        runpy.run_path(step["preview_script"], run_name="__main__")
        changed = set(filter(None, git("diff", "--name-only", "HEAD").splitlines()))
        require(changed == set(step["source_blobs"]),
                "iteration changed unexpected paths or source snapshot")
        require(not git("ls-files", "--others", "--exclude-standard"),
                "iteration created untracked files")
        for path, sha in step["source_blobs"].items():
            require(blob(Path(path).read_bytes()) == sha,
                    "candidate source Git blob mismatch: " + path)
        require(POINTER.read_bytes() == old_ptr and
                FULL.read_bytes() == old_full and
                LIGHT.read_bytes() == old_light,
                "iteration changed original release or pointer")
        artifact = builder["build"]("development")
        require(len(artifact) == step["lightweight_bytes"] and
                digest(artifact) == step["lightweight_sha256"] and
                digest(artifact) != prior_sha,
                "candidate unchanged or mismatched expected identity")
        prior_sha = digest(artifact)
    if not steps:
        artifact = builder["build"]("development")
        require(artifact == old_light, "baseline-only mode changed released lightweight")
    require(artifact == builder["build"]("development"),
            "repeated lightweight build differs")
    require(POINTER.read_bytes() == old_ptr and FULL.read_bytes() == old_full and
            LIGHT.read_bytes() == old_light, "tracked release was changed")
    require(not git("ls-files", "--others", "--exclude-standard"),
            "untracked source or release artifact")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(artifact)
    manifest = {
        "status": "Development Preview — Not a Verified Release",
        "exact_commit": commit,
        "verified_build_commit": base["verified_build_commit"],
        "baseline_sha256": base["full_sha256"],
        "baseline_checkpoint": base["checkpoint_folder"],
        "mode": state["mode"],
        "iterations": [{"slug": s["slug"], "lightweight_sha256": s["lightweight_sha256"]}
                       for s in steps],
        "lightweight_bytes": len(artifact),
        "lightweight_sha256": digest(artifact),
        "promotion_authorized": False,
        "release_changed": False,
        "preflight_seconds": round(time.perf_counter() - started, 3),
    }
    mp = output.parent / "rehearsal-manifest.json"
    mp.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n",
                  encoding="utf-8")
    # For future approved changes, verify candidate before upload in the
    # modified disposable worktree. A clean downstream job independently
    # runs full baseline verification and verifies exact artifact provenance.
    # Re-running baseline_check here against intentionally changed src would
    # incorrectly reject every non-empty approved iteration.
    if not steps:
        check_artifact(output, mp, state, commit)
    else:
        require(manifest["lightweight_sha256"] == steps[-1]["lightweight_sha256"] and
                manifest["lightweight_bytes"] == steps[-1]["lightweight_bytes"] and
                manifest["promotion_authorized"] is False,
                "approved-step candidate manifest mismatch")
    print("PASS exact G3.1 source-only rehearsal, preflight_seconds=" +
          str(manifest["preflight_seconds"]), flush=True)
    print(json.dumps(manifest, sort_keys=True), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check-artifact", type=Path)
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    state = json.loads(CONTRACT.read_text(encoding="utf-8"))
    if args.check_artifact is not None:
        require(args.output is None and args.manifest is not None,
                "artifact validation arguments")
        check_artifact(args.check_artifact, args.manifest, state, args.base)
        print("PASS exact commit and artifact provenance", flush=True)
    else:
        require(args.output is not None and args.manifest is None,
                "rehearsal output arguments")
        generate(state, args.base, args.output)


if __name__ == "__main__":
    main()
