#!/usr/bin/env python3
"""Verify user-approved exact rounded-corner fullscreen hover in both real Gallery modes.

Use Gallery's actual Player page and button. OS fullscreenchange events are
simulated to avoid depending on browser-window fullscreen support in CI.
"""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

FILES=(('full','gallery/Gallery-current.html'),('lightweight','gallery/Gallery-development.html'))
THEMES=('ocean','twilight','ember','slate','glacier','verdant')
PATHS=(
 ('tl','M4 8v-2a2 2 0 0 1 2 -2h2'),
 ('bl','M4 16v2a2 2 0 0 0 2 2h2'),
 ('tr','M16 4h2a2 2 0 0 1 2 2v2'),
 ('br','M16 20h2a2 2 0 0 0 2 -2v-2'),
)
ROOT='https://gallery-fullscreen-corners-audit.invalid/'

def pose(page):
    return page.locator('#fullscreen').evaluate("""el => ({
      expanded:el.dataset.g4Expanded,
      isFull:el.dataset.g4Fullscreen,
      label:el.getAttribute('aria-label'),
      corners:[...el.querySelectorAll('.g4-fullscreen-piece')].map(g=>{
        const m=new DOMMatrix(getComputedStyle(g).transform);
        return {x:m.e,y:m.f,duration:getComputedStyle(g).transitionDuration};
      }),
      button:(()=>{const r=el.getBoundingClientRect();return [r.x,r.y,r.width,r.height]})(),
      svg:(()=>{const r=el.querySelector('svg').getBoundingClientRect();return [r.x,r.y,r.width,r.height]})()
    })""")

def near(a,b,t=.2):
    return abs(a-b)<=t

def assert_pose(p,expanded,motion,label):
    assert p['expanded']==str(expanded).lower(),(label,p)
    movement=1.75 if expanded else 0
    for part,(sx,sy) in zip(p['corners'],((-1,-1),(-1,1),(1,-1),(1,1))):
        assert near(part['x'],sx*movement) and near(part['y'],sy*movement),(label,p)
        assert part['duration']==('0s' if motion=='reduce' else '0.3s'),(label,p)

def assert_stable_bounds(before,after,label):
    for field in ('button','svg'):
        assert all(near(a,b,.35) for a,b in zip(before[field],after[field])),(label,field,before,after)

