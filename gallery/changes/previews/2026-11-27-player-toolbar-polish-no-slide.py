#!/usr/bin/env python3
"""Approved follow-up visual preview: remove only the sideways Player Settings submenu slide.

User asked 2026-11-28 to remove the Player Settings sliding animation.
Preserve existing seven-item source-only refinements, popup entrance motion,
Settings icon animation, controls, accessibility and full-release baseline.
Do not publish HTML or alter canonical source. Run only inside isolated worktree.
"""
import hashlib
from pathlib import Path
import runpy

PREVIEW_CONTRACT={
  "slug": "2026-11-27-player-toolbar-polish-no-slide",
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
    "gallery/src/styles/26-player-icons-and-timelines.css": "d6ff87377a617ca21109bf1fc8ae3495421e3782",
    "gallery/src/js/11b-player-page.js": "46579ad867f0d43c23ef43fa37a0a155092e8ab2",
    "gallery/src/js/11g-player-playback.js": "a1bc6a5cae90739abb74325f16e2e96f042a391a",
    "gallery/src/js/11h-player-controls.js": "b787a3acc410ab37fe51bb2fc235c6d4ab07aa52",
    "gallery/src/styles/28-unified-headers-and-history-frame.css": "b226fffa0211a66e0b2c084087ebe1ad42e6c9e6"
  },
  "preview_sha256": "dbb5635e9836b52246bbd0a84898565ce43b3fab8f5966cb71370b5246811318",
  "preview_bytes": 660618
}

# Replay the exact previously approved seven-item source patch on the clean
# immutable verified release before applying one scoped CSS-only adjustment.
runpy.run_path("gallery/changes/previews/2026-11-27-player-toolbar-polish.py", run_name="__main__")
source=Path("gallery/src/styles/26-player-icons-and-timelines.css")
raw=source.read_text(encoding="utf-8")
old="/* Submenus advance within the same anchored menu, without shifting its frame. */\n.player-settings-popover-items{display:flex;flex-direction:column;padding:4px 0;animation:player-settings-section-in 160ms ease-out both}\n@keyframes player-settings-section-in{from{opacity:.6;transform:translateX(7px)}to{opacity:1;transform:translateX(0)}}"
new="/* Submenus switch immediately, without horizontal movement or fades. */\n.player-settings-popover-items{display:flex;flex-direction:column;padding:4px 0}"
def git_blob(data):
 return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\x00"+data).hexdigest()
assert git_blob(raw.encode("utf-8"))=="41dbc6178d04a36823c31d5612b5d893beec8968", "previous seven-item source drift"
assert raw.count(old)==1,"Player Settings horizontal slide selector drift"
result=raw.replace(old,new,1).encode("utf-8")
assert git_blob(result)==PREVIEW_CONTRACT["source_blobs"][str(source)],"new CSS blob mismatch"
source.write_bytes(result)
print("PASS Player Settings submenu switches instantly; popup entrance and all seven fixes preserved",flush=True)
