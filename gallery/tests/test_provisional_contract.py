#!/usr/bin/env python3
"""Read-only provisional contract unit tests; cannot publish or mutate Gallery."""
import copy
import json
from pathlib import Path
import runpy
import tempfile

api=runpy.run_path("gallery/tools/provisional-contract.py")
p=api["load_contract"]()
assert p["promotion"]["status"]=="not-approved"
assert p["request"]["slug"]=="2026-11-22-g31-more-actions-smooth-ripple"

def invalid(modify):
    broken=copy.deepcopy(p)
    modify(broken)
    with tempfile.TemporaryDirectory() as d:
        path=Path(d)/"malformed.json"
        path.write_text(json.dumps(broken),encoding="utf-8")
        try:
            api["load_contract"](path)
        except (AssertionError, ValueError, KeyError, TypeError):
            return
    raise AssertionError("Contract accepted unsafe provisional state")

invalid(lambda q: q.update(schema=2))
invalid(lambda q: q["promotion"].update(status="approved"))
invalid(lambda q: q["promotion"].update(promoted_commit="fake"))
invalid(lambda q: q["request"].update(file="../escape.py"))
invalid(lambda q: q["candidate"].update(changed_source_git_blobs={"gallery/assets/portrait.png":"a"*40}))
invalid(lambda q: q["baseline"].update(full_sha256="not-sha"))
invalid(lambda q: q["request"].update(slug="../../oops"))
invalid(lambda q: q["candidate"].update(lightweight_bytes=0))
print("PASS fail-closed provisional schema, immutable promotion boundary, source path checks")
