#!/usr/bin/env python3
"""Run the checksum-guarded original Q2-B3 gate for one build and motion.

Only the outer motion loop and exact comparison-count assertion differ.
All original interaction, style, pseudo, geometry and layout assertions run.
"""
import hashlib
from pathlib import Path

ORIGINAL=Path(__file__).with_name("2026-11-14-q2b3-anime-details-comparison.py")
ORIGINAL_BLOB="4fbe8a79313712c81d04c04523276064341ee390"
MOTIONS={"normal":"no-preference","reduced":"reduce"}
CANDIDATES={
    "gallery/Gallery-current.html":"17f0af64a3f1ada057557327c9e26feeeb676a801be319fd23e2f1905b29cd5b",
    "gallery/Gallery-development.html":"4c17191d059b4492bb4cae0eff22669559dd12410e7b2bf8af6f7c8c56c9d5dc",
}
def shard_source(motion):
    assert motion in MOTIONS,"Unexpected motion shard"
    raw=ORIGINAL.read_bytes()
    assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==ORIGINAL_BLOB,"Original gate changed"
    text=raw.decode()
    replacements=(
        ("for motion in ('no-preference','reduce'):","for motion in ("+repr(MOTIONS[motion])+",):"),
        ("assert checks>=1000,(mode,checks)","assert checks==576,(mode,checks)"),
    )
    for old,new in replacements:
        assert text.count(old)==1,old
        text=text.replace(old,new,1)
    return text
def run(mode,motion):
    assert mode in ("full","lightweight") and motion in MOTIONS
    for path,sha in CANDIDATES.items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==sha,("Unexpected retry candidate",path)
    namespace={"__name__":"q2b3_sharded_gate","__file__":str(ORIGINAL)}
    exec(compile(shard_source(motion),str(ORIGINAL),"exec"),namespace)
    namespace["run"](mode)
    print("PASS: Q2-B3 exact required shard",mode,motion,"576 comparisons",flush=True)
