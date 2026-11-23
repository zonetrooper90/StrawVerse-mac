#!/usr/bin/env python3
"""Approved nonvisual G3.1 preview probe, applied ONLY in a disposable worktree.

One stylesheet comment is appended. This changes generated lightweight HTML
bytes while leaving every rendered CSS rule and runtime behavior unchanged.
No tracked source, generated HTML, artwork or checkpoint is published.
"""
import hashlib
from pathlib import Path

source = Path("gallery/src/styles/28-unified-headers-and-history-frame.css")
original = source.read_bytes()
expected_original_blob = "a8cd52c9a9dd1b9b1b8c6760db3c850ce711542c"
blob = hashlib.sha1(
    b"blob " + str(len(original)).encode() + b"\0" + original
).hexdigest()
if blob != expected_original_blob:
    raise AssertionError("Stage 7 probe expected the immutable G3.1 source blob")
if not original.endswith(b"}\n"):
    raise AssertionError("Stage 7 probe expected the unmodified final CSS rule")
probe = b"/* Stage 7 source-only preview probe: HTML bytes change; visual behavior stays G3.1. */\n"
if probe in original:
    raise AssertionError("Stage 7 preview probe must run only once")
source.write_bytes(original + probe)
