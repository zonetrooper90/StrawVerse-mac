#!/usr/bin/env python3
"""Q2-B5: exactly six user-approved earlier application typography declarations."""
import hashlib, json, runpy
from pathlib import Path
SLUG="2026-11-14-q2b5-typography"
BASE="f17c79f13fe5948f724cde1b6f1b44702273cd89"
FILES={"full":("gallery/Gallery-current.html","0a3a9f474ad454b99e758a70a3c93d3bd03ac3f2c4ddf92aaa3ca536e28b6bbd"),
       "lightweight":("gallery/Gallery-development.html","9c2b205045ee5fd6c462743ecb7707f44a8d7e322bdc8502ae5688fe7a6c1646")}
PAIRS=[[".settings-font-tile{min-width:0;display:flex;flex-direction:column;align-items:stretch;text-align:left;gap:10px;position:relative;border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:13px;padding:15px;transition:background .16s,border-color .16s}",".settings-font-tile{min-width:0;text-align:left;gap:10px;position:relative;border:1px solid var(--line);background:var(--surface);color:var(--ink);padding:15px;transition:background .16s,border-color .16s}"],[".settings-font-tile{flex-direction:column;align-items:stretch;gap:9px}",".settings-font-tile{gap:9px}"]]
SHARDS=("full-normal","full-reduced","lightweight-normal","lightweight-reduced")
def transform(raw):
    result=raw
    for old,new in PAIRS:
        old=old.encode()
        assert result.count(old)==1,old
        result=result.replace(old,new.encode(),1)
    assert len(raw)-len(result)==116
    return result
def main():
    p=json.loads(Path("gallery/checkpoints/current.json").read_text())
    assert (p["folder"],p["sha256"],p["bytes"])==("2026-11-14-q2b4-about",FILES["full"][1],6903073)
    for path,digest in FILES.values():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,path
    plan=runpy.run_path("gallery/tools/publisher-candidate.py")["plan"](SLUG)["include"]
    assert len(plan)==7 and {g["mode"] for g in plan if g["kind"]=="comparison"}==set(SHARDS),plan
    path=Path("gallery/src/styles/13-typography.css")
    raw=path.read_bytes()
    assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()=="038938c774b7bc872f62aa7a0eaad511f5a66878"
    path.write_bytes(transform(raw))
    print("PASS: exact six-declaration typography deletion, 116 bytes",flush=True)
if __name__=="__main__":
    main()
