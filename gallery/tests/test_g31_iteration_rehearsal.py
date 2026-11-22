#!/usr/bin/env python3
"""Stage 5: reject unsafe source iterations before expensive browser jobs."""
import copy
import json
from pathlib import Path
import runpy

api = runpy.run_path("gallery/tools/g31-iteration-rehearsal.py")
original = json.loads(Path("gallery/development/g31-iterations.json").read_text())
assert api["validate"](original) == []


def reject(change):
    broken = copy.deepcopy(original)
    change(broken)
    try:
        api["validate"](broken)
    except (AssertionError, TypeError, KeyError, ValueError):
        return
    raise AssertionError("unsafe G3.1 lightweight iteration contract accepted")


reject(lambda x: x.update(schema=2))
reject(lambda x: x.update(status="release"))
reject(lambda x: x.update(baseline_ref="gallery/development/provisional.json"))
reject(lambda x: x.update(baseline_git_blob="../wrong"))
reject(lambda x: x["promotion"].update(status="authorized"))
reject(lambda x: x["promotion"].update(published_commit="a"*40))
reject(lambda x: x.update(mode="approved-source-only-steps"))
reject(lambda x: x["iterations"].append({"slug": "2026-11-22-unapproved"}))

# A hypothetical, syntactically valid future step remains ONLY a contract
# rehearsal: its scripts are not executed, and it cannot authorize publication.
slug = "2026-12-01-approved-future-example"
example = {"slug": slug,
           "preview_script": "gallery/changes/previews/" + slug + ".py",
           "preview_script_blob": "a"*40,
           "approved_script": "gallery/changes/pending/" + slug + ".py",
           "approved_script_blob": "b"*40,
           "source_blobs": {"gallery/src/styles/28-unified-headers-and-history-frame.css":"c"*40},
           "lightweight_sha256": "d"*64,
           "lightweight_bytes": 645999}
future = copy.deepcopy(original)
future["mode"] = "approved-source-only-steps"
future["iterations"] = [example]
assert len(api["validate"](future)) == 1
reject(lambda x: x.update(mode="released"))
for bad in (
    {"source_blobs": {"gallery/assets/icon.png": "a"*40}},
    {"source_blobs": {"gallery/src/../assets/icon.png": "a"*40}},
    {"source_blobs": {"gallery/src/js/something.js": "a"*12}},
    {"preview_script": "gallery/changes/previews/other.py"},
    {"lightweight_bytes": 0},
):
    variant = copy.deepcopy(future)
    variant["iterations"][0].update(bad)
    try:
        api["validate"](variant)
    except (AssertionError, KeyError, ValueError, TypeError):
        pass
    else:
        raise AssertionError("unsafe future step accepted: " + str(bad))

# Well-formed but incorrect values are rejected by content checks, not syntax.
wrong = copy.deepcopy(original)
wrong["baseline_git_blob"] = "0"*40
api["validate"](wrong)
try:
    api["baseline_check"](wrong)
except AssertionError:
    pass
else:
    raise AssertionError("modified G3.1 baseline source was accepted")

print("PASS fail-closed G3.1 iteration contract, future provenance schema, "
      "no-promotion gate and baseline tamper rejection.")
