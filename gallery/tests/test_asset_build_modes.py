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
        print(f"Testing {filename}", flush=True)
        page = browser.new_page(viewport={"width": 1600, "height": 950}, reduced_motion="no-preference")
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto((root / filename).as_uri(), wait_until="load")
        page.wait_for_timeout(240)
        page.locator("#settings").click()
        page.wait_for_function('() => document.body.classList.contains("settings-view") && !galleryStageTransition && !gallerySettingsOpening', timeout=6000)
        page.wait_for_timeout(260)
        page.locator('[data-settings-section="playback"]').click()
        page.wait_for_function("() => settingsLastSection === 'playback' && !document.querySelector('[data-settings-panel=playback]').hidden")
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
        try:
            page.wait_for_function("() => subtitleReducedMotion.matches && subtitleStages().every(s => Number(s.querySelector('.subtitle-stage-night').style.opacity) === 0)", timeout=6000)
        except Exception:
            print(page.evaluate("""() => ({
                media: subtitleReducedMotion.matches,
                freshMedia: matchMedia('(prefers-reduced-motion: reduce)').matches,
                hidden: document.hidden,
                frame: subtitleCycleFrame,
                layers: subtitleStages().map(s => ({
                    inline: s.querySelector('.subtitle-stage-night').style.opacity,
                    computed: getComputedStyle(s.querySelector('.subtitle-stage-night')).opacity
                }))
            })"""), errors, flush=True)
            raise
        assert not errors, errors
        geometries.append(geometry)
        page.close()
    for full, light in zip(*geometries):
        assert all(abs(a-b) <= 1 for a,b in zip(full, light)), geometries
    browser.close()
print("Both preview modes preserve geometry, synchronized day/night fade and reduced motion.")
