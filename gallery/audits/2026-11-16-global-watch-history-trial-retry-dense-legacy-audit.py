#!/usr/bin/env python3
"""Retain every historical dense fixture assertion with the normal-data rail opt-in."""
import hashlib,sys
from pathlib import Path
path=Path(__file__).with_name("2026-11-15-recently-watched-dense-test-fixture-regression.py")
raw=path.read_bytes()
assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()=="737acc302cd327c59b1c937bb8bce3d296bd95b4"
source=raw.decode("utf-8")
for old,new in (
    ('page.goto(origin,wait_until="domcontentloaded")','page.goto(origin+"#recently-watched-legacy",wait_until="domcontentloaded")'),
    ('page.goto(origin+"?normal=1",wait_until="domcontentloaded")','page.goto(origin+"?normal=1#recently-watched-legacy",wait_until="domcontentloaded")'),
):
    assert source.count(old)==1,old
    source=source.replace(old,new)
exec(compile(source,str(path),"exec"),{"__name__":"__main__","__file__":str(path)})
