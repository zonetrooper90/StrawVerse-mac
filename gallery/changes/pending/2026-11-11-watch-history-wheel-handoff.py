#!/usr/bin/env python3
"""Correct Watch History wheel handoff when a browser latches nested scrolling.

Only affects the nested Watch History episode scroller at its vertical boundary;
Downloads and native scrolling within either list are left untouched.
"""
from pathlib import Path
import hashlib

p = Path('gallery/Gallery-current.html')
before = p.read_bytes()
assert len(before) == 6950451 and hashlib.sha256(before).hexdigest() == '878e61a27bb36d77481ad0bc4a4fe2e2e3de2c050b1b4f97a9f48a7b63a250b5', 'STOP: GitHub working HTML does not match its approved starting checkpoint'
s = before.decode('utf-8')

def one(old, new):
    global s
    assert s.count(old) == 1, f'STOP: expected exactly one HTML replacement anchor: {old[:90]!r}'
    s = s.replace(old, new)

one(
    " const onKey=e=>{if(['ArrowDown','ArrowUp','PageDown','PageUp','Home','End',' '].includes(e.key))intentScroll();};\n const down=e=>",
    """ const onKey=e=>{if(['ArrowDown','ArrowUp','PageDown','PageUp','Home','End',' '].includes(e.key))intentScroll();};
 /* Some wheel/trackpad gestures remain latched to the nested episode list
    at a boundary even though CSS permits scroll chaining. Transfer only the
    unconsumed vertical delta to Watch History's existing workspace scroller. */
 const handoffWheel=e=>{
  if(!e.cancelable||Math.abs(e.deltaY)<=Math.abs(e.deltaX)||currentScrollSurface()!==workspace)return;
  const delta=e.deltaY*(e.deltaMode===1?16:e.deltaMode===2?area.clientHeight:1);
  if(!delta)return;
  const max=Math.max(0,area.scrollHeight-area.clientHeight);
  const top=Math.max(0,Math.min(max,area.scrollTop));
  const available=delta>0?max-top:top;
  if(Math.abs(delta)<=available+.5)return;
  e.preventDefault();
  area.scrollTop=Math.max(0,Math.min(max,top+delta));
  workspace.scrollTop+=delta-Math.sign(delta)*available;
  signalUserScroll();
 };
 const down=e=>"""
)
one(
    " area.addEventListener('wheel',intentScroll,{passive:true});area.addEventListener('touchmove',intentScroll,{passive:true});area.addEventListener('scroll',onScroll,{passive:true});area.addEventListener('keydown',onKey);",
    " area.addEventListener('wheel',intentScroll,{passive:true});area.addEventListener('wheel',handoffWheel,{passive:false});area.addEventListener('touchmove',intentScroll,{passive:true});area.addEventListener('scroll',onScroll,{passive:true});area.addEventListener('keydown',onKey);"
)
one(
    "area.removeEventListener('wheel',intentScroll);area.removeEventListener('touchmove',intentScroll);",
    "area.removeEventListener('wheel',intentScroll);area.removeEventListener('wheel',handoffWheel);area.removeEventListener('touchmove',intentScroll);"
)
updated = s.encode('utf-8')
assert len(updated) == 6951376 and hashlib.sha256(updated).hexdigest() == '3373d11f52f4f2b76be892fc891adc0597a4b41a7d5437259646182b374a333f', 'STOP: patched HTML output differs from locally tested version'
p.write_bytes(updated)

# The prior real wheel test alone could pass under Chromium even when a real
# user encountered boundary latching. Test the explicit fallback with a
# cancellable WheelEvent; synthetic events have no native default scrolling.
tests = Path('gallery/tests/test_history_row_maintenance.py')
t = tests.read_text(encoding='utf-8')
anchor = "    assert_episode_scroll_chains(history.locator('.wh-episode-scroll'),page.locator('.workspace'),'Watch History')\n    assert not errors,errors"
assert t.count(anchor)==1, 'STOP: existing Watch History browser regression anchor changed'
addition = '''    # Explicit boundary transfer, including a wheel tick that overshoots the end.
    # A dispatched synthetic WheelEvent cannot scroll natively, so this proves
    # the Watch History handler forwards unconsumed delta to its parent.
    probes=page.evaluate("""() => {
      const inner=document.querySelectorAll('.wh-episode-scroll')[1];
      const outer=document.querySelector('.workspace');
      function check(innerTop,outerTop,dy,dx=0,mode=0){
        const max=inner.scrollHeight-inner.clientHeight;
        inner.scrollTop=innerTop==='end'?max:innerTop;
        outer.scrollTop=outerTop;
        const start={inner:inner.scrollTop,outer:outer.scrollTop,max};
        const event=new WheelEvent('wheel',{bubbles:true,cancelable:true,deltaX:dx,deltaY:dy,deltaMode:mode});
        inner.dispatchEvent(event);
        return {start,end:{inner:inner.scrollTop,outer:outer.scrollTop},prevented:event.defaultPrevented};
      }
      return {
        down:check('end',100,180),
        up:check(0,370,-160),
        overshoot:check(inner.scrollHeight-inner.clientHeight-25,100,160),
        inside:check(150,100,80),
        horizontal:check('end',100,70,200)
      };
    }""")
    assert probes['down']['prevented'] and abs(probes['down']['end']['outer']-280)<=2,probes
    assert probes['up']['prevented'] and abs(probes['up']['end']['outer']-210)<=2,probes
    assert probes['overshoot']['prevented'] and abs(probes['overshoot']['end']['outer']-235)<=2,probes
    assert abs(probes['overshoot']['end']['inner']-probes['overshoot']['start']['max'])<=1,probes
    assert not probes['inside']['prevented'] and probes['inside']['end']['outer']==probes['inside']['start']['outer'],probes
    assert not probes['horizontal']['prevented'] and probes['horizontal']['end']['outer']==probes['horizontal']['start']['outer'],probes
'''
t = t.replace(anchor, "    assert_episode_scroll_chains(history.locator('.wh-episode-scroll'),page.locator('.workspace'),'Watch History')\n" + addition + "    assert not errors,errors")
tests.write_text(t,encoding='utf-8')
print('Watch History boundary handoff patched, exact HTML digest verified; stronger regression added.')
