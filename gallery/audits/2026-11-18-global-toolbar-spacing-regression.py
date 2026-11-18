#!/usr/bin/env python3
"""Global header: actual circle/center/gap geometry on all routes, motion and themes."""
import os,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
source=Path(sys.argv[1]).read_bytes()
origin="https://gallery-toolbar-spacing.invalid/"
themes=("ocean","twilight","ember","slate","glacier","verdant")
sizes=((1440,900),(960,900),(750,900),(620,800),(420,900),(340,700))
def settled(page):
    page.wait_for_function("()=>!galleryStageTransition&&!galleryStageFadeInProgress&&!galleryStagePending&&!gallerySettingsOpening&&!settingsClosing",timeout=10000)
def frame(page):
    page.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
def geometry(page):
    return page.evaluate("""()=>{
      const box=e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height,right:r.right,bottom:r.bottom,cx:r.x+r.width/2,cy:r.y+r.height/2}};
      const buttons=['search','header-watch-history','settings'].map(id=>document.getElementById(id));
      return {buttons:buttons.map(box),icons:buttons.map(e=>box(e.querySelector('svg'))),wrapper:box(document.querySelector('#header-search')),
      field:box(document.querySelector('#header-search-field')),gap:getComputedStyle(document.querySelector('.toolbar')).columnGap,
      disabled:buttons[1].disabled,viewport:innerWidth,theme:document.body.dataset.theme};
    }""")
def close(a,b):return abs(a-b)<=.5
def assert_geometry(data,disabled):
    a,b,c=data["buttons"]
    assert data["gap"]=="8px" and data["disabled"]==disabled,data
    assert all(close(e["w"],40) and close(e["h"],40) for e in (a,b,c)),data
    assert close(b["x"]-a["right"],8) and close(c["x"]-b["right"],8),data
    assert close(b["cx"]-a["cx"],48) and close(c["cx"]-b["cx"],48),data
    assert close(a["cy"],b["cy"]) and close(b["cy"],c["cy"]),data
    assert a["x"]>=0 and c["right"]<=data["viewport"]+.5,data
    assert all(close(a[k],data["wrapper"][k]) for k in ("x","y","w","h")),data
    assert [(e["w"],e["h"]) for e in data["icons"]]==[(21,21),(21,21),(23,23)],data
def sweep(page,label,disabled=False):
    for theme in themes:
        page.evaluate("t=>{state.theme=t;document.body.dataset.theme=t}",theme)
        for width,height in sizes:
            page.set_viewport_size({"width":width,"height":height});frame(page)
            assert_geometry(geometry(page),disabled)
    page.set_viewport_size({"width":1440,"height":900});frame(page)
    print("PASS toolbar geometry",label,36,"configurations",flush=True)
def search_cycle(page,motion):
    # Separate real interaction test, across responsive breakpoints.
    for width,height in sizes:
        page.set_viewport_size({"width":width,"height":height});frame(page)
        before=geometry(page)
        page.locator("#search").click()
        page.wait_for_function("()=>searchOpen")
        page.wait_for_timeout(380 if motion=="no-preference" else 30)
        after=geometry(page);assert_geometry(after,False)
        assert before["buttons"]==after["buttons"],(before,after)
        assert close(after["buttons"][0]["x"]-after["field"]["right"],8),after
        assert after["field"]["x"]>=-.5,after
        assert page.locator("#header-search-input").evaluate("e=>document.activeElement===e")
        page.locator("#header-search-input").press("Escape")
        page.wait_for_function("()=>!searchOpen")
        page.wait_for_timeout(380 if motion=="no-preference" else 30)
        assert geometry(page)["buttons"]==before["buttons"]
    page.set_viewport_size({"width":1440,"height":900});frame(page)
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path=os.environ.get("GALLERY_TEST_CHROMIUM") or None,args=["--no-sandbox"])
    for motion in ("no-preference","reduce"):
        page=browser.new_page(viewport={"width":1440,"height":900},reduced_motion=motion)
        errors=[];page.on("pageerror",lambda e:errors.append(str(e)))
        page.route(origin+"**",lambda r:r.fulfill(status=200,content_type="text/html; charset=utf-8",body=source))
        page.goto(origin,wait_until="domcontentloaded");settled(page)
        for view in ("discover","library","downloads"):
            if view!="discover":
                page.locator("#nav-"+view).click()
                page.wait_for_function("v=>state.view===v",arg=view);settled(page)
            sweep(page,view)
            search_cycle(page,motion)
        page.locator("#nav-discover").click();page.wait_for_function("()=>state.view==='discover'");settled(page)
        page.locator('[data-tab-page="discover"] .poster-button[data-detail]').first.click()
        page.wait_for_selector("#detail-back");settled(page);sweep(page,"Anime Details")
        page.locator('.detail-actions [data-episode-action="watch"]').first.click()
        page.wait_for_selector("#back-from-playback");settled(page);sweep(page,"Player",True)
        page.locator("#back-from-playback").click();page.wait_for_selector("#detail-back");settled(page)
        page.locator("#detail-back").click();settled(page)
        page.locator("#header-watch-history").click();page.wait_for_selector("#wh-root [data-wh-exit]");settled(page)
        sweep(page,"Watch History");search_cycle(page,motion)
        page.locator("#settings").click();page.wait_for_selector("#settings-back");settled(page)
        sweep(page,"Settings",True)
        page.locator("#settings-back").click();settled(page)
        assert not errors,errors
        page.close()
    browser.close()
print("PASS 504 toolbar route/theme/width/motion geometry configurations and 48 Search cycles",flush=True)
