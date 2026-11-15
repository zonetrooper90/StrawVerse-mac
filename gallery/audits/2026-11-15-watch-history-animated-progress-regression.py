#!/usr/bin/env python3
"""Actual History DOM, geometry, overlap, state changes, reversal and lifecycle."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
source=Path(sys.argv[1]).read_text(encoding="utf-8")
themes=("ocean","twilight","ember","slate","glacier","verdant")
snapshot="""() => {
 const row=document.querySelector('[data-wh-row="motion-test"]'), t=row.querySelector('.wh-progress');
 if(!t)return {complete:!!row.querySelector('.wh-completed')};
 const a=t.querySelector('.wh-progress-done'), b=t.querySelector('.wh-progress-rest'), s=t.querySelector('.wh-progress-solid'), e=t.querySelector('.wh-progress-end');
 const tr=t.getBoundingClientRect(), ar=a.getBoundingClientRect(), br=b.getBoundingClientRect();
 return {complete:false,width:tr.width,height:tr.height,started:ar.width,rest:br.width,gap:br.left-ar.right,done:+s.getAttribute('width'),end:+e.getAttribute('width'),
   endX:+e.getAttribute('x'),path:t.querySelector('.wh-progress-capsules').getAttribute('d'),cut:t.querySelector('.wh-progress-cut').getAttribute('d'),
   mask:e.getAttribute('mask'),color:getComputedStyle(s).fill,accent:getComputedStyle(t).getPropertyValue('--accent').trim(),
   same:t===window.__whTestTrack,summary:row.querySelector('.wh-summary')===window.__whTestSummary,
   panel:row.querySelector('.wh-episodes')===window.__whTestPanel,count:row.querySelector('.wh-progress-count').textContent};
}"""
def geom(s,w,p):
    assert not s["complete"],s
    u=s["width"]-5
    assert abs(s["gap"]-5)<.3 and abs(s["height"]-5)<.3,s
    assert abs(s["started"]-u*(w+p)/12)<.4 and abs(s["done"]-u*w/12)<.4,s
    assert abs(s["rest"]-u*(12-w-p)/12)<.4,s
    assert abs(s["end"]-min(8,u*p/12))<.4 and abs(s["endX"]+s["end"]-s["started"])<.4,s
    assert s["color"]!="none" and s["mask"].startswith("url("),s
def wait(page,motion):
    if motion=="no-preference":page.wait_for_timeout(350)
def reset(page,w,p):
    page.evaluate("""([w,p])=>{
      const r={...whSeedRecords()[0],id:'motion-test',episodes:Array.from({length:12},(_,i)=>({n:i+1,started:i<w+p,watched:i<w,progressSeconds:i<w+p?42:0,duration:1440,manualStatus:i<w?'watched':i<w+p?'partial':'never'})),latestEpisode:1};
      whRecords=[r];whExpanded=new Set([r.id]);whRender();
      const row=document.querySelector('[data-wh-row="motion-test"]');
      window.__whTestTrack=row.querySelector('.wh-progress');window.__whTestSummary=row.querySelector('.wh-summary');window.__whTestPanel=row.querySelector('.wh-episodes');
    }""",[w,p])
def click(page,n):
    # Actual delegated click without Playwright's stability wait during a reversal.
    page.evaluate("n=>document.querySelector('[data-wh-episode=\"motion-test:'+n+'\"]').click()",n)
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True)
    for width in (1440,620):
      for motion in ("no-preference","reduce"):
       page=browser.new_page(viewport={"width":width,"height":900},reduced_motion=motion)
       errors=[];page.on("pageerror",lambda e:errors.append(str(e)))
       page.set_content(source,wait_until="domcontentloaded")
       page.locator("#wh-view-history").click()
       page.wait_for_function("()=>whOpen&&document.querySelector('#wh-root')&&!galleryStageTransition&&!galleryStageFadeInProgress",timeout=8000)
       for theme in themes:
        page.evaluate("t=>document.body.dataset.theme=t",theme)
        reset(page,5,3)
        first=page.evaluate(snapshot);geom(first,5,3)
        assert first["path"] and first["same"] and first["summary"] and first["panel"],first
        page.wait_for_timeout(130)
        later=page.evaluate(snapshot);geom(later,5,3)
        assert (first["path"]==later["path"])==(motion=="reduce"),(theme,motion,first,later)
        # Actual transparent endpoint cutout must appear in a full pattern period.
        cuts=page.evaluate("""async()=>{const path=document.querySelector('.wh-progress-cut');const seen=[];
          for(let i=0;i<18;i++){seen.push(path.getAttribute('d'));await new Promise(r=>setTimeout(r,70));}return seen;}""") if motion=="no-preference" else []
        if cuts:assert any(cuts) and any(not c for c in cuts),cuts
        click(page,9) # never -> partial: only the started boundary moves
        if motion=="no-preference":
            page.wait_for_timeout(90);mid=page.evaluate(snapshot)
            target=(mid["width"]-5)*9/12
            assert first["started"]<mid["started"]<target and abs(mid["done"]-first["done"])<.4,mid
        wait(page,motion);after=page.evaluate(snapshot);geom(after,5,4)
        assert after["same"] and after["summary"] and after["panel"] and after["count"]=="5 of 12 episodes watched",after
        click(page,6) # partial -> watched: gap remains stationary
        if motion=="no-preference":
            page.wait_for_timeout(90);mid=page.evaluate(snapshot)
            assert after["done"]<mid["done"]<(mid["width"]-5)*6/12 and abs(mid["started"]-after["started"])<.4,mid
        wait(page,motion);geom(page.evaluate(snapshot),6,3)
        click(page,6) # watched -> never
        wait(page,motion);geom(page.evaluate(snapshot),5,3)
        assert page.evaluate("whRecords[0].episodes[5].progressSeconds")==42
        # rapid cycle and reversal must not leave stale geometry or replace the panel
        click(page,9);click(page,9);click(page,9)
        wait(page,motion);geom(page.evaluate(snapshot),5,3)
        # zero started and all started / partially watched endpoint
        reset(page,0,0);geom(page.evaluate(snapshot),0,0)
        reset(page,0,12);geom(page.evaluate(snapshot),0,12)
        reset(page,11,1);geom(page.evaluate(snapshot),11,1)
        click(page,12)
        if motion=="no-preference":
            page.wait_for_timeout(90);mid=page.evaluate(snapshot)
            assert not mid["complete"] and mid["done"]<mid["width"]-5 and mid["same"],mid
            click(page,12) # interrupt completion, watched -> never
            wait(page,motion);geom(page.evaluate(snapshot),11,0)
            click(page,12);wait(page,motion);click(page,12)
        wait(page,motion);assert page.evaluate(snapshot)["complete"],(theme,motion)
        click(page,12);wait(page,motion);geom(page.evaluate(snapshot),11,0)
        assert page.evaluate(snapshot)["panel"] and page.evaluate(snapshot)["summary"]
        # a single partial episode within a long season: small endpoint stays within its region
        page.evaluate("""()=>{const r=whRecords[0];r.episodes=Array.from({length:120},(_,i)=>({n:i+1,started:i===0,watched:false,progressSeconds:0,duration:1440,manualStatus:i===0?'partial':'never'}));whRender()}""")
        tiny=page.evaluate(snapshot)
        assert 0<tiny["end"]<8 and tiny["path"]=="" and abs(tiny["gap"]-5)<.3,tiny
        assert not errors,errors
        print("PASS History Option A",Path(sys.argv[1]).name,width,motion,theme,flush=True)
       reset(page,5,3)
       page.locator("[data-wh-exit]").click()
       page.wait_for_function("()=>!whOpen&&!document.querySelector('#wh-root')&&!whProgressFrame&&whProgressEntries.size===0",timeout=8000)
       assert not errors,errors
       page.close()
    browser.close()
