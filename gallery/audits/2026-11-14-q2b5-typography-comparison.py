#!/usr/bin/env python3
"""Q2-B5: actual application font tile equivalence and persistence."""
import hashlib,re,runpy,subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright
S=runpy.run_path("gallery/changes/pending/2026-11-14-q2b5-typography.py")
THEMES=("ocean","twilight","ember","slate","glacier","verdant")
FONTS=("system","atkinson","inter")
WIDTHS=(1440,1101,1100,711,710,701,700,531,530,441,440,370)
URL="https://gallery-typography-audit.invalid/"
STYLE=re.compile(br'<style>(.*?)</style>',re.S)
EXPECTED=6*(len(WIDTHS)*3+2*3*2*2+3*2+2)

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
    assert S["transform"](base)==css and len(before)-len(after)==116
    print("PASS: exact six-declaration, 116-byte CSS-only deletion",path,flush=True)
    return after.decode(),base.decode(),css.decode()

COMPARE=r'''()=>{
 const style=document.querySelector('style'), candidate=window.__q2candidate, baseline=window.__q2baseline;
 if(style.textContent!==candidate)throw Error('Unexpected stylesheet');
 const roots=['#settings-font-card','#appearance-typography-tab','#appearance-theme-tab','#settings-back','.settings-side'].map(s=>document.querySelector(s));
 if(roots.some(e=>!e||!e.getClientRects().length))throw Error('Missing actual Typography DOM');
 const nodes=new Set();
 for(const e of roots){
   nodes.add(e);
   for(const c of e.querySelectorAll('*'))if(!c.closest('[hidden]')&&c.getClientRects().length)nodes.add(c);
   for(let p=e.parentElement;p;p=p.parentElement){nodes.add(p);if(p===document.body)break;}
 }
 function snap(){
   return Array.from(nodes,e=>{
     const r=e.getBoundingClientRect(),s=getComputedStyle(e);
     return {tag:e.tagName,cls:e.getAttribute('class'),props:Array.from(s,k=>[k,s.getPropertyValue(k)]),
       pseudo:['::before','::after'].map(k=>{const p=getComputedStyle(e,k);return Array.from(p,n=>[n,p.getPropertyValue(n)]);}),
       rect:[r.x,r.y,r.width,r.height,e.clientWidth,e.clientHeight,e.scrollWidth,e.scrollHeight],
       state:[e.matches(':hover'),e.matches(':focus-visible'),e.getAttribute('aria-pressed'),e.getAttribute('aria-selected'),e.hidden],
       text:e.matches('.settings-font-glyphs,.settings-font-sample-label,#settings-font-missing')?e.textContent:null};
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
     for(let j=0;j<x.props.length;j++)if(x.props[j][0]!==y.props[j][0]||x.props[j][1]!==y.props[j][1])return {...info,error:x.props[j][0],before:x.props[j][1],after:y.props[j][1]};
     if(JSON.stringify(x.pseudo)!==JSON.stringify(y.pseudo))return {...info,error:'pseudo style'};
     if(x.rect.some((v,j)=>Math.abs(v-y.rect[j])>0.02))return {...info,error:'geometry',before:x.rect,after:y.rect};
     for(const k of ['state','text'])if(JSON.stringify(x[k])!==JSON.stringify(y[k]))return {...info,error:k};
   }
   return {nodes:a.length};
 } finally {if(style.textContent!==candidate)style.textContent=candidate;}
}'''

def settle(page,ms=520):
    page.wait_for_function("()=>!galleryStageTransition && !galleryStageFadeInProgress && settingsScrollFrame===null",timeout=10000)
    page.wait_for_timeout(ms)

def rest(page):
    page.mouse.move(0,0)
    page.evaluate("()=>document.activeElement?.blur()")
    settle(page)

def setup(page,baseline,candidate):
    page.wait_for_selector('#settings')
    page.evaluate("""({baseline,candidate})=>{
      window.__q2baseline=baseline;window.__q2candidate=candidate;
      if(document.querySelector('style').textContent!==candidate)throw Error('Wrong stylesheet');
    }""",{'baseline':baseline,'candidate':candidate})

def open_typography(page):
    page.locator('#settings').click()
    page.wait_for_function("()=>document.body.classList.contains('settings-view')&&!galleryStageTransition&&!galleryStageFadeInProgress")
    page.locator('#appearance-typography-tab').click()
    settle(page)
    assert page.locator('#appearance-typography-pane').is_visible()

