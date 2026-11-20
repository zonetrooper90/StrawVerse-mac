#!/usr/bin/env python3
"""G1.1: click-driven toolbar animation and 450ms Settings. Exact source only.

The guarded publisher validates the authoritative checkpoint, stages source
fragments, regenerates both builds, tests and archives only after every gate
passes. This script never edits generated HTML, assets or checkpoints.
"""
from pathlib import Path
import hashlib

def git_blob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+bytes([0])+raw).hexdigest()

PATCHES = [
["gallery/src/js/07a-watch-history.js","f83c1d58e704a95a1981df960d596691f0669309","785d6cbd57f0cc4b4fbee4a0e8462f548065d0e8",[[" button.setAttribute('aria-pressed',String(whOpen&&!settings));\n}"," button.setAttribute('aria-pressed',String(whOpen&&!settings));\n // Keep the icon's settled state if Settings temporarily overlays History.\n button.dataset.g1Active=String(whOpen);\n}"],["function whEnter(){\n if(whOpen||state.playback||document.body.classList.contains('settings-view')||modalHost.firstChild)return;\n transitionGalleryStage(()=>{","function whEnter(){\n if(whOpen||state.playback||document.body.classList.contains('settings-view')||modalHost.firstChild)return;\n // Animate on the accepted action, before the 150ms outgoing page fade.\n document.getElementById('header-watch-history').dataset.g1Active='true';\n transitionGalleryStage(()=>{"],["function whExit({renderAfter=true}={}){\n if(!whOpen)return;\n const exit=()=>{","function whExit({renderAfter=true}={}){\n if(!whOpen)return;\n // Reverse the ring immediately, including History's Back action.\n document.getElementById('header-watch-history').dataset.g1Active='false';\n const exit=()=>{"]]],
["gallery/src/js/19e-settings-navigation.js","d5a2e4ae54a04edbd4a0e315404580ae82259621","107f1a7b8782c610185d344317d846bfaa44e1f0",[[" gallerySettingsOpening=true;\n transitionGalleryStage(()=>{"," gallerySettingsOpening=true;\n // Decouple immediate slider feedback from the delayed route commit.\n document.getElementById('settings').dataset.g1Active='true';\n transitionGalleryStage(()=>{"],[" settingsButton.setAttribute('aria-expanded','true');\n settingsButton.setAttribute('aria-controls','settings-page');"," settingsButton.setAttribute('aria-expanded','true');\n settingsButton.dataset.g1Active='true';\n settingsButton.setAttribute('aria-controls','settings-page');"],["function closeSettings(){\n if(!document.body.classList.contains('settings-view')||settingsClosing)return;\n cancelGalleryTextColorPopover(false);","function closeSettings(){\n if(!document.body.classList.contains('settings-view')||settingsClosing)return;\n // Reverse immediately for toolbar, Back and Escape without moving the page midpoint.\n document.getElementById('settings').dataset.g1Active='false';\n cancelGalleryTextColorPopover(false);"],["  button.setAttribute('aria-expanded','false');\n  syncHeaderWatchHistory();","  button.setAttribute('aria-expanded','false');\n  button.dataset.g1Active='false';\n  syncHeaderWatchHistory();"]]],
["gallery/src/styles/28-unified-headers-and-history-frame.css","f4912c28aa853f6f4c30350f4241ea6ea84a97d2","e808e4caaa890008dc968e185116c8d952741085",[["body[data-theme] #header-watch-history[aria-pressed=\"true\"]:not(:disabled),\nbody[data-theme] #settings[aria-expanded=\"true\"]{","body[data-theme] #header-watch-history[data-g1-active=\"true\"]:not(:disabled),\nbody[data-theme] #settings[data-g1-active=\"true\"]{"],["body[data-theme] #header-watch-history[aria-pressed=\"true\"]:hover:not(:disabled),\nbody[data-theme] #settings[aria-expanded=\"true\"]:hover:not(:disabled){background:var(--circle-hover)}","body[data-theme] #header-watch-history[data-g1-active=\"true\"]:hover:not(:disabled),\nbody[data-theme] #settings[data-g1-active=\"true\"]:hover:not(:disabled){background:var(--circle-hover)}"],["#header-watch-history[aria-pressed=\"true\"] .g1-history-rim{transform:rotate(-360deg)}","#header-watch-history[data-g1-active=\"true\"] .g1-history-rim{transform:rotate(-360deg)}"],[" transform:translateX(0);transition:transform .3s cubic-bezier(.22,.72,.2,1);"," transform:translateX(0);transition:transform .45s cubic-bezier(.22,.72,.2,1);"],["#settings[aria-expanded=\"true\"] .g1-settings-knob.upper{transform:translateX(6px)}","#settings[data-g1-active=\"true\"] .g1-settings-knob.upper{transform:translateX(6px)}"],["#settings[aria-expanded=\"true\"] .g1-settings-knob.lower{transform:translateX(-6px)}","#settings[data-g1-active=\"true\"] .g1-settings-knob.lower{transform:translateX(-6px)}"],["body[data-theme] #header-watch-history:hover:not(:disabled),\nbody[data-theme] #settings:hover:not(:disabled){\n background:var(--circle-hover);border-color:var(--sat-border);\n}","body[data-theme] #header-watch-history:hover:not(:disabled),\nbody[data-theme] #settings:hover:not(:disabled){\n background:var(--circle-hover);border-color:var(--sat-border);\n}\n/* The legacy aria-pressed border must not outlive an immediate G1 close.\n   Keep ordinary and hover outlines intact throughout the outgoing fade. */\nbody[data-theme] #header-watch-history[data-g1-active=\"false\"]:not(:disabled){\n color:var(--fg);border-color:var(--circle-border);\n}\nbody[data-theme] #header-watch-history[data-g1-active=\"false\"]:hover:not(:disabled){\n border-color:var(--sat-border);\n}"]]]
]
for path,old_sha,new_sha,changes in PATCHES:
    p=Path(path)
    old=p.read_bytes()
    if git_blob(old)!=old_sha:
        raise RuntimeError("G1.1 baseline source drift: "+path)
    next_text=old.decode("utf-8")
    for before,after in changes:
        if next_text.count(before)!=1:
            raise RuntimeError("G1.1 source patch anchor is not unique: "+path+" "+before[:90])
        next_text=next_text.replace(before,after,1)
    raw=next_text.encode("utf-8")
    if raw==old or git_blob(raw)!=new_sha:
        raise RuntimeError("G1.1 generated source hash differs: "+path)
    p.write_bytes(raw)
    if git_blob(p.read_bytes())!=new_sha:
        raise RuntimeError("G1.1 write/read-back differs: "+path)
    print("Verified exact G1.1 source:",path,new_sha,flush=True)
print("G1.1 source-only patch done; guarded publisher owns output and checkpoint.",flush=True)
