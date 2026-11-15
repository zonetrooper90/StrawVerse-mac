#!/usr/bin/env python3
"""Dense actual pointer transfers: no cumulative displacement or orphan gaps."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
source=Path(sys.argv[1]).read_text(encoding="utf-8")
origin="https://gallery-switch.invalid/"
themes=("ocean","twilight","ember","slate","glacier","verdant")
snapshot="""()=>{
 const row=document.querySelector('.wh-recent-row'),r=row.getBoundingClientRect();
 const items=[...row.querySelectorAll('.wh-recent-item:not(.is-preview-hidden)')],a=items.find(e=>e.classList.contains('is-active'));
 const box=e=>{const b=e.getBoundingClientRect();return [b.left-r.left,b.right-r.left,b.top,b.height]};
 return {width:row.clientWidth,left:r.left,top:r.top,items:items.map(e=>box(e.querySelector('button'))),
  ids:items.map(e=>e.querySelector('button').dataset.whRecent),labels:items.map(e=>Number(getComputedStyle(e.querySelector('.wh-recent-card-label')).opacity)),
  active:items.indexOf(a),side:a?.dataset.whSide,panel:a?box(a.querySelector('.wh-recent-info')):null,
  opacity:a?Number(getComputedStyle(a.querySelector('.wh-recent-info')).opacity):0,history:box(row.querySelector('#wh-view-history')),
  explore:document.querySelector('#sf-discover-explore').getBoundingClientRect().top,scroll:row.scrollLeft,height:r.height};
}"""
def snap(page):return page.evaluate(snapshot)
def near(a,b,tol=1.1):return all(abs(x-y)<=tol for x,y in zip(a,b))
def stable(page):
    page.wait_for_function("()=>!document.querySelector('.wh-recent-row').getAnimations({subtree:true}).some(a=>a.playState==='running')",timeout=5000)
def exposed_point(page,i):
    # Select a real hit-testable pixel of the requested portrait, not a synthetic
    # event or locator click on an occluded center. Use the actual stacked DOM.
    return page.evaluate("""i=>{
      const row=document.querySelector('.wh-recent-row');
      const cards=[...row.querySelectorAll('.wh-recent-item:not(.is-preview-hidden) .wh-recent-card')];
      const card=cards[i],r=card.getBoundingClientRect(),y=r.top+r.height/2;
      const hits=[];for(let x=Math.ceil(r.left+3);x<=Math.floor(r.right-3);x+=2)
        if(document.elementFromPoint(x,y)?.closest('.wh-recent-card')===card)hits.push(x);
      return hits.length?{x:hits[Math.floor(hits.length/2)],y,left:r.left}:null;
    }""",i)
def assert_layout(base,s,i,anchor):
    assert s['active']==i and s['ids']==base['ids'] and s['opacity']>=.99,s
    assert abs(s['items'][i][0]+s['left']-anchor)<=1.1,(i,anchor,s)
    assert near(s['history'],base['history']) and abs(s['explore']-base['explore'])<=1 and s['height']==96 and s['scroll']==0,s
    info=s['panel'];assert info[1]-info[0]>=55 and info[0]>=-1 and info[1]<=s['history'][0]-9,s
    assert abs((info[0] if s['side']=='right' else info[1])-(s['items'][i][1] if s['side']=='right' else s['items'][i][0]))<=1.1,s
    for j,b in enumerate(s['items']):
        assert b[0]>=-1 and b[1]<=s['history'][0]-9 and abs(b[1]-b[0]-66)<=1,s
        if j!=i:assert b[1]<=info[0]+1 or b[0]>=info[1]-1,s
        if j:
            gap=b[0]-s['items'][j-1][0]
            panel_gap=(s['side']=='right' and j==i+1) or (s['side']=='left' and j==i)
            if panel_gap:assert abs(gap-76-(info[1]-info[0]))<=1.1,(j,gap,s)
            else:assert 17<=gap<=77,(j,gap,s)
        overlap=(j>0 and b[0]-s['items'][j-1][0]<65.5) or (j+1<len(s['items']) and s['items'][j+1][0]-b[0]<65.5)
        assert s['labels'][j]==(0 if overlap and j!=i else 1),(j,s)
    # The packed fixture must not lose a whole card slot of usable end space.
    assert s['items'][0][0]<=base['items'][0][0]+76 and s['items'][-1][0]>=base['items'][-1][0]-76,s
def arm_pointer_probe(page,i):
    # Observe the *real* pointer event in capture phase before the row handler.
    # A bounding rect sampled in a preceding Playwright RPC can be several pixels
    # stale while the previous transition is running.
    page.evaluate("""i=>{
      const probe={expected:i,event:null,frames:[],done:false};
      window.__whPointerProbe=probe;
      document.addEventListener('pointermove',event=>{
        const cards=[...document.querySelectorAll('.wh-recent-item:not(.is-preview-hidden) .wh-recent-card')];
        const card=event.target.closest('.wh-recent-card'),index=cards.indexOf(card);
        probe.event={index,x:event.clientX,y:event.clientY,left:card?.getBoundingClientRect().left};
        if(index!==i)return;
        const item=card.closest('.wh-recent-item');
        let start=null;
        const tick=t=>{
          if(window.__whPointerProbe!==probe){probe.done=true;return;}
          if(item.classList.contains('is-active')){
            if(start===null)start=t;
            probe.frames.push({t:t-start,left:card.getBoundingClientRect().left,
              transition:getComputedStyle(item).transitionProperty});
            if(t-start>=700){probe.done=true;return;}
          }else if(start!==null){probe.done=true;return;}
          requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
      },{capture:true,once:true});
    }""",i)
def switch(page,base,i,settle=True):
    arm_pointer_probe(page,i)
    point=exposed_point(page,i);assert point is not None,('cover must remain hit-testable',i,snap(page))
    page.mouse.move(point['x'],point['y'])
    page.wait_for_function("()=>window.__whPointerProbe.event!==null",timeout=3000)
    event=page.evaluate("()=>window.__whPointerProbe.event")
    assert event['index']==i and event['left'] is not None,('real pointer target',i,point,event)
    page.wait_for_function("i=>[...document.querySelectorAll('.wh-recent-item:not(.is-preview-hidden)')][i].classList.contains('is-active')",arg=i,timeout=3000)
    # Even a switch interrupted before settling must pin the selected portrait.
    page.wait_for_function("()=>window.__whPointerProbe.frames.length>=2",timeout=3000)
    frames=page.evaluate("()=>window.__whPointerProbe.frames")
    assert all(abs(f['left']-event['left'])<=1.1 and f['transition']=='none' for f in frames),(i,event,frames)
    if settle:
        stable(page);page.wait_for_function("()=>window.__whPointerProbe.done",timeout=3000)
        frames=page.evaluate("()=>window.__whPointerProbe.frames")
        assert len(frames)>=3 and frames[-1]['t']>=700,(i,event,frames)
        assert all(abs(f['left']-event['left'])<=1.1 and f['transition']=='none' for f in frames),(i,event,frames)
        assert_layout(base,snap(page),i,event['left'])
        # A stationary pointer must not trigger another selection after reflow.
        page.wait_for_timeout(100);assert snap(page)['active']==i
    return event
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
          page.mouse.move(2,2);stable(page);base=snap(page);n=len(base['items'])
          assert n>=3 and base['active']==-1 and all(x==1 for x in base['labels']),base
          sequence=[0,n//3,2*n//3,n-1,n-2,n//2,1,0,n-1,n//2]
          sequence=[i for j,i in enumerate(sequence) if not j or i!=sequence[j-1]]
          if motion=='reduce':
            for i in sequence:
              p=exposed_point(page,i);assert p;page.mouse.move(p['x'],p['y']);page.wait_for_timeout(140)
              s=snap(page);assert s['active']==-1 and s['items']==base['items'] and s['labels']==base['labels'],s
          else:
            for i in sequence:switch(page,base,i)
            # Reverse while the previous transition is still in flight.
            # Use visible hit targets and sample the anchor at that instant.
            switch(page,base,0,False);page.wait_for_timeout(100)
            point=switch(page,base,n-1,False);page.wait_for_timeout(100)
            point=switch(page,base,n//2,True)
            page.mouse.move(2,2);stable(page);rest=snap(page)
            assert rest['active']==-1 and all(near(a,b) for a,b in zip(rest['items'],base['items'])) and all(x==1 for x in rest['labels']),rest
          assert not errors,errors
          print('PASS coordinated continuous hover',width,motion,theme,n,len(sequence),flush=True)
        page.close()
    browser.close()
print('PASS continuous Recently Watched pointer transfer, reversals, labels and fixed frame',flush=True)
