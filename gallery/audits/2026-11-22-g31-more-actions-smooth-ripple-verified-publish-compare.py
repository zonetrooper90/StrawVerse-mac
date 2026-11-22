#!/usr/bin/env python3
"""G3.1 guarded publisher gate: exact independently verified 48-case passive comparison.

The approved CSS candidate, expected full/lightweight hashes and inherited
checks are locked in the verified correction. Never weaken or skip its tests.
"""
from pathlib import Path
import hashlib
import runpy

def git_blob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

verified=Path("gallery/audits/2026-11-22-g31-more-actions-smooth-ripple-passive-corrected-compare.py")
assert git_blob(verified.read_bytes())=="0c5b52ebc8ebff885ddfbd79b0a7ceda8ba6f4c0", "Verified G3.1 passive audit changed"
runpy.run_path(str(verified),run_name="__main__")
