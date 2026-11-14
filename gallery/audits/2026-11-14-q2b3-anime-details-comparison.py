#!/usr/bin/env python3
"""Q2-B3 exact-scope gate with real Anime Details DOM comparisons."""
import hashlib,re,subprocess,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
BASE="fcc1d493b09dac7fa68703d199e3e234a33e1c37"
PAIRS=[[".detail-audio-toggle button[aria-pressed=\"true\"]{background:var(--tab);border-color:var(--accent);color:var(--accent-ink)}",".detail-audio-toggle button[aria-pressed=\"true\"]{background:var(--tab);border-color:var(--accent)}"],[".detail-control-panel{grid-column:2;grid-row:2;max-width:460px}",".detail-control-panel{grid-column:2;max-width:460px}"],[".detail-control-panel{grid-column:1 / -1;grid-row:auto;max-width:none;padding:14px;gap:12px}",".detail-control-panel{grid-column:1 / -1;grid-row:auto;padding:14px;gap:12px}"],[".episode-item{display:grid;grid-template-columns:44px minmax(160px,1fr) minmax(140px,auto) auto;align-items:center;gap:14px;border:0;border-radius:0;min-height:74px;padding:10px 12px;background:transparent;box-shadow:none;cursor:default}",".episode-item{display:grid;grid-template-columns:44px minmax(160px,1fr) minmax(140px,auto) auto;border:0;border-radius:0;min-height:74px;padding:10px 12px;background:transparent;box-shadow:none;cursor:default}"],[".detail-hero{grid-template-columns:160px minmax(0,1fr);gap:22px}",".detail-hero{gap:22px}"],[".detail-hero{grid-template-columns:114px minmax(0,1fr);gap:15px;margin-bottom:23px}",".detail-hero{gap:15px;margin-bottom:23px}"],[".episode-tools{grid-column:3;display:flex;align-items:center;justify-content:flex-end;gap:12px;min-width:0}",".episode-tools{gap:12px}"]]
FILES={"full":("gallery/Gallery-current.html","369f2ddb37e01b2ebe30901c5143157543a1c72fdbd6b850ef0829e675205e04"),"lightweight":("gallery/Gallery-development.html","e174093426b9d92bad7e91239eaf644e87034d549847bd4144a666bea33b5b08")}
THEMES=('ocean','twilight','ember','slate','glacier','verdant')
MEDIA_WIDTHS=(1440,1051,1050,971,970,851,850,791,790,681,680,621,620,571,570,391,390,371,370)
BREAKS=(710,635,515,320)
TARGETS=['.detail-hero','.detail-control-panel','.detail-audio-toggle','.episode-toolbar','.episode-list','.episode-item','.episode-tools','.episode-flags','.episode-actions']
STYLE=re.compile(br'<style>(.*?)</style>',re.S)
def unpack(html):
    matches=list(STYLE.finditer(html))
    assert len(matches)==1
    m=matches[0]
    return html[:m.start(1)],m.group(1),html[m.end(1):]
