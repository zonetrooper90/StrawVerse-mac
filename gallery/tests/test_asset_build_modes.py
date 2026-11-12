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
    # Compare the exact archived pre-cleanup baseline to this specific maintenance build.
    # Other future builds keep the regular functional tests without comparing to a stale visual baseline.
    import hashlib, base64, gzip, json, runpy
    if hashlib.sha256((root / "Gallery-current.html").read_bytes()).hexdigest() == "062e6a921b2f252c069c50159f1170ce4ef172bb5bc879b2871c6d0cef0dc5ae":
        old_dir = root / "checkpoints/2026-11-12-adaptive-subtitle-preview-controls"
        manifest = json.loads((old_dir / "manifest.json").read_text())
        chunks = []
        for part in manifest["parts"]:
            data = (old_dir / part["file"]).read_bytes()
            assert len(data) == part["encoded_chars"] and hashlib.sha256(data).hexdigest() == part["sha256"]
            chunks.append(data)
        compressed = base64.b64decode(b"".join(chunks), validate=True)
        assert len(compressed) == manifest["compressed_bytes"] and hashlib.sha256(compressed).hexdigest() == manifest["compressed_sha256"]
        old_full = gzip.decompress(compressed)
        assert len(old_full) == 6917688 and hashlib.sha256(old_full).hexdigest() == "6dbb668ae63dea26bd1ed03c70db20596c2b96f85a6466c428fdc3b9741aba55"
        builder = runpy.run_path(str(root / "tools/build-gallery.py"))
        old_light = old_full
        for name in ("day", "night"):
            asset = (root / "assets/subtitle-preview" / f"shrine-{name}.png").read_bytes()
            old_light = builder["replace_once"](old_light, b"data:image/png;base64," + base64.b64encode(asset), builder["COLORS"][name])
        for old, new in builder["LIGHT_PATCHES"]:
            old_light = builder["replace_once"](old_light, old, new)
        assert hashlib.sha256(old_light).hexdigest() == "51c12e00ff5e2b7f2b92c625a1076b22c58d5c708bd4770d0ba8ba444a9580e4"
        themes = ("ocean", "twilight", "ember", "slate", "glacier", "verdant")

        def theme_snapshots(page, selector):
            result = {}
            for theme in themes:
                # Sample the exact supported CSS theme scope, independently of timing in navigation.
                page.evaluate("(t) => {state.theme=t;document.body.dataset.theme=t}", theme)
                result[theme] = page.evaluate("""(selector) => {
                    const props=['display','visibility','color','backgroundColor','backgroundImage','borderColor','borderRadius','boxShadow','fontSize','fontWeight','width','height','padding','margin','gap','scrollbarColor','scrollbarWidth','colorScheme','animationName','animationDuration','transitionDuration'];
                    const vars=['--window','--surface','--raised','--hover','--line','--ink','--muted','--accent','--accent-ink','--tab','--strong','--player-remaining','--nav-bg','--nav-active-a','--nav-active-b'];
                    const body=getComputedStyle(document.body);
                    const nodes=[...document.querySelectorAll(selector)];
                    if(!nodes.length)throw Error('Missing comparison nodes: '+selector);
                    return {vars:vars.map(v=>body.getPropertyValue(v)),nodes:nodes.map(e=>{
                        const c=getComputedStyle(e);
                        const pseudo=['::before','::after','::-webkit-scrollbar','::-webkit-scrollbar-track','::-webkit-scrollbar-thumb'].map(p=>{
                            const x=getComputedStyle(e,p);
                            return [x.color,x.backgroundColor,x.backgroundImage,x.borderColor,x.borderRadius,x.width];
                        });
                        return [e.tagName,e.id,props.map(p=>c[p]),pseudo];
                    })};
                }""", selector)
            return result

        def cleanup_snapshot(source, width):
            page = browser.new_page(viewport={"width":width,"height":950}, reduced_motion="reduce")
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            try:
                page.set_content(source.decode("utf-8"), wait_until="domcontentloaded")
                page.wait_for_timeout(240)
                page.mouse.move(0,0)
                nav = theme_snapshots(page, "body,.app,.tabs,.tabs>.tab")
                page.locator("[data-detail]").first.click()
                page.wait_for_timeout(350)
                page.locator('.detail-actions [data-episode-action="watch"]').first.click()
                page.wait_for_selector("#player-area")
                page.wait_for_timeout(180)
                page.mouse.move(0,0)
                player = theme_snapshots(page, "#player-area,#player-area .player-icon,#player-area .player-main-action,#player-area input")
                page.evaluate("setView('discover')")
                page.wait_for_function("() => !state.playback && !galleryStageTransition")
                page.locator("#settings").click()
                page.wait_for_function('() => document.body.classList.contains("settings-view") && !galleryStageTransition && !gallerySettingsOpening')
                page.locator('[data-settings-section="playback"]').click()
                page.locator('[data-playback-tab="subtitles"]').click()
                page.evaluate("showExpandedSubtitlePreview()")
                page.wait_for_selector("#subtitle-expanded-stage")
                page.wait_for_timeout(180)
                page.mouse.move(0,0)
                dialog = theme_snapshots(page, ".dialog,.dialog-scroll,.dialog-head,.dialog-head button,#subtitle-expanded-stage")
                assert not errors, errors
                return {"navigation":nav,"player":player,"dialog":dialog}
            finally:
                page.close()

        for filename, old in (("Gallery-current.html", old_full), ("Gallery-development.html", old_light)):
            new = (root / filename).read_bytes()
            for width in (1600,700):
                before, after = cleanup_snapshot(old,width), cleanup_snapshot(new,width)
                for surface in before:
                    for theme in themes:
                        assert before[surface][theme] == after[surface][theme], (filename,width,surface,theme)
                print(filename, width, "all six themes: exact sampled computed styles match baseline (navigation, Player, expanded dialog)", flush=True)
    # C3: verify all 14 affected selectors with the actual old and new stylesheet,
    # including exact breakpoint edges and a representative hover state.
    if hashlib.sha256((root / "Gallery-current.html").read_bytes()).hexdigest() == "7183e66611050352cb35fbc25f361f8f19f5c1821231aa72496f81181ad9749e":
        old_dir = root / "checkpoints/2026-11-12-retired-theme-css"
        manifest = json.loads((old_dir / "manifest.json").read_text())
        chunks = []
        for part in manifest["parts"]:
            data = (old_dir / part["file"]).read_bytes()
            assert len(data) == part["encoded_chars"] and hashlib.sha256(data).hexdigest() == part["sha256"]
            chunks.append(data)
        compressed = base64.b64decode(b"".join(chunks), validate=True)
        assert len(compressed) == manifest["compressed_bytes"] and hashlib.sha256(compressed).hexdigest() == manifest["compressed_sha256"]
        old_full = gzip.decompress(compressed)
        assert len(old_full) == 6915281 and hashlib.sha256(old_full).hexdigest() == "062e6a921b2f252c069c50159f1170ce4ef172bb5bc879b2871c6d0cef0dc5ae"
        def stylesheet(raw):
            return raw.split(b"<style>", 1)[1].split(b"</style>", 1)[0].decode("utf-8")
        new_css = stylesheet((root / "Gallery-current.html").read_bytes())
        assert new_css == stylesheet((root / "Gallery-development.html").read_bytes())
        old_css = stylesheet(old_full)
        # Isolated representative markup also covers legacy selectors not present
        # in current screens; real UI navigation is tested by the existing suites.
        fixture = """
        <div class="collection-panel" data-c3="collection">Collection</div>
        <div class="detail-hero" data-c3="hero"><div>Cover</div><div>Details</div></div>
        <div class="episode-item"><div class="episode-copy" data-c3="episode">Episode</div></div>
        <div class="episode-toolbar"><div class="episode-heading"><h2 data-c3="heading">Episodes</h2></div></div>
        <div class="episode-availability"><span class="availability-label" data-c3="availability">Available</span><span class="episode-shown" data-c3="shown">1 shown</span></div>
        <div class="settings-page-head"><h1 data-c3="settings-title">Settings</h1></div>
        <button class="settings-back" data-c3="back" style="position:fixed;top:4px;left:4px;z-index:99999"><span data-c3="back-label">Back</span></button>
        <div class="about-identity-copy" data-c3="identity">Gallery</div>
        <div class="settings-font-tile"><div class="settings-font-top" data-c3="font">Font</div></div>
        <div id="playback-subtitles-pane" data-c3="subtitles">Subtitle preview</div>
        <div class="sf-dl-episode-row"><div class="sf-dl-episode-status" data-c3="status">Ready</div><div class="sf-dl-episode-track" data-c3="track">Progress</div></div>
        """
        widths = (1600, 761, 760, 751, 750, 571, 570, 531, 530, 441, 440, 371, 370, 340)
        themes = ("ocean", "twilight", "ember", "slate", "glacier", "verdant")
        def snap(pg):
            return pg.evaluate("""() => {
                const props=['paddingTop','paddingRight','paddingBottom','paddingLeft','gridTemplateColumns','rowGap','columnGap','minWidth','fontSize','lineHeight','marginTop','marginRight','marginBottom','marginLeft','display','alignItems','whiteSpace','transitionProperty','transitionDuration','transitionDelay','color','backgroundColor','flexGrow','flexShrink','flexBasis','containerType','gridArea'];
                return [...document.querySelectorAll('[data-c3]')].map(e=>{
                    const c=getComputedStyle(e);return [e.dataset.c3,...props.map(p=>c[p])];
                });
            }""")
        def settle(pg, hovered):
            # Force style resolution, then wait for the actual finite CSS transitions.
            pg.evaluate("() => {for(const e of document.querySelectorAll('[data-c3]'))getComputedStyle(e).color}")
            pg.wait_for_function("""(hovered) => {
                const back=document.querySelector('[data-c3="back"]');
                if(back.matches(':hover')!==hovered)return false;
                return [...document.querySelectorAll('[data-c3]')].every(e=>e.getAnimations().every(a=>a.playState!=='running' && !a.pending));
            }""",arg=hovered,timeout=5000)
        for motion in ("no-preference", "reduce"):
            for theme in themes:
                # Fresh pages per theme avoid a previous theme's hover/transition state.
                a=browser.new_page(viewport={"width":1600,"height":950},reduced_motion=motion)
                b=browser.new_page(viewport={"width":1600,"height":950},reduced_motion=motion)
                try:
                    for pg,css in ((a,old_css),(b,new_css)):
                        pg.mouse.move(0,0)
                        pg.set_content('<!doctype html><html><head><style>'+css+'</style></head><body data-theme="'+theme+'">'+fixture+'</body></html>')
                        pg.mouse.move(0,0)
                    for width in widths:
                        for pg in (a,b):
                            pg.set_viewport_size({"width":width,"height":950})
                        for pg in (a,b):
                            settle(pg,False)
                        before,after=snap(a),snap(b)
                        assert len(before)==14 and before==after,(motion,theme,width,before,after)
                    for pg in (a,b):
                        pg.set_viewport_size({"width":440,"height":950})
                        pg.locator('[data-c3="back"]').hover()
                    for pg in (a,b):
                        settle(pg,True)
                    assert snap(a)==snap(b),(motion,theme,"hover",snap(a),snap(b))
                finally:
                    a.close()
                    b.close()
            print("C3 exact duplicate cascade comparison passed:",motion,"all six themes, 14 widths, settled hover and 14 representative elements",flush=True)
    browser.close()
print("Both modes: manual scene switching, synchronization, geometry, keyboard and reduced motion passed.")
