#!/usr/bin/env python3
"""Q2-B8: exact CSS scope, actual Player DOM and browser fullscreen."""
import hashlib,re,runpy,subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright
S=runpy.run_path("gallery/changes/pending/2026-11-14-q2b8-player.py")
THEMES=("ocean","twilight","ember","slate","glacier","verdant")
WIDTHS=(1440,751,750,741,740,721,720,601,600,571,570,561,560,501,500,441,440,391,390,370)
STYLE=re.compile(br'<style>(.*?)</style>',re.S)
EXPECTED=6*(len(WIDTHS)+2*17)
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
    assert S["transform"](base)==css and len(before)-len(after)==124
    print("PASS: exact eight-declaration, 124-byte CSS-only deletion",path,flush=True)
    return after.decode(),base.decode(),css.decode()
COMPARE=r"""()=>{
 const style=document.querySelector('style'),candidate=window.__q2candidate,baseline=window.__q2baseline;
 if(style.textContent!==candidate)throw Error('Unexpected stylesheet');
 const root=document.querySelector('.playback-page');
 if(!root||!root.getClientRects().length)throw Error('Missing actual Player');
 for(const s of ['.playback-compactbar','.playback-title-inline','#back-from-playback','#player-area','#local-video','#player-overlay','.player-episode-nav','.player-episode-label'])
   if(!root.querySelector(s))throw Error('Missing actual Player node '+s);
 const nodes=new Set([root]);
 for(const e of root.querySelectorAll('*'))
   if(!e.closest('[hidden]')&&e.getClientRects().length)nodes.add(e);
 for(let p=root.parentElement;p;p=p.parentElement)nodes.add(p);
 for(const e of document.querySelectorAll('.top,.brand-row,.toolbar'))
   if(e.getClientRects().length)nodes.add(e);
 function snap(){
   return Array.from(nodes,e=>{
     const r=e.getBoundingClientRect(),s=getComputedStyle(e);
     return {tag:e.tagName,cls:e.getAttribute('class'),id:e.id,
       props:Array.from(s,k=>[k,s.getPropertyValue(k)]),
       pseudo:['::before','::after'].map(k=>{const p=getComputedStyle(e,k);return Array.from(p,n=>[n,p.getPropertyValue(n)]);}),
       rect:[r.x,r.y,r.width,r.height,e.clientWidth,e.clientHeight,e.scrollWidth,e.scrollHeight],
       state:[e.matches(':hover'),e.matches(':focus-visible'),e.matches(':disabled'),e.matches(':fullscreen'),e.getAttribute('aria-label'),e.getAttribute('aria-pressed'),e.hidden],
       text:e.matches('.playback-title-inline,.player-episode-label,.player-episode-slot,#back-from-playback')?e.innerText:null};
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
   return {nodes:a.length,fullscreen:document.fullscreenElement?.id||null};
 }finally{if(style.textContent!==candidate)style.textContent=candidate;}
}"""
def settle(page,ms=700):
    page.wait_for_function("()=>!galleryStageTransition&&!galleryStageFadeInProgress",timeout=10000)
    page.wait_for_timeout(ms)
def rest(page):
    page.mouse.move(0,0);page.evaluate("()=>document.activeElement?.blur()");settle(page)
