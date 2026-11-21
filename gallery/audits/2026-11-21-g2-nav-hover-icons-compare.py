#!/usr/bin/env python3
"""G2: compare exact reviewed navigation SVGs and hover motion in both builds."""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT="https://gallery-g2-hover-audit.invalid/"
FILES=(("full","gallery/Gallery-current.html"),("lightweight","gallery/Gallery-development.html"))
THEMES=("ocean","twilight","ember","slate","glacier","verdant")
GET_BOUNDS="""() => ['discover','library','downloads'].map(id=>{
 const el=document.getElementById('nav-'+id),svg=el.querySelector('svg');
 const a=el.getBoundingClientRect(),b=svg.getBoundingClientRect();
 return {id,button:[a.x,a.y,a.width,a.height],svg:[b.x,b.y,b.width,b.height]};
})"""
def scalar(page,selector,axis):
    return page.locator(selector).evaluate(
      """(el,axis)=>{let m=new DOMMatrix(getComputedStyle(el).transform);return m[axis]}""",axis)
def near(a,b,tol=.13):
    return abs(a-b)<tol
def exact_paths(page,label):
    assert page.locator('#nav-discover .g2-compass-needle').get_attribute('d')=='m16 8-3 5-5 3 3-5 5-3z',label
    assert page.locator('#nav-discover circle').get_attribute('r')=='9',label
    assert page.locator('#nav-library .g2-library-first').get_attribute('d')=='M6 5v14',label
    assert page.locator('#nav-library .g2-library-second').get_attribute('d')=='M2 7v10',label
    box=page.locator('#nav-library rect')
    for key,value in (('x','10'),('y','3'),('width','12'),('height','18'),('rx','2')):
        assert box.get_attribute(key)==value,(label,key)
    assert page.locator('#nav-library svg').get_attribute('stroke-width')=='2',label
    assert page.locator('#nav-downloads .g2-download-arrow path').get_attribute('d')=='M12 2v13m-5-5 5 5 5-5',label
    assert page.locator('#nav-downloads svg>path').get_attribute('d')=='M4 18v3h16v-3',label
    assert page.locator('#nav-discover svg').get_attribute('viewBox')=='0 0 24 24',label
    assert page.locator('#nav-library svg').get_attribute('viewBox')=='0 0 24 24',label
    assert page.locator('#nav-downloads svg').get_attribute('viewBox')=='0 0 24 24',label

def geometry(before,after,label):
    assert len(before)==len(after)==3,label
    for b,a in zip(before,after):
        assert b['id']==a['id'],label
        for old,new in zip(b['button']+b['svg'],a['button']+a['svg']):
            assert abs(old-new)<.75,(label,b,a)

with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,
      executable_path=os.environ.get('GALLERY_TEST_CHROMIUM') or None,
      args=['--no-sandbox','--disable-dev-shm-usage'])
    cases=0
    for mode,path in FILES:
        raw=Path(path).read_bytes()
        for motion in ('no-preference','reduce'):
            normal=motion=='no-preference'
            page=browser.new_page(viewport={'width':1100,'height':850},reduced_motion=motion)
            errors=[]
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.route(ROOT+'**',lambda route:route.fulfill(
              status=200,content_type='text/html; charset=utf-8',body=raw))
            page.goto(ROOT,wait_until='domcontentloaded')
            page.wait_for_function("()=>!!document.querySelector('#nav-library .g2-library-first')")
            assert page.locator('#header-watch-history .g1-history-rim').count()==1
            assert page.locator('#settings .g1-settings-knob').count()==2
            for width in (1100,390):
                page.set_viewport_size({'width':width,'height':850})
                for theme in THEMES:
                    page.evaluate("t=>document.body.dataset.theme=t",theme)
                    label=f"{mode}/{motion}/{width}px/{theme}"
                    exact_paths(page,label)
                    before=page.evaluate(GET_BOUNDS)
                    page.locator('#nav-discover').hover()
                    page.wait_for_timeout(860 if normal else 30)
                    a=scalar(page,'#nav-discover .g2-compass-needle','a')
                    b=scalar(page,'#nav-discover .g2-compass-needle','b')
                    assert near(a,0,.07) and near(b,-1,.07) if normal else near(a,1,.07) and near(b,0,.07),(label,a,b)
                    geometry(before,page.evaluate(GET_BOUNDS),label+' Discover')
                    page.mouse.move(0,0)
                    page.wait_for_timeout(860 if normal else 30)
                    assert near(scalar(page,'#nav-discover .g2-compass-needle','a'),1,.07),label
                    assert near(scalar(page,'#nav-discover .g2-compass-needle','b'),0,.07),label
                    page.locator('#nav-downloads').hover()
                    page.wait_for_timeout(710 if normal else 30)
                    y=scalar(page,'#nav-downloads .g2-download-arrow','f')
                    assert near(y,2.25,.12) if normal else near(y,0,.07),(label,y)
                    geometry(before,page.evaluate(GET_BOUNDS),label+' Downloads')
                    page.mouse.move(0,0)
                    page.wait_for_timeout(700 if normal else 25)
                    assert near(scalar(page,'#nav-downloads .g2-download-arrow','f'),0,.07),label
                    page.locator('#nav-library').hover()
                    page.wait_for_timeout(710 if normal else 35)
                    for path_name in ('first','second'):
                        sel='#nav-library .g2-library-'+path_name
                        x=scalar(page,sel,'e')
                        opacity=float(page.locator(sel).evaluate('el=>getComputedStyle(el).opacity'))
                        assert near(x,0,.1) and near(opacity,1,.02),(label,path_name,x,opacity)
                    geometry(before,page.evaluate(GET_BOUNDS),label+' Library')
                    page.mouse.move(0,0)
                    page.wait_for_timeout(45)
                    for path_name in ('first','second'):
                        assert near(scalar(page,'#nav-library .g2-library-'+path_name,'e'),0,.1),label
                    cases+=1
                print('PASS G2 all themes',mode,motion,width,flush=True)
            for tab in ('library','downloads','discover'):
                page.locator('#nav-'+tab).click()
                page.wait_for_function('(tab)=>state.view===tab',arg=tab,timeout=15000)
                assert page.locator('#nav-'+tab).evaluate("el=>el.classList.contains('active')")
            assert not errors,(mode,motion,errors)
            page.close()
    browser.close()
    print('PASS G2 exact reviewed SVG paths, hover, release, responsive geometry, all themes, reduced motion and native tab clicks:',cases,'contexts',flush=True)
