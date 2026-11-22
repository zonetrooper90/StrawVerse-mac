#!/usr/bin/env python3
"""G3.1 byte-identical application replay; corrected passive frame-observation test only."""
from pathlib import Path
import hashlib
import runpy

def blob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

original=Path("gallery/changes/pending/2026-11-22-g31-more-actions-smooth-ripple.py")
assert blob(original.read_bytes())=="c974130c69d86678607f1f5a7f970089c4be0505", "Original approved G3.1 source request changed"
runpy.run_path(str(original),run_name="__main__")
expected={
 "gallery/src/styles/28-unified-headers-and-history-frame.css":"a8cd52c9a9dd1b9b1b8c6760db3c850ce711542c",
 "gallery/src/js/07c-library.js":"ca08b3bd258bdf79c039467af8f41edd42381541",
 "gallery/src/js/04h-tab-rendering-and-events.js":"adef513d3394b6ef6a911c7b9e2e77c3436439bd"
}
for path,sha in expected.items():
    assert blob(Path(path).read_bytes())==sha,("G3.1 immutable source candidate drift",path)
print("PASS G3.1 exact original source and unchanged Library JS; no application correction",flush=True)
