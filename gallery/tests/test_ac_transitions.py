#!/usr/bin/env python3
"""Verify A+C keyframes, secondary routes, main-tab motion and reduced motion."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import sys
html=Path(sys.argv[1]).read_text(encoding='utf-8')
assert "@keyframes gallery-stage-leave{0%{opacity:1;transform:scale(1)}48%" in html
assert "@keyframes gallery-stage-arrive{0%{opacity:.05;transform:scale(1.008)}48%" in html
assert "::view-transition-old(gallery-stage){animation:gallery-stage-leave .45s" in html
assert "::view-transition-new(gallery-stage){animation:gallery-stage-arrive .45s" in html
assert 'gallery-about-forward .45s' in html
assert 'transform:translateY(-5px)' not in html[:60000]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 for size,motion in [(1440,'no-preference'),(620,'no-preference'),(1440,'reduce')]:
  page=browser.new_page(viewport={'width':size,'height':900},reduced_motion=motion)
  errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
  page.set_content(html,wait_until='load')
  page.wait_for_timeout(300)
  # Main-tab transitions remain native Gallery slides.
  page.locator('.tab[data-view="library"]').click()
  page.wait_for_timeout(35)
  assert page.evaluate("state.view")=='library'
  page.wait_for_timeout(500)
  page.locator('.tab[data-view="discover"]').click()
  page.wait_for_timeout(530)
  page.locator('[data-detail]').first.click()
  page.wait_for_timeout(90)
  status=page.evaluate("""() => ({
    detail:state.detailId,
    transition:!!galleryStageTransition,
    old:getComputedStyle(document.documentElement,'::view-transition-old(gallery-stage)').animationDuration,
    next:getComputedStyle(document.documentElement,'::view-transition-new(gallery-stage)').animationDuration,
    stage:workspace.style.viewTransitionName
  })""")
  assert status['detail'] is not None,status
  if motion!='reduce':
   assert status['transition'],status
   assert status['old']=='0.45s' and status['next']=='0.45s',status
  else:
   assert not status['transition'],status
  page.wait_for_timeout(550)
  page.locator('#detail-back').click()
  page.wait_for_timeout(550)
  assert page.evaluate("state.detailId") is None
  page.locator('#settings').click()
  page.wait_for_timeout(80)
  assert page.evaluate("document.body.classList.contains('settings-view')")
  assert page.evaluate("getComputedStyle(document.querySelector('#settings-page')).animationDuration")=='0.28s' if motion!='reduce' else True
  page.locator('#settings-back').click()
  page.wait_for_timeout(460)
  assert not page.evaluate("document.body.classList.contains('settings-view')")
  assert not errors,errors
  print('PASS',size,motion,'secondary A+C route and Settings exit')
  page.close()
 browser.close()
