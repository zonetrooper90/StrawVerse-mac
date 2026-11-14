#!/usr/bin/env python3
"""Real Chromium coordinated Discover Search shell, margin and scroll motion; original assertions retained."""
import argparse,os
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
THEMES=("ocean","twilight","ember","slate","glacier","verdant")
SNAP="""()=>{const p=tabPages.discover,s=p.querySelector('.continue-shell');
 return {top:p.scrollTop,max:p.scrollHeight-p.clientHeight,height:s.getBoundingClientRect().height,
   margin:parseFloat(getComputedStyle(p.querySelector('.sf-discover-explore')).marginTop),
   open:searchOpen,guard:p.classList.contains('search-scroll-restoring'),
   same:s===window.__scrollShell,focus:document.activeElement?.id,
   anchor:getComputedStyle(p).overflowAnchor,ids:[...p.querySelectorAll('.discover-result-region [data-detail]')].map(e=>e.dataset.detail)};
}"""
TRACE="""()=>{window.__scrollTrace=null;
 const handler=e=>{if(!e.target.closest('#search,#header-search-close'))return;
  document.removeEventListener('click',handler);
  const p=tabPages.discover,s=p.querySelector('.continue-shell'),explore=p.querySelector('.sf-discover-explore'),start=performance.now(),frames=[];
  const sample=()=>{const h=s.getBoundingClientRect().height;frames.push({t:performance.now()-start,top:p.scrollTop,max:p.scrollHeight-p.clientHeight,height:h,margin:parseFloat(getComputedStyle(explore).marginTop),guard:p.classList.contains('search-scroll-restoring')});};
  sample();
  const timing=s.getAnimations().filter(a=>a.transitionProperty==='grid-template-rows').map(a=>a.effect.getTiming().duration);
  const marginTiming=explore.getAnimations().filter(a=>a.transitionProperty==='margin-top').map(a=>a.effect.getTiming().duration);
  const tick=()=>{sample();if(performance.now()-start<650)requestAnimationFrame(tick);else window.__scrollTrace={frames,timing,marginTiming};};
  requestAnimationFrame(tick);
 };document.addEventListener('click',handler);
}"""
def snap(page):return page.evaluate(SNAP)
def wait(page):
    page.wait_for_function("""()=>!galleryStageTransition&&!galleryStageFadeInProgress&&!tabTrackAnimation&&
      !gallerySettingsOpening&&!settingsClosing&&!tabPages.discover.classList.contains('search-scroll-restoring')&&
      !tabPages.discover.querySelector('.continue-shell')?.getAnimations().some(a=>a.pending||a.playState==='running')""",timeout=10000)
    page.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
def open_search(page):
    page.locator('#search').click()
    wait(page)
    assert snap(page)['open'] and snap(page)['height']<=1,snap(page)
def position(page,kind):
    page.evaluate("""kind=>{const p=tabPages.discover;p.scrollTo({top:kind==='bottom'?p.scrollHeight-p.clientHeight:kind,behavior:'instant'});}""",kind)
    page.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
    return snap(page)
def near(x,y):return abs(x-y)<=1
def restored(page,before):
    after=snap(page)
    assert near(after['top'],before['top']) and near(after['height'],before['height']) and near(after['margin'],before['margin']) and after['same'] and not after['guard'] and not after['open'] and after['ids']==before['ids'],(before,after)
    assert after['anchor']==before['anchor'] and after['focus']=='search',(before,after)
    return after
