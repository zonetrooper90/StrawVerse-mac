#!/usr/bin/env python3
import hashlib,runpy,subprocess
from pathlib import Path
S=runpy.run_path("gallery/changes/pending/2026-11-14-discover-search-scroll-restoration.py")
mode="full"
path,digest=S["FILES"][mode]
old=subprocess.check_output(["git","show",S["BASE"]+":"+path])
assert hashlib.sha256(old).hexdigest()==digest
assert Path(path).read_bytes()==S["transform"](old),"Unexpected application byte changes"
print("PASS: candidate HTML equals exact approved transformation of verified baseline",mode,flush=True)
runpy.run_path("gallery/tests/test_discover_search_scroll.py")["run"](mode,"reduce")
