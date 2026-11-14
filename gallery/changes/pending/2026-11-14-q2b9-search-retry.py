#!/usr/bin/env python3
"""Byte-identical Q2-B9 retry: test-only correction, original application request unchanged."""
import hashlib,runpy
from pathlib import Path
ORIGINAL="gallery/changes/pending/2026-11-14-q2b9-search.py"
EXPECTED={"full":"20720ad2357c910abab55d800ade47dc2dc9a03b43c78994e51ed55c4c9d8bec","lightweight":"75165538c7da503fb697a45738e89c7639f7399f79cfa1d2d8522922a4991c00"}
def main():
    raw=Path(ORIGINAL).read_bytes()
    assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()=="203e195e537fb3b08164c6dfcb71ea7c16ce0880"
    S=runpy.run_path(ORIGINAL)
    for mode,(name,digest) in S["FILES"].items():
        old=Path(name).read_bytes()
        assert hashlib.sha256(old).hexdigest()==digest
        assert hashlib.sha256(S["transform"](old)).hexdigest()==EXPECTED[mode],mode
    plan=runpy.run_path("gallery/tools/publisher-candidate.py")["plan"]("2026-11-14-q2b9-search-retry")["include"]
    assert len(plan)==7 and {x["mode"] for x in plan if x["kind"]=="comparison"}==set(S["SHARDS"]),plan
    S["main"]()
    print("PASS: retry predicts both exact original candidate HTML hashes",flush=True)
if __name__=="__main__":main()
