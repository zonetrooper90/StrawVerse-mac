#!/usr/bin/env python3
"""Require exact byte identity to the previously prepared global History trial."""
from pathlib import Path
import hashlib
for name,expected in (
 ("gallery/Gallery-current.html","4c8cc55e6c7e4c001b37934c91c2ce0dd4db9e39073ade3d060bf43f49f1eb6f"),
 ("gallery/Gallery-development.html","7613bb3a37b7e826f28b23c59e033ae408ee81baf7c7785d7d47e1e9d7fa9a98"),
):
    digest=hashlib.sha256(Path(name).read_bytes()).hexdigest()
    assert digest==expected,(name,digest,expected)
    print("PASS byte-identical original candidate",name,digest,flush=True)
