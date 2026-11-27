#!/usr/bin/env python3
"""Focused exact-artifact Player/toolbar visual behavior smoke (not a release gate).

Normal/reduced motion, desktop/narrow, two themes; check no scrollbar during
settings submenu slide, stable press geometry, transient volume percentage and
optical corrections without changing the existing toolbar/button dimensions.
"""
import os
from pathlib import Path
import sys
from playwright.sync_api import sync_playwright

raw=Path(sys.argv[1]).read_bytes()
assert b"data:image/png;base64," not in raw
URL="https://gallery-polish-preview.invalid/"
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path=os.environ.get("GALLERY_TEST_CHROMIUM") or None,
                            args=["--no-sandbox","--disable-dev-shm-usage"])
 total=0
 for width,motion in ((1280,"no-preference"),(430,"reduce")):
  page=browser.new_page(viewport={"width":width,"height":870},reduced_motion=motion)
  errors=[]
  page.on("pageerror",lambda e: errors.append(str(e)))
  page.route(URL+"**",lambda route:route.fulfill(status=200,content_type="text/html; charset=utf-8",body=raw))
  page.goto(URL,wait_until="domcontentloaded")
  for theme in ("ocean","ember"):
   page.evaluate("(x)=>{state.theme=x;document.body.dataset.theme=x}",theme)
   # Toolbar frame centers and widths remain invariant; only inner glyph offsets change.
   metrics=page.evaluate("""()=>{
    const vals=["search","header-watch-history","settings"].map(id=>{
     const el=document.getElementById(id);
     const r=el.getBoundingClientRect();
     return [r.x,r.y,r.width,r.height];
    });
    return {vals,search:getComputedStyle(document.querySelector("#search>.icon")).transform,
      history:getComputedStyle(document.querySelector("#header-watch-history>.g1-history-icon")).transform}
    }
   """)
   assert all(abs(q[2]-40)<.2 and abs(q[3]-40)<.2 for q in metrics["vals"]),(theme,width,"toolbar circle size",metrics)
   assert metrics["search"] not in ("none","matrix(1, 0, 0, 1, -0.45, -0.45)"),(theme,"search correction",metrics)
   assert metrics["history"] not in ("none","matrix(1, 0, 0, 1, 0.35, 0)"),(theme,"history correction",metrics)
   total+=1
  page.locator("[data-detail]").first.click()
  page.wait_for_function("()=>!!state.detailId&&!galleryStageFadeInProgress&&!galleryStageTransition",timeout=12000)
  page.locator('.detail-actions [data-episode-action="watch"]').first.click()
  page.wait_for_function("()=>!!state.playback&&!!document.getElementById('player-settings')&&!galleryStageFadeInProgress&&!galleryStageTransition",timeout=12000)
  page.locator("#sf-player-demo-start").click()
  page.wait_for_function("()=>sfPlayerDemo.active&&document.getElementById('player-empty').hidden",timeout=12000)
  for key in ("pause-play","rewind10","forward10"):
   el=page.locator("#"+key)
   r=el.bounding_box()
   page.mouse.move(r["x"]+r["width"]/2,r["y"]+r["height"]/2)
   page.mouse.down()
   # The entire control frame must never shrink on pointer activation.
   active=page.locator("#"+key).evaluate("e=>({transform:getComputedStyle(e).transform,r:e.getBoundingClientRect().toJSON()})")
   assert active["transform"]=="none",(key,width,motion,"pressed whole-button transform",active)
   page.mouse.up()
  vol=page.locator("#volume")
  if vol.is_visible():
   vol.fill("35")
   page.wait_for_timeout(180)
   badge=page.locator("#player-volume-feedback")
   assert badge.inner_text().strip()=="35%" and badge.evaluate("e=>getComputedStyle(e).opacity")!="0",(width,"volume feedback")
  page.locator("#mute").click()
  assert page.locator("#player-volume-feedback").inner_text().strip()=="0%",(width,"mute feedback")
  settings=page.locator("#player-settings")
  settings.evaluate("e=>e.click()")
  menu=page.locator("#player-settings-popover")
  assert menu.count()==1 and menu.is_visible()
  # The Player panel itself scales in for 180 ms; measure only the subsequent
  # submenu transition, when the anchored outer panel is stationary.
  page.wait_for_timeout(230 if motion=="no-preference" else 15)
  state=menu.evaluate("""e=>{
   const style=getComputedStyle(e),r=e.getBoundingClientRect();
   return {background:style.backgroundColor,overflowX:style.overflowX,
       width:r.width,right:r.right,scrollX:window.scrollX};
  }""")
  assert state["overflowX"]=="hidden",(width,"no transient horizontal scrollbar",state)
  assert state["background"].endswith(", 0.84)"),(width,"translucent popover",state)
  page.locator("#player-speed-option").click()
  page.wait_for_timeout(35)
  during=menu.evaluate("""e=>({r:e.getBoundingClientRect().toJSON(),scrollX:window.scrollX})""")
  assert abs(during["r"]["width"]-state["width"])<.2 and abs(during["r"]["right"]-state["right"])<.2,(width,"menu width/edge jump")
  assert during["scrollX"]==state["scrollX"],(width,"unwanted page horizontal scroll")
  page.locator('[data-player-menu="speed:1.5"]').click()
  assert page.evaluate('document.querySelector("#local-video").playbackRate')==1.5
  page.keyboard.press("Escape")
  assert menu.count()==0
  assert not errors,(width,motion,errors)
  page.close()
  print("PASS Player/toolbar polish preview",width,motion,"both themes, anchored menu, stable button, volume feedback",flush=True)
 browser.close()
 assert total==4
