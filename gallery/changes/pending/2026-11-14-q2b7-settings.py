#!/usr/bin/env python3
"""Q2-B7: exact approved eighteen earlier Settings declarations; 361 bytes."""
import hashlib,json,runpy
from pathlib import Path
SLUG="2026-11-14-q2b7-settings"
BASE="2f0eafede1ba7402ad54d32384576203c7eb57d2"
FILES={"full":("gallery/Gallery-current.html","ecc20f6750f4c61ba093c88bd4f2392a8e25f1f542dfa94a0c33a36c9127cf68"),
       "lightweight":("gallery/Gallery-development.html","352e2c0231422b65650cd9afa77cb2100a10abb452e2b189332a434d194999c2")}
PATCHES=[
  [
    ".settings-page-head{padding:23px 2px 24px;display:flex;align-items:center;gap:22px;border-bottom:1px solid var(--line)}",
    ".settings-page-head{padding:23px 2px 24px;gap:22px}"
  ],
  [
    ".settings-back{display:flex;align-items:center;gap:6px;background:transparent;color:var(--muted);border:1px solid var(--line);border-radius:10px;padding:10px 12px;flex:none}",
    ".settings-back{display:flex;gap:6px;color:var(--muted);border:1px solid var(--line);padding:10px 12px;flex:none}"
  ],
  [
    ".settings-layout{display:grid;grid-template-columns:minmax(185px,222px) minmax(0,1fr);gap:32px;padding-top:28px;align-items:start}",
    ".settings-layout{display:grid;gap:32px;padding-top:28px}"
  ],
  [
    ".settings-section-button{display:flex;align-items:center;gap:12px;text-align:left;border:1px solid transparent;border-radius:10px;padding:12px 13px;background:transparent;color:var(--muted);font-weight:600;width:100%;font-size:13px}",
    ".settings-section-button{display:flex;align-items:center;gap:12px;text-align:left;border-radius:10px;padding:12px 13px;background:transparent;color:var(--muted);font-weight:600;width:100%;font-size:13px}"
  ],
  [
    ".settings-card-title{font-size:15px;font-weight:690;letter-spacing:-.01em}",
    ".settings-card-title{font-weight:690;letter-spacing:-.01em}"
  ],
  [
    ".settings-layout{grid-template-columns:1fr;gap:20px;padding-top:20px}",
    ".settings-layout{gap:20px;padding-top:20px}"
  ],
  [
    ".settings-side{position:static;flex-direction:row;overflow-x:auto;scrollbar-width:none;gap:3px}",
    ".settings-side{scrollbar-width:none}"
  ],
  [
    ".settings-section-button{width:auto;flex:none;padding:10px 12px;gap:7px;font-size:12px}",
    ".settings-section-button{padding:10px 12px;font-size:12px}"
  ]
]
SHARDS=("full-normal","full-reduced","lightweight-normal","lightweight-reduced")
def transform(raw):
    result=raw
    for old,new in PATCHES:
        old,new=old.encode(),new.encode()
        assert result.count(old)==1,old
        result=result.replace(old,new,1)
    assert len(raw)-len(result)==361
    return result
def main():
    p=json.loads(Path("gallery/checkpoints/current.json").read_text())
    assert (p["folder"],p["sha256"],p["bytes"])==("2026-11-14-selected-release-auto-reveal-retry",FILES["full"][1],6906203)
    for path,digest in FILES.values():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,path
    plan=runpy.run_path("gallery/tools/publisher-candidate.py")["plan"](SLUG)["include"]
    assert len(plan)==7 and {g["mode"] for g in plan if g["kind"]=="comparison"}==set(SHARDS),plan
    later=Path("gallery/src/styles/12-about-and-settings-refinements.css").read_bytes()
    assert hashlib.sha1(b"blob "+str(len(later)).encode()+b"\0"+later).hexdigest()=="2be782715f161929cbfc7d3c8b655b811bd9d0e1"
    path=Path("gallery/src/styles/10-settings.css")
    raw=path.read_bytes()
    assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()=="8a423f4bc21209e6905716e33e2b4ebd8d893c74"
    path.write_bytes(transform(raw))
    print("PASS: exact eighteen approved Settings declarations, 361 bytes",flush=True)
if __name__=="__main__":
    main()
