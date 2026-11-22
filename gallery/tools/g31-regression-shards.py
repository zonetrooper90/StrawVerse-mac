#!/usr/bin/env python3
"""Read-only, nine-shard rehearsal of the unchanged mandatory Gallery browser suite.

This workflow neither replaces gallery-transition-ui.yml nor authorizes release,
lightweight-only development or changing the original tests. The exact original
suite list and Git blobs must match a checked-in contract before Chromium runs.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import runpy
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "gallery/development/g31-regression-shards.json"
BASELINE = ROOT / "gallery/development/verified-baseline.json"
ORIGINAL = ROOT / ".github/workflows/gallery-transition-ui.yml"
SHA40 = re.compile(r"[0-9a-f]{40}\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")
SUITE_FILES = {
    "transitions": "gallery/tests/test_transitions.py",
    "coordinated-fades": "gallery/tests/test_coordinated_fades.py",
    "history-row-maintenance": "gallery/tests/test_history_row_maintenance.py",
    "player-settings-regression": "gallery/tests/test_player_settings_regression.py",
    "subtitle-preview-modes": "gallery/tests/test_asset_build_modes.py",
}
MODE_SUITES = tuple(k for k in SUITE_FILES if k != "subtitle-preview-modes")
MATRIX = [{"mode": mode, "suite": suite}
          for mode in ("full", "lightweight") for suite in MODE_SUITES] + [
          {"mode": "both", "suite": "subtitle-preview-modes"}]
EXPECTED_FILES = [SUITE_FILES[k] for k in MODE_SUITES] + [
    SUITE_FILES["subtitle-preview-modes"]]


def require(ok, message):
    if not ok:
        raise AssertionError("Gallery strict shard rehearsal: " + message)


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def git_blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args],
                                   text=True).strip()


def validate(cfg):
    require(isinstance(cfg, dict) and set(cfg) ==
            {"schema", "status", "baseline_build_commit",
             "verified_baseline_blob", "original_workflow_blob",
             "baseline_browser_run", "immutable_test_blobs", "matrix",
             "promotion"}, "schema has missing/extra fields")
    require(type(cfg["schema"]) is int and cfg["schema"] == 1 and
            cfg["status"] == "read-only-regression-sharding-benchmark-not-release",
            "schema and purpose")
    require(all(type(cfg[k]) is str and SHA40.fullmatch(cfg[k]) for k in
                ("baseline_build_commit", "verified_baseline_blob",
                 "original_workflow_blob")), "exact Git object identities")
    require(type(cfg["baseline_browser_run"]) is int and
            cfg["baseline_browser_run"] > 0, "original browser reference")
    require(isinstance(cfg["immutable_test_blobs"], dict) and
            set(cfg["immutable_test_blobs"]) == set(SUITE_FILES.values()) and
            all(type(v) is str and SHA40.fullmatch(v) for v in
                cfg["immutable_test_blobs"].values()), "complete pinned suite blobs")
    require(cfg["matrix"] == MATRIX, "coverage missing, duplicated, reordered or reduced")
    require(cfg["promotion"] ==
            {"status": "not-authorized", "published_commit": None},
            "no release or workflow cutover authorization")
    return cfg


def verify_source(cfg, commit):
    validate(cfg)
    require(isinstance(commit, str) and SHA40.fullmatch(commit) and
            git("rev-parse", "HEAD") == commit, "exact triggering commit")
    require(not git("status", "--porcelain"), "source checkout is not clean")
    require(git("merge-base", "--is-ancestor",
                cfg["baseline_build_commit"], "HEAD") == "",
            "cannot confirm verified build ancestry")
    require(git_blob(BASELINE.read_bytes()) == cfg["verified_baseline_blob"],
            "G3.1 baseline record changed")
    require(git_blob(ORIGINAL.read_bytes()) == cfg["original_workflow_blob"],
            "original mandatory workflow changed; stop and re-review coverage")
    source = ORIGINAL.read_text(encoding="utf-8")
    found = re.findall(r"\bpython3 gallery/tests/(test_[a-z_]+\.py)\b", source)
    require(found == [Path(p).name for p in EXPECTED_FILES],
            "exact mandatory test command list/order changed")
    require("browser-routes" in source and "subtitle-preview-modes" in source and
            "fail-fast: false" in source, "original browser matrix changed")
    for path, expected in cfg["immutable_test_blobs"].items():
        require(git_blob((ROOT / path).read_bytes()) == expected,
                "original suite code changed: " + path)
    base = json.loads(BASELINE.read_text(encoding="utf-8"))
    require(cfg["baseline_build_commit"] == base["baseline"]["verified_build_commit"],
            "pinned G3.1 release identity differs")
    baseline_api = runpy.run_path(str(ROOT / "gallery/tools/verify-development-baseline.py"))
    baseline_api["verify"](base)
    print("PASS all 9 exact original browser suite/mode combinations, immutable "
          "G3.1 baseline and release artifacts, no missing coverage.", flush=True)
    return base["baseline"]


def record(cfg, commit, mode, suite, seconds, output):
    base = verify_source(cfg, commit)
    require({"mode": mode, "suite": suite} in MATRIX, "unrecognized shard")
    require(type(seconds) is int and 0 <= seconds <= 3600,
            "unreasonable duration")
    require(not output.resolve().is_relative_to(ROOT), "proof may not be inside Git")
    ident = mode + "-" + suite
    require(output.name == ident + ".json", "proof filename must match shard")
    data = {"status": "passed-read-only-benchmark",
            "exact_commit": commit,
            "baseline_commit": base["verified_build_commit"],
            "mode": mode, "suite": suite,
            "test_blob": cfg["immutable_test_blobs"][SUITE_FILES[suite]],
            "html_sha256": (base["full_sha256"] if mode == "full"
                            else base["lightweight_sha256"] if mode == "lightweight"
                            else "both-modes-verified-by-original-test"),
            "script_seconds": seconds,
            "promotion_authorized": False}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, sort_keys=True) + "\n", encoding="utf-8")
    print("PASS benchmark shard provenance: " + ident + " " + str(seconds) + "s",
          flush=True)


def aggregate(cfg, commit, folder):
    base = verify_source(cfg, commit)
    expected = {m["mode"] + "-" + m["suite"] + ".json": m for m in MATRIX}
    observed = {p.name: p for p in folder.glob("*.json")}
    require(set(observed) == set(expected), "all nine unique passing proof files required")
    results = {}
    for name, entry in expected.items():
        data = json.loads(observed[name].read_text(encoding="utf-8"))
        require(isinstance(data, dict) and set(data) ==
                {"status", "exact_commit", "baseline_commit", "mode", "suite",
                 "test_blob", "html_sha256", "script_seconds",
                 "promotion_authorized"}, "shard proof schema")
        mode, suite = entry["mode"], entry["suite"]
        require(data["status"] == "passed-read-only-benchmark" and
                data["exact_commit"] == commit and
                data["baseline_commit"] == base["verified_build_commit"] and
                data["mode"] == mode and data["suite"] == suite and
                data["test_blob"] == cfg["immutable_test_blobs"][SUITE_FILES[suite]]
                and data["html_sha256"] ==
                (base["full_sha256"] if mode == "full" else
                 base["lightweight_sha256"] if mode == "lightweight" else
                 "both-modes-verified-by-original-test") and
                type(data["script_seconds"]) is int and
                0 <= data["script_seconds"] <= 3600 and
                data["promotion_authorized"] is False,
                "invalid or mismatched shard result: " + name)
        results[mode + "/" + suite] = data["script_seconds"]
    full_serial = sum(results["full/" + s] for s in MODE_SUITES)
    light_serial = sum(results["lightweight/" + s] for s in MODE_SUITES)
    full_parallel = max(results["full/" + s] for s in MODE_SUITES)
    light_parallel = max(results["lightweight/" + s] for s in MODE_SUITES)
    subtitle = results["both/subtitle-preview-modes"]
    summary = {
        "status": "PASS: read-only coverage-preserving sharding rehearsal, not release",
        "exact_commit": commit,
        "suite_shards": len(results),
        "script_seconds_by_shard": results,
        "modeled_serial_full_seconds": full_serial,
        "modeled_serial_lightweight_seconds": light_serial,
        "modeled_parallel_full_seconds": full_parallel,
        "modeled_parallel_lightweight_seconds": light_parallel,
        "modeled_total_script_seconds_all_shards": full_serial + light_serial + subtitle,
        "modeled_parallel_critical_script_seconds": max(full_parallel, light_parallel,
                                                         subtitle),
        "warning": "Script-time model only; runner startup, Chromium, queueing, "
                   "contention and comparison against the original CI run must be "
                   "assessed separately. No existing mandatory gates replaced.",
        "promotion_authorized": False}
    print(json.dumps(summary, indent=2, sort_keys=True), flush=True)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--record", action="store_true")
    parser.add_argument("--aggregate", type=Path)
    parser.add_argument("--mode")
    parser.add_argument("--suite")
    parser.add_argument("--seconds", type=int)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    cfg = json.loads(CONTRACT.read_text(encoding="utf-8"))
    require(sum([args.verify, args.record, args.aggregate is not None]) == 1,
            "choose exactly one mode")
    if args.record:
        require(args.mode and args.suite and args.seconds is not None and args.output,
                "proof request incomplete")
        record(cfg, args.base, args.mode, args.suite, args.seconds, args.output)
    elif args.aggregate is not None:
        require(not args.mode and not args.suite and args.output is None,
                "aggregate cannot publish")
        aggregate(cfg, args.base, args.aggregate)
    else:
        require(not args.mode and not args.suite and args.output is None,
                "preflight-only inputs")
        verify_source(cfg, args.base)


if __name__ == "__main__":
    main()
