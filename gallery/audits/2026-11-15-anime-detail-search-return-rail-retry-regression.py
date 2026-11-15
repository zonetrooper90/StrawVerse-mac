#!/usr/bin/env python3
"""Contextual Search from Anime Details: restore on dismiss, discard on navigation."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
source=Path(sys.argv[1]).read_text(encoding="utf-8")
themes=("ocean","twilight","ember","slate","glacier","verdant")
def settled(page):
    page.wait_for_function("()=>!galleryStageTransition&&!galleryStageFadeInProgress&&!galleryStagePending",timeout=8000)
def detail(page,id):
    page.wait_for_function("id=>state.detailId===id&&!screen.hidden&&!whOpen&&!galleryStageFadeInProgress",arg=id,timeout=8000)
def catalogue(page,view):
    page.wait_for_function("view=>state.view===view&&!state.detailId&&screen.hidden&&!tabPagesViewport.hidden&&!galleryStageFadeInProgress",arg=view,timeout=8000)
def search(page,view):
    page.locator("#search").click()
    page.wait_for_function("view=>searchOpen&&state.view===view&&!state.detailId&&screen.hidden&&!galleryStageFadeInProgress",arg=view,timeout=8000)
    assert page.locator("#header-search-input").evaluate("e=>document.activeElement===e")
def snapshot(page):
    return page.evaluate("""()=>({view:state.view,id:state.detailId,season:state.detailSeason,related:state.detailRelated,
      episode:state.detailEpisode,audio:state.detailAudio,filter:state.detailEpisodeFilter,returnHistory:state.detailReturnHistory,
      returnView:state.detailReturnView,returnScroll:state.detailReturnScroll,scroll:workspace.scrollTop,
      rail:screen.querySelector('#inline-installment-rail')?.scrollLeft||0,
      selected:screen.querySelector('[data-inline-installment][aria-current="true"]')?.dataset.inlineInstallment,
      back:screen.querySelector('#detail-back')?.textContent,
      visibleEpisodes:screen.querySelectorAll('.episode-item').length})""")
def same_detail(before,after):
    for key in before:
        if key in ("scroll","rail"):assert abs(before[key]-after[key])<=2,(key,before,after)
        else:assert before[key]==after[key],(key,before,after)
def select_release(page,id):
    # Actual release handler, without an offscreen pointer target intercepted by the rail arrows.
    page.locator('[data-inline-installment="'+id+'"]').evaluate("e=>e.click()")
    page.wait_for_timeout(500)
    # Native long-distance smooth scroll can outlast a fixed wall-clock wait.
    # Require a stable rail before capturing the position; do not relax equality.
    page.wait_for_function("""async()=>{
      const rail=screen.querySelector('#inline-installment-rail'),x=rail.scrollLeft;
      for(let i=0;i<8;i++){await new Promise(r=>requestAnimationFrame(r));if(Math.abs(rail.scrollLeft-x)>.5)return false;}
      return true;
    }""",timeout=5000)
    assert page.locator('[data-inline-installment="'+id+'"]').get_attribute("aria-current")=="true"
def scroll_detail(page):
    page.evaluate("()=>{workspace.scrollTo({top:Math.min(230,workspace.scrollHeight-workspace.clientHeight),behavior:'instant'})}")
def restored(page,before):
    detail(page,before["id"])
    page.wait_for_function("()=>!searchOpen&&searchDetailReturn===null&&!discoverSearchRestore&&!tabPages.discover.classList.contains('search-scroll-restoring')&&!tabPages.discover.classList.contains('search-scope-open')")
    same_detail(before,snapshot(page))
    assert page.locator("#search").get_attribute("aria-expanded")=="false"
def back(page,view):
    page.locator("#detail-back").click()
    catalogue(page,view)
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True)
    for width in (1440,620):
      for motion in ("no-preference","reduce"):
        page=browser.new_page(viewport={"width":width,"height":850},reduced_motion=motion)
        errors=[];page.on("pageerror",lambda e:errors.append(str(e)))
        page.set_content(source,wait_until="domcontentloaded")
        page.wait_for_selector("#wh-view-history")
        for theme in themes:
          page.evaluate("t=>document.body.dataset.theme=t",theme)
          catalogue(page,"discover")
          # Discover: selected second season, nondefault audio/filter, scroll and Back provenance.
          page.locator('.tab-page[data-tab-page="discover"] [data-detail="demo:quints"]').first.click()
          detail(page,"demo:quints")
          select_release(page,"quints-s2")
          page.locator('[data-detail-audio="dub"]').evaluate("e=>e.click()")
          page.locator('[data-episode-filter="playable"]').evaluate("e=>e.click()")
          page.wait_for_timeout(350);scroll_detail(page)
          before=snapshot(page)
          search(page,"discover")
          page.locator("#header-search-input").fill("no matching title zzz")
          assert page.locator('.tab-page[data-tab-page="discover"] .search-empty').count()==1
          page.locator("#header-search-input").press("Escape")
          restored(page,before)
          # Empty-query X dismiss, repeated opening, and related release identity.
          select_release(page,"quints-movie");scroll_detail(page);before=snapshot(page)
          search(page,"discover")
          page.locator("#header-search-close").click()
          restored(page,before)
          search(page,"discover")
          page.locator("#search").click()
          restored(page,before)
          back(page,"discover")
          # Library: long rail position and collection provenance, close by Escape.
          page.locator("#nav-library").click();catalogue(page,"library")
          page.wait_for_timeout(500)
          page.locator('.tab-page[data-tab-page="library"] [data-detail="demo:long"]').first.click()
          detail(page,"demo:long")
          select_release(page,"long-s10")
          scroll_detail(page);before=snapshot(page)
          assert before["rail"]>0,before
          search(page,"library")
          captured=page.evaluate("()=>searchDetailReturn.railScroll")
          assert abs(captured-before["rail"])<=2,(captured,before)
          page.locator("#header-search-input").fill("Solo Leveling")
          page.locator("#header-search-input").press("Escape")
          restored(page,before)
          # Deliberately choose a non-snap offset and verify the exact offset survives.
          page.evaluate("""()=>{const rail=screen.querySelector('#inline-installment-rail');
            rail.style.scrollSnapType='none';void rail.offsetWidth;
            rail.scrollTo({left:Math.min(rail.scrollWidth-rail.clientWidth,rail.scrollLeft+37),behavior:'instant'});}""")
          before=snapshot(page)
          search(page,"library")
          assert abs(page.evaluate("()=>searchDetailReturn.railScroll")-before["rail"])<=2
          page.locator("#header-search-input").press("Escape")
          restored(page,before)
          rail=page.locator("#inline-installment-rail")
          assert rail.evaluate("e=>getComputedStyle(e).scrollSnapType")=="none"
          # The already approved intentional-rail-input handler restores normal snap.
          rail.evaluate("e=>e.dispatchEvent(new WheelEvent('wheel',{deltaX:1}))")
          assert rail.evaluate("e=>e.style.scrollSnapType")=="" and rail.evaluate("e=>getComputedStyle(e).scrollSnapType")!="none"
          # Result selection wins, including keyboard Enter; Back uses the search catalogue.
          search(page,"library")
          page.locator("#header-search-input").fill("Solo Leveling")
          page.locator("#header-search-input").press("Enter")
          detail(page,"demo:solo")
          assert page.evaluate("()=>!searchOpen&&searchDetailReturn===null&&state.detailSeason===0&&state.detailReturnView==='library'&&!state.detailReturnHistory")
          back(page,"library")
          # Explicit tab navigation discards the old origin; ordinary top-level Search stays top-level.
          page.locator('.tab-page[data-tab-page="library"] [data-detail="demo:quints"]').first.click()
          detail(page,"demo:quints");search(page,"library")
          page.locator("#nav-discover").click();catalogue(page,"discover")
          page.wait_for_timeout(500)
          assert page.evaluate("()=>!searchOpen&&searchDetailReturn===null")
          page.locator("#search").click()
          page.locator("#header-search-input").press("Escape")
          page.wait_for_function("()=>!searchOpen&&!state.detailId&&!discoverSearchRestore",timeout=8000)
          # History-origin detail: preserve suspended filter/expanded/scroll and Back destination.
          page.locator("#wh-view-history").click()
          page.wait_for_function("()=>whOpen&&!galleryStageFadeInProgress&&!!document.querySelector('#wh-root')",timeout=8000)
          page.locator('[data-wh-filter="progress"]').click()
          page.locator('[data-wh-row="q2"] [data-wh-expand]').click()
          page.wait_for_timeout(400)
          history=page.evaluate("()=>({filter:whFilter,expanded:[...whExpanded],scroll:workspace.scrollTop})")
          page.locator('[data-wh-row="q2"] .wh-anime-title').click()
          detail(page,"demo:quints")
          before=snapshot(page);assert before["returnHistory"] and before["season"]==1,before
          search(page,"library")
          page.locator("#header-search-input").press("Escape")
          restored(page,before)
          page.locator("#detail-back").click()
          page.wait_for_function("()=>whOpen&&!galleryStageFadeInProgress",timeout=8000)
          now=page.evaluate("()=>({filter:whFilter,expanded:[...whExpanded],scroll:workspace.scrollTop})")
          assert history==now,(history,now)
          page.locator("[data-wh-exit]").click();catalogue(page,"discover")
          assert not errors,errors
          print("PASS contextual detail Search return",Path(sys.argv[1]).name,width,motion,theme,flush=True)
        page.close()
    browser.close()