def traced_action(page,selector,before,target,opening,motion):
    page.evaluate(TRACE)
    page.locator(selector).click()
    page.wait_for_function("()=>window.__scrollTrace!==null",timeout=10000)
    wait(page)
    after=snap(page);trace=page.evaluate("window.__scrollTrace");frames=trace["frames"]
    assert len(frames)>=2 and near(after["top"],target) and near(frames[-1]["top"],target),trace
    assert after["same"] and not after["guard"] and after["anchor"]==before["anchor"],(before,after)
    assert after["open"]==opening and after["focus"]==("header-search-input" if opening else "search"),after
    assert (after["height"]<=1 if opening else after["height"]>10),after
    assert near(before['margin'],29 if opening else 5) and near(after['margin'],5 if opening else 29),(before,after)
    if motion=="reduce":
        assert trace["timing"]==[] and all(near(f["top"],target) and near(f["height"],after["height"]) for f in frames),trace
        assert trace['marginTiming']==[] and all(near(f['margin'],after['margin']) for f in frames),trace
    else:
        assert trace["timing"]==[420],trace
        start,end=before["top"],target
        h0,h1=before["height"],after["height"]
        assert abs(frames[0]["top"]-start)<=2 and abs(frames[0]["height"]-h0)<=2,trace
        assert trace["marginTiming"]==[420] and near(frames[0]["margin"],before["margin"]),trace
        assert abs(frames[0]["max"]-before["max"])<=2,trace
        assert any(6<f["margin"]<28 for f in frames),trace
        for f in frames:
            progress=max(0,min(1,(f["height"]-h0)/(h1-h0)))
            expected_margin=before["margin"]+(after["margin"]-before["margin"])*progress
            assert abs(f["margin"]-expected_margin)<=2,(f,expected_margin,trace)
        assert any(f["guard"] for f in frames[1:-1]),trace
        mid=[f for f in frames if min(h0,h1)+2<f["height"]<max(h0,h1)-2]
        assert mid,trace
        if abs(end-start)>10:
            assert any(min(start,end)+2<f["top"]<max(start,end)-2 for f in mid),trace
            # Compare the scroll with observed native grid motion, allowing
            # layout rounding and the legal scroll range near the bottom.
            for f in frames:
                progress=max(0,min(1,(f["height"]-h0)/(h1-h0)))
                expected=min(f["max"],start+(end-start)*progress)
                assert abs(f["top"]-expected)<=max(5,abs(end-start)*.16),(before,after,f,expected,trace)
            sign=1 if end>start else -1
            assert all(sign*(b["top"]-a["top"])>=-2 for a,b in zip(frames,frames[1:])),trace
        else:assert all(near(f["top"],target) for f in frames),trace
    return after
def reverse_midflight(page,closing_first):
    # Dispatch the second real button action at an observed intermediate offset,
    # in the same browser frame as the continuity measurement.
    result=page.evaluate("""closing=>{
      const p=tabPages.discover;
      return new Promise((resolve,reject)=>{
       const start=performance.now();
       const tick=()=>{
        const top=p.scrollTop;
        if(top>5&&top<95){
         searchToggle.click();
         const next=p.scrollTop;
         resolve({before:top,after:next,open:searchOpen,saved:searchScrollBefore,guard:p.classList.contains('search-scroll-restoring')});
        }else if(performance.now()-start>1200)reject(Error('No intermediate scroll position for reversal '+top));
        else requestAnimationFrame(tick);
       };requestAnimationFrame(tick);
      });
    }""",closing_first)
    assert abs(result["after"]-result["before"])<=2 and result["open"]==closing_first and near(result["saved"],100) and result["guard"],result
    wait(page)
