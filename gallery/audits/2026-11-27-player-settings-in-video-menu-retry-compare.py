#!/usr/bin/env python3
"""Original-route in-player nonmodal Player Settings audit (48 UI contexts).

Full and lightweight, six themes, desktop/narrow, normal/reduced motion;
exact shared G1 knob timing/pose, no global modal or page dim, anchored menu,
immediate playback speed/subtitle selection, keyboard and outside dismissal.
"""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT='https://gallery-player-menu-audit.invalid/'
FILES=(('full','gallery/Gallery-current.html'),('lightweight','gallery/Gallery-development.html'))
THEMES=('ocean','twilight','ember','slate','glacier','verdant')
EASE='cubic-bezier(0.22, 0.72, 0.2, 1)'
def near(a,b,t=.35):return abs(float(a)-float(b))<=t
def pose(page):
 return page.locator('#player-settings').evaluate('''el=>({
  active:el.dataset.g1Active,expanded:el.getAttribute('aria-expanded'),
  offsets:[...el.querySelectorAll('.g1-settings-knob')].map(e=>new DOMMatrix(getComputedStyle(e).transform).e),
  duration:[...el.querySelectorAll('.g1-settings-knob')].map(e=>getComputedStyle(e).transitionDuration),
  easing:[...el.querySelectorAll('.g1-settings-knob')].map(e=>getComputedStyle(e).transitionTimingFunction),
  rect:(()=>{const r=el.getBoundingClientRect(),a=el.closest('#player-area').getBoundingClientRect();return [r.x-a.x,r.y-a.y,r.width,r.height]})()
 })''')
def assert_pose(p,opened,motion,tag):
 assert p['active']==str(opened).lower() and p['expanded']==str(opened).lower(),(tag,'icon/aria',p)
 assert all(near(x,y) for x,y in zip(p['offsets'],(6,-6) if opened else (0,0))),(tag,'knobs',p)
 assert p['duration']==(['0s']*2 if motion=='reduce' else ['0.45s']*2),(tag,'duration',p)
 assert p['easing']==(['ease']*2 if motion=='reduce' else [EASE]*2),(tag,'easing',p)
