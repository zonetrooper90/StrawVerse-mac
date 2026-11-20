#!/usr/bin/env python3
"""G1.1: accepted clicks animate before the route midpoint in both HTML modes."""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT="https://gallery-g11-click-audit.invalid/"
FILES=(("full","gallery/Gallery-current.html"),
       ("lightweight","gallery/Gallery-development.html"))
HOOK=r"""()=>{
 window.__g11Clicks=[];
 document.addEventListener('click',event=>{
  const target=event.target.closest('#header-watch-history,#settings,#settings-back,[data-wh-exit]');
  if(!target)return;
  const history=document.getElementById('header-watch-history');
  const settings=document.getElementById('settings');
  window.__g11Clicks.push({
   id:target.id||'history-back',
   wh:history.dataset.g1Active,
   settings:settings.dataset.g1Active,
   whAria:history.getAttribute('aria-pressed'),
   settingsAria:settings.getAttribute('aria-expanded'),
   historyCommitted:whOpen,
   settingsCommitted:document.body.classList.contains('settings-view'),
   fading:galleryStageFadeInProgress
  });
 },false); // document bubble occurs after the accepted control click handler
}"""
def settled(page):
    page.wait_for_function(
        "()=>!galleryStageFadeInProgress&&!galleryStagePending&&!gallerySettingsOpening&&!settingsClosing",
        timeout=20000)
def click(page,selector):
    page.evaluate("()=>{window.__g11Clicks.length=0}")
    page.locator(selector).click(timeout=15000)
    data=page.evaluate("()=>window.__g11Clicks")
    assert data and len(data)==1,(selector,data)
    return data[0]
def open_history(page,normal):
    snap=click(page,"#header-watch-history")
    assert snap["wh"]=="true",snap
    if normal:
        assert snap["historyCommitted"] is False and snap["whAria"]=="false" and snap["fading"],snap
    page.wait_for_function("()=>whOpen")
    settled(page)
    assert page.locator("#header-watch-history").get_attribute("aria-pressed")=="true"
def close_history(page,normal,selector="#header-watch-history"):
    snap=click(page,selector)
    assert snap["wh"]=="false",snap
    if normal:
        assert snap["historyCommitted"] is True and snap["whAria"]=="true" and snap["fading"],snap
    page.wait_for_function("()=>!whOpen")
    settled(page)
    assert page.locator("#header-watch-history").get_attribute("aria-pressed")=="false"
def open_settings(page,normal):
    snap=click(page,"#settings")
    assert snap["settings"]=="true",snap
    if normal:
        assert snap["settingsCommitted"] is False and snap["settingsAria"]=="false" and snap["fading"],snap
    page.wait_for_function("()=>document.body.classList.contains('settings-view')")
    settled(page)
    assert page.locator("#settings").get_attribute("aria-expanded")=="true"
def close_settings(page,normal,selector="#settings"):
    snap=click(page,selector)
    assert snap["settings"]=="false",snap
    if normal:
        assert snap["settingsCommitted"] is True and snap["settingsAria"]=="true" and snap["fading"],snap
    page.wait_for_function("()=>!document.body.classList.contains('settings-view')")
    settled(page)
    assert page.locator("#settings").get_attribute("aria-expanded")=="false"

with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,
        executable_path=os.environ.get("GALLERY_TEST_CHROMIUM") or None,
        args=["--no-sandbox"])
    total=0
    for mode,path in FILES:
        source=Path(path).read_bytes()
        for preference in ("no-preference","reduce"):
            normal=preference=="no-preference"
            page=browser.new_page(viewport={"width":1100,"height":850},
                reduced_motion=preference)
            errors=[]
            page.on("pageerror",lambda exc:errors.append(str(exc)))
            page.route(ROOT+"**",lambda route:route.fulfill(
                status=200,content_type="text/html; charset=utf-8",body=source))
            page.goto(ROOT,wait_until="domcontentloaded")
            settled(page)
            page.evaluate(HOOK)
            timing=page.evaluate("""()=>{
             const history=getComputedStyle(document.querySelector('#header-watch-history .g1-history-rim'));
             const settings=getComputedStyle(document.querySelector('#settings .g1-settings-knob'));
             return {history:history.transitionDuration,settings:settings.transitionDuration};
            }""")
            assert timing==({"history":"1.1s","settings":"0.45s"} if normal
                            else {"history":"0s","settings":"0s"}),(mode,preference,timing)
            open_history(page,normal)
            close_history(page,normal)
            open_history(page,normal)
            close_history(page,normal,"#wh-root [data-wh-exit]")
            open_history(page,normal)
            open_settings(page,normal)
            assert page.locator("#header-watch-history").get_attribute("data-g1-active")=="true"
            close_settings(page,normal)
            assert page.locator("#header-watch-history").get_attribute("data-g1-active")=="true"
            close_history(page,normal)
            open_settings(page,normal)
            close_settings(page,normal)
            open_settings(page,normal)
            close_settings(page,normal,"#settings-back")
            open_settings(page,normal)
            page.keyboard.press("Escape")
            assert page.locator("#settings").get_attribute("data-g1-active")=="false"
            page.wait_for_function("()=>!document.body.classList.contains('settings-view')")
            settled(page)
            assert not errors,(mode,preference,errors)
            print("PASS G1.1 immediate click/Back/Escape",mode,preference,
                  "History=1100ms Settings=450ms" if normal else "reduced-motion snap",
                  flush=True)
            page.close()
            total+=1
    browser.close()
print("PASS G1.1 click-time motion in",total,"full/lightweight × normal/reduced contexts",flush=True)
