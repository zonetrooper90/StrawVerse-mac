#!/usr/bin/env python3
"""Real first-season partial click must animate, not snap; no application edits."""
import os,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
HTML=Path(sys.argv[1]).read_text(encoding='utf-8')
THEMES=('ocean','twilight','ember','slate','glacier','verdant')
FIRST='aot-s1'
SECOND='aot-s2'
RAIL='#inline-installment-rail'
GEOM=r"""()=>{
 const e=document.querySelector('#inline-installment-rail'),v=e.closest('.inline-release-viewport');
 const r=e.getBoundingClientRect(),l=v.querySelector('.inline-release-fade-left'),
       right=v.querySelector('.inline-release-fade-right');
 return {x:e.scrollLeft,max:e.scrollWidth-e.clientWidth,w:e.clientWidth,origin:r.left,y:r.top+r.height/2,
  l:l.getBoundingClientRect().width,r:right.getBoundingClientRect().width,
  left:v.classList.contains('can-left'),right:v.classList.contains('can-right'),
  guardL:v.classList.contains('guard-left'),guardR:v.classList.contains('guard-right'),
  snap:getComputedStyle(e).scrollSnapType,vertical:workspace.scrollTop,
  verticalMax:Math.max(0,workspace.scrollHeight-workspace.clientHeight),pageY:window.scrollY,
  cards:[...e.children].map(c=>{const b=c.getBoundingClientRect();return {id:c.dataset.inlineInstallment,
    a:b.left-r.left+e.scrollLeft,b:b.right-r.left+e.scrollLeft,selected:c.getAttribute('aria-current')==='true'};})};
}"""
TRACE=r"""()=>{
 const rail=document.querySelector('#inline-installment-rail'),nav=rail.closest('.inline-installments');
 const original=rail.scrollTo,trace={frames:[],calls:[],preClick:null,postClick:null,removed:false,originalRail:true};
 window.__firstRevealTrace=trace;
 const observer=new MutationObserver(records=>{
   for(const record of records)for(const node of record.removedNodes)
     if(node===nav||node===rail||node.contains?.(rail))trace.removed=true;
 });
 observer.observe(nav.parentElement,{childList:true,subtree:true});
 rail.scrollTo=function(...args){trace.calls.push(args[0]);return original.apply(this,args);};
 let frame=0;
 function capture(event){
   if(event.target.closest('[data-inline-installment]')?.dataset.inlineInstallment!=='aot-s1')return;
   trace.preClick=rail.scrollLeft;
   const start=performance.now();
   function sample(time){
     trace.frames.push({t:time-start,x:rail.scrollLeft,connected:rail.isConnected});
     if(time-start<850)frame=requestAnimationFrame(sample);
   }
   frame=requestAnimationFrame(sample);
 }
 function bubble(event){
   if(event.target.closest('[data-inline-installment]')?.dataset.inlineInstallment!=='aot-s1')return;
   trace.postClick=rail.scrollLeft;
   trace.originalRail=rail===document.querySelector('#inline-installment-rail');
 }
 document.addEventListener('click',capture,true);
 document.addEventListener('click',bubble,false);
 window.__finishFirstTrace=()=>{
   cancelAnimationFrame(frame);observer.disconnect();rail.scrollTo=original;
   document.removeEventListener('click',capture,true);
   document.removeEventListener('click',bubble,false);
   return trace;
 };
}"""
def geom(page):return page.evaluate(GEOM)
def card(g,id):return next(c for c in g['cards'] if c['id']==id)
def rail(page):return page.locator(RAIL)
def arrow(page,side):return page.locator('[data-inline-scroll="'+str(side)+'"]')
def settle(page,ms=650):
    page.wait_for_function("()=>!galleryStageFadeInProgress&&!galleryStageTransition",timeout=10000)
    page.wait_for_timeout(ms)
def position(page,x):
    page.mouse.move(0,0)
    page.evaluate("()=>document.activeElement?.blur()")
    # Only the initial offset is controlled, to reliably create the clipped
    # card regardless of proximity snapping. Selection is a real pointer click.
    rail(page).evaluate("(e,x)=>{e.style.scrollSnapType='none';e.scrollTo({left:x,behavior:'instant'});}",x)
    settle(page,320)
    g=geom(page)
    assert abs(g['x']-x)<=1,(x,g)
    assert not g['guardL'] and not g['guardR'],g
    return g
def hit(page,id):
    g=geom(page);c=card(g,id)
    a=max(c['a'],g['x']+(g['l'] if g['left'] else 0))
    b=min(c['b'],g['x']+g['w']-(g['r'] if g['right'] else 0))
    assert b-a>12,(id,g)
    x=g['origin']+(a+b)/2-g['x'];y=g['y']
    page.mouse.move(x,y)
    assert page.evaluate("({x,y,id})=>document.elementFromPoint(x,y)?.closest('[data-inline-installment]')?.dataset.inlineInstallment===id",dict(x=x,y=y,id=id)),(id,g)
    before=geom(page)
    page.mouse.click(x,y)
    return before
