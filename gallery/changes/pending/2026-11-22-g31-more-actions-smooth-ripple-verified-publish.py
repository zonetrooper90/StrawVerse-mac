#!/usr/bin/env python3
"""Approved G3.1 guarded full publication; byte-identical source, corrected strict audit.

The original G3.1 CSS request and its inherited G3 JS/geometry are immutable.
This is a new publisher request, not a retry of either failed historical run.
"""
from pathlib import Path
import hashlib
import runpy

def git_blob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

original=Path("gallery/changes/pending/2026-11-22-g31-more-actions-smooth-ripple-passive-retry.py")
assert git_blob(original.read_bytes())=="eea2d3e07185965026964295558d1cb69190222d", "Original approved G3.1 source replay changed"
audit=Path("gallery/audits/2026-11-22-g31-more-actions-smooth-ripple-verified-publish-compare.py")
assert git_blob(audit.read_bytes())=="dec3f3c5b290d34d71f224d17e3a2c23e38aa78c", "Verified G3.1 publisher comparison wrapper changed"
verified=Path("gallery/audits/2026-11-22-g31-more-actions-smooth-ripple-passive-corrected-compare.py")
assert git_blob(verified.read_bytes())=="0c5b52ebc8ebff885ddfbd79b0a7ceda8ba6f4c0", "Verified 48-context audit changed"
api=runpy.run_path(str(verified))
inherited=api["materialize"]()
assert "assert cases==48" in inherited and ".currentTime=" not in inherited and ".pause()" not in inherited, "Corrected inherited browser comparison failed static preflight"
runpy.run_path(str(original),run_name="__main__")
print("PASS: G3.1 publisher source identical to verified provisional candidate; strict corrected audit; unchanged G3 Library JS",flush=True)