def playback(page,id,release,episode):
    page.wait_for_function("()=>!!state.playback && !galleryStageTransition&&!galleryStageFadeInProgress",timeout=10000)
    assert page.evaluate("()=>[state.detailId,state.playback.installmentId,state.playback.episode]")==[id,release,episode]
    assert page.locator('#player-area').is_visible()
    assert page.locator('.playback-title-inline strong').inner_text()==page.evaluate("()=>demo.find(x=>x.id===state.detailId).name")
    assert page.locator('#back-from-playback').inner_text().strip()=="Back to episodes"
    assert page.locator('.player-episode-label strong').inner_text()==('The Quintessential Quintuplets Movie' if release=='quints-movie' else 'Episode '+str(episode))
    assert page.locator('.player-episode-label small').inner_text()==('Movie' if release=='quints-movie' else 'Season '+str(page.evaluate("state.detailSeason")+1))
    info=page.evaluate("""()=>{
      const label=document.querySelector('.player-episode-label small'),s=getComputedStyle(label);
      const buttons=[-1,1].map(step=>{
        const b=document.getElementById(step===-1?'previous-episode':'next-episode'),n=playbackNeighbor(step);
        return {exists:!!b,expected:!!n,label:b?.getAttribute('aria-label'),want:n?.label,
          full:b?getComputedStyle(b.querySelector('.nav-label-full')).display:null,
          compact:b?getComputedStyle(b.querySelector('.nav-label-compact')).display:null};
      });
      const slots=[...document.querySelectorAll('.player-episode-slot')].map(e=>e.getBoundingClientRect().width);
      return {small:[s.whiteSpace,s.overflowX,s.textOverflow],buttons,slots,width:innerWidth,
         hidden:document.querySelector('#player-empty').hidden};
    }""")
    assert info['small']==['nowrap','hidden','ellipsis'],info
    assert len(info['slots'])==2 and abs(info['slots'][0]-info['slots'][1])<2,info
    for q in info['buttons']:
        assert q['exists']==q['expected'],info
        if q['exists']:
            assert q['label']==q['want'],q
            assert (q['full']=='none')==(info['width']<=560),q
            assert (q['compact']!='none')==(info['width']<=560),q
def detail(page,id):
    page.locator('[data-detail="'+id+'"]').first.click()
    page.wait_for_function("(id)=>state.detailId===id&&!galleryStageFadeInProgress&&!galleryStageTransition",arg=id,timeout=10000)
    assert page.locator('#detail-back').is_visible()
    rest(page)
def watch(page,id,release,episode):
    target=page.locator('.episode-actions [data-episode-action="watch"][data-episode="'+str(episode)+'"]')
    if target.count()==0:
        target=page.locator('.detail-actions [data-episode-action="watch"][data-episode="'+str(episode)+'"]')
    assert target.count()==1 and target.is_enabled()
    target.click();settle(page);rest(page);playback(page,id,release,episode)
    assert page.locator('#player-empty').is_visible() and page.locator('#pause-play').is_disabled() and page.locator('#seek').is_disabled()
def navigate(page,step,id,release,episode):
    target=page.locator('#next-episode' if step==1 else '#previous-episode')
    assert target.is_visible() and target.is_enabled()
    target.click();rest(page);playback(page,id,release,episode)
    assert page.locator('#player-empty').is_visible()
def back(page,id,release,episode,keyboard=False):
    target=page.locator('#back-from-playback')
    if keyboard:
        page.keyboard.press('Tab');target.focus();assert target.evaluate("e=>e.matches(':focus-visible')")
        target.press('Enter')
    else:target.click()
    page.wait_for_function("()=>!state.playback&&!galleryStageTransition&&!galleryStageFadeInProgress",timeout=10000)
    assert page.evaluate("()=>[state.detailId,activeInstallment(demo.find(x=>x.id===state.detailId)).id,state.detailEpisode]")==[id,release,episode]
    assert page.locator('#detail-back').is_visible()
    rest(page)
def to_gallery(page):
    page.locator('#detail-back').click()
    page.wait_for_function("()=>!state.detailId&&!galleryStageFadeInProgress&&!galleryStageTransition",timeout=10000)
    rest(page)
def dimensions(page):
    return page.evaluate("""()=>['#player-area','.playback-compactbar','.player-episode-nav'].map(q=>{
      const r=document.querySelector(q).getBoundingClientRect();return [r.width,r.height];
    })""")
def fullscreen_geometry(page):
    return page.evaluate("""()=>{
      const a=document.querySelector('#player-area'),v=document.querySelector('#local-video'),s=getComputedStyle(a),r=a.getBoundingClientRect(),vr=v.getBoundingClientRect();
      return {actual:document.fullscreenElement===a,rect:[r.x,r.y,r.width,r.height],
        video:[vr.x,vr.y,vr.width,vr.height],window:[innerWidth,innerHeight],
        border:[s.borderTopWidth,s.borderRightWidth,s.borderBottomWidth,s.borderLeftWidth],
        radius:[s.borderTopLeftRadius,s.borderTopRightRadius,s.borderBottomLeftRadius,s.borderBottomRightRadius],
        fit:getComputedStyle(v).objectFit,align:s.alignItems,justify:s.justifyContent};
    }""")
