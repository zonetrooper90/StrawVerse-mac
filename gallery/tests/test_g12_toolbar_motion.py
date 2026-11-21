#!/usr/bin/env python3
"""Read-only G1.2 icon-motion audit on exactly one generated Gallery HTML build."""
import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

HTML=Path(sys.argv[1])
assert HTML.is_file()
ROOT="https://gallery-g12-audit.invalid/"
THEMES=("ocean","twilight","ember","slate","glacier","verdant")
WIDTHS=((1100,850),(390,780))
MEASURE=r"""() => {
 const ids=['search','header-watch-history','settings'];
 const box=el=>{const r=el.getBoundingClientRect();return {
   x:r.x,y:r.y,w:r.width,h:r.height,right:r.right,cx:r.x+r.width/2,cy:r.y+r.height/2}};
 const buttons=ids.map(id=>document.getElementById(id));
 return {buttons:buttons.map(box),icons:buttons.map(b=>box(b.querySelector('svg'))),
         field:box(document.getElementById('header-search-field')),open:searchOpen};
}"""
REVERSE=r"""([selector,id]) => {
 const el=document.querySelector(selector),button=document.getElementById(id);
 const matrix=()=>{let a=new DOMMatrix(getComputedStyle(el).transform);
   return [a.a,a.b,a.c,a.d,a.e,a.f];};
 const before=matrix();
 button.click();
 return {before,after:matrix(),active:button.dataset.g1Active,
   history:whOpen,settings:document.body.classList.contains('settings-view'),
   fading:galleryStageFadeInProgress};
}"""

def near(a,b,tol=.75):
    return abs(a-b)<=tol

def geometry(obj,where):
    bs=obj["buttons"]
    assert all(near(b["w"],40) and near(b["h"],40) for b in bs),(where,bs)
    assert near(bs[1]["x"]-bs[0]["right"],8) and near(bs[2]["x"]-bs[1]["right"],8),(where,bs)
    assert all(near(b["cy"],bs[0]["cy"]) for b in bs),(where,bs)
    for b,i,size in zip(bs,obj["icons"],(21,21,23)):
        assert near(i["w"],size) and near(i["h"],size),(where,i)
        assert near(b["cx"],i["cx"]) and near(b["cy"],i["cy"]),(where,b,i)

def aligned(a,b,where):
    geometry(b,where)
    for first,second in zip(a["buttons"],b["buttons"]):
        assert all(near(first[k],second[k]) for k in ("x","y","w","h","cx","cy")),(where,a,b)

def settled(page):
    page.wait_for_function(
      "()=>!galleryStageFadeInProgress&&!galleryStagePending&&!gallerySettingsOpening&&!settingsClosing",
      timeout=20000)

def matrix_delta(snap):
    return max(abs(a-b) for a,b in zip(snap["before"],snap["after"]))

def search_cycle(page,normal,where):
    base=page.evaluate(MEASURE)
    page.locator("#search").click()
    assert page.evaluate("searchOpen"),where
    page.wait_for_timeout(100 if normal else 25)
    mid=page.evaluate(MEASURE)
    aligned(base,mid,where+" Search opening")
    assert mid["field"]["w"]>2 and mid["field"]["x"]>=-.75,(where,mid)
    snap=page.evaluate("""() => {
      const field=document.getElementById('header-search-field');
      const before=field.getBoundingClientRect().width;
      document.getElementById('search').click();
      return {before,after:field.getBoundingClientRect().width,open:searchOpen};
    }""")
    assert not snap["open"],(where,snap)
    if normal:assert abs(snap["before"]-snap["after"])<5,(where,snap)
    aligned(base,page.evaluate(MEASURE),where+" Search reversing")
    page.wait_for_timeout(405 if normal else 25)
    end=page.evaluate(MEASURE)
    aligned(base,end,where+" Search closed")
    assert not end["open"] and end["field"]["w"]<1,(where,end)
    assert page.locator("#header-search-field").get_attribute("aria-hidden")=="true"

