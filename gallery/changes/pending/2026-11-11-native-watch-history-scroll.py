#!/usr/bin/env python3
"""Switch Watch History nested scrolling to browser-native wheel chaining.

Scope: remove Watch History's delayed manual wheel forwarding; make its two
clipping wrappers non-scroll containers with CSS overflow:clip. Keep the
approved 280ms expansion and custom fading scrollbar, and leave Downloads alone.
"""
from pathlib import Path
import hashlib

html=Path("gallery/Gallery-current.html")
original=html.read_bytes()
assert len(original)==6952163 and hashlib.sha256(original).hexdigest()=="c5e22d522b1d75840bc87f92f58e7d5d9bbef4f1125c7a26792c5d31b92a7604", "STOP: authoritative GitHub HTML baseline differs"
s=original.decode("utf-8")

def one(before,after):
    global s
    assert s.count(before)==1, f"STOP: expected one HTML source anchor: {before[:80]}"
    s=s.replace(before,after)

one(
    "#wh-root .wh-season{border:1px solid var(--line);border-radius:15px;background:var(--surface);overflow:hidden;",
    "#wh-root .wh-season{border:1px solid var(--line);border-radius:15px;background:var(--surface);overflow:clip;"
)
one(
    "#wh-root .wh-episodes-inner{min-height:0;overflow:hidden;",
    "#wh-root .wh-episodes-inner{min-height:0;overflow:clip;"
)

start=s.index(" /* Preserve native wheel/trackpad momentum while handing off at episode")
end=s.index(" const down=e=>",start)
s=s[:start]+" /* Native scroll chaining through clipped, non-scrollable wrappers; no wheel interception. */\n"+s[end:]
one("area.addEventListener('wheel',handoffWheel,{passive:false});","")
one("if(pendingWheelTimer)clearTimeout(pendingWheelTimer);pendingWheel=null;","")
one("area.removeEventListener('wheel',handoffWheel);","")
assert 'handoffWheel' not in s and 'pendingWheel' not in s, "STOP: legacy wheel code remains"
updated=s.encode("utf-8")
assert len(updated)==6950542 and hashlib.sha256(updated).hexdigest()=="6e1d57fc6a3e956adc032c57bdbf656d0a283e2db79779c3f07c2258c6f6b909", "STOP: patched HTML differs from locally tested trial"
html.write_bytes(updated)

tests=Path("gallery/tests/test_history_row_maintenance.py")
source=tests.read_text(encoding="utf-8")
old_start="    # Synthetic events have no native wheel default. These prove that the"
old_end="    assert not errors,errors"
assert source.count(old_start)==1 and source.count(old_end)==1, "STOP: regression insertion anchors changed"
a=source.index(old_start)
b=source.index(old_end,a)
native='''    # A native scrolling architecture must not inject delayed scrollTop writes.
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
'''
tests.write_text(source[:a]+native+source[b:],encoding="utf-8")
print("Verified native scroll-chaining HTML and updated real-wheel browser regressions.")
