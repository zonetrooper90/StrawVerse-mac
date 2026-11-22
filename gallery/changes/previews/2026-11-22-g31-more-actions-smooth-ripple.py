#!/usr/bin/env python3
"""Stage-2 provisional lightweight preview of the exact approved G3.1 source.

This does not publish Gallery or change the checked-in source/checkpoint.
The original request is immutable; its content and exact generated CSS are
checksum-guarded before the existing stage-1 runner creates the preview.
"""
from pathlib import Path
import hashlib
import runpy

def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

original=Path("gallery/changes/pending/2026-11-22-g31-more-actions-smooth-ripple.py")
assert blob(original.read_bytes()) == "c974130c69d86678607f1f5a7f970089c4be0505", "Approved G3.1 request changed"
runpy.run_path(str(original), run_name="__main__")
expected={
    "gallery/src/styles/28-unified-headers-and-history-frame.css": "a8cd52c9a9dd1b9b1b8c6760db3c850ce711542c",
    "gallery/src/js/07c-library.js": "ca08b3bd258bdf79c039467af8f41edd42381541",
    "gallery/src/js/04h-tab-rendering-and-events.js": "adef513d3394b6ef6a911c7b9e2e77c3436439bd",
}
for path,expected_sha in expected.items():
    actual=blob(Path(path).read_bytes())
    assert actual==expected_sha, ("Candidate source differs from previously approved G3.1",path,actual)
print("PASS exact G3.1 approved source replay in disposable preview worktree",flush=True)
