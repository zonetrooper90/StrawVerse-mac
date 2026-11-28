#!/usr/bin/env python3
"""Guarded release comparison of approved Player/toolbar polish in BOTH built modes.

48 combinations of 2 HTML modes, 2 widths, 2 motion preferences and 6
themes. Preserve existing independent full/lightweight regression scripts.
"""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

FILES=(("full","gallery/Gallery-current.html"),("lightweight","gallery/Gallery-development.html"))
THEMES=("ocean","twilight","ember","slate","glacier","verdant")
ROOT="https://gallery-approved-polish-audit.invalid/"
def near(a,b,t=.35):return abs(float(a)-float(b))<=t

with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path=os.environ.get("GALLERY_TEST_CHROMIUM") or None,
                            args=["--no-sandbox","--disable-dev-shm-usage"])
 total=0
 for mode,path in FILES:
  raw=Path(path).read_bytes()
  assert (b"data:image/png;base64," in raw)==(mode=="full"),(mode,"asset payload mode")
  for width in (1280,430):
   for motion in ("no-preference","reduce"):
    page=browser.new_page(viewport={"width":width,"height":870},reduced_motion=motion)
    errors=[]
    page.on("pageerror",lambda e:errors.append(str(e)))
    page.route(ROOT+"**",lambda route:route.fulfill(status=200,content_type="text/html; charset=utf-8",body=raw))
    page.goto(ROOT,wait_until="domcontentloaded")
    for theme in THEMES:
     page.evaluate("(x)=>{state.theme=x;document.body.dataset.theme=x}",theme)
     metrics=page.evaluate("""()=>{
      const buttons=['search','header-watch-history','settings'].map(id=>{
       const r=document.getElementById(id).getBoundingClientRect();
       return [r.x,r.y,r.width,r.height];
      });
      return {buttons,
       search:getComputedStyle(document.querySelector('#search>.icon')).transform,
       history:getComputedStyle(document.querySelector('#header-watch-history>.g1-history-icon')).transform};
     }""")
     assert all(near(b[2],40,.2) and near(b[3],40,.2) for b in metrics["buttons"]),(mode,width,theme,"toolbar geometry",metrics)
     assert metrics["search"] not in ("none","matrix(1, 0, 0, 1, -0.45, -0.45)"),(mode,theme,"search optical alignment")
     assert metrics["history"] not in ("none","matrix(1, 0, 0, 1, 0.35, 0)"),(mode,theme,"history optical alignment")
     total+=1
    page.locator("[data-detail]").first.click()
    page.wait_for_function("()=>!!state.detailId&&!galleryStageFadeInProgress&&!galleryStageTransition",timeout=12000)
    page.locator('.detail-actions [data-episode-action="watch"]').first.click()
    page.wait_for_function("()=>!!state.playback&&!!document.getElementById('player-settings')&&!galleryStageFadeInProgress&&!galleryStageTransition",timeout=12000)
    page.locator("#sf-player-demo-start").click()
    page.wait_for_function("()=>sfPlayerDemo.active&&document.getElementById('player-empty').hidden",timeout=12000)
    # Play/pause icon remains a path morph without a blurry CSS filter.
    icon=page.locator("#player-play-morph-svg")
    assert icon.count()==1 and icon.locator("path").count()==2
    assert icon.evaluate("e=>getComputedStyle(e).filter")=="none",(mode,motion,"play glyph blur")
    assert all(icon.locator("path").nth(i).get_attribute("d") for i in range(2)),(mode,"play glyph paths")
    for id in ("pause-play","rewind10","forward10"):
     el=page.locator("#"+id)
     r=el.bounding_box()
     page.mouse.move(r["x"]+r["width"]/2,r["y"]+r["height"]/2)
     page.mouse.down()
     pressed=el.evaluate("e=>getComputedStyle(e).transform")
     assert pressed=="none",(mode,motion,id,"no press-induced icon displacement",pressed)
     page.mouse.up()
    volume=page.locator("#volume")
    if volume.is_visible():
     volume.fill("35")
     page.wait_for_timeout(180)
     badge=page.locator("#player-volume-feedback")
     assert badge.inner_text().strip()=="35%" and badge.evaluate("e=>getComputedStyle(e).opacity")!="0",(mode,motion,"volume numeric feedback")
    page.locator("#mute").click()
    assert page.locator("#player-volume-feedback").inner_text().strip()=="0%",(mode,motion,"muted volume feedback")
    page.locator("#player-settings").evaluate("e=>e.click()")
    menu=page.locator("#player-settings-popover")
    assert menu.count()==1 and menu.is_visible()
    page.wait_for_timeout(230 if motion=="no-preference" else 15)
    before=menu.evaluate("""e=>{
     const c=getComputedStyle(e),r=e.getBoundingClientRect();
     return {bg:c.backgroundColor,x:c.overflowX,width:r.width,right:r.right,scroll:window.scrollX,animation:c.animationName}
    }""")
    assert before["bg"].endswith(", 0.65)"),(mode,motion,"exact approved 65% glass",before)
    assert before["x"]=="hidden",(mode,width,"no horizontal scrollbar",before)
    assert before["animation"]==("none" if motion=="reduce" else "player-settings-in"),(mode,motion,"outer popup animation preserved",before)
    page.locator("#player-speed-option").click()
    assert menu.locator(".player-settings-popover-items").evaluate("e=>getComputedStyle(e).animationName")=="none",(mode,motion,"instant submenu")
    page.wait_for_timeout(35)
    after=menu.evaluate("""e=>{
     const r=e.getBoundingClientRect();return {width:r.width,right:r.right,scroll:window.scrollX}
    }""")
    assert near(before["width"],after["width"],.2) and near(before["right"],after["right"],.2),(mode,motion,"menu geometry jump",before,after)
    assert before["scroll"]==after["scroll"],(mode,motion,"page horizontal movement")
    page.locator('[data-player-menu="speed:1.5"]').click()
    assert page.evaluate('document.querySelector("#local-video").playbackRate')==1.5,(mode,motion,"speed applied")
    page.keyboard.press("Escape")
    assert menu.count()==0,(mode,"menu Escape")
    assert not errors,(mode,motion,"JS errors",errors)
    page.close()
  print("PASS Player/toolbar integrated release comparison",mode,"six themes, two sizes, both motion modes",flush=True)
 browser.close()
 assert total==48,total
 print("PASS 48 full/lightweight-theme contexts: optical alignment, stable controls, play morph, volume number, glass .65, instant submenu, no horizontal scrollbar",flush=True)