def history_cycle(page,normal,where):
    base=page.evaluate(MEASURE)
    page.locator("#header-watch-history").click()
    assert page.locator("#header-watch-history").get_attribute("data-g1-active")=="true",where
    settled(page)
    assert page.evaluate("whOpen"),where
    aligned(base,page.evaluate(MEASURE),where+" History active")
    snap=page.evaluate(REVERSE,[".g1-history-rim","header-watch-history"])
    assert snap["active"]=="false",(where,snap)
    if normal:
        assert snap["history"] and snap["fading"],(where,snap)
        assert matrix_delta(snap)<.13,(where,snap)
        assert max(abs(snap["before"][0]-1),abs(snap["before"][1]))>.08,(where,snap)
    settled(page)
    assert not page.evaluate("whOpen"),where
    aligned(base,page.evaluate(MEASURE),where+" History returned")
    page.wait_for_timeout(1120 if normal else 25)
    end=page.evaluate("""() => {
      let a=new DOMMatrix(getComputedStyle(document.querySelector('.g1-history-rim')).transform);
      return [a.a,a.b];
    }""")
    assert near(end[0],1,.02) and near(end[1],0,.02),(where,end)
    assert page.locator("#header-watch-history").get_attribute("aria-pressed")=="false"

def settings_cycle(page,normal,where):
    base=page.evaluate(MEASURE)
    page.locator("#settings").click()
    assert page.locator("#settings").get_attribute("data-g1-active")=="true",where
    settled(page)
    assert page.evaluate("document.body.classList.contains('settings-view')"),where
    aligned(base,page.evaluate(MEASURE),where+" Settings active")
    before=page.evaluate("""() => [
       new DOMMatrix(getComputedStyle(document.querySelector('.g1-settings-knob.upper')).transform).e,
       new DOMMatrix(getComputedStyle(document.querySelector('.g1-settings-knob.lower')).transform).e
    ]""")
    assert .1<before[0]<=6.05 and -6.05<=before[1]<-.1,(where,before)
    snap=page.evaluate(REVERSE,[".g1-settings-knob.upper","settings"])
    assert snap["active"]=="false",(where,snap)
    if normal:
        assert snap["settings"] and snap["fading"],(where,snap)
        assert matrix_delta(snap)<.13,(where,snap)
    settled(page)
    assert not page.evaluate("document.body.classList.contains('settings-view')"),where
    aligned(base,page.evaluate(MEASURE),where+" Settings returned")
    page.wait_for_timeout(475 if normal else 25)
    end=page.evaluate("""() => [
       new DOMMatrix(getComputedStyle(document.querySelector('.g1-settings-knob.upper')).transform).e,
       new DOMMatrix(getComputedStyle(document.querySelector('.g1-settings-knob.lower')).transform).e
    ]""")
    assert all(abs(x)<.02 for x in end),(where,end)
    assert page.locator("#settings").get_attribute("aria-expanded")=="false"

with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,
      executable_path=os.environ.get("GALLERY_TEST_CHROMIUM") or None,
      args=["--no-sandbox","--disable-dev-shm-usage"])
    src=HTML.read_bytes()
    count=0
    for preference in ("no-preference","reduce"):
        normal=preference=="no-preference"
        page=browser.new_page(viewport={"width":1100,"height":850},reduced_motion=preference)
        errors=[]
        page.on("pageerror",lambda e:errors.append(str(e)))
        page.route(ROOT+"**",lambda route:route.fulfill(
          status=200,content_type="text/html; charset=utf-8",body=src))
        page.goto(ROOT,wait_until="domcontentloaded")
        settled(page)
        for width,height in WIDTHS:
            page.set_viewport_size({"width":width,"height":height})
            for theme in THEMES:
                page.evaluate("theme=>{state.theme=theme;document.body.dataset.theme=theme}",theme)
                where=f"{HTML.name} {preference} {theme} {width}"
                geometry(page.evaluate(MEASURE),where)
                search_cycle(page,normal,where)
                count+=1
            for theme in ("ocean","verdant"):
                page.evaluate("theme=>{state.theme=theme;document.body.dataset.theme=theme}",theme)
                where=f"{HTML.name} {preference} {theme} {width}"
                history_cycle(page,normal,where)
                settings_cycle(page,normal,where)
            print("PASS G1.2 theme/width",HTML.name,preference,width,flush=True)
        page.keyboard.press("Control+f")
        assert page.evaluate("searchOpen"),(HTML.name,preference)
        page.keyboard.press("Escape")
        assert not page.evaluate("searchOpen"),(HTML.name,preference)
        page.wait_for_timeout(410 if normal else 30)
        assert not errors,(HTML.name,preference,errors)
        page.close()
    browser.close()
print("PASS G1.2 toolbar interruption/geometry",HTML.name,count,"Search theme/width contexts")
