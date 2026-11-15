#!/usr/bin/env python3
"""Mandatory Recently Watched directional stacking regression."""
import sys, math
from pathlib import Path
from playwright.sync_api import sync_playwright
source=Path(sys.argv[1]).read_text(encoding="utf-8")
themes=("ocean","twilight","ember","slate","glacier","verdant")
def snap(page):
    return page.evaluate("""()=>{
      const row=document.querySelector('.wh-recent-row'), r=row.getBoundingClientRect();
      const box=e=>{const b=e.getBoundingClientRect();return [b.left-r.left,b.right-r.left,b.top,b.height]};
      const all=[...row.querySelectorAll('.wh-recent-item')],items=all.filter(e=>!e.classList.contains('is-preview-hidden'));
      const active=items.find(e=>e.classList.contains('is-active'));
      return {width:row.clientWidth,total:all.length,items:items.map(e=>box(e.querySelector('button'))),
        ids:items.map(e=>e.querySelector('button').dataset.whRecent),active:items.indexOf(active),side:active?.dataset.whSide,
        info:active?box(active.querySelector('.wh-recent-info')):null,
        opacity:active?Number(getComputedStyle(active.querySelector('.wh-recent-info')).opacity):0,
        history:box(row.querySelector('#wh-view-history')),explore:document.querySelector('#sf-discover-explore').getBoundingClientRect().top,
        height:r.height,scroll:row.scrollLeft};
    }""")
def same(a,b,tol=1):return all(abs(x-y)<=tol for x,y in zip(a,b))
def packed(s):
    assert len(s['items'])==min(s['total'],max(0,math.floor((s['width']-66)/76))),s
    assert abs(s['history'][1]-s['width'])<=1 and s['height']==96 and s['scroll']==0,s
    for i,b in enumerate(s['items']):
        assert abs(b[0]-i*76)<=1 and abs(b[1]-b[0]-66)<=1 and b[1]<=s['history'][0]-9,s
def stable(page):
    page.wait_for_function("()=>!document.querySelector('.wh-recent-row').getAnimations({subtree:true}).some(a=>a.playState==='running')",timeout=5000)
def clear(page):
    page.mouse.move(2,2);page.wait_for_function("()=>!document.querySelector('.wh-recent-item.is-active')");stable(page)
def check_open(before,after,i):
    assert after['active']==i and after['opacity']>=.99 and same(before['items'][i],after['items'][i]),(before,after)
    assert same(before['history'],after['history']) and abs(before['explore']-after['explore'])<=1,(before,after)
    assert before['ids']==after['ids'] and after['height']==96 and after['scroll']==0,after
    info=after['info'];assert info[1]-info[0]>=55 and info[0]>=-1 and info[1]<=after['history'][0]-9,after
    for j,b in enumerate(after['items']):
        assert b[0]>=-1 and b[1]<=after['history'][0]-9 and abs(b[1]-b[0]-66)<=1,after
        if j:assert b[0]-after['items'][j-1][0]>=17,after
        if j!=i:assert b[1]<=info[0]+1 or b[0]>=info[1]-1,after
    assert abs((info[0] if after['side']=='right' else info[1])-(after['items'][i][1] if after['side']=='right' else after['items'][i][0]))<=1,after
def card(page,i):return page.locator('.wh-recent-item:not(.is-preview-hidden) .wh-recent-card').nth(i)
def hover_card(page,i):
    card(page,i).hover()
    page.wait_for_function("i=>[...document.querySelectorAll('.wh-recent-item:not(.is-preview-hidden)')][i].classList.contains('is-active')",arg=i)
    stable(page)
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True)
    for width in (1440,920,620,420):
      for reduced in ('no-preference','reduce'):
        page=browser.new_page(viewport={'width':width,'height':850},reduced_motion=reduced)
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.set_content(source,wait_until='domcontentloaded');page.wait_for_selector('#wh-view-history');page.wait_for_timeout(150)
        for theme in themes:
          page.evaluate("t=>document.body.dataset.theme=t",theme)
          clear(page);before=snap(page);packed(before);n=len(before['items'])
          for i in sorted(set([0,n-1,n//2])) if n else []:
            req=lambda k:76+(k-1)*18 if k else 0
            x=before['items'][i][0];limit=before['width']-142
            left=x-req(i);right=limit-x-req(n-i-1);cap=max(left,right)
            if reduced=='reduce' or cap<55:
              card(page,i).hover();page.wait_for_timeout(180)
              assert snap(page)['active']==-1 and snap(page)['items']==before['items'],(width,reduced,i,snap(page))
            else:
              hover_card(page,i);after=snap(page);check_open(before,after,i)
              assert after['side']==('right' if right>=left else 'left'),after
            clear(page);rest=snap(page);packed(rest);assert rest['items']==before['items'] and same(rest['history'],before['history']),rest
          assert not errors,errors
          print('PASS recent stack',width,reduced,theme,n,flush=True)
        if width==920 and reduced=='no-preference' and len(snap(page)['items'])>=3:
          hover_card(page,0);page.emulate_media(reduced_motion='reduce')
          page.wait_for_function("()=>!document.querySelector('.wh-recent-item.is-active')");packed(snap(page))
          page.emulate_media(reduced_motion='no-preference');clear(page);hover_card(page,0)
          page.locator('#search').click();page.wait_for_function("()=>searchOpen&&!document.querySelector('.wh-recent-item.is-active')")
          page.locator('#header-search-input').press('Escape');page.wait_for_function("()=>!searchOpen");page.wait_for_timeout(500);packed(snap(page))
        assert not errors,errors
        page.close()
    page=browser.new_page(viewport={'width':620,'height':850},has_touch=True,reduced_motion='no-preference')
    page.set_content(source,wait_until='domcontentloaded');page.wait_for_selector('#wh-view-history');page.wait_for_timeout(150)
    before=snap(page);packed(before)
    if before['items']:
      card(page,0).dispatch_event('pointermove',{'pointerType':'touch','isPrimary':True})
      page.wait_for_timeout(180);assert snap(page)['active']==-1 and snap(page)['items']==before['items']
    page.close();browser.close()
print('PASS Recently Watched directional stack and reduced-motion/touch policy',flush=True)
