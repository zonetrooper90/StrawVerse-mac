#!/usr/bin/env python3
"""Q2-B6: exactly one approved earlier release-arrow hover declaration."""
import hashlib,json,runpy
from pathlib import Path
SLUG="2026-11-14-q2b6-release-arrow"
BASE="043eb6b22011e4540c5c843fb8b7d12b297ba913"
FILES={"full":("gallery/Gallery-current.html","3df19003fa0e0b1bbe2a4d47bca65835223052fc5e7e1222bf955fd3c63b1aa8"),
       "lightweight":("gallery/Gallery-development.html","b01c98b76d195b7d00d180f2fae92ed086e9a6e5e21eef2380e3a68581e2bde1")}
OLD=".inline-release-fade .inline-arrow:hover{\n  color:var(--accent);background:transparent;border:0;box-shadow:none;\n}".encode()
NEW=".inline-release-fade .inline-arrow:hover{\n  background:transparent;border:0;box-shadow:none;\n}".encode()
SHARDS=("full-normal","full-reduced","lightweight-normal","lightweight-reduced")
def transform(raw):
    assert raw.count(OLD)==1
    result=raw.replace(OLD,NEW,1)
    assert len(raw)-len(result)==20
    return result
def main():
    p=json.loads(Path("gallery/checkpoints/current.json").read_text())
    assert (p["folder"],p["sha256"],p["bytes"])==("2026-11-14-q2b5-typography",FILES["full"][1],6902957)
    for path,digest in FILES.values():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,path
    plan=runpy.run_path("gallery/tools/publisher-candidate.py")["plan"](SLUG)["include"]
    assert len(plan)==7 and {g["mode"] for g in plan if g["kind"]=="comparison"}==set(SHARDS),plan
    path=Path("gallery/src/styles/07-anime-detail-refinements.css")
    raw=path.read_bytes()
    assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()=="7de22f2c9de4ab0fa46d44d6758d9e70cf7a82ac"
    path.write_bytes(transform(raw))
    print("PASS: exact one-declaration release arrow hover deletion, 20 bytes",flush=True)
if __name__=="__main__":
    main()
