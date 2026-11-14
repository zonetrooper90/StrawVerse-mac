#!/usr/bin/env python3
"""Retry the original approved auto-reveal patch without any application changes."""
import hashlib,runpy
from pathlib import Path
SLUG="2026-11-14-selected-release-auto-reveal-retry"
ORIGINAL=Path("gallery/changes/pending/2026-11-14-selected-release-auto-reveal.py")
raw=ORIGINAL.read_bytes()
assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()=="4a4c3131b851728b7744c8e7531306f71cfddd82"
S=runpy.run_path(str(ORIGINAL))
def main():
    plan=runpy.run_path("gallery/tools/publisher-candidate.py")["plan"](SLUG)["include"]
    assert len(plan)==7 and {g["mode"] for g in plan if g["kind"]=="comparison"}=={"full-normal","full-reduced","lightweight-normal","lightweight-reduced"},plan
    for mode,digest in {"full":"ecc20f6750f4c61ba093c88bd4f2392a8e25f1f542dfa94a0c33a36c9127cf68","lightweight":"352e2c0231422b65650cd9afa77cb2100a10abb452e2b189332a434d194999c2"}.items():
        path,_=S["FILES"][mode]
        assert hashlib.sha256(S["expected_html"](Path(path).read_bytes())).hexdigest()==digest,mode
    S["main"]()
    print("PASS: identical original approved auto-reveal application candidate",flush=True)
if __name__=="__main__":
    main()
