#!/usr/bin/env python3
"""Restore approved subtitle default white and four intensity presets.

Applies only to GitHub's authoritative verified working HTML.
No image assets, preview geometry, scrolling, player or motion code is edited.
"""
from pathlib import Path
import hashlib

html=Path("gallery/Gallery-current.html")
raw=html.read_bytes()
assert len(raw)==6951729 and hashlib.sha256(raw).hexdigest()=="7f9922d18f2ddd8b61035f5d2a524d3482fa3df5ea84045cf75be12c004eff45", "STOP: authoritative working HTML differs from the immutable checkpoint"
s=raw.decode("utf-8")
changes=[
 ("color:'#f5f5f5',colorMode:'white'","color:'#f8f8f8',colorMode:'white'"),
 ("const SUBTITLE_TEXT_COLOR_PRESETS=Object.freeze({white:'#f5f5f5',yellow:'#ffe066'});","const SUBTITLE_TEXT_COLOR_PRESETS=Object.freeze({white:'#f8f8f8',yellow:'#ffe066'});"),
 ('style="background:#F5F5F5" aria-hidden="true"','style="background:#F8F8F8" aria-hidden="true"'),
 ("if(previous==='#ffe066')v.colorMode='yellow';\n    else if(previous!=='#ffffff' && previous!=='#f5f5f5'){","if(previous==='#ffe066')v.colorMode='yellow';\n    else if(!['#ffffff','#f5f5f5','#f8f8f8'].includes(previous)){"),
 ("// A10 — Consistent Subtle / Normal / Strong labels under Effect intensity.","// Four intensity labels preserve existing light/normal/strong strengths, with a new Max."),
 ("outline:{light:1,normal:3,strong:5},\n shadow:{light:1.5,normal:3,strong:6},\n box:{light:35,normal:65,strong:85}","outline:{light:1,normal:3,strong:5,max:6},\n  shadow:{light:1.5,normal:3,strong:6,max:10},\n  box:{light:35,normal:65,strong:85,max:100}"),
 ("const SUBTITLE_EFFECT_LABELS=Object.freeze(['Subtle','Normal','Strong']);","const SUBTITLE_EFFECT_LABELS=Object.freeze(['Low','Medium','High','Max']);"),
 ("['light','normal','strong'].includes(saved)?saved:","['light','normal','strong','max'].includes(saved)?saved:"),
 ("${['light','normal','strong'].map((value,i)=>","${['light','normal','strong','max'].map((value,i)=>"),
 (".sf-subtitle-three{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:5px}",".sf-subtitle-four{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:5px}"),
 (".sf-subtitle-three .sf-subtitle-choice",".sf-subtitle-four .sf-subtitle-choice"),
 ('class="sf-subtitle-three" role="group"','class="sf-subtitle-four" role="group"')
]
for before,after in changes:
 expected=2 if before==".sf-subtitle-three .sf-subtitle-choice" else 1
 assert s.count(before)==expected, f"STOP: unexpected subtitle source anchor {before[:100]}: {s.count(before)}"
 s=s.replace(before,after)
updated=s.encode("utf-8")
assert len(updated)==6951780 and hashlib.sha256(updated).hexdigest()=="6d1aad0729347ff2f2078d35e931872e3eaf3f57924091203e4d777962be2c7c", "STOP: build does not match exact locally tested candidate"
html.write_bytes(updated)
print("Approved subtitle HTML correction:",len(updated),hashlib.sha256(updated).hexdigest())

# Extend the existing permanent browser regression; never change its other assertions.
test=Path("gallery/tests/test_player_settings_regression.py")
t=test.read_text(encoding="utf-8")
anchor=' check(page.locator("[data-subtitle-effect]").count()==4,"Four subtitle styles")'
assert t.count(anchor)==1, "STOP: missing settings regression anchor"
added=''' check(page.locator("[data-effect-strength]").count()==4,"Four effect intensity options")
 check(page.locator("[data-effect-strength]").all_inner_texts()==["Low","Medium","High","Max"],"Correct intensity labels")
 check(page.evaluate("SUBTITLE_DEFAULTS.color")=="#f8f8f8","Approved default subtitle soft white")
 check(page.evaluate("SUBTITLE_TEXT_COLOR_PRESETS.white")=="#f8f8f8","Soft White preset matches default")
 check(page.locator('[data-subtitle-text-color="white"] .sf-subtitle-swatch').evaluate('(e)=>getComputedStyle(e).backgroundColor')=="rgb(248, 248, 248)","White color swatch matches default")
'''
t=t.replace(anchor,anchor+"\n"+added.rstrip("\n"))
anchor2=' page.locator("#subtitle-reset").click()'
assert t.count(anchor2)==1,"STOP: subtitle reset regression anchor changed"
presetTests=''' for effect,key,values in [("outline","outline",[1,3,5,6]),("shadow","shadow",[1.5,3,6,10]),("box","boxOpacity",[35,65,85,100])]:
  page.locator('[data-subtitle-effect="'+effect+'"]').click()
  for preset,value in zip(("light","normal","strong","max"),values):
   page.locator('[data-effect-strength="'+preset+'"]').click()
   cap=page.evaluate("maximumSubtitleOutline(subtitlePrefs.size)") if effect=="outline" else value
   check(page.evaluate("subtitlePrefs."+key)==min(value,cap),"Effect value "+effect+"/"+preset)
   check(page.locator('[data-effect-strength="'+preset+'"]').get_attribute("aria-pressed")=="true","Selected intensity "+effect+"/"+preset)
'''
t=t.replace(anchor2,presetTests+anchor2)
anchor3=""" check(page.locator('[data-subtitle-size="normal"]').get_attribute("aria-pressed")=="true" and page.locator("#subtitle-font").input_value()=="system","Subtitle reset")"""
assert t.count(anchor3)==1,"STOP: subtitle reset result assertion changed"
t=t.replace(anchor3,anchor3+'\n check(page.evaluate("subtitlePrefs.color")=="#f8f8f8" and page.evaluate("subtitlePrefs.outlinePreset")=="normal","Reset restores white and medium intensity")')
anchor4='  visible=page.locator("#subtitle-preview-stage").is_visible()'
assert t.count(anchor4)==1,"STOP: responsive regression anchor changed"
t=t.replace(anchor4,'''  choice_group=page.locator(".sf-subtitle-four")
  check(choice_group.count()==1 and page.locator("[data-effect-strength]").count()==4,"Four intensity buttons at "+str(width))
  group_rect=choice_group.bounding_box()
  buttons=[btn.bounding_box() for btn in page.locator("[data-effect-strength]").all()]
  check(bool(group_rect) and all(b and b["x"]>=group_rect["x"]-1 and b["x"]+b["width"]<=group_rect["x"]+group_rect["width"]+1 for b in buttons),"No intensity button overflow at "+str(width))
'''+anchor4)
test.write_text(t,encoding="utf-8")
print("Player/Settings browser test extended for restored white, all strengths and narrow layout")
