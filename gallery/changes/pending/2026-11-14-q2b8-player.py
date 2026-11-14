#!/usr/bin/env python3
"""Q2-B8: exact approved eight earlier Player declarations; 124 bytes."""
import hashlib,json,runpy
from pathlib import Path
SLUG="2026-11-14-q2b8-player"
BASE="881e546da8bdf640fb7b10ed8e465d1461996821"
FILES={"full":("gallery/Gallery-current.html","0bac7523d2c3e5345a36445038a4d369d7e0774059f75fb9640ef5066b32b53d"),
       "lightweight":("gallery/Gallery-development.html","f52cae3f84e5283a5bedaae1aec167223f620f23958453d599d7f47b3b0b7037")}
SOURCES=[
  [
    "gallery/src/styles/03-player-and-desktop-frame.css",
    "6d4512791c21328cfb1047e22c8dd045f616a491"
  ],
  [
    "gallery/src/styles/27-player-navigation-and-header-refinements.css",
    "4c9f312b64572ffc890c7ccdbab7d3b6b28f39b9"
  ]
]
PATCHES=[
  [
    0,
    ".player-area:fullscreen{border:0;border-radius:0;display:flex;align-items:center;justify-content:center;background:#050508}",
    ".player-area:fullscreen{display:flex;align-items:center;justify-content:center;background:#050508}"
  ],
  [
    0,
    ".player-episode-nav small{display:block;color:var(--muted);font-size:12px;margin-top:5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}",
    ".player-episode-nav small{display:block;color:var(--muted);font-size:12px;margin-top:5px}"
  ],
  [
    0,
    ".playback-compactbar .detail-back{margin:0;padding:7px 6px;white-space:nowrap;flex:none}",
    ".playback-compactbar .detail-back{margin:0;padding:7px 6px;white-space:nowrap}"
  ],
  [
    0,
    ".playback-title-inline{display:flex;gap:10px;align-items:baseline;justify-content:center;flex:1;min-width:0;overflow:hidden}",
    ".playback-title-inline{display:flex;gap:10px;align-items:baseline;justify-content:center;flex:1;overflow:hidden}"
  ],
  [
    1,
    "body.player-view .playback-compactbar{\n min-height:43px;display:flex;align-items:center;justify-content:space-between;\n border-bottom:1px solid var(--line);padding:1px 3px 7px;margin-bottom:6px\n}",
    "body.player-view .playback-compactbar{\n min-height:43px;display:flex;justify-content:space-between;\n border-bottom:1px solid var(--line);padding:1px 3px 7px;margin-bottom:6px\n}"
  ]
]
SHARDS=("full-normal","full-reduced","lightweight-normal","lightweight-reduced")
def transform(raw,index=None):
    result=raw
    delta=0
    for i,old,new in PATCHES:
        if index is not None and i!=index:continue
        old,new=old.encode(),new.encode()
        assert result.count(old)==1,old
        result=result.replace(old,new,1)
        delta+=len(old)-len(new)
    assert len(raw)-len(result)==delta==({0:105,1:19}[index] if index is not None else 124)
    return result
def main():
    p=json.loads(Path("gallery/checkpoints/current.json").read_text())
    assert (p["folder"],p["sha256"],p["bytes"])==("2026-11-14-q2b7-settings",FILES["full"][1],6905842)
    for path,digest in FILES.values():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,path
    plan=runpy.run_path("gallery/tools/publisher-candidate.py")["plan"](SLUG)["include"]
    assert len(plan)==7 and {g["mode"] for g in plan if g["kind"]=="comparison"}==set(SHARDS),plan
    for i,(name,sha) in enumerate(SOURCES):
        path=Path(name);raw=path.read_bytes()
        assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==sha
        path.write_bytes(transform(raw,i))
    print("PASS: exact eight approved Player declarations, 124 bytes",flush=True)
if __name__=="__main__":main()
