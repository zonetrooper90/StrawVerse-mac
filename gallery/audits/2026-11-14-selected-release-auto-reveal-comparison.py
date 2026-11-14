#!/usr/bin/env python3
"""Real release selection, minimum reveal, responsive clearance and manual navigation."""
import hashlib,math,runpy,subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright
S=runpy.run_path("gallery/changes/pending/2026-11-14-selected-release-auto-reveal.py")
helper=Path("gallery/audits/2026-11-14-q2b6-release-arrow-comparison.py")
raw=helper.read_bytes()
assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()=="accf105c7ccf768e71de9cf2a67e4216893eb4f7"
G=runpy.run_path(str(helper)); H=G["H"]
THEMES=G["THEMES"]
WIDTHS=(1440,561,560,461,460,370)
EXPECTED=6*(len(WIDTHS)*3+8)
GEOMETRY=r"""()=> {
 const e=document.querySelector('#inline-installment-rail'),r=e.getBoundingClientRect(),v=e.closest('.inline-release-viewport');
 const left=v.querySelector('.inline-release-fade-left'),right=v.querySelector('.inline-release-fade-right');
 return {x:e.scrollLeft,max:e.scrollWidth-e.clientWidth,w:e.clientWidth,l:left.getBoundingClientRect().width,
   r:right.getBoundingClientRect().width,origin:r.left,y:r.top+r.height/2,
   left:v.classList.contains('can-left'),right:v.classList.contains('can-right'),
   guardL:v.classList.contains('guard-left'),guardR:v.classList.contains('guard-right'),
   snap:getComputedStyle(e).scrollSnapType,vertical:workspace.scrollTop,
   verticalMax:Math.max(0,workspace.scrollHeight-workspace.clientHeight),
   pageY:window.scrollY,
   cards:[...e.children].map(c=>{const b=c.getBoundingClientRect();return {id:c.dataset.inlineInstallment,
     a:b.left-r.left+e.scrollLeft,b:b.right-r.left+e.scrollLeft,w:b.width,selected:c.getAttribute('aria-current')==='true'};})};
}"""
def exact_pair(mode):
    path,digest=S["FILES"][mode]
    base=subprocess.check_output(["git","show",S["BASE"]+":"+path])
    assert hashlib.sha256(base).hexdigest()==digest
    candidate=Path(path).read_bytes()
    assert S["expected_html"](base)==candidate
    print("PASS: exact approved auto-reveal HTML scope",path,flush=True)
    return base.decode(),candidate.decode()
def geom(page):return page.evaluate(GEOMETRY)
def card(g,id):return next(c for c in g["cards"] if c["id"]==id)
def bounds(g,x):
    return (x+(g["l"] if g["max"]>3 and x>2 else 0),
            x+g["w"]-(g["r"] if g["max"]>3 and x<g["max"]-2 else 0))
def visible(g,c,x,tol=0.6):
    a,b=bounds(g,x)
    return c["a"]>=a-tol and c["b"]<=b+tol
def nearest(g,c):
    if visible(g,c,g["x"],0.01):return g["x"]
    # Independent brute-force integer destination oracle, including both ends.
    options=[x for x in range(int(g["max"])+1) if visible(g,c,x,0.02)]
    assert options,("No full-card destination",g,c)
    return min(options,key=lambda x:abs(x-g["x"]))
def settle(page):G["settle"](page)
def rest(page):G["rest"](page)
def rail(page):return G["rail"](page)
def open_anime(page,id):
    page.set_viewport_size({'width':1440,'height':1100})
    H["open_anime"](page,id)
    if rail(page).count():
        rail(page).scroll_into_view_if_needed()
        settle(page)
def size(page,w):
    page.set_viewport_size({'width':w,'height':1100})
    rail(page).scroll_into_view_if_needed()
    settle(page)
def position(page,x):
    rest(page)
    # Establish an exact partial exposure independent of proximity snapping.
    # All selection and arrow actions below are real pointer/keyboard events.
    rail(page).evaluate("(e,x)=>{e.style.scrollSnapType='none';e.scrollTo({left:x,behavior:'instant'});}",x)
    settle(page)
    g=geom(page)
    assert abs(g["x"]-x)<=1.1,(x,g)
    return g
