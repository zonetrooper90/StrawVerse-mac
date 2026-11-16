#!/usr/bin/env python3
"""Approved 46px Player exception; align against the surrounding band."""
import hashlib,json
from pathlib import Path
GUARDS=json.loads("{\"gallery/src/styles/03-player-and-desktop-frame.css\":\"680ced13116f35e22a8ee9e71a666e5fbde80652\",\"gallery/src/styles/27-player-navigation-and-header-refinements.css\":\"1d5bfd4d555ab1f29001d47ddcb9a57ad82652eb\",\"gallery/src/styles/28-unified-headers-and-history-frame.css\":\"203324627cfc745ce85ccb51dd33cccd9d64b2ba\",\"gallery/tests/test_player_settings_regression.py\":\"9d7b7d6b5f2ee6ccb133e18cb35b3cff3111f60b\",\"gallery/audits/2026-11-16-compact-player-header-regression.py\":\"2d310ab51e8182ebc2e2f90f523bb7c6dad5f8a7\"}")
for name,expected in GUARDS.items():
    raw=Path(name).read_bytes()
    assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==expected,name
for name,edits in json.loads("{\"gallery/src/styles/03-player-and-desktop-frame.css\":[[\"body.player-view .workspace{padding:5px 13px 15px;scrollbar-gutter:auto}\",\"body.player-view .workspace{padding:3px 13px 15px;scrollbar-gutter:auto}\",1],[\"body.player-view .workspace{padding:5px 8px 14px}\",\"body.player-view .workspace{padding:3px 8px 14px}\",1],[\"100dvh - 182px\",\"100dvh - 183px\",2],[\"100dvh - 169px\",\"100dvh - 170px\",2]],\"gallery/src/styles/27-player-navigation-and-header-refinements.css\":[[\"  height: 45px;\\n  min-height: 45px;\\n\",\"  /* Compact height is owned by the Player exception in 28. */\\n\",1]],\"gallery/src/styles/28-unified-headers-and-history-frame.css\":[[\"/* Approved Player exception: retain the original 45px flex band, existing\\n   title/Back alignment and page gutters; the video frame is the boundary. */\",\"/* Approved Player exception: even 46px flex band with equal 3px gaps\\n   between the global header and video frame. Back is mathematically centered;\\n   the title alone retains the shared 1px optical correction. */\",1],[\"  height:45px;\\n  min-height:45px;\\n  border-bottom:0;\\n  margin-top:-5px; /* player .workspace top padding = 5px */\",\"  height:46px;\\n  min-height:46px;\\n  border-bottom:0;\\n  padding-block:0;\\n  margin-block:0 3px; /* match the 3px Player workspace top padding */\",1],[\"/* The original compact Player video budget lives in 03-player-and-desktop-frame.css\\n   (182px desktop / 169px narrow). No tall-header override is needed. */\",\"/* The compact Player video budget lives in 03-player-and-desktop-frame.css\\n   (183px desktop / 170px narrow, accounting for the 1px taller row).\\n   No tall-header override is needed. */\",1]],\"gallery/tests/test_player_settings_regression.py\":[[\"/'2026-11-16-compact-player-header-regression.py'\",\"/'2026-11-16-player-header-centerline-regression.py'\",1]]}").items():
    path=Path(name)
    source=path.read_text(encoding="utf-8")
    for old,replacement,count in edits:
        assert source.count(old)==count,(name,old,source.count(old),count)
        source=source.replace(old,replacement)
    path.write_text(source,encoding="utf-8")
print("PASS guarded 46px centered Player exception",flush=True)
