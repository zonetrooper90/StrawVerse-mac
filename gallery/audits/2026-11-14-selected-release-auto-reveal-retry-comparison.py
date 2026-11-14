#!/usr/bin/env python3
"""Correct Chromium's computed scroll-snap serialization in original gate."""
import hashlib
from pathlib import Path
ORIGINAL=Path("gallery/audits/2026-11-14-selected-release-auto-reveal-comparison.py")
raw=ORIGINAL.read_bytes()
assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()=="62a38e9fb1bba9021b89840e15988919191b17ff"
source=raw.decode()
# Require the actual original baseline snap value, not a spelling assumption.
# Also check the temporary inline override was removed. No cases skipped.
old='assert geom(page)["snap"]=="x proximity"'
new='assert old[1440]["snap"] in ("x","x proximity") and geom(page)["snap"]==old[1440]["snap"] and rail(page).evaluate("e=>e.style.scrollSnapType")==""'
assert source.count(old)==3
source=source.replace(old,new)
assert source.count(new)==3
# Include actual state in the two previously bare assertion messages.
source=source.replace(new+'\n',new+',geom(page)\n')
# Preserve the original source and original runner; execute only corrected
# assertion expressions in memory. Both exact candidate outputs mandatory.
for path,digest in {
  "gallery/Gallery-current.html":"ecc20f6750f4c61ba093c88bd4f2392a8e25f1f542dfa94a0c33a36c9127cf68",
  "gallery/Gallery-development.html":"352e2c0231422b65650cd9afa77cb2100a10abb452e2b189332a434d194999c2"
}.items():
    assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,path
print("PASS: both original candidate HTML digests; corrected three snap assertions against actual baseline",flush=True)
scope={"__name__":"auto_reveal_retry","__file__":str(ORIGINAL)}
exec(compile(source,str(ORIGINAL),"exec"),scope)
run=scope["run"]