def setup_partial(page,side,exclude=()):
    g=geom(page)
    for c in g["cards"]:
        if c["selected"] or c["id"] in exclude:continue
        x=round(c["a"]-g["l"]/2 if side==-1 else c["b"]-g["w"]+g["r"]/2)
        if not 3<x<g["max"]-3:continue
        a,b=bounds(g,x)
        if side==-1 and not (c["a"]<a-5 and c["b"]<=b+0.5):continue
        if side==1 and not (c["b"]>b+5 and c["a"]>=a-0.5):continue
        g=position(page,x)
        c=card(g,c["id"])
        assert not visible(g,c,g["x"]),g
        assert abs(nearest(g,c)-g["x"])>4
        return c["id"]
    raise AssertionError(("Could not establish partial exposure",side,g))
def monitor(page):
    page.evaluate("""()=>{
      const e=document.querySelector('#inline-installment-rail');
      window.__revealRail=e;
      window.__calls=[];
      const original=e.scrollTo;
      e.scrollTo=function(...args){window.__calls.push(args[0]);return original.apply(this,args);};
    }""")
def hit(page,id):
    g=geom(page); c=card(g,id); a,b=bounds(g,g["x"])
    a=max(a,c["a"]);b=min(b,c["b"])
    assert b-a>4,("Not enough exposed card to click",id,g)
    x=g["origin"]+(a+b)/2-g["x"]; y=g["y"]
    page.mouse.move(x,y)
    assert page.evaluate("""({x,y,id})=>document.elementFromPoint(x,y)?.closest('[data-inline-installment]')?.dataset.inlineInstallment===id""",{"x":x,"y":y,"id":id}),("Click intercepted",id,g)
    before=geom(page)
    page.mouse.click(x,y)
    return before
def validate(page,id,before,motion,expect_move=None):
    c=card(before,id)
    expected=nearest(before,c)
    page.wait_for_function("id=>document.querySelector('[data-inline-installment=\"'+id+'\"]')?.getAttribute('aria-current')==='true'",arg=id)
    settle(page)
    after=geom(page); selected=card(after,id)
    assert visible(after,selected,after["x"]),("Selected card not fully visible",id,before,after)
    assert abs(after["x"]-expected)<=1.1,("Not minimum movement",id,expected,before,after)
    assert [c["id"] for c in after["cards"] if c["selected"]]==[id]
    assert page.evaluate("window.__revealRail===document.querySelector('#inline-installment-rail')"),"Rail replaced"
    assert abs(after["vertical"]-min(before["vertical"],after["verticalMax"]))<=1,("Vertical movement",before,after)
    assert before["pageY"]==after["pageY"]
    changed=abs(expected-before["x"])>1
    if expect_move is not None:assert changed==expect_move,(id,before,expected)
    calls=page.evaluate("window.__calls")
    if changed:
        assert calls and calls[-1]["behavior"]==("instant" if motion=="reduce" else "smooth"),calls
        assert abs(calls[-1]["left"]-expected)<=1.1,calls
        assert after["snap"]=="none",after
    return after
def click(page,id,motion,move=None):
    page.evaluate("window.__calls=[]")
    before=hit(page,id)
    after=validate(page,id,before,motion,move)
    return after
def edge(page,side):
    g=geom(page)
    return position(page,g["max"] if side==1 else 0)
def guard(page,side):
    rest(page)
    for _ in range(12):
        g=geom(page)
        if not g["right" if side==1 else "left"]:break
        G["click_arrow"](page,side)
    g=geom(page)
    assert not g["right" if side==1 else "left"] and g["guardR" if side==1 else "guardL"],g
    a=G["arrow"](page,side)
    assert a.evaluate("""e=>{const r=e.getBoundingClientRect();return document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)===e&&!e.disabled&&getComputedStyle(e.parentElement).opacity==='0'}"""),g
    a.click();settle(page)
    assert geom(page)==g,("Guard click changed state",g,geom(page))
    rest(page)
    assert G["arrow"](page,side).is_disabled()
