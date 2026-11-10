#!/usr/bin/env python3
"""Regression tests for hidden transfer actions and Download-style Watch History rows."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

source=Path(sys.argv[1]).read_text(encoding='utf-8')
assert 'GALLERY_COLLECTION_TRANSFER_UI_ENABLED=false' in source
assert 'function showImport()' in source and 'function showShare()' in source
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True)
    page=browser.new_page(viewport={'width':1200,'height':850})
    errors=[]
    page.on('pageerror', lambda exc: errors.append(str(exc)))
    page.set_content(source, wait_until='domcontentloaded')
    page.wait_for_timeout(160)
    assert page.locator('#wh-view-history').count()==1
    page.locator('[data-view="library"]').first.click()
    page.wait_for_timeout(500)
    assert page.locator('#import').count()==0
    assert page.locator('#newtag').count()==1
    assert page.locator('#sharetag').count()==0
    page.locator('[data-tag="Comfort Picks"]').first.click()
    page.wait_for_timeout(120)
    assert page.locator('#sharetag').count()==0
    page.locator('[data-view="discover"]').first.click()
    page.wait_for_timeout(500)
    page.locator('#wh-view-history').click()
    page.wait_for_timeout(500)
    assert page.locator('#wh-root').count()==1
    first=page.locator('.wh-season').first
    assert first.locator('.wh-summary-hit').count()==1
    assert first.locator('.wh-episodes').count()==0
    first.locator('.wh-summary-hit').click(position={'x':180,'y':50})
    page.wait_for_timeout(140)
    first=page.locator('.wh-season').first
    assert first.locator('.wh-episodes').count()==1
    assert first.locator('.wh-summary-hit').get_attribute('aria-expanded')=='true'
    episode=first.locator('.wh-episode-row').first
    assert episode.count()==1 and episode.get_attribute('role') is None
    before=episode.get_attribute('aria-pressed')
    episode.locator('.wh-episode-number').click()
    assert episode.get_attribute('aria-pressed')!=before
    episode.focus()
    episode.press('Space')
    assert episode.get_attribute('aria-pressed')==before
    assert first.locator('.wh-anime-title').count()==1
    first.locator('.wh-anime-title').click()
    page.wait_for_timeout(470)
    assert page.locator('#detail-back').count()==1
    page.locator('#detail-back').click()
    page.wait_for_timeout(470)
    first=page.locator('.wh-season').first
    assert first.locator('.wh-episodes').count()==1
    n=page.locator('.wh-season').count()
    first.locator('.wh-trash').click()
    assert page.locator('.wh-season').count()==n-1
    page.locator('[data-wh-undo-all]').click()
    assert page.locator('.wh-season').count()==n
    page.locator('[data-wh-exit]').click()
    page.wait_for_timeout(450)
    page.locator('[data-view="downloads"]').first.click()
    page.wait_for_timeout(500)
    assert page.locator('[data-download-toggle]').count()>0
    assert not errors,errors
    browser.close()
print('History row and hidden transfer regression tests passed')
