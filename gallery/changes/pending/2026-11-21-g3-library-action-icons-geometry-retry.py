#!/usr/bin/env python3
"""G3 exact-source replay; original candidate source, HTML bytes and audit preserved."""
import hashlib
from pathlib import Path
import runpy

def blob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
request=Path("gallery/changes/pending/2026-11-21-g3-library-action-icons.py")
assert blob(request.read_bytes())=="d4ec60a6cb640e16cb67eb3f4df621a55768761b", "Original G3 request changed"
runpy.run_path(str(request),run_name="__main__")
expected={
 "gallery/src/js/07c-library.js":"ca08b3bd258bdf79c039467af8f41edd42381541",
 "gallery/src/js/04h-tab-rendering-and-events.js":"adef513d3394b6ef6a911c7b9e2e77c3436439bd",
 "gallery/src/styles/28-unified-headers-and-history-frame.css":"802a703b9853efa01fb6aeab5dec178ea123a4d8",
}
for path,sha in expected.items():
    assert blob(Path(path).read_bytes())==sha, ("Byte-exact G3 source replay failed",path)
print("PASS G3 exact original source candidate; no application correction",flush=True)
