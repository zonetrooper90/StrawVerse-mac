#!/usr/bin/env python3
"""Real Chromium Discover Search scroll restoration; no style/animation replacement."""
import argparse,os
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
THEMES=("ocean","twilight","ember","slate","glacier","verdant")
SNAP="""()=>{const p=tabPages.discover,s=p.querySelector('.continue-shell');
 return {top:p.scrollTop,max:p.scrollHeight-p.clientHeight,height:s.getBoundingClientRect().height,
   open:searchOpen,guard:p.classList.contains('search-scroll-restoring'),
   same:s===window.__scrollShell,focus:document.activeElement?.id,
   anchor:getComputedStyle(p).overflowAnchor,ids:[...p.querySelectorAll('.discover-result-region [data-detail]')].map(e=>e.dataset.detail)};
}"""
TRACE="""()=>{window.__scrollTrace=null;
 const handler=e=>{if(!e.target.closest('#search,#header-search-close'))return;
  document.removeEventListener('click',handler);
  const p=tabPages.discover,s=p.querySelector('.continue-shell'),start=performance.now(),frames=[];
  const sample=()=>{const h=s.getBoundingClientRect().height;frames.push({top:p.scrollTop,max:p.scrollHeight-p.clientHeight,height:h,guard:p.classList.contains('search-scroll-restoring')});};
  sample();
  const timing=s.getAnimations().filter(a=>a.transitionProperty==='grid-template-rows').map(a=>a.effect.getTiming().duration);
  const tick=()=>{sample();if(performance.now()-start<650)requestAnimationFrame(tick);else window.__scrollTrace={frames,timing};};
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
    assert near(after['top'],before['top']) and near(after['height'],before['height']) and after['same'] and not after['guard'] and not after['open'] and after['ids']==before['ids'],(before,after)
    assert after['anchor']==before['anchor'] and after['focus']=='search',(before,after)
    return after
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
                for kind in ((100,) if smoke else (0,100,"bottom")):
                    before=position(page,kind)
                    assert before["height"]>10 and before["max"]>100 and not before["guard"],before
                    if kind=="bottom":assert near(before["top"],before["max"]),before
                    open_search(page)
                    if kind!=0:
                        q=page.evaluate("getSourceCataloguePreview().titles[0].name")
                        page.locator('#header-search-input').fill(q)
                        assert page.evaluate("state.query")==q
                        page.locator('#header-search-input').fill('zzzz-no-gallery-match-zzzz')
                        assert page.locator('.discover-result-region .poster-button').count()==0
                        page.locator('#header-search-clear').click()
                        assert not page.evaluate("state.query")
                    page.evaluate(TRACE)
                    page.locator('#header-search-close' if kind==100 else '#search').click()
                    page.wait_for_function("()=>window.__scrollTrace!==null",timeout=10000)
                    wait(page);after=restored(page,before)
                    trace=page.evaluate("window.__scrollTrace")
                    frames=trace["frames"]
                    assert len(frames)>=2 and near(frames[-1]["top"],before["top"]),trace
                    assert all(near(f["top"],min(before["top"],f["max"])) for f in frames),(mode,motion,theme,width,kind,before,trace)
                    if motion=="reduce":
                        assert trace["timing"]==[] and all(near(f["height"],after["height"]) for f in frames),trace
                    else:
                        assert trace["timing"]==[420],trace
                        assert any(2<f["height"]<after["height"]-2 for f in frames),trace
                    count+=1
                if not smoke:
                    # Rapid reopen supersedes the earlier restoration. Escape is a real close.
                    before=position(page,100);open_search(page)
                    page.locator('#search').click();page.locator('#search').click()
                    assert page.evaluate("searchOpen&&!tabPages.discover.classList.contains('search-scroll-restoring')")
                    wait(page);page.locator('#header-search-input').press('Escape');wait(page)
                    restored(page,before);count+=1
                    # An intentional wheel scroll must not be overwritten by the guard.
                    if motion=="no-preference":
                        before=position(page,300);open_search(page)
                        p=page.locator('[data-tab-page="discover"]').bounding_box()
                        page.mouse.move(p["x"]+p["width"]/2,p["y"]+p["height"]/2)
                        page.locator('#search').click()
                        page.mouse.move(p["x"]+p["width"]/2,p["y"]+p["height"]/2)
                        page.mouse.wheel(0,-180)
                        wait(page)
                        page.wait_for_function("()=>tabPages.discover.scrollTop<220",timeout=5000)
                        assert not snap(page)["guard"],snap(page)
                        page.wait_for_timeout(150)
                        assert snap(page)["top"]<220,snap(page)
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
    expected=1 if smoke else 6*2*(6 if motion=="no-preference" else 5)
    assert count==expected,(count,expected)
    print("PASS: Discover search scroll restoration",mode,motion,count,"real interaction cases",flush=True)
def main():
    p=argparse.ArgumentParser();p.add_argument("--smoke",action="store_true");p.add_argument("--mode",choices=["full","lightweight"]);p.add_argument("--motion",choices=["no-preference","reduce"]);a=p.parse_args()
    if a.smoke:
        for mode in ("full","lightweight"):
            for motion in ("no-preference","reduce"):run(mode,motion,True)
    else:run(a.mode,a.motion)
if __name__=="__main__":main()
