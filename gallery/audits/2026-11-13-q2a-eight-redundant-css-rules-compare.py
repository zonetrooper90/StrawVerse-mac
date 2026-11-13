#!/usr/bin/env python3
"""Q2-A publication gate: exact HTML diff and real-DOM before/after comparison."""
import hashlib
import re
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE="41383b618be8c7dc92511a8d7370e359db3e9465"
BLOCKS=[".demo-download-footer .tip{margin:0}",".player-controls .controls-middle{justify-content:center}",".player-episode-nav .btn{font-size:12px;min-width:0;max-width:100%}",".settings-panel-head .description{font-size:13px;line-height:1.5}",".settings-back{padding:8px}","body[data-theme] .sf-dl-episode-name{grid-area:name}","body[data-theme] .sf-dl-episode-control{grid-area:control}","body[data-theme] .sf-dl-episode-percent{grid-area:percent}"]
FILES=[["gallery/Gallery-current.html","6d62486f67526e5e310d08bf2cbcbf14f7a466e9df79edf8b562b6b3b057881d"],["gallery/Gallery-development.html","81ae67aecd5505f004e9ce9fa3c66cd53241e2e76e74f27b68bab11782dff49d"]]
THEMES=('ocean','twilight','ember','slate','glacier','verdant')
WIDTHS=(1440,761,760,721,720,561,560,441,440,391,390,340)
INTERACTION_WIDTHS=(1440,760,440,390)
ROUTES={
    'downloads': {
        'targets': ['.demo-download-footer .tip','.sf-dl-episode-name','.sf-dl-episode-control','.sf-dl-episode-percent'],
        'scope': '.sf-dl-list',
        'interaction': '.sf-dl-card.is-expanded .sf-dl-control-button:visible',
    },
    'player': {
        'targets': ['.player-controls .controls-middle','.player-episode-nav .btn'],
        'scope': '.playback-page',
        'interaction': '.player-episode-nav .btn:visible:not([disabled])',
    },
    'settings': {
        'targets': ['.settings-panel-head .description','.settings-back'],
        'scope': '.settings-page',
        'interaction': '#settings-back',
    },
}
STYLE=re.compile(br'<style>(.*?)</style>',re.S)
def unpack(html):
    matches=list(STYLE.finditer(html))
    assert len(matches)==1
    m=matches[0]
    return html[:m.start(1)],m.group(1),html[m.end(1):]
def exact_pair(path,expected_sha):
    before=subprocess.check_output(['git','show',f'{BASE}:{path}'])
    assert hashlib.sha256(before).hexdigest()==expected_sha,path
    after=Path(path).read_bytes()
    pre,css,post=unpack(before)
    candidate_pre,candidate_css,candidate_post=unpack(after)
    assert pre==candidate_pre and post==candidate_post,('Non-CSS bytes changed',path)
    expected=css
    for block in BLOCKS:
        raw=block.encode()
        assert expected.count(raw)==1,block
        expected=expected.replace(raw,b'',1)
    assert expected==candidate_css,('Unexpected CSS diff',path)
    print('PASS: exact eight-rule deletion, all other HTML bytes unchanged',path,len(css)-len(candidate_css),flush=True)
    return after.decode('utf-8'),css.decode('utf-8'),candidate_css.decode('utf-8')

# Both style versions are evaluated on the same mounted app DOM in the same
# JS task. Compare every enumerable computed property, pseudo-element styles,
# box geometry, and the sizes of the immediate layout ancestors. We do not
# disable CSS animations/transitions or replace actual app markup with fixtures.
COMPARE=r'''({targets,scope}) => {
  const style=document.querySelector('head style') || document.querySelector('style');
  if(!style) throw Error('Missing application stylesheet');
  const candidate=window.__q2candidate, baseline=window.__q2baseline;
  if(style.textContent!==candidate) throw Error('Unexpected active stylesheet');
  const root=document.querySelector(scope);
  if(!root) throw Error('Missing route scope '+scope);
  const nodes=new Set();
  const counts={};
  for(const sel of targets){
    const matches=[...root.querySelectorAll(sel)];
    counts[sel]=matches.length;
    if(!matches.length) throw Error('Missing target '+sel);
    for(const el of matches){
      nodes.add(el);
      for(const child of el.querySelectorAll('*')) nodes.add(child);
      if(el.parentElement) nodes.add(el.parentElement);
    }
  }
  function snapshot(){
    return Array.from(nodes,el=>{
      const r=el.getBoundingClientRect(), cs=getComputedStyle(el);
      const all=Array.from(cs,p=>[p,cs.getPropertyValue(p)]);
      const pseudo=['::before','::after'].map(p=>{
        const s=getComputedStyle(el,p);
        return [s.content,Array.from(s,k=>[k,s.getPropertyValue(k)])];
      });
      return {tag:el.tagName,cls:el.getAttribute('class'),all,pseudo,
        rect:[r.x,r.y,r.width,r.height,el.clientWidth,el.clientHeight,el.scrollWidth,el.scrollHeight],
        hovered:el.matches(':hover'),focused:el.matches(':focus-visible')};
    });
  }
  try {
    style.textContent=baseline;
    const a=snapshot();
    style.textContent=candidate;
    const b=snapshot();
    for(let i=0;i<a.length;i++){
      const x=a[i], y=b[i];
      for(let j=0;j<x.all.length;j++){
        if(x.all[j][0]!==y.all[j][0] || x.all[j][1]!==y.all[j][1])
          return {counts,node:i,tag:x.tag,cls:x.cls,property:x.all[j][0],before:x.all[j][1],after:y.all[j][1]};
      }
      if(JSON.stringify(x.pseudo)!==JSON.stringify(y.pseudo))
        return {counts,node:i,tag:x.tag,cls:x.cls,property:'pseudo computed style'};
      if(x.rect.some((v,j)=>typeof v==='number'&&Math.abs(v-y.rect[j])>0.02))
        return {counts,node:i,tag:x.tag,cls:x.cls,property:'geometry',before:x.rect,after:y.rect};
      if(x.hovered!==y.hovered || x.focused!==y.focused)
        return {counts,node:i,tag:x.tag,cls:x.cls,property:'interaction state'};
    }
    return {counts,nodes:a.length};
  } finally {
    if(style.textContent!==candidate) style.textContent=candidate;
  }
}'''
def stable(page):
    page.wait_for_function('() => !galleryStageTransition && !galleryStageFadeInProgress',timeout=6000)
    page.wait_for_timeout(500)
