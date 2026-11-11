#!/usr/bin/env python3
"""Regression tests for hidden transfer actions and Download-style Watch History rows."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

source=Path(sys.argv[1]).read_text(encoding='utf-8')
assert 'GALLERY_COLLECTION_TRANSFER_UI_ENABLED=false' in source
assert 'function showImport()' in source and 'function showShare()' in source
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True)
    page=browser.new_page(viewport={'width':1200,'height':850})
    errors=[]
    page.on('pageerror', lambda exc: errors.append(str(exc)))
    page.set_content(source, wait_until='domcontentloaded')
    page.wait_for_timeout(160)
    assert page.locator('#wh-view-history').count()==1
    page.locator('[data-view="library"]').first.click()
    page.wait_for_timeout(500)
    assert page.locator('#import').count()==0
    assert page.locator('#newtag').count()==1
    assert page.locator('#sharetag').count()==0
    page.locator('[data-tag="Comfort Picks"]').first.click()
    page.wait_for_timeout(120)
    assert page.locator('#sharetag').count()==0
    page.locator('[data-view="discover"]').first.click()
    page.wait_for_timeout(500)
    page.locator('#wh-view-history').click()
    page.wait_for_timeout(500)
    assert page.locator('#wh-root').count()==1
    first=page.locator('.wh-season').first
    assert first.locator('.wh-summary-hit').count()==1
    assert first.locator('.wh-episodes').count()==1
    assert first.locator('.wh-episodes-inner').get_attribute('inert') is not None
    page.evaluate('window.__historyPanel=document.querySelector(".wh-season .wh-episodes")')
    first.locator('.wh-summary-hit').click(position={'x':180,'y':50})
    page.wait_for_timeout(140)
    first=page.locator('.wh-season').first
    assert first.locator('.wh-episodes').count()==1
    assert first.locator('.wh-summary-hit').get_attribute('aria-expanded')=='true'
    assert first.locator('.wh-episodes-inner').get_attribute('inert') is None
    assert page.evaluate('window.__historyPanel===document.querySelector(".wh-season .wh-episodes")')
    opening_height=first.locator('.wh-episodes').evaluate('(el)=>el.getBoundingClientRect().height')
    page.wait_for_timeout(210)
    full_height=first.locator('.wh-episodes').evaluate('(el)=>el.getBoundingClientRect().height')
    assert 0 < opening_height < full_height, (opening_height,full_height)
    episode=first.locator('.wh-episode-row').first
    assert episode.count()==1 and episode.get_attribute('role') is None
    before=episode.get_attribute('aria-pressed')
    episode.locator('.wh-episode-number').click()
    assert episode.get_attribute('aria-pressed')!=before
    episode.focus()
    episode.press('Space')
    assert episode.get_attribute('aria-pressed')==before
    first.locator('.wh-summary-hit').click()
    page.wait_for_timeout(330)
    assert first.locator('.wh-episodes').evaluate('(el)=>el.getBoundingClientRect().height')==0
    assert first.locator('.wh-episodes-inner').get_attribute('inert') is not None
    first.locator('.wh-summary-hit').click()
    page.wait_for_timeout(330)
    assert page.evaluate('window.__historyPanel===document.querySelector(".wh-season .wh-episodes")')
    assert first.locator('.wh-anime-title').count()==1
    first.locator('.wh-anime-title').click()
    page.wait_for_timeout(470)
    assert page.locator('#detail-back').count()==1
    page.locator('#detail-back').click()
    page.wait_for_timeout(470)
    first=page.locator('.wh-season').first
    assert first.locator('.wh-episodes').count()==1
    n=page.locator('.wh-season').count()
    first.locator('.wh-trash').click()
    assert page.locator('.wh-season').count()==n-1
    page.locator('[data-wh-undo-all]').click()
    assert page.locator('.wh-season').count()==n
    page.locator('[data-wh-exit]').click()
    page.wait_for_timeout(450)
    page.locator('[data-view="downloads"]').first.click()
    page.wait_for_timeout(500)
    assert page.locator('[data-download-toggle]').count()>0
    # Wheel/trackpad input at an episode boundary must scroll the parent page.
    page.set_viewport_size({'width':1100,'height':750})
    def assert_episode_scroll_chains(inner,outer,label):
        assert inner.evaluate('(e)=>getComputedStyle(e).overscrollBehaviorY')=='auto',label
        inner.scroll_into_view_if_needed()
        assert inner.evaluate('(e)=>e.scrollHeight-e.clientHeight')>0,label
        assert outer.evaluate('(e)=>e.scrollHeight-e.clientHeight')>180,label
        inner.evaluate('(e)=>e.scrollTop=e.scrollHeight')
        outer.evaluate('(e)=>e.scrollTop=0')
        inner.scroll_into_view_if_needed()
        before=outer.evaluate('(e)=>e.scrollTop')
        rect=inner.bounding_box()
        page.mouse.move(rect['x']+rect['width']/2,rect['y']+rect['height']/2)
        page.mouse.wheel(0,180)
        page.wait_for_timeout(250)
        after=outer.evaluate('(e)=>e.scrollTop')
        assert after>before+20,(label,'down',before,after)
        inner.evaluate('(e)=>e.scrollTop=0')
        outer.evaluate('(e)=>e.scrollTop=90')
        inner.scroll_into_view_if_needed()
        before=outer.evaluate('(e)=>e.scrollTop')
        rect=inner.bounding_box()
        page.mouse.move(rect['x']+rect['width']/2,rect['y']+rect['height']/2)
        page.mouse.wheel(0,-120)
        page.wait_for_timeout(250)
        after=outer.evaluate('(e)=>e.scrollTop')
        assert after<before-20,(label,'up',before,after)
    dl=page.locator('.sf-dl-card').first
    dl.locator('[data-download-toggle]').click()
    page.wait_for_timeout(330)
    assert_episode_scroll_chains(dl.locator('.sf-dl-viewport'),page.locator('.tab-page[data-tab-page="downloads"]'),'Downloads')
    page.locator('[data-view="discover"]').first.click()
    page.wait_for_timeout(400)
    page.locator('#wh-view-history').click()
    page.wait_for_timeout(400)
    history=page.locator('.wh-season').nth(1)
    history.locator('[data-wh-expand]').click()
    page.wait_for_timeout(330)
    assert_episode_scroll_chains(history.locator('.wh-episode-scroll'),page.locator('.workspace'),'Watch History')
    # Native wheel must not double-scroll when the episode scrollbar is visible.
    inner=history.locator('.wh-episode-scroll')
    outer=page.locator('.workspace')
    inner.scroll_into_view_if_needed()
    inner.evaluate('(e)=>e.scrollTop=e.scrollHeight')
    outer.evaluate('(e)=>e.scrollTop=180')
    rect=inner.bounding_box()
    page.mouse.move(rect['x']+rect['width']/2,rect['y']+rect['height']/2)
    page.mouse.wheel(0,80)
    page.wait_for_timeout(120)
    delta=outer.evaluate('(e)=>e.scrollTop')-180
    assert 55<=delta<=105,('Native wheel double-scroll or handoff failure',delta)

    # Synthetic events have no native wheel default. These prove that the
    # fallback handles continuous noncancelable events, reversed direction,
    # overshooting a boundary, and does not fight a real native parent scroll.
    probes=page.evaluate("""async () => {
      const inner=document.querySelectorAll('.wh-episode-scroll')[1];
      const outer=document.querySelector('.workspace');
      const sleep=()=>new Promise(resolve=>setTimeout(resolve,85));
      async function check(innerAt,outerAt,events,adjust={}){
        const max=inner.scrollHeight-inner.clientHeight;
        inner.scrollTop=innerAt==='end'?max:innerAt;
        outer.scrollTop=outerAt;
        const start={inner:inner.scrollTop,outer:outer.scrollTop};
        const prevented=[];
        for(const item of events){
          const ev=new WheelEvent('wheel',{bubbles:true,cancelable:item.cancelable,deltaY:item.y,deltaX:item.x||0});
          inner.dispatchEvent(ev);prevented.push(ev.defaultPrevented);
        }
        if(adjust.nativeInner)inner.scrollTop=max;
        if(adjust.nativeOuter)outer.scrollTop+=adjust.nativeOuter;
        await sleep();
        return {start,end:{inner:inner.scrollTop,outer:outer.scrollTop},prevented};
      }
      return {
        continuous:await check('end',150,[{y:40,cancelable:true},{y:45,cancelable:false},{y:35,cancelable:false}]),
        upward:await check(0,330,[{y:-35,cancelable:false},{y:-55,cancelable:false}]),
        native:await check('end',150,[{y:90,cancelable:true}],{nativeOuter:90}),
        overshoot:await check(inner.scrollHeight-inner.clientHeight-25,150,[{y:100,cancelable:false}],{nativeInner:true}),
        inside:await check(100,150,[{y:30,cancelable:true}]),
        horizontal:await check('end',150,[{y:30,x:130,cancelable:false}])
      };
    }""")
    assert abs(probes['continuous']['end']['outer']-270)<=2,probes
    assert abs(probes['upward']['end']['outer']-240)<=2,probes
    assert abs(probes['native']['end']['outer']-240)<=2,probes
    assert abs(probes['overshoot']['end']['outer']-225)<=2,probes
    assert abs(probes['overshoot']['end']['inner']-probes['overshoot']['start']['inner']-25)<=2,probes
    assert probes['inside']['end']['outer']==150,probes
    assert probes['horizontal']['end']['outer']==150,probes
    assert all(not any(x['prevented']) for x in probes.values()),probes
    assert not errors,errors
    browser.close()
print('History row and hidden transfer regression tests passed')
