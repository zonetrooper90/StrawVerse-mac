#!/usr/bin/env python3
"""Q2-B9: actual contextual search, exact CSS scope and real motion."""
import hashlib,re,runpy,subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright
S=runpy.run_path("gallery/changes/pending/2026-11-14-q2b9-search.py")
THEMES=("ocean","twilight","ember","slate","glacier","verdant")
WIDTHS=(1440,961,960,751,750,741,740,721,720,561,560,481,480,370)
STYLE=re.compile(br'<style>(.*?)</style>',re.S)
# 14 widths x 3 states; 2 widths x (5 contexts x 5 states + 6 additional states).
EXPECTED=6*(len(WIDTHS)*3+2*(5*5+6))
def unpack(raw):
    matches=list(STYLE.finditer(raw));assert len(matches)==1
    m=matches[0]
    return raw[:m.start(1)],m.group(1),raw[m.end(1):]
def exact_pair(mode):
    path,digest=S["FILES"][mode]
    before=subprocess.check_output(["git","show",S["BASE"]+":"+path])
    assert hashlib.sha256(before).hexdigest()==digest
    after=Path(path).read_bytes()
    pre,base,post=unpack(before);cp,css,ct=unpack(after)
    assert (pre,post)==(cp,ct)
    assert S["transform"](base)==css and len(before)-len(after)==139
    print("PASS: exact eleven-declaration, 139-byte CSS-only deletion",path,flush=True)
    return before.decode(),after.decode(),base.decode(),css.decode()

