#!/usr/bin/env python3
"""Global History preserves real pre-hide primary scroll, nested Downloads and Settings."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
source=Path(sys.argv[1]).read_text(encoding="utf-8")
origin="https://gallery-history-scroll.invalid/"
themes=("ocean","twilight","ember","slate","glacier","verdant")
def settled(page):
    page.wait_for_function("()=>!galleryStageTransition&&!galleryStageFadeInProgress&&!galleryStagePending&&!tabTrackAnimation",timeout=8000)
def snap(page):
    return page.evaluate("""()=>({top:tabPages.downloads.scrollTop,max:tabPages.downloads.scrollHeight-tabPages.downloads.clientHeight,
      inner:tabPages.downloads.querySelector('[data-scroll-group="demo:quints"]').scrollTop,
      innerMax:tabPages.downloads.querySelector('[data-scroll-group="demo:quints"]').scrollHeight-tabPages.downloads.querySelector('[data-scroll-group="demo:quints"]').clientHeight,
      expanded:[...downloadDemo.expanded],filter:state.downloadStatus})""")
def verify(page,before):
    after=snap(page)
    assert abs(after['top']-before['top'])<=1,(before,after)
    assert abs(after['inner']-before['inner'])<=1,(before,after)
    assert after['expanded']==before['expanded'] and after['filter']==before['filter'],(before,after)
    assert page.locator('[data-download-toggle="demo:quints"]').get_attribute('aria-expanded')=='true'
    assert page.evaluate("()=>state.view==='downloads'&&!whOpen&&!tabPagesViewport.hidden")
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True)
    for width in (1440,420):
      for motion in ('no-preference','reduce'):
        for theme in themes:
          page=browser.new_page(viewport={'width':width,'height':900},reduced_motion=motion)
          errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
          page.route(origin+"**",lambda route:route.fulfill(status=200,content_type="text/html",body=source))
          page.goto(origin,wait_until="domcontentloaded")
          page.evaluate("t=>{state.theme=t;document.body.dataset.theme=t}",theme)
          page.locator('#nav-downloads').click();settled(page)
          page.locator('[data-download-toggle="demo:quints"]').click()
          page.wait_for_timeout(350 if motion=='no-preference' else 30)
          page.evaluate("""()=>{const p=tabPages.downloads,inner=p.querySelector('[data-scroll-group="demo:quints"]');
            inner.scrollTop=inner.scrollHeight; p.scrollTop=p.scrollHeight;}""")
          before=snap(page)
          assert before['top']>0 and before['inner']>0,before
          # Test exact capture from visible primary layout before the larger History viewport.
          page.locator('#header-watch-history').click();settled(page)
          assert page.evaluate("()=>whOpen&&whParentView==='downloads'&&!!whOriginTabs")
          saved=page.evaluate("()=>({top:whOriginTabs.tops.get('downloads'),inner:whOriginTabs.downloads.get('demo:quints')})")
          assert saved=={'top':before['top'],'inner':before['inner']},(before,saved)
          assert page.locator('#wh-root').is_visible()
          page.locator('#settings').click();settled(page)
          page.locator('#settings-back').click();settled(page)
          assert page.locator('#wh-root').is_visible()
          page.locator('[data-wh-exit]').click();settled(page)
          verify(page,before)
          # Revisit and use the global shortcut to close History; do not reuse stale positions.
          page.evaluate("""()=>{const p=tabPages.downloads,inner=p.querySelector('[data-scroll-group="demo:quints"]');
            inner.scrollTop=Math.floor(inner.scrollTop/2);p.scrollTop=Math.floor(p.scrollTop/2);}""")
          before=snap(page)
          page.locator('#header-watch-history').click();settled(page)
          page.locator('#header-watch-history').click();settled(page)
          verify(page,before)
          assert page.evaluate("()=>whOriginTabs===null")
          assert not errors,errors
          print('PASS global History Downloads outer and inner scroll',width,motion,theme,flush=True)
          page.close()
    browser.close()
