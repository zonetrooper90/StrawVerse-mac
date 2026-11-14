#!/usr/bin/env python3
"""Read-only diagnostic: exact failed coordinated-motion candidate, no publication."""
import hashlib,json,runpy,sys
from pathlib import Path
from playwright.sync_api import sync_playwright

def checked(path,sha):
    raw=Path(path).read_bytes()
    assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==sha,path
    return runpy.run_path(path)

S=checked("gallery/changes/pending/2026-11-14-discover-search-coordinated-scroll.py","49837b18cf6d5500e947d13a772825686f005cc3")
T=checked("gallery/tests/test_discover_search_motion.py","abef4b34f8df79d1b82db62805d479ab5645599e")
EXPECTED={"full":"3c3f44942a825fc140ff062b871f0b9488e80e911cbcad49546e3e10abe1a606","lightweight":"1944d6341c760c0b7be55704dc9263aa6fb46d73e329e0e1553852cfff2f7b91"}
DETAIL="""()=>{const p=tabPages.discover,s=p.querySelector('.continue-shell');
 const e=document.querySelector('#sf-discover-explore'),r=e?.getBoundingClientRect();
 return {top:p.scrollTop,max:p.scrollHeight-p.clientHeight,height:s.getBoundingClientRect().height,
   client:p.clientHeight,scrollHeight:p.scrollHeight,outer:workspace.scrollTop,
   doc:document.scrollingElement.scrollTop,viewport:[innerWidth,innerHeight],
   explore:r?[r.x,r.y,r.width,r.height]:null,saved:searchScrollBefore,open:searchOpen,
   active:document.activeElement?.id,anchor:getComputedStyle(p).overflowAnchor,
   font:document.fonts.status,guard:p.classList.contains('search-scroll-restoring')};
}"""
# Capture the input events before the app and capture the same click after it.
# Keep the original trace unchanged; no animation or application code is altered.
EVENTS="""()=>{window.__motionEvents=[];const read=()=>{const p=tabPages.discover,s=p.querySelector('.continue-shell'),r=s.getBoundingClientRect();
 return {t:performance.now(),top:p.scrollTop,max:p.scrollHeight-p.clientHeight,height:r.height,
   outer:workspace.scrollTop,doc:document.scrollingElement.scrollTop,saved:searchScrollBefore,
   open:searchOpen,focus:document.activeElement?.id,guard:p.classList.contains('search-scroll-restoring'),
   motion:typeof discoverSearchRestore!=='undefined'&&discoverSearchRestore?
     {from:discoverSearchRestore.from,top:discoverSearchRestore.top,opening:discoverSearchRestore.opening}:null};};
 for(const type of ['pointerdown','mousedown','pointerup','mouseup','click']){
  const capture=e=>{if(!e.target.closest('#search,#header-search-close'))return;window.__motionEvents.push({phase:type+'-capture',...read()});};
  const bubble=e=>{if(!e.target.closest('#search,#header-search-close'))return;window.__motionEvents.push({phase:type+'-bubble',...read()});};
  document.addEventListener(type,capture,true);document.addEventListener(type,bubble);
 }
}"""
def detail(page):return page.evaluate(DETAIL)
def trace(page,selector,before,target,opening,motion):
    page.evaluate("()=>window.__motionEvents=[]")
    pre=detail(page)
    page.evaluate(T["TRACE"])
    page.locator(selector).click()
    page.wait_for_function("()=>window.__scrollTrace!==null",timeout=10000)
    T["wait"](page)
    after=detail(page)
    result=page.evaluate("()=>({events:window.__motionEvents,trace:window.__scrollTrace})")
    frames=result["trace"]["frames"];events=result["events"]
    cap=next(e for e in events if e["phase"]=="click-capture")
    bubble=next(e for e in events if e["phase"]=="click-bubble")
    actual_start=cap["top"]
    h0,h1=cap["height"],after["height"]
    expected_end=target
    if opening:expected_end=0
    mid=[f for f in frames if min(h0,h1)+2<f["height"]<max(h0,h1)-2]
    deviations=[]
    if abs(h1-h0)>2:
        for f in frames:
            progress=max(0,min(1,(f["height"]-h0)/(h1-h0)))
            expected=max(0,min(f["max"],actual_start+(expected_end-actual_start)*progress))
            deviations.append(abs(f["top"]-expected))
    evidence={"expectedBefore":before,"preClick":pre,"capture":cap,"bubble":bubble,
       "firstFrame":frames[0],"lastFrame":frames[-1],"settled":after,"timing":result["trace"]["timing"],
       "originalStartAssertion":abs(frames[0]["top"]-before["top"])<=2 and abs(frames[0]["height"]-before["height"])<=2,
       "preClickDrift":cap["top"]-before["top"],"clickJump":bubble["top"]-cap["top"],
       "heightDrift":cap["height"]-before["height"],"endError":after["top"]-expected_end,
       "maxSyncError":max(deviations,default=0),"intermediateFrames":len(mid),
       "intermediateScrollFrames":sum(min(actual_start,expected_end)+2<f["top"]<max(actual_start,expected_end)-2 for f in mid),
       "events":events}
    return evidence
