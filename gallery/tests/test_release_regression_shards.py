#!/usr/bin/env python3
"""Fail-closed negative tests for dynamic exact-build 9-way read-only sharding."""
import copy
import json
from pathlib import Path
import runpy
import subprocess
import tempfile

api = runpy.run_path("gallery/tools/release-regression-shards.py")
cfg = json.loads(Path("gallery/development/release-regression-shards.json").read_text())
api["validate"](cfg)
matrix = api["MATRIX"]
assert len(matrix) == len({(x["mode"], x["suite"]) for x in matrix}) == 9
assert {x["mode"] for x in matrix} == {"full", "lightweight", "both"}

def reject_cfg(change):
    c = copy.deepcopy(cfg)
    change(c)
    try:
        api["validate"](c)
    except (AssertionError, TypeError, ValueError, KeyError):
        return
    raise AssertionError("unsafe configuration accepted")

reject_cfg(lambda c: c.update(schema=2))
reject_cfg(lambda c: c.update(status="mandatory-release"))
reject_cfg(lambda c: c["promotion"].update(status="authorized"))
reject_cfg(lambda c: c["promotion"].update(published_commit="0" * 40))
reject_cfg(lambda c: c["matrix"].pop())
reject_cfg(lambda c: c["matrix"].append(copy.deepcopy(c["matrix"][0])))
reject_cfg(lambda c: c["matrix"].reverse())
reject_cfg(lambda c: c["matrix"][0].update(suite="shortened"))
reject_cfg(lambda c: c["immutable_test_blobs"].pop("gallery/tests/test_transitions.py"))
reject_cfg(lambda c: c["immutable_test_blobs"].update({"gallery/tests/test_fake.py": "0" * 40}))
reject_cfg(lambda c: c.update(original_workflow_blob="invalid"))
reject_cfg(lambda c: c.update(integrity_workflow_blob="not-a-git-sha"))
reject_cfg(lambda c: c.update(baseline_ancestor="../unknown"))

wrong = copy.deepcopy(cfg)
wrong["original_workflow_blob"] = "0" * 40
actual = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
try:
    api["verify_source"](wrong, actual)
except AssertionError:
    pass
else:
    raise AssertionError("tampered original mandatory workflow blob accepted")

identity = {
    "commit": "a" * 40,
    "checkpoint_folder": "future-approved-release",
    "checkpoint_sha256": "b" * 64,
    "checkpoint_bytes": 8000000,
    "pointer_blob": "c" * 40,
    "full_sha256": "b" * 64,
    "full_bytes": 8000000,
    "lightweight_sha256": "d" * 64,
    "lightweight_bytes": 700000,
    "manifest_blob": "e" * 40,
    "original_workflow_blob": cfg["original_workflow_blob"],
    "integrity_workflow_blob": cfg["integrity_workflow_blob"],
}
p = api["proof"](cfg, identity, "full", "transitions", 14, 12345, 1)
assert api["verify_proof"](cfg, identity, p, "full", "transitions", 12345, 1) == 14

def reject_proof(change):
    candidate = copy.deepcopy(p)
    change(candidate)
    try:
        api["verify_proof"](cfg, identity, candidate, "full", "transitions", 12345, 1)
    except (AssertionError, TypeError, ValueError, KeyError):
        return
    raise AssertionError("unsafe shard proof accepted")

reject_proof(lambda c: c.update(status="skipped"))
reject_proof(lambda c: c.update(mode="lightweight"))
reject_proof(lambda c: c.update(suite="coordinated-fades"))
reject_proof(lambda c: c.update(test_blob="f" * 40))
reject_proof(lambda c: c.update(run_id=12346))
reject_proof(lambda c: c.update(run_attempt=2))
reject_proof(lambda c: c.update(script_seconds=True))
reject_proof(lambda c: c.update(script_seconds=-1))
reject_proof(lambda c: c.update(promotion_authorized=True))
reject_proof(lambda c: c["identity"].update(full_sha256="f" * 64))
reject_proof(lambda c: c["identity"].update(commit="0" * 40))
reject_proof(lambda c: c["identity"].update(checkpoint_folder="../unsafe"))
reject_proof(lambda c: c.update(extra=True))

with tempfile.TemporaryDirectory() as td:
    folder = Path(td)
    try:
        api["aggregate_proofs"](cfg, identity, folder, 12345, 1)
    except AssertionError:
        pass
    else:
        raise AssertionError("missing nine proofs were accepted")
    for e in matrix:
        name = e["mode"] + "-" + e["suite"] + ".json"
        good = api["proof"](cfg, identity, e["mode"], e["suite"], 8, 12345, 1)
        (folder / name).write_text(json.dumps(good), encoding="utf-8")
    summary = api["aggregate_proofs"](cfg, identity, folder, 12345, 1)
    assert summary["proofs"] == 9 and not summary["promotion_authorized"]
    (folder / "extra.json").write_text("{}", encoding="utf-8")
    try:
        api["aggregate_proofs"](cfg, identity, folder, 12345, 1)
    except AssertionError:
        pass
    else:
        raise AssertionError("extra proof accepted")
    (folder / "extra.json").unlink()
    (folder / "full-transitions.json").unlink()
    try:
        api["aggregate_proofs"](cfg, identity, folder, 12345, 1)
    except AssertionError:
        pass
    else:
        raise AssertionError("missing proof accepted")

future = copy.deepcopy(identity)
future.update(commit="0" * 40, checkpoint_folder="new-release",
              full_sha256="1" * 64, checkpoint_sha256="1" * 64,
              lightweight_sha256="2" * 64)
future_proof = api["proof"](cfg, future, "lightweight", "transitions", 9, 99, 2)
assert future_proof["identity"] == future
assert future_proof["identity"]["full_sha256"] != identity["full_sha256"]
print("PASS dynamic per-commit release identity, exact unchanged nine suites, "
      "negative proof tampering and incomplete aggregate rejection.", flush=True)
