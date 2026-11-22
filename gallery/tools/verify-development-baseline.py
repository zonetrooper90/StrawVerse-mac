#!/usr/bin/env python3
"""Read-only exact G3.1 development-baseline reconciliation.

This is a baseline reference for FUTURE lightweight development, not a preview
or release promotion. Never write source, release HTML, pointers, or archives.
"""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "gallery/development/verified-baseline.json"
SHA40 = re.compile(r"[0-9a-f]{40}\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")
FULL = "gallery/Gallery-current.html"
LIGHT = "gallery/Gallery-development.html"
POINTER = "gallery/checkpoints/current.json"
SOURCES = ("gallery/src/build-manifest.json",
           "gallery/src/styles/28-unified-headers-and-history-frame.css")
HISTORICAL = ("gallery/development/provisional.json",
              "gallery/development/iterations.json")


def require(ok, why):
    if not ok:
        raise AssertionError("G3.1 read-only baseline: " + why)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def git_blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def git(*args, check=True):
    return subprocess.run(["git", "-C", str(ROOT), *args],
                          check=check, capture_output=True, text=True)


def validate(contract):
    require(isinstance(contract, dict) and set(contract) ==
            {"schema", "status", "baseline", "release_blobs",
             "source_blobs", "checkpoint_manifest_blob",
             "historical_contract_blobs", "verified_runs", "promotion"},
            "unexpected contract schema keys")
    require(type(contract["schema"]) is int and contract["schema"] == 1
            and contract["status"] == "verified-development-baseline-not-release-promotion",
            "contract schema/status")
    base = contract["baseline"]
    require(isinstance(base, dict) and set(base) ==
            {"verified_build_commit", "checkpoint_folder", "full_sha256",
             "full_bytes", "lightweight_sha256", "lightweight_bytes"},
            "baseline schema")
    require(isinstance(base["verified_build_commit"], str) and
            SHA40.fullmatch(base["verified_build_commit"]), "exact build commit")
    require(type(base["checkpoint_folder"]) is str and
            re.fullmatch(r"20[0-9]{2}-[0-9]{2}-[0-9]{2}-[a-z0-9-]+",
                         base["checkpoint_folder"]), "checkpoint folder")
    for key in ("full", "lightweight"):
        require(isinstance(base[key + "_sha256"], str) and
                SHA256.fullmatch(base[key + "_sha256"]) and
                type(base[key + "_bytes"]) is int and
                base[key + "_bytes"] > 0, key + " exact artifact dimensions")
    for section, paths in (("release_blobs", (FULL, LIGHT)),
                           ("source_blobs", SOURCES),
                           ("historical_contract_blobs", HISTORICAL)):
        values = contract[section]
        require(isinstance(values, dict) and set(values) == set(paths)
                and all(isinstance(v, str) and SHA40.fullmatch(v)
                        for v in values.values()), section + " fixed paths/blobs")
    require(isinstance(contract["checkpoint_manifest_blob"], str) and
            SHA40.fullmatch(contract["checkpoint_manifest_blob"]),
            "immutable checkpoint manifest")
    runs = contract["verified_runs"]
    require(isinstance(runs, dict) and set(runs) ==
            {"publisher", "checkpoint_integrity", "full_lightweight_browser"}
            and all(type(v) is int and v > 0 for v in runs.values()),
            "exact known verified workflow identifiers")
    require(contract["promotion"] ==
            {"status": "not-authorized", "published_commit": None},
            "this rehearsal must not authorize a release")
    return base


def verify(contract):
    base = validate(contract)
    require(git("rev-parse", "HEAD").stdout.strip() != "",
            "missing exact HEAD")
    require(git("merge-base", "--is-ancestor",
                base["verified_build_commit"], "HEAD", check=False).returncode == 0,
            "verified build commit is not an ancestor")
    # Old G3 development contracts are historical snapshots, not the current release.
    for section in ("historical_contract_blobs", "release_blobs", "source_blobs"):
        for filename, expected in contract[section].items():
            path = ROOT / filename
            require(path.is_file() and git_blob(path.read_bytes()) == expected,
                    "unexpected mutation: " + filename)
    old_contract = json.loads((ROOT / HISTORICAL[0]).read_text(encoding="utf-8"))
    old_steps = json.loads((ROOT / HISTORICAL[1]).read_text(encoding="utf-8"))
    require(old_contract["baseline"] == old_steps["baseline"]
            and old_contract["promotion"]["status"] == "not-approved"
            and old_steps["promotion"]["status"] == "not-approved",
            "historical G3 preview metadata rewritten")
    pointer = json.loads((ROOT / POINTER).read_text(encoding="utf-8"))
    require(all(pointer[key] == base[value] for key, value in
                (("folder", "checkpoint_folder"), ("bytes", "full_bytes"),
                 ("sha256", "full_sha256"))), "active immutable release pointer differs")
    archive_manifest_path = (
        ROOT / "gallery/checkpoints" / base["checkpoint_folder"] / "manifest.json"
    )
    require(archive_manifest_path.is_file() and
            git_blob(archive_manifest_path.read_bytes()) ==
            contract["checkpoint_manifest_blob"],
            "immutable checkpoint manifest changed")
    manifest = json.loads(archive_manifest_path.read_text(encoding="utf-8"))
    require(manifest["checkpoint"] == base["checkpoint_folder"] and
            manifest["source_bytes"] == base["full_bytes"] and
            manifest["source_sha256"] == base["full_sha256"],
            "immutable checkpoint manifest provenance")
    for path, key in ((FULL, "full"), (LIGHT, "lightweight")):
        raw = (ROOT / path).read_bytes()
        require(len(raw) == base[key + "_bytes"] and
                digest(raw) == base[key + "_sha256"],
                "verified build drift: " + path)
    # Existing independent safeguards remain operational, not replaced by this audit.
    for command in (("gallery/tools/restore-checkpoint.py", "--verify-only"),
                    ("gallery/tools/build-gallery.py", "--check")):
        subprocess.run([sys.executable, "-B", str(ROOT / command[0]),
                        *command[1:]], cwd=ROOT, check=True)
    print("PASS G3.1 exact published source/HTML/immutable checkpoint, "
          "historical G3 provisional records preserved; no release promotion.")
    return True


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true", required=True)
    args = parser.parse_args()
    require(args.verify, "explicit read-only verification required")
    verify(json.loads(CONTRACT.read_text(encoding="utf-8")))


if __name__ == "__main__":
    main()
