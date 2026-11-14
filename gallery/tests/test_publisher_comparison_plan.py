#!/usr/bin/env python3
"""Fail-closed comparison matrix and exact Q2-B3 shard source regression."""
import ast
import os
from pathlib import Path
import runpy
import tempfile

root=Path(__file__).resolve().parents[2]
helper=runpy.run_path(str(root/"gallery/tools/publisher-candidate.py"))
plan=helper["plan"]
retry=helper["Q2B3_RETRY"]
modes=helper["MOTION_SHARDS"]
assert modes==("full-normal","full-reduced","lightweight-normal","lightweight-reduced")
runner=runpy.run_path(str(root/"gallery/audits/2026-11-14-q2b3-anime-details-retry-shards.py"))
original=runner["ORIGINAL"].read_text()
for motion,value in (("normal","no-preference"),("reduced","reduce")):
    text=runner["shard_source"](motion)
    # Reversing only the two permitted edits must yield exactly the original.
    assert text.replace("for motion in ("+repr(value)+",):","for motion in ('no-preference','reduce'):",1).replace("assert checks==576,(mode,checks)","assert checks>=1000,(mode,checks)",1)==original
    ast.parse(text)
for mode in modes:
    path=root/"gallery/audits"/(retry+"-compare-"+mode+".py")
    source=path.read_text()
    build,motion=mode.split("-")
    assert source.endswith('["run"]("'+build+'","'+motion+'")\n')
    ast.parse(source)
def reject(request):
    try:
        plan(request)
    except AssertionError:
        return
    raise AssertionError("Invalid gate accepted: "+request)
with tempfile.TemporaryDirectory() as tmp:
    prev=Path.cwd()
    try:
        os.chdir(tmp)
        audit=Path("gallery/audits");audit.mkdir(parents=True)
        def touch(request,suffix):
            p=audit/(request+"-compare"+suffix+".py");p.touch();return p
        def comparisons(request):
            return [x["mode"] for x in plan(request)["include"] if "comparison" in x["kind"]]
        reject(retry)
        for mode in modes[:-1]:
            touch(retry,"-"+mode)
            reject(retry)
        last=touch(retry,"-"+modes[-1])
        assert comparisons(retry)==list(modes) and len(plan(retry)["include"])==7
        extra=touch(retry,"");reject(retry);extra.unlink()
        extra=touch(retry,"-full");reject(retry);extra.unlink()
        last.unlink();reject(retry);last.touch()
        assert comparisons(retry)==list(modes)
        regular="2026-11-14-fixture"
        assert len(plan(regular)["include"])==3
        p=touch(regular,"-full");reject(regular)
        q=touch(regular,"-lightweight")
        assert comparisons(regular)==["full","lightweight"]
        extra=touch(regular,"");reject(regular);extra.unlink();p.unlink();q.unlink()
        touch(regular,"");assert comparisons(regular)==["both"]
        historical=helper["HISTORICAL_SHARD"]
        reject(historical);touch(historical,"")
        assert comparisons(historical)==["full","lightweight"]
        for request in ("2026-11-13-q2a-eight-redundant-css-rules","2026-11-13-q2b1-downloads-declarations","2026-11-14-q2b2-episode-toolbar","2026-11-14-q2b3-anime-details"):
            reject(request)
    finally:
        os.chdir(prev)
print("PASS: exact four-shard plan, complete/ambiguous/missing gate rejection, unchanged historical gates and source transformations")
