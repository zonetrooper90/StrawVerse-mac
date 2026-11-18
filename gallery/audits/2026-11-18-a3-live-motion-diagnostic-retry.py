#!/usr/bin/env python3
"""A3.1 setup-corrected retry of the original diagnostic. Findings are not assertions of a fix."""
import hashlib,json,os,sys,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright

mode,policy,out=sys.argv[1:]
assert mode in ("full","lightweight") and policy in ("live","reduce","normal")
root=Path(__file__).resolve().parents[1]
path=root/("Gallery-current.html" if mode=="full" else "Gallery-development.html")
raw=path.read_bytes()
expected={"full":(6938816,"e7ebd13cb49423448f3878e5f163d74840a7c5691f65708d036028cb8dd7650d"),"lightweight":(623126,"088a6d31cee139e9e7f7fad5f00cd54692a0192ac2d9616c83f3c313375d55e4")}[mode]
assert (len(raw),hashlib.sha256(raw).hexdigest())==expected
source=raw.decode("utf-8")
origin="http://127.0.0.1:8765/gallery.html"
kinds=("tab","fade-out","fade-in","player-route","play","next","modal-scroll","settings-scroll","rail","search","history")
widths=(1440,620)
report={"mode":mode,"policy":policy,"sha256":expected[1],"cases":[]}
out=Path(out)