COMPARE=r"""()=>{
 const style=document.querySelector('style'),candidate=window.__q2candidate,baseline=window.__q2baseline;
 if(style.textContent!==candidate)throw Error('Unexpected stylesheet');
 const head=document.querySelector('.top'),field=document.querySelector('#header-search-field');
 const scope=document.body.classList.contains('settings-view')?'settings':whOpen?'history':state.detailId?'detail':state.view;
 const root=scope==='settings'?settingsPage:scope==='history'||scope==='detail'?screen:tabPages[state.view];
 if(!head||!field||!root||!root.getClientRects().length)throw Error('Missing Search DOM');
 const nodes=new Set([head,field,root]);
 for(const e of head.querySelectorAll('*'))nodes.add(e);
 // Include affected visible content, but exclude the unrelated animated download
 // progress/timer descendants; all header nodes and download group shells remain.
 for(const e of root.querySelectorAll('*'))
   if(!e.closest('[hidden]')&&e.getClientRects().length&&
     (scope!=='downloads'||e.matches('.page-header,.page-header *, .download-filters,.download-filters *, .download-groups,.download-group,.search-empty,.empty')))nodes.add(e);
 for(let p=root.parentElement;p;p=p.parentElement)nodes.add(p);
 function snap(){
   return Array.from(nodes,e=>{
     const r=e.getBoundingClientRect(),s=getComputedStyle(e);
     const pseudos=['::before','::after'];if(e===searchInput)pseudos.push('::placeholder');
     return {tag:e.tagName,cls:e.getAttribute('class'),id:e.id,
       props:Array.from(s,k=>[k,s.getPropertyValue(k)]),
       pseudo:pseudos.map(k=>{const p=getComputedStyle(e,k);return Array.from(p,n=>[n,p.getPropertyValue(n)]);}),
       rect:[r.x,r.y,r.width,r.height,e.clientWidth,e.clientHeight,e.scrollWidth,e.scrollHeight],
       state:[e.matches(':hover'),e.matches(':focus-visible'),e.matches(':disabled'),e.inert,e.hidden,e.getAttribute('aria-label'),e.getAttribute('aria-hidden'),e.getAttribute('aria-expanded'),e.getAttribute('aria-pressed'),e.getAttribute('aria-current')],
       text:e.matches('.brandname,.subtitle,.search-empty,.empty,.discover-results-heading,.discover-result-count,.settings-result-item,.wh-result-count,.poster-title')?e.innerText:null};
   });
 }
 try{
   style.textContent=baseline;
   const a=snap();
   style.textContent=candidate;
   const b=snap();
   for(let i=0;i<a.length;i++){
     const x=a[i],y=b[i],info={i,tag:x.tag,cls:x.cls,id:x.id};
     if(x.props.length!==y.props.length)return {...info,error:'property count'};
     for(let j=0;j<x.props.length;j++)if(x.props[j][0]!==y.props[j][0]||x.props[j][1]!==y.props[j][1])
       return {...info,error:x.props[j][0],before:x.props[j][1],after:y.props[j][1]};
     if(JSON.stringify(x.pseudo)!==JSON.stringify(y.pseudo))return {...info,error:'pseudo style'};
     if(x.rect.some((v,j)=>Math.abs(v-y.rect[j])>0.02))return {...info,error:'geometry',before:x.rect,after:y.rect};
     for(const k of ['state','text'])if(JSON.stringify(x[k])!==JSON.stringify(y[k]))return {...info,error:k};
   }
   return {nodes:a.length,scope};
 }finally{if(style.textContent!==candidate)style.textContent=candidate;}
}"""
GEOMETRY=r"""()=>{
 const box=e=>{const r=e.getBoundingClientRect();return [r.x,r.y,r.width,r.height]};
 const f=searchField,s=getComputedStyle(f),brand=document.querySelector('.brand-row .brand');
 const shell=tabPages.discover.querySelector('.continue-shell'),clip=shell?.querySelector('.continue-clip');
 const explore=tabPages.discover.querySelector('#sf-discover-explore');
 return {field:box(f),search:box(searchToggle),settings:box(document.querySelector('#settings')),
   brand:box(brand),brandOpacity:Number(getComputedStyle(brand).opacity),opacity:Number(s.opacity),visibility:s.visibility,
   width:innerWidth,overflow:document.documentElement.scrollWidth,open:searchOpen,
   inert:f.inert,aria:f.getAttribute('aria-hidden'),expanded:searchToggle.getAttribute('aria-expanded'),
   focus:document.activeElement?.id,outline:s.outlineStyle,
   shell:shell?box(shell):null,clip:clip?box(clip):null,explore:explore?box(explore):null,
   shellOpacity:shell?Number(getComputedStyle(shell).opacity):null,shellPointer:shell?getComputedStyle(shell).pointerEvents:null,
   clipStyle:clip?[getComputedStyle(clip).minHeight,getComputedStyle(clip).overflow]:null,
   sameShell:shell===window.__searchShell};
}"""
def geo(page):return page.evaluate(GEOMETRY)
def settle(page,ms=520):
    page.wait_for_function("()=>!galleryStageTransition&&!galleryStageFadeInProgress&&!tabTrackAnimation&&!gallerySettingsOpening&&!settingsClosing",timeout=10000)
    page.wait_for_timeout(ms)
def blur(page):
    page.mouse.move(0,0);page.evaluate("()=>document.activeElement?.blur()");settle(page)
def state_check(page,opened,focus=True):
    g=geo(page)
    assert (g['open'],g['inert'],g['aria'],g['expanded'])==(opened,not opened,str(not opened).lower(),str(opened).lower()),g
    assert g['visibility']==('visible' if opened else 'hidden') and g['opacity']==int(opened),g
    if focus:assert g['focus']==('header-search-input' if opened else 'search'),g
    if opened:
        assert g['field'][2]>50 and g['field'][0]>=-1 and g['field'][0]+g['field'][2]<g['search'][0]+1,g
        assert g['brandOpacity']==(0 if g['width']<=720 else 1),g
        assert page.locator('#header-search-input').evaluate("""e=>{
          const r=e.getBoundingClientRect(),hit=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);
          return hit===e;
        }"""),g
    else:assert g['field'][2]<=2,g
    return g
def stationary(a,b):
    for key in ('search','settings'):
        assert all(abs(x-y)<=1 for x,y in zip(a[key],b[key])),(key,a,b)
    assert b['overflow']<=max(a['overflow'],b['width'])+1,(a,b)
def opening(page,keyboard=False):
    before=geo(page)
    if keyboard:
        page.keyboard.press('Control+f')
    else:page.locator('#search').click()
    settle(page);g=state_check(page,True)
    stationary(before,g)
    if keyboard:assert g['outline']=='solid',g
    else:assert g['outline']=='none',g
    return before,g
def close(page,kind='escape'):
    if kind=='escape':page.locator('#header-search-input').press('Escape')
    elif kind=='button':page.locator('#header-search-close').click()
    else:page.locator('#search').click()
    settle(page);return state_check(page,False)
def fill(page,q):
    page.locator('#header-search-input').fill(q);settle(page)
    assert page.evaluate("state.query")==q
    assert page.locator('#header-search-clear').is_visible()==bool(q)
    assert page.locator('#header-search-close').is_visible()==(not q)
def clear(page):
    page.locator('#header-search-clear').click();settle(page)
    assert page.evaluate("state.query")=='' and page.locator('#header-search-input').input_value()==''
    state_check(page,True)
def tab(page,key):
    page.locator('#nav-'+key).click();settle(page)
    assert page.evaluate("state.view")==key and not page.evaluate("searchOpen")
def scope_root(page,scope):
    return page.locator('#settings-page' if scope=='settings' else '#wh-root' if scope=='history' else '[data-tab-page="'+scope+'"]')
def result_ids(page,scope):
    selector='[data-wh-row]' if scope=='history' else '[data-download-group]' if scope=='downloads' else '.settings-result-item' if scope=='settings' else ('.discover-result-region .poster-button[data-detail]' if scope=='discover' else '.poster-button[data-detail]')
    return scope_root(page,scope).locator(selector).evaluate_all("(es)=>es.map(e=>e.dataset.whRow||e.dataset.downloadGroup||e.dataset.settingsSearchKey||e.dataset.detail)")
def remember(page,scope):
    page.evaluate("""scope=>{window.__q2remember=(scope==='library'||scope==='downloads')?tabPages[scope].querySelector('.page-header'):null;}""",scope)
def context(page,scope):
    if scope=='history':
        tab(page,'discover');page.locator('#wh-view-history').click();settle(page)
        assert page.evaluate("whOpen")
    elif scope=='settings':
        page.locator('#settings').click();settle(page)
        assert page.locator('#settings-page').is_visible()
    else:tab(page,scope)
    assert scope_root(page,scope).is_visible()
def depart(page,scope):
    if scope=='history':
        page.locator('[data-wh-exit]').click();settle(page)
        assert not page.evaluate("whOpen")
    elif scope=='settings':
        page.locator('#settings-back').click();settle(page)
        assert not page.evaluate("document.body.classList.contains('settings-view')")
def query_for(page,scope):
    if scope=='settings':return 'Typography','font'
    if scope=='discover':
        return page.evaluate("()=>{const x=getSourceCataloguePreview().titles[0];return [x.name,x.id]}")
    if scope=='library':return 'Quintessential','demo:quints'
    if scope=='history':
        return page.evaluate("()=>{const x=whGroups()[0].items[0];return [x.title,x.id]}")
    return page.evaluate("()=>{const id=visibleDownloadEntries()[0].animeId;return [demo.find(x=>x.id===id).name,id]}")
