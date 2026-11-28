#!/usr/bin/env python3
"""Publish only the user-approved seven-item Player/toolbar polish, no-slide, and .65 glass.

This runs inside the existing controlled publisher candidate worktree.
Use the already independently verified, exact source-only preview scripts.
No image, asset, generated HTML, checkpoint, workflow or test is edited here.
"""
import ast
import hashlib
from pathlib import Path
import runpy

SCRIPT_BLOBS={
 "gallery/changes/previews/2026-11-27-player-toolbar-polish.py":"b261c267084d8d08875d307222f079f24e17ca48",
 "gallery/changes/previews/2026-11-27-player-toolbar-polish-no-slide.py":"481afd7e57629ce4991bd41a10bd7489a6ae32a0",
 "gallery/changes/previews/2026-11-27-player-toolbar-polish-translucency.py":"329ef2a8e40086a437ed0a4c6d657c5b44b8c6e7",
}
ORIGINAL_BLOBS={
 "gallery/src/js/11f-player-motion.js":"b14a561704782fa2a3c6bf700c302ff439688106",
 "gallery/src/styles/26-player-icons-and-timelines.css":"c736bb80c51b9d53b3c6d32154327cf3e5117660",
 "gallery/src/js/11b-player-page.js":"0aaa01c361849af728e5da796bfe764f785c9246",
 "gallery/src/js/11g-player-playback.js":"ba72c6ca997908777a2be0bdeae442f5822818e7",
 "gallery/src/js/11h-player-controls.js":"e690cb7dd7aeb8cfa99c35517b1124e5069b4d78",
 "gallery/src/styles/28-unified-headers-and-history-frame.css":"008f1f35b4bb41f01553bd4800adb2465d57cd99",
}
FINAL_BLOBS={
 "gallery/src/js/11f-player-motion.js":"d3f7f2c0de39cfea69c0169f71af04ad63487901",
 "gallery/src/styles/26-player-icons-and-timelines.css":"b5d3e396b46d570445de29f3b986303f6278faa0",
 "gallery/src/js/11b-player-page.js":"46579ad867f0d43c23ef43fa37a0a155092e8ab2",
 "gallery/src/js/11g-player-playback.js":"a1bc6a5cae90739abb74325f16e2e96f042a391a",
 "gallery/src/js/11h-player-controls.js":"b787a3acc410ab37fe51bb2fc235c6d4ab07aa52",
 "gallery/src/styles/28-unified-headers-and-history-frame.css":"b226fffa0211a66e0b2c084087ebe1ad42e6c9e6",
}
def blob(data):
 return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
def verify(entries,label):
 for path,expected in entries.items():
  actual=blob(Path(path).read_bytes())
  assert actual==expected,(label,path,actual,expected)

assert set(ORIGINAL_BLOBS)==set(FINAL_BLOBS)
verify(SCRIPT_BLOBS,"immutable approved preview script drift")
verify(ORIGINAL_BLOBS,"verified original release source drift")
for path in SCRIPT_BLOBS:
 ast.parse(Path(path).read_text(encoding="utf-8"),filename=path)
runpy.run_path("gallery/changes/previews/2026-11-27-player-toolbar-polish-translucency.py",run_name="__main__")
verify(FINAL_BLOBS,"approved final source differs from verified visual preview")
css=Path("gallery/src/styles/26-player-icons-and-timelines.css").read_text(encoding="utf-8")
assert "background:rgba(17,17,21,.65);" in css and "player-settings-section-in" not in css
print("PASS exact six approved source fragments = independently checked translucent no-slide preview; release compiler/publisher owns HTML and new checkpoint",flush=True)