# Passive sampling of live application state; no monkeypatch to its clock, animation,
# event listeners or cancellation functions. Diagnostic RAF stops after each case.
TRACE=r"""kind=>{
 const q=s=>document.querySelector(s), num=v=>Number.isFinite(v)?v:null;
 const opacity=e=>e?Number(getComputedStyle(e).opacity):null;
 const m=matchMedia('(prefers-reduced-motion: reduce)');
 const t={frames:[],events:[],stop:false,kind,seq:0};
 const anim=a=>({name:a.animationName||a.transitionProperty||'WAAPI',state:a.playState,
   time:num(a.currentTime),progress:num(a.effect?.getComputedTiming().progress),
   target:a.effect?.target?.id||a.effect?.target?.className?.baseVal||'',pseudo:a.effect?.pseudoElement||''});
 const snapshot=()=>{
  const a=q('.app'),rail=q('#inline-installment-rail'),dialog=q('.dialog-scroll'),shell=tabPages.discover.querySelector('.continue-shell'),
   history=q('[data-wh-row="a31-motion"] .wh-progress'),entry=history&&whProgressEntries.get(history);
  const track=measuredTrackX()/Math.max(1,tabPagesViewport.clientWidth);
  const all=document.getAnimations().map(anim);
  return {seq:++t.seq,ms:performance.now(),reduce:m.matches,kind,view:state.view,detail:state.detailId,
   playback:!!state.playback,settings:document.body.classList.contains('settings-view'),history:whOpen,
   route:screen.dataset.surfaceKey,busy:a.getAttribute('aria-busy'),stage:galleryStageFadeInProgress,
   pending:!!galleryStagePending,snapshot:!!galleryStageTransition,stageName:workspace.style.viewTransitionName,
   opening:gallerySettingsOpening,closing:settingsClosing,opacity:opacity(workspace),tabsOpacity:opacity(q('.top .tabs')),
   track,trackActive:!!tabTrackAnimation,trackTarget:tabTrackTarget,
   play:sfPlayMorph.amount,playFrame:!!sfPlayMorph.frame,playTarget:sfPlayMorph.target,
   playPath:q('#player-play-morph-first')?.getAttribute('d'),playOffset:q('#player-play-morph-group')?.getAttribute('transform'),
   next:playNextMorph.amount,nextFrame:!!playNextMorph.frame,nextTarget:playNextShown,
   nextPath:q('#player-morph-first')?.getAttribute('points'),playLabel:q('#pause-play')?.getAttribute('aria-label'),
   nextLabel:q('#forward10')?.getAttribute('aria-label'),modalFrame:modalScrollFrame!==null,
   modalY:dialog?.scrollTop??null,modalGoal:modalScrollGoal,modalMax:dialog?dialog.scrollHeight-dialog.clientHeight:null,
   settingsFrame:settingsScrollFrame!==null,settingsY:workspace.scrollTop,settingsMax:workspace.scrollHeight-workspace.clientHeight,
   focus:document.activeElement?.id||'',focusVisible:(()=>{const e=document.activeElement;if(!e)return false;const r=e.getBoundingClientRect(),v=(dialog||workspace).getBoundingClientRect();return r.top>=v.top-1&&r.bottom<=v.bottom+1;})(),
   inert:a.inert,railX:rail?.scrollLeft??null,railMax:rail?rail.scrollWidth-rail.clientWidth:null,
   search:searchOpen,searchActive:!!discoverSearchRestore,searchY:tabPages.discover.scrollTop,
   shellHeight:shell?.getBoundingClientRect().height??null,guard:tabPages.discover.classList.contains('search-scroll-restoring'),
   whMotion:!!entry?.motion,whDone:entry?.done??null,whStarted:entry?.started??null,
   whPath:history?.querySelector('.wh-progress-capsules')?.getAttribute('d')??null,whFrame:!!whProgressFrame,
   animations:all};
 };
 t.snap=snapshot;t.frames.push(snapshot());
 const tick=()=>{if(t.stop)return;t.frames.push(snapshot());if(t.frames.length<500)t.raf=requestAnimationFrame(tick);};
 t.raf=requestAnimationFrame(tick);
 t.listener=e=>t.events.push({type:'preference',matches:e.matches,ms:performance.now(),frame:snapshot()});
 m.addEventListener('change',t.listener);
 const input=e=>t.events.push({type:e.type,trusted:e.isTrusted,key:e.key||'',id:e.target?.id||'',ms:performance.now()});
 document.addEventListener('click',input,true);document.addEventListener('keydown',input,true);
 t.finish=()=>{t.stop=true;cancelAnimationFrame(t.raf);m.removeEventListener('change',t.listener);document.removeEventListener('click',input,true);document.removeEventListener('keydown',input,true);return {frames:t.frames,events:t.events};};
 window.__a31=t;
}"""
SETTLED="()=>!galleryStageTransition&&!galleryStageFadeInProgress&&!galleryStagePending&&!gallerySettingsOpening&&!settingsClosing"
# Conditions require actual intermediate geometry/amount, not only a scheduled handle.
MID={
 "tab":"s.trackActive&&s.track<-.035&&s.track>-.92",
 "fade-out":"s.stage&&!s.settings&&s.opacity<.94&&s.opacity>.12",
 "fade-in":"s.stage&&s.settings&&s.opacity>.06&&s.opacity<.90",
 "player-route":"s.snapshot&&s.animations.some(a=>a.name.startsWith('gallery-stage-fade')&&a.progress!==null&&a.progress>.04&&a.progress<.85)",
 "play":"s.playFrame&&s.play>.025&&s.play<.94",
 "next":"s.nextFrame&&s.next>.025&&s.next<.94",
 "modal-scroll":"s.modalFrame&&s.modalY>3&&s.modalY<s.modalMax-3",
 "settings-scroll":"s.settingsFrame&&s.settingsY>3&&s.settingsY<s.settingsMax-3",
 "rail":"s.railX>2&&s.railX<s.railMax-2",
 "search":"s.searchActive&&s.searchY>2&&s.searchY<window.__a31Base.searchY-2",
 "history":"s.whMotion&&s.whStarted>8/12+.002&&s.whStarted<9/12-.002",
}
def settle(page):
    page.wait_for_function(SETTLED,timeout=8000)
    page.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
def click(page,sel):
    el=page.locator(sel).first
    el.wait_for(state="visible")
    el.scroll_into_view_if_needed()
    assert el.is_enabled(),sel
    b=el.bounding_box();assert b and b["width"]>0 and b["height"]>0,sel
    x,y=b["x"]+b["width"]/2,b["y"]+b["height"]/2
    assert el.evaluate("(e,p)=>e.contains(document.elementFromPoint(...p))",[x,y]),("occluded",sel,x,y)
    page.mouse.click(x,y)
def detail(page):
    click(page,'[data-detail="demo:aot"]');settle(page)
    assert page.evaluate("state.detailId==='demo:aot'")
def player(page):
    detail(page);click(page,'.detail-actions [data-episode-action="watch"]');settle(page)
    assert page.evaluate("!!state.playback&&!!sfPlayerSession")
