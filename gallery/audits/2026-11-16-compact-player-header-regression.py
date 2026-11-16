#!/usr/bin/env python3
"""Actual route geometry: compact Player exception, preserved standard headers."""
import os,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
source=Path(sys.argv[1]).read_text(encoding="utf-8")
origin="https://gallery-compact-player.invalid/"
themes=("ocean","twilight","ember","slate","glacier","verdant")
sizes=((1440,900),(1280,650),(750,900),(420,900),(340,700))
def settled(page):
    page.wait_for_function("()=>!galleryStageTransition&&!galleryStageFadeInProgress&&!galleryStagePending&&!gallerySettingsOpening",timeout=10000)
def resize(page,width,height):
    page.set_viewport_size({"width":width,"height":height})
    page.evaluate("()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))")
def standard(page,selector,primary=False):
    for width,height in sizes:
        resize(page,width,height)
        data=page.locator(selector).evaluate("""(el,primary)=>{
          const band=primary?el.querySelector('.page-header-primary'):el;
          const divider=primary?el.querySelector('.page-header-divider'):null;
          const style=getComputedStyle(band),after=getComputedStyle(band,'::after');
          return {min:parseFloat(style.minHeight),height:band.getBoundingClientRect().height,
          divider:primary?divider?.getBoundingClientRect().height:parseFloat(after.height),
          content:primary?'explicit':after.content};
        }""",primary)
        expected=86 if width<=750 else 94
        assert data["min"]==expected and data["height"]>=expected-.5,(selector,width,height,data)
        assert data["divider"]==1 and data["content"]!="none",(selector,width,height,data)
def player(page):
    for width,height in sizes:
        resize(page,width,height)
        data=page.evaluate("""()=>{
          const bar=document.querySelector('.playback-compactbar'),title=bar.querySelector('.playback-title-inline'),
          back=bar.querySelector('#back-from-playback'),frame=document.querySelector('#player-area'),
          nav=document.querySelector('.player-episode-nav'),pg=document.querySelector('.playback-page');
          const rect=e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height,right:r.right,bottom:r.bottom,cy:r.y+r.height/2}};
          const s=getComputedStyle(bar),f=getComputedStyle(frame);
          return {bar:rect(bar),title:rect(title),back:rect(back),frame:rect(frame),nav:rect(nav),page:rect(pg),
          divider:getComputedStyle(bar,'::after').content,border:parseFloat(s.borderBottomWidth),
          maxHeight:parseFloat(f.maxHeight),titleText:title.textContent,backText:back.textContent,
          tabs:getComputedStyle(document.querySelector('.top .tabs')).display,innerHeight};
        }""")
        bar,title,back,frame,nav,pg=(data[k] for k in ("bar","title","back","frame","nav","page"))
        budget=169 if width<=740 else 182
        expected=min(pg["w"],(data["innerHeight"]-budget)*16/9)
        old_expected=min(pg["w"],(data["innerHeight"]-(218 if width<=740 else 231))*16/9)
        assert abs(bar["h"]-45)<=.5 and data["border"]==0 and data["divider"] in ("none","normal"),data
        assert abs(back["cy"]-bar["cy"])<=.5 and title["right"]<=back["x"]+1,data
        assert abs(title["x"]-bar["x"])<=1 and abs(back["right"]-bar["right"])<=1,data
        assert title["w"]>0 and data["titleText"].strip() and "Back to episodes" in data["backText"],data
        assert frame["y"]>=bar["bottom"]-.5 and frame["y"]-bar["bottom"]<=8,data
        assert abs(data["maxHeight"]-(data["innerHeight"]-budget))<=.5 and abs(frame["w"]-expected)<=2,data
        assert frame["w"]>=old_expected-2 and (expected-old_expected<=2 or frame["w"]>old_expected+1),data
        assert abs(nav["x"]-frame["x"])<=1 and abs(nav["w"]-frame["w"])<=1,data
        assert frame["x"]>=pg["x"]-1 and frame["right"]<=pg["right"]+1 and data["tabs"]=="none",data
        print("PASS compact Player",width,height,page.evaluate("state.theme"),page.evaluate("galleryReducedMotion.matches"),"frame",frame["w"],"recovered",round(frame["w"]-old_expected,1),flush=True)
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path=os.environ.get("GALLERY_TEST_CHROMIUM") or None,args=["--no-sandbox"])
    for motion in ("no-preference","reduce"):
      for theme in themes:
        page=browser.new_page(viewport={"width":1440,"height":900},reduced_motion=motion)
        errors=[];page.on("pageerror",lambda e:errors.append(str(e)))
        page.route(origin+"**",lambda route:route.fulfill(status=200,content_type="text/html; charset=utf-8",body=source))
        page.goto(origin,wait_until="domcontentloaded")
        page.evaluate("t=>{state.theme=t;document.body.dataset.theme=t}",theme)
        for view in ("discover","library","downloads"):
            resize(page,1440,900)
            if view!="discover":
                page.locator("#nav-"+view).click()
                page.wait_for_function("v=>state.view===v",arg=view)
                settled(page)
            standard(page,'[data-tab-page="'+view+'"] .page-header',True)
        resize(page,1440,900)
        page.locator("#nav-discover").click();settled(page)
        page.locator('[data-tab-page="discover"] .poster-button[data-detail]').first.click()
        page.wait_for_selector("#detail-back");settled(page)
        standard(page,".detail-page-header")
        resize(page,1440,900)
        page.locator('.detail-actions [data-episode-action="watch"]').first.click()
        page.wait_for_selector("#back-from-playback");settled(page)
        player(page)
        resize(page,1440,900)
        page.locator("#sf-player-demo-start").click()
        page.locator("#fullscreen").click()
        page.wait_for_function("()=>document.fullscreenElement===document.getElementById('player-area')",timeout=10000)
        box=page.locator("#player-area").bounding_box()
        assert abs(box["width"]-1440)<=1 and abs(box["height"]-900)<=1,box
        page.locator("#fullscreen").click()
        page.wait_for_function("()=>!document.fullscreenElement",timeout=10000)
        page.locator("#back-from-playback").click();page.wait_for_selector("#detail-back");settled(page)
        page.locator("#detail-back").click();settled(page)
        page.locator("#header-watch-history").click();page.wait_for_selector("#wh-root [data-wh-exit]");settled(page)
        standard(page,"#wh-root > .wh-page-header")
        resize(page,1440,900)
        page.locator("#wh-root [data-wh-exit]").click();settled(page)
        page.locator("#settings").click();page.wait_for_selector("#settings-back");settled(page)
        standard(page,".settings-page-head")
        resize(page,1440,900)
        page.locator("#settings-back").click();settled(page)
        assert not errors,errors
        page.close()
    browser.close()
print("PASS 60 compact Player configurations, 12 fullscreen cycles and retained standard header geometry",flush=True)