def enter(page,route):
    if route=='downloads':
        page.locator('.tab[data-view="downloads"]').click()
        page.wait_for_function('() => state.view==="downloads"')
        stable(page)
        for group in page.locator('.sf-dl-card').all():
            if not group.evaluate('(e)=>e.classList.contains("is-expanded")'):
                group.locator('[data-download-toggle]').click()
        page.wait_for_timeout(450)
        assert page.locator('.sf-dl-card.is-expanded').count()>0
    elif route=='player':
        page.locator('[data-detail]').first.click()
        stable(page)
        page.locator('.detail-actions [data-episode-action="watch"]').first.click()
        page.wait_for_selector('#player-area')
        stable(page)
    else:
        page.locator('#settings').click()
        page.wait_for_function('() => document.body.classList.contains("settings-view") && !gallerySettingsOpening')
        stable(page)

def run(browser,path,html,baseline,candidate):
    checks=0
    for motion in ('no-preference','reduce'):
        for route,config in ROUTES.items():
            page=browser.new_page(viewport={'width':1440,'height':950},reduced_motion=motion)
            errors=[]
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.set_content(html,wait_until='domcontentloaded')
            page.wait_for_selector('#wh-view-history')
            enter(page,route)
            # Keep both full stylesheets in page memory, not in tracked files.
            page.evaluate('''({baseline,candidate})=>{
                window.__q2baseline=baseline;window.__q2candidate=candidate;
                if(document.querySelector('style').textContent!==candidate)
                    throw Error('Candidate stylesheet does not match actual DOM');
            }''',{'baseline':baseline,'candidate':candidate})
            def compare(theme,width,interaction):
                nonlocal checks
                result=page.evaluate(COMPARE,{'targets':config['targets'],'scope':config['scope']})
                assert 'property' not in result,(path,route,motion,theme,width,interaction,result)
                assert result['nodes']>0,result
                checks+=1
            for theme in THEMES:
                page.evaluate('(theme)=>{state.theme=theme;document.body.dataset.theme=theme;}',theme)
                page.wait_for_timeout(300)
                for width in WIDTHS:
                    page.set_viewport_size({'width':width,'height':950})
                    page.mouse.move(0,0)
                    page.evaluate('()=>document.activeElement?.blur()')
                    page.wait_for_timeout(100)
                    compare(theme,width,'rest')
                    if width in INTERACTION_WIDTHS:
                        target=page.locator(config['interaction']).first
                        assert target.count() and target.is_visible(),(route,width,'interaction target missing')
                        target.hover(timeout=5000)
                        page.wait_for_timeout(280)
                        assert target.evaluate('(e)=>e.matches(":hover")'),(route,width,'hover not achieved')
                        compare(theme,width,'hover')
                        page.mouse.move(0,0)
                        page.keyboard.press('Tab')
                        target.focus()
                        page.wait_for_timeout(280)
                        assert target.evaluate('(e)=>e.matches(":focus-visible")'),(route,width,'keyboard focus not achieved')
                        compare(theme,width,'focus-visible')
            assert not errors,(path,route,motion,errors)
            print('PASS: Q2-A route',path,route,motion,'six themes; 12 widths; rest/hover/focus',flush=True)
            page.close()
    print('PASS: Q2-A actual DOM equivalence',path,checks,'comparisons',flush=True)

with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
    for path,sha in FILES:
        html,baseline,candidate=exact_pair(path,sha)
        run(browser,path,html,baseline,candidate)
    browser.close()
print('PASS: Q2-A comparison gate; exact eight-rule scope and sampled styles/geometry equivalent in both builds.',flush=True)