def exact_pair(path,sha):
    before=subprocess.check_output(['git','show',f'{BASE}:{path}'])
    assert hashlib.sha256(before).hexdigest()==sha
    after=Path(path).read_bytes()
    pre,css,post=unpack(before)
    cpre,candidate,cpost=unpack(after)
    assert pre==cpre and post==cpost
    expected=css
    for old,new in PAIRS:
        old=old.encode()
        assert expected.count(old)==1,old
        expected=expected.replace(old,new.encode(),1)
    assert expected==candidate and len(css)-len(candidate)==245
    print('PASS: Q2-B3 exact 12-declaration, 245-byte CSS-only deletion',path,flush=True)
    return after.decode(),css.decode(),candidate.decode()
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
    if(!matches.length && ['.detail-hero','.detail-control-panel','.detail-audio-toggle','.episode-toolbar','.episode-list'].includes(sel)) throw Error('Missing target '+sel);
    for(const el of matches){
      nodes.add(el);
      for(const child of el.querySelectorAll('*')) nodes.add(child);
      for(let parent=el.parentElement;parent;parent=parent.parentElement){nodes.add(parent);if(parent===document.body)break;}
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


def settle(page,ms=520):
    page.wait_for_function('()=>!galleryStageTransition && !galleryStageFadeInProgress',timeout=10000)
    page.wait_for_timeout(ms)
def rest(page):
    page.mouse.move(0,0)
    page.evaluate('()=>document.activeElement?.blur()')
    settle(page)
def width(page,w):
    page.set_viewport_size({'width':w,'height':950})
    return page.locator('.detail-section').evaluate('''e=>{const s=getComputedStyle(e);return e.getBoundingClientRect().width-parseFloat(s.paddingLeft)-parseFloat(s.paddingRight)-parseFloat(s.borderLeftWidth)-parseFloat(s.borderRightWidth)}''')
def calibrate(page):
    # Find real container-query widths from the mounted application rather
    # than imposing a width on its elements or assuming a viewport offset.
    samples={}
    def measure(w):
        if w not in samples:
            samples[w]=width(page,w)
        return samples[w]
    for w in range(300,1201,20):
        measure(w)
    result={}
    for threshold in BREAKS:
        near=sorted(samples,key=lambda w:abs(samples[w]-threshold))[:5]
        guesses={w+round(threshold-samples[w])+d for w in near for d in range(-4,5)}
        for w in sorted(guesses):
            if 280<=w<=1440:
                measure(w)
        lower=min((w for w,v in samples.items() if v<=threshold),key=lambda w:threshold-samples[w])
        upper=min((w for w,v in samples.items() if v>threshold),key=lambda w:samples[w]-threshold)
        assert threshold-4<=samples[lower]<=threshold<samples[upper]<=threshold+4,(threshold,lower,samples[lower],upper,samples[upper])
        result[threshold]=(lower,upper)
        print('Container coverage',threshold,lower,samples[lower],upper,samples[upper],flush=True)
    return result

def open_anime(page,anime):
    if page.locator('#detail-back').count():
        page.locator('#detail-back').click()
        page.wait_for_function('()=>!state.detailId')
        settle(page)
    page.locator('[data-detail="'+anime+'"]').first.click()
    page.wait_for_function('id=>state.detailId===id',arg=anime)
    page.locator('.episode-toolbar').wait_for()
    rest(page)
def release(page,release_id):
    button=page.locator('[data-inline-installment="'+release_id+'"]')
    button.click()
    page.wait_for_function('id=>document.querySelector(\'[data-inline-installment="\'+id+\'"]\')?.getAttribute("aria-current")==="true"',arg=release_id)
    rest(page)
def audio(page,lang):
    button=page.locator('[data-detail-audio="'+lang+'"]')
    if button.get_attribute('aria-pressed')!='true':
        button.click()
    assert button.get_attribute('aria-pressed')=='true'
    rest(page)
def filt(page,kind):
    button=page.locator('[data-episode-filter="'+kind+'"]')
    if button.get_attribute('aria-pressed')!='true':
        button.click()
    assert page.locator('[data-episode-filter="'+kind+'"]').get_attribute('aria-pressed')=='true'
    rest(page)
def count(page,shown,total,hidden):
    c=page.locator('.episode-shown')
    assert c.count()==1
    assert c.evaluate('(e)=>e.classList.contains("is-hidden")')==hidden
    assert c.get_attribute('aria-hidden')==('true' if hidden else None)
    assert c.evaluate('(e)=>getComputedStyle(e).opacity')==('0' if hidden else '1')
    if not hidden:
        assert c.inner_text()==f'{shown} of {total} shown'
        assert c.get_attribute('role')=='status'
    assert page.locator('.episode-list .episode-item').count()==shown

def run(mode):
    path,sha=FILES[mode]
    html,baseline,candidate=exact_pair(path,sha)
    checks=0
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
        for motion in ('no-preference','reduce'):
            page=browser.new_page(viewport={'width':1440,'height':950},reduced_motion=motion)
            errors=[]
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.set_content(html,wait_until='domcontentloaded')
            page.wait_for_selector('[data-detail="demo:solo"]')
            page.evaluate('''({baseline,candidate})=>{
                window.__q2baseline=baseline;window.__q2candidate=candidate;
                if(document.querySelector('style').textContent!==candidate)throw Error('Unexpected actual stylesheet');
            }''',{'baseline':baseline,'candidate':candidate})
            open_anime(page,'demo:solo')
            release(page,'solo-s2')
            audio(page,'dub')
            count(page,13,13,True)
            widths=calibrate(page)
            sizes=sorted(set(MEDIA_WIDTHS+tuple(w for pair in widths.values() for w in pair)),reverse=True)
            def compare(theme,label,matched=True):
                nonlocal checks
                result=page.evaluate(COMPARE,{'targets':TARGETS,'scope':'.anime-detail'})
                assert 'property' not in result,(path,motion,theme,label,result)
                assert result['nodes']>0 and result['counts']['.episode-toolbar']==1 and result['counts']['.episode-list']==1,result
                assert all(result['counts'][s]>0 for s in TARGETS[:5]),result
                if matched:
                    assert all(result['counts'][s]>0 for s in TARGETS[5:]),result
                else:
                    assert all(result['counts'][s]==0 for s in TARGETS[5:]),result
                checks+=1
            def interact(theme,selector):
                target=page.locator(selector).first
                assert target.is_enabled(),selector
                target.hover()
                settle(page)
                assert target.evaluate('(e)=>e.matches(":hover")')
                compare(theme,selector+' hover')
                page.mouse.move(0,0)
                page.keyboard.press('Tab')
                target.focus()
                settle(page)
                assert target.evaluate('(e)=>e.matches(":focus-visible")')
                compare(theme,selector+' keyboard focus')
                rest(page)
            def gradient():
                return page.evaluate('''()=>[...document.querySelectorAll('.detail-audio-toggle button')].map(e=>{
                    const s=getComputedStyle(e,'::before'),r=e.getBoundingClientRect();
                    return [e.dataset.detailAudio,e.getAttribute('aria-pressed'),s.backgroundImage,s.opacity,r.width,r.height];
                })''')
            def audio_interactions(theme):
                before=gradient()
                assert len(before)==2 and [x[3] for x in before if x[1]=='true']==['1'] and [x[3] for x in before if x[1]=='false']==['0'],before
                for lang in ('sub','dub'):
                    target=page.locator('[data-detail-audio="'+lang+'"]')
                    target.hover()
                    settle(page)
                    assert target.evaluate('(e)=>e.matches(":hover")')
                    assert gradient()==before,('Selected gradient moved on hover',theme,lang,before,gradient())
                    compare(theme,lang+' audio hover')
                    page.mouse.move(0,0)
                    page.keyboard.press('Tab')
                    target.focus()
                    settle(page)
                    assert target.evaluate('(e)=>e.matches(":focus-visible")')
                    assert gradient()==before,('Selected gradient changed on focus',theme,lang)
                    compare(theme,lang+' audio focus')
                    rest(page)
            for theme in THEMES:
                width(page,1440)
                open_anime(page,'demo:solo') if page.evaluate('state.detailId')!='demo:solo' else None
                release(page,'solo-s2')
                audio(page,'dub')
                filt(page,'all')
                page.evaluate('(theme)=>{state.theme=theme;document.body.dataset.theme=theme;}',theme)
                rest(page)
                count(page,13,13,True)
                assert page.locator('.episode-list [data-episode-action="watch"][disabled]').count()==4
                assert page.locator('.episode-list [data-episode-action="watch"]:not([disabled])').count()==9
                assert page.locator('.episode-list [data-episode-action="download"]:not([disabled])').count()==13
                # Measure actual container coverage independently in every theme.
                for threshold,(lo,hi) in widths.items():
                    low=width(page,lo);high=width(page,hi)
                    assert threshold-4<=low<=threshold<high<=threshold+4,(theme,threshold,low,high)
                for w in sizes:
                    width(page,w)
                    rest(page)
                    compare(theme,('all dub',w))
                for w in (1440,widths[515][0]):
                    width(page,w)
                    rest(page)
                    audio_interactions(theme)
                    for action in ('watch','download'):
                        interact(theme,'.episode-list [data-episode-action="'+action+'"]:not([disabled])')
                    row=page.locator('.episode-item.episode-not-playable').first
                    row.hover()
                    settle(page)
                    assert row.evaluate('(e)=>e.matches(":hover")')
                    compare(theme,('unavailable row hover',w))
                    disabled=row.locator('[data-episode-action="watch"]')
                    assert disabled.is_disabled()
                    disabled.hover()
                    settle(page)
                    assert disabled.evaluate('(e)=>e.matches(":hover")')
                    compare(theme,('disabled watch hover',w))
                    rest(page)
                width(page,1440)
                rest(page)
                # The actual count element must survive filtering and keep the
                # approved opacity animation; check events for both motion modes.
                page.evaluate('''()=>{const e=document.querySelector('.episode-shown');window.__toolbarCount=e;window.__countEvents=[];e.addEventListener('transitionend',x=>{if(x.propertyName==='opacity')window.__countEvents.push(x.propertyName)})}''')
                filt(page,'playable')
                count(page,9,13,False)
                assert page.evaluate('window.__toolbarCount===document.querySelector(".episode-shown")')
                assert page.evaluate('window.__countEvents.length')==(0 if motion=='reduce' else 1)
                compare(theme,'playable count shown')
                for w in sizes:
                    width(page,w)
                    rest(page)
                    compare(theme,('playable dub',w))
                for w in (1440,widths[515][0]):
                    width(page,w)
                    rest(page)
                    interact(theme,'[data-episode-filter="all"]')
                    interact(theme,'[data-episode-filter="playable"]')
                width(page,1440)
                audio(page,'sub')
                count(page,13,13,True)
                compare(theme,'playable sub, count hidden')
                audio(page,'dub')
                count(page,9,13,False)
                compare(theme,'playable dub restored')
                filt(page,'all')
                count(page,13,13,True)
                compare(theme,'all restored')
                open_anime(page,'demo:quints')
                audio(page,'sub')
                count(page,12,12,True)
                for w in (1440,widths[710][0],widths[320][0]):
                    width(page,w)
                    rest(page)
                    compare(theme,('fully matched',w))
                filt(page,'playable')
                count(page,12,12,True)
                compare(theme,'fully matched playable')
                width(page,1440)
                open_anime(page,'demo:long')
                audio(page,'dub')
                count(page,12,12,True)
                assert page.locator('.episode-list [data-episode-action="watch"][disabled]').count()==12
                assert page.locator('.detail-actions [data-episode-action="watch"]').is_disabled()
                compare(theme,'no dub availability, all')
                filt(page,'playable')
                count(page,0,12,False)
                assert page.locator('.episode-empty-filter').count()==1
                compare(theme,'no dub availability, empty playable',False)
                audio(page,'sub')
                count(page,12,12,True)
                compare(theme,'available sub restored')
                width(page,1440)
                open_anime(page,'demo:aot')
                release(page,'aot-s3')
                assert page.locator('.provider-unmatched').count()==1
                assert page.locator('.episode-availability').count()==0
                for w in (1440,widths[710][0],widths[320][0]):
                    width(page,w)
                    rest(page)
                    compare(theme,('unmatched',w),False)
                assert not errors,(mode,motion,theme,errors)
                print('PASS: Q2-B3 theme',mode,motion,theme,len(sizes),'viewport samples; all container boundaries; complete/partial/unmatched; audio/filter/focus/hover',flush=True)
            page.close()
        browser.close()
    assert checks>=1000,(mode,checks)
    print('PASS: Q2-B3 actual DOM equivalence',path,checks,'comparisons',flush=True)
if __name__=='__main__':
    run(sys.argv[1])
