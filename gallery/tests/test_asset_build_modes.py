#!/usr/bin/env python3
"""Check original and lightweight preview layers, geometry and synchronization."""
from pathlib import Path
import os
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parents[1]
with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True, executable_path=os.environ.get("GALLERY_TEST_CHROMIUM") or None, args=["--no-sandbox"])
    geometries = []
    for filename, light in (("Gallery-current.html", False), ("Gallery-development.html", True)):
        page = browser.new_page(viewport={"width": 1600, "height": 950})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.set_content((root / filename).read_text(encoding="utf-8"), wait_until="domcontentloaded")
        page.locator("#settings").click()
        page.wait_for_function('() => document.body.classList.contains("settings-view") && !galleryStageTransition && !gallerySettingsOpening', timeout=6000)
        page.locator('[data-settings-section="playback"]').click()
        page.locator('[data-playback-tab="subtitles"]').click()
        page.wait_for_selector("#subtitle-preview-stage")
        page.evaluate("showExpandedSubtitlePreview()")
        page.wait_for_selector("#subtitle-expanded-stage")
        geometry = []
        for selector in ("#subtitle-preview-stage", "#subtitle-expanded-stage"):
            stage = page.locator(selector)
            for name, color in (("day", "rgb(213, 219, 226)"), ("night", "rgb(9, 27, 44)")):
                layer = stage.locator(".subtitle-stage-" + name)
                if light:
                    assert layer.get_attribute("src") is None, "Lightweight preview must not request artwork"
                    assert layer.evaluate("(e) => getComputedStyle(e).backgroundColor") == color
                else:
                    layer.evaluate("(e) => e.decode()")
                    assert layer.get_attribute("src").startswith("data:image/png;base64,")
                    assert layer.evaluate("(e) => e.naturalWidth") > 0
            rect = stage.bounding_box()
            assert rect and abs(rect["width"] / rect["height"] - 16 / 9) < .02
            geometry.append((rect["width"], rect["height"]))
        # Paint both layers at the exact midpoint of the approved fade in one JS task.
        opacities = page.evaluate("""() => {
          paintSubtitleNight(subtitleCycleStartTime + SUBTITLE_FADE_MS / 2);
          return subtitleStages().map(s => s.querySelector('.subtitle-stage-night').style.opacity);
        }""")
        assert opacities == ["0.5", "0.5"], opacities
        page.emulate_media(reduced_motion="reduce")
        page.wait_for_function("() => subtitleStages().every(s => Number(s.querySelector('.subtitle-stage-night').style.opacity) === 0)")
        assert not errors, errors
        geometries.append(geometry)
        page.close()
    for full, light in zip(*geometries):
        assert all(abs(a-b) <= 1 for a,b in zip(full, light)), geometries
    browser.close()
print("Both preview modes preserve geometry, synchronized day/night fade and reduced motion.")
