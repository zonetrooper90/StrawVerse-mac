from playwright.sync_api import sync_playwright
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
import json
POINTER=json.loads((ROOT/'current.json').read_text(encoding='utf-8'))
P=ROOT / POINTER['folder'] / POINTER['source_name']
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path=__import__('os').environ.get('GALLERY_TEST_CHROMIUM') or None,args=['--no-sandbox','--disable-dev-shm-usage'])
    for size,reduced in [((1440,900),'no-preference'),((700,900),'no-preference'),((400,850),'no-preference'),((1440,900),'reduce')]:
        page=browser.new_page(viewport={'width':size[0],'height':size[1]},reduced_motion=reduced)
        errs=[];page.on('pageerror',lambda e:errs.append(str(e)))
        page.set_content(P.read_text(),wait_until="load")
        page.wait_for_timeout(120)
        assert page.locator('.demo-card').count()==5
        assert [e for e in page.locator('.scene').all_text_contents() if 'Discover' in e].__len__()==5
        page.locator('.toolbar [data-page="anime"]').click()
        page.wait_for_timeout(150)
        frame=page.evaluate('''() => [...document.querySelectorAll('.demo-card')].map(c=>({kind:c.dataset.style,layers:c.querySelectorAll('.scene').length,animations:c._animations.length,viewport:c.querySelector('.viewport').getBoundingClientRect().toJSON()}))''')
        if reduced=='no-preference':
            assert all(f['animations']==2 for f in frame),frame
            frames=page.locator('[data-style="hybrid"]').evaluate("card=>card._animations.map(a=>a.effect.getKeyframes())")
            getscale=lambda v:float(v.replace('scale(','').replace(')',''))
            assert abs(getscale(frames[0][-1]['transform'])-.994)<.00001,frames
            assert abs(getscale(frames[1][0]['transform'])-1.008)<.00001,frames
            assert all(f['layers']==2 for f in frame),frame
        else: assert all(f['animations']==0 for f in frame)
        page.wait_for_timeout(420)
        assert all(x=='anime' for x in page.locator('.scene').evaluate_all('(els)=>els.map(e=>e.dataset.scene)'))
        page.locator('.toolbar [data-page="settings"]').click();page.wait_for_timeout(510)
        assert all(x=='settings' for x in page.locator('.scene').evaluate_all('(els)=>els.map(e=>e.dataset.scene)'))
        page.locator('#back').click();page.wait_for_timeout(510)
        assert all(x=='anime' for x in page.locator('.scene').evaluate_all('(els)=>els.map(e=>e.dataset.scene)'))
        page.locator('#replay').click();page.wait_for_timeout(100)
        # replay should be anime from previous settings scene
        frames=page.locator('.demo-card').first.locator('.scene').evaluate_all('(els)=>els.map(e=>e.dataset.scene)')
        if reduced=='no-preference':assert frames==['settings','anime'],frames
        page.wait_for_timeout(460)
        assert all(x=='anime' for x in page.locator('.scene').evaluate_all('(els)=>els.map(e=>e.dataset.scene)'))
        page.locator('[data-focus="drift"]').click()
        assert page.locator('#lab').evaluate("el=>el.classList.contains('focus')")
        assert page.locator('.demo-card.focused').get_attribute('data-style')=='drift'
        page.locator('[data-focus="drift"]').click()
        assert not page.locator('#lab').evaluate("el=>el.classList.contains('focus')")
        page.locator('[data-focus="hybrid"]').click()
        assert page.locator('.demo-card.focused').get_attribute('data-style')=='hybrid'
        page.locator('[data-focus="hybrid"]').click()
        assert not page.locator('#lab').evaluate("el=>el.classList.contains('focus')")
        page.locator('#tour').click();page.wait_for_timeout(260)
        assert page.locator('#tour').get_attribute('aria-pressed')=='true'
        page.locator('#tour').click()
        assert page.locator('#tour').get_attribute('aria-pressed')=='false'
        if reduced=='no-preference' and size[0]==1440:
            page.locator('[data-focus="depth"]').click()
        print('PASSED',size,reduced,'errors',errs)
        assert not errs,errs
        page.close()
    browser.close()