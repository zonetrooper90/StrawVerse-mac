#!/usr/bin/env python3
"""Prepare a NEW immutable Gallery HTML checkpoint and advance the LOCAL pointer.

This only stages local files. It does NOT push to GitHub. The backup is complete
only when the changes are committed, remote SHA verified and GitHub CI passes.

Example:
    python gallery/tools/stage-checkpoint.py --input Gallery-edited.html \
      --id 2026-11-11-player-polish --status delivered-for-user-testing
"""
import argparse
import base64
import gzip
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

GALLERY = Path(__file__).resolve().parents[1]
CHECKPOINTS = GALLERY / 'checkpoints'
PART_SIZE = 245760
MARKERS = (b'<!doctype html>',b'player-episode-nav',b'player-upnext',b'Watch History',b'settings-view')


def digest(b):
    return hashlib.sha256(b).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input', type=Path, required=True, help='Complete tested Gallery HTML')
    p.add_argument('--id', required=True, help='Unique YYYY-MM-DD-slug (never reused)')
    p.add_argument('--status', required=True, choices=('delivered-for-user-testing','user-approved','experiment'))
    args = p.parse_args()
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}-[a-z0-9][a-z0-9-]*', args.id):
        p.error('ID must be YYYY-MM-DD-lowercase-slug')
    if args.input.suffix.lower() != '.html':
        p.error('Use a complete .html file, not a patch')
    if (CHECKPOINTS/args.id).exists():
        p.error('Immutable checkpoint already exists: '+args.id)
    raw = args.input.read_bytes()
    for mark in MARKERS:
        if mark not in raw:
            p.error('HTML lacks expected Gallery marker: '+str(mark))
    prev_path = CHECKPOINTS / 'current.json'
    previous = prev_path.read_bytes()
    current = json.loads(previous)
    if digest(raw) == current['sha256']:
        p.error('File matches current checkpoint; nothing to stage')
    compressed = gzip.compress(raw,compresslevel=9,mtime=0)
    encoded = base64.b64encode(compressed).decode('ascii')
    pieces = [encoded[n:n+PART_SIZE] for n in range(0,len(encoded),PART_SIZE)]
    folder = CHECKPOINTS / args.id
    try:
        (folder/'parts').mkdir(parents=True,exist_ok=False)
        parts=[]
        for i,piece in enumerate(pieces,1):
            name=f'part-{i:03d}.b64'
            data=piece.encode('ascii')
            (folder/'parts'/name).write_bytes(data)
            parts.append({'file':'parts/'+name,'encoded_chars':len(data),'sha256':digest(data)})
        manifest={
          'schema_version':1, 'checkpoint':args.id,
          'source_name':args.input.name, 'output_filename':'Gallery-current.html',
          'source_bytes':len(raw), 'source_sha256':digest(raw),
          'compression':'gzip (mtime=0) + base64',
          'compressed_bytes':len(compressed), 'compressed_sha256':digest(compressed),
          'encoded_chars':len(encoded), 'parts':parts,
          'status':args.status,
          'provenance':'Generated from a locally tested complete HTML file; commit and verify before delivery.'
        }
        (folder/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
        pointer={
          'folder':args.id,'sha256':digest(raw),'bytes':len(raw),
          'source_name':args.input.name,'status':args.status,
          'note':'Local staging only until GitHub commit and CI verification.'
        }
        temp=CHECKPOINTS/'current.json.tmp'
        temp.write_text(json.dumps(pointer,indent=2)+'\n',encoding='utf-8')
        temp.replace(prev_path)
        subprocess.run([sys.executable,str(GALLERY/'tools'/'restore-checkpoint.py'),'--verify-only'],check=True)
    except Exception:
        prev_path.write_bytes(previous)
        if folder.exists():
            shutil.rmtree(folder)
        raise
    print('\nSTAGED ONLY, NOT YET BACKED UP TO GITHUB.')
    print('New folder:',folder)
    print('New source SHA-256:',digest(raw))
    print('Next: commit this folder + gallery/checkpoints/current.json, then verify remote GitHub branch head and successful GitHub Actions integrity run.')


if __name__=='__main__':
    main()