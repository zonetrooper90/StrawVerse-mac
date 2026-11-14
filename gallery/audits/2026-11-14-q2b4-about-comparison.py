#!/usr/bin/env python3
"""Q2-B4: real mounted About navigation and exact-scope DOM equivalence."""
import hashlib, re, runpy, subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

S=runpy.run_path("gallery/changes/pending/2026-11-14-q2b4-about.py")
THEMES=("ocean","twilight","ember","slate","glacier","verdant")
WIDTHS=(1440,1051,1050,711,710,701,700,521,520,441,440,370)
PARENT={"overview":None,"credits":"overview","components":"credits","licenses":"overview",
        "legal":"overview","terms":"legal","privacy":"legal","copyright":"legal"}
BACK={"overview":"Back to Gallery","credits":"Back to About","components":"Back to Acknowledgements",
      "licenses":"Back to About","legal":"Back to About","terms":"Back to Legal & Privacy",
      "privacy":"Back to Legal & Privacy","copyright":"Back to Legal & Privacy"}
STYLE=re.compile(br'<style>(.*?)</style>',re.S)
EXPECTED=6*(len(WIDTHS)*len(PARENT)+2*3*2+1)

def unpack(raw):
    matches=list(STYLE.finditer(raw))
    assert len(matches)==1
    m=matches[0]
    return raw[:m.start(1)],m.group(1),raw[m.end(1):]

def exact_pair(mode):
    path,digest=S["FILES"][mode]
    before=subprocess.check_output(["git","show",S["BASE"]+":"+path])
    assert hashlib.sha256(before).hexdigest()==digest
    after=Path(path).read_bytes()
    pre,base,post=unpack(before)
    cp,css,ct=unpack(after)
    assert (pre,post)==(cp,ct)
    assert S["transform"](base)==css and len(before)-len(after)==74
    print("PASS: exact five-declaration, 74-byte CSS-only deletion",path,flush=True)
    return after.decode(),base.decode(),css.decode()

COMPARE=r'''({view})=>{
 const style=document.querySelector('style'), candidate=window.__q2candidate, baseline=window.__q2baseline;
 if(style.textContent!==candidate)throw Error('Unexpected stylesheet');
 const root=document.querySelector('#settings-about-root');
 const active=root.querySelector('[data-about-view="'+view+'"]');
 const back=document.querySelector('#settings-back');
 if(!root || !active || active.hidden || !back)throw Error('Missing actual About view');
 const nodes=new Set();
 for(const el of [root,active,back]){
   nodes.add(el);
   for(const child of el.querySelectorAll('*')){
     if(!child.closest('[hidden]') && child.getClientRects().length)nodes.add(child);
   }
   for(let p=el.parentElement;p;p=p.parentElement){nodes.add(p);if(p===document.body)break;}
 }
 function snap(){
   return Array.from(nodes,e=>{
     const r=e.getBoundingClientRect(),s=getComputedStyle(e);
     const props=Array.from(s,k=>[k,s.getPropertyValue(k)]);
     const pseudo=['::before','::after'].map(k=>{
       const p=getComputedStyle(e,k);return Array.from(p,n=>[n,p.getPropertyValue(n)]);
     });
     return {tag:e.tagName,cls:e.getAttribute('class'),props,pseudo,
       rect:[r.x,r.y,r.width,r.height,e.clientWidth,e.clientHeight,e.scrollWidth,e.scrollHeight],
       state:[e.matches(':hover'),e.matches(':focus-visible'),e.getAttribute('aria-label'),e.hidden],
       text:e===active?e.innerText:null,
       link:e.matches('a[href]')?[e.getAttribute('href'),e.getAttribute('target'),e.getAttribute('rel')]:null};
   });
 }
 try{
   style.textContent=baseline;
   const a=snap();
   style.textContent=candidate;
   const b=snap();
   for(let i=0;i<a.length;i++){
     const x=a[i],y=b[i],info={i,tag:x.tag,cls:x.cls};
     if(x.props.length!==y.props.length)return {...info,error:'property count'};
     for(let j=0;j<x.props.length;j++){
       if(x.props[j][0]!==y.props[j][0] || x.props[j][1]!==y.props[j][1])
         return {...info,error:x.props[j][0],before:x.props[j][1],after:y.props[j][1]};
     }
     if(JSON.stringify(x.pseudo)!==JSON.stringify(y.pseudo))return {...info,error:'pseudo style'};
     if(x.rect.some((v,j)=>Math.abs(v-y.rect[j])>0.02))return {...info,error:'geometry',before:x.rect,after:y.rect};
     for(const k of ['state','text','link'])if(JSON.stringify(x[k])!==JSON.stringify(y[k]))return {...info,error:k};
   }
   return {nodes:a.length,links:active.querySelectorAll('a[href]').length};
 } finally {if(style.textContent!==candidate)style.textContent=candidate;}
}'''

def settle(page,ms=520):
    page.wait_for_function("()=>!galleryStageTransition && !galleryStageFadeInProgress && settingsScrollFrame===null",timeout=10000)
    page.wait_for_timeout(ms)

