#!/usr/bin/env python3
"""Q2-B9: exact approved eleven earlier Search declarations; 139 bytes."""
import hashlib,json,runpy
from pathlib import Path
SLUG="2026-11-14-q2b9-search"
BASE="d7d110e05e3a35da2c5bec16552b0f2881d993b4"
FILES={"full":("gallery/Gallery-current.html","2c57113ca6bdd5f76b4f5da82b5cf17409bad92011342318d97cf747f728bbd9"),
       "lightweight":("gallery/Gallery-development.html","6300cf03e7b19cf5c98705fbd0fe137e94133eb123fc09a846720099e3bd677e")}
PATCHES=[
  [
    ".brand-row.is-searching .toolbar{flex:0 1 474px;min-width:0}",
    ".brand-row.is-searching .toolbar{flex:0 1 474px}"
  ],
  [
    ".brand-row.is-searching .brand{flex:0 1 auto;min-width:0}",
    ".brand-row.is-searching .brand{flex:0 1 auto}"
  ],
  [
    ".header-search-field{display:flex;align-items:center;gap:5px;min-width:0;flex:1 1 auto;width:0;max-width:0;opacity:0;visibility:hidden;overflow:hidden;transition:max-width .28s cubic-bezier(.2,.72,.2,1),opacity .16s ease,visibility 0s .28s}",
    ".header-search-field{display:flex;align-items:center;gap:5px;flex:1 1 auto;max-width:0;transition:max-width .28s cubic-bezier(.2,.72,.2,1),opacity .16s ease,visibility 0s .28s}"
  ],
  [
    ".header-search.is-open .header-search-field{max-width:440px;opacity:1;visibility:visible;transition-delay:0s,.07s,0s}",
    ".header-search.is-open .header-search-field{max-width:440px;transition-delay:0s,.07s,0s}"
  ],
  [
    ".header-search-field input{appearance:none;-webkit-appearance:none;width:100%;min-width:0;height:36px;flex:1 1 auto;padding:0 3px;border:0!important;outline:0!important;background:transparent;color:var(--ink);font-size:13px}",
    ".header-search-field input{appearance:none;-webkit-appearance:none;width:100%;height:36px;flex:1 1 auto;padding:0 3px;border:0!important;outline:0!important;background:transparent;color:var(--ink);font-size:13px}"
  ],
  [
    ".brand-row.is-searching .brand{max-width:0;flex-basis:0;opacity:0}",
    ".brand-row.is-searching .brand{max-width:0;flex-basis:0}"
  ]
]
SHARDS=("full-normal","full-reduced","lightweight-normal","lightweight-reduced")
def transform(raw):
    result=raw
    for old,new in PATCHES:
        old,new=old.encode(),new.encode()
        assert result.count(old)==1,old
        result=result.replace(old,new,1)
    assert len(raw)-len(result)==139
    return result
def main():
    p=json.loads(Path("gallery/checkpoints/current.json").read_text())
    assert (p["folder"],p["sha256"],p["bytes"])==("2026-11-14-q2b8-player",FILES["full"][1],6905718)
    for path,digest in FILES.values():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,path
    plan=runpy.run_path("gallery/tools/publisher-candidate.py")["plan"](SLUG)["include"]
    assert len(plan)==7 and {g["mode"] for g in plan if g["kind"]=="comparison"}==set(SHARDS),plan
    path=Path("gallery/src/styles/09-search.css");raw=path.read_bytes()
    assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()=="c37c3918507ce10914b1baa6bf406ed2e816e921"
    path.write_bytes(transform(raw))
    print("PASS: exact eleven approved Search declarations, 139 bytes",flush=True)
if __name__=="__main__":main()
