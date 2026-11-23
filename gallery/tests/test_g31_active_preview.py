#!/usr/bin/env python3
"""Stage 7 negative, no-browser contract tests."""
import copy
import json
from pathlib import Path
import runpy

api = runpy.run_path("gallery/tools/g31-active-preview.py")
original = json.loads(Path("gallery/development/g31-active-preview.json").read_text())
assert len(api["validate"](original)) == 1
assert original["mode"] == "approved-source-only"
assert original["steps"][0]["slug"] == "2026-11-23-stage7-source-probe"
assert original["steps"][0]["preview_bytes"] == 646042
assert original["steps"][0]["preview_sha256"] == (
    "6cd42f43e04c3a678bc6e5eb67d839616bd7a3c972ef40eec0c4e69da4ad9922")
assert original["steps"][0]["source_blobs"] == {
    "gallery/src/styles/28-unified-headers-and-history-frame.css":
        "8fbefc98cba2123482963db830de36289a591ef1"}
assert original["steps"][0]["approval_heading"] == (
    "## 2026-11-23 — Approved Stage 7 nonvisual source-change preview probe")
assert original["promotion"] == {"status": "not-authorized", "published_commit": None}


def reject(x):
    try:
        api["validate"](x)
    except (AssertionError, KeyError, ValueError, TypeError):
        return
    raise AssertionError("Unsafe preview contract accepted")


for k, value in (("schema", 2), ("mode", "baseline-only"),
                 ("status", "release"), ("baseline_git_blob", "../wrong")):
    x = copy.deepcopy(original)
    x[k] = value
    reject(x)
for k, value in (("status", "authorized"), ("published_commit", "a" * 40)):
    x = copy.deepcopy(original)
    x["promotion"][k] = value
    reject(x)

slug = "2026-12-01-future-example"
step = {"slug": slug, "script": "gallery/development/preview-scripts/" + slug + ".py",
        "script_blob": "a" * 40,
        "approval_heading": "## 2026-12-01 — Approved future example",
        "source_blobs": {"gallery/src/styles/28-unified-headers-and-history-frame.css":
                         "b" * 40},
        "preview_bytes": 650000, "preview_sha256": "c" * 64}
future = copy.deepcopy(original)
future["mode"] = "approved-source-only"
future["steps"] = [step]
assert len(api["validate"](future)) == 1
for k, v in (
    ("script", "gallery/changes/pending/" + slug + ".py"),
    ("script_blob", "short"),
    ("approval_heading", "unapproved"),
    ("source_blobs", {"gallery/assets/example.png": "b" * 40}),
    ("source_blobs", {"gallery/src/../checkpoints/current.json": "b" * 40}),
    ("preview_sha256", "bad"),
    ("preview_bytes", 0),
):
    x = copy.deepcopy(future)
    x["steps"][0][k] = v
    reject(x)
x = copy.deepcopy(future)
x["steps"].append(copy.deepcopy(step))
reject(x)
wrong = copy.deepcopy(original)
wrong["baseline_git_blob"] = "0" * 40
api["validate"](wrong)
try:
    api["baseline"](wrong)
except AssertionError:
    pass
else:
    raise AssertionError("Wrong G3.1 baseline accepted")
print("PASS fail-closed, source-only, approval-pinned preview contract")