def verify_view(page,view,focused=False,reset=True):
    page.wait_for_function("""view=>currentAboutView===view && settingsLastSection==='about' &&
      [...document.querySelectorAll('#settings-about-root [data-about-view]')].filter(e=>!e.hidden).length===1 &&
      !document.querySelector('[data-about-view="'+view+'"]').hidden""",arg=view)
    active=page.locator('[data-about-view="'+view+'"]')
    assert active.is_visible()
    assert page.locator('#settings-back').get_attribute('aria-label')==BACK[view]
    assert page.locator('#settings-back').get_attribute('title')==BACK[view]
    if focused:
        target='#settings-about-card' if view=='overview' else '#settings-about-'+view
        assert page.locator(target).evaluate("e=>e===document.activeElement"),(view,'focus')
    if reset:
        page.wait_for_function("()=>Math.abs(workspace.scrollTop)<1",timeout=10000)

def rest(page):
    page.mouse.move(0,0)
    page.evaluate("()=>document.activeElement?.blur()")
    settle(page)

def go(page,view):
    page.locator('[data-about-open="'+view+'"]').click()
    verify_view(page,view,focused=True)
    rest(page)

def back(page,view):
    expected=PARENT[view]
    assert expected is not None
    # Exercise scroll reset from real scrollable content where present.
    amount=page.evaluate("()=>{const n=Math.min(80,workspace.scrollHeight-workspace.clientHeight);workspace.scrollTop=n;return n;}")
    if amount>1:
        page.wait_for_function("()=>workspace.scrollTop>0")
    page.locator('#settings-back').click()
    verify_view(page,expected,focused=True)
    rest(page)

def run(mode,motion):
    assert mode in S["FILES"] and motion in ('no-preference','reduce')
    html,baseline,candidate=exact_pair(mode)
    count=0
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
        page=browser.new_page(viewport={'width':1440,'height':950},reduced_motion=motion)
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.set_content(html,wait_until='domcontentloaded')
        page.evaluate("""({baseline,candidate})=>{
          window.__q2baseline=baseline;window.__q2candidate=candidate;
          if(document.querySelector('style').textContent!==candidate)throw Error('Wrong stylesheet');
        }""",{'baseline':baseline,'candidate':candidate})
        page.locator('#settings').click()
        page.wait_for_function("()=>document.body.classList.contains('settings-view') && !galleryStageTransition && !galleryStageFadeInProgress")
        page.locator('[data-settings-section="about"]').click()
        settle(page)
        verify_view(page,'overview')
        assert page.locator('#settings-about-root [data-about-view]').count()==8

        def compare(theme,view,label):
            nonlocal count
            verify_view(page,view,reset=False)
            result=page.evaluate(COMPARE,{'view':view})
            assert 'error' not in result,(mode,motion,theme,view,label,result)
            assert result['nodes']>10,result
            count+=1

        def interaction(theme,view,target):
            assert target.is_visible() and target.is_enabled()
            target.hover()
            settle(page)
            assert target.evaluate("e=>e.matches(':hover')")
            compare(theme,view,'hover')
            page.mouse.move(0,0)
            page.keyboard.press('Tab')
            target.focus()
            settle(page)
            assert target.evaluate("e=>e.matches(':focus-visible')")
            compare(theme,view,'keyboard focus')
            rest(page)

        for theme in THEMES:
            page.evaluate("(theme)=>{state.theme=theme;document.body.dataset.theme=theme;}",theme)
            for w in WIDTHS:
                page.set_viewport_size({'width':w,'height':950})
                page.evaluate("()=>workspace.scrollTop=0")
                rest(page)
                verify_view(page,'overview')
                compare(theme,'overview',w)
                go(page,'credits')
                compare(theme,'credits',w)
                go(page,'components')
                compare(theme,'components',w)
                back(page,'components')
                back(page,'credits')
                go(page,'licenses')
                compare(theme,'licenses',w)
                back(page,'licenses')
                go(page,'legal')
                compare(theme,'legal',w)
                for child in ('terms','privacy','copyright'):
                    go(page,child)
                    compare(theme,child,w)
                    back(page,child)
                back(page,'legal')
            for w in (1440,370):
                page.set_viewport_size({'width':w,'height':950})
                page.evaluate("()=>workspace.scrollTop=0")
                rest(page)
                interaction(theme,'overview',page.locator('[data-about-open="credits"]'))
                go(page,'credits')
                interaction(theme,'credits',page.locator('#settings-back'))
                interaction(theme,'credits',page.locator('[data-about-view="credits"] a[href]').first)
                back(page,'credits')
            page.set_viewport_size({'width':1440,'height':950})
            rest(page)
            page.locator('#search').click()
            page.locator('#header-search-input').fill('Privacy Policy')
            page.locator('[data-settings-search-key="privacy"]').click()
            verify_view(page,'privacy',focused=True,reset=False)
            assert page.locator('#search').get_attribute('aria-expanded')=='false'
            page.wait_for_function("()=>!document.querySelector('.settings-search-target')",timeout=10000)
            settle(page)
            compare(theme,'privacy','actual Settings search deep link')
            back(page,'privacy')
            back(page,'legal')
            assert not errors,(mode,motion,theme,errors)
            print('PASS: About theme',mode,motion,theme,'109 comparisons; all views, nested Back, search, hover/focus',flush=True)
        page.close()
        browser.close()
    assert count==EXPECTED==654,(mode,motion,count,EXPECTED)
    print('PASS: Q2-B4 actual DOM equivalence',mode,motion,count,'comparisons',flush=True)