with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,
      executable_path=os.environ.get('GALLERY_TEST_CHROMIUM') or None,
      args=['--no-sandbox','--disable-dev-shm-usage'])
    tested=0
    for mode,path in FILES:
        raw=Path(path).read_bytes()
        for motion in ('no-preference','reduce'):
            page=browser.new_page(viewport={'width':1100,'height':850},reduced_motion=motion)
            errors=[]
            page.on('pageerror',lambda error:errors.append(str(error)))
            page.route(ROOT+'**',lambda route:route.fulfill(status=200,
                content_type='text/html; charset=utf-8',body=raw))
            page.goto(ROOT,wait_until='domcontentloaded')
            # The detail Watch button mounts at the *midpoint* of Gallery's
            # coordinated route fade, before the 150ms incoming phase has
            # completed. Wait for the actual stage lifecycle to settle rather
            # than clicking during the incoming fade.
            page.locator('[data-detail]').first.click()
            page.wait_for_function(
              "()=>!!state.detailId&&!galleryStageFadeInProgress&&!galleryStageTransition",
              timeout=10000)
            page.wait_for_selector('.detail-actions [data-episode-action="watch"]',timeout=10000)
            page.locator('.detail-actions [data-episode-action="watch"]').first.click()
            page.wait_for_function(
              "()=>!!state.playback&&!!document.getElementById('fullscreen')&&!galleryStageFadeInProgress&&!galleryStageTransition",
              timeout=10000)
            # In this prototype an intentional no-media overlay owns pointer
            # input until a local file or *real* Player simulation is opened.
            # Use the same supported simulation control as existing Player CI,
            # never bypass the overlay with forced clicks or altered CSS.
            page.locator('#sf-player-demo-start').click()
            page.wait_for_function(
              "()=>sfPlayerDemo.active&&document.getElementById('player-empty').hidden",
              timeout=10000)
            page.wait_for_selector('#fullscreen .g4-fullscreen-piece',state='visible',timeout=10000)
            page.wait_for_timeout(420)
            button=page.locator('#fullscreen')
            assert button.get_attribute('aria-label')=='Toggle fullscreen'
            svg=button.locator('svg')
            assert svg.get_attribute('viewBox')=='0 0 24 24'
            assert svg.get_attribute('stroke-width')=='2'
            assert svg.get_attribute('width')==svg.get_attribute('height')=='21'
            assert button.locator('.g4-fullscreen-piece').count()==4
            for part,d in PATHS:
                assert button.locator('.g4-fullscreen-'+part+' path').get_attribute('d')==d,(mode,part)
            # Click handlers remain the real Gallery implementation; only the OS
            # fullscreen API/event is replaced for deterministic headless tests.
            page.evaluate("""()=>{
              window.__g4MockFull=false;
              const area=document.getElementById('player-area');
              Object.defineProperty(document,'fullscreenElement',{
                configurable:true,get:()=>window.__g4MockFull?area:null});
              area.requestFullscreen=()=>{
                window.__g4MockFull=true;
                document.dispatchEvent(new Event('fullscreenchange'));
                return Promise.resolve();
              };
              document.exitFullscreen=()=>{
                window.__g4MockFull=false;
                document.dispatchEvent(new Event('fullscreenchange'));
                return Promise.resolve();
              };
              document.dispatchEvent(new Event('fullscreenchange'));
            }""")
            for width in (1100,430):
                page.set_viewport_size({'width':width,'height':850})
                for theme in THEMES:
                    page.evaluate('t=>{document.body.dataset.theme=t;state.theme=t}',theme)
                    label=f'{mode}/{motion}/{width}/{theme}'
                    page.mouse.move(0,0)
                    page.wait_for_timeout(335 if motion=='no-preference' else 25)
                    rest=pose(page)
                    assert rest['isFull']=='false' and rest['label']=='Toggle fullscreen',label
                    assert_pose(rest,False,motion,label+' windowed rest')
                    button.hover()
                    page.wait_for_timeout(335 if motion=='no-preference' else 25)
                    outward=pose(page)
                    assert_pose(outward,True,motion,label+' hovered windowed')
                    assert_stable_bounds(rest,outward,label+' windowed geometry')
                    # While hovered, changing mode must never reset the corners.
                    button.click()
                    entered=pose(page)
                    assert entered['isFull']=='true',label
                    assert_pose(entered,True,motion,label+' fullscreen click continuity')
                    page.mouse.move(0,0)
                    page.wait_for_timeout(335 if motion=='no-preference' else 25)
                    assert_pose(pose(page),True,motion,label+' fullscreen resting expanded')
                    button.hover()
                    page.wait_for_timeout(335 if motion=='no-preference' else 25)
                    inward=pose(page)
                    assert_pose(inward,False,motion,label+' hovered fullscreen')
                    assert_stable_bounds(rest,inward,label+' fullscreen geometry')
                    button.click()
                    exited=pose(page)
                    assert exited['isFull']=='false',label
                    assert_pose(exited,False,motion,label+' windowed click continuity')
                    page.mouse.move(0,0)
                    page.wait_for_timeout(335 if motion=='no-preference' else 25)
                    assert_pose(pose(page),False,motion,label+' final resting')
                    # OS / Escape event, without clicking the button.
                    page.evaluate("""()=>{
                      window.__g4MockFull=true;
                      document.dispatchEvent(new Event('fullscreenchange'));
                    }""")
                    page.wait_for_timeout(335 if motion=='no-preference' else 25)
                    assert_pose(pose(page),True,motion,label+' OS enter')
                    page.evaluate("""()=>{
                      window.__g4MockFull=false;
                      document.dispatchEvent(new Event('fullscreenchange'));
                    }""")
                    page.wait_for_timeout(335 if motion=='no-preference' else 25)
                    assert_pose(pose(page),False,motion,label+' Escape/OS exit')
                    tested+=1
                print('PASS fullscreen corners',mode,motion,width,'six themes',flush=True)
            assert not errors,(mode,motion,errors)
            page.close()
    browser.close()
    assert tested==48,tested
    print('PASS exact SVG, outward/inward hover, click continuity, OS events, reduced motion, geometry, six themes, two widths, both HTMLs; 48 contexts',flush=True)
