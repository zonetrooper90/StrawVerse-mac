#!/usr/bin/env python3
"""Small real-Chromium smoke gate for provisional lightweight-only Gallery HTML.

Creates an actual custom tag before checking its More Actions button, as
required by the unchanged Gallery Library UI. Both motion modes are retained.
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

path = Path(sys.argv[1])
raw = path.read_bytes()
assert b"data:image/png;base64," not in raw, "Preview embeds original artwork"
origin = "http://127.0.0.1:43891/gallery-preview/"
with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
    for width, height, motion in ((1440, 900, "no-preference"), (420, 850, "reduce")):
        page = browser.new_page(viewport={"width": width, "height": height}, reduced_motion=motion)
        errors = []
        page.on("pageerror", lambda exc: errors.append(str(exc)))
        page.route(origin + "**", lambda route: route.fulfill(
            status=200, content_type="text/html; charset=utf-8", body=raw
        ))
        page.goto(origin, wait_until="domcontentloaded")
        page.locator("#nav-library").click()
        page.wait_for_function(
            '() => state.view === "library" && !!document.querySelector("#newtag")'
            ' && !galleryStageTransition && !galleryStageFadeInProgress',
            timeout=9000,
        )
        page.locator("#newtag").click()
        page.locator("#tag-name").fill("Lightweight Preview Audit")
        page.locator("#create-tag").click()
        page.wait_for_function(
            '() => state.tag === "Lightweight Preview Audit" && !!document.querySelector("#tag-options")',
            timeout=9000,
        )
        opts = page.locator("#tag-options")
        opts.wait_for(state="visible")
        assert opts.locator(".g3-thinking-dot").count() == 3, "Three-dot More Actions SVG missing"
        assert opts.get_attribute("aria-expanded") == "false"
        opts.click()
        page.locator("#tag-options-menu").wait_for(state="visible")
        assert opts.get_attribute("aria-expanded") == "true"
        opts.click()
        page.locator("#tag-options-menu").wait_for(state="hidden")
        assert opts.get_attribute("aria-expanded") == "false"
        assert not errors, (width, motion, errors)
        page.close()
        print("PASS provisional lightweight custom-tag lifecycle", width, motion, flush=True)
    browser.close()
