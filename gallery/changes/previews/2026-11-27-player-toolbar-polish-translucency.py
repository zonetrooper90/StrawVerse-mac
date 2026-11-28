#!/usr/bin/env python3
"""Approved Player Settings translucency correction, development preview only.

This source-only preview layers a .65-alpha glass panel on the immutable
seven-item/no-slide preview; full release, source and checkpoint stay unchanged.
"""
import hashlib
from pathlib import Path
import runpy

PREVIEW_CONTRACT={
  "slug": "2026-11-27-player-toolbar-polish-translucency",
  "scope": "player-toolbar-polish",
  "approval_heading": "## 2026-11-27 — Approved current-release lightweight-first workflow and seven-item Player/toolbar polish",
  "base_source_blobs": {
    "gallery/src/js/11f-player-motion.js": "b14a561704782fa2a3c6bf700c302ff439688106",
    "gallery/src/styles/26-player-icons-and-timelines.css": "c736bb80c51b9d53b3c6d32154327cf3e5117660",
    "gallery/src/js/11b-player-page.js": "0aaa01c361849af728e5da796bfe764f785c9246",
    "gallery/src/js/11g-player-playback.js": "ba72c6ca997908777a2be0bdeae442f5822818e7",
    "gallery/src/js/11h-player-controls.js": "e690cb7dd7aeb8cfa99c35517b1124e5069b4d78",
    "gallery/src/styles/28-unified-headers-and-history-frame.css": "008f1f35b4bb41f01553bd4800adb2465d57cd99"
  },
  "source_blobs": {
    "gallery/src/js/11f-player-motion.js": "d3f7f2c0de39cfea69c0169f71af04ad63487901",
    "gallery/src/styles/26-player-icons-and-timelines.css": "b5d3e396b46d570445de29f3b986303f6278faa0",
    "gallery/src/js/11b-player-page.js": "46579ad867f0d43c23ef43fa37a0a155092e8ab2",
    "gallery/src/js/11g-player-playback.js": "a1bc6a5cae90739abb74325f16e2e96f042a391a",
    "gallery/src/js/11h-player-controls.js": "b787a3acc410ab37fe51bb2fc235c6d4ab07aa52",
    "gallery/src/styles/28-unified-headers-and-history-frame.css": "b226fffa0211a66e0b2c084087ebe1ad42e6c9e6"
  },
  "preview_sha256": "0b5fc52a2d405fa10e2b8ec238b96a26d19b9385b25c6c29acf2f3053d06b7f4",
  "preview_bytes": 660618
}

runpy.run_path("gallery/changes/previews/2026-11-27-player-toolbar-polish-no-slide.py",run_name="__main__")
source=Path("gallery/src/styles/26-player-icons-and-timelines.css")
raw=source.read_text(encoding="utf-8")
old="color:#f8f6fa;background:rgba(17,17,21,.84);"
new="color:#f8f6fa;background:rgba(17,17,21,.65);"
def git_blob(data):
 return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\x00"+data).hexdigest()
assert git_blob(raw.encode("utf-8"))=="d6ff87377a617ca21109bf1fc8ae3495421e3782","approved no-slide preview CSS drift"
assert raw.count(old)==1,"expected one Player Settings translucent background"
candidate=raw.replace(old,new,1).encode("utf-8")
assert git_blob(candidate)==PREVIEW_CONTRACT["source_blobs"][str(source)],"translucency candidate CSS hash mismatch"
source.write_bytes(candidate)
print("PASS Player Settings glass opacity .65; all seven refinements and no-slide preserved",flush=True)
