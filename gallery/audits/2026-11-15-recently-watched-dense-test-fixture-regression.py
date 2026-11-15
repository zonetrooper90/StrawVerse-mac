#!/usr/bin/env python3
"""Dense Recently Watched fixture: opt-in, isolated history, full-width geometry."""
import math,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
source=Path(sys.argv[1]).read_text(encoding="utf-8")
origin="https://gallery-fixture.invalid/"
def snapshot(page):
    return page.evaluate("""()=>{
      const row=document.querySelector('.wh-recent-row'),r=row.getBoundingClientRect();
      const bounds=e=>{const b=e.getBoundingClientRect();return [b.left-r.left,b.right-r.left,b.top,b.height]};
      const items=[...row.querySelectorAll('.wh-recent-item')],visible=items.filter(e=>!e.classList.contains('is-preview-hidden'));
      const active=visible.find(e=>e.classList.contains('is-active'));
      return {width:row.clientWidth,total:items.length,items:visible.map(e=>bounds(e.querySelector('button'))),
        history:bounds(row.querySelector('#wh-view-history')),active:visible.indexOf(active),side:active?.dataset.whSide,
        panel:active?bounds(active.querySelector('.wh-recent-info')):null,scroll:row.scrollLeft,
        title:document.querySelector('.wh-recent-header').textContent,explore:document.querySelector('#sf-discover-explore').getBoundingClientRect().top};
    }""")
def stable(page):
    page.wait_for_function("()=>!document.querySelector('.wh-recent-row').getAnimations({subtree:true}).some(a=>a.playState==='running')",timeout=5000)
def near(a,b):return all(abs(x-y)<=1 for x,y in zip(a,b))
def packed(s):
    assert s['total']==24 and len(s['items'])==min(24,math.floor((s['width']-66)/76)),s
    assert s['width']-s['history'][1]<=1 and s['scroll']==0,s
    for i,b in enumerate(s['items']):
        assert abs(b[0]-i*76)<=1 and abs(b[1]-b[0]-66)<=1 and b[1]<=s['history'][0]-9,s
def open_fixture(page):
    page.goto(origin+"?test=1#recently-watched-test",wait_until="domcontentloaded")
    page.wait_for_selector('#wh-view-history')
    page.wait_for_function("()=>document.querySelectorAll('.wh-recent-item:not(.is-preview-hidden)').length===Math.min(24,Math.floor((document.querySelector('.wh-recent-row').clientWidth-66)/76))")
    assert page.evaluate("()=>whRecentTestMode&&!whStorageReadable&&whRecords.length===25&&new Set(whRecords.map(r=>r.group)).size===24")
    assert page.evaluate("()=>JSON.stringify(whRecoverRecords(whRecords))===JSON.stringify(whRecords)"),"Fixture records must satisfy normal validation"
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True)
    for width in (1440,1920):
      for motion in ('no-preference','reduce'):
        page=browser.new_page(viewport={'width':width,'height':900},reduced_motion=motion)
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.route(origin+"**",lambda route:route.fulfill(status=200,content_type="text/html",body=source))
        page.goto(origin,wait_until="domcontentloaded");page.wait_for_selector('#wh-view-history')
        assert page.evaluate("()=>!whRecentTestMode&&whRecords.length===9")
        saved=page.evaluate("""()=>{const raw=JSON.stringify([whSeed[0]]);localStorage.setItem(whStorageKey,raw);
          localStorage.setItem(whRecoveryKey,'original-recovery-marker');return raw}""")
        open_fixture(page)
        before=snapshot(page);packed(before);assert 'Test data' in before['title']
        assert len(before['items'])>8 and len(before['items'])<24,before
        for i in (0,len(before['items'])//2,len(before['items'])-1):
          cards=page.locator('.wh-recent-item:not(.is-preview-hidden) .wh-recent-card')
          cards.nth(i).hover()
          if motion=='reduce':
            page.wait_for_timeout(180);assert snapshot(page)['active']==-1
          else:
            page.wait_for_function("i=>[...document.querySelectorAll('.wh-recent-item:not(.is-preview-hidden)')][i].classList.contains('is-active')",arg=i)
            stable(page);after=snapshot(page)
            assert after['active']==i and near(after['items'][i],before['items'][i]) and near(after['history'],before['history']),after
            assert abs(after['explore']-before['explore'])<=1 and after['scroll']==0,after
            assert after['side']==('right' if i==0 else 'left') if i in (0,len(before['items'])-1) else after['side'] in ('left','right')
            assert any(not near(a,b) for a,b in zip(before['items'],after['items'])),after
            assert after['panel'][0]>=-1 and after['panel'][1]<=after['history'][0]-9,after
            for j,b in enumerate(after['items']):
                assert b[0]>=-1 and b[1]<=after['history'][0]-9 and abs(b[1]-b[0]-66)<=1,after
                if j:assert b[0]-after['items'][j-1][0]>=17,after
                if j!=i:assert b[1]<=after['panel'][0]+1 or b[0]>=after['panel'][1]-1,after
          page.mouse.move(2,2);page.wait_for_function("()=>!document.querySelector('.wh-recent-item.is-active')");stable(page)
          restored=snapshot(page);packed(restored);assert all(near(a,b) for a,b in zip(before['items'],restored['items']))
        # Explicit save attempts in fixture mode must not touch either storage key.
        page.evaluate("()=>{whRecords[0].episodes[0].manualStatus='never';whSave()}")
        assert page.evaluate("()=>[localStorage.getItem(whStorageKey),localStorage.getItem(whRecoveryKey)]")==[saved,'original-recovery-marker']
        page.goto(origin+"?normal=1",wait_until="domcontentloaded");page.wait_for_selector('#wh-view-history')
        assert page.evaluate("()=>!whRecentTestMode&&whRecords.length===1&&whRecords[0].id==='q2'")
        assert 'Test data' not in page.locator('.wh-recent-header').inner_text()
        assert page.evaluate("()=>[localStorage.getItem(whStorageKey),localStorage.getItem(whRecoveryKey)]")==[saved,'original-recovery-marker']
        assert not errors,errors
        print('PASS dense fixture',width,motion,len(before['items']),flush=True)
        page.close()
    browser.close()
print('PASS dense fixture isolation, packing, directional stacking and restoration',flush=True)
