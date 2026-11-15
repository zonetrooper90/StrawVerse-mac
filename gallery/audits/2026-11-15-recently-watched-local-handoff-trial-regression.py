#!/usr/bin/env python3
"""Local handoff trial: fixed-edge pane, no cross-slide or outgoing pane."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
source=Path(sys.argv[1]).read_text(encoding="utf-8")
origin="https://gallery-local-handoff.invalid/"
themes=("ocean","twilight","ember","slate","glacier","verdant")
def stable(page):
    page.wait_for_function("()=>!document.querySelector('.wh-recent-row').getAnimations({subtree:true}).some(a=>a.playState==='running')",timeout=5000)
def arm(page):
    page.evaluate("""()=>{
      const probe={frames:[],done:false};
      window.__whLocalProbe=probe;
      const row=document.querySelector('.wh-recent-row');
      const items=[...row.querySelectorAll('.wh-recent-item:not(.is-preview-hidden)')];
      let start=null;
      const tick=t=>{
        if(window.__whLocalProbe!==probe)return;
        if(start===null)start=t;
        const active=items.find(e=>e.classList.contains('is-active'));
        const card=active?.querySelector('.wh-recent-card'),pane=active?.querySelector('.wh-recent-info');
        const box=e=>{const b=e.getBoundingClientRect();return [b.left,b.right,b.top,b.bottom]};
        const other=items.filter(e=>e!==active).map(e=>{
          const p=e.querySelector('.wh-recent-info'),s=getComputedStyle(p);
          return {opacity:Number(s.opacity),visibility:s.visibility,card:box(e.querySelector('.wh-recent-card'))};
        });
        const style=pane&&getComputedStyle(pane);
        probe.frames.push({t:t-start,active:items.indexOf(active),transfer:row.classList.contains('is-transferring'),
          side:active?.dataset.whSide,card:card&&box(card),pane:pane&&box(pane),opacity:style&&Number(style.opacity),
          transform:style&&style.transform,properties:style&&style.transitionProperty,
          delay:style&&style.transitionDelay,duration:style&&style.transitionDuration,
          other,history:box(row.querySelector('#wh-view-history'))});
        if(t-start>=1000){probe.done=true;return;}
        requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    }""")
def hit(page,i):
    return page.evaluate("""i=>{
      const cards=[...document.querySelectorAll('.wh-recent-item:not(.is-preview-hidden) .wh-recent-card')];
      const card=cards[i],r=card.getBoundingClientRect(),y=r.top+r.height/2;
      const hits=[];for(let x=Math.ceil(r.left+3);x<=Math.floor(r.right-3);x+=2)
        if(document.elementFromPoint(x,y)?.closest('.wh-recent-card')===card)hits.push(x);
      return hits.length?{x:hits[Math.floor(hits.length/2)],y}:null;
    }""",i)
def frames(page):
    page.wait_for_function("()=>window.__whLocalProbe.done",timeout=5000)
    return page.evaluate("()=>window.__whLocalProbe.frames")
def check(samples,history,expected=None,transfer=None):
    assert len(samples)>=3,samples
    for f in samples:
        assert all(abs(a-b)<=1.1 for a,b in zip(f['history'],history)),f
        # An outgoing pane may never move with its portrait or remain visible.
        assert all(o['opacity']==0 and o['visibility']=='hidden' for o in f['other']),f
        if f['active']<0:continue
        assert f['transform']=='none' and f['properties']=='opacity',f
        assert f['side'] in ('left','right'),f
        assert abs((f['pane'][0] if f['side']=='right' else f['pane'][1])-
                   (f['card'][1] if f['side']=='right' else f['card'][0]))<=1.1,f
        assert f['delay']==('0.3s' if f['transfer'] else '0.55s') and f['duration']=='0.14s',f
        if f['opacity']>.01:
            for o in f['other']:
                assert o['card'][1]<=f['pane'][0]+1.1 or o['card'][0]>=f['pane'][1]-1.1,f
    if expected is not None:
        chosen=[f for f in samples if f['active']==expected]
        assert len(chosen)>=3 and chosen[-1]['opacity']>=.99,(expected,chosen)
        assert all(f['transfer']==transfer for f in chosen),(expected,transfer,chosen)
        assert any(f['opacity']<.99 for f in chosen),chosen
        return chosen[-1]['side']
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True)
    for width in (1440,620):
      for motion in ('no-preference','reduce'):
        page=browser.new_page(viewport={'width':width,'height':900},reduced_motion=motion)
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.route(origin+"**",lambda route:route.fulfill(status=200,content_type="text/html",body=source))
        page.goto(origin+"#recently-watched-test",wait_until="domcontentloaded");page.wait_for_selector('#wh-view-history')
        page.wait_for_function("()=>document.querySelectorAll('.wh-recent-item:not(.is-preview-hidden)').length===Math.min(24,Math.floor((document.querySelector('.wh-recent-row').clientWidth-66)/76))")
        for theme in themes:
          page.evaluate("t=>document.body.dataset.theme=t",theme)
          page.mouse.move(2,2);stable(page)
          n=page.locator('.wh-recent-item:not(.is-preview-hidden)').count();assert n>=3
          history=page.evaluate("()=>{const b=document.querySelector('#wh-view-history').getBoundingClientRect();return [b.left,b.right,b.top,b.bottom]}")
          sequence=[0,n-1,n//2,0,n-1]
          sides=set()
          for k,i in enumerate(sequence):
            arm(page);p=hit(page,i);assert p,(i,k)
            page.mouse.move(p['x'],p['y'])
            if motion=='no-preference':
              page.wait_for_function("i=>[...document.querySelectorAll('.wh-recent-item:not(.is-preview-hidden)')][i].classList.contains('is-active')",arg=i,timeout=3000)
              sides.add(check(frames(page),history,i,k>0))
              stable(page)
            else:
              sample=frames(page);check(sample,history)
              assert all(f['active']==-1 for f in sample),sample
          if motion=='no-preference':assert sides=={'left','right'},sides
          arm(page);page.mouse.move(2,2);sample=frames(page);check(sample,history)
          assert sample[-1]['active']==-1 and not sample[-1]['transfer'],sample[-1]
          assert not errors,errors
          print('PASS fixed-edge pane handoff',width,motion,theme,flush=True)
        page.close()
    browser.close()
print('PASS local fixed-edge pane trial and no outgoing cross-slide',flush=True)
