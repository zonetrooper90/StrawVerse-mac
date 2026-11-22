#!/usr/bin/env python3
"""Fail-closed provenance validator for Gallery's durable provisional source state.

No commit, push, checkpoint, HTML publication, or modification of tracked files.
The promotion mode only renders full HTML in memory to check readiness; it is
NEVER proof of final browser regressions, release authorization or publication.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import runpy
import subprocess

PROVISIONAL = Path("gallery/development/provisional.json")
CHECKPOINT = Path("gallery/checkpoints/current.json")
FULL = Path("gallery/Gallery-current.html")
LIGHT = Path("gallery/Gallery-development.html")
SHA40 = re.compile(r"[0-9a-f]{40}")
SHA256 = re.compile(r"[0-9a-f]{64}")
SLUG = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}-[a-z0-9-]+")


def ensure(condition, detail):
    if not condition:
        raise AssertionError("Provisional contract invalid: " + detail)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()


def load_contract(path=PROVISIONAL):
    p = json.loads(path.read_text(encoding="utf-8"))
    ensure(isinstance(p, dict) and p.get("schema") == 1
           and p.get("status") == "provisional-development-not-release", "schema/status")
    b, req, candidate, promotion = (p.get(k) for k in
                                      ("baseline", "request", "candidate", "promotion"))
    ensure(all(isinstance(v, dict) for v in (b, req, candidate, promotion)), "sections")
    ensure(SHA40.fullmatch(str(b.get("verified_commit", ""))) is not None,
           "baseline commit")
    ensure(isinstance(b.get("checkpoint_folder"), str)
           and b["checkpoint_folder"] and "/" not in b["checkpoint_folder"], "checkpoint folder")
    for section, keys in ((b, ("full_sha256", "lightweight_sha256")),
                          (candidate, ("full_sha256", "lightweight_sha256"))):
        for k in keys:
            ensure(SHA256.fullmatch(str(section.get(k, ""))) is not None, k)
    for section, keys in ((b, ("full_bytes", "lightweight_bytes")),
                          (candidate, ("full_bytes", "lightweight_bytes"))):
        for k in keys:
            ensure(type(section.get(k)) is int and section[k] > 0, k)
    slug = req.get("slug")
    ensure(isinstance(slug, str) and SLUG.fullmatch(slug) is not None,
           "request slug")
    ensure(req.get("file") == "gallery/changes/previews/" + slug + ".py",
           "immutable preview request path")
    ensure(req.get("approved_request_file") == "gallery/changes/pending/" + slug + ".py",
           "immutable approved source request path")
    for k in ("git_blob_sha", "approved_request_git_blob_sha"):
        ensure(SHA40.fullmatch(str(req.get(k, ""))) is not None, k)
    changes = candidate.get("changed_source_git_blobs")
    ensure(isinstance(changes, dict) and changes
           and all(isinstance(k, str) and k.startswith("gallery/src/")
                   and ".." not in Path(k).parts and SHA40.fullmatch(str(v))
                   for k, v in changes.items()), "scoped changed-source blobs")
    ensure(promotion.get("status") == "not-approved"
           and promotion.get("promoted_commit") is None, "must not represent a release")
    return p


def check_prepared_candidate(p, preview, manifest, full_dry_run=False):
    req, candidate, baseline = p["request"], p["candidate"], p["baseline"]
    ensure(subprocess.run(["git", "merge-base", "--is-ancestor",
                           baseline["verified_commit"], "HEAD"],
                          check=False).returncode == 0, "unrelated Git history")
    ensure(blob(Path(req["file"]).read_bytes()) == req["git_blob_sha"],
           "durable preview request changed")
    ensure(blob(Path(req["approved_request_file"]).read_bytes()) ==
           req["approved_request_git_blob_sha"], "original approved request changed")
    ptr = json.loads(CHECKPOINT.read_text(encoding="utf-8"))
    ensure(ptr["folder"] == baseline["checkpoint_folder"]
           and ptr["sha256"] == baseline["full_sha256"]
           and ptr["bytes"] == baseline["full_bytes"],
           "immutable pointer advanced unexpectedly")
    full_raw = FULL.read_bytes()
    light_raw = LIGHT.read_bytes()
    ensure(digest(full_raw) == baseline["full_sha256"]
           and len(full_raw) == baseline["full_bytes"], "verified full release changed")
    ensure(digest(light_raw) == baseline["lightweight_sha256"]
           and len(light_raw) == baseline["lightweight_bytes"], "tracked lightweight changed")
    changed = git("diff", "--name-only", "HEAD").splitlines()
    ensure(set(changed) == set(candidate["changed_source_git_blobs"]), "unexpected source edits")
    for path, expected in candidate["changed_source_git_blobs"].items():
        ensure(blob(Path(path).read_bytes()) == expected, "candidate source blob: " + path)
    raw = preview.read_bytes()
    ensure(digest(raw) == candidate["lightweight_sha256"]
           and len(raw) == candidate["lightweight_bytes"], "candidate lightweight bytes")
    ensure(manifest["status"] == "Development Preview — Not a Verified Release"
           and manifest["request"] == req["slug"]
           and manifest["github_commit"] == git("rev-parse", "HEAD")
           and manifest["request_sha256"] == digest(Path(req["file"]).read_bytes())
           and manifest["lightweight_sha256"] == digest(raw)
           and manifest["lightweight_bytes"] == len(raw)
           and manifest["verified_full_baseline_sha256"] == baseline["full_sha256"]
           and manifest["immutable_checkpoint"] == baseline["checkpoint_folder"]
           and manifest["full_release_rebuilt_or_published"] is False,
           "provisional evidence mismatch")
    ensure(set(manifest["changed_source_files"]) == set(changed),
           "manifest source paths mismatch")
    if full_dry_run:
        builder = runpy.run_path("gallery/tools/build-gallery.py")
        proposed = builder["build"]("full")
        ensure(digest(proposed) == candidate["full_sha256"]
               and len(proposed) == candidate["full_bytes"],
               "candidate full HTML differs from approved source snapshot")
        ensure(builder["build"]("subtitle-preview") == proposed,
               "full and artwork preview differ")
        ensure(builder["build"]("development") == raw, "full/preview source mismatch")
        ensure(FULL.read_bytes() == full_raw and LIGHT.read_bytes() == light_raw,
               "promotion preflight unexpectedly changed tracked HTML")
    return {
        "status": "PROVISIONAL, NOT PUBLISHED",
        "request": req["slug"],
        "source_files": changed,
        "lightweight_sha256": digest(raw),
        "full_dry_run_checked": full_dry_run,
        "full_candidate_sha256": candidate["full_sha256"] if full_dry_run else None,
        "release_pointer_unchanged": True,
        "promotion_authorized": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request", required=True)
    parser.add_argument("--preview", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--promotion-dry-run", action="store_true")
    args = parser.parse_args()
    p = load_contract()
    ensure(args.request == p["request"]["slug"], "wrong approved provisional request")
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    result = check_prepared_candidate(p, args.preview, manifest, args.promotion_dry_run)
    print("PASS exact provisional source contract:", json.dumps(result, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
