#!/usr/bin/env python3
"""Gallery secondary page route-matrix regression test against a recovered HTML checkpoint.

Run: python3 gallery/tools/restore-checkpoint.py --output /tmp/Gallery-current.html
     python3 gallery/tests/test_transitions.py /tmp/Gallery-current.html
Requires: pip install playwright && python -m playwright install chromium
"""
from playwright.sync_api import sync_playwright
from pathlib import Path
import os, sys, subprocess
import traceback
PATH=Path(sys.argv[1] if len(sys.argv)>1 else 'Gallery-current.html')
checks=[];issues=[]
def rec(label,cond,meta=None):
 ok=bool(cond);checks.append((label,ok,meta))
 if not ok: issues.append((label,meta))
 print(('PASS' if ok else 'FAIL'), label, meta or '')
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True, executable_path=os.environ.get('GALLERY_TEST_CHROMIUM') or None,args=['--no-sandbox','--disable-dev-shm-usage'])
 for width,height,reduced in [(1440,900,'no-preference'),(620,750,'no-preference'),(1440,900,'reduce')]:
  page=browser.new_page(viewport={'width':width,'height':height},reduced_motion=reduced)
  err=[];page.on('pageerror', lambda e:err.append(str(e)))
  page.set_content(PATH.read_text(),wait_until='load')
  page.wait_for_timeout(350)
  print('\n======',width,reduced,'======')
  def stat():return page.evaluate('''() => ({detail:state.detailId,returnHistory:state.detailReturnHistory,wh:whOpen,view:state.view,screen:!screen.hidden,settings:document.body.classList.contains('settings-view'),key:screen.dataset.surfaceKey,animations:document.getAnimations().map(a=>a.animationName||'WAAPI'),historyFilter:whFilter,expanded:[...whExpanded],transition:!!galleryStageTransition})''')
  def wait():
   # A 300ms CSS/WAAPI duration is not a reliable 320ms wall-clock guarantee.
   # Await the actual route animation completion before clicking an element
   # on the newly visible page; this is what an ordinary user experiences.
   page.wait_for_timeout(320)
   page.wait_for_function("() => !galleryStageTransition && (typeof galleryStageFadeInProgress === 'undefined' || !galleryStageFadeInProgress)",timeout=5000)
  # tabs
  for name in ['library','downloads','discover']:
   page.locator('.tab[data-view="'+name+'"]').click();wait()
   rec('main tab '+name,stat()['view']==name)
  page.locator('[data-detail]').first.click();wait()
  rec('Discover -> Anime',stat()['detail'] is not None)
  page.locator('#detail-back').click();wait()
  rec('Anime -> Discover',not stat()['screen'] and stat()['key']=='')
  page.locator('[data-detail]').first.click();wait()
  rec('same Anime revisit',stat()['detail'] is not None)
  page.locator('#detail-back').click();wait()
  # history
  page.locator('#wh-view-history').click();wait()
  rec('Discover -> History',stat()['wh'])
  page.locator('[data-wh-filter="progress"]').click();wait()
  page.locator('[data-wh-expand]').first.click();wait()
  rec('History filter/expand',stat()['historyFilter']=='progress' and len(stat()['expanded'])==1,stat())
  # settings from history
  page.locator('#settings').click();wait()
  rec('History -> Settings',stat()['settings'] and stat()['wh'],stat())
  page.locator('#settings-back').click();page.wait_for_timeout(440)
  rec('Settings -> History',stat()['wh'] and not stat()['settings'] and stat()['historyFilter']=='progress' and len(stat()['expanded'])==1,stat())
  # linked anime
  candidate=page.locator('[data-wh-open]')
  print('history links',candidate.count())
  if candidate.count():
   try:
    candidate.first.click();wait()
    rec('History -> linked anime',stat()['detail'] is not None and stat()['returnHistory'],stat())
    if stat()['detail']:
     rec('Anime Back label History', 'Watch History' in page.locator('#detail-back').inner_text())
     page.locator('#detail-back').click();wait()
     rec('linked Anime -> History',stat()['wh'] and stat()['historyFilter']=='progress',stat())
   except Exception as e:issues.append(('history anime exception',str(e)));print('ERROR history anime',e)
  # history exit
  if stat()['wh']:
   page.locator('[data-wh-exit]').click();wait()
   rec('History -> Discover',not stat()['wh'] and stat()['view']=='discover' and not stat()['screen'],stat())
  # about nested pages
  page.locator('#settings').click();wait()
  page.locator('[data-settings-section="about"]').click();wait()
  about=page.locator('[data-about-open]')
  if about.count():
   dest=about.first.get_attribute('data-about-open');about.first.click();page.wait_for_timeout(55)
   active=page.evaluate('''() => ({active:currentAboutView,animations:[...document.getAnimations()].map(a=>a.animationName).filter(Boolean)})''')
   rec('About forward motion obeyed',active['active']==dest and (any('gallery-about' in str(x) for x in active['animations']) if reduced!='reduce' else not any('gallery-about' in str(x) for x in active['animations'])),active)
   page.locator('#settings-back').click();page.wait_for_timeout(55)
   active=page.evaluate('''() => ({active:currentAboutView,animations:[...document.getAnimations()].map(a=>a.animationName).filter(Boolean)})''')
   rec('About Back motion obeyed',active['active']=='overview' and (any('gallery-about' in str(x) for x in active['animations']) if reduced!='reduce' else not any('gallery-about' in str(x) for x in active['animations'])),active)
  page.locator('#settings-back').click();page.wait_for_timeout(400)
  rec('settings close',not stat()['settings'])
  rec('no JS errors',not err,err[:8])
  if reduced=='reduce':
   page.locator('[data-detail]').first.click();wait()
   page.emulate_media(reduced_motion='no-preference');page.wait_for_timeout(70)
   rec('live reduced motion toggle no stale class',not page.locator('#screen').evaluate("e=>e.classList.contains('surface-enter')"),stat())
  page.close()
 browser.close()
print('RESULT',len(checks),'checks, issues',len(issues),issues)
if issues:raise SystemExit(1)
# Mandatory in both existing browser/publisher regression runners.
subprocess.run([sys.executable,str(Path(__file__).with_name('test_first_release_reveal.py')),str(PATH)],check=True)
