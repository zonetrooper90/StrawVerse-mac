#!/usr/bin/env python3
"""Q2-B3: delete only the 12 approved earlier Anime Details declarations."""
import hashlib,json
from pathlib import Path
p=json.loads(Path("gallery/checkpoints/current.json").read_text())
assert p["folder"]=="2026-11-14-q2b2-episode-toolbar" and p["sha256"]=="369f2ddb37e01b2ebe30901c5143157543a1c72fdbd6b850ef0829e675205e04"
path=Path("gallery/src/styles/02-anime-detail.css")
raw=path.read_bytes()
assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()=="213171d142dc2339aed85cc14591dfe302018f90"
pairs=[[".detail-audio-toggle button[aria-pressed=\"true\"]{background:var(--tab);border-color:var(--accent);color:var(--accent-ink)}",".detail-audio-toggle button[aria-pressed=\"true\"]{background:var(--tab);border-color:var(--accent)}"],[".detail-control-panel{grid-column:2;grid-row:2;max-width:460px}",".detail-control-panel{grid-column:2;max-width:460px}"],[".detail-control-panel{grid-column:1 / -1;grid-row:auto;max-width:none;padding:14px;gap:12px}",".detail-control-panel{grid-column:1 / -1;grid-row:auto;padding:14px;gap:12px}"],[".episode-item{display:grid;grid-template-columns:44px minmax(160px,1fr) minmax(140px,auto) auto;align-items:center;gap:14px;border:0;border-radius:0;min-height:74px;padding:10px 12px;background:transparent;box-shadow:none;cursor:default}",".episode-item{display:grid;grid-template-columns:44px minmax(160px,1fr) minmax(140px,auto) auto;border:0;border-radius:0;min-height:74px;padding:10px 12px;background:transparent;box-shadow:none;cursor:default}"],[".detail-hero{grid-template-columns:160px minmax(0,1fr);gap:22px}",".detail-hero{gap:22px}"],[".detail-hero{grid-template-columns:114px minmax(0,1fr);gap:15px;margin-bottom:23px}",".detail-hero{gap:15px;margin-bottom:23px}"],[".episode-tools{grid-column:3;display:flex;align-items:center;justify-content:flex-end;gap:12px;min-width:0}",".episode-tools{gap:12px}"]]
new=raw
for old,replacement in pairs:
    old=old.encode()
    assert new.count(old)==1,old
    new=new.replace(old,replacement.encode(),1)
assert len(raw)-len(new)==245
path.write_bytes(new)
print("PASS: exact 12-declaration Anime Details deletion, 245 bytes")
