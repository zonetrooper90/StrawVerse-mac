#!/usr/bin/env python3
"""Q2-B6: release rail actual DOM equivalence, interactions and boundary guards."""
import hashlib,re,runpy,subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright
S=runpy.run_path("gallery/changes/pending/2026-11-14-q2b6-release-arrow.py")
HELPER=Path("gallery/audits/2026-11-14-q2b3-anime-details-comparison.py")
raw=HELPER.read_bytes()
assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()=="4fbe8a79313712c81d04c04523276064341ee390"
H=runpy.run_path(str(HELPER))
THEMES=H["THEMES"]
WIDTHS=(1440,561,560,461,460,370)
INTERACTION_WIDTHS=(1440,560,370)
TARGETS=['.inline-installments']
EXPECTED=6*(len(WIDTHS)*3+len(INTERACTION_WIDTHS)*12+5)
STYLE=re.compile(br'<style>(.*?)</style>',re.S)

def exact_pair(mode):
    path,digest=S["FILES"][mode]
    before=subprocess.check_output(["git","show",S["BASE"]+":"+path])
    assert hashlib.sha256(before).hexdigest()==digest
    after=Path(path).read_bytes()
    pre,base,post=H["unpack"](before)
    cp,css,ct=H["unpack"](after)
    assert (pre,post)==(cp,ct)
    assert S["transform"](base)==css and len(before)-len(after)==20
    print("PASS: exact one-declaration, 20-byte CSS-only deletion",path,flush=True)
    return after.decode(),base.decode(),css.decode()

def settle(page):
    H["settle"](page,600)
def rest(page):
    page.mouse.move(0,0)
    page.evaluate("()=>document.activeElement?.blur()")
    settle(page)
def rail(page):
    return page.locator('#inline-installment-rail')
def arrow(page,side):
    return page.locator('[data-inline-scroll="'+str(side)+'"]')
def fade(page,side):
    return page.locator('.inline-release-fade-'+('right' if side==1 else 'left'))
def geometry(page):
    return rail(page).evaluate("""e=>{
      const r=e.getBoundingClientRect(),v=e.closest('.inline-release-viewport');
      return {x:e.scrollLeft,max:e.scrollWidth-e.clientWidth,width:e.clientWidth,
        offsets:[...e.children].map(c=>c.getBoundingClientRect().left-r.left+e.scrollLeft),
        left:v.classList.contains('can-left'),right:v.classList.contains('can-right'),
        guardL:v.classList.contains('guard-left'),guardR:v.classList.contains('guard-right'),
        selection:[...e.children].filter(c=>c.getAttribute('aria-current')==='true').map(c=>c.dataset.inlineInstallment)};
    }""")
def to_edge(page,side):
    rest(page)
    rail(page).evaluate("(e,side)=>e.scrollTo({left:side>0?e.scrollWidth:0,behavior:'instant'})",side)
    settle(page)
    g=geometry(page)
    assert abs(g['x']-(g['max'] if side==1 else 0))<=2,g
    assert not g['guardL'] and not g['guardR'],g
    return g

def arrow_state(page,side,visible,guard=False):
    a=arrow(page,side)
    data=fade(page,side).evaluate("""e=>{
      const s=getComputedStyle(e),b=e.querySelector('button'),bs=getComputedStyle(b),
        r=e.getBoundingClientRect(),br=b.getBoundingClientRect();
      return {opacity:s.opacity,visibility:s.visibility,gradient:getComputedStyle(e,'::before').backgroundImage,
        w:r.width,h:r.height,bw:br.width,bh:br.height,disabled:b.disabled,pointer:bs.pointerEvents,
        transition:s.transitionDuration,bg:bs.backgroundColor,shadow:bs.boxShadow};
    }""")
    assert data['gradient'].startswith('linear-gradient('),data
    assert data['opacity']==('1' if visible else '0'),data
    assert data['visibility']==('visible' if visible or guard else 'hidden'),data
    assert data['disabled']==(not (visible or guard)),data
    assert abs(data['w']-data['bw'])<0.1 and abs(data['h']-data['bh'])<0.1,data
    assert data['w']==(54 if page.viewport_size['width']<=560 else 70),data
    assert data['bg']=='rgba(0, 0, 0, 0)' and data['shadow']=='none',data
    return data

