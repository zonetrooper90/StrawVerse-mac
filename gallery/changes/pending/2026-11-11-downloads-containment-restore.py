#!/usr/bin/env python3
"""Restore the original, user-approved Downloads episode scroll containment.

Change only Downloads' single CSS declaration. Watch History's latest native
scroll trial, its animations, scrollbar and interactions are preserved as-is.
"""
from pathlib import Path
import hashlib

html=Path("gallery/Gallery-current.html")
before=html.read_bytes()
assert len(before)==6950542 and hashlib.sha256(before).hexdigest()=="6e1d57fc6a3e956adc032c57bdbf656d0a283e2db79779c3f07c2258c6f6b909", "STOP: GitHub HTML differs from latest verified checkpoint"
text=before.decode("utf-8")
old="""body[data-theme] .sf-dl-list .sf-dl-viewport {
  max-height:384px;
  overflow-y:auto;overflow-x:hidden;
  overscroll-behavior-x:contain;overscroll-behavior-y:auto;
  background:transparent;"""
new="""body[data-theme] .sf-dl-list .sf-dl-viewport {
  max-height:384px;
  overflow-y:auto;overflow-x:hidden;
  overscroll-behavior:contain;
  background:transparent;"""
assert text.count(old)==1, "STOP: Downloads scroll declaration changed"
text=text.replace(old,new)
assert text.count("#wh-root .wh-episode-scroll{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));grid-auto-rows:42px;max-height:252px;overflow-y:auto;overflow-x:hidden;overscroll-behavior-x:contain;overscroll-behavior-y:auto;")==1, "STOP: Watch History scroller changed"
after=text.encode("utf-8")
assert before!=after and after.count(b"overscroll-behavior:contain;")==before.count(b"overscroll-behavior:contain;")+1
html.write_bytes(after)
print("Restored exactly one Downloads CSS declaration:",len(after),hashlib.sha256(after).hexdigest())

tests=Path("gallery/tests/test_history_row_maintenance.py")
t=tests.read_text(encoding="utf-8")
anchor="""    assert_episode_scroll_chains(dl.locator('.sf-dl-viewport'),page.locator('.tab-page[data-tab-page="downloads"]'),'Downloads')"""
assert t.count(anchor)==1, "STOP: Downloads regression anchor changed"
replacement='''    # Downloads deliberately retains its original scroll containment.
    # Wheel motion should scroll within its episode viewport without chaining
    # to the parent when the episode viewport reaches the bottom.
    dl_inner=dl.locator('.sf-dl-viewport')
    dl_outer=page.locator('.tab-page[data-tab-page="downloads"]')
    assert dl_inner.evaluate('(e)=>getComputedStyle(e).overscrollBehaviorY')=='contain'
    dl_inner.scroll_into_view_if_needed()
    assert dl_inner.evaluate('(e)=>e.scrollHeight-e.clientHeight')>0
    dl_inner.evaluate('(e)=>e.scrollTop=0')
    rect=dl_inner.bounding_box()
    page.mouse.move(rect['x']+rect['width']/2,rect['y']+rect['height']/2)
    page.mouse.wheel(0,110)
    page.wait_for_timeout(180)
    assert dl_inner.evaluate('(e)=>e.scrollTop')>30,'Downloads inner scrolling stopped working'
    dl_inner.evaluate('(e)=>e.scrollTop=e.scrollHeight')
    dl_outer.evaluate('(e)=>e.scrollTop=100')
    dl_inner.scroll_into_view_if_needed()
    before_dl=dl_outer.evaluate('(e)=>e.scrollTop')
    rect=dl_inner.bounding_box()
    page.mouse.move(rect['x']+rect['width']/2,rect['y']+rect['height']/2)
    page.mouse.wheel(0,110)
    page.wait_for_timeout(180)
    after_dl=dl_outer.evaluate('(e)=>e.scrollTop')
    assert abs(after_dl-before_dl)<3,('Downloads original scroll containment',before_dl,after_dl)'''
t=t.replace(anchor,replacement)
assert t.count("assert_episode_scroll_chains(history.locator('.wh-episode-scroll'),page.locator('.workspace'),'Watch History')")==1
tests.write_text(t,encoding="utf-8")
print("Downloads scroll regression updated; Watch History regression left untouched.")
