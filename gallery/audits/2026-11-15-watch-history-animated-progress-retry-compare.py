#!/usr/bin/env python3
"""Test-only retry: exact original candidate HTML in both modes."""
import hashlib
from pathlib import Path
expected={"gallery/Gallery-current.html":"dd93f30c2bc170d08f43ceaa459205bd4b157e8d40d2df8f29e0133de10134d3",
          "gallery/Gallery-development.html":"76ede7481d40dfc3b0e674c4808de45df468818792e5d4dd937ae205cb953da3"}
for name,digest in expected.items():
    actual=hashlib.sha256(Path(name).read_bytes()).hexdigest()
    assert actual==digest,(name,actual,digest)
    print("PASS byte-identical original animation candidate",name,actual,flush=True)
