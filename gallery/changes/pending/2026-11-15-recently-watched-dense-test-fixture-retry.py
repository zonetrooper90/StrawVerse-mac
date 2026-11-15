#!/usr/bin/env python3
"""Single byte-identical retry of the approved dense fixture; no test relaxation."""
import hashlib,runpy
from pathlib import Path
SLUG="2026-11-15-recently-watched-dense-test-fixture-retry"
ORIGINAL="2026-11-15-recently-watched-dense-test-fixture"
def guard(name,sha):
    raw=Path(name).read_bytes()
    assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==sha,name
def main():
    path="gallery/changes/pending/"+ORIGINAL+".py"
    guard(path,"78ef6e7f2471018906a20226687834e175fd126d")
    guard("gallery/audits/"+ORIGINAL+"-regression.py","737acc302cd327c59b1c937bb8bce3d296bd95b4")
    guard("gallery/audits/2026-11-15-watch-history-animated-progress-retry-regression.py","19050ab4e22c6cd2657e95992946d045e158c585")
    plan=runpy.run_path("gallery/tools/publisher-candidate.py")["plan"](SLUG)["include"]
    assert len(plan)==4 and {(g["kind"],g["mode"]) for g in plan}=={("regression","full"),("regression","lightweight"),("assets","both"),("comparison","both")},plan
    runpy.run_path(path,run_name="__main__")
    print("PASS original approved fixture patch and original mandatory tests unchanged",flush=True)
if __name__=="__main__":main()
