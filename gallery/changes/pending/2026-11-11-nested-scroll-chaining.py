#!/usr/bin/env python3
"""Allow scrolling beyond nested episodes in both Watch History and Downloads.

Applied on GitHub's authoritative HTML by the controlled checkpoint publisher.
"""
from pathlib import Path
import hashlib

html=Path('gallery/Gallery-current.html')
original=html.read_bytes()
assert len(original)==6950393 and hashlib.sha256(original).hexdigest()=='c850b767a00c1749d56d52468e23c01d31afd27edc225f74b3ec9440b1db1717', 'STOP: GitHub baseline changed'
s=original.decode('utf-8')

def replace_one(before,after):
    global s
    assert s.count(before)==1, 'Unique CSS selector missing or changed: '+before[:75]
    s=s.replace(before,after)

replace_one(
    '#wh-root .wh-episode-scroll{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));grid-auto-rows:42px;max-height:252px;overflow-y:auto;overflow-x:hidden;overscroll-behavior:contain;scrollbar-gutter:auto;scrollbar-width:none;-ms-overflow-style:none}',
    '#wh-root .wh-episode-scroll{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));grid-auto-rows:42px;max-height:252px;overflow-y:auto;overflow-x:hidden;overscroll-behavior-x:contain;overscroll-behavior-y:auto;scrollbar-gutter:auto;scrollbar-width:none;-ms-overflow-style:none}'
)
replace_one(
    'body[data-theme] .sf-dl-list .sf-dl-viewport {\n  max-height:384px;\n  overflow-y:auto;overflow-x:hidden;\n  overscroll-behavior:contain;\n  background:transparent;',
    'body[data-theme] .sf-dl-list .sf-dl-viewport {\n  max-height:384px;\n  overflow-y:auto;overflow-x:hidden;\n  overscroll-behavior-x:contain;overscroll-behavior-y:auto;\n  background:transparent;'
)

updated=s.encode('utf-8')
assert len(updated)==6950451 and hashlib.sha256(updated).hexdigest()=='878e61a27bb36d77481ad0bc4a4fe2e2e3de2c050b1b4f97a9f48a7b63a250b5', 'STOP: unexpected HTML output'
html.write_bytes(updated)

# Extend the existing browser suite with actual wheel events at both boundaries.
tests=Path('gallery/tests/test_history_row_maintenance.py')
content=tests.read_text(encoding='utf-8')
marker="    assert page.locator('[data-download-toggle]').count()>0\n    assert not errors,errors"
assert content.count(marker)==1, 'STOP: regression insertion point changed'
addition='''    # Wheel/trackpad input at an episode boundary must scroll the parent page.
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
'''
content=content.replace(marker,"    assert page.locator('[data-download-toggle]').count()>0\n"+addition+"    assert not errors,errors")
tests.write_text(content,encoding='utf-8')
print('Verified scoped CSS change and both wheel-chaining browser tests installed.')
