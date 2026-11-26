#!/usr/bin/env python3
"""Real-route Player Settings G1 matching click/open/close comparison.

Verify both generated modes, six themes, desktop/mobile, normal/reduced motion,
exact main Settings SVG apart from original Player 21px scale, shared 450ms
easing, no hover-only animation, instant-on-click active state, five dialog
dismissal/replacement paths, maintained focus/ARIA, and stable control geometry.
"""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT='https://gallery-player-settings-motion.invalid/'
FILES=(('full','gallery/Gallery-current.html'),('lightweight','gallery/Gallery-development.html'))
THEMES=('ocean','twilight','ember','slate','glacier','verdant')
EXPECTED_EASE='cubic-bezier(0.22, 0.72, 0.2, 1)'
def near(x,y,t=.22):
 return abs(float(x)-float(y))<=t
def pose(page):
 return page.locator('#player-settings').evaluate("""el=>{
 const svg=el.querySelector('svg'),gs=[...svg.querySelectorAll('.g1-settings-knob')];
 const rect=node=>{const r=node.getBoundingClientRect();return [r.x,r.y,r.width,r.height]};
 return {active:el.dataset.g1Active,label:el.getAttribute('aria-label'),
  duration:gs.map(g=>getComputedStyle(g).transitionDuration),
  easing:gs.map(g=>getComputedStyle(g).transitionTimingFunction),
  shifts:gs.map(g=>new DOMMatrix(getComputedStyle(g).transform).e),
  button:rect(el),svg:rect(svg),paths:svg.querySelectorAll('path').length,
  knobs:gs.length};
}""")
def assert_pose(p,active,motion,tag):
 assert p['active']==str(active).lower(),(tag,'state',p)
 expect=(6,-6) if active else (0,0)
 assert all(near(x,y) for x,y in zip(p['shifts'],expect)),(tag,'knobs',p)
 assert p['duration']==(['0s']*2 if motion=='reduce' else ['0.45s']*2),(tag,'duration',p)
 # With transition:none, Chromium reports the default 'ease' value; no interpolation occurs.
 assert p['easing']==(['ease']*2 if motion=='reduce' else [EXPECTED_EASE]*2),(tag,'easing',p)
