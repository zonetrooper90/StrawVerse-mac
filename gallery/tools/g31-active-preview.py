#!/usr/bin/env python3
"""Guarded G3.1 lightweight source previews. Never publishes a release."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import runpy
import subprocess
import time

ROOT = Path.cwd().resolve()
CONTRACT = Path("gallery/development/g31-active-preview.json")
BASELINE = Path("gallery/development/verified-baseline.json")
POINTER = Path("gallery/checkpoints/current.json")
FULL = Path("gallery/Gallery-current.html")
LIGHT = Path("gallery/Gallery-development.html")
DECISIONS = Path("gallery/APPROVED-DECISIONS.md")
SHA40 = re.compile(r"[0-9a-f]{40}\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")
SLUG = re.compile(r"20\d\d-\d\d-\d\d-[a-z0-9-]+\Z")


def must(value, description):
    if not value:
        raise AssertionError("G3.1 preview: " + description)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()


def validate(s):
    must(type(s) is dict and set(s) ==
         {"schema", "status", "baseline_ref", "baseline_git_blob",
          "mode", "steps", "promotion"}, "contract keys")
    must(type(s["schema"]) is int and s["schema"] == 1 and
         s["status"] == "g31-source-preview-not-release", "contract version")
    must(s["baseline_ref"] == str(BASELINE) and
         type(s["baseline_git_blob"]) is str and
         SHA40.fullmatch(s["baseline_git_blob"]), "verified baseline pin")
    must(s["promotion"] == {"status": "not-authorized", "published_commit": None},
         "publication forbidden")
    steps = s["steps"]
    must(type(steps) is list and len(steps) <= 8 and
         ((not steps and s["mode"] == "baseline-only") or
          (bool(steps) and s["mode"] == "approved-source-only")),
         "approved preview mode")
    seen = set()
    for x in steps:
        must(type(x) is dict and set(x) ==
             {"slug", "script", "script_blob", "approval_heading", "source_blobs",
              "preview_sha256", "preview_bytes"}, "step schema")
        slug = x["slug"]
        must(type(slug) is str and SLUG.fullmatch(slug) and slug not in seen,
             "unique dated slug")
        seen.add(slug)
        must(x["script"] == "gallery/development/preview-scripts/" + slug + ".py" and
             type(x["script_blob"]) is str and SHA40.fullmatch(x["script_blob"]),
             "immutable preview script")
        must(type(x["approval_heading"]) is str and
             re.fullmatch(r"## 20\d\d-\d\d-\d\d . Approved [^\n]+",
                          x["approval_heading"]), "recorded user approval heading")
        src = x["source_blobs"]
        must(type(src) is dict and 1 <= len(src) <= 128,
             "nonempty exact source snapshot")
        for path, checksum in src.items():
            must(type(path) is str and path.startswith("gallery/src/") and
                 ".." not in Path(path).parts and
                 Path(path).suffix in (".html", ".css", ".js", ".json") and
                 type(checksum) is str and SHA40.fullmatch(checksum),
                 "allowed source path/blob")
        must(type(x["preview_sha256"]) is str and
             SHA256.fullmatch(x["preview_sha256"]) and
             type(x["preview_bytes"]) is int and x["preview_bytes"] > 0,
             "exact preview checksum and size")
    return steps


def baseline(s):
    must(blob(BASELINE.read_bytes()) == s["baseline_git_blob"],
         "baseline reference modified")
    data = json.loads(BASELINE.read_text())
    runpy.run_path("gallery/tools/verify-development-baseline.py")["verify"](data)
    return data["baseline"]


def check_commit(commit):
    must(type(commit) is str and SHA40.fullmatch(commit) and
         git("rev-parse", "HEAD") == commit, "exact triggering commit")
    must(not git("status", "--porcelain"), "dirty exact-commit checkout")


def expected(base, steps):
    return (steps[-1]["preview_sha256"], steps[-1]["preview_bytes"]) if steps else (
        base["lightweight_sha256"], base["lightweight_bytes"])


def make_manifest(commit, state, base, html, elapsed):
    return {"status": "Development Preview — Not a Verified Release",
            "exact_commit": commit, "contract_blob": blob(CONTRACT.read_bytes()),
            "verified_build_commit": base["verified_build_commit"],
            "checkpoint_folder": base["checkpoint_folder"],
            "full_sha256": base["full_sha256"],
            "mode": state["mode"],
            "steps": [{"slug": x["slug"], "script_blob": x["script_blob"],
                       "preview_sha256": x["preview_sha256"]}
                      for x in state["steps"]],
            "preview_bytes": len(html), "preview_sha256": digest(html),
            "promotion_authorized": False, "release_changed": False,
            "preflight_seconds": elapsed}


def generate(commit, state, output):
    start = time.perf_counter()
    steps = validate(state)
    check_commit(commit)
    must(not output.resolve().is_relative_to(ROOT),
         "preview output must be outside checkout")
    base = baseline(state)
    old = (POINTER.read_bytes(), FULL.read_bytes(), LIGHT.read_bytes())
    decisions = DECISIONS.read_text(encoding="utf-8")
    build = runpy.run_path("gallery/tools/build-gallery.py")["build"]
    previous = base["lightweight_sha256"]
    for step in steps:
        must(decisions.splitlines().count(step["approval_heading"]) == 1,
             "separate explicit user approval not recorded")
        script = Path(step["script"])
        raw = script.read_bytes()
        must(blob(raw) == step["script_blob"], "changed script Git blob")
        compile(raw, str(script), "exec")
        runpy.run_path(str(script), run_name="__main__")
        changed = set(filter(None, git("diff", "--name-only", "HEAD").splitlines()))
        must(changed == set(step["source_blobs"]), "unapproved modified files")
        must(not git("ls-files", "--others", "--exclude-standard"),
             "untracked files created")
        for path, sha in step["source_blobs"].items():
            must(Path(path).is_file() and blob(Path(path).read_bytes()) == sha,
                 "source Git blob mismatch")
        must((POINTER.read_bytes(), FULL.read_bytes(), LIGHT.read_bytes()) == old and
             DECISIONS.read_text(encoding="utf-8") == decisions,
             "published release or approvals changed")
        html = build("development")
        must((digest(html), len(html)) == (step["preview_sha256"],
                                           step["preview_bytes"]) and
             digest(html) != previous, "source preview identity differs")
        previous = digest(html)
    if not steps:
        html = build("development")
        must(html == old[2], "baseline-only preview is not original lightweight")
    must(html == build("development"), "non-deterministic build")
    must((POINTER.read_bytes(), FULL.read_bytes(), LIGHT.read_bytes()) == old,
         "original release/checkpoint touched")
    must(not git("ls-files", "--others", "--exclude-standard"),
         "untracked files in worktree")
    must(b"data:image/png;base64," not in html, "lightweight preview embeds PNG")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(html)
    manifest = make_manifest(commit, state, base, html,
                             round(time.perf_counter() - start, 3))
    (output.parent / "preview-manifest.json").write_text(
        json.dumps(manifest, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    must(output.read_bytes() == html, "artifact read-back")
    print("PASS guarded G3.1 lightweight candidate; no publication")
    print(json.dumps(manifest, sort_keys=True))


def check_artifact(commit, state, html_path, manifest_path):
    steps = validate(state)
    check_commit(commit)
    base = baseline(state)
    html = html_path.read_bytes()
    must((digest(html), len(html)) == expected(base, steps),
         "candidate is not exact approved lightweight build")
    must(b"data:image/png;base64," not in html, "embedded artwork")
    manifest = json.loads(manifest_path.read_text())
    elapsed = manifest.get("preflight_seconds")
    must(type(elapsed) in (int, float) and elapsed >= 0 and
         manifest == make_manifest(commit, state, base, html, elapsed),
         "stale or tampered manifest/commit")
    print("PASS exact GitHub commit, checkpoint and preview provenance")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--base", required=True)
    p.add_argument("--output", type=Path)
    p.add_argument("--check-artifact", type=Path)
    p.add_argument("--manifest", type=Path)
    a = p.parse_args()
    state = json.loads(CONTRACT.read_text())
    if a.output is not None:
        must(a.check_artifact is None and a.manifest is None, "generation arguments")
        generate(a.base, state, a.output)
    else:
        must(a.check_artifact is not None and a.manifest is not None,
             "verification arguments")
        check_artifact(a.base, state, a.check_artifact, a.manifest)


if __name__ == "__main__":
    main()
