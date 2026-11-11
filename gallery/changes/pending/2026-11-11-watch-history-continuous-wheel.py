#!/usr/bin/env python3
"""Correct Watch History continuous wheel/trackpad handoff without interrupting native scrolling."""
from pathlib import Path
import hashlib

p=Path("gallery/Gallery-current.html")
before=p.read_bytes()
assert len(before)==6951376 and hashlib.sha256(before).hexdigest()=="3373d11f52f4f2b76be892fc891adc0597a4b41a7d5437259646182b374a333f", "STOP: GitHub HTML baseline mismatch"
s=before.decode("utf-8")
old=""" /* Some wheel/trackpad gestures remain latched to the nested episode list
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
 };"""
new=""" /* Preserve native wheel/trackpad momentum while handing off at episode
    boundaries. Never cancel the browser's wheel default; only fill missing
    movement after it has tried to scroll the parent. This also works for
    non-cancelable events in a continuous wheel gesture. */
 let pendingWheel=null,pendingWheelTimer=0;
 const handoffWheel=e=>{
  if(Math.abs(e.deltaY)<=Math.abs(e.deltaX)||currentScrollSurface()!==workspace)return;
  const delta=e.deltaY*(e.deltaMode===1?16:e.deltaMode===2?area.clientHeight:1);
  if(!delta)return;
  const max=Math.max(0,area.scrollHeight-area.clientHeight);
  const top=Math.max(0,Math.min(max,area.scrollTop));
  const available=delta>0?max-top:top;
  if(Math.abs(delta)<=available+.5&&!pendingWheel)return;
  if(pendingWheel&&Math.sign(pendingWheel.delta)!==Math.sign(delta)){
   clearTimeout(pendingWheelTimer);
   pendingWheel=null;
  }
  if(!pendingWheel){
   pendingWheel={delta:0,inner:area.scrollTop,outer:workspace.scrollTop};
   pendingWheelTimer=setTimeout(()=>{
    const wheel=pendingWheel;pendingWheel=null;pendingWheelTimer=0;
    if(!wheel||!area.isConnected||currentScrollSurface()!==workspace)return;
    const outerMoved=workspace.scrollTop-wheel.outer;
    if(outerMoved*wheel.delta>.5)return; // browser handled chaining natively
    const innerMoved=area.scrollTop-wheel.inner;
    const leftover=wheel.delta-innerMoved;
    if(leftover*wheel.delta>.5){
     workspace.scrollTop+=leftover;
     signalUserScroll();
    }
   },36);
  }
  pendingWheel.delta+=delta;
 };"""
assert s.count(old)==1, "STOP: expected unique wheel handler"
s=s.replace(old,new)
old_cleanup="return {area,update,destroy(){clearTimeout(timer);area.removeEventListener('wheel',intentScroll);"
new_cleanup="return {area,update,destroy(){clearTimeout(timer);if(pendingWheelTimer)clearTimeout(pendingWheelTimer);pendingWheel=null;area.removeEventListener('wheel',intentScroll);"
assert s.count(old_cleanup)==1,"STOP: expected unique scroller cleanup"
s=s.replace(old_cleanup,new_cleanup)
out=s.encode("utf-8")
assert len(out)==6952163 and hashlib.sha256(out).hexdigest()=="c5e22d522b1d75840bc87f92f58e7d5d9bbef4f1125c7a26792c5d31b92a7604","STOP: unexpected output digest"
p.write_bytes(out)

# Replace the earlier synchronous/manual-scroll probes with a regression that
# validates native, async-fallback and continuous noncancelable wheel events.
t=Path("gallery/tests/test_history_row_maintenance.py")
test=t.read_text(encoding="utf-8")
start_marker="    # Explicit boundary transfer, including a wheel tick that overshoots the end."
end_marker="    assert not errors,errors"
assert test.count(start_marker)==1 and test.count(end_marker)==1,"STOP: history regression anchors changed"
start=test.index(start_marker)
end=test.index(end_marker,start)
replacement='''    # Native wheel must not double-scroll when the episode scrollbar is visible.
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
'''
test=test[:start]+replacement+test[end:]
t.write_text(test,encoding="utf-8")
print("Gallery wheel momentum refinement matches exact tested HTML; regression suite updated.")
