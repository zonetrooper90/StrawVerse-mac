#!/usr/bin/env python3
"""Mandatory byte-for-byte identity with the diagnosed Search rail retry."""
import hashlib
from pathlib import Path
for name,expected in (
    ("Gallery-current.html","c6a0cd867be620287cc21cc9ce8d2060635ae0be97f024c2fcd7b40d1a6fa2dd"),
    ("Gallery-development.html","772f46684ccdd99ddbd4196eefdac73f942c4ad63d03bc64316e35275ec6b0e1"),
):
    raw=(Path("gallery")/name).read_bytes()
    digest=hashlib.sha256(raw).hexdigest()
    assert digest==expected,(name,digest,expected)
    print("PASS byte-identical approved Search candidate",name,len(raw),digest,flush=True)
