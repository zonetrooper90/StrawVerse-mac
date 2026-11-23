#!/usr/bin/env python3
"""Read-only dynamic exact-build Gallery regression shards, NOT a release gate.

The full/lightweight bytes and checkpoint are derived from this exact commit,
never from the fixed G3.1 baseline. Original browser tests and two mandatory
independent postpublication workflows remain protected and unchanged.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import runpy
import subprocess

ROOT = Path(__file__).resolve().parents[2]
CFG = ROOT / "gallery/development/release-regression-shards.json"
ORIGINAL = ROOT / ".github/workflows/gallery-transition-ui.yml"
INTEGRITY = ROOT / ".github/workflows/gallery-checkpoint-integrity.yml"
MANIFEST = ROOT / "gallery/src/build-manifest.json"
POINTER = ROOT / "gallery/checkpoints/current.json"
FULL = ROOT / "gallery/Gallery-current.html"
LIGHT = ROOT / "gallery/Gallery-development.html"
SHA40 = re.compile(r"[0-9a-f]{40}\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")
SUITES = {
    "transitions": "gallery/tests/test_transitions.py",
    "coordinated-fades": "gallery/tests/test_coordinated_fades.py",
    "history-row-maintenance": "gallery/tests/test_history_row_maintenance.py",
    "player-settings-regression": "gallery/tests/test_player_settings_regression.py",
    "subtitle-preview-modes": "gallery/tests/test_asset_build_modes.py",
}
STANDARD = tuple(k for k in SUITES if k != "subtitle-preview-modes")
MATRIX = [{"mode": mode, "suite": suite} for mode in ("full", "lightweight")
          for suite in STANDARD] + [{"mode": "both", "suite": "subtitle-preview-modes"}]
IDENTITY_FIELDS = (
    "commit", "checkpoint_folder", "checkpoint_sha256", "checkpoint_bytes",
    "pointer_blob", "full_sha256", "full_bytes", "lightweight_sha256",
    "lightweight_bytes", "manifest_blob", "original_workflow_blob",
    "integrity_workflow_blob",
)
PROOF_FIELDS = {
    "status", "identity", "mode", "suite", "test_blob", "run_id",
    "run_attempt", "script_seconds", "promotion_authorized",
}

def require(ok, message):
    if not ok:
        raise AssertionError("Gallery exact-build shard trial: " + message)

def sha256(raw):
    return hashlib.sha256(raw).hexdigest()

def git_blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True).strip()

def validate(cfg):
    require(isinstance(cfg, dict) and set(cfg) == {
        "schema", "status", "baseline_ancestor", "original_workflow_blob",
        "integrity_workflow_blob", "immutable_test_blobs", "matrix", "promotion"
    }, "unexpected or missing contract keys")
    require(type(cfg["schema"]) is int and cfg["schema"] == 1, "schema")
    require(cfg["status"] ==
            "read-only-dynamic-exact-build-regression-trial-not-release",
            "trial must never be promoted")
    for key in ("baseline_ancestor", "original_workflow_blob",
                "integrity_workflow_blob"):
        require(isinstance(cfg[key], str) and SHA40.fullmatch(cfg[key]),
                "invalid Git object identity " + key)
    require(isinstance(cfg["immutable_test_blobs"], dict) and
            set(cfg["immutable_test_blobs"]) == set(SUITES.values()) and
            all(isinstance(v, str) and SHA40.fullmatch(v)
                for v in cfg["immutable_test_blobs"].values()),
            "missing or modified original test coverage")
    require(cfg["matrix"] == MATRIX, "incomplete, changed or reordered matrix")
    require(cfg["promotion"] == {"status": "not-authorized",
                                 "published_commit": None},
            "cannot promote a trial to a release")
    return cfg

def verify_source(cfg, commit):
    validate(cfg)
    require(isinstance(commit, str) and SHA40.fullmatch(commit),
            "invalid exact commit")
    require(git("rev-parse", "HEAD") == commit, "checkout differs from triggering SHA")
    require(git("status", "--porcelain") == "", "checkout has dirty files")
    ancestry = subprocess.run(
        ["git", "-C", str(ROOT), "merge-base", "--is-ancestor",
         cfg["baseline_ancestor"], "HEAD"], check=False)
    require(ancestry.returncode == 0, "build does not descend from approved G3.1")
    require(git_blob(ORIGINAL.read_bytes()) == cfg["original_workflow_blob"],
            "original mandatory browser workflow changed")
    require(git_blob(INTEGRITY.read_bytes()) == cfg["integrity_workflow_blob"],
            "independent mandatory checkpoint workflow changed")
    original = ORIGINAL.read_text(encoding="utf-8")
    found = re.findall(r"\bpython3 gallery/tests/(test_[a-z_]+\.py)\b", original)
    expected = [Path(SUITES[k]).name for k in SUITES]
    require(found == expected and "fail-fast: false" in original and
            "subtitle-preview-modes" in original,
            "original mandatory suite order or mode coverage changed")
    for path, blob in cfg["immutable_test_blobs"].items():
        require(git_blob((ROOT / path).read_bytes()) == blob,
                "original test script changed; requires separate review: " + path)

    pointer = json.loads(POINTER.read_text(encoding="utf-8"))
    require(isinstance(pointer, dict) and
            {"folder", "bytes", "sha256"} <= set(pointer),
            "missing checkpoint fields")
    require(isinstance(pointer["folder"], str) and
            re.fullmatch(r"[0-9a-z][0-9a-z-]*", pointer["folder"]),
            "invalid checkpoint folder path")
    require(type(pointer["bytes"]) is int and pointer["bytes"] > 0 and
            isinstance(pointer["sha256"], str) and
            SHA256.fullmatch(pointer["sha256"]), "invalid checkpoint digest or size")
    full, light = FULL.read_bytes(), LIGHT.read_bytes()
    require(len(full) == pointer["bytes"] and
            sha256(full) == pointer["sha256"],
            "current full build differs from immutable checkpoint")
    checkpoint_api = runpy.run_path(str(ROOT / "gallery/tools/restore-checkpoint.py"))
    restored, _, restored_pointer = checkpoint_api["restore"]()
    require(restored == full and restored_pointer == pointer,
            "immutable archive does not reproduce current HTML")
    builder = runpy.run_path(str(ROOT / "gallery/tools/build-gallery.py"))
    builder["check"]()  # BOTH current HTML modes and assets, byte exact, no writes
    require(git("status", "--porcelain") == "", "verification modified checkout")

    identity = {
        "commit": commit,
        "checkpoint_folder": pointer["folder"],
        "checkpoint_sha256": pointer["sha256"],
        "checkpoint_bytes": pointer["bytes"],
        "pointer_blob": git_blob(POINTER.read_bytes()),
        "full_sha256": sha256(full),
        "full_bytes": len(full),
        "lightweight_sha256": sha256(light),
        "lightweight_bytes": len(light),
        "manifest_blob": git_blob(MANIFEST.read_bytes()),
        "original_workflow_blob": cfg["original_workflow_blob"],
        "integrity_workflow_blob": cfg["integrity_workflow_blob"],
    }
    require(set(identity) == set(IDENTITY_FIELDS), "release identity incomplete")
    require(identity["full_sha256"] == identity["checkpoint_sha256"],
            "published full build is not checkpointed")
    print("PASS dynamic exact-commit dual-build reconstruction, original tests, "
          "archived full checkpoint and unmodified mandatory verifiers.", flush=True)
    print("Build identity:", json.dumps(identity, sort_keys=True), flush=True)
    return identity

def proof(cfg, identity, mode, suite, seconds, run_id, attempt):
    validate(cfg)
    require(set(identity) == set(IDENTITY_FIELDS),
            "incomplete commit-specific identity")
    require({"mode": mode, "suite": suite} in MATRIX, "unknown suite/mode")
    require(type(seconds) is int and 0 <= seconds <= 3600,
            "invalid original test duration")
    require(type(run_id) is int and run_id > 0 and
            type(attempt) is int and attempt > 0,
            "invalid Actions run/attempt")
    return {
        "status": "passed-original-unchanged-browser-test-not-release",
        "identity": identity,
        "mode": mode,
        "suite": suite,
        "test_blob": cfg["immutable_test_blobs"][SUITES[suite]],
        "run_id": run_id,
        "run_attempt": attempt,
        "script_seconds": seconds,
        "promotion_authorized": False,
    }

def verify_proof(cfg, identity, data, mode, suite, run_id, attempt):
    require(isinstance(data, dict) and set(data) == PROOF_FIELDS,
            "invalid proof schema")
    seconds = data["script_seconds"]
    require(type(seconds) is int and 0 <= seconds <= 3600,
            "invalid duration")
    expect = proof(cfg, identity, mode, suite, seconds, run_id, attempt)
    require(data == expect, "proof identity, exact job or test result mismatch")
    return seconds

def aggregate_proofs(cfg, identity, folder, run_id, attempt):
    validate(cfg)
    expected = {e["mode"] + "-" + e["suite"] + ".json": e for e in MATRIX}
    observed = {p.name: p for p in folder.glob("*.json")}
    require(set(observed) == set(expected),
            "missing/extra/duplicate original suite proof")
    durations = {}
    for filename, entry in expected.items():
        data = json.loads(observed[filename].read_text(encoding="utf-8"))
        mode, suite = entry["mode"], entry["suite"]
        durations[mode + "/" + suite] = verify_proof(
            cfg, identity, data, mode, suite, run_id, attempt)
    full_serial = sum(durations["full/" + k] for k in STANDARD)
    light_serial = sum(durations["lightweight/" + k] for k in STANDARD)
    parallel = max(*(durations["full/" + k] for k in STANDARD),
                   *(durations["lightweight/" + k] for k in STANDARD),
                   durations["both/subtitle-preview-modes"])
    summary = {
        "status": "PASS all nine unchanged exact-build browser scripts; trial only",
        "identity": identity,
        "run_id": run_id,
        "run_attempt": attempt,
        "proofs": len(durations),
        "script_seconds_by_shard": durations,
        "modeled_serial_full_seconds": full_serial,
        "modeled_serial_lightweight_seconds": light_serial,
        "modeled_total_script_seconds": full_serial + light_serial +
                                        durations["both/subtitle-preview-modes"],
        "modeled_parallel_critical_script_seconds": parallel,
        "promotion_authorized": False,
    }
    print(json.dumps(summary, indent=2, sort_keys=True), flush=True)
    return summary

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--exact-commit", required=True)
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--verify", action="store_true")
    group.add_argument("--record", action="store_true")
    group.add_argument("--aggregate", type=Path)
    ap.add_argument("--mode")
    ap.add_argument("--suite")
    ap.add_argument("--seconds", type=int)
    ap.add_argument("--output", type=Path)
    ap.add_argument("--run-id", type=int)
    ap.add_argument("--run-attempt", type=int)
    args = ap.parse_args()
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    identity = verify_source(cfg, args.exact_commit)
    if args.verify:
        require(args.mode is None and args.suite is None and
                args.seconds is None and args.output is None and
                args.run_id is None and args.run_attempt is None,
                "verify accepts no proof parameters")
    elif args.record:
        require(args.mode and args.suite and args.seconds is not None and
                args.output is not None and args.run_id and args.run_attempt,
                "record input incomplete")
        dest = args.output.resolve()
        require(not dest.is_relative_to(ROOT), "proof must be outside Git checkout")
        require(dest.name == args.mode + "-" + args.suite + ".json",
                "mismatched shard proof filename")
        entry = proof(cfg, identity, args.mode, args.suite, args.seconds,
                      args.run_id, args.run_attempt)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(entry, sort_keys=True) + "\n", encoding="utf-8")
        print("PASS original", args.mode, args.suite,
              "for exact commit", args.exact_commit, flush=True)
    else:
        require(args.mode is None and args.suite is None and
                args.seconds is None and args.output is None and
                args.run_id and args.run_attempt,
                "aggregate input incomplete")
        aggregate_proofs(cfg, identity, args.aggregate,
                         args.run_id, args.run_attempt)
    require(git("status", "--porcelain") == "", "tool modified repository")

if __name__ == "__main__":
    main()
