#!/usr/bin/env python3
"""Approved YouTube-style Player Settings popover (source-first, fail-closed).

Only modify Player-specific JS/CSS and the established Player regression to
match the approved immediate-apply behavior without dropping its assertions.
All shared modal, fullscreen, source, assets and generated HTML remain untouched.
"""
import hashlib, ast
from pathlib import Path

EXPECT={
 'gallery/src/js/11e-player-subtitles.js':'8c4ee78ab4ebce8fe918f438005637fcd50f1dc7',
 'gallery/src/js/11h-player-controls.js':'f63d5028f25bc1fc1427154f2e0cc64c0dc3df5c',
 'gallery/src/styles/26-player-icons-and-timelines.css':'6b3343dbf4462daced4ff772388f591fd9b306cc',
 'gallery/tests/test_player_settings_regression.py':'d74f5ad0ec0add9c38a5bf9c12e094e4652d3641',
 'gallery/src/js/11j-dialog-lifecycle.js':'aa8fd2a4b61d145ab4181b5d46c08d39718e4801',
 'gallery/src/js/11b-player-page.js':'0aaa01c361849af728e5da796bfe764f785c9246',
 'gallery/src/styles/03-player-and-desktop-frame.css':'3195ff5165d10aca30d196fd189a6a5f8179a041',
}
def blob(raw):return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def one(s,old,new,path):
 assert s.count(old)==1,(path,'missing or duplicated anchor',old[:100],s.count(old))
 return s.replace(old,new,1)
for path,expected in EXPECT.items():
 data=Path(path).read_bytes()
 assert blob(data)==expected,(path,'base drift',blob(data),expected)

feature_path=Path('gallery/changes/specimens/2026-11-26-player-settings-in-video-menu.js')
css_path=Path('gallery/changes/specimens/2026-11-26-player-settings-in-video-menu.css')
assert blob(feature_path.read_bytes())=='6857bf6e44177d2d0154381d3a37af36d7e15f6d','Player menu implementation payload changed'
assert blob(css_path.read_bytes())=='db84035ecd2e989b2c82295581581fc0ce137c45','Player menu CSS payload changed'
feature=feature_path.read_text(encoding='utf-8')
css=css_path.read_text(encoding='utf-8')
# Historical modal and its tests are never rewritten: only this Player function.
p='gallery/src/js/11e-player-subtitles.js';s=Path(p).read_text()
start=s.index('function openPlayerSettings(video){')
stop=s.index('function fmtTime(sec){')
assert s.count('function openPlayerSettings(video){')==1 and stop>start
assert 'modal(\'Player settings\'' in s[start:stop] and '#save-player-settings' not in s[start:stop], 'Unexpected original Player dialog'
s=s[:start]+feature+'\n'+s[stop:]
assert s.count('function openPlayerSettings(video){')==1 and s.count('function fmtTime(sec){')==1
Path(p).write_text(s)

p='gallery/src/js/11h-player-controls.js';s=Path(p).read_text()
s=one(s,' owner.active=false;++owner.request;',' closePlayerSettings();\n owner.active=false;++owner.request;',p)
old='if(document.getElementById(\'modal-host\')?.firstElementChild)return;'
assert s.count(old)==2,(p,'idle control guards drift',s.count(old))
s=s.replace(old,"if(playerSettingsMenu || document.getElementById('modal-host')?.firstElementChild)return;")
begin=s.index(" const playerSettingsButton=document.getElementById('player-settings');")
end=s.index(' const fullscreen=()=>',begin)
assert s.count(' const playerSettingsButton=document.getElementById(\'player-settings\');')==1
assert "openPlayerSettings(v);" in s[begin:end] and "gallery-modal-will-close" in s[begin:end]
replacement=""" const playerSettingsButton=document.getElementById('player-settings');
 playerSettingsButton.dataset.g1Active='false';
 playerSettingsButton.setAttribute('aria-haspopup','dialog');
 playerSettingsButton.setAttribute('aria-expanded','false');
 playerSettingsButton.onclick=()=>openPlayerSettings(v);
"""
s=s[:begin]+replacement+s[end:]
anchor=" on(document,'keydown',e=>{if(e.key==='Tab')playerKeyboardFocus=true;});"
extra=""" on(document,'pointerdown',e=>{
  const menu=playerSettingsMenu;
  if(menu&&!e.composedPath().includes(menu.panel)&&!e.composedPath().includes(menu.button))closePlayerSettings();
 });
 // Also handle programmatic, assistive-technology and keyboard clicks.
 on(document,'click',e=>{
  const menu=playerSettingsMenu;
  if(menu&&!e.composedPath().includes(menu.panel)&&!e.composedPath().includes(menu.button))closePlayerSettings();
 });
 on(document,'focusin',e=>{
  const menu=playerSettingsMenu;
  if(menu&&!e.composedPath().includes(menu.panel)&&!e.composedPath().includes(menu.button))closePlayerSettings();
 });
 on(document,'keydown',e=>{
  if(playerSettingsMenu&&e.key==='Escape'){
   e.preventDefault();e.stopPropagation();closePlayerSettings({restoreFocus:true});
  }
 });
 on(window,'resize',positionPlayerSettingsMenu);
 on(document,'fullscreenchange',positionPlayerSettingsMenu);
"""
s=one(s,anchor,anchor+'\n'+extra.rstrip('\n'),p)
Path(p).write_text(s)

