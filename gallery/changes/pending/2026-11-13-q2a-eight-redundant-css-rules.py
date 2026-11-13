#!/usr/bin/env python3
"""Q2-A: remove exactly eight reviewed earlier CSS rules, retaining all later copies."""
import hashlib
import json
from pathlib import Path

pointer=json.loads(Path('gallery/checkpoints/current.json').read_text())
assert pointer['folder']=='2026-11-13-shared-download-history-width'
assert pointer['sha256']=='6d62486f67526e5e310d08bf2cbcbf14f7a466e9df79edf8b562b6b3b057881d'
changes=[{"path":"gallery/src/styles/01-base-and-page-headers.css","sha":"b73cdb07ffedcaac7ea54358a3341ecd9f1156a7","blocks":[".demo-download-footer .tip{margin:0}"]},{"path":"gallery/src/styles/03-player-and-desktop-frame.css","sha":"90821beb4bcbe85ebee81ee54ea837716f8fb6d7","blocks":[".player-controls .controls-middle{justify-content:center}",".player-episode-nav .btn{font-size:12px;min-width:0;max-width:100%}"]},{"path":"gallery/src/styles/10-settings.css","sha":"11776e53096c82911cf8ff2827f5173ef13e8292","blocks":[".settings-panel-head .description{font-size:13px;line-height:1.5}",".settings-back{padding:8px}"]},{"path":"gallery/src/styles/21-themed-downloads.css","sha":"2ba10de27b8f334d0492c633805838958cd57159","blocks":["body[data-theme] .sf-dl-episode-name{grid-area:name}","body[data-theme] .sf-dl-episode-control{grid-area:control}","body[data-theme] .sf-dl-episode-percent{grid-area:percent}"]}]
updates=[]
for item in changes:
    path=Path(item['path'])
    raw=path.read_bytes()
    assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==item['sha'],str(path)
    data=raw.decode('utf-8')
    for block in item['blocks']:
        assert data.count(block)==1, (str(path),block)
        data=data.replace(block,'',1)
    updates.append((path,data.encode('utf-8')))
assert sum(len(item['blocks']) for item in changes)==8
for path,data in updates:
    path.write_bytes(data)
print('Q2-A: eight exact earlier blocks removed; later rules, whitespace outside blocks and other sources preserved.')
