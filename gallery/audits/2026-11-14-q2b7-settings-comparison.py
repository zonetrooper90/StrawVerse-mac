#!/usr/bin/env python3
"""Q2-B7: exact Settings CSS-only scope and real mounted DOM equivalence."""
import hashlib,re,runpy,subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright
S=runpy.run_path("gallery/changes/pending/2026-11-14-q2b7-settings.py")
THEMES=("ocean","twilight","ember","slate","glacier","verdant")
WIDTHS=(1440,1101,1100,1051,1050,751,750,711,710,701,700,531,530,521,520,441,440,370)
PARENT={"credits":"overview","components":"credits","licenses":"overview","legal":"overview","terms":"legal","privacy":"legal","copyright":"legal"}
BACK={"overview":"Back to Gallery","credits":"Back to About","components":"Back to Acknowledgements","licenses":"Back to About","legal":"Back to About","terms":"Back to Legal & Privacy","privacy":"Back to Legal & Privacy","copyright":"Back to Legal & Privacy"}
SECTIONS=("appearance","playback","downloads","sources","about")
STYLE=re.compile(br'<style>(.*?)</style>',re.S)
# 18 shared widths + 8 additional views at 3 widths + 7 nested About
# pages at 2 widths + 4 search states at 2 widths + 6 interaction states
# at 2 widths + 2 scrolled layout states + 2 close/reopen states.
EXPECTED=6*(len(WIDTHS)+8*3+7*2+4*2+6*2+2+2)
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
    assert S["transform"](base)==css and len(before)-len(after)==361
    print("PASS: exact eighteen-declaration, 361-byte CSS-only deletion",path,flush=True)
    return after.decode(),base.decode(),css.decode()

COMPARE=r"""()=>{
 const style=document.querySelector('style'),candidate=window.__q2candidate,baseline=window.__q2baseline;
 if(style.textContent!==candidate)throw Error('Unexpected stylesheet');
 const root=document.querySelector('#settings-page');
 const required=['.settings-page-head','#settings-back','.settings-layout','.settings-side','.settings-content'];
 if(!root||root.hidden||required.some(s=>!root.querySelector(s)?.getClientRects().length))
    throw Error('Missing actual Settings layout');
 const nodes=new Set([root]);
 for(const e of root.querySelectorAll('*'))
   if(!e.closest('[hidden]')&&e.getClientRects().length)nodes.add(e);
 for(let p=root.parentElement;p;p=p.parentElement)nodes.add(p);
 for(const e of document.querySelectorAll('.top,.brand-row,.brand,.toolbar,#header-search,#header-search-input'))
   if(e.getClientRects().length)nodes.add(e);
 function snap(){
   return Array.from(nodes,e=>{
     const r=e.getBoundingClientRect(),s=getComputedStyle(e);
     return {tag:e.tagName,cls:e.getAttribute('class'),props:Array.from(s,k=>[k,s.getPropertyValue(k)]),
       pseudo:['::before','::after'].map(k=>{const p=getComputedStyle(e,k);return Array.from(p,n=>[n,p.getPropertyValue(n)]);}),
       rect:[r.x,r.y,r.width,r.height,e.clientWidth,e.clientHeight,e.scrollWidth,e.scrollHeight,e.scrollTop||0,e.scrollLeft||0],
       state:[e.matches(':hover'),e.matches(':focus-visible'),e.matches(':disabled'),e.getAttribute('aria-label'),e.getAttribute('aria-current'),e.getAttribute('aria-selected'),e.getAttribute('aria-pressed'),e.hidden],
       text:e.matches('.settings-card-title,.settings-section-button,.settings-back,.settings-panel-head,.settings-result-item')?e.innerText:null};
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
     for(let j=0;j<x.props.length;j++)if(x.props[j][0]!==y.props[j][0]||x.props[j][1]!==y.props[j][1])
       return {...info,error:x.props[j][0],before:x.props[j][1],after:y.props[j][1]};
     if(JSON.stringify(x.pseudo)!==JSON.stringify(y.pseudo))return {...info,error:'pseudo style'};
     if(x.rect.some((v,j)=>Math.abs(v-y.rect[j])>0.02))return {...info,error:'geometry',before:x.rect,after:y.rect};
     for(const k of ['state','text'])if(JSON.stringify(x[k])!==JSON.stringify(y[k]))return {...info,error:k};
   }
   return {nodes:a.length,disabled:Array.from(nodes).filter(e=>e.matches(':disabled')).length};
 }finally{if(style.textContent!==candidate)style.textContent=candidate;}
}"""
def settle(page,ms=520):
    page.wait_for_function("()=>!galleryStageTransition&&!galleryStageFadeInProgress&&!gallerySettingsOpening&&!settingsClosing&&settingsScrollFrame===null",timeout=10000)
    page.wait_for_timeout(ms)
    page.wait_for_function("()=>!galleryStageTransition&&!galleryStageFadeInProgress&&settingsScrollFrame===null",timeout=10000)
def rest(page,reset=False):
    page.mouse.move(0,0);page.evaluate("()=>document.activeElement?.blur()")
    if reset:page.evaluate("()=>{workspace.scrollTo({top:0,behavior:'instant'});}")
    settle(page)
def resize(page,w):
    page.set_viewport_size({'width':w,'height':950});rest(page,True)
def section(page,key):
    button=page.locator('[data-settings-section="'+key+'"]')
    button.click();rest(page)
    assert page.evaluate("settingsLastSection")==key
    assert page.locator('[data-settings-panel="'+key+'"]').is_visible()
    assert button.get_attribute('aria-current')=='page'
    assert page.locator('.settings-section-button[aria-current="page"]').count()==1
    assert page.locator('#settings-back').get_attribute('aria-label')=='Back to Gallery'
def tab(page,group,key):
    target=page.locator('[data-'+group+'-tab="'+key+'"]')
    target.click();rest(page)
    assert target.get_attribute('aria-selected')=='true'
    if group=='source':
        assert page.locator('#sources-'+key+'-region' if key!='repositories' else '#settings-repositories-card').is_visible()
    else:assert page.locator('[data-'+group+'-pane="'+key+'"]').is_visible()
def about_verify(page,view):
    assert page.evaluate("currentAboutView")==view
    assert page.locator('[data-about-view="'+view+'"]').is_visible()
    assert page.locator('#settings-back').get_attribute('aria-label')==BACK[view]
    assert page.locator('#settings-back').get_attribute('title')==BACK[view]
def about_go(page,view):
    page.locator('[data-about-open="'+view+'"]').click();rest(page)
    about_verify(page,view)
def about_back(page,view):
    page.locator('#settings-back').click();rest(page)
    about_verify(page,PARENT[view])
def open_settings(page):
    page.locator('#settings').click()
    page.wait_for_function("()=>document.body.classList.contains('settings-view')&&!galleryStageFadeInProgress&&!gallerySettingsOpening",timeout=10000)
    rest(page)
    assert page.locator('#appearance-theme-pane').is_visible()
def close_settings(page):
    page.locator('#settings-back').click()
    page.wait_for_function("()=>!document.body.classList.contains('settings-view')&&!galleryStageFadeInProgress&&!settingsClosing",timeout=10000)
    assert page.evaluate("state.view")== 'discover'
    assert not page.evaluate("tabPagesViewport.inert")
def run(mode,motion):
    html,baseline,candidate=exact_pair(mode)
    count=0;disabled_seen=0
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
        page=browser.new_page(viewport={'width':1440,'height':950},reduced_motion=motion)
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.set_content(html,wait_until='domcontentloaded')
        page.evaluate("""({baseline,candidate})=>{
          window.__q2baseline=baseline;window.__q2candidate=candidate;
          if(document.querySelector('style').textContent!==candidate)throw Error('Wrong stylesheet');
        }""",{'baseline':baseline,'candidate':candidate})
        open_settings(page)
        assert page.locator('[data-settings-section]').count()==len(SECTIONS)
        def compare(theme,label):
            nonlocal count,disabled_seen
            result=page.evaluate(COMPARE)
            assert 'error' not in result,(mode,motion,theme,label,result)
            assert result['nodes']>20,result
            disabled_seen+=result['disabled'];count+=1
        def interaction(theme,target,label):
            assert target.is_visible() and target.is_enabled()
            target.hover();settle(page)
            assert target.evaluate("e=>e.matches(':hover')")
            compare(theme,(label,'hover'))
            page.mouse.move(0,0);page.keyboard.press('Tab');target.focus();settle(page)
            assert target.evaluate("e=>e.matches(':focus-visible')")
            compare(theme,(label,'keyboard focus'))
            rest(page)
        for theme in THEMES:
            page.evaluate("(t)=>{state.theme=t;document.body.dataset.theme=t;}",theme)
            section(page,'appearance');tab(page,'appearance','theme')
            for w in WIDTHS:
                resize(page,w)
                compare(theme,('shared layout/theme',w))
            for w in (1440,710,370):
                resize(page,w);section(page,'appearance');tab(page,'appearance','typography')
                compare(theme,('typography',w))
                section(page,'playback');tab(page,'playback','general')
                compare(theme,('playback general',w))
                tab(page,'playback','subtitles')
                # Sample genuine disabled effect controls at the mobile layout
                # boundary; restore the previous style using the actual button.
                if w==710:
                    effect=page.evaluate("subtitlePrefs.effect")
                    page.locator('[data-subtitle-effect="none"]').click();rest(page)
                    assert page.locator('#subtitle-effect-color').is_disabled()
                    compare(theme,('subtitles disabled controls',w))
                    page.locator('[data-subtitle-effect="'+effect+'"]').click();rest(page)
                else:compare(theme,('subtitles',w))
                section(page,'downloads');compare(theme,('downloads',w))
                section(page,'sources')
                for source in ('installed','marketplace','repositories'):
                    tab(page,'source',source);compare(theme,(source,w))
                section(page,'about');about_verify(page,'overview')
                compare(theme,('about overview',w))
            for w in (1440,370):
                resize(page,w);section(page,'about');about_verify(page,'overview')
                about_go(page,'credits');compare(theme,('credits',w))
                about_go(page,'components');compare(theme,('components',w))
                about_back(page,'components');about_back(page,'credits')
                about_go(page,'licenses');compare(theme,('licenses',w));about_back(page,'licenses')
                about_go(page,'legal');compare(theme,('legal',w))
                for child in ('terms','privacy','copyright'):
                    about_go(page,child);compare(theme,(child,w));about_back(page,child)
                about_back(page,'legal')
                # Real Settings search, including the active nav suppression.
                section(page,'appearance');page.locator('#search').click();settle(page)
                results=page.locator('#settings-search-results')
                assert results.is_visible() and page.locator('.settings-section-button[aria-current="page"]').count()==0
                assert results.locator('.settings-search-placeholder').is_visible()
                compare(theme,('search empty',w))
                query=page.locator('#header-search-input')
                query.fill('zzzzno-matching-gallery-settings');settle(page)
                assert results.locator('.settings-search-no-results').is_visible()
                compare(theme,('search no match',w))
                query.fill('Typography');settle(page)
                found=page.locator('[data-settings-search-key="font"]')
                assert found.is_visible()
                compare(theme,('search matches',w))
                found.click()
                assert page.locator('#settings-font-card').evaluate("e=>e===document.activeElement")
                assert page.locator('#search').get_attribute('aria-expanded')=='false'
                page.wait_for_function("()=>!document.querySelector('.settings-search-target')",timeout=10000)
                settle(page);assert page.locator('#appearance-typography-pane').is_visible()
                compare(theme,('search deep link',w))
                # Three real hover and keyboard-focus states.
                interaction(theme,page.locator('#settings-back'),('Back',w))
                interaction(theme,page.locator('[data-settings-section="appearance"]'),('active nav',w))
                interaction(theme,page.locator('[data-settings-section="downloads"]'),('inactive nav',w))
                # Activate section with keyboard, then verify real Back.
                target=page.locator('[data-settings-section="downloads"]')
                page.keyboard.press('Tab');target.focus();target.press('Enter');settle(page)
                assert page.evaluate("settingsLastSection")=='downloads'
                close_settings(page);open_settings(page)
                compare(theme,('close/reopen',w))
            resize(page,1440)
            page.set_viewport_size({'width':1440,'height':620});rest(page,True)
            section(page,'playback');tab(page,'playback','subtitles')
            # Sticky sidebar remains at its computed position when workspace scrolls.
            sidebar=page.locator('.settings-side')
            assert sidebar.evaluate("e=>getComputedStyle(e).position")== 'sticky'
            amount=page.evaluate("()=>Math.min(150,workspace.scrollHeight-workspace.clientHeight)")
            assert amount>10
            page.evaluate("n=>workspace.scrollTo({top:n,behavior:'instant'})",amount);settle(page)
            assert page.evaluate("workspace.scrollTop")>10
            compare(theme,'desktop sticky scroll')
            resize(page,370);section(page,'appearance')
            data=sidebar.evaluate("e=>({position:getComputedStyle(e).position,direction:getComputedStyle(e).flexDirection,overflow:getComputedStyle(e).overflowX,max:e.scrollWidth-e.clientWidth})")
            assert data['position']=='static' and data['direction']=='row' and data['overflow']=='auto' and data['max']>10,data
            sidebar.evaluate("(e,n)=>e.scrollTo({left:n,behavior:'instant'})",data['max']);settle(page)
            assert sidebar.evaluate("e=>e.scrollLeft")>10
            compare(theme,'narrow horizontal scroll')
            assert not errors,(mode,motion,theme,errors)
            print('PASS: Settings theme',mode,motion,theme,'80 comparisons',flush=True)
        page.close();browser.close()
    assert count==EXPECTED==480,(mode,motion,count,EXPECTED)
    assert disabled_seen>0,('No real disabled controls sampled',mode,motion)
    print('PASS: Q2-B7 actual DOM equivalence',mode,motion,count,'comparisons',flush=True)
