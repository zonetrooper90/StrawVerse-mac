#!/usr/bin/env python3
"""Approved byte-identical A2.4 retry; original application patch retained."""
import hashlib,runpy
from pathlib import Path
original=Path("gallery/changes/pending/2026-11-17-a2-dialog-settings-ownership.py")
raw=original.read_bytes()
assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()=="42383cb4a5c09f42810f4ea17022bb8ca62a97b1",original
runpy.run_path(str(original),run_name="__main__")
path=Path("gallery/tests/test_player_settings_regression.py")
source=path.read_text(encoding="utf-8")
old="2026-11-17-a2-dialog-settings-ownership-regression.py"
new="2026-11-17-a2-dialog-settings-ownership-retry-regression.py"
assert source.count(old)==1
path.write_text(source.replace(old,new),encoding="utf-8")
print("PASS exact original A2.4 application patch; corrected strict test entrypoint",flush=True)
