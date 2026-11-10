#!/usr/bin/env python3
"""Browser visual-layout regression: no visible state switch before fully faded."""
import os,sys
from pathlib import Path
from playwright.sync_api import sync_playwright

src=Path(sys.argv[1]).read_text(encoding='utf-8')
assert 'function transitionGalleryPlayer(mutator)' in src
assert 'function transitionGalleryStage(mutator)' in src
assert 'showDetail(r.galleryId,false,r.installmentId)' in src
assert 'galleryStageFadeInProgress' in src
failures=[]
checks=0

def rec(name,condition,details=None):
 global checks
 checks+=1
 print('PASS' if condition else 'FAIL',name,details if not condition else '')
 if not condition: failures.append((name,details))

def do_route(page,label,action,target_check,expect_tabs=False,mode='fade'):
 before=page.evaluate("""()=>({view:state.view,detail:state.detailId,wh:whOpen,settings:document.body.classList.contains('settings-view'),nav:!!document.querySelector('.tabs').getClientRects().length,brand:document.querySelector('.brand').getBoundingClientRect().toJSON(),top:document.querySelector('.top').getBoundingClientRect().toJSON()})""")
 if mode=='fade':
  # Observe the DOM's real class mutation; it must happen only at full opacity 0.
  page.evaluate("""()=>{
    window.__fadeSwapSamples=[];
    window.__fadeSwapObserver?.disconnect();
    window.__fadeSwapObserver=new MutationObserver((entries)=>{
      for(const e of entries){
        const nav=document.querySelector('.top .tabs');
        window.__fadeSwapSamples.push({opacity:Number(getComputedStyle(workspace).opacity),navOpacity:Number(getComputedStyle(nav).opacity),busy:galleryStageFadeInProgress,classes:document.body.className,at:performance.now()});
      }
    });
    window.__fadeSwapObserver.observe(document.body,{attributes:true,attributeFilter:['class']});
  }""")
 action()
 if mode=='fade':
  page.wait_for_timeout(55)
  during=page.evaluate("""()=>({busy:galleryStageFadeInProgress,opacity:getComputedStyle(workspace).opacity,view:state.view,detail:state.detailId,wh:whOpen,settings:document.body.classList.contains('settings-view'),nav:!!document.querySelector('.tabs').getClientRects().length,brand:document.querySelector('.brand').getBoundingClientRect().toJSON()})""")
  rec(label+' outgoing state unchanged',during['view']==before['view'] and during['detail']==before['detail'] and during['wh']==before['wh'] and during['settings']==before['settings'],[before,during])
  rec(label+' outgoing phase active',during['busy'] and 0<float(during['opacity'])<=1,[during])
  rec(label+' header brand stays put',abs(during['brand']['y']-before['brand']['y'])<.1,[before,during])
  page.wait_for_function("()=>!galleryStageFadeInProgress",timeout=3000)
  after=page.evaluate("""()=>({busy:galleryStageFadeInProgress,opacity:getComputedStyle(workspace).opacity,nav:!!document.querySelector('.tabs').getClientRects().length,brand:document.querySelector('.brand').getBoundingClientRect().toJSON(),swaps:window.__fadeSwapSamples})""")
  rec(label+' nav matches incoming page',after['nav']==expect_tabs,after)
  rec(label+' swap occurred only at 0 opacity',len(after['swaps'])>0 and all(s['opacity']<0.02 and s['navOpacity']<0.02 and s['busy'] for s in after['swaps']),after['swaps'])
  rec(label+' fade cleaned up',not after['busy'] and float(after['opacity'])>.99,after)
  rec(label+' header brand never jumps',abs(after['brand']['y']-before['brand']['y'])<.1,[before['brand'],after['brand']])
 else:
  page.wait_for_timeout(80)
  now=page.evaluate("""()=>({busy:galleryStageFadeInProgress,transition:!!galleryStageTransition})""")
  rec(label+' reduced motion no delayed fade',not now['busy'] and not now['transition'],now)
 rec(label+' destination',target_check(),{})

