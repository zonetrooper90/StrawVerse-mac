#!/usr/bin/env python3
"""Verify A+C timings, bidirectional Settings, source deep link and reduced motion."""
from pathlib import Path
import os, sys
from playwright.sync_api import sync_playwright

source = Path(sys.argv[1]).read_text(encoding="utf-8")
assert "::view-transition-old(gallery-stage){animation:gallery-stage-leave .45s" in source
assert "::view-transition-new(gallery-stage){animation:gallery-stage-arrive .45s" in source
assert "48%{opacity:.83;transform:scale(.998)}" in source
assert "100%{opacity:.05;transform:scale(.994)}" in source
assert "0%{opacity:.05;transform:scale(1.008)}" in source
assert "48%{opacity:.60;transform:scale(1.004)}" in source
assert "function showSettings(afterOpen=null)" in source
assert "function galleryOpenSettingsNow()" in source
assert "function openSourceManagerFromDiscover()" in source

checks = []

def rec(label, valid, detail=None):
    checks.append((label, bool(valid), detail))
    print(("PASS" if valid else "FAIL"), label, detail or "")

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        executable_path=os.environ.get("GALLERY_TEST_CHROMIUM") or None,
        args=["--no-sandbox", "--disable-dev-shm-usage"],
    )
    for width, height, reduced in (
        (1440, 900, "no-preference"),
        (620, 750, "no-preference"),
        (1440, 900, "reduce"),
    ):
        page = browser.new_page(viewport={"width": width, "height": height}, reduced_motion=reduced)
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.set_content(source, wait_until="load")
        page.wait_for_timeout(350)
        print("CHECKING", width, height, reduced)
        def status():
            return page.evaluate("""() => ({
                view:state.view,
                detail:state.detailId,
                settings:document.body.classList.contains('settings-view'),
                section:settingsLastSection,
                stageActive:!!galleryStageTransition,
                stageName:workspace.style.viewTransitionName,
                screensDisabled:screen.inert,
                animationNames:[...document.getAnimations()].map(x=>x.animationName).filter(Boolean),
                headerCount:document.querySelectorAll('.top').length,
                route:document.querySelector('#screen')?.dataset.surfaceKey
            })""")
        rec("View Transitions API available", page.evaluate("typeof document.startViewTransition==='function'"))
        page.locator('[data-detail]').first.click()
        page.wait_for_timeout(130)
        now = status()
        rec("Anime opens", now["detail"] is not None, now)
        if reduced == "no-preference":
            rec("A+C anime capture active", now["stageActive"], now)
            rec("Workspace only named for snapshot", now["stageName"] == "gallery-stage", now)
            rec("Common header remains outside snapshot", now["headerCount"] == 1)
        else:
            rec("Reduced motion skips A+C capture", not now["stageActive"] and not now["stageName"], now)
        page.wait_for_timeout(550)
        rec("Transition finishes and cleans up", not status()["stageActive"] and not status()["stageName"], status())
        page.locator('#settings').click()
        page.wait_for_timeout(130)
        now = status()
        rec("Settings opens from Anime", now["settings"] and now["screensDisabled"], now)
        if reduced == "no-preference":
            rec("A+C Settings entrance active", now["stageActive"] and now["stageName"] == "gallery-stage", now)
        else:
            rec("Reduced Settings entrance instantaneous", not now["stageActive"], now)
        page.wait_for_timeout(550)
        page.locator('#settings-back').click()
        page.wait_for_timeout(130)
        now = status()
        rec("Settings closes preserving Anime", not now["settings"] and now["detail"] is not None and not now["screensDisabled"], now)
        if reduced == "no-preference":
            rec("A+C Settings return active", now["stageActive"] and now["stageName"] == "gallery-stage", now)
        else:
            rec("Reduced Settings return instantaneous", not now["stageActive"], now)
        page.wait_for_timeout(550)
        rec("Settings return cleans up", not status()["stageActive"] and not status()["stageName"], status())
        page.locator('#detail-back').click()
        page.wait_for_timeout(550)
        rec("Anime returns to Discover", status()["detail"] is None and status()["view"] == "discover")
        page.evaluate("openSourceManagerFromDiscover()")
        # The View Transitions callback runs after Chromium captures the outgoing
        # page. Wait on the actual destination, not an arbitrary frame budget.
        page.wait_for_function("() => document.body.classList.contains('settings-view') && settingsLastSection==='sources'", timeout=7000)
        rec("Sources deep link survives asynchronous capture", status()["settings"] and status()["section"] == "sources", status())
        page.wait_for_timeout(550)
        page.locator('#settings-back').click()
        page.wait_for_timeout(550)
        rec("Sources exits to Discover", not status()["settings"] and status()["view"] == "discover", status())
        rec("No JavaScript errors", not errors, errors[:5])
        page.close()
    browser.close()
failed = [r for r in checks if not r[1]]
print("A+C TEST RESULT", len(checks), "checks,", len(failed), "failures", failed)
if failed:
    sys.exit(1)