def verify_fullscreen(page):
    g=fullscreen_geometry(page)
    assert g['actual'] and g['border']==['0px']*4 and g['radius']==['0px']*4,g
    assert g['fit']=='contain' and g['align']=='center' and g['justify']=='center',g
    assert all(abs(x-y)<=1 for x,y in zip(g['rect'],[0,0]+g['window'])),g
    assert all(abs(x-y)<=1 for x,y in zip(g['rect'],g['video'])),g
def overlay(page,hidden,motion):
    g=page.evaluate("""()=>{
      const a=document.querySelector('#player-area'),o=document.querySelector('#player-overlay'),b=document.querySelector('#fullscreen');
      const s=getComputedStyle(o),r=b.getBoundingClientRect(),hit=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);
      return {hidden:a.classList.contains('controls-hidden'),opacity:s.opacity,pointer:getComputedStyle(b).pointerEvents,
       hit:!!hit&&b.contains(hit),duration:s.transitionDuration};
    }""")
    assert g['hidden']==hidden and g['opacity']==('0' if hidden else '1'),g
    assert (g['pointer']=='none')==hidden and g['hit']!=hidden,g
    if motion=='reduce':assert all(float(x.strip().removesuffix('s'))==0 for x in g['duration'].split(',')),g
def run(mode,motion):
    html,baseline,candidate=exact_pair(mode)
    count=0;fullscreen_count=0
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
        def new_page(theme,w):
            page=browser.new_page(viewport={'width':w,'height':950},screen={'width':w,'height':950},reduced_motion=motion)
            errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
            page.set_content(html,wait_until='domcontentloaded')
            page.evaluate("""({baseline,candidate,theme})=>{
              window.__q2baseline=baseline;window.__q2candidate=candidate;
              if(document.querySelector('style').textContent!==candidate)throw Error('Wrong stylesheet');
              state.theme=theme;document.body.dataset.theme=theme;
              state.defaultPlayback='sub';
            }""",{'baseline':baseline,'candidate':candidate,'theme':theme})
            rest(page)
            return page,errors
        def compare(page,theme,label,full=False):
            nonlocal count
            result=page.evaluate(COMPARE)
            assert 'error' not in result,(mode,motion,theme,label,result)
            assert result['nodes']>20 and result['fullscreen']==('player-area' if full else None),result
            count+=1
        def interaction(page,theme,target,label):
            assert target.is_visible() and target.is_enabled()
            target.hover();settle(page)
            assert target.evaluate("e=>e.matches(':hover')")
            compare(page,theme,(label,'hover'))
            page.mouse.move(0,0);page.keyboard.press('Tab');target.focus();settle(page)
            assert target.evaluate("e=>e.matches(':focus-visible')")
            compare(page,theme,(label,'focus'));rest(page)
        for theme in THEMES:
            page,errors=new_page(theme,1440)
            detail(page,'demo:aot');watch(page,'demo:aot','aot-s1',12)
            for w in WIDTHS:
                page.set_viewport_size({'width':w,'height':950});rest(page)
                playback(page,'demo:aot','aot-s1',12)
                compare(page,theme,('middle episode, no media',w))
            assert not errors,errors;page.close()
            for w in (1440,370):
                page,errors=new_page(theme,w)
                detail(page,'demo:aot');watch(page,'demo:aot','aot-s1',1)
                assert page.locator('#previous-episode').count()==0
                compare(page,theme,('first',w))
                navigate(page,1,'demo:aot','aot-s1',2);compare(page,theme,('next',w))
                navigate(page,-1,'demo:aot','aot-s1',1);compare(page,theme,('previous',w))
                back(page,'demo:aot','aot-s1',1)
                watch(page,'demo:aot','aot-s1',25)
                assert page.locator('#next-episode').get_attribute('aria-label')=='Next season'
                assert not page.evaluate("playerCanAdvance()")
                compare(page,theme,('last',w))
                navigate(page,1,'demo:aot','aot-s2',1)
                assert page.locator('#previous-episode').get_attribute('aria-label')=='Previous season'
                compare(page,theme,('next season',w))
                navigate(page,-1,'demo:aot','aot-s1',25);compare(page,theme,('previous season',w))
                back(page,'demo:aot','aot-s1',25,keyboard=True);to_gallery(page)
                detail(page,'demo:quints')
                movie=page.locator('[data-inline-installment="quints-movie"]')
                page.keyboard.press('Tab');movie.focus();movie.press('Enter');settle(page)
                assert page.evaluate("state.detailRelated")=='quints-movie'
                watch(page,'demo:quints','quints-movie',1)
                assert page.locator('#next-episode').count()==page.locator('#previous-episode').count()==0
                compare(page,theme,('movie',w))
                back(page,'demo:quints','quints-movie',1)
                season=page.locator('[data-inline-installment="quints-s1"]')
                page.keyboard.press('Tab');season.focus();season.press('Enter');settle(page)
                assert page.evaluate("state.detailRelated") is None
                watch(page,'demo:quints','quints-s1',5)
                compare(page,theme,('long title',w))
                interaction(page,theme,page.locator('#back-from-playback'),('Back',w))
                interaction(page,theme,page.locator('#next-episode'),('next episode',w))
                page.locator('#sf-player-demo-start').click();settle(page);rest(page)
                assert page.evaluate("sfPlayerDemo.active&&!sfPlayerDemo.playing")
                assert page.locator('#pause-play').is_enabled() and page.locator('#seek').is_enabled()
                compare(page,theme,('paused simulation',w))
                before=dimensions(page)
                # Real user activation; no synthetic fullscreen selectors or mocking.
                assert page.evaluate("document.fullscreenEnabled")
                page.locator('#fullscreen').click()
                page.wait_for_function("()=>document.fullscreenElement===document.querySelector('#player-area')",timeout=10000)
                settle(page);verify_fullscreen(page);overlay(page,False,motion)
                compare(page,theme,('actual fullscreen paused',w),True)
                fullscreen_count+=1
                page.locator('#pause-play').click()
                assert page.evaluate("sfPlayerDemo.playing")
                page.wait_for_function("()=>document.querySelector('#player-area').classList.contains('controls-hidden')",timeout=10000)
                settle(page);overlay(page,True,motion);verify_fullscreen(page)
                compare(page,theme,('actual fullscreen hidden controls',w),True)
                # Wake via pointer movement, then pause using the real button.
                area=page.locator('#player-area').bounding_box()
                page.mouse.move(area['x']+area['width']/2,area['y']+area['height']/2)
                page.wait_for_function("()=>!document.querySelector('#player-area').classList.contains('controls-hidden')")
                settle(page)
                page.locator('#pause-play').click();settle(page)
                assert page.evaluate("sfPlayerDemo.active&&!sfPlayerDemo.playing")
                overlay(page,False,motion);verify_fullscreen(page)
                compare(page,theme,('actual fullscreen wake and pause',w),True)
                page.locator('#fullscreen').click()
                page.wait_for_function("()=>document.fullscreenElement===null",timeout=10000)
                settle(page)
                after=dimensions(page)
                assert all(abs(x-y)<=1 for a,b in zip(before,after) for x,y in zip(a,b)),(before,after)
                playback(page,'demo:quints','quints-s1',5)
                assert page.evaluate("sfPlayerDemo.active&&!sfPlayerDemo.playing")
                compare(page,theme,('actual fullscreen exited',w))
                back(page,'demo:quints','quints-s1',5,keyboard=True)
                assert not errors,(theme,w,errors)
                page.close()
            print('PASS: Player theme',mode,motion,theme,'54 comparisons, two actual fullscreen cycles',flush=True)
        browser.close()
    assert count==EXPECTED==324 and fullscreen_count==12,(mode,motion,count,fullscreen_count)
    print('PASS: Q2-B8 actual DOM equivalence',mode,motion,count,'comparisons;',fullscreen_count,'actual fullscreen cycles',flush=True)