def run(mode,motion,smoke=False):
    html=(ROOT/("Gallery-current.html" if mode=="full" else "Gallery-development.html")).read_text()
    count=0
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,executable_path=os.environ.get("GALLERY_TEST_CHROMIUM") or None,args=["--no-sandbox","--disable-dev-shm-usage"])
        for theme in (THEMES[:1] if smoke else THEMES):
            for width in ((1440,) if smoke else (1440,370)):
                page=browser.new_page(viewport={"width":width,"height":950},reduced_motion=motion)
                errors=[];page.on("pageerror",lambda e:errors.append(str(e)))
                page.set_content(html,wait_until="domcontentloaded")
                page.evaluate("""theme=>{state.theme=theme;document.body.dataset.theme=theme;window.__scrollShell=tabPages.discover.querySelector('.continue-shell');}""",theme)
                wait(page)
                for kind in (("bottom",) if smoke else (0,100,"bottom")):
                    before=position(page,kind)
                    assert before["height"]>10 and before["max"]>100 and not before["guard"],before
                    if kind=="bottom":assert near(before["top"],before["max"]),before
                    opened=traced_action(page,'#search',before,0,True,motion)
                    if kind!=0:
                        q=page.evaluate("getSourceCataloguePreview().titles[0].name")
                        page.locator('#header-search-input').fill(q)
                        assert page.evaluate("state.query")==q
                        page.locator('#header-search-input').fill('zzzz-no-gallery-match-zzzz')
                        assert page.locator('.discover-result-region .poster-button').count()==0
                        page.locator('#header-search-clear').click()
                        assert not page.evaluate("state.query")
                    traced_action(page,'#header-search-close' if kind==100 else '#search',snap(page),before["top"],False,motion)
                    restored(page,before)
                    count+=1
                if not smoke:
                    # Both reversals preserve the initial saved destination.
                    before=position(page,100);open_search(page)
                    page.locator('#search').click()
                    if motion=="no-preference":
                        reverse_midflight(page,True)
                    else:
                        page.locator('#search').click();wait(page)
                    assert snap(page)["open"] and near(snap(page)["top"],0) and not snap(page)["guard"]
                    page.locator('#header-search-input').press('Escape');wait(page)
                    restored(page,before);count+=1
                    before=position(page,100)
                    page.locator('#search').click()
                    if motion=="no-preference":
                        reverse_midflight(page,False)
                    else:
                        page.locator('#search').click();wait(page)
                    restored(page,before);count+=1
                    # Intentional wheel input must win in both directions.
                    if motion=="no-preference":
                        for opening in (False,True):
                            before=position(page,300)
                            if not opening:open_search(page)
                            p=page.locator('[data-tab-page="discover"]').bounding_box()
                            page.locator('#search').click()
                            page.mouse.move(p["x"]+p["width"]/2,p["y"]+p["height"]/2)
                            page.mouse.wheel(0,80 if opening else -180)
                            wait(page)
                            page.wait_for_function("opening=>opening?tabPages.discover.scrollTop>1:tabPages.discover.scrollTop<220",arg=opening,timeout=5000)
                            page.wait_for_timeout(150)
                            after=snap(page)
                            assert not after["guard"] and (after["top"]>1 if opening else after["top"]<220),after
                            if opening:
                                page.locator('#search').click();wait(page)
                                restored(page,before)
                            count+=1
                    # Leaving during expansion cannot retain a restoration guard.
                    position(page,100);open_search(page)
                    page.locator('#search').click();page.locator('#nav-library').click();wait(page)
                    assert page.evaluate("state.view==='library'&&!searchOpen&&!tabPages.discover.classList.contains('search-scroll-restoring')")
                    # Non-Discover Search must not activate this guard.
                    page.locator('#search').click();wait(page)
                    page.locator('#search').click();wait(page)
                    assert not snap(page)["guard"]
                    count+=1
                assert not errors,(mode,motion,theme,width,errors)
                page.close()
        browser.close()
    expected=1 if smoke else 6*2*(8 if motion=="no-preference" else 6)
    assert count==expected,(count,expected)
    print("PASS: Coordinated Discover search scroll motion",mode,motion,count,"real interaction cases",flush=True)
def main():
    p=argparse.ArgumentParser();p.add_argument("--smoke",action="store_true");p.add_argument("--mode",choices=["full","lightweight"]);p.add_argument("--motion",choices=["no-preference","reduce"]);a=p.parse_args()
    if a.smoke:
        for mode in ("full","lightweight"):
            for motion in ("no-preference","reduce"):run(mode,motion,True)
    else:run(a.mode,a.motion)
if __name__=="__main__":main()