def choose_second(page):
    g=geom(page);c=card(g,SECOND)
    clear=g['w']-g['l']-g['r']
    x=round(c['a']-g['l']-(clear-(c['b']-c['a']))/2)
    position(page,max(0,min(g['max'],x)))
    hit(page,SECOND);settle(page)
    assert card(geom(page),SECOND)['selected']
def first_case(page,motion,selected):
    g=geom(page)
    assert card(g,FIRST)['selected']==selected,g
    c=card(g,FIRST);offset=round((c['b']-c['a']-g['l'])/2)
    assert offset>24,(offset,g)
    g=position(page,offset);c=card(g,FIRST)
    assert g['left'] and g['right'] and c['a']<g['x']+g['l']<c['b'],g
    assert c['b']<=g['x']+g['w']-g['r']+0.5,g
    page.evaluate(TRACE)
    before=hit(page,FIRST)
    page.wait_for_function("""()=>{
      const e=document.querySelector('#inline-installment-rail');
      return e.scrollLeft<=0.5 && e.querySelector('[data-inline-installment="aot-s1"]').getAttribute('aria-current')==='true';
    }""",timeout=5000)
    page.wait_for_function("()=>window.__firstRevealTrace.frames.length>=2",timeout=5000)
    settle(page,320)
    trace=page.evaluate("window.__finishFirstTrace()")
    after=geom(page)
    assert trace['preClick'] is not None and trace['postClick'] is not None,trace
    assert abs(trace['preClick']-before['x'])<=1,('Pre-click jump',before,trace)
    assert trace['originalRail'] and not trace['removed'] and all(f['connected'] for f in trace['frames']),trace
    assert trace['calls'] and trace['calls'][-1]['behavior']==('instant' if motion=='reduce' else 'smooth'),trace
    assert abs(trace['calls'][-1]['left'])<=0.5,trace
    middle=[f['x'] for f in trace['frames'] if 1<f['x']<before['x']-1]
    if motion=='reduce':
        assert abs(trace['postClick'])<=1 and not middle,('Reduced motion animated',trace)
    else:
        assert abs(trace['postClick']-before['x'])<=2,('Abrupt jump during selection',trace)
        assert middle,('No actual intermediate animation frame',trace)
        seq=[trace['postClick']]+[f['x'] for f in trace['frames']]
        assert all(b<=a+1 for a,b in zip(seq,seq[1:])),('Motion reversed',trace)
    assert after['x']<=0.5 and not after['left'] and after['right'],after
    c=card(after,FIRST)
    assert c['a']>=-0.5 and c['b']<=after['w']-after['r']+0.5,after
    assert [x['id'] for x in after['cards'] if x['selected']]==[FIRST]
    assert abs(after['vertical']-min(before['vertical'],after['verticalMax']))<=1 and after['pageY']==before['pageY'],(before,after)
    assert not after['guardL'] and arrow(page,-1).is_disabled(),after
    print('PASS first-season reveal',motion,'already selected' if selected else 'new selection',
          'offset',before['x'],'intermediate frames',len(middle),flush=True)
def guard_check(page):
    arrow(page,1).click();settle(page)
    g=geom(page)
    assert g['x']>2 and g['left'] and g['snap'] in ('x','x proximity'),g
    assert rail(page).evaluate("e=>e.style.scrollSnapType")==''
    arrow(page,-1).click();settle(page)
    g=geom(page)
    assert g['x']<=0.5 and g['guardL'] and not g['left'],g
    a=arrow(page,-1)
    assert a.evaluate("e=>{const r=e.getBoundingClientRect();return document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)===e&&!e.disabled&&getComputedStyle(e.parentElement).opacity==='0'}"),g
    a.click();settle(page)
    assert geom(page)==g,('Guard changed release',g,geom(page))
    page.mouse.move(0,0);settle(page,320)
    assert arrow(page,-1).is_disabled()
def main():
    checks=0
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,executable_path=os.environ.get('GALLERY_TEST_CHROMIUM') or None,args=['--no-sandbox','--disable-dev-shm-usage'])
        for motion in ('no-preference','reduce'):
            for width in (1440,370):
                page=browser.new_page(viewport={'width':width,'height':1100},reduced_motion=motion)
                errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                page.set_content(HTML,wait_until='load')
                page.locator('[data-detail="demo:aot"]').first.click()
                page.wait_for_function("()=>state.detailId==='demo:aot'")
                rail(page).wait_for()
                rail(page).scroll_into_view_if_needed();settle(page)
                assert geom(page)['cards'][0]['id']==FIRST
                for theme in THEMES:
                    page.evaluate("(t)=>{state.theme=t;document.body.dataset.theme=t;}",theme)
                    settle(page,320)
                    first_case(page,motion,True);checks+=1
                    choose_second(page)
                    first_case(page,motion,False);checks+=1
                    guard_check(page)
                    print('PASS first release boundary guard',width,theme,motion,flush=True)
                assert not errors,errors
                page.close()
        browser.close()
    assert checks==48,checks
    print('PASS first-season animation regression',sys.argv[1],checks,'cases',flush=True)
if __name__=='__main__':main()
