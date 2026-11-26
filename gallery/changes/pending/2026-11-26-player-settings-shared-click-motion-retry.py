#!/usr/bin/env python3
"""Guarded retry of approved Player Settings G1 click motion.

Replay the exact original approved candidate in the publisher's disposable
worktree. Correct only its Player Settings early-reopen guard. Retain the
existing modal() replacement and closing semantics, and restore the active
icon pose after any outgoing dialog's synchronous will-close notification.
The dedicated original comparison is extended (not weakened) for immediate
reopening under normal and reduced motion.
"""
import ast
import hashlib
from pathlib import Path
import runpy

def git_blob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

original=Path('gallery/changes/pending/2026-11-26-player-settings-shared-click-motion.py')
assert git_blob(original.read_bytes())=='6a6e0514820c76eb948e0ece781a214356fff21b', 'Original approved Player Settings patch drift'
failed_comparison=Path('gallery/audits/2026-11-26-player-settings-shared-click-motion-compare.py')
assert git_blob(failed_comparison.read_bytes())=='ad24cb79aab608bfac1ed9108318e5f7884748cc', 'Historical first comparison changed'
corrected=Path('gallery/audits/2026-11-26-player-settings-shared-click-motion-retry-compare.py')
assert git_blob(corrected.read_bytes())=='085bdc1e8b985a7eff3e0474ebc62af380d64c00', 'Approved retry comparison drift'
comparison=corrected.read_text(encoding='utf-8')
ast.parse(comparison, filename=str(corrected))
for required in (
 "assert tested==48,tested",
 "(['ease']*2 if motion=='reduce' else [EXPECTED_EASE]*2)",
 "rapid dialog replacement",
 "rapid final reverse",
 "settings.evaluate('(el)=>el.click()')",
):
    assert comparison.count(required)==1,(required,'corrected regression missing or duplicated')

# Replay only on the exact immutable original source baselines. This writes
# the approved five modular source fragments, never the tracked HTML.
runpy.run_path(str(original),run_name='__main__')
outputs={
 'gallery/src/js/11b-player-page.js':'0aaa01c361849af728e5da796bfe764f785c9246',
 'gallery/src/js/11h-player-controls.js':'fc433a03d09d1533d9f263c221731d22e4e34b11',
 'gallery/src/js/11j-dialog-lifecycle.js':'aa8fd2a4b61d145ab4181b5d46c08d39718e4801',
 'gallery/src/styles/26-player-icons-and-timelines.css':'6b3343dbf4462daced4ff772388f591fd9b306cc',
 'gallery/src/styles/28-unified-headers-and-history-frame.css':'008f1f35b4bb41f01553bd4800adb2465d57cd99',
}
for path,expected in outputs.items():
    actual=git_blob(Path(path).read_bytes())
    assert actual==expected,(path,'unapproved source drift',actual,expected)

controls=Path('gallery/src/js/11h-player-controls.js')
source=controls.read_text(encoding='utf-8')
old_guard="  if(modalHost.firstElementChild)return;\n"
assert source.count(old_guard)==1,'Original reentry guard missing'
source=source.replace(old_guard,
 "  // Preserve the original Player's synchronous reopen/replacement while an\n"
 "  // older modal is still exiting; modal() owns the existing exit cleanup.\n",1)
old_anchor=(
 "  if(!overlay?.querySelector('.dialog[aria-label=\"Player settings\"]')){\n"
 "   playerSettingsButton.dataset.g1Active='false';return;\n"
 "  }\n"
 "  // Session-bound, one-dialog listener:"
)
new_anchor=(
 "  if(!overlay?.querySelector('.dialog[aria-label=\"Player settings\"]')){\n"
 "   playerSettingsButton.dataset.g1Active='false';return;\n"
 "  }\n"
 "  // Replacing an outgoing Player dialog dispatched its will-close callback\n"
 "  // during openPlayerSettings(). Keep the just-opened dialog in active pose.\n"
 "  // Both state writes occur within the same click before browser paint.\n"
 "  playerSettingsButton.dataset.g1Active='true';\n"
 "  // Session-bound, one-dialog listener:"
)
assert source.count(old_anchor)==1,'Expected one original Player dialog ownership branch'
source=source.replace(old_anchor,new_anchor,1)
assert source.count("playerSettingsButton.dataset.g1Active='true';")==2,'Open and new-dialog state must both be explicit'
assert "if(modalHost.firstElementChild)return;" not in source,'Old reentry blocker remained'
controls.write_text(source,encoding='utf-8')
assert git_blob(controls.read_bytes())!='fc433a03d09d1533d9f263c221731d22e4e34b11'
for path,expected in outputs.items():
    if path==str(controls):continue
    assert git_blob(Path(path).read_bytes())==expected,(path,'Approved icon/motion changed')
print('PASS: exact original G1 SVG, CSS, dialog lifecycle and full-screen behavior; Player reentry repaired; strict 48-context plus rapid-reopen comparison pinned',flush=True)
