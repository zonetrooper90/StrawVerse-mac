#!/usr/bin/env python3
"""Check manual day/night controls in full and lightweight Gallery previews."""
from pathlib import Path
import os
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parents[1]

def assert_scene(page, night):
    expected = "1" if night else "0"
    layers = page.evaluate("""() => subtitleStages().map(s => ({
        inline: s.querySelector('.subtitle-stage-night').style.opacity,
        computed: getComputedStyle(s.querySelector('.subtitle-stage-night')).opacity
    }))""")
    assert layers and all(x == {"inline": expected, "computed": expected} for x in layers), layers
    scene = "night" if night else "day"
    assert page.locator('.sf-subtitle-scene-toggle').evaluate_all(
        "(els,scene) => els.every(e => e.dataset.active === scene && [...e.querySelectorAll('button')].every(b => b.getAttribute('aria-pressed') === String(b.dataset.subtitleScene === scene)))", scene
    )

def open_subtitles(page, filename):
    page.goto((root / filename).as_uri(), wait_until="load")
    page.wait_for_timeout(240)
    page.locator("#settings").click()
    page.wait_for_function('() => document.body.classList.contains("settings-view") && !galleryStageTransition && !gallerySettingsOpening')
    page.wait_for_timeout(260)
    page.locator('[data-settings-section="playback"]').click()
    page.wait_for_function("() => settingsLastSection === 'playback' && !document.querySelector('[data-settings-panel=playback]').hidden")
    page.locator('[data-playback-tab="subtitles"]').click()

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True, executable_path=os.environ.get("GALLERY_TEST_CHROMIUM") or None, args=["--no-sandbox"])
    geometries = {}
    for filename, light in (("Gallery-current.html", False), ("Gallery-development.html", True)):
        for reduced in ("no-preference", "reduce"):
            for width in (1600, 700, 420):
                page = browser.new_page(viewport={"width": width, "height": 950}, reduced_motion=reduced)
                errors = []
                page.on("pageerror", lambda e: errors.append(str(e)))
                open_subtitles(page, filename)
                main = page.locator("#subtitle-preview-stage")
                toggle = page.locator(".sf-subtitle-preview-heading .sf-subtitle-scene-toggle")
                wide = width == 1600
                assert toggle.is_visible() == wide
                assert_scene(page, False)
                assert page.locator("text=About subtitle rendering").count() == 0
                assert page.locator("#subtitle-saved-status").count() == 1
                assert page.locator("#settings-subtitle-appearance").is_visible()
                page.locator("#settings-subtitle-appearance").focus()
                assert page.locator("#settings-subtitle-appearance").evaluate("(e) => document.activeElement === e")
                assert toggle.locator("svg").count() == 2
                if wide:
                    assert page.locator(".sf-subtitle-full-title").inner_text() == "Subtitle preview"
                    a,b = toggle.bounding_box(), main.bounding_box()
                    assert abs(a["x"]+a["width"]-b["x"]-b["width"]) <= 2 and a["y"]+a["height"] <= b["y"]
                    toggle.locator('[data-subtitle-scene="night"]').hover()
                    assert_scene(page, False)
                    toggle.locator('[data-subtitle-scene="day"]').click()
                    assert_scene(page, False)
                    toggle.locator('[data-subtitle-scene="night"]').click()
                    assert_scene(page, True)
                    page.locator("#subtitle-expand-preview").click()
                else:
                    page.locator("#subtitle-compact-preview").click()
                expanded = page.locator("#subtitle-expanded-stage")
                expanded.wait_for()
                dialog_toggle = page.locator(".dialog-head .subtitle-expanded-header-controls .sf-subtitle-scene-toggle")
                scale = page.locator(".dialog-head #subtitle-actual-size")
                assert dialog_toggle.locator("svg").count() == 2
                assert scale.inner_text() == "100%"
                assert page.locator(".subtitle-expanded-toolbar, .subtitle-expanded-help").count() == 0
                assert page.locator(".subtitle-preview-dialog .dialog-scroll").evaluate("(e) => ['Top','Right','Bottom','Left'].every(s => getComputedStyle(e)['padding'+s] === '12px')")
                page.wait_for_timeout(260)
                assert scale.is_visible() == (not wide), expanded.bounding_box()
                if wide:
                    assert expanded.evaluate("(e) => [e.offsetWidth,e.offsetHeight]") == [1280,720]
                    assert dialog_toggle.locator('[aria-pressed="true"]').evaluate("(e) => e === document.activeElement")
                    page.set_viewport_size({"width": width, "height": 600})
                    scale.wait_for(state="visible")
                    assert expanded.evaluate("(e) => e.offsetWidth") < 1280
                header = page.locator(".subtitle-preview-dialog .dialog-head").bounding_box()
                a,b,c = scale.bounding_box(),dialog_toggle.bounding_box(),page.locator("#close-dialog").bounding_box()
                assert a["x"]+a["width"] <= b["x"]+1
                assert a["y"]+a["height"] <= header["y"]+header["height"]+1
                assert b["x"]+b["width"] <= header["x"]+header["width"]+1
                if width > 580:
                    assert b["x"]+b["width"] <= c["x"]+1
                scale.click()
                assert scale.inner_text() == "Fit" and scale.get_attribute("aria-pressed") == "true"
                assert expanded.evaluate("(e) => [e.offsetWidth,e.offsetHeight]") == [1280,720]
                assert scale.is_visible()
                scale.click()
                assert scale.inner_text() == "100%" and scale.get_attribute("aria-pressed") == "false"
                assert expanded.evaluate("(e) => e.offsetWidth") < 1280
                assert page.locator("#subtitle-expanded-viewport").evaluate("(e) => e.scrollLeft") == 0
                if wide:
                    scale.focus()
                    page.set_viewport_size({"width": width, "height": 950})
                    scale.wait_for(state="hidden")
                    assert dialog_toggle.locator('[aria-pressed="true"]').evaluate("(e) => e === document.activeElement")
                assert_scene(page, wide)
                other = dialog_toggle.locator('[data-subtitle-scene="' + ("day" if wide else "night") + '"]')
                selected = dialog_toggle.locator('[data-subtitle-scene="' + ("night" if wide else "day") + '"]')
                other.hover()
                assert_scene(page, wide)
                selected.click()
                assert_scene(page, wide)
                other.press("Space")
                assert_scene(page, not wide)
                selected.click()
                assert_scene(page, wide)
                # The selected option owns its gradient, with identical timing to Sub/Dub.
                page.wait_for_timeout(300)
                assert selected.evaluate("(e) => getComputedStyle(e,'::before').opacity") == "1"
                assert other.evaluate("(e) => getComputedStyle(e,'::before').opacity") == "0"
                if reduced == "reduce":
                    assert selected.evaluate("(e) => getComputedStyle(e,'::before').transitionDuration") == "0s"
                page.emulate_media(reduced_motion="reduce" if reduced == "no-preference" else "no-preference")
                page.wait_for_timeout(5500)
                assert_scene(page, wide)
                geometry = []
                for stage in (main, expanded):
                    for name, color in (("day", "rgb(213, 219, 226)"), ("night", "rgb(9, 27, 44)")):
                        layer = stage.locator(".subtitle-stage-" + name)
                        if light:
                            assert layer.get_attribute("src") is None
                            assert layer.evaluate("(e) => getComputedStyle(e).backgroundColor") == color
                        else:
                            layer.evaluate("(e) => e.decode()")
                            assert layer.get_attribute("src").startswith("data:image/png;base64,")
                            assert layer.evaluate("(e) => e.naturalWidth") > 0
                    if stage.is_visible():
                        rect = stage.bounding_box()
                        assert rect and abs(rect["width"] / rect["height"] - 16 / 9) < .02
                        geometry.append((rect["width"], rect["height"]))
                key = (reduced, width)
                if light:
                    assert len(geometry) == len(geometries[key])
                    assert all(abs(a-b) <= 1 for x,y in zip(geometry,geometries[key]) for a,b in zip(x,y))
                else:
                    geometries[key] = geometry
                page.locator("#close-dialog").click()
                page.wait_for_selector("#subtitle-expanded-stage", state="detached")
                assert_scene(page, wide)
                page.locator("#subtitle-reset").click()
                assert page.locator("#subtitle-saved-status").text_content() == "Subtitle preview settings reset to defaults."
                assert not errors, errors
                page.close()
                print(filename, reduced, width, "passed", flush=True)
    browser.close()
print("Both modes: manual scene switching, synchronization, geometry, keyboard and reduced motion passed.")
