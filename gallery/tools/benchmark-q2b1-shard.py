#!/usr/bin/env python3
"""Read-only benchmark: run one complete build-mode shard of the historical Q2-B1 gate.

The original approved gate is immutable. Only its final FILES iteration is
restricted to one mode, and the original count is asserted for that mode.
The workflow runs both shards on independent runners with fail-fast disabled.
No patch, build, staging, or publication takes place.
"""
import argparse
import hashlib
import json
from pathlib import Path

parser=argparse.ArgumentParser()
parser.add_argument("mode",choices=("full","lightweight"))
args=parser.parse_args()
pointer=json.loads(Path("gallery/checkpoints/current.json").read_text())
assert pointer["folder"]=="2026-11-13-q2b1-downloads-declarations-retry"
assert pointer["sha256"]=="2c0dbfd0aa3ff31fd36d0f0b82ae3421351a128cd6e9c39f46fbde232d24d608"
for filename,expected in (("Gallery-current.html","2c0dbfd0aa3ff31fd36d0f0b82ae3421351a128cd6e9c39f46fbde232d24d608"),("Gallery-development.html","f9ca46ad2de6dfd320872b7aa529ef4b44ecfbc8507410e6dd1e9394636f2721")):
    assert hashlib.sha256((Path("gallery")/filename).read_bytes()).hexdigest()==expected,filename
gate=Path("gallery/audits/2026-11-13-q2b1-downloads-declarations-retry-compare.py")
raw=gate.read_bytes()
assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()=="d9671d447fb6e7d063a44ef7565aae184d4d03fc","Historical gate changed"
source=raw.decode("utf-8")
index=0 if args.mode=="full" else 1
replacements=[
    ("    for path,sha in FILES:","    for path,sha in FILES["+str(index)+":"+str(index+1)+"]:"),
    ("    print('PASS: Q2-B1 actual DOM equivalence',path,checks,'comparisons',flush=True)",
     "    assert checks==336,('Unexpected comparison count',path,checks)\n    print('PASS: Q2-B1 actual DOM equivalence',path,checks,'comparisons',flush=True)"),
    ("print('PASS: Q2-B1 comparison gate; exact scope and sampled styles/geometry equivalent in both builds.',flush=True)",
     "print('PASS: Q2-B1 comparison shard; 336 comparisons in selected build.',flush=True)")
]
for old,new in replacements:
    assert source.count(old)==1,old
    source=source.replace(old,new,1)
print("Benchmark mode:",args.mode,flush=True)
exec(compile(source,str(gate),"exec"),{"__name__":"__main__","__file__":str(gate)})