def verify_font(page,font):
    data=page.evaluate("""()=>{
      const families={system:'SF Pro Display',atkinson:'Atkinson Hyperlegible Next',inter:'Inter'};
      const selected=state.font, name=selected==='system'?'':families[selected];
      const notice=document.querySelector('#settings-font-missing');
      return {selected,body:document.body.dataset.font,stored:localStorage.getItem('gallery.font'),
       family:getComputedStyle(document.body).fontFamily,
       missing:!notice.hidden,expectedMissing:!!name&&!galleryFontAvailable(name),notice:notice.textContent,
       tiles:[...document.querySelectorAll('[data-font-choice]')].map(e=>({
         id:e.dataset.fontChoice,pressed:e.getAttribute('aria-pressed'),
         check:getComputedStyle(e.querySelector('.settings-font-check')).opacity,
         family:getComputedStyle(e.querySelector('.settings-font-example')).fontFamily,
         labels:[...e.querySelectorAll('.settings-font-sample-label')].map(x=>x.textContent),
         samples:[...e.querySelectorAll('.settings-font-glyphs')].map(x=>x.textContent),
         display:getComputedStyle(e).display,direction:getComputedStyle(e).flexDirection,
         alignment:getComputedStyle(e).alignItems,radius:getComputedStyle(e).borderRadius
       }))};
    }""")
    assert data['selected']==data['body']==data['stored']==font,data
    families={'system':'SF Pro Display','atkinson':'Atkinson Hyperlegible Next','inter':'Inter'}
    assert families[font] in data['family'],data
    assert data['missing']==data['expectedMissing'],data
    assert (families[font] in data['notice']) if data['missing'] else data['notice']=='',data
    assert [t['id'] for t in data['tiles']]==list(FONTS),data
    for t in data['tiles']:
        assert t['pressed']==str(t['id']==font).lower(),t
        assert t['check']==('1' if t['id']==font else '0'),t
        assert families[t['id']] in t['family'],t
        assert t['labels']==['Uppercase','Lowercase','Numbers & symbols','Similar-looking characters'],t
        assert t['samples'][:2]==['ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'],t
        assert len(t['samples'])==4 and all(t['samples']),t
        assert (t['display'],t['direction'],t['alignment'],t['radius'])==('flex','column','stretch','13px'),t

def tile(page,font):
    return page.locator('[data-font-choice="'+font+'"]')

def choose(page,font,keyboard=False):
    target=tile(page,font)
    if keyboard:
        page.keyboard.press('Tab')
        target.focus()
        settle(page)
        assert target.evaluate("e=>e.matches(':focus-visible')")
        target.press('Enter')
    else:
        target.click()
    rest(page)
    verify_font(page,font)

def run(mode,motion):
    assert mode in S["FILES"] and motion in ('no-preference','reduce')
    html,baseline,candidate=exact_pair(mode)
    count=0
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
        page=browser.new_page(viewport={'width':1440,'height':950},reduced_motion=motion)
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.route(URL,lambda route:route.fulfill(status=200,content_type='text/html; charset=utf-8',body=html))
        page.goto(URL,wait_until='domcontentloaded')
        setup(page,baseline,candidate)
        open_typography(page)
        def compare(theme,font,label):
            nonlocal count
            assert page.locator('#appearance-typography-pane').is_visible()
            verify_font(page,font)
            result=page.evaluate(COMPARE)
            assert 'error' not in result,(mode,motion,theme,font,label,result)
            assert result['nodes']>50,result
            count+=1
        def set_theme(theme):
            page.evaluate("(theme)=>{state.theme=theme;document.body.dataset.theme=theme;}",theme)
            rest(page)
        for theme in THEMES:
            set_theme(theme)
            for w in WIDTHS:
                page.set_viewport_size({'width':w,'height':950})
                for font in FONTS:
                    choose(page,font)
                    page.evaluate("()=>workspace.scrollTop=0")
                    rest(page)
                    compare(theme,font,('selected',w))
            for w in (1440,370):
                page.set_viewport_size({'width':w,'height':950})
                for i,font in enumerate(FONTS):
                    choose(page,font,keyboard=True)
                    for other in (font,FONTS[(i+1)%3]):
                        target=tile(page,other)
                        target.hover()
                        settle(page)
                        assert target.evaluate("e=>e.matches(':hover')")
                        compare(theme,font,('hover',other,w))
                        page.mouse.move(0,0)
                        page.keyboard.press('Tab')
                        target.focus()
                        settle(page)
                        assert target.evaluate("e=>e.matches(':focus-visible')")
                        compare(theme,font,('focus',other,w))
                        rest(page)
            page.set_viewport_size({'width':1440,'height':950})
            for font in FONTS:
                choose(page,font)
                page.locator('#settings-back').click()
                page.wait_for_function("()=>!document.body.classList.contains('settings-view')&&!galleryStageTransition&&!galleryStageFadeInProgress")
                open_typography(page)
                rest(page)
                compare(theme,font,'close and reopen')
                page.reload(wait_until='domcontentloaded')
                setup(page,baseline,candidate)
                assert page.evaluate("state.font")==font
                assert page.evaluate("localStorage.getItem('gallery.font')")==font
                open_typography(page)
                set_theme(theme)
                compare(theme,font,'same-origin reload')
            page.locator('#appearance-typography-tab').focus()
            page.locator('#appearance-typography-tab').press('ArrowLeft')
            assert page.locator('#appearance-theme-pane').is_visible()
            page.locator('#appearance-theme-tab').press('ArrowRight')
            settle(page)
            assert page.locator('#appearance-typography-tab').get_attribute('aria-selected')=='true'
            assert page.locator('#appearance-typography-tab').evaluate("e=>e===document.activeElement")
            compare(theme,'inter','keyboard tab navigation')
            page.locator('#search').click()
            page.locator('#header-search-input').fill('Typography')
            page.locator('[data-settings-search-key="font"]').click()
            assert page.locator('#settings-font-card').evaluate("e=>e===document.activeElement")
            assert page.locator('#search').get_attribute('aria-expanded')=='false'
            page.wait_for_function("()=>!document.querySelector('.settings-search-target')",timeout=10000)
            settle(page)
            compare(theme,'inter','actual Settings search deep link')
            assert not errors,(mode,motion,theme,errors)
            print('PASS: Typography theme',mode,motion,theme,'68 comparisons; all fonts, widths, selection, reload, search, hover/focus',flush=True)
        page.close()
        browser.close()
    assert count==EXPECTED==408,(mode,motion,count,EXPECTED)
    print('PASS: Q2-B5 actual DOM equivalence',mode,motion,count,'comparisons',flush=True)
