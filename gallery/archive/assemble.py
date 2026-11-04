#!/usr/bin/env python3
"""Reassemble exact Gallery HTML snapshots from the GitHub archive chunks."""
from pathlib import Path
import json, hashlib
root=Path(__file__).resolve().parent
manifest=root/"manifest.json"
if not manifest.exists():
    print("No manifest yet")
    raise SystemExit(0)
files=json.loads(manifest.read_text())["files"]
out=root/"html"
out.mkdir(exist_ok=True)
for name, info in files.items():
    folder=root/"chunks"/name
    parts=[folder/f"part-{i:03d}" for i in range(1,info["parts"]+1)]
    if not all(p.exists() for p in parts):
        raise SystemExit("Missing archive part for "+name)
    data=b"".join(p.read_bytes() for p in parts)
    digest=hashlib.sha256(data).hexdigest()
    assert len(data)==info["size"] and digest==info["sha256"],"Checksum failed for "+name
    (out/name).write_bytes(data)
    print("Verified:",name,digest)
