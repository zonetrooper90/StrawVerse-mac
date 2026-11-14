#!/usr/bin/env python3
"""Q2-B2: remove only 17 earlier identical declarations in seven Anime toolbar rules."""
import hashlib,json
from pathlib import Path
p=json.loads(Path("gallery/checkpoints/current.json").read_text())
assert p["folder"]=="2026-11-13-q2b1-downloads-declarations-retry" and p["sha256"]=="2c0dbfd0aa3ff31fd36d0f0b82ae3421351a128cd6e9c39f46fbde232d24d608"
path=Path("gallery/src/styles/07-anime-detail-refinements.css")
raw=path.read_bytes()
assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()=="ce896087cebd15258aed9a1c2e47d13ddf75a04e"
pairs=[[".episode-toolbar{display:flex;align-items:center;gap:17px;margin:0 0 13px;min-width:0}",".episode-toolbar{display:flex;gap:17px}"],[".episode-toolbar .episode-heading{flex:0 0 90px;min-width:0;align-self:center;display:flex;align-items:center}",".episode-toolbar .episode-heading{flex:0 0 90px;min-width:0;display:flex;align-items:center}"],[".episode-toolbar .episode-availability{flex:1 1 auto;min-width:0;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:7px 10px 7px 14px;margin:0;border-radius:12px}",".episode-toolbar .episode-availability{flex:1 1 auto;display:flex;justify-content:space-between;border-radius:12px}"],[".episode-availability .episode-stats{display:flex;align-items:center;gap:15px;min-width:0;flex-wrap:wrap;row-gap:6px}",".episode-availability .episode-stats{gap:15px;flex-wrap:wrap;row-gap:6px}"],[".episode-availability .episode-shown{display:inline-flex;align-items:center;gap:13px;white-space:nowrap;color:var(--muted);font-size:11px;font-variant-numeric:tabular-nums;opacity:1;transition:opacity .42s ease}",".episode-availability .episode-shown{display:inline-flex;align-items:center;gap:13px;color:var(--muted);font-size:11px;font-variant-numeric:tabular-nums;opacity:1;transition:opacity .42s ease}"],[".episode-availability .episode-filter{flex:0 0 auto;margin:0;display:inline-flex;gap:2px;align-items:center;flex-wrap:nowrap;padding:3px;border-radius:9px;background:var(--window)}",".episode-availability .episode-filter{display:inline-flex;gap:2px;align-items:center;flex-wrap:nowrap;padding:3px;border-radius:9px;background:var(--window)}"],[".episode-availability .episode-filter button{border:1px solid transparent;background:transparent;border-radius:7px;color:var(--muted);min-height:30px;padding:6px 10px;font-size:11px;font-weight:650;white-space:nowrap;line-height:1.1}",".episode-availability .episode-filter button{border:1px solid transparent;background:transparent;border-radius:7px;color:var(--muted);font-size:11px;font-weight:650;white-space:nowrap;line-height:1.1}"]]
new=raw
for old,replacement in pairs:
    old=old.encode()
    assert new.count(old)==1,old
    new=new.replace(old,replacement.encode(),1)
assert len(raw)-len(new)==259
path.write_bytes(new)
print("PASS: exact 17-declaration Anime episode toolbar deletion, 259 bytes")