def assert_anchored(page,tag):
 p=page.locator('#player-settings-popover')
 assert p.count()==1 and p.is_visible(),(tag,'missing popover')
 region=p.evaluate('''el=>{
  const r=el.getBoundingClientRect(),a=el.closest('#player-area').getBoundingClientRect();
  const css=getComputedStyle(el);
  return {x:r.x,y:r.y,right:r.right,bottom:r.bottom,area:[a.x,a.y,a.right,a.bottom],parent:el.parentElement.id,
    bg:css.backgroundColor,role:el.getAttribute('role'),modal:el.getAttribute('aria-modal')};
 }''')
 a=region['area'];r=region
 assert r['parent']=='player-area' and r['role']=='dialog' and r['modal']=='false',(tag,'inside nonmodal player',r)
 assert r['x']>=a[0]-2 and r['y']>=a[1]-2 and r['right']<=a[2]+2 and r['bottom']<=a[3]+2,(tag,'overflow',r)
 assert not page.evaluate('galleryApp.inert') and page.locator('#modal-host .overlay').count()==0,(tag,'global app must not dim/block')
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path=os.environ.get('GALLERY_TEST_CHROMIUM') or None,args=['--no-sandbox','--disable-dev-shm-usage'])
 total=0
 for mode,path in FILES:
  raw=Path(path).read_bytes()
  for motion in ('no-preference','reduce'):
   page=browser.new_page(viewport={'width':1100,'height':850},reduced_motion=motion)
   errs=[];page.on('pageerror',lambda e:errs.append(str(e)))
   page.route(ROOT+'**',lambda route:route.fulfill(status=200,content_type='text/html; charset=utf-8',body=raw))
   page.goto(ROOT,wait_until='domcontentloaded')
   page.locator('[data-detail]').first.click()
   page.wait_for_function("()=>!!state.detailId&&!galleryStageFadeInProgress&&!galleryStageTransition",timeout=12000)
   page.locator('.detail-actions [data-episode-action="watch"]').first.click()
   page.wait_for_function("()=>!!state.playback&&!!document.getElementById('player-settings')&&!galleryStageFadeInProgress&&!galleryStageTransition",timeout=12000)
   page.locator('#sf-player-demo-start').click()
   page.wait_for_function('()=>sfPlayerDemo.active&&document.getElementById("player-empty").hidden',timeout=12000)
   settings=page.locator('#player-settings')
   assert settings.count()==1 and settings.get_attribute('aria-label')=='Player settings'
   assert page.locator('#fullscreen .g4-fullscreen-piece').count()==4,'Previously approved fullscreen glyph changed'
   main=page.locator('#settings .g1-settings-icon').evaluate('el=>el.outerHTML')
   player=page.locator('#player-settings svg').evaluate('''el=>{const s=el.cloneNode(true);s.setAttribute('width','23');s.setAttribute('height','23');return s.outerHTML}''')
   assert main==player,(mode,motion,'shared Settings SVG changed')
   for width in (1100,430):
    page.set_viewport_size({'width':width,'height':850})
    for i,theme in enumerate(THEMES):
     page.evaluate('theme=>{state.theme=theme;document.body.dataset.theme=theme}',theme)
     tag=f'{mode}/{motion}/{width}/{theme}'
     page.mouse.move(0,0)
     page.wait_for_timeout(485 if motion=='no-preference' else 25)
     before=pose(page)
     assert_pose(before,False,motion,tag+' rest')
     settings.hover()
     page.wait_for_timeout(40)
     assert_pose(pose(page),False,motion,tag+' hover does not animate')
     if i==0 and width==1100:
      settings.focus();settings.press('Enter')
     else:settings.click()
     assert_anchored(page,tag+' opening')
     assert page.locator('#player-speed-option').count()==1 and page.locator('#player-subtitles-option').count()==1
     page.wait_for_timeout(490 if motion=='no-preference' else 25)
     opened=pose(page)
     assert_pose(opened,True,motion,tag+' hold')
     assert all(near(x,y,.5) for x,y in zip(before['rect'],opened['rect'])),(tag,'button moved',before['rect'],opened['rect'])
     if i%2==0:
      page.locator('#player-speed-option').click()
      assert page.locator('.player-settings-back').count()==1 and page.locator('[data-player-menu="speed:1.5"]').count()==1
      page.locator('[data-player-menu="speed:1.5"]').click()
      assert page.evaluate('document.querySelector("#local-video").playbackRate')==1.5,(tag,'immediate speed')
      assert '1.5×' in page.locator('#player-speed-option').inner_text(),(tag,'displayed speed')
      page.locator('#player-subtitles-option').click()
      page.locator('[data-player-menu="subtitle:off"]').click()
      assert not page.evaluate('playerSubtitleState.enabled'),(tag,'immediate subtitles Off')
      assert 'Off' in page.locator('#player-subtitles-option').inner_text()
      assert_anchored(page,tag+' selected without closing')
     else:
      page.locator('#player-subtitles-option').click()
      page.locator('.player-settings-back').click()
      assert page.locator('#player-speed-option').count()==1,(tag,'submenu back')
     # Menu click is an explicit close; page remains uninert and no backdrop is created.
     if i%3==0:page.keyboard.press('Escape')
     elif i%3==1:settings.evaluate('el=>el.click()')
     else:page.locator('#player-area').evaluate("el=>el.dispatchEvent(new MouseEvent('click',{bubbles:true}))")
     assert page.locator('#player-settings-popover').count()==0,(tag,'close route')
     page.wait_for_timeout(490 if motion=='no-preference' else 25)
     returned=pose(page)
     assert_pose(returned,False,motion,tag+' reverse')
     # Relative geometry is invariant under legitimate viewport/workspace scrolling
     # caused by submenu focus. Preserve the strict .5px layout check.
     assert all(near(x,y,.5) for x,y in zip(before['rect'],returned['rect'])),(tag,'closing changed geometry',before['rect'],returned['rect'])
     # Rapid reopen should not be blocked by the old global modal lifecycle.
     if i==0:
      settings.evaluate('el=>el.click()')
      assert_anchored(page,tag+' immediate reopen')
      page.keyboard.press('Escape')
      assert page.locator('#player-settings-popover').count()==0,(tag,'rapid Escape closes')
      page.wait_for_timeout(490 if motion=='no-preference' else 25)
     total+=1
    print('PASS in-player menu',mode,motion,width,'six themes, placement, speed/subtitles, exit and icon',flush=True)
   assert not errs,(mode,motion,'page errors',errs)
   page.close()
 browser.close()
 assert total==48,total
 print('PASS 48 contexts: exact G1 SVG and 450ms/reduced-motion poses, in-player position, interactive playback settings without dimming, six themes, desktop/narrow, keyboard and outside close',flush=True)