def hover(page,side):
    a=arrow(page,side)
    a.hover()
    settle(page)
    assert a.evaluate("e=>e.matches(':hover')")
    assert a.evaluate("""e=>{
      const t=document.createElement('span');t.style.color='var(--accent)';e.append(t);
      const same=getComputedStyle(t).color===getComputedStyle(e).color;t.remove();return same;
    }"""),'arrow hover color'
def focus(page,side):
    a=arrow(page,side)
    page.mouse.move(0,0)
    page.keyboard.press('Tab')
    a.evaluate("e=>e.focus({preventScroll:true})")
    settle(page)
    assert a.evaluate("e=>e.matches(':focus-visible')")
    assert a.evaluate("e=>getComputedStyle(e).outlineStyle==='solid'&&getComputedStyle(e).outlineWidth==='2px'")

def click_arrow(page,side):
    a=arrow(page,side)
    old=geometry(page)
    choices=[x for x in old['offsets'] if x>old['x']+4] if side==1 else [x for x in reversed(old['offsets']) if x<old['x']-4]
    assert choices,old
    target=max(0,min(choices[0],old['max']))
    # Real pointer click, left stationary to exercise the edge guard.
    a.click()
    settle(page)
    new=geometry(page)
    assert abs(new['x']-target)<=2.5,(side,old,target,new)
    assert new['selection']==old['selection'],(old,new)
    return new

def go_boundary(page,side):
    g=geometry(page)
    for _ in range(12):
        if not g['right' if side==1 else 'left']:break
        g=click_arrow(page,side)
    assert not g['right' if side==1 else 'left'],g
    assert g['guardR' if side==1 else 'guardL'],g
    arrow_state(page,side,False,True)
    a=arrow(page,side)
    assert a.evaluate("""e=>{
      const r=e.getBoundingClientRect();return document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)===e;
    }"""),'guard does not own its full edge hit target'
    return g

def choose(page,id):
    a=page.locator('[data-inline-installment="'+id+'"]')
    # Scroll the rail to the appropriate boundary before selecting the card;
    # this is the existing UI, not the planned selected-card auto-reveal.
    a.click()
    page.wait_for_function("id=>document.querySelector('[data-inline-installment=\"'+id+'\"]')?.getAttribute('aria-current')==='true'",arg=id)
    rest(page)
    assert geometry(page)['selection']==[id]
    assert page.evaluate("window.__rail===document.querySelector('#inline-installment-rail')")
    assert page.evaluate("state.detailEpisode")==1

