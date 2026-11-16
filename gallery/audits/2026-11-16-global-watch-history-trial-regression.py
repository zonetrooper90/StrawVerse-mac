#!/usr/bin/env python3
"""Global Watch History trial: exact default HTML, primary/detail origins, search and accessibility."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
source=Path(sys.argv[1]).read_text(encoding="utf-8")
origin="https://gallery-global-history.invalid/"
themes=("ocean","twilight","ember","slate","glacier","verdant")
def settled(page):
    page.wait_for_function("()=>!galleryStageTransition&&!galleryStageFadeInProgress&&!galleryStagePending",timeout=8000)
def primary(page,view):
    page.wait_for_function("v=>state.view===v&&!whOpen&&!state.detailId&&!state.playback&&!tabPagesViewport.hidden&&!galleryStageFadeInProgress",arg=view,timeout=8000)
def history(page):
    page.wait_for_function("()=>whOpen&&!screen.hidden&&!galleryStageFadeInProgress",timeout=8000)
    assert page.locator("#header-watch-history").get_attribute("aria-pressed")=="true"
    assert page.locator("#wh-root").is_visible() and not page.locator(".tabs").is_visible()
    assert page.locator("#header-search-input").get_attribute("placeholder")=="Search watch history…"
def controls(page):
    return page.evaluate("""()=>['search','header-watch-history','settings'].map(id=>{
      const r=document.getElementById(id).getBoundingClientRect();return [r.left,r.right,r.top,r.bottom]
    })""")
def no_banner(page):
    assert page.locator(".continue-shell,.wh-recent-row,#wh-view-history").count()==0
    assert page.locator("#sf-discover-explore").count()==1
def detail_snapshot(page):
    return page.evaluate("""()=>({id:state.detailId,view:state.view,season:state.detailSeason,related:state.detailRelated,
      episode:state.detailEpisode,audio:state.detailAudio,filter:state.detailEpisodeFilter,returnView:state.detailReturnView,
      returnHistory:state.detailReturnHistory,returnScroll:state.detailReturnScroll,scroll:workspace.scrollTop,
      rail:screen.querySelector('#inline-installment-rail')?.scrollLeft||0})""")
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True)
    for width in (1440,420):
      for motion in ('no-preference','reduce'):
        for theme in themes:
          page=browser.new_page(viewport={'width':width,'height':900},reduced_motion=motion)
          errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
          page.route(origin+"**",lambda route:route.fulfill(status=200,content_type="text/html",body=source))
          page.goto(origin,wait_until="domcontentloaded");primary(page,'discover')
          page.evaluate("t=>{state.theme=t;document.body.dataset.theme=t}",theme)
          no_banner(page)
          button=page.locator('#header-watch-history')
          assert button.is_visible() and button.is_enabled() and button.get_attribute('aria-label')=='Watch History'
          assert button.get_attribute('aria-pressed')=='false'
          before=controls(page)
          assert before[0][1]<before[1][0] and before[1][1]<before[2][0],before
          assert all(b[0]>=0 and b[1]<=width for b in before),before
          # Search expands left, never moves the utility controls or resurrects the rail.
          margin=page.locator('#sf-discover-explore').evaluate("e=>getComputedStyle(e).marginTop")
          page.locator('#search').click();page.wait_for_timeout(380 if motion=='no-preference' else 30)
          assert controls(page)==before,(before,controls(page))
          field=page.locator('#header-search-field').bounding_box()
          assert field and field['x']>=0 and field['x']+field['width']<=before[0][0]+1,field
          page.locator('#header-search-input').fill('Astra');no_banner(page)
          assert page.locator('#sf-discover-explore').evaluate("e=>getComputedStyle(e).marginTop")==margin
          page.locator('#header-search-input').press('Escape');page.wait_for_timeout(380 if motion=='no-preference' else 30)
          no_banner(page)
          for view,label in (('discover','Discover'),('library','Library'),('downloads','Downloads')):
            if view!='discover':
              page.locator('#nav-'+view).click();primary(page,view)
              page.wait_for_timeout(650 if motion=='no-preference' else 30)
            page.evaluate("v=>tabPages[v].scrollTop=Math.min(140,tabPages[v].scrollHeight-tabPages[v].clientHeight)",view)
            scroll=page.evaluate("v=>tabPages[v].scrollTop",view)
            button.focus();page.keyboard.press('Enter');history(page)
            assert 'Back to '+label in page.locator('[data-wh-exit]').inner_text()
            if view=='discover':
              # Full history search and Settings retain context.
              page.locator('[data-wh-filter="progress"]').click()
              page.locator('#search').click()
              page.locator('#header-search-input').fill('Astra')
              assert page.evaluate("()=>whSearch")=='Astra'
              page.locator('#header-search-input').press('Escape')
              assert page.evaluate("()=>whSearch")=='' and page.locator('#header-search-input').get_attribute('placeholder')=='Search watch history…'
              page.locator('#settings').click();settled(page)
              assert button.is_disabled()
              page.locator('#settings-back').click();settled(page);history(page)
              assert button.is_enabled() and page.locator('[data-wh-filter="progress"]').get_attribute('aria-pressed')=='true'
            if view=='library':button.click()
            else:page.locator('[data-wh-exit]').click()
            primary(page,view)
            assert button.get_attribute('aria-pressed')=='false'
            assert abs(page.evaluate("v=>tabPages[v].scrollTop",view)-scroll)<=1,(view,scroll)
            no_banner(page)
          page.locator('#nav-discover').click();primary(page,'discover')
          page.wait_for_timeout(650 if motion=='no-preference' else 30)
          page.locator('[data-tab-page="discover"] .poster-button[data-detail]').first.click();settled(page)
          assert page.evaluate("()=>Boolean(state.detailId)")
          prior=detail_snapshot(page)
          button.click();history(page)
          assert 'Back to Anime Details' in page.locator('[data-wh-exit]').inner_text()
          page.locator('[data-wh-exit]').click();settled(page)
          after=detail_snapshot(page)
          for key in prior:
            if key in ('scroll','rail'):assert abs(prior[key]-after[key])<=2,(key,prior,after)
            else:assert prior[key]==after[key],(key,prior,after)
          page.locator('#detail-back').click();primary(page,'discover');no_banner(page)
          assert not errors,errors
          page.close()
          print('PASS global Watch History',width,motion,theme,flush=True)
    browser.close()
print('PASS default no-banner layout and global Watch History routes',flush=True)