with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=os.environ.get('GALLERY_TEST_CHROMIUM') or None,args=['--no-sandbox','--disable-dev-shm-usage'])
 for width,height,reduced in [(1440,900,'no-preference'),(620,750,'no-preference'),(1440,900,'reduce')]:
  print('\n===== VIEW',width,height,reduced)
  page=browser.new_page(viewport={'width':width,'height':height},reduced_motion=reduced)
  errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content(src,wait_until='load')
  page.wait_for_timeout(250)
  mode='instant' if reduced=='reduce' else 'fade'
  def stat():
   return page.evaluate("""()=>({view:state.view,wh:whOpen,detail:state.detailId,retHistory:state.detailReturnHistory,returnView:state.detailReturnView,settings:document.body.classList.contains('settings-view'),playback:!!state.playback,filters:whFilter,expanded:[...whExpanded],busy:galleryStageFadeInProgress})""")
  def route(label,action,test,has_nav=False):do_route(page,label,action,test,has_nav,mode)
  # This exact route was broken in the user's recording.
  recent=page.locator('[data-wh-recent]')
  rec('Recently Watched tiles exist',recent.count()>0,recent.count())
  route('Discover Recently Watched to Anime',lambda:recent.first.click(),lambda: stat()['detail'] is not None and not stat()['wh'] and not stat()['retHistory'] and stat()['returnView']=='discover')
  rec('Recently Watched Back label is Discover','Back to Discover' in page.locator('#detail-back').inner_text(),page.locator('#detail-back').inner_text())
  route('Recently Watched Anime back to Discover',lambda:page.locator('#detail-back').click(),lambda: stat()['detail'] is None and stat()['view']=='discover',True)
  route('Discover poster to Anime',lambda:page.locator('[data-detail]').first.click(),lambda: stat()['detail'] is not None)
  route('Anime to Settings',lambda:page.locator('#settings').click(),lambda:stat()['settings'])
  route('Settings back to Anime',lambda:page.locator('#settings-back').click(),lambda:not stat()['settings'] and stat()['detail'] is not None)
  route('Anime back to Discover',lambda:page.locator('#detail-back').click(),lambda:stat()['detail'] is None and stat()['view']=='discover',True)
  route('Discover to History',lambda:page.locator('#wh-view-history').click(),lambda:stat()['wh'])
  page.locator('[data-wh-filter="progress"]').click()
  page.locator('[data-wh-expand]').first.click()
  rec('History filter expansion survives',stat()['filters']=='progress' and len(stat()['expanded'])==1,stat())
  route('History to Settings',lambda:page.locator('#settings').click(),lambda:stat()['settings'] and stat()['wh'])
  route('Settings back to History',lambda:page.locator('#settings-back').click(),lambda:stat()['wh'] and not stat()['settings'] and stat()['filters']=='progress' and len(stat()['expanded'])==1)
  if page.locator('[data-wh-open]').count():
   route('History to linked Anime',lambda:page.locator('[data-wh-open]').first.click(),lambda:stat()['detail'] is not None and stat()['retHistory'])
   rec('History linked Back is Watch History','Back to Watch History' in page.locator('#detail-back').inner_text(),page.locator('#detail-back').inner_text())
   route('linked Anime back to History',lambda:page.locator('#detail-back').click(),lambda:stat()['wh'] and stat()['filters']=='progress')
  route('History to Discover',lambda:page.locator('[data-wh-exit]').click(),lambda:not stat()['wh'] and stat()['view']=='discover',True)
  route('Discover to Settings',lambda:page.locator('#settings').click(),lambda:stat()['settings'])
  route('Settings back to Discover',lambda:page.locator('#settings-back').click(),lambda:not stat()['settings'] and stat()['view']=='discover',True)
  page.evaluate('openSourceManagerFromDiscover()')
  page.wait_for_timeout(410 if mode=='fade' else 65)
  rec('Sources deep link',page.evaluate("settingsLastSection==='sources' && document.body.classList.contains('settings-view')"))
  route('Source Settings back to Discover',lambda:page.locator('#settings-back').click(),lambda:stat()['view']=='discover' and not stat()['settings'],True)
  # Player transitions retain the previous View Transition implementation.
  route('Discover poster to Anime for Player',lambda:page.locator('[data-detail]').first.click(),lambda:stat()['detail'] is not None)
  watch=page.locator('[data-episode-action="watch"]:not([disabled])')
  rec('Anime has watch button',watch.count()>0,watch.count())
  if watch.count():
   watch.first.click()
   page.wait_for_timeout(70)
   if mode=='fade':
    rec('Player uses preserved snapshot',page.evaluate('!!galleryStageTransition && !galleryStageFadeInProgress'))
   page.wait_for_timeout(350 if mode=='fade' else 80)
   rec('Player opened',stat()['playback'])
   page.locator('#back-from-playback').click()
   page.wait_for_timeout(70)
   if mode=='fade':rec('Player back preserved snapshot',page.evaluate('!!galleryStageTransition && !galleryStageFadeInProgress'))
   page.wait_for_timeout(380 if mode=='fade' else 60)
   rec('Player back opens same Anime',not stat()['playback'] and stat()['detail'] is not None)
  rec('No browser errors',not errors,errors[:5])
  page.close()
 browser.close()
print('TOTAL',checks,'FAILURES',len(failures))
for f in failures:print('FAIL',f)
if failures:sys.exit(1)
