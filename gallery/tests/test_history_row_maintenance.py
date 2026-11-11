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

    # A native scrolling architecture must not inject delayed scrollTop writes.
    assert 'handoffWheel' not in source and 'pendingWheelTimer' not in source
    assert history.evaluate('(e)=>getComputedStyle(e).overflowY')=='clip'
    assert history.locator('.wh-episodes-inner').evaluate('(e)=>getComputedStyle(e).overflowY')=='clip'
    assert inner.evaluate('(e)=>getComputedStyle(e).overscrollBehaviorY')=='auto'

    # Multiple wheel events in one gesture must chain continuously, without
    # a pause for the episode's fading overlay scrollbar or any double-scroll.
    for direction in (1,-1):
        inner.evaluate('(e,d)=>e.scrollTop=d>0?e.scrollHeight:0',direction)
        outer.evaluate('(e,d)=>e.scrollTop=d>0?180:460',direction)
        inner.scroll_into_view_if_needed()
        before=outer.evaluate('(e)=>e.scrollTop')
        rect=inner.bounding_box()
        page.mouse.move(rect['x']+rect['width']/2,rect['y']+rect['height']/2)
        for _ in range(4):
            page.mouse.wheel(0,direction*70)
            page.wait_for_timeout(18)
        page.wait_for_timeout(130)
        travelled=outer.evaluate('(e)=>e.scrollTop')-before
        assert abs(travelled-direction*280)<20,('Native continuous wheel',direction,travelled)

    # A wheel tick that finishes the last bit of inner scrolling may be
    # consumed by the inner viewport. The next tick must chain immediately
    # without an application-specific handoff timer.
    inner.evaluate('(e)=>e.scrollTop=e.scrollHeight-e.clientHeight-25')
    outer.evaluate('(e)=>e.scrollTop=500')
    inner.scroll_into_view_if_needed()
    before=outer.evaluate('(e)=>e.scrollTop')
    rect=inner.bounding_box()
    page.mouse.move(rect['x']+rect['width']/2,rect['y']+rect['height']/2)
    page.mouse.wheel(0,150)
    page.wait_for_timeout(24)
    page.mouse.wheel(0,70)
    page.wait_for_timeout(135)
    assert outer.evaluate('(e)=>e.scrollTop')>before+50,'No native chain after episode-list boundary'
    assert not errors,errors
    browser.close()
print('History row and hidden transfer regression tests passed')
