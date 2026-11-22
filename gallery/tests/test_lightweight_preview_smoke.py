#!/usr/bin/env python3
"""Small real-Chromium smoke gate for provisional lightweight-only Gallery HTML."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

path = Path(sys.argv[1])
html = path.read_text(encoding="utf-8")
assert "data:image/png;base64," not in html, "Preview embeds artwork"
with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
    for width, height, motion in ((1440, 900, "no-preference"), (420, 850, "reduce")):
        page = browser.new_page(viewport={"width": width, "height": height}, reduced_motion=motion)
        errors = []
        page.on("pageerror", lambda exc: errors.append(str(exc)))
        page.goto("about:blank#recently-watched-legacy")
        page.set_content(html, wait_until="load")
        page.locator('.tab[data-view="library"]').wait_for(timeout=8000)
        page.locator('.tab[data-view="library"]').click()
        page.wait_for_function(
            '() => state.view === "library" && !galleryStageTransition && !galleryStageFadeInProgress',
            timeout=9000,
        )
        page.locator("#newtag").wait_for(state="visible", timeout=8000)
        assert page.locator("#tag-options").count() >= 1, "Library More Actions missing"
        assert not errors, (width, motion, errors)
        page.close()
        print("PASS provisional lightweight smoke", width, motion, flush=True)
    browser.close()
