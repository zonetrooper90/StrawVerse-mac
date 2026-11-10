#!/usr/bin/env python3
"""Restore and verify the exact latest Gallery HTML committed to GitHub.

Usage:
  python gallery/tools/restore-checkpoint.py --verify-only
  python gallery/tools/restore-checkpoint.py --output ./Gallery-current.html

This reads the checked-in `gallery/checkpoints/current.json` pointer and all
referenced chunks. It refuses to write an output unless every chunk and the
resulting HTML match the expected SHA-256 checksums and byte counts.
"""
import argparse
import base64
import gzip
import hashlib
import json
from pathlib import Path
import sys

GALLERY = Path(__file__).resolve().parents[1]


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def restore():
    pointer = json.loads((GALLERY / 'checkpoints' / 'current.json').read_text(encoding='utf-8'))
    folder = GALLERY / 'checkpoints' / pointer['folder']
    manifest = json.loads((folder / 'manifest.json').read_text(encoding='utf-8'))
    parts = []
    for info in manifest['parts']:
        path = folder / info['file']
        data = path.read_bytes()
        if len(data) != info['encoded_chars'] or sha256(data) != info['sha256']:
            raise ValueError(f'Corrupted or missing checkpoint chunk: {path}')
        parts.append(data)
    encoded = b''.join(parts)
    if len(encoded) != manifest['encoded_chars']:
        raise ValueError('Checkpoint encoded length mismatch')
    compressed = base64.b64decode(encoded, validate=True)
    if len(compressed) != manifest['compressed_bytes'] or sha256(compressed) != manifest['compressed_sha256']:
        raise ValueError('Compressed checkpoint failed checksum')
    html = gzip.decompress(compressed)
    if len(html) != manifest['source_bytes'] or sha256(html) != manifest['source_sha256']:
        raise ValueError('Recovered HTML failed checksum')
    if manifest['source_sha256'] != pointer['sha256'] or len(html) != pointer['bytes']:
        raise ValueError('Current pointer does not match checkpoint manifest')
    required = [b'<!doctype html>', b'player-episode-nav', b'player-upnext',
                b'Watch History', b'settings-view', b'surface-enter']
    for token in required:
        if token not in html:
            raise ValueError(f'Expected Gallery feature marker missing: {token!r}')
    return html, manifest, pointer


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--verify-only', action='store_true', help='Do not write an output file')
    p.add_argument('--output', type=Path, default=Path('Gallery-current.html'))
    args = p.parse_args()
    try:
        html, manifest, pointer = restore()
        if not args.verify_only:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            temporary = args.output.with_suffix(args.output.suffix + '.tmp')
            temporary.write_bytes(html)
            temporary.replace(args.output)
        print('Gallery checkpoint verified:',pointer['folder'])
        print('SHA-256:',manifest['source_sha256'])
        print('Size:',len(html),'bytes')
        if not args.verify_only:
            print('Restored:',args.output)
    except Exception as exc:
        print('ERROR: Gallery checkpoint validation failed:',exc,file=sys.stderr)
        raise SystemExit(1)

if __name__ == '__main__':
    main()