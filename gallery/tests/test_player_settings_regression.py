#!/usr/bin/env python3
"""Read-only Player and Settings regression tests for the Gallery HTML prototype."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import os,sys
html=Path(sys.argv[1]).read_text(encoding="utf-8")
n=0
def check(value,label):
 global n
 n+=1
 assert value,label
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path=os.environ.get("GALLERY_TEST_CHROMIUM") or None,args=["--no-sandbox"])
 def make(width=1440,height=900):
  page=browser.new_page(viewport={"width":width,"height":height})
  errors=[]
  page.on("pageerror",lambda e:errors.append(str(e)))
  page.set_content(html,wait_until="domcontentloaded")
  page.wait_for_timeout(240)
  return page,errors
 def settings(page):
  page.locator("#settings").click()
  page.wait_for_function('() => document.body.classList.contains("settings-view") && !galleryStageTransition && !gallerySettingsOpening',timeout=6000)
  page.wait_for_timeout(260)
 # DS02: shared Back color treatment on the four actual secondary routes.
 # Test each theme and responsive size, including the icon-only Settings Back.
 def ds02_check(page,selector,route,motion):
  button=page.locator(selector)
  check(button.count()==1 and button.is_visible(),"DS02 visible "+route)
  def snapshot(hover):
   return button.evaluate('''(el,hover)=>{
    const s=getComputedStyle(el), r=el.getBoundingClientRect();
    const probe=document.createElement('span');
    probe.style.cssText='position:absolute;visibility:hidden;pointer-events:none';
    el.append(probe);
    probe.style.color='var(--accent)';
    probe.style.backgroundColor=hover?'color-mix(in srgb,var(--panel) 80%,var(--accent) 20%)':'color-mix(in srgb,var(--panel) 88%,var(--accent) 12%)';
    probe.style.borderTopColor=hover?'color-mix(in srgb,var(--panel2) 30%,var(--accent) 70%)':'color-mix(in srgb,var(--panel2) 45%,var(--accent) 55%)';
    const p=getComputedStyle(probe);
    const expected=[p.color,p.backgroundColor,p.borderTopColor];
    probe.remove();
    const canvas=document.createElement('canvas');canvas.width=canvas.height=1;
    const ctx=canvas.getContext('2d',{willReadFrequently:true});
    const lum=color=>{
     ctx.clearRect(0,0,1,1);ctx.fillStyle=color;ctx.fillRect(0,0,1,1);
     const rgb=[...ctx.getImageData(0,0,1,1).data].slice(0,3).map(x=>x/255).map(x=>x<=.04045?x/12.92:((x+.055)/1.055)**2.4);
     return .2126*rgb[0]+.7152*rgb[1]+.0722*rgb[2];
    };
    const a=lum(s.color),b=lum(s.backgroundColor);
    return {actual:[s.color,s.backgroundColor,s.borderTopColor],expected,
     icon:getComputedStyle(el.querySelector('svg')).color,
     contrast:(Math.max(a,b)+.05)/(Math.min(a,b)+.05),
     geometry:[r.left,r.top,r.width,r.height,s.borderTopWidth,s.borderRadius,s.padding,s.fontSize],
     outline:s.outlineStyle,outlineWidth:s.outlineWidth,focus:el.matches(':focus-visible'),
     hover:el.matches(':hover')};
   }''',hover)
  for theme in ('ocean','twilight','ember','slate','glacier','verdant'):
   page.evaluate('(theme)=>{state.theme=theme;document.body.dataset.theme=theme;}',theme)
   for width in (1440,750,420):
    page.set_viewport_size({'width':width,'height':900})
    page.mouse.move(0,0)
    page.evaluate('()=>document.activeElement?.blur()')
    page.wait_for_timeout(350)
    rest=snapshot(False)
    check(rest['actual']==rest['expected'] and rest['icon']==rest['actual'][0],('DS02 rest accent',route,theme,width,motion,rest))
    check(rest['contrast']>=4.5,('DS02 text contrast',route,theme,width,rest['contrast']))
    button.hover(timeout=5000)
    page.wait_for_timeout(350)
    hover=snapshot(True)
    check(hover['hover'] and hover['actual']==hover['expected'] and hover['actual']!=rest['actual'],('DS02 hover',route,theme,width,hover))
    check(hover['contrast']>=4.5 and hover['geometry']==rest['geometry'],('DS02 hover contrast/geometry',route,theme,width,rest,hover))
    page.mouse.move(0,0)
    page.keyboard.press('Tab')
    button.focus()
    page.wait_for_timeout(350)
    focus=snapshot(False)
    check(focus['focus'] and focus['outline']!='none' and float(focus['outlineWidth'].removesuffix('px'))>=2,('DS02 keyboard focus',route,theme,width,focus))
    check(focus['actual']==rest['actual'] and focus['geometry']==rest['geometry'],('DS02 focus geometry/color',route,theme,width,focus))
  page.set_viewport_size({'width':1440,'height':900})
  page.mouse.move(0,0)
  page.wait_for_timeout(350)
  print('PASS: DS02 Back accent',route,motion,'six themes; 1440/750/420; rest/hover/focus; contrast >=4.5',flush=True)
 def ds02_stable(page):
  page.wait_for_function('() => !galleryStageTransition && !galleryStageFadeInProgress',timeout=6000)
  page.wait_for_timeout(350)
 for motion in ('no-preference','reduce'):
  pg=browser.new_page(viewport={'width':1440,'height':900},reduced_motion=motion)
  ds02_errors=[]
  pg.on('pageerror',lambda e:ds02_errors.append(str(e)))
  pg.set_content(html,wait_until='domcontentloaded')
  pg.wait_for_selector('#wh-view-history')
  pg.locator('[data-detail]').first.click()
  pg.wait_for_selector('#detail-back')
  ds02_stable(pg)
  ds02_check(pg,'#detail-back','Anime details',motion)
  pg.locator('.detail-actions [data-episode-action="watch"]').first.click()
  pg.wait_for_selector('#back-from-playback')
  ds02_stable(pg)
  ds02_check(pg,'#back-from-playback','Player',motion)
  pg.locator('#back-from-playback').click()
  pg.wait_for_selector('#detail-back')
  ds02_stable(pg)
  pg.locator('#detail-back').click()
  ds02_stable(pg)
  pg.locator('#wh-view-history').click()
  pg.wait_for_selector('#wh-root [data-wh-exit]')
  ds02_stable(pg)
  ds02_check(pg,'#wh-root [data-wh-exit]','Watch History',motion)
  pg.locator('#wh-root [data-wh-exit]').click()
  ds02_stable(pg)
  pg.locator('#settings').click()
  pg.wait_for_function('() => document.body.classList.contains("settings-view") && !gallerySettingsOpening')
  ds02_stable(pg)
  ds02_check(pg,'#settings-back','Settings',motion)
  pg.locator('#settings-back').click()
  pg.wait_for_function('() => !document.body.classList.contains("settings-view")')
  ds02_stable(pg)
  check(pg.locator('#wh-view-history').is_visible() and not ds02_errors,('DS02 Back navigation',motion,ds02_errors))
  pg.close()
 page,errors=make()
 page.locator("[data-detail]").first.click()
 page.wait_for_timeout(550)
 page.locator('.detail-actions [data-episode-action="watch"]').first.click()
 page.wait_for_selector("#player-area",timeout=6000)
 page.wait_for_timeout(160)
 check(page.evaluate("state.playback.audio")=="sub","Preselected audio remains in Player")
 check(abs(page.evaluate('document.querySelector("#local-video").volume')-.7)<.001,"Player starts at 70 percent volume")
 nav=page.locator(".player-episode-nav")
 check("Episode 5" in nav.inner_text() and "Season 1" in nav.inner_text(),"Episode/season context")
 widths=nav.evaluate('(e)=>[e.firstElementChild.getBoundingClientRect().width,e.lastElementChild.getBoundingClientRect().width]')
 check(abs(widths[0]-widths[1])<2,"Reserved previous/next navigation widths")
 check(page.locator("#player-settings").count()==1 and page.locator("#player-subtitles").count()==0,"Subtitle chooser is not in control bar")
 # The no-media overlay blocks pointer use until media or simulation starts.
 page.locator("#player-settings").evaluate("(e)=>e.click()")
 check(page.locator("#video-rate").count()==1 and page.locator("#player-subtitle-track").count()==1,"Player Settings speed and subtitle controls")
 page.locator("#video-rate").select_option("1.5")
 page.locator("#player-subtitle-track").select_option("off")
 page.locator("#save-player-settings").click()
 check(page.evaluate('document.querySelector("#local-video").playbackRate')==1.5 and not page.evaluate("playerSubtitleState.enabled"),"Speed and subtitle Off applied independently")
 page.locator("#player-settings").evaluate("(e)=>e.click()")
 check(page.locator("#player-subtitle-track").input_value()=="off","Subtitle Off remembered")
 page.locator("#save-player-settings").click()
 page.locator("#sf-player-demo-start").click()
 page.wait_for_timeout(100)
 check(not page.locator("#pause-play").is_disabled() and not page.locator("#seek").is_disabled(),"Simulation enables Player controls")
 levels=[]
 for v in (0,1,25,26,50,51,75,76,100):
  page.locator("#volume").fill(str(v))
  levels.append(page.locator(".player-volume-icon").get_attribute("data-level"))
 check(levels==["0","1","1","2","2","3","3","4","4"],"Volume icons follow 25 percent steps")
 page.locator("#volume").fill("70")
 page.locator("#mute").evaluate("(e)=>e.click()")
 pressed=page.locator("#mute").get_attribute("aria-pressed")
 page.locator("#mute").evaluate("(e)=>e.click()")
 check(pressed=="true" and page.locator("#volume").input_value()=="70","Mute preserves slider")
 page.evaluate("sfPlayerDemoSeek(SF_PLAYER_DEMO_DURATION-15)")
 page.wait_for_timeout(120)
 check(page.locator("#player-area").evaluate('(e)=>e.classList.contains("play-next-active")') and "00:15" in page.locator("#player-upnext-countdown").inner_text(),"Play Next within last 20 seconds")
 check(page.locator("#forward10").get_attribute("aria-label")=="Next episode" and page.locator("#player-morph-first").count()==1,"Forward morphs into Next")
 page.locator("#player-upnext-cancel").evaluate("(e)=>e.click()")
 check(not page.locator("#player-area").evaluate('(e)=>e.classList.contains("play-next-active")'),"Cancel Play Next")
 page.evaluate("sfPlayerDemoSeek(SF_PLAYER_DEMO_DURATION-30)")
 page.evaluate("sfPlayerDemoSeek(SF_PLAYER_DEMO_DURATION-12)")
 check(page.locator("#player-area").evaluate('(e)=>e.classList.contains("play-next-active")'),"Leaving final 20 seconds resets cancel")
 page.locator("#sf-player-demo-autoplay").evaluate('(e)=>{e.checked=false;e.dispatchEvent(new Event("change",{bubbles:true}));}')
 check(not page.locator("#player-area").evaluate('(e)=>e.classList.contains("play-next-active")'),"Autoplay Off hides Play Next")
 page.locator("#sf-player-demo-resume").evaluate("(e)=>e.click()")
 check(page.locator("#sf-resume-now").count()==1 and page.locator("#sf-start-over").count()==1,"Simulated Resume/Start Over dialog")
 page.locator("#sf-resume-now").evaluate("(e)=>e.click()")
 check(page.evaluate("Math.floor(sfPlayerDemo.time)")==730,"Simulated Resume seeks eight seconds earlier")
 check(not errors,str(errors))
 page.close()
 page,errors=make(1600,950)
 settings(page)
 check(not page.locator("#nav-discover").is_visible(),"Settings hides primary navigation")
 check(page.locator("[data-settings-section]").count()==5,"Settings sections")
 themes=("ocean","twilight","ember","slate","glacier","verdant")
 check(all(page.locator('[data-theme-button="'+t+'"]').count()==1 for t in themes),"Six theme controls")
 for theme in themes:
  page.locator('[data-theme-button="'+theme+'"]').click()
  check(page.locator("body").get_attribute("data-theme")==theme,"Theme "+theme)
 page.locator('[data-settings-section="playback"]').click()
 page.locator('[data-playback-tab="subtitles"]').click()
 page.wait_for_timeout(90)
 check(page.locator("#subtitle-font option").count()==3,"Three subtitle fonts")
 check(page.locator("[data-subtitle-size]").count()==5,"Five subtitle sizes")
 check(page.locator("[data-subtitle-effect]").count()==4,"Four subtitle styles")
 check(page.locator("[data-effect-strength]").count()==3,"Three effect intensity options")
 check(page.locator("[data-effect-strength]").all_inner_texts()==["Low","Medium","High"],"Correct intensity labels")
 check(page.evaluate("SUBTITLE_DEFAULTS.color")=="#f8f8f8","Approved default subtitle soft white")
 check(page.evaluate("SUBTITLE_TEXT_COLOR_PRESETS.white")=="#f8f8f8","Soft White preset matches default")
 check(page.locator('[data-subtitle-text-color="white"] .sf-subtitle-swatch').evaluate('(e)=>getComputedStyle(e).backgroundColor')=="rgb(248, 248, 248)","White color swatch matches default")
 check("The quick brown fox jumps over the lazy dog" in " ".join(page.locator("#subtitle-live-caption").inner_text().split()),"Preview sample sentence")
 check(page.locator("#subtitle-preview-stage .sf-day").count()==1 and page.locator("#subtitle-preview-stage .sf-night").count()==1,"Day/night images")
 check(page.locator("#subtitle-preview-stage").is_visible(),"Full-size subtitle preview")
 rect=page.locator("#subtitle-preview-stage").bounding_box()
 check(abs(rect["width"]/rect["height"]-16/9)<.02,"Full-size preview aspect ratio")
 page.locator('[data-subtitle-size="large"]').click()
 page.locator("#subtitle-font").select_option("inter")
 check(page.locator('[data-subtitle-size="large"]').get_attribute("aria-pressed")=="true" and page.locator("#subtitle-font").input_value()=="inter","Subtitle controls update")
 for effect,key,values in [("outline","outline",[1,3,6]),("shadow","shadow",[1.5,3,10]),("box","boxOpacity",[35,65,100])]:
  page.locator('[data-subtitle-effect="'+effect+'"]').click()
  for preset,value in zip(("light","normal","strong"),values):
   page.locator('[data-effect-strength="'+preset+'"]').click()
   cap=page.evaluate("maximumSubtitleOutline(subtitlePrefs.size)") if effect=="outline" else value
   check(page.evaluate("subtitlePrefs."+key)==min(value,cap),"Effect value "+effect+"/"+preset)
   check(page.locator('[data-effect-strength="'+preset+'"]').get_attribute("aria-pressed")=="true","Selected intensity "+effect+"/"+preset)
 page.locator("#subtitle-reset").click()
 check(page.locator('[data-subtitle-size="normal"]').get_attribute("aria-pressed")=="true" and page.locator("#subtitle-font").input_value()=="system","Subtitle reset")
 check(page.evaluate("subtitlePrefs.color")=="#f8f8f8" and page.evaluate("subtitlePrefs.outlinePreset")=="normal","Reset restores white and medium intensity")
 # Distinguish unsaved Custom from a white preset; only Done stores a swatch.
 custom=page.locator('[data-subtitle-text-color="custom"]')
 palette=page.locator("#subtitle-custom-palette")
 swatch=page.locator("#subtitle-custom-swatch")
 check(palette.is_visible() and not swatch.is_visible(),"Unsaved Custom shows palette")
 custom.click()
 page.locator(".gallery-color-hex").fill("#3366CC")
 page.locator(".gallery-color-close").click()
 check(palette.is_visible() and not swatch.is_visible() and page.evaluate("subtitlePrefs.colorMode")=="white","Cancelled custom change retains White and palette")
 custom.click()
 page.locator(".gallery-color-hex").fill("#3366CC")
 page.locator(".gallery-color-done").click()
 check(not palette.is_visible() and swatch.is_visible(),"Confirmed Custom displays saved swatch")
 check(page.evaluate("subtitlePrefs.customColorSet && subtitlePrefs.color==='#3366cc'") and swatch.evaluate("(e)=>getComputedStyle(e).backgroundColor")=="rgb(51, 102, 204)","Custom color and swatch match")
 page.locator('[data-subtitle-text-color="yellow"]').click()
 check(swatch.is_visible() and page.evaluate("subtitlePrefs.color")=="#ffe066","Saved swatch remains visible when Yellow selected")
 custom.click()
 check(page.evaluate("subtitlePrefs.color")=="#3366cc" and page.locator(".gallery-color-popover").count()==0,"Recall saved custom color without reopening editor")
 custom.click()
 check(page.locator(".gallery-color-popover").is_visible(),"Click selected Custom to edit")
 page.locator(".gallery-color-close").click()
 page.locator('[data-subtitle-effect="none"]').click()
 check(all(b.is_disabled() for b in page.locator("[data-effect-strength]").all()),"None disables intensity")
 page.locator("#subtitle-reset").click()
 check(palette.is_visible() and not swatch.is_visible(),"Reset restores palette placeholder")
 check(not errors,str(errors))
 page.close()
 for width in (1600,1280,800,440,340):
  page,errors=make(width,820)
  settings(page)
  page.locator('[data-settings-section="playback"]').click()
  page.locator('[data-playback-tab="subtitles"]').click()
  page.wait_for_timeout(100)
  choice_group=page.locator(".sf-subtitle-three")
  check(choice_group.count()==1 and page.locator("[data-effect-strength]").count()==3,"Three intensity buttons at "+str(width))
  group_rect=choice_group.bounding_box()
  buttons=[btn.bounding_box() for btn in page.locator("[data-effect-strength]").all()]
  check(bool(group_rect) and all(b and b["x"]>=group_rect["x"]-1 and b["x"]+b["width"]<=group_rect["x"]+group_rect["width"]+1 for b in buttons),"No intensity button overflow at "+str(width))
  visible=page.locator("#subtitle-preview-stage").is_visible()
  compact=page.locator("#subtitle-compact-preview").is_visible()
  check(visible!=compact,"Exactly one preview layout at "+str(width))
  if visible:
   r=page.locator("#subtitle-preview-stage").bounding_box()
   check(abs(r["width"]/r["height"]-16/9)<.02,"Preview ratio at "+str(width))
  else:
   page.locator("#subtitle-compact-preview").click()
   check(page.locator("#subtitle-expanded-stage").is_visible(),"Compact preview opens at "+str(width))
  check(not errors,str(errors))
  page.close()
 # Current preferences round-trip and invalid values fall back to defaults.
 prefs=browser.new_page(viewport={"width":1200,"height":850})
 prefs.route("https://gallery-audit.invalid/**",lambda route:route.fulfill(status=200,content_type="text/html",body=html))
 prefs.goto("https://gallery-audit.invalid/")
 prefs.evaluate("""() => {
  Object.assign(subtitlePrefs,{font:'inter',size:'large',effect:'shadow',outlinePreset:'strong',shadowPreset:'light',boxPreset:'strong',colorMode:'custom',customColor:'#123456',customColorSet:true,outlineColor:'#abcdef',shadowColor:'#334455',boxColor:'#556677'});
  assignSubtitlePresetNumbers(subtitlePrefs);
  subtitlePrefs.color=subtitlePrefs.customColor;
  persistSubtitlePrefs();
  Object.assign(galleryVolumePreferences,{mode:'user',preferred:35,precision:'fine'});
  saveGalleryVolumePreferences();
  localStorage.setItem('gallery.font','inter');
  localStorage.setItem('gallery.softFuturistic.theme','glacier');
 }""")
 prefs.reload()
 saved=prefs.evaluate("subtitlePrefs")
 check([saved[k] for k in ("font","size","effect","outlinePreset","shadowPreset","boxPreset")]==["inter","large","shadow","strong","light","strong"],"Current subtitle choices survive reload")
 check([saved[k] for k in ("outline","shadow","boxOpacity")]==[6,1.5,100],"Current intensity values recomputed")
 check(saved["color"]=="#123456" and saved["customColorSet"] and [saved[k] for k in ("outlineColor","shadowColor","boxColor")]==["#abcdef","#334455","#556677"],"Current subtitle colors survive reload")
 check(prefs.evaluate("galleryVolumePreferences")=={"mode":"user","preferred":35,"precision":"fine"} and prefs.evaluate("playerSessionVolume")==35,"Current starting volume survives reload")
 check(prefs.evaluate("state.font")=="inter" and prefs.evaluate("state.theme")=="glacier","Current font and theme survive reload")
 prefs.evaluate("""() => {
  localStorage.setItem('gallery.subtitlePreferences', JSON.stringify({font:'bad',size:44,effect:'bad',outlinePreset:'max',shadowPreset:'bad',boxPreset:'bad',colorMode:'bad',customColor:'invalid',customColorSet:'bad',outline:6,shadow:10,boxOpacity:100,background:'solid'}));
  localStorage.setItem('gallery.playback.startingVolume',JSON.stringify({mode:'fixed',preferred:20,precision:'bad'}));
  localStorage.setItem('gallery.font','bad');
  localStorage.setItem('gallery.softFuturistic.theme','paper');
 }""")
 invalid=prefs.evaluate("readSubtitlePrefs()")
 check(invalid==prefs.evaluate("SUBTITLE_DEFAULTS"),"Unsupported subtitle fields fall back to current defaults")
 check(prefs.evaluate("readGalleryVolumePreferences().mode")=="gallery","Unsupported volume mode falls back to Gallery")
 check(prefs.evaluate("readGalleryFont()")=="system" and prefs.evaluate("readSoftFuturisticTheme()")=="ocean","Unsupported font and theme fall back")
 prefs.evaluate("""() => {
  localStorage.removeItem('gallery.subtitlePreferences');
  localStorage.removeItem('gallery.font');
  localStorage.setItem('gallery.layoutExperimentA.subtitlePreview',JSON.stringify({size:'large'}));
  localStorage.setItem('gallery.layoutExperimentA.font','inter');
 }""")
 check(prefs.evaluate("readSubtitlePrefs()")==prefs.evaluate("SUBTITLE_DEFAULTS") and prefs.evaluate("readGalleryFont()")=="system","Retired storage keys ignored")
 prefs.evaluate("localStorage.setItem('gallery.subtitlePreferences','{invalid')")
 check(prefs.evaluate("readSubtitlePrefs()")==prefs.evaluate("SUBTITLE_DEFAULTS"),"Malformed subtitle storage uses defaults")
 prefs.close()

 # Exact before/after equivalence for the retired subtitle selector cleanup.
 import hashlib,base64,gzip,json
 if hashlib.sha256(html.encode("utf-8")).hexdigest()=="64942fe6416fcd07de902b24c46cc20414af3ff5ba48a7e67a7f5f729c8370c5":
  old_dir=Path(__file__).resolve().parents[1]/"checkpoints"/"2026-11-12-remove-prototype-preference-migrations"
  manifest=json.loads((old_dir/"manifest.json").read_text())
  chunks=[]
  for part in manifest["parts"]:
   data=(old_dir/part["file"]).read_bytes()
   assert len(data)==part["encoded_chars"] and hashlib.sha256(data).hexdigest()==part["sha256"]
   chunks.append(data)
  old_raw=gzip.decompress(base64.b64decode(b"".join(chunks),validate=True))
  assert len(old_raw)==6949666 and hashlib.sha256(old_raw).hexdigest()=="12001b0ec4915bc3971380bc8c4b5348f1581743c08548f4e559ec3b169c242a"
  old_html=old_raw.decode("utf-8")
  def subtitle_snapshot(source,width,theme):
   pg=browser.new_page(viewport={"width":width,"height":900},reduced_motion="reduce")
   errs=[]
   pg.on("pageerror",lambda e:errs.append(str(e)))
   try:
    pg.set_content(source,wait_until="domcontentloaded")
    pg.wait_for_timeout(240)
    settings(pg)
    pg.locator('[data-theme-button="'+theme+'"]').click()
    pg.locator('[data-settings-section="playback"]').click()
    pg.locator('[data-playback-tab="subtitles"]').click()
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(150)
    def snap():
     return pg.evaluate("""() => {
      const props=['display','visibility','position','width','height','minWidth','maxWidth','minHeight','maxHeight','padding','margin','gap','gridTemplateColumns','gridTemplateRows','alignItems','justifyContent','border','borderRadius','backgroundColor','backgroundImage','color','fontFamily','fontSize','fontWeight','lineHeight','boxShadow','textShadow','webkitTextStroke','overflowX','overflowY','transform'];
      const roots=[document.querySelector('#playback-subtitles-pane'),document.querySelector('.subtitle-preview-dialog'),document.querySelector('.gallery-color-popover')].filter(Boolean);
      return roots.map(root=>[root,...root.querySelectorAll('*')].map(e=>{
       const r=e.getBoundingClientRect(),c=getComputedStyle(e);
       return [e.tagName,e.id,e.getAttribute('class'),[r.x,r.y,r.width,r.height].map(v=>Math.round(v*10)/10),props.map(p=>c[p])];
      }));
     }""")
    states=[snap()]
    for effect in ("none","shadow","box","outline"):
     pg.locator('[data-subtitle-effect="'+effect+'"]').click()
     states.append(snap())
    pg.locator('[data-subtitle-text-color="custom"]').click()
    pg.wait_for_selector(".gallery-color-popover")
    states.append(snap())
    pg.locator(".gallery-color-close").click()
    if pg.locator("#subtitle-compact-preview").is_visible():
     pg.locator("#subtitle-compact-preview").click()
    else:
     pg.evaluate("showExpandedSubtitlePreview()")
    pg.wait_for_selector("#subtitle-expanded-stage")
    pg.wait_for_timeout(150)
    states.append(snap())
    assert not errs,errs
    return states
   finally:
    pg.close()
  for width in (1600,700):
   for theme in ("ocean","twilight","ember","slate","glacier","verdant"):
    before=subtitle_snapshot(old_html,width,theme)
    after=subtitle_snapshot(html,width,theme)
    check(before==after,"Exact subtitle computed layout/style equivalence: "+theme+" at "+str(width))
 browser.close()
print("Player and Settings regression suite passed:",n,"checks")