def setup(page,kind):
    if kind=="tab":return lambda:click(page,'.tab[data-view="library"]')
    if kind.startswith("fade"):return lambda:click(page,'#settings')
    if kind=="player-route":
        detail(page);return lambda:click(page,'.detail-actions [data-episode-action="watch"]')
    if kind in ("play","next"):
        player(page)
        if kind=="play":
            click(page,'#sf-player-demo-start')
            assert page.evaluate("sfPlayerDemo.active&&!sfPlayerDemo.playing")
            return lambda:click(page,'#pause-play')
        # The dev-only preview button is hidden in the current UI. Exercise the
        # real visible range input and actual demo autoplay threshold instead.
        click(page,'#sf-player-demo-start')
        assert page.evaluate("sfPlayerDemo.active&&!sfPlayerDemo.playing&&sfPlayerDemo.autoplay&&playerCanAdvance()&&!playNextShown")
        seek=page.locator('#seek')
        assert seek.is_visible() and seek.is_enabled()
        seek.focus()
        page.keyboard.press("End")
        assert page.evaluate("sfPlayerDemo.time===SF_PLAYER_DEMO_DURATION&&!playNextShown&&!playNextMorph.frame")
        assert page.evaluate("document.activeElement.id==='seek'")
        # One native range step before the end is inside the final 20 seconds.
        return lambda:page.keyboard.press("ArrowLeft")
    if kind=="modal-scroll":
        # Controlled disposable overflow fixture using existing modal API, then trusted keyboard wrap.
        page.evaluate("""()=>{document.getElementById('settings').focus();modal('A3.1 scroll fixture',
        '<div style="min-height:1600px"><button id="a31-first">First</button></div>',
        '<button id="a31-last">Last</button>');document.getElementById('close-dialog').focus({preventScroll:true})}""")
        page.wait_for_function("()=>!document.getAnimations().some(a=>a.playState==='running'&&a.animationName?.startsWith('gallery-dialog'))")
        assert page.evaluate("()=>modalHost.querySelector('.dialog-scroll').scrollHeight-modalHost.querySelector('.dialog-scroll').clientHeight>300")
        return lambda:page.keyboard.press("Shift+Tab")
    if kind=="settings-scroll":
        click(page,'#settings');settle(page)
        click(page,'[data-settings-section="playback"]')
        click(page,'[data-playback-tab="subtitles"]')
        page.wait_for_function("()=>!document.getAnimations().some(a=>a.playState==='running'&&a.animationName==='settings-panel-enter')")
        # Keep the original subtitle case wherever it has enough real overflow.
        # At desktop the compact subtitle panel fits; use the actual General
        # or Sources controls instead of artificially resizing production DOM.
        choose="""()=>{
          workspace.scrollTop=0;
          const controls=[searchToggle,searchInput,searchClear,searchClose,document.getElementById('settings'),...settingsPage.querySelectorAll('button:not([disabled]),input:not([disabled]),select:not([disabled]),a[href]')].filter(el=>el.getClientRects().length&&!el.closest('[hidden]')&&!el.hidden&&!el.closest('[inert]'));
          const v=workspace.getBoundingClientRect(),max=workspace.scrollHeight-workspace.clientHeight;let best=null;
          for(let j=1;j<controls.length;j++){
            const el=controls[j],r=el.getBoundingClientRect();
            if(!settingsPage.contains(el)||r.height>v.height-40||r.bottom<=v.bottom+140)continue;
            const goal=Math.max(0,Math.min(max,r.bottom-v.bottom+20));
            if(goal>=140&&r.top-goal>=v.top-1&&r.bottom-goal<=v.bottom+1&&(!best||goal>best.goal))best={j,goal,r};
          }
          if(!best)return null;
          const el=controls[best.j],prev=controls[best.j-1];prev.focus({preventScroll:true});
          window.__a31FocusTarget=el;window.__a31SettingsGoal=best.goal;
          return {panel:settingsLastSection,tab:playbackTab,sourceTab:sourcesTab,goal:best.goal,max,
            target:el.id||el.getAttribute('aria-label')||el.textContent.trim().slice(0,100),
            bottom:best.r.bottom,view:v.bottom,focused:document.activeElement===prev,top:workspace.scrollTop};
        }"""
        def pick():
            page.wait_for_function("()=>!settingsScrollFrame&&!document.getAnimations().some(a=>a.playState==='running'&&a.animationName==='settings-panel-enter')")
            page.evaluate("()=>{workspace.scrollTo({top:0,behavior:'instant'})}")
            return page.evaluate(choose)
        target=pick()
        if not target:
            click(page,'[data-playback-tab="general"]')
            target=pick()
        if not target:
            click(page,'[data-settings-section="sources"]')
            click(page,'[data-source-tab="marketplace"]')
            target=pick()
        assert target and target["focused"] and abs(target["top"])<1,target
        page.evaluate("s=>window.__a31SettingsSetup=s",target)
        return lambda:page.keyboard.press("Tab")
    if kind=="rail":
        detail(page)
        page.locator('#inline-installment-rail').scroll_into_view_if_needed()
        page.wait_for_function("()=>!document.querySelector('[data-inline-scroll=\"1\"]').disabled")
        assert page.evaluate("()=>{const r=document.getElementById('inline-installment-rail');return r.scrollLeft<2&&r.scrollWidth-r.clientWidth>30}")
        return lambda:click(page,'[data-inline-scroll="1"]')
    if kind=="search":
        page.evaluate("()=>{tabPages.discover.scrollTop=100}")
        assert page.evaluate("()=>tabPages.discover.scrollTop>50&&tabPages.discover.querySelector('.continue-shell').getBoundingClientRect().height>10")
        return lambda:click(page,'#search')
    if kind=="history":
        click(page,'#wh-view-history');settle(page)
        page.evaluate("""()=>{const r={...whSeedRecords()[0],id:'a31-motion',episodes:Array.from({length:12},(_,i)=>({n:i+1,started:i<8,watched:i<5,progressSeconds:i<8?42:0,duration:1440,manualStatus:i<5?'watched':i<8?'partial':'never'})),latestEpisode:1};whRecords=[r];whExpanded=new Set([r.id]);whRender();}""")
        page.locator('[data-wh-episode="a31-motion:9"]').scroll_into_view_if_needed()
        return lambda:click(page,'[data-wh-episode="a31-motion:9"]')
    raise AssertionError(kind)