def run(mode,motion):
    base,html=exact_pair(mode)
    checks=0
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
        def make(content):
            page=browser.new_page(viewport={'width':1440,'height':1100},reduced_motion=motion)
            page.set_content(content,wait_until='domcontentloaded')
            page.wait_for_selector('[data-detail="demo:solo"]')
            return page
        baseline=make(base);open_anime(baseline,'demo:aot')
        old={}
        for w in WIDTHS:
            size(baseline,w)
            old[w]=geom(baseline)
        assert any(c["w"]>old[370]["w"]-old[370]["l"]-old[370]["r"] for c in old[370]["cards"][1:-1]),("Baseline narrow blocker not reproduced",old[370])
        assert old[370]["l"]==old[370]["r"]==54
        baseline.close()
        page=make(html)
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        for theme in THEMES:
            open_anime(page,'demo:aot')
            page.evaluate("(t)=>{state.theme=t;document.body.dataset.theme=t;}",theme)
            rest(page);monitor(page)
            assert page.evaluate("document.querySelector('#inline-installment-rail').children.length")==8
            for w in WIDTHS:
                size(page,w);g=geom(page)
                assert abs(g["w"]-old[w]["w"])<=1
                assert all(abs(c["w"]-o["w"])<=0.1 for c,o in zip(g["cards"],old[w]["cards"])),("Card sizes changed",w,g,old[w])
                assert all(c["w"]<=g["w"]-g["l"]-g["r"]+0.1 for c in g["cards"]),("Insufficient unobstructed width",w,g)
                assert abs(g["l"]-g["r"])<=0.1
                assert abs(g["l"]-(min(54,0.115*g["w"]) if w<=460 else 54 if w<=560 else 70))<=0.8,(w,g)
                assert G["arrow"](page,1).locator('.icon').evaluate("e=>e.getBoundingClientRect().width")==21
                for side in (-1,1):
                    id=setup_partial(page,side)
                    before=geom(page)
                    after=click(page,id,motion,True)
                    assert (after['x']-before['x'])*side>1,(side,before,after)
                    checks+=1
                # Re-select the now fully visible card: no position change.
                click(page,id,motion,False);checks+=1
            size(page,1440)
            # First and last releases: the disappearing boundary arrow must
            # allow full visibility; position and selection remain independent.
            g=edge(page,-1); click(page,'aot-s1',motion,False);checks+=1
            # Natural arrow navigation from the start restores proximity snap.
            G["click_arrow"](page,1)
            assert geom(page)["snap"]=="x proximity"
            checks+=1
            # An actual right-arrow run to the boundary, then consume guard.
            guard(page,1);checks+=1
            click(page,'aot-oad',motion,False);checks+=1
            guard(page,-1);checks+=1
            # Real horizontal wheel restores normal snapping after a reveal.
            id=setup_partial(page,1);click(page,id,motion,True)
            g=geom(page)
            page.mouse.move(g["origin"]+g["w"]/2,g["y"])
            page.mouse.wheel(180,0);settle(page)
            assert geom(page)["snap"]=="x proximity",geom(page)
            checks+=1
            # Rapid consecutive user clicks: last selection wins and remains visible.
            id=setup_partial(page,1);page.evaluate("window.__calls=[]")
            hit(page,id)
            g=geom(page)
            alternatives=[c for c in g["cards"] if c["id"]!=id and visible(g,c,g["x"])]
            assert alternatives,g
            last=alternatives[0]["id"]
            before=hit(page,last)
            validate(page,last,before,motion)
            checks+=1
            # No overflow and a separate single-release route.
            open_anime(page,'demo:solo');monitor(page)
            g=geom(page);assert g["max"]<=3,g
            click(page,'solo-s2',motion,False)
            assert geom(page)["snap"]=="x proximity"
            open_anime(page,'demo:04');assert rail(page).count()==0
            checks+=1
            assert not errors,(theme,errors)
            print('PASS: selected release auto-reveal',mode,motion,theme,'26 cases',flush=True)
        browser.close()
    assert checks==EXPECTED==156,(checks,EXPECTED)
    print("PASS: selected-release auto-reveal",mode,motion,checks,"cases",flush=True)