def main(mode,motion):
    filename,digest=S["FILES"][mode]
    baseline=Path(filename).read_bytes()
    assert hashlib.sha256(baseline).hexdigest()==digest
    candidate=S["transform"](baseline)
    assert hashlib.sha256(candidate).hexdigest()==EXPECTED[mode]
    print("EXACT FAILED CANDIDATE",mode,motion,EXPECTED[mode],flush=True)
    count=0;failures=[];jumps=[];wrong_end=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
        for theme in T["THEMES"]:
            for width in (1440,370):
                page=browser.new_page(viewport={"width":width,"height":950},reduced_motion=motion)
                errors=[];page.on("pageerror",lambda e:errors.append(str(e)))
                page.set_content(candidate.decode(),wait_until="domcontentloaded")
                page.evaluate("""theme=>{state.theme=theme;document.body.dataset.theme=theme;window.__scrollShell=tabPages.discover.querySelector('.continue-shell');}""",theme)
                T["wait"](page);page.evaluate(EVENTS)
                # Replay the original sequence on the same page: top, 100px, bottom.
                # Record the pre-click values before and after Playwright input.
                for kind in (0,100,"bottom"):
                    before=T["position"](page,kind)
                    initial=detail(page)
                    opened=trace(page,"#search",before,0,True,motion)
                    if kind!=0:
                        q=page.evaluate("getSourceCataloguePreview().titles[0].name")
                        page.locator("#header-search-input").fill(q)
                        assert page.evaluate("state.query")==q
                        page.locator("#header-search-input").fill("zzzz-no-gallery-match-zzzz")
                        assert page.locator(".discover-result-region .poster-button").count()==0
                        page.locator("#header-search-clear").click()
                        assert not page.evaluate("state.query")
                    closed=trace(page,"#header-search-close" if kind==100 else "#search",T["snap"](page),before["top"],False,motion)
                    for direction,e in (("open",opened),("close",closed)):
                        case={"theme":theme,"width":width,"position":kind,"direction":direction}
                        print("MOTION EVIDENCE",mode,motion,json.dumps({**case,"initial":initial,**e},sort_keys=True),flush=True)
                        if motion=="no-preference":
                            if not e["originalStartAssertion"]:failures.append({**case,**{k:e[k] for k in ("preClickDrift","heightDrift","clickJump","endError","maxSyncError")},"expectedBefore":e["expectedBefore"],"capture":e["capture"],"bubble":e["bubble"]})
                            if abs(e["clickJump"])>2:jumps.append({**case,"jump":e["clickJump"]})
                        if abs(e["endError"])>1:wrong_end.append({**case,"error":e["endError"]})
                        count+=1
                assert not errors,errors
                page.close()
        browser.close()
    assert count==72,count
    print("DIAGNOSTIC RESULT",mode,motion,json.dumps({"actions":count,"originalAssertionFailures":failures,"clickJumps":jumps,"incorrectDestinations":wrong_end},sort_keys=True),flush=True)
if __name__=="__main__":main(*sys.argv[1:])