def snap(page):return page.evaluate("window.__a31.snap()")
def intermediate(page,kind):
    page.wait_for_function("()=>{const s=window.__a31.snap();return "+MID[kind]+"}",timeout=3000,polling="raf")
    s=snap(page)
    # A short native animation may finish between protocol calls. Require evidence
    # in the trace and mark the actual trigger-time phase independently.
    return s
def settled_target(page,kind,reverse=False):
    expressions={
        "tab": "(!tabTrackAnimation&&state.view==='discover'&&Math.abs(measuredTrackX())<1)" if reverse else "(!tabTrackAnimation&&state.view==='library'&&Math.abs(measuredTrackX()+tabPagesViewport.clientWidth)<1)",
        "fade-out":"document.body.classList.contains('settings-view')&&!galleryStageFadeInProgress&&!gallerySettingsOpening",
        "fade-in":"document.body.classList.contains('settings-view')&&!galleryStageFadeInProgress&&!gallerySettingsOpening",
        "player-route":"!!state.playback&&!galleryStageTransition&&!galleryStageFadeInProgress",
        "play":"!sfPlayMorph.frame&&sfPlayMorph.amount==="+("0&&!sfPlayerDemo.playing" if reverse else "1&&sfPlayerDemo.playing"),
        "next":"!playNextMorph.frame&&playNextMorph.amount==="+("0&&!playNextShown" if reverse else "1&&playNextShown"),
        "modal-scroll":"modalScrollFrame===null&&document.activeElement.id==='a31-last'&&Math.abs(modalHost.querySelector('.dialog-scroll').scrollTop-(modalHost.querySelector('.dialog-scroll').scrollHeight-modalHost.querySelector('.dialog-scroll').clientHeight))<2",
        "settings-scroll":"settingsScrollFrame===null&&document.activeElement===window.__a31FocusTarget&&window.__a31.snap().focusVisible&&Math.abs(workspace.scrollTop-window.__a31SettingsGoal)<2",
        "rail":"document.getElementById('inline-installment-rail').scrollLeft>2",
        "search":"searchOpen&&!discoverSearchRestore&&!tabPages.discover.classList.contains('search-scroll-restoring')&&tabPages.discover.scrollTop<2&&document.activeElement===searchInput",
        "history":"(()=>{const e=whProgressEntries.get(document.querySelector('[data-wh-row=\"a31-motion\"] .wh-progress'));return !!e&&!e.motion&&Math.abs(e.started-9/12)<.0001})()",
    }
    page.wait_for_function("()=>"+expressions[kind],timeout=8000)