p='gallery/src/styles/26-player-icons-and-timelines.css';s=Path(p).read_text();assert 'player-settings-popover' not in s
Path(p).write_text(s+'\n'+css)

p='gallery/tests/test_player_settings_regression.py';s=Path(p).read_text();s=one(s,' # The no-media overlay blocks pointer use until media or simulation starts.\n page.locator("#player-settings").evaluate("(e)=>e.click()")\n check(page.locator("#video-rate").count()==1 and page.locator("#player-subtitle-track").count()==1,"Player Settings speed and subtitle controls")\n page.locator("#video-rate").select_option("1.5")\n page.locator("#player-subtitle-track").select_option("off")\n page.locator("#save-player-settings").click()\n check(page.evaluate(\'document.querySelector("#local-video").playbackRate\')==1.5 and not page.evaluate("playerSubtitleState.enabled"),"Speed and subtitle Off applied independently")\n page.locator("#player-settings").evaluate("(e)=>e.click()")\n check(page.locator("#player-subtitle-track").input_value()=="off","Subtitle Off remembered")\n page.locator("#save-player-settings").click()\n',' # The no-media overlay blocks physical Player controls until media or\n # simulation starts; programmatic invocation still exercises the same menu.\n page.locator("#player-settings").evaluate("(e)=>e.click()")\n check(page.locator("#player-settings-popover[role=\'dialog\'][aria-modal=\'false\']").count()==1 and page.locator("#player-speed-option").count()==1 and page.locator("#player-subtitles-option").count()==1,"Player Settings in-video speed/subtitle menu")\n check(page.locator("#modal-host .overlay").count()==0 and not page.evaluate("galleryApp.inert"),"Player Settings does not dim or block entire app")\n check(page.locator("#player-settings").get_attribute("aria-expanded")=="true" and page.locator("#player-settings").get_attribute("data-g1-active")=="true","Player Settings open icon remains active")\n page.locator("#player-speed-option").click()\n check(page.locator(\'[data-player-menu="speed:1.5"]\').count()==1,"All original playback speed choices accessible")\n page.locator(\'[data-player-menu="speed:1.5"]\').click()\n check(page.evaluate(\'document.querySelector("#local-video").playbackRate\')==1.5 and "1.5×" in page.locator("#player-speed-option").inner_text(),"Playback speed applies immediately and row displays selection")\n page.locator("#player-subtitles-option").click()\n page.locator(\'[data-player-menu="subtitle:off"]\').click()\n check(not page.evaluate("playerSubtitleState.enabled") and "Off" in page.locator("#player-subtitles-option").inner_text(),"Subtitle Off applies independently and immediately")\n page.locator("#player-settings").evaluate("(e)=>e.click()")\n check(page.locator("#player-settings-popover").count()==0 and page.locator("#player-settings").get_attribute("data-g1-active")=="false","Player Settings toggle dismisses and reverses the slider icon")\n page.locator("#player-settings").evaluate("(e)=>e.click()")\n check("Off" in page.locator("#player-subtitles-option").inner_text(),"Subtitle Off remembered on reopening")\n page.keyboard.press("Escape")\n check(page.locator("#player-settings-popover").count()==0,"Escape closes only the Player Settings panel")\n',p)
# Preserve all old test sections and original coverage beyond the Player settings input.
assert 'Volume icons follow 25 percent steps' in s and 'Simulated Resume seeks eight seconds earlier' in s
assert 'Subtitle reset' in s and 'DS02 Back accent' in s
ast.parse(s,filename=p)
Path(p).write_text(s)
for p in EXPECT:
 if p in ('gallery/src/js/11j-dialog-lifecycle.js','gallery/src/js/11b-player-page.js','gallery/src/styles/03-player-and-desktop-frame.css'):
  assert blob(Path(p).read_bytes())==EXPECT[p],('Unapproved modal/fullscreen/source drift',p)
 else:
  new=blob(Path(p).read_bytes())
  assert new!=EXPECT[p],('Expected approved source change missing',p)
  print('PLAYER POPOVER SOURCE',p,'git-blob',new,flush=True)
print('PASS: player-only popover, immediate speed/subtitle application, unchanged global modal/fullscreen, preserved and adapted original regression',flush=True)
