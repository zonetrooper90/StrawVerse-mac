#!/usr/bin/env python3
"""Q2-B1: delete exactly 16 earlier redundant declarations in six Downloads rules."""
import hashlib,json
from pathlib import Path
p=json.loads(Path('gallery/checkpoints/current.json').read_text())
assert p['folder']=='2026-11-13-ds02b-stronger-back-accent'
assert p['sha256']=='333498a79e7ef34f1d85fd3049d599013c24f1d3b5ff81b80d13f8bf1bf7fee3'
changes=[{"path":"gallery/src/styles/01-base-and-page-headers.css","sha":"9cf3c3fb7989f7bb0033c9a15b8c154bc7c6485b","replacements":[[".demo-download-footer{display:flex;align-items:center;flex-wrap:wrap;gap:7px 14px;margin-top:11px}",".demo-download-footer{gap:7px 14px;margin-top:11px}"]]},{"path":"gallery/src/styles/21-themed-downloads.css","sha":"ac62184c58ee4b7d2f7c0d5b24ed67883e10f2f2","replacements":[["body[data-theme] .sf-dl-list .sf-dl-episode{\n display:grid;grid-template-columns:minmax(100px,1fr) minmax(115px,.95fr) minmax(140px,1.45fr) 126px 44px;\n gap:12px;align-items:center;min-width:0;min-height:48px;padding:7px 0;\n border:0;color:var(--fg)\n}","body[data-theme] .sf-dl-list .sf-dl-episode{\n display:grid;grid-template-columns:minmax(100px,1fr) minmax(115px,.95fr) minmax(140px,1.45fr) 126px 44px;\n align-items:center;min-width:0;padding:7px 0;\n color:var(--fg)\n}"],["body[data-theme] .sf-dl-episode-track{display:flex;align-items:center;min-width:0;width:100%}","body[data-theme] .sf-dl-episode-track{display:flex;align-items:center;width:100%}"],["body[data-theme] .sf-dl-control-button{height:28px;min-width:74px;padding:0 8px;background:#ffffff0d;border:1px solid var(--line);border-radius:16px;color:var(--fg);font-size:11px;font-weight:650;display:flex;align-items:center;justify-content:center;gap:5px;cursor:pointer}","body[data-theme] .sf-dl-control-button{height:28px;min-width:74px;padding:0 8px;background:#ffffff0d;border:1px solid var(--line);color:var(--fg);font-weight:650;display:flex;gap:5px;cursor:pointer}"],["body[data-theme] .sf-dl-episode-percent{width:44px;justify-self:end;text-align:right;font-size:11px;font-weight:620;color:var(--muted);font-variant-numeric:tabular-nums}","body[data-theme] .sf-dl-episode-percent{font-size:11px;font-weight:620;color:var(--muted)}"],["body[data-theme] .sf-dl-list .sf-dl-episode{grid-template-columns:minmax(85px,1fr) minmax(90px,.9fr) minmax(100px,1.4fr) 126px 44px;gap:9px}","body[data-theme] .sf-dl-list .sf-dl-episode{grid-template-columns:minmax(85px,1fr) minmax(90px,.9fr) minmax(100px,1.4fr) 126px 44px}"]]}]
updates=[]
for item in changes:
    path=Path(item['path'])
    raw=path.read_bytes()
    assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==item['sha'],str(path)
    data=raw.decode('utf-8')
    for old,new in item['replacements']:
        assert data.count(old)==1,(str(path),old)
        data=data.replace(old,new,1)
    updates.append((path,data.encode('utf-8')))
assert sum(len(path.read_bytes())-len(data) for path,data in updates)==256
for path,data in updates:
    path.write_bytes(data)
print('Q2-B1: exactly 16 earlier Downloads declarations removed; 256 bytes; six rules retained.')
