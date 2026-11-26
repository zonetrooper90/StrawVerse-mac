#!/usr/bin/env python3
"""Approved Player Settings click-driven reuse of existing G1 sliders.

Only Player Settings SVG/button state, original shared G1 knob selectors,
Player-size glyph layout, and one passive modal-lifecycle notification change.
Do not modify global Settings behavior or generated HTML directly.
"""
import hashlib
import re
from pathlib import Path

EXPECT={
 'gallery/src/js/11b-player-page.js':'d13791c0c18fe1b79964f9dc19b6fb02a7a04782',
 'gallery/src/js/11h-player-controls.js':'720bafd0b7a6dbfc59afebbef6532cdbee7b66aa',
 'gallery/src/js/11j-dialog-lifecycle.js':'6d5a7c8a12b0902554858708f6bb14b129bdd2d4',
 'gallery/src/styles/26-player-icons-and-timelines.css':'5eb8ab5e2be345d80451fdee671cb7ee5cc2fb5a',
 'gallery/src/styles/28-unified-headers-and-history-frame.css':'a8cd52c9a9dd1b9b1b8c6760db3c850ce711542c',
 'gallery/src/js/19h-bootstrap.js':'08ef24222d42057b7a4964943e6d497cf44c0c4b',
 'gallery/src/js/11e-player-subtitles.js':'8c4ee78ab4ebce8fe918f438005637fcd50f1dc7',
}
def blob(raw):
 return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def change(txt,before,after,path):
 assert txt.count(before)==1,(path,'nonunique or missing guarded exact anchor',before[:100])
 return txt.replace(before,after,1)

source={}
for path,expected in EXPECT.items():
 raw=Path(path).read_bytes()
 assert blob(raw)==expected,(path,'baseline drift',blob(raw),expected)
 source[path]=raw.decode('utf-8')
header=source['gallery/src/js/19h-bootstrap.js']
pattern=r"document\.getElementById\('settings'\)\.innerHTML='(?P<svg><svg .*?</svg>)';"
matched=list(re.finditer(pattern,header))
assert len(matched)==1,'Could not uniquely reuse existing main Settings SVG'
original_svg=matched[0].group('svg')
assert original_svg.count('g1-settings-knob')==2
assert 'width="23" height="23"' in original_svg and 'stroke-width="1.7"' in original_svg
assert '<path d="M4 7h16M4 17h16"/>' in original_svg
assert '<circle cx="9" cy="7" r="2" fill="var(--window)"/>' in original_svg
assert '<circle cx="15" cy="17" r="2" fill="var(--window)"/>' in original_svg
# Same SVG source and SVG-space six-unit knob translations as the main Settings.
# Render at the Player's previously approved 21px glyph scale.
player_svg=original_svg.replace('width="23" height="23"','width="21" height="21"')
page='gallery/src/js/11b-player-page.js'
before='<button type="button" class="player-icon" id="player-settings" aria-label="Player settings">'+'$'+"{icon('settings',21)}"+'</button>'
after=before.replace('$'+"{icon('settings',21)}",player_svg)
source[page]=change(source[page],before,after,page)

controls='gallery/src/js/11h-player-controls.js'
entry=" document.getElementById('player-settings').onclick=()=>openPlayerSettings(v);"
replacement=""" const playerSettingsButton=document.getElementById('player-settings');
 playerSettingsButton.dataset.g1Active='false';
 playerSettingsButton.onclick=()=>{
  if(modalHost.firstElementChild)return;
  // Begin the same G1 slider move on the accepted click, not modal appearance.
  playerSettingsButton.dataset.g1Active='true';
  openPlayerSettings(v);
  const overlay=modalHost.querySelector('.overlay');
  if(!overlay?.querySelector('.dialog[aria-label="Player settings"]')){
   playerSettingsButton.dataset.g1Active='false';return;
  }
  // Session-bound, one-dialog listener: immediate reverse on Apply, X,
  // Escape, backdrop, or replacement; no global Settings state changes.
  on(overlay,'gallery-modal-will-close',()=>{
   playerSettingsButton.dataset.g1Active='false';
  });
 };
"""
source[controls]=change(source[controls],entry,replacement.rstrip('\n'),controls)

modal='gallery/src/js/11j-dialog-lifecycle.js'
source[modal]=change(source[modal],
 " if(outgoing)retireModalWork(outgoing);",
 " if(outgoing){outgoing.dispatchEvent(new Event('gallery-modal-will-close'));retireModalWork(outgoing);}",
 modal)
source[modal]=change(source[modal],
 " if(!overlay||overlay.classList.contains('is-closing'))return;\n cancelModalExit();",
 " if(!overlay||overlay.classList.contains('is-closing'))return;\n // Notify only this dialog before its exit (or reduced-motion removal).\n overlay.dispatchEvent(new Event('gallery-modal-will-close'));\n cancelModalExit();",
 modal)

styles='gallery/src/styles/28-unified-headers-and-history-frame.css'
css=source[styles]
css=change(css,"#settings .g1-settings-knob{\n",
 "#settings .g1-settings-knob,\n#player-settings .g1-settings-knob{\n",styles)
css=change(css,
 '#settings[data-g1-active="true"] .g1-settings-knob.upper{transform:translateX(6px)}',
 '#settings[data-g1-active="true"] .g1-settings-knob.upper,\n#player-settings[data-g1-active="true"] .g1-settings-knob.upper{transform:translateX(6px)}',styles)
css=change(css,
 '#settings[data-g1-active="true"] .g1-settings-knob.lower{transform:translateX(-6px)}',
 '#settings[data-g1-active="true"] .g1-settings-knob.lower,\n#player-settings[data-g1-active="true"] .g1-settings-knob.lower{transform:translateX(-6px)}',styles)
css=change(css,
 ' #settings .g1-settings-knob{transition:none!important}',
 ' #settings .g1-settings-knob,\n #player-settings .g1-settings-knob{transition:none!important}',styles)
source[styles]=css

playercss='gallery/src/styles/26-player-icons-and-timelines.css'
source[playercss]+="""
/* The exact G1 Settings slider SVG (only 21px render scale in Player).
   Knob timing and translations are shared with #settings; no hover motion.
   Preserve the existing Player button dimensions and hit area. */
#player-settings>.g1-settings-icon{
 display:block;width:21px;height:21px;flex:none;pointer-events:none;
}
"""
for path in EXPECT:
 if path in ('gallery/src/js/19h-bootstrap.js','gallery/src/js/11e-player-subtitles.js'):
  assert source[path].encode('utf-8')==Path(path).read_bytes(),path
  continue
 result=source[path].encode('utf-8')
 assert result!=Path(path).read_bytes(),('Did not modify approved source',path)
 Path(path).write_bytes(result)
 assert Path(path).read_bytes()==result
 print('PLAYER SETTINGS APPROVED SOURCE',path,'git-blob',blob(result),flush=True)
print('PASS exact main Settings SVG artwork, original 450ms easing, click-driven Player dialog and unchanged global Settings',flush=True)