def active(s,kind):
    return {"tab":s["trackActive"],"fade-out":s["stage"],"fade-in":s["stage"],"player-route":s["snapshot"],
        "play":s["playFrame"],"next":s["nextFrame"],"modal-scroll":s["modalFrame"],"settings-scroll":s["settingsFrame"],
        "rail":False,"search":s["searchActive"],"history":s["whMotion"]}[kind]
def value(s,kind):
    return {"tab":s["track"],"fade-out":s["opacity"],"fade-in":s["opacity"],
      "player-route":tuple((a["name"],a["progress"]) for a in s["animations"] if a["name"].startswith("gallery-stage-fade")),
      "play":s["play"],"next":s["next"],"modal-scroll":s["modalY"],"settings-scroll":s["settingsY"],
      "rail":s["railX"],"search":s["searchY"],"history":s["whStarted"]}[kind]
def run(browser,width,kind,reverse=False):
    row={"width":width,"kind":kind,"reverse":reverse,"status":"pending","errors":[]}
    report["cases"].append(row)
    c=browser.new_context(viewport={"width":width,"height":700},reduced_motion="reduce" if policy=="reduce" else "no-preference")
    p=c.new_page();p.on("pageerror",lambda e:row["errors"].append(str(e)))
    try:
        # Real localhost document origin, no network, exact unmodified HTML.
        url=origin+("#recently-watched-legacy" if kind in ("search","history") else "")
        p.route("**/*",lambda r:r.fulfill(status=200,content_type="text/html; charset=utf-8",body=source) if r.request.url.split("#")[0]==origin else r.abort())
        p.goto(url,wait_until="domcontentloaded");settle(p)
        action=setup(p,kind)
        if kind=="settings-scroll":row["settingsSetup"]=p.evaluate("window.__a31SettingsSetup")
        p.evaluate(TRACE,kind)
        base=snap(p);row["base"]=base;p.evaluate("s=>window.__a31Base=s",base)
        action()
        if policy!="reduce":
            row["mid"]=intermediate(p,kind)
            if policy=="live":
                row["beforeSwitch"]=snap(p)
                # Fail before issuing the preference change if the actual
                # painted state has already left the required intermediate phase.
                assert p.evaluate("(s)=>"+MID[kind],row["beforeSwitch"]),"Missed intermediate phase before switch"
                p.emulate_media(reduced_motion="reduce")
                p.wait_for_function("()=>window.__a31.events.some(e=>e.type==='preference'&&e.matches)",timeout=3000)
            elif reverse:
                if kind=="next":
                    assert p.evaluate("document.activeElement.id==='seek'&&playNextShown")
                    p.keyboard.press("Home")
                else:
                    sel={"tab":'.tab[data-view="discover"]',"play":"#pause-play"}[kind]
                    click(p,sel)
        settled_target(p,kind,reverse)
        # Native smooth scroll has no app-owned RAF; observe actual position after settling.
        p.wait_for_timeout(650 if kind=="rail" else 100)
        row["final"]=snap(p)
        if kind=="rail":
            row["railSettled"]=p.evaluate("()=>new Promise(r=>{const a=document.getElementById('inline-installment-rail');const x=a.scrollLeft;requestAnimationFrame(()=>requestAnimationFrame(()=>r(Math.abs(x-a.scrollLeft)<.5)))})")
            assert row["railSettled"]
        if policy in ("live","reduce"):
            p.emulate_media(reduced_motion="no-preference")
            p.wait_for_function("()=>window.__a31.events.some(e=>e.type==='preference'&&!e.matches)",timeout=3000)
            p.wait_for_timeout(350);row["reenabled"]=snap(p)
        row["trace"]=p.evaluate("window.__a31.finish()")
        f=row["final"]
        if kind=="next":
            assert f["nextLabel"]==("Forward 10 seconds" if reverse else "Next episode"),f
            assert p.evaluate("sfPlayerDemo.time===0") if reverse else p.evaluate("sfPlayerDemo.time>SF_PLAYER_DEMO_DURATION-20&&sfPlayerDemo.time<SF_PLAYER_DEMO_DURATION")
            assert any(e.get("trusted") and e.get("id")=="seek" and e.get("key")=="ArrowLeft" for e in row["trace"]["events"]),"Missing trusted threshold crossing"
            if reverse:assert any(e.get("trusted") and e.get("id")=="seek" and e.get("key")=="Home" for e in row["trace"]["events"]),"Missing trusted reversal"
        assert not f["stage"] and not f["snapshot"] and not f["busy"] and not f["pending"],f
        assert not row["errors"],row["errors"]
        assert any(e.get("trusted") for e in row["trace"]["events"] if e["type"] in ("click","keydown")),"No trusted action"
        if policy=="live":
            event=next(e for e in row["trace"]["events"] if e["type"]=="preference" and e["matches"])
            ev=event["frame"]
            post=[s for s in row["trace"]["frames"] if s["ms"]>event["ms"] and s["reduce"]]
            assert post,"No reduced-motion frames"
            # Confirm genuine in-flight preference delivery separately from any outcome.
            # Native CSS can settle synchronously before the event; compare before-switch
            # and trace in addition to the event snapshot. A missed active window is not a pass.
            before=row["beforeSwitch"]
            # The condition was sampled on a real frame; recheck the phase immediately
            # before the protocol request, with no reliance on a stale handle.
            timely=p.evaluate("(s)=>"+MID[kind],before)
            row["timelyTrigger"]=bool(timely)
            if not timely:raise AssertionError("Missed intermediate phase before preference switch")
            # Preserve the measured pre-switch frame and the last sampled
            # normal frame. If a subsequent normal frame already settled the
            # action, do not misattribute its ordinary completion to reduction.
            normal=[s for s in row["trace"]["frames"] if not s["reduce"] and before["ms"]<=s["ms"]<event["ms"]]
            row["lastNormalBeforeChange"]=normal[-1] if normal else before
            if normal:
                last=normal[-1]
                assert p.evaluate("(s)=>"+MID[kind],last),"Animation left the intermediate phase before preference delivery"
            row["switchDeliveryMs"]=event["ms"]-before["ms"]
            later=post[2:] # allow event/render delivery for two frames
            vals=[value(s,kind) for s in later]
            row["findings"]={"event":ev,"postFrames":len(post),"activeAfterTwoFrames":sum(active(s,kind) for s in later),
                "distinctValuesAfterTwoFrames":len(set(vals)),
                "firstTwo":post[:2],"valueAtEvent":value(ev,kind),"valueFinal":value(f,kind),
                "replayActive":active(row["reenabled"],kind),"replayValue":value(row["reenabled"],kind)}
        elif policy=="reduce":
            row["findings"]={"activeReducedFrames":sum(active(s,kind) for s in row["trace"]["frames"] if s["reduce"]),
                             "replayActive":active(row["reenabled"],kind)}
        else:
            row["findings"]={"normalControl":True,"reverse":reverse}
        row["status"]="collected"
        print("COLLECTED",mode,policy,width,kind,"reverse",reverse,json.dumps({k:v for k,v in row["findings"].items() if k not in ("event","firstTwo")}),flush=True)
    except Exception as e:
        row["status"]="harness-error";row["exception"]=str(e);row["stack"]=traceback.format_exc()
        try:row["trace"]=p.evaluate("window.__a31?.finish()")
        except Exception:pass
        print("HARNESS ERROR",mode,policy,width,kind,str(e),flush=True)
    finally:
        c.close();out.write_text(json.dumps(report,indent=2),encoding="utf-8")
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path=os.environ.get("GALLERY_TEST_CHROMIUM") or None,args=["--no-sandbox","--disable-dev-shm-usage"])
    for width in widths:
        for kind in kinds:run(browser,width,kind)
        if policy=="normal":
            for kind in ("tab","play","next"):run(browser,width,kind,True)
    browser.close()
expected_cases=28 if policy=="normal" else 22
report["summary"]={"expected":expected_cases,"collected":sum(r["status"]=="collected" for r in report["cases"]),"harnessErrors":sum(r["status"]!="collected" for r in report["cases"]),"pageErrors":sum(len(r["errors"]) for r in report["cases"])}
out.write_text(json.dumps(report,indent=2),encoding="utf-8")
print("A3.1 SUMMARY",json.dumps(report["summary"]),flush=True)
assert len(report["cases"])==expected_cases and report["summary"]["collected"]==expected_cases and not report["summary"]["pageErrors"],report["summary"]
