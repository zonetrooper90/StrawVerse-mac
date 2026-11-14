#!/usr/bin/env python3
"""Q2-B4: exactly the five user-approved earlier About declarations."""
import hashlib, json, runpy
from pathlib import Path

SLUG="2026-11-14-q2b4-about"
BASE="5cc1750e8199ec525587f1ac7f449e7826248b97"
FILES={"full":("gallery/Gallery-current.html","17f0af64a3f1ada057557327c9e26feeeb676a801be319fd23e2f1905b29cd5b"),
       "lightweight":("gallery/Gallery-development.html","4c17191d059b4492bb4cae0eff22669559dd12410e7b2bf8af6f7c8c56c9d5dc")}
PAIRS=[[".about-shell{max-width:730px;margin:0 auto;min-width:0}",".about-shell{max-width:730px;margin:0 auto}"],[".about-menu-item .about-menu-copy strong{font-size:13px;font-weight:620}",".about-menu-item .about-menu-copy strong{font-weight:620}"],[".about-detail-title{font-size:20px;font-weight:720;letter-spacing:-.035em;line-height:1.3;margin:0 0 7px}",".about-detail-title{font-weight:720;letter-spacing:-.035em;line-height:1.3;margin:0 0 7px}"],[".about-identity{display:flex;align-items:center;gap:19px;padding:20px 22px;border:1px solid var(--line);border-radius:16px;background:var(--surface)}",".about-identity{display:flex;gap:19px;padding:20px 22px;border:1px solid var(--line);border-radius:16px;background:var(--surface)}"],[".about-identity{padding:17px;gap:13px}",".about-identity{gap:13px}"]]
SHARDS=("full-normal","full-reduced","lightweight-normal","lightweight-reduced")

def transform(raw):
    result=raw
    for old,new in PAIRS:
        old=old.encode()
        assert result.count(old)==1,old
        result=result.replace(old,new.encode(),1)
    assert len(raw)-len(result)==74
    return result

def main():
    p=json.loads(Path("gallery/checkpoints/current.json").read_text())
    assert (p["folder"],p["sha256"],p["bytes"])==("2026-11-14-q2b3-anime-details-retry",FILES["full"][1],6903147)
    for path,digest in FILES.values():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,path
    # Reject absent or incomplete comparison gates before applying the patch.
    plan=runpy.run_path("gallery/tools/publisher-candidate.py")["plan"](SLUG)["include"]
    assert len(plan)==7 and {g["mode"] for g in plan if g["kind"]=="comparison"}==set(SHARDS),plan
    path=Path("gallery/src/styles/12-about-and-settings-refinements.css")
    raw=path.read_bytes()
    assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()=="26613146f5fa98d841b3f0e0b3e18ce958a60b7d"
    path.write_bytes(transform(raw))
    print("PASS: exact five-declaration About deletion, 74 bytes",flush=True)

if __name__=="__main__":
    main()
