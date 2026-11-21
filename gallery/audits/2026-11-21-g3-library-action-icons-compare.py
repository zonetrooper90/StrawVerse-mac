#!/usr/bin/env python3
"""G3 Library New Tag / More Actions actual-build hover and state audit, both modes."""
import math
import os
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT="https://gallery-g3-library-audit.invalid/"
BUILDS=(("full","gallery/Gallery-current.html"),("lightweight","gallery/Gallery-development.html"))
THEMES=("ocean","twilight","ember","slate","glacier","verdant")
def angle(page):
    raw=page.locator("#newtag .g3-plus-mark").evaluate("el=>el.style.transform")
    match=re.fullmatch(r"rotate\((\d+)deg\)",raw)
    return int(match.group(1)) if match else 0
def value(page, selector, prop):
    return page.locator(selector).evaluate("(el,prop)=>getComputedStyle(el)[prop]",prop)
def matrix_y(page, selector):
    return page.locator(selector).evaluate("(el)=>new DOMMatrix(getComputedStyle(el).transform).f")
def box(page, selector):
    return page.locator(selector).evaluate("(el)=>{let a=el.getBoundingClientRect();return [a.x,a.y,a.width,a.height]}")
def unchanged(a,b,label):
    assert all(abs(x-y)<.6 for x,y in zip(a,b)),(label,a,b)
def paths(page,label):
    assert page.locator("#newtag .g3-plus-mark path").get_attribute("d")=="M12 5v14M5 12h14",label
    assert page.locator("#newtag svg").get_attribute("viewBox")=="0 0 24 24",label
    assert page.locator("#newtag svg").get_attribute("width")=="17",label
    dots=page.locator("#tag-options .g3-thinking-dot")
    assert dots.count()==3,label
    assert [(dots.nth(i).get_attribute("cx"),dots.nth(i).get_attribute("cy"),dots.nth(i).get_attribute("r")) for i in range(3)]==[("5","12","1"),("12","12","1"),("19","12","1")],label
    assert page.locator("#tag-options svg").get_attribute("width")=="19",label
    assert page.locator("#import").count()==0 and page.locator("#sharetag").count()==0,label
    assert page.locator(".custom-tag-icon .icon").count()>=1,label

with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,
       executable_path=os.environ.get("GALLERY_TEST_CHROMIUM") or None,
       args=["--no-sandbox","--disable-dev-shm-usage"])
    cases=0
    for build,filename in BUILDS:
      raw=Path(filename).read_bytes()
      for motion in ("no-preference","reduce"):
       page=browser.new_page(viewport={"width":1100,"height":850},reduced_motion=motion)
       errors=[]
       page.on("pageerror",lambda e:errors.append(str(e)))
       page.route(ROOT+"**",lambda route:route.fulfill(status=200,content_type="text/html; charset=utf-8",body=raw))
       page.goto(ROOT,wait_until="domcontentloaded")
       page.locator("#nav-library").click()
       page.wait_for_function("()=>state.view==='library' && !!document.querySelector('#newtag')")
       page.wait_for_timeout(550)
       # Exercise the original Create Tag dialog; do not bypass menu availability.
       page.locator("#newtag").click()
       page.locator("#tag-name").fill("G3 Motion Audit")
       page.locator("#create-tag").click()
       page.wait_for_function("()=>!!document.querySelector('#tag-options') && state.tag==='G3 Motion Audit'")
       page.mouse.move(0,0)
       for width in (1100,390):
        page.set_viewport_size({"width":width,"height":850})
        for theme in THEMES:
         page.evaluate("t=>document.body.dataset.theme=t",theme)
         label=f"{build}/{motion}/{width}/{theme}"
         paths(page,label)
         before=box(page,"#newtag")
         svg_before=box(page,"#newtag svg")
         opts_before=box(page,"#tag-options")
         plus=page.locator("#newtag")
         initial=angle(page)
         plus.hover()
         page.wait_for_timeout(460 if motion=="no-preference" else 40)
         assert angle(page)==initial+90,(label,angle(page),initial)
         unchanged(before,box(page,"#newtag"),label+" button hover")
         unchanged(svg_before,box(page,"#newtag svg"),label+" svg hover")
         page.mouse.move(0,0)
         page.wait_for_timeout(90)
         assert angle(page)==initial+90,(label,"exit reversed")
         # Reenter and require a further clockwise quarter turn, not reset.
         plus.hover()
         page.wait_for_timeout(460 if motion=="no-preference" else 40)
         assert angle(page)==initial+180,(label,"second turn")
         page.mouse.move(0,0)
         page.wait_for_timeout(35)
         assert angle(page)==initial+180,(label,"second exit")
         assert value(page,"#newtag .g3-plus-mark","transitionDuration")==("0s" if motion=="reduce" else "0.4s"),label
         opts=page.locator("#tag-options")
         opts.hover()
         dots=page.locator("#tag-options .g3-thinking-dot")
         assert all(abs(float(value(page,f"#tag-options .g3-thinking-dot:nth-child({i})","opacity"))-1)<.001 for i in (1,2,3)),(label,"dot opacity")
         if motion=="no-preference":
          assert "g3-thinking-wave" in value(page,"#tag-options .g3-thinking-dot:first-child","animationName"),label
          page.wait_for_function("()=>{let el=document.querySelector('#tag-options .g3-thinking-dot');return new DOMMatrix(getComputedStyle(el).transform).f < -.45}",timeout=1400)
          assert all(abs(float(value(page,f"#tag-options .g3-thinking-dot:nth-child({i})","opacity"))-1)<.001 for i in (1,2,3)),(label,"opacity during motion")
          page.wait_for_timeout(760)
          assert not opts.evaluate("el=>el.classList.contains('g3-waving')"),(label,"wave replay")
         else:
          assert value(page,"#tag-options .g3-thinking-dot:first-child","animationName")=="none",label
         assert all(abs(matrix_y(page,f"#tag-options .g3-thinking-dot:nth-child({i})"))<.1 for i in (1,2,3)),(label,"settled positions")
         unchanged(opts_before,box(page,"#tag-options"),label+" menu geometry")
         opts.click()
         assert opts.get_attribute("aria-expanded")=="true" and page.locator("#tag-options-menu").is_visible(),label
         assert not opts.evaluate("el=>el.classList.contains('g3-waving')"),label
         assert page.locator("#renametag").count()==1 and page.locator("#deletetag").count()==1,label
         opts.click()
         assert opts.get_attribute("aria-expanded")=="false" and page.locator("#tag-options-menu").is_hidden(),label
         page.mouse.move(0,0)
         cases+=1
        print("PASS G3 Library themes",build,motion,width,flush=True)
       assert not errors,(build,motion,errors)
       page.close()
    browser.close()
    print("PASS G3 approved Library actions: 48 contexts, fully opaque thinking wave, nonreversing plus, original paths, exact geometry and menu functionality",cases,flush=True)
    assert cases==48