# Capture actual CSS transitions created by a real user click. Freeze them only
# for deterministic sampling at common elapsed times; finish them afterward.
# This uses native CSSTransition objects, not synthetic selectors or animations.
TRACE_INSTALL=r"""()=>{
 const get=()=>({field:searchField,brand:document.querySelector('.brand-row .brand'),
   shell:tabPages.discover.querySelector('.continue-shell')});
 window.__q2trace=null;
 const click=e=>{
   if(!searchToggle.contains(e.target))return;
   document.removeEventListener('click',click);
   const elements=get();
   const measure=()=>{const f=searchField,b=elements.brand,s=elements.shell,fs=getComputedStyle(f),ss=getComputedStyle(s);
     const rect=e=>{const r=e.getBoundingClientRect();return [r.x,r.y,r.width,r.height]};
     return {field:rect(f),opacity:Number(fs.opacity),visibility:fs.visibility,brandOpacity:Number(getComputedStyle(b).opacity),
       shellHeight:s.getBoundingClientRect().height,shellOpacity:Number(ss.opacity),
       search:rect(searchToggle),settings:rect(document.querySelector('#settings'))};
   };
   measure(); // Force a style update before enumerating the native transitions.
   const list=Object.entries(elements).flatMap(([name,el])=>el.getAnimations().filter(a=>a instanceof CSSTransition).map(a=>({name,property:a.transitionProperty,a})));
   const timing=list.map(({name,property,a})=>({name,property,duration:a.effect.getTiming().duration,delay:a.effect.getTiming().delay,easing:a.effect.getTiming().easing})).sort((a,b)=>(a.name+a.property).localeCompare(b.name+b.property));
   for(const {a} of list)a.pause();
   const samples=[0,40,80,120,160,200,240,280,320,360,420,500].map(t=>{
     for(const {a} of list)a.currentTime=t;
     return measure();
   });
   for(const {a} of list)a.finish();
   window.__q2trace={timing,samples};
 };
 document.addEventListener('click',click);
}"""
LIVE_INSTALL=r"""()=>{
 window.__q2live=null;
 const click=e=>{
   if(!searchToggle.contains(e.target))return;
   document.removeEventListener('click',click);
   const start=performance.now(),frames=[];
   const sample=()=>{const f=searchField,s=tabPages.discover.querySelector('.continue-shell');
     const r=f.getBoundingClientRect();frames.push([performance.now()-start,r.width,Number(getComputedStyle(f).opacity),s.getBoundingClientRect().height,Number(getComputedStyle(s).opacity)]);
     if(performance.now()-start<560)requestAnimationFrame(sample);else window.__q2live=frames;
   };sample();
 };document.addEventListener('click',click);
}"""
def trace(page,motion,opening):
    before=geo(page)
    page.evaluate(TRACE_INSTALL);page.locator('#search').click()
    result=page.evaluate("window.__q2trace")
    assert result is not None
    settle(page);after=state_check(page,opening);stationary(before,after)
    by={(x['name'],x['property']):x for x in result['timing']}
    if motion=='reduce':
        assert not by,by
    else:
        for key,duration in [(('field','width'),320),(('field','opacity'),200),(('shell','grid-template-rows'),420),(('shell','opacity'),250)]:
            assert key in by and abs(by[key]['duration']-duration)<=1,(key,by)
        assert by[('field','width')]['delay']==0
        assert by[('field','opacity')]['delay']==0
        if not opening:assert ('field','visibility') in by and by[('field','visibility')]['delay']==320,by
        widths=[x['field'][2] for x in result['samples']]
        assert any(min(widths[0],widths[-1])+2<x<max(widths[0],widths[-1])-2 for x in widths[1:-1]),widths
        heights=[x['shellHeight'] for x in result['samples']]
        assert any(min(heights[0],heights[-1])+2<x<max(heights[0],heights[-1])-2 for x in heights[1:-1]),heights
    return result
def equivalent_trace(a,b):
    assert a['timing']==b['timing'],(a['timing'],b['timing'])
    for i,(x,y) in enumerate(zip(a['samples'],b['samples'])):
        assert x['visibility']==y['visibility'],(i,x,y)
        for key in ('field','search','settings'):
            assert all(abs(u-v)<=1 for u,v in zip(x[key],y[key])),(i,key,x,y)
        for key in ('opacity','brandOpacity','shellOpacity','shellHeight'):
            assert abs(x[key]-y[key])<=(1 if key=='shellHeight' else .015),(i,key,x,y)
def live(page,motion,opening):
    before=geo(page)
    page.evaluate(LIVE_INSTALL);page.locator('#search').click()
    page.wait_for_function("()=>window.__q2live!==null",timeout=5000)
    frames=page.evaluate("window.__q2live")
    after=state_check(page,opening);stationary(before,after)
    assert len(frames)>=2
    if motion=='reduce':
        assert all(abs(f[1]-after['field'][2])<=1 and abs(f[3]-after['shell'][3])<=1 for f in frames),frames
    else:
        for index,start,end in [(1,before['field'][2],after['field'][2]),(3,before['shell'][3],after['shell'][3])]:
            assert any(min(start,end)+2<f[index]<max(start,end)-2 for f in frames),frames
            assert abs(frames[-1][index]-end)<=1,frames
    return frames
