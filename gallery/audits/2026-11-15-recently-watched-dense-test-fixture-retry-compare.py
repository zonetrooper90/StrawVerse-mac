#!/usr/bin/env python3
"""Require exact candidate HTML bytes from the original failed publication."""
import hashlib
from pathlib import Path
for name,size,digest in [
    ("Gallery-current.html",6925082,"0a73fd1027e6b0a993fd318e3147e4fbb51b60812ce4b2827451a87a84908dbc"),
    ("Gallery-development.html",609392,"9a3614054fc204d702da1b6c16dd3764e64791f00a760e689192d0441672bc7b"),
]:
    raw=(Path("gallery")/name).read_bytes()
    assert (len(raw),hashlib.sha256(raw).hexdigest())==(size,digest),name
    print("PASS byte-identical dense fixture candidate",name,size,digest,flush=True)