def stable(p,q,tag):
 for kind in ('button','svg'):
  assert all(near(a,b,.40) for a,b in zip(p[kind],q[kind])),(tag,kind,p,q)
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path=os.environ.get('GALLERY_TEST_CHROMIUM') or None,args=['--no-sandbox','--disable-dev-shm-usage'])
 tested=0
 for mode,file in FILES:
  raw=Path(file).read_bytes()
  for motion in ('no-preference','reduce'):
   page=browser.new_page(viewport={'width':1100,'height':850},reduced_motion=motion)
   errors=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.route(ROOT+'**',lambda route:route.fulfill(status=200,content_type='text/html; charset=utf-8',body=raw))
   page.goto(ROOT,wait_until='domcontentloaded')
   page.locator('[data-detail]').first.click()
   page.wait_for_function("()=>!!state.detailId&&!galleryStageFadeInProgress&&!galleryStageTransition",timeout=10000)
   page.locator('.detail-actions [data-episode-action="watch"]').first.click()
   page.wait_for_function("()=>!!state.playback&&!!document.getElementById('player-settings')&&!galleryStageFadeInProgress&&!galleryStageTransition",timeout=10000)
   page.locator('#sf-player-demo-start').click()
   page.wait_for_function("()=>sfPlayerDemo.active&&document.getElementById('player-empty').hidden",timeout=10000)
   settings=page.locator('#player-settings')
   assert settings.count()==1 and settings.is_visible() and settings.get_attribute('aria-label')=='Player settings'
   assert page.locator('#fullscreen .g4-fullscreen-piece').count()==4,'Previously approved fullscreen glyph changed'
   main_svg=page.locator('#settings .g1-settings-icon').evaluate('(el)=>el.outerHTML')
   player_svg=settings.locator('svg').evaluate("""el=>{
    const s=el.cloneNode(true);s.setAttribute('width','23');s.setAttribute('height','23');return s.outerHTML;
   }""")
   assert main_svg==player_svg,(mode,motion,'Exact main Settings SVG geometry differs',main_svg,player_svg)
   assert settings.locator('svg').get_attribute('width')=='21'
   for width in (1100,430):
    page.set_viewport_size({'width':width,'height':850})
    for index,theme in enumerate(THEMES):
     page.evaluate('theme=>{document.body.dataset.theme=theme;state.theme=theme}',theme)
     tag=f'{mode}/{motion}/{width}/{theme}'
     main_before=page.locator('#settings').evaluate('el=>({active:el.dataset.g1Active,html:el.innerHTML})')
     page.mouse.move(0,0)
     page.wait_for_timeout(490 if motion=='no-preference' else 25)
     rest=pose(page)
     assert rest['label']=='Player settings' and rest['paths']==1 and rest['knobs']==2,tag
     assert_pose(rest,False,motion,tag+' rest')
     settings.hover()
     page.wait_for_timeout(35)
     assert_pose(pose(page),False,motion,tag+' hover must not animate')
     # Modal opening and G1 slider transition must be committed by the
     # synchronous accepted-click handler, not the delayed dialog animation.
     if index==0 and width==1100:
      settings.focus()
      settings.press('Enter')
     else:
      settings.click()
     assert settings.get_attribute('data-g1-active')=='true',tag+' same-click active'
     assert page.locator('.dialog[aria-label="Player settings"]').count()==1,tag+' dialog opens'
     assert page.locator('#settings').evaluate('el=>({active:el.dataset.g1Active,html:el.innerHTML})')==main_before,tag+' main Settings unaffected'
     page.wait_for_timeout(495 if motion=='no-preference' else 25)
     opened=pose(page)
     assert_pose(opened,True,motion,tag+' open')
     stable(rest,opened,tag+' button geometry unchanged')
     assert page.locator('.overlay').count()==1,tag+' open overlay'
     dismissal=index % 5
     if dismissal==0:
      page.locator('#close-dialog').click()
     elif dismissal==1:
      page.keyboard.press('Escape')
     elif dismissal==2:
      page.locator('.overlay').evaluate("el=>el.dispatchEvent(new MouseEvent('click',{bubbles:true}))")
     elif dismissal==3:
      page.locator('#save-player-settings').click()
     else:
      page.evaluate("()=>modal('Replacement test','<p>Dialog replacement</p>')")
     # This is the essential immediate-reversal assertion, before the
     # exit lifecycle has removed or hidden the old dialog.
     assert settings.get_attribute('data-g1-active')=='false',(tag,'immediate closing',dismissal)
     if dismissal==4:
      assert page.locator('.dialog[aria-label="Replacement test"]').count()==1,tag
      page.locator('#close-dialog').click()
     page.wait_for_function("()=>!document.querySelector('#modal-host .overlay')",timeout=6000)
     page.wait_for_timeout(490 if motion=='no-preference' else 25)
     returned=pose(page)
     assert_pose(returned,False,motion,tag+' returned')
     stable(rest,returned,tag+' geometry after dialog')
     assert page.locator('#settings').evaluate('el=>({active:el.dataset.g1Active,html:el.innerHTML})')==main_before,tag+' unaffected on closing'
     # The original Player regression programmatically reopens while a prior
     # Apply dismissal is still exiting. Preserve that existing reentry path,
     # and keep the new G1 icon active for the replacement dialog.
     if index==0 and width==1100:
      settings.click()
      assert settings.get_attribute('data-g1-active')=='true',tag+' rapid opener active'
      page.locator('#save-player-settings').click()
      assert settings.get_attribute('data-g1-active')=='false',tag+' rapid exit immediate reverse'
      settings.evaluate('(el)=>el.click()')
      assert page.locator('.dialog[aria-label="Player settings"]').count()==1,tag+' rapid dialog replacement'
      assert settings.get_attribute('data-g1-active')=='true',tag+' replacement keeps active pose'
      page.locator('#save-player-settings').click()
      assert settings.get_attribute('data-g1-active')=='false',tag+' rapid final reverse'
      page.wait_for_function("()=>!document.querySelector('#modal-host .overlay')",timeout=6000)
      page.wait_for_timeout(490 if motion=='no-preference' else 25)
      assert_pose(pose(page),False,motion,tag+' rapid final rest')
     tested+=1
    print('PASS Player Settings',mode,motion,width,'six themes, click/keyboard and dismissal',flush=True)
   assert not errors,(mode,motion,errors)
   page.close()
 browser.close()
 assert tested==48,tested
 print('PASS 48 contexts: shared SVG, 450ms original G1 motion, click-open/close, hover inert, Escape/X/Apply/backdrop/replacement, six themes, both builds, reduced motion, preserved main Settings/fullscreen/geometry',flush=True)