def run(mode,motion):
    old_html,html,baseline,candidate=exact_pair(mode)
    count=0;motion_count=0
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
        def make(theme,w,source=html):
            page=browser.new_page(viewport={'width':w,'height':950},reduced_motion=motion)
            errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
            page.set_content(source,wait_until='domcontentloaded')
            page.evaluate("""({baseline,candidate,theme})=>{
              window.__q2baseline=baseline;window.__q2candidate=candidate;
              state.theme=theme;document.body.dataset.theme=theme;
              window.__searchShell=tabPages.discover.querySelector('.continue-shell');
            }""",{'baseline':baseline,'candidate':candidate,'theme':theme})
            blur(page)
            return page,errors
        def compare(page,theme,label):
            nonlocal count
            result=page.evaluate(COMPARE)
            assert 'error' not in result,(mode,motion,theme,label,result)
            assert result['nodes']>20,result
            count+=1
        for theme in THEMES:
            page,errors=make(theme,1440)
            for w in WIDTHS:
                page.set_viewport_size({'width':w,'height':950});blur(page)
                before=state_check(page,False,False);compare(page,theme,('closed',w))
                a,b=opening(page);assert b['sameShell'] and b['clipStyle']==['0px','hidden'],b
                assert b['shell'][3]<=1 and b['clip'][3]<=1 and b['shellPointer']=='none',b
                compare(page,theme,('open',w))
                after=close(page);stationary(before,after)
                assert after['sameShell'] and abs(after['shell'][3]-before['shell'][3])<=2,after
                compare(page,theme,('restored',w))
            assert not errors,errors;page.close()
            for w in (1440,370):
                page,errors=make(theme,w)
                for scope in ('discover','library','downloads','history','settings'):
                    context(page,scope)
                    if scope=='library':page.locator('[data-tag="Watching"]').click();settle(page)
                    if scope=='downloads':page.locator('[data-download-filter="Completed"]').click();settle(page)
                    if scope=='history':page.locator('[data-wh-filter="progress"]').click();settle(page)
                    remember(page,scope)
                    ids=result_ids(page,scope);q,wanted=query_for(page,scope)
                    if scope in ('library','downloads'):assert ids,scope
                    if scope in ('discover','library','downloads'):
                        page.evaluate("(s)=>{const p=tabPages[s];p.scrollTo({top:Math.min(100,p.scrollHeight-p.clientHeight),behavior:'instant'});}",scope)
                        settle(page)
                    before=geo(page)
                    old_scroll=page.evaluate("(s)=>s==='settings'?workspace.scrollTop:tabPages[state.view].scrollTop",scope)
                    opening(page,keyboard=True)
                    if scope in ('library','downloads'):
                        assert page.evaluate("(s)=>window.__q2remember===tabPages[s].querySelector('.page-header')",scope)
                        assert result_ids(page,scope)==ids
                    compare(page,theme,(scope,'empty',w))
                    fill(page,q);assert wanted in result_ids(page,scope),(scope,q,wanted,result_ids(page,scope))
                    if scope=='library':assert page.evaluate("state.tag")=='Watching'
                    if scope=='downloads':assert page.evaluate("state.downloadStatus")=='Completed'
                    if scope=='discover':assert geo(page)['sameShell']
                    if scope=='history':assert page.evaluate("whFilter")=='progress'
                    if scope=='library':
                        page.locator('#header-search-input').press('ArrowDown')
                        assert page.evaluate("document.activeElement.dataset.detail")==wanted
                        page.keyboard.press('ArrowUp');assert page.evaluate("document.activeElement===searchInput")
                    compare(page,theme,(scope,'matching',w))
                    fill(page,'zzzz-no-gallery-match-zzzz');assert result_ids(page,scope)==[],(scope,result_ids(page,scope))
                    compare(page,theme,(scope,'no match',w))
                    clear(page)
                    compare(page,theme,(scope,'cleared',w))
                    close(page,kind='button');assert result_ids(page,scope)==ids,(scope,ids,result_ids(page,scope))
                    if scope in ('discover','library','downloads','settings'):
                        assert abs(page.evaluate("(s)=>s==='settings'?workspace.scrollTop:tabPages[state.view].scrollTop",scope)-old_scroll)<=1
                    stationary(before,geo(page))
                    compare(page,theme,(scope,'closed',w))
                    depart(page,scope)
                # Real keyboard result navigation and actual destination.
                tab(page,'discover');opening(page,keyboard=True)
                q,wanted=query_for(page,'discover');fill(page,q)
                page.locator('#header-search-input').press('ArrowDown')
                assert page.evaluate("document.activeElement.dataset.detail")==wanted
                page.keyboard.press('ArrowUp');assert page.evaluate("document.activeElement===searchInput")
                compare(page,theme,('keyboard input',w))
                page.locator('#header-search-input').press('Enter');settle(page)
                assert page.evaluate("state.detailId")==wanted and not page.evaluate("searchOpen")
                assert page.locator('#detail-back').is_visible()
                compare(page,theme,('Discover result detail',w))
                # Search from a real detail returns to its original tab.
                page.locator('#search').click();settle(page)
                assert page.evaluate("!state.detailId && state.view==='discover' && searchOpen")
                state_check(page,True);compare(page,theme,('detail return',w))
                # Tab switch closes search.
                page.locator('#nav-library').click();settle(page)
                assert page.evaluate("state.view==='library'&&!searchOpen")
                compare(page,theme,('tab switch',w))
                # Real Settings index keyboard result deep link.
                context(page,'settings');opening(page,keyboard=True);fill(page,'Typography')
                page.locator('#header-search-input').press('ArrowDown')
                assert page.evaluate("document.activeElement.dataset.settingsSearchKey")=='font'
                page.keyboard.press('ArrowUp');assert page.evaluate("document.activeElement===searchInput")
                page.locator('#header-search-input').press('Enter')
                page.wait_for_function("()=>!searchOpen&&appearanceTab==='typography'&&!document.querySelector('.settings-search-target')",timeout=10000)
                settle(page);assert page.locator('#settings-font-card').is_visible()
                compare(page,theme,('Settings deep link',w))
                depart(page,'settings')
                # Hover and real hit test the search trigger in closed state.
                page.locator('#search').hover();settle(page)
                assert page.locator('#search').evaluate("e=>e.matches(':hover')")
                compare(page,theme,('trigger hover',w))
                # Real modal and Player prohibit keyboard Search. These are
                # behavior assertions; not additional equivalence samples.
                tab(page,'discover');page.locator('#filters').click();settle(page)
                page.keyboard.press('Control+f')
                assert not page.evaluate("searchOpen") and page.locator('#close-dialog').is_visible()
                page.locator('#close-dialog').click();page.wait_for_function("()=>!modalHost.firstChild");settle(page)
                page.locator('.discover-result-region [data-detail="demo:quints"]').click();settle(page)
                page.locator('.detail-actions [data-episode-action="watch"]').click();settle(page)
                assert page.evaluate("!!state.playback")
                page.keyboard.press('Control+f');assert not page.evaluate("searchOpen")
                assert not errors,(theme,w,errors);page.close()
                # Baseline and candidate both use real clicks and native CSS
                # transitions; normalized timing plus separate live frame traces.
                traces=[]
                for source in (old_html,html):
                    pg,errs=make(theme,w,source)
                    traces.append([trace(pg,motion,True),trace(pg,motion,False)])
                    live(pg,motion,True);live(pg,motion,False)
                    assert not errs,errs;pg.close()
                for i in (0,1):equivalent_trace(traces[0][i],traces[1][i]);motion_count+=1
            print('PASS: Search theme',mode,motion,theme,'104 DOM comparisons; four paired motion directions',flush=True)
        browser.close()
    assert count==EXPECTED==624 and motion_count==24,(mode,motion,count,motion_count)
    print('PASS: Q2-B9 actual DOM equivalence',mode,motion,count,'comparisons;',motion_count,'paired motion directions',flush=True)
