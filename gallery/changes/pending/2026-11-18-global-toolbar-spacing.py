#!/usr/bin/env python3
"""Approved shared global toolbar spacing correction, CSS-only application patch."""
import hashlib,json
from pathlib import Path
for name,expected in json.loads("{\"gallery/src/styles/09-search.css\":\"99219bd2f0e6107c0bdaee11e42afaa2ad1a2d75\",\"gallery/tests/test_history_row_maintenance.py\":\"10c523812380fd137be62d69760b97ebc0baa3a1\"}").items():
    raw=Path(name).read_bytes()
    assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==expected,name
pointer=json.loads(Path("gallery/checkpoints/current.json").read_text())
assert pointer["folder"]=="2026-11-18-a2-background-operation-ownership"
assert pointer["sha256"]=="f4d7d67df2f04ff9835c800b2fcd7138d1a1274ef94ab17e9ac3f5858b22ea94"
assert pointer["bytes"]==6938822
for name,changes in json.loads("{\"gallery/src/styles/09-search.css\":[[\".header-search,.header-search.is-open{flex:0 0 38px;width:38px;min-width:38px;background:transparent;border-color:transparent;box-shadow:none}\",\".header-search,.header-search.is-open{flex:0 0 40px;width:40px;min-width:40px;height:40px;background:transparent;border:0;box-shadow:none}\",1],[\"right:calc(100% + 7px);left:auto;\",\"right:calc(100% + 8px);left:auto;\",1],[\".brand-row.is-searching .header-search{flex:0 0 38px}\",\".brand-row.is-searching .header-search{flex:0 0 40px}\",1],[\"/* Global Watch History shortcut — keep the existing Search/Settings geometry. */\",\"/* Global Watch History shortcut — shared 40px utility buttons and 8px gaps. */\",1]],\"gallery/tests/test_history_row_maintenance.py\":[[\"subprocess.run([sys.executable,str(Path(__file__).resolve().parents[1]/'audits'/'2026-11-16-a2-player-session-ownership-regression.py'),sys.argv[1]],check=True)\",\"subprocess.run([sys.executable,str(Path(__file__).resolve().parents[1]/'audits'/'2026-11-16-a2-player-session-ownership-regression.py'),sys.argv[1]],check=True)\\n\\n# Mandatory shared global toolbar spacing and fixed Search geometry regression.\\nsubprocess.run([sys.executable,str(Path(__file__).resolve().parents[1]/'audits'/'2026-11-18-global-toolbar-spacing-regression.py'),sys.argv[1]],check=True)\",1]]}").items():
    path=Path(name)
    source=path.read_text(encoding="utf-8")
    for old,new,count in changes:
        assert source.count(old)==count,(name,old,source.count(old),count)
        source=source.replace(old,new)
    path.write_text(source,encoding="utf-8")
print("PASS guarded global toolbar spacing correction",flush=True)
