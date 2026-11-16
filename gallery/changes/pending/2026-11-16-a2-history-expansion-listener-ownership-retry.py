#!/usr/bin/env python3
"""Replay the exact approved A2.3 app change; only replace the pending test hook."""
import hashlib,runpy
from pathlib import Path
original=Path("gallery/changes/pending/2026-11-16-a2-history-expansion-listener-ownership.py")
raw=original.read_bytes()
assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()=="546da0c36211375e59efc5b47b7023139c492370",original
runpy.run_path(str(original),run_name="__main__")
runner=Path("gallery/tests/test_player_settings_regression.py")
source=runner.read_text(encoding="utf-8")
old="'2026-11-16-a2-history-expansion-listener-ownership-regression.py'"
new="'2026-11-16-a2-history-expansion-listener-ownership-retry-regression.py'"
assert source.count(old)==1
runner.write_text(source.replace(old,new),encoding="utf-8")
print("PASS exact approved A2.3 application replay with synchronized mandatory regression",flush=True)