def run(mode,motion):
    html,baseline,candidate=exact_pair(mode)
    checks=0
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
        page=browser.new_page(viewport={'width':1440,'height':950},reduced_motion=motion)
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.set_content(html,wait_until='domcontentloaded')
        page.wait_for_selector('[data-detail="demo:solo"]')
        page.evaluate("""({baseline,candidate})=>{
          window.__q2baseline=baseline;window.__q2candidate=candidate;
          if(document.querySelector('style').textContent!==candidate)throw Error('Wrong stylesheet');
        }""",{'baseline':baseline,'candidate':candidate})
        def compare(theme,label,targets=TARGETS):
            nonlocal checks
            result=page.evaluate(H["COMPARE"],{'targets':targets,'scope':'.anime-detail'})
            assert 'property' not in result,(mode,motion,theme,label,result)
            assert result['nodes']>0 and all(result['counts'][t]>0 for t in targets),result
            checks+=1
        def size(w):
            page.set_viewport_size({'width':w,'height':950})
            rail(page).scroll_into_view_if_needed()
            settle(page)
        for theme in THEMES:
            page.set_viewport_size({'width':1440,'height':950})
            H["open_anime"](page,'demo:aot')
            page.evaluate("(t)=>{state.theme=t;document.body.dataset.theme=t;}",theme)
            rest(page)
            assert rail(page).locator('.inline-installment-card').count()==8
            assert rail(page).locator('.inline-installment-card').evaluate_all("es=>es.map(e=>e.dataset.inlineInstallment)")==['aot-s1','aot-s2','aot-s3','aot-s4a','aot-s4b','aot-finalchapters','aot-lastattack','aot-oad']
            for w in WIDTHS:
                size(w)
                g=to_edge(page,-1)
                assert g['max']>4 and g['right'] and not g['left'],g
                data=arrow_state(page,1,True)
                assert all(float(v.strip().rstrip('s'))==0 for v in data['transition'].split(',')) if motion=='reduce' else '0.23s' in data['transition'],data
                arrow_state(page,-1,False)
                compare(theme,('start',w))
                # Real middle offset, allowing the existing proximity snap.
                rail(page).evaluate("e=>e.scrollTo({left:(e.scrollWidth-e.clientWidth)/2,behavior:'instant'})")
                settle(page)
                g=geometry(page)
                assert g['left'] and g['right'],g
                arrow_state(page,1,True);arrow_state(page,-1,True)
                compare(theme,('middle',w))
                to_edge(page,1)
                arrow_state(page,1,False);arrow_state(page,-1,True)
                compare(theme,('end',w))
            for w in INTERACTION_WIDTHS:
                size(w)
                for side in (1,-1):
                    to_edge(page,-side)
                    hover(page,side);compare(theme,('hover',w,side))
                    focus(page,side);compare(theme,('focus',w,side))
                    hover(page,side)
                    assert arrow(page,side).evaluate("e=>e.matches(':focus-visible')")
                    compare(theme,('hover and focus',w,side))
                    # Real single-card advance (possibly the final step).
                    click_arrow(page,side)
                    compare(theme,('one card',w,side))
                    g=go_boundary(page,side)
                    compare(theme,('boundary guard',w,side))
                    arrow(page,side).click()
                    settle(page)
                    assert geometry(page)==g,('guard click changed rail or selection',g,geometry(page))
                    rest(page)
                    arrow_state(page,side,False)
                    compare(theme,('guard released',w,side))
            size(1440)
            to_edge(page,-1)
            page.evaluate("()=>window.__rail=document.querySelector('#inline-installment-rail')")
            choose(page,'aot-s2')
            assert page.evaluate("state.detailSeason")==1
            compare(theme,'season selection')
            to_edge(page,1)
            choose(page,'aot-oad')
            assert page.evaluate("state.detailRelated")=='aot-oad'
            compare(theme,'related selection')
            H["open_anime"](page,'demo:quints')
            size(1440);to_edge(page,1)
            page.evaluate("()=>window.__rail=document.querySelector('#inline-installment-rail')")
            choose(page,'quints-sp-2024')
            assert page.evaluate("state.detailRelated")=='quints-sp-2024'
            compare(theme,'special selection')
            H["open_anime"](page,'demo:solo')
            size(1440);g=to_edge(page,-1)
            assert g['max']<=3 and not g['left'] and not g['right'],g
            arrow_state(page,1,False);arrow_state(page,-1,False)
            compare(theme,'no overflow')
            H["open_anime"](page,'demo:04')
            assert rail(page).count()==0 and page.locator('.inline-release-fade').count()==0
            compare(theme,'single release',['.detail-hero'])
            assert not errors,(theme,errors)
            print('PASS: release arrows',mode,motion,theme,'59 comparisons',flush=True)
        page.close()
        browser.close()
    assert checks==EXPECTED==354,(checks,EXPECTED)
    print('PASS: Q2-B6 actual DOM equivalence',mode,motion,checks,'comparisons',flush=True)
