#!/usr/bin/env python3
"""Approved A2.3 History expansion listener ownership; no CSS or progress changes."""
import hashlib,json
from pathlib import Path
GUARDS=json.loads("{\"gallery/src/js/07a-watch-history.js\":\"00eaf2a38071bcd49c9a79793bf8352ee0cf6650\",\"gallery/tests/test_player_settings_regression.py\":\"ab11adf241d077bfb7d494476de77d8195aecca8\",\"gallery/audits/2026-11-16-a2-history-expansion-listener-diagnostic.py\":\"8436ff06f25eee1b08b8c69932059c6fcffcd891\"}")
for name,expected in GUARDS.items():
    raw=Path(name).read_bytes()
    assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==expected,name
for name,edits in json.loads("{\"gallery/src/js/07a-watch-history.js\":[[\" row.querySelector('.wh-episodes').addEventListener('transitionend',event=>{\\n  if(event.propertyName==='grid-template-rows')updateTabScrollOverlay();\\n },{once:true});\\n\",\"\",1],[\"/* All page actions live in one delegated listener; episode toggles don't rebuild their list. */\",\"/* The persistent screen owns transition completion, not individual toggles.\\n * Reversals and reduced motion cannot accumulate row listeners. Ignore events\\n * from descendants, replaced panels and intentionally suspended History. */\\nfunction whHandleExpansionTransition(event){\\n if(!whOpen||screen.hidden||document.body.classList.contains('settings-view')||\\n    event.propertyName!=='grid-template-rows'||event.pseudoElement)return;\\n const panel=event.target;\\n if(!(panel instanceof Element)||!panel.matches('.wh-episodes')||!panel.isConnected)return;\\n const root=screen.querySelector('#wh-root'),row=panel.parentElement;\\n if(!root||!row?.matches('.wh-season[data-wh-row]')||row.closest('#wh-root')!==root||\\n    row.querySelector('.wh-episodes')!==panel)return;\\n updateTabScrollOverlay();\\n}\\nscreen.addEventListener('transitionend',whHandleExpansionTransition);\\nscreen.addEventListener('transitioncancel',whHandleExpansionTransition);\\n/* All page actions live in one delegated listener; episode toggles don't rebuild their list. */\",1]],\"gallery/tests/test_player_settings_regression.py\":[[\"subprocess.run([sys.executable,str(Path(__file__).resolve().parents[1]/'audits'/'2026-11-16-a2-detail-rail-ownership-regression.py'),sys.argv[1]],check=True)\",\"subprocess.run([sys.executable,str(Path(__file__).resolve().parents[1]/'audits'/'2026-11-16-a2-detail-rail-ownership-regression.py'),sys.argv[1]],check=True)\\n\\n# Mandatory A2.3 History expansion transition ownership regression.\\nsubprocess.run([sys.executable,str(Path(__file__).resolve().parents[1]/'audits'/'2026-11-16-a2-history-expansion-listener-ownership-regression.py'),sys.argv[1]],check=True)\",1]]}").items():
    path=Path(name)
    source=path.read_text(encoding="utf-8")
    for old,replacement,count in edits:
        assert source.count(old)==count,(name,old,source.count(old),count)
        source=source.replace(old,replacement)
    path.write_text(source,encoding="utf-8")
print("PASS guarded A2.3 shared History transition ownership",flush=True)
