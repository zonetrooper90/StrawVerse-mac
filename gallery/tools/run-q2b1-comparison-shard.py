#!/usr/bin/env python3
"""Shard the immutable, corrected Q2-B1 comparison on its historical baseline."""
import argparse
import hashlib
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument("mode",choices=("full","lightweight"))
a=p.parse_args()
gate=Path("gallery/audits/2026-11-13-q2b1-downloads-declarations-retry-compare.py")
raw=gate.read_bytes()
assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()=="d9671d447fb6e7d063a44ef7565aae184d4d03fc"
source=raw.decode()
i=0 if a.mode=="full" else 1
pairs=[
    ("    for path,sha in FILES:","    for path,sha in FILES["+str(i)+":"+str(i+1)+"]:"),
    ("    print('PASS: Q2-B1 actual DOM equivalence',path,checks,'comparisons',flush=True)","    assert checks==336,('Unexpected comparison count',path,checks)\n    print('PASS: Q2-B1 actual DOM equivalence',path,checks,'comparisons',flush=True)"),
    ("print('PASS: Q2-B1 comparison gate; exact scope and sampled styles/geometry equivalent in both builds.',flush=True)","print('PASS: Q2-B1 comparison shard; 336 comparisons in selected build.',flush=True)")
]
for old,new in pairs:
    assert source.count(old)==1
    source=source.replace(old,new,1)
exec(compile(source,str(gate),"exec"),{"__name__":"__main__","__file__":str(gate)})
