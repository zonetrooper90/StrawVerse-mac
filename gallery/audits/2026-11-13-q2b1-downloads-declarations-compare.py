#!/usr/bin/env python3
"""Q2-B1 gate: exact scoped CSS deletions and actual Downloads DOM equivalence."""
import hashlib,re,subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright
BASE="e108c7c892eab7e41d892ae06874c78f58160011"
PAIRS=[[".demo-download-footer{display:flex;align-items:center;flex-wrap:wrap;gap:7px 14px;margin-top:11px}",".demo-download-footer{gap:7px 14px;margin-top:11px}"],["body[data-theme] .sf-dl-list .sf-dl-episode{\n display:grid;grid-template-columns:minmax(100px,1fr) minmax(115px,.95fr) minmax(140px,1.45fr) 126px 44px;\n gap:12px;align-items:center;min-width:0;min-height:48px;padding:7px 0;\n border:0;color:var(--fg)\n}","body[data-theme] .sf-dl-list .sf-dl-episode{\n display:grid;grid-template-columns:minmax(100px,1fr) minmax(115px,.95fr) minmax(140px,1.45fr) 126px 44px;\n align-items:center;min-width:0;padding:7px 0;\n color:var(--fg)\n}"],["body[data-theme] .sf-dl-episode-track{display:flex;align-items:center;min-width:0;width:100%}","body[data-theme] .sf-dl-episode-track{display:flex;align-items:center;width:100%}"],["body[data-theme] .sf-dl-control-button{height:28px;min-width:74px;padding:0 8px;background:#ffffff0d;border:1px solid var(--line);border-radius:16px;color:var(--fg);font-size:11px;font-weight:650;display:flex;align-items:center;justify-content:center;gap:5px;cursor:pointer}","body[data-theme] .sf-dl-control-button{height:28px;min-width:74px;padding:0 8px;background:#ffffff0d;border:1px solid var(--line);color:var(--fg);font-weight:650;display:flex;gap:5px;cursor:pointer}"],["body[data-theme] .sf-dl-episode-percent{width:44px;justify-self:end;text-align:right;font-size:11px;font-weight:620;color:var(--muted);font-variant-numeric:tabular-nums}","body[data-theme] .sf-dl-episode-percent{font-size:11px;font-weight:620;color:var(--muted)}"],["body[data-theme] .sf-dl-list .sf-dl-episode{grid-template-columns:minmax(85px,1fr) minmax(90px,.9fr) minmax(100px,1.4fr) 126px 44px;gap:9px}","body[data-theme] .sf-dl-list .sf-dl-episode{grid-template-columns:minmax(85px,1fr) minmax(90px,.9fr) minmax(100px,1.4fr) 126px 44px}"]]
FILES=[["gallery/Gallery-current.html","333498a79e7ef34f1d85fd3049d599013c24f1d3b5ff81b80d13f8bf1bf7fee3"],["gallery/Gallery-development.html","64e1be5e874e4e2b66015c7a1adcbb540276a887d2a17eacb8f90b5e8a133223"]]
THEMES=('ocean','twilight','ember','slate','glacier','verdant')
WIDTHS=(1440,1121,1120,761,760,451,450,371,370,340)
INTERACTION_WIDTHS=(1440,450)
SCOPE='.tab-page[data-tab-page="downloads"]'
TARGETS=['.demo-download-footer','.sf-dl-episode','.sf-dl-episode-track','.sf-dl-control-button','.sf-dl-episode-percent']
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
    for old,new in PAIRS:
        raw=old.encode()
        assert expected.count(raw)==1,old
        expected=expected.replace(raw,new.encode(),1)
    assert expected==candidate_css and len(css)-len(candidate_css)==256,('Unexpected CSS diff',path)
    print('PASS: Q2-B1 exact 16-declaration deletion, all other HTML bytes unchanged',path,len(css)-len(candidate_css),flush=True)
    return after.decode('utf-8'),css.decode('utf-8'),candidate_css.decode('utf-8')

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
    if(!matches.length && sel!=='.sf-dl-control-button') throw Error('Missing target '+sel);
    for(const el of matches){
      nodes.add(el);
      for(const child of el.querySelectorAll('*')) nodes.add(child);
      for(let parent=el.parentElement;parent;parent=parent.parentElement){nodes.add(parent);if(parent===root)break;}
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
def expand(page,expanded):
    for group in page.locator('.sf-dl-card').all():
        if group.evaluate('(e)=>e.classList.contains("is-expanded")')!=expanded:
            group.locator('[data-download-toggle]').click()
    page.mouse.move(0,0)
    page.evaluate('()=>document.activeElement?.blur()')
    page.wait_for_timeout(500)
    assert page.locator('.sf-dl-card.is-expanded').count()==(page.locator('.sf-dl-card').count() if expanded else 0)
def rest(page):
    page.mouse.move(0,0)
    page.evaluate('()=>document.activeElement?.blur()')
    page.wait_for_timeout(300)
def run(browser,path,html,baseline,candidate):
    checks=0
    for motion in ('no-preference','reduce'):
        page=browser.new_page(viewport={'width':1440,'height':950},reduced_motion=motion)
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.set_content(html,wait_until='domcontentloaded')
        page.wait_for_selector('#wh-view-history')
        page.locator('.tab[data-view="downloads"]').click()
        page.wait_for_function('() => state.view==="downloads"')
        stable(page)
        page.evaluate('''({baseline,candidate})=>{
            window.__q2baseline=baseline;window.__q2candidate=candidate;
            if(document.querySelector('style').textContent!==candidate)
                throw Error('Candidate stylesheet does not match actual DOM');
        }''',{'baseline':baseline,'candidate':candidate})
        expand(page,True)
        # Exercise real pause action to render Resume, keeping other active and
        # failed rows. The demo has deterministic mixed transfer statuses.
        page.locator('[data-download-pause="quints-9"]').click()
        page.wait_for_function('()=>document.querySelector(\'[data-download-episode="quints-9"] [data-status="Paused"]\')!==null')
        rest(page)
        assert page.locator('[data-download-pause="quints-9"]').inner_text()=='Resume'
        assert page.locator('[data-download-retry]').count()>0
        assert page.locator('[data-download-dismiss]').count()>0
        assert page.locator('[data-download-cancel]').count()>0
        def compare(theme,width,label):
            nonlocal checks
            result=page.evaluate(COMPARE,{'targets':TARGETS,'scope':SCOPE})
            assert 'property' not in result,(path,motion,theme,width,label,result)
            assert result['nodes']>0 and result['counts']['.sf-dl-episode']>0,result
            checks+=1
        def interact(theme,width,selector,label):
            target=page.locator(selector).first
            assert target.count() and target.is_visible(),(width,label,'missing target')
            target.hover(timeout=5000)
            page.wait_for_timeout(300)
            assert target.evaluate('(e)=>e.matches(":hover")'),(width,label,'hover missing')
            compare(theme,width,label+' hover')
            page.mouse.move(0,0)
            page.keyboard.press('Tab')
            target.focus()
            page.wait_for_timeout(300)
            assert target.evaluate('(e)=>e.matches(":focus-visible")'),(width,label,'keyboard focus missing')
            compare(theme,width,label+' focus')
            rest(page)
        for theme in THEMES:
            page.evaluate('(theme)=>{state.theme=theme;document.body.dataset.theme=theme;}',theme)
            page.wait_for_timeout(300)
            for width in WIDTHS:
                page.set_viewport_size({'width':width,'height':950})
                rest(page)
                compare(theme,width,'expanded mixed statuses')
                if width in INTERACTION_WIDTHS:
                    interact(theme,width,'[data-download-pause="quints-9"]','Resume')
                    interact(theme,width,'[data-download-retry="astra-04"]','Retry')
                    # Hover a completed row to reveal its dismiss control; use
                    # the actual keyboard-focus state on the quick action.
                    row=page.locator('[data-download-episode="quints-1"]')
                    row.hover(timeout=5000)
                    page.wait_for_timeout(300)
                    assert row.evaluate('(e)=>e.matches(":hover")')
                    compare(theme,width,'row hover')
                    quick=row.locator('[data-download-dismiss]')
                    page.keyboard.press('Tab')
                    quick.focus()
                    page.mouse.move(0,0)
                    page.wait_for_timeout(300)
                    assert quick.evaluate('(e)=>e.matches(":focus-visible")')
                    compare(theme,width,'dismiss focus')
                    rest(page)
                    expand(page,False)
                    compare(theme,width,'collapsed')
                    expand(page,True)
            # Real filter and search interactions at a representative width.
            page.set_viewport_size({'width':760,'height':950})
            for status in ('Downloading','Completed','All'):
                page.locator('[data-download-filter="'+status+'"]').click()
                rest(page)
                assert page.locator('[data-download-filter="'+status+'"]').get_attribute('aria-pressed')=='true'
                compare(theme,760,'filter '+status)
            page.locator('#search').click()
            page.locator('#header-search-input').fill('Failed')
            page.wait_for_function('()=>state.query.trim().toLowerCase()==="failed" && !!document.querySelector(\'.sf-dl-episode [data-status="Failed"]\')')
            page.wait_for_timeout(500)
            assert page.locator('.sf-dl-episode [data-status="Failed"]').count()==page.locator('.sf-dl-episode').count()
            compare(theme,760,'search failed')
            page.locator('#header-search-close').click()
            page.wait_for_function('()=>!searchOpen && !state.query')
            stable(page)
            expand(page,True)
            assert not errors,(path,motion,theme,errors)
            print('PASS: Q2-B1 theme',path,theme,motion,'10 widths; expanded/collapsed; mixed statuses; hover/focus; filters/search',flush=True)
        page.close()
    print('PASS: Q2-B1 actual DOM equivalence',path,checks,'comparisons',flush=True)
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
    for path,sha in FILES:
        html,baseline,candidate=exact_pair(path,sha)
        run(browser,path,html,baseline,candidate)
    browser.close()
print('PASS: Q2-B1 comparison gate; exact scope and sampled styles/geometry equivalent in both builds.',flush=True)
