#!/usr/bin/env python3
"""Static rejection and missing-proof tests for strict 9-way browser sharding."""
import copy
import json
from pathlib import Path
import runpy
import subprocess
import tempfile

api = runpy.run_path("gallery/tools/g31-regression-shards.py")
cfg = json.loads(Path("gallery/development/g31-regression-shards.json").read_text())
assert api["validate"](cfg) is cfg
assert len(api["MATRIX"]) == 9
assert {m["mode"] for m in api["MATRIX"]} == {"full", "lightweight", "both"}
assert len(set(m["mode"] + "/" + m["suite"] for m in api["MATRIX"])) == 9


def reject(mutator):
    broken = copy.deepcopy(cfg)
    mutator(broken)
    try:
        api["validate"](broken)
    except (AssertionError, TypeError, KeyError, ValueError):
        return
    raise AssertionError("unsafe coverage/promotion schema accepted")


reject(lambda c: c.update(schema=2))
reject(lambda c: c.update(status="published"))
reject(lambda c: c["promotion"].update(status="authorized"))
reject(lambda c: c["promotion"].update(published_commit="0" * 40))
reject(lambda c: c["matrix"].pop())
reject(lambda c: c["matrix"].append(copy.deepcopy(c["matrix"][0])))
reject(lambda c: c["matrix"].reverse())
reject(lambda c: c["matrix"][0].update(mode="skipped"))
reject(lambda c: c["immutable_test_blobs"].pop("gallery/tests/test_transitions.py"))
reject(lambda c: c["immutable_test_blobs"].update(
    {"gallery/tests/shortened.py": "a"*40}))
reject(lambda c: c.update(original_workflow_blob="malformed"))
reject(lambda c: c.update(baseline_build_commit="../unsafe"))
reject(lambda c: c.update(baseline_browser_run=0))

commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
# A Git hash with valid syntax but wrong bytes must fail closed before Chromium.
wrong = copy.deepcopy(cfg)
wrong["original_workflow_blob"] = "0" * 40
api["validate"](wrong)
try:
    api["verify_source"](wrong, commit)
except AssertionError:
    pass
else:
    raise AssertionError("incorrect original test workflow blob accepted")

with tempfile.TemporaryDirectory() as tmp:
    try:
        api["aggregate"](cfg, commit, Path(tmp))
    except AssertionError:
        pass
    else:
        raise AssertionError("missing all nine test proofs was accepted")

print("PASS original mandatory test matrix, immutable source contract, "
      "fail-closed missing coverage/tampering and no-promotion tests.")
