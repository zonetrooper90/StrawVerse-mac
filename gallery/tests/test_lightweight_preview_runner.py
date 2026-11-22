#!/usr/bin/env python3
"""Deterministic, no-browser tests of lightweight preview safety gates."""
from pathlib import Path
import runpy
import tempfile

tool = runpy.run_path("gallery/tools/lightweight-preview.py")
valid = tool["validate_name"]
assert valid("baseline") == "baseline"
assert valid("2026-11-22-example-preview") == "2026-11-22-example-preview"
for invalid in ("../sneak", "other/one", "G3.1", "no-date", "", "2026-11-22-X"):
    try:
        valid(invalid)
    except tool["PreviewError"]:
        continue
    raise AssertionError(("invalid request accepted", invalid))
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    (root / "original.py").write_text("left middle right", encoding="utf-8")
    wrapper = root / "wrapper.py"
    wrapper.write_text(
        'original=Path("original.py")\n'
        'replace_once("left","new-left")\n'
        'replace_once("middle","new-middle")\n',
        encoding="utf-8",
    )
    assert tool["preflight_audit"](wrapper, root=root) == 2
    wrapper.write_text(
        'original=Path("original.py")\n'
        'replace_once("missing anchor","replacement")\n',
        encoding="utf-8",
    )
    try:
        tool["preflight_audit"](wrapper, root=root)
    except tool["PreviewError"]:
        pass
    else:
        raise AssertionError("Broken audit anchor was not rejected")
    wrapper.write_text(
        'original=Path("../outside.py")\n'
        'replace_once("left","replacement")\n',
        encoding="utf-8",
    )
    try:
        tool["preflight_audit"](wrapper, root=root)
    except tool["PreviewError"]:
        pass
    else:
        raise AssertionError("Parent path escape was not rejected")
print("PASS lightweight preview slug, inherited-audit anchors, source path isolation")
