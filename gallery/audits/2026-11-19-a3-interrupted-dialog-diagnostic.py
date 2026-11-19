#!/usr/bin/env python3
"""A3.2 read-only rendered dialog interruption and lifecycle diagnostic."""
import hashlib,json,os,sys,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright

mode,motion,out=sys.argv[1:]
assert mode in ("full","lightweight") and motion in ("no-preference","reduce")
path=Path(__file__).resolve().parents[1]/("Gallery-current.html" if mode=="full" else "Gallery-development.html")
raw=path.read_bytes()
expected={"full":(6941329,"9ff90e5f458778b76be835afe178d6c4b9273229a2af9bb457bc4738f75071a1"),"lightweight":(625639,"214d322abab0dfb3a7f2d7d32a690fa1b7b3695fc17c4eba111a3736d2a02816")}[mode]
assert (len(raw),hashlib.sha256(raw).hexdigest())==expected
source=raw.decode("utf-8")
origin="http://127.0.0.1:8765/gallery.html"
report={"mode":mode,"motion":motion,"sha256":expected[1],"cases":[]}
out=Path(out)

# Native callbacks still run at the browser's own times. Observe only exit
# timer handles and expanded subtitle observer targets, with no clock changes.
INIT=r"""(()=>{
 const t=window.__a32={frames:[],events:[],timers:new Map(),registered:new Set(),ids:new WeakMap(),serial:0,record:false};
 const id=e=>{if(!e)return null;if(!t.ids.has(e))t.ids.set(e,++t.serial);return t.ids.get(e)};
 const log=(type,data={})=>{if(t.record)t.events.push({type,ms:performance.now(),...data})};
 const nativeSet=window.setTimeout.bind(window),nativeClear=window.clearTimeout.bind(window);
 window.setTimeout=function(cb,delay,...args){
  if(typeof cb!=='function'||!(new Error().stack||'').includes('closeModal'))return nativeSet(cb,delay,...args);
  let handle;handle=nativeSet(function(...a){
   const owner=t.timers.get(handle);t.timers.delete(handle);log('exit-deliver',{handle,owner,current:id(document.querySelector('#modal-host .overlay'))});return cb(...a);
  },delay,...args);
  const owner=id(document.querySelector('#modal-host .overlay'));t.timers.set(handle,owner);log('exit-schedule',{handle,owner,delay});return handle;
 };
 window.clearTimeout=function(handle){
  if(t.timers.has(handle)){log('exit-cancel',{handle,owner:t.timers.get(handle)});t.timers.delete(handle)}
  return nativeClear(handle);
 };
 const Native=window.ResizeObserver;
 window.ResizeObserver=class extends Native{
  constructor(cb){
   const owner=new Set();
   super((entries,observer)=>{
    for(const e of entries)if(e.target.id==='subtitle-expanded-stage')log('observer-deliver',{node:id(e.target),connected:e.target.isConnected,registered:owner.has(id(e.target)),closing:!!e.target.closest('.is-closing')});
    return cb(entries,observer);
   });
   this.a32owner=owner;
  }
  observe(target,...args){
   if(target.id==='subtitle-expanded-stage'){const node=id(target);this.a32owner.add(node);t.registered.add(node);log('observe',{node});}
   return super.observe(target,...args);
  }
  unobserve(target){
   const node=id(target);if(this.a32owner.delete(node)){t.registered.delete(node);log('unobserve',{node});}
   return super.unobserve(target);
  }
  disconnect(){
   for(const node of this.a32owner){t.registered.delete(node);log('unobserve',{node,disconnect:true});}
   this.a32owner.clear();return super.disconnect();
  }
 };
 const geometry=e=>{
  if(!e)return null;
  const c=getComputedStyle(e),m=c.transform==='none'?new DOMMatrixReadOnly():new DOMMatrixReadOnly(c.transform),r=e.getBoundingClientRect();
  return {opacity:Number(c.opacity),x:m.m41,y:m.m42,scaleX:m.a,scaleY:m.d,transform:c.transform,
    rect:{x:r.x,y:r.y,width:r.width,height:r.height},pointerEvents:c.pointerEvents,
    animations:e.getAnimations().map(a=>({name:a.animationName||a.transitionProperty||'WAAPI',state:a.playState,time:typeof a.currentTime==='number'?a.currentTime:null,progress:a.effect?.getComputedTiming().progress??null}))};
 };
 const snap=()=>{
  const host=document.getElementById('modal-host'),overlay=host?.querySelector('.overlay'),dialog=overlay?.querySelector('.dialog'),stage=overlay?.querySelector('#subtitle-expanded-stage'),app=document.querySelector('.app');
  const back=geometry(overlay),front=geometry(dialog),focused=document.activeElement;
  return {ms:performance.now(),reduce:matchMedia('(prefers-reduced-motion: reduce)').matches,owner:id(overlay),stage:id(stage),
    closing:!!overlay?.classList.contains('is-closing'),label:dialog?.getAttribute('aria-label')||null,back,front,
    effectiveOpacity:back&&front?back.opacity*front.opacity:null,
    inert:app?.inert,focus:id(focused),focusId:focused?.id||null,focusInModal:!!overlay?.contains(focused),opener:id(modalReturnFocus),
    exitTimer:modalExitTimer??null,modalFrame:modalScrollFrame??null,revealFrame:modalFocusRevealFrame??null,scrollOwner:id(modalScrollContainer),
    pendingExits:[...t.timers].map(([handle,owner])=>({handle,owner})),registered:[...t.registered]};
 };
 t.snap=snap;
 // Window capture runs before the application's document Escape handler and
 // element close handler. Capture the actual pre-close state of trusted input.
 const input=e=>{
  if(!t.record)return;
  const key=e.type==='keydown'&&e.key==='Escape';
  const button=e.type==='click'&&e.target.closest?.('#close-dialog');
  if(!key&&!button)return;
  const s=snap();if(!s.owner)return;
  log('close-input',{trusted:e.isTrusted,action:key?'escape':'button',before:s});
 };
 window.addEventListener('keydown',input,true);window.addEventListener('click',input,true);
 const pref=e=>{if(t.record)log('preference',{matches:e.matches,frame:snap()})};
 matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change',pref);
 const animation=e=>{if(t.record&&e.animationName?.startsWith('gallery-dialog')||t.record&&e.animationName?.startsWith('gallery-backdrop'))log(e.type,{name:e.animationName,elapsed:e.elapsedTime,target:id(e.target),frame:snap()})};
 for(const type of ['animationstart','animationend','animationcancel'])document.addEventListener(type,animation,true);
 t.start=()=>{
  t.record=true;
  const observer=new MutationObserver(records=>{
   if(records.some(r=>r.type==='childList'&&r.target===modalHost||r.type==='attributes'&&r.target.classList?.contains('overlay')))
    log('modal-mutation',{frame:snap()});
  });
  observer.observe(modalHost,{childList:true,subtree:true,attributes:true,attributeFilter:['class']});
  t.observer=observer;
  const tick=()=>{if(!t.record)return;t.frames.push(snap());t.raf=requestAnimationFrame(tick)};
  t.frames.push(snap());t.raf=requestAnimationFrame(tick);
 };
 t.finish=()=>{t.record=false;t.observer?.disconnect();cancelAnimationFrame(t.raf);return {frames:t.frames,events:t.events}};
})()"""
SETTLED="()=>!galleryStageTransition&&!galleryStageFadeInProgress&&!galleryStagePending&&!gallerySettingsOpening&&!settingsClosing"
def snap(p):return p.evaluate("window.__a32.snap()")
def wait(p,expr,timeout=5000):p.wait_for_function(expr,timeout=timeout,polling="raf")
def settle(p):
    wait(p,SETTLED)
    p.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
def prepare(p,kind):
    if kind=="filters":
        opener=p.locator("#filters")
        opener.wait_for(state="visible")
    else:
        p.locator("#settings").click();settle(p)
        p.locator('[data-settings-section="playback"]').click()
        p.locator('[data-playback-tab="subtitles"]').click()
        opener=p.locator("#subtitle-compact-preview") if p.locator("#subtitle-compact-preview").is_visible() else p.locator("#subtitle-expand-preview")
        opener.wait_for(state="visible")
    opener.scroll_into_view_if_needed()
    # Explicitly settle the normal opener and verify original focus identity.
    opener.focus()
    return opener
def open_dialog(p,opener):
    # Stable real control; no force-click, synthetic event, or animation seek.
    opener.click()
    wait(p,"()=>!!modalHost.querySelector('.overlay')")
    s=snap(p)
    assert s["inert"] and s["focusInModal"] and s["opener"],s
    return s
def entrance(p,phase):
    if phase=="settled":
        wait(p,"()=>{const s=window.__a32.snap();return s.front&&s.front.opacity>=.999&&s.back.opacity>=.999&&Math.abs(s.front.y)<.01&&s.front.animations.every(a=>a.state!=='running')&&s.back.animations.every(a=>a.state!=='running')}")
    else:
        threshold=20 if phase=="early" else 75
        wait(p,"()=>{const s=window.__a32.snap(),a=s.front?.animations.find(a=>a.name==='gallery-dialog-in');return !!a&&a.state==='running'&&a.time>="+str(threshold)+"&&a.time<170&&s.front.opacity>.001&&s.front.opacity<.999}")
    return snap(p)
def close_input(p,method):
    if method=="escape":p.keyboard.press("Escape")
    else:
        # Avoid Playwright stability waits on the animating close button.
        # Real pointer hit is verified in the event capture below.
        b=p.locator("#close-dialog").bounding_box();assert b,b
        x,y=b["x"]+b["width"]/2,b["y"]+b["height"]/2
        assert p.evaluate("([x,y])=>!!document.elementFromPoint(x,y)?.closest('#close-dialog')",[x,y]),("close button occluded",b)
        p.mouse.click(x,y)
def closed(p,opener):
    wait(p,"()=>!modalHost.firstElementChild&&modalExitTimer===null")
    s=snap(p)
    assert not s["inert"] and not s["owner"] and not s["opener"] and s["modalFrame"] is None and s["revealFrame"] is None and s["scrollOwner"] is None and not s["pendingExits"] and not s["registered"],s
    assert opener.evaluate("e=>document.activeElement===e"),s
    return s
def close_events(trace):
    return [e for e in trace["events"] if e["type"]=="close-input"]
def relevant_frames(trace,owner,event):
    return [s for s in trace["frames"] if s["ms"]>=event["ms"] and s["owner"]==owner and s["closing"]]
def jump(before,after):
    return {"backdropOpacity":after["back"]["opacity"]-before["back"]["opacity"],
        "dialogOpacity":after["front"]["opacity"]-before["front"]["opacity"],
        "effectiveOpacity":after["effectiveOpacity"]-before["effectiveOpacity"],
        "translateY":after["front"]["y"]-before["front"]["y"],
        "scaleX":after["front"]["scaleX"]-before["front"]["scaleX"],
        "scaleY":after["front"]["scaleY"]-before["front"]["scaleY"],
        "rectY":after["front"]["rect"]["y"]-before["front"]["rect"]["y"]}
normal_cases=(("early","escape"),("early","button"),("mid","escape"),("settled","escape"),("settled","button"),("replace","escape"),("reopen","escape"),("live-close","escape"))
reduce_cases=(("settled","escape"),("settled","button"),("reopen","escape"))
cases=normal_cases if motion=="no-preference" else reduce_cases
def run(browser,width,kind,phase,method):
    row={"width":width,"dialog":kind,"phase":phase,"method":method,"status":"pending","errors":[]}
    report["cases"].append(row)
    context=browser.new_context(viewport={"width":width,"height":800},reduced_motion=motion)
    p=context.new_page();p.on("pageerror",lambda e:row["errors"].append(str(e)))
    try:
        p.add_init_script(INIT)
        p.route("**/*",lambda r:r.fulfill(status=200,content_type="text/html; charset=utf-8",body=source) if r.request.url==origin else r.abort())
        p.goto(origin,wait_until="domcontentloaded");settle(p)
        opener=prepare(p,kind)
        p.evaluate("window.__a32.start()")
        row["open"]=open_dialog(p,opener)
        owner=row["open"]["owner"]
        if kind=="subtitle":assert row["open"]["stage"] in row["open"]["registered"],row["open"]
        if motion=="no-preference":
            row["trigger"]=entrance(p,phase if phase in ("early","mid") else "settled")
        else:
            row["trigger"]=snap(p)
            assert row["trigger"]["front"]["opacity"]==1 and row["trigger"]["back"]["opacity"]==1
            assert not row["trigger"]["front"]["animations"] and not row["trigger"]["back"]["animations"],row["trigger"]
        close_input(p,method)
        if phase=="replace":
            # Programmatic stress is deliberately separate from trusted close:
            # app is inert so a real underlying opener cannot be clicked yet.
            wait(p,"()=>window.__a32.frames.some(s=>s.closing&&s.owner===window.__a32.snap().owner)")
            row["beforeReplacement"]=snap(p)
            assert row["beforeReplacement"]["owner"]==owner and row["beforeReplacement"]["exitTimer"] is not None
            p.evaluate("()=>{"+("showExpandedSubtitlePreview()" if kind=="subtitle" else "showFilters()")+"}")
            row["replacement"]=snap(p)
            assert row["replacement"]["owner"]!=owner and row["replacement"]["inert"] and row["replacement"]["opener"]==row["open"]["opener"],row
            assert row["replacement"]["exitTimer"] is None and not row["replacement"]["pendingExits"],row["replacement"]
            assert row["open"]["stage"] not in row["replacement"]["registered"],row["replacement"]
            if kind=="subtitle":assert row["replacement"]["stage"] in row["replacement"]["registered"]
            # Past original exit deadline AND normal replacement entrance.
            entrance(p,"settled")
            p.wait_for_timeout(180)
            assert snap(p)["owner"]==row["replacement"]["owner"] and snap(p)["inert"],"Replacement removed by old timer"
            close_input(p,"escape")
            row["final"]=closed(p,opener)
        elif phase=="live-close":
            wait(p,"()=>{const s=window.__a32.snap();return s.closing&&s.front.opacity<.98&&s.front.opacity>.1}")
            row["beforeSwitch"]=snap(p)
            p.emulate_media(reduced_motion="reduce")
            wait(p,"()=>window.__a32.events.some(e=>e.type==='preference'&&e.matches)")
            row["final"]=closed(p,opener)
            p.emulate_media(reduced_motion="no-preference")
            wait(p,"()=>window.__a32.events.some(e=>e.type==='preference'&&!e.matches)")
            p.wait_for_timeout(250)
            assert not snap(p)["owner"] and not snap(p)["inert"],"Stale replay after re-enable"
        else:
            row["final"]=closed(p,opener)
            if phase=="reopen":
                row["reopened"]=open_dialog(p,opener)
                assert row["reopened"]["owner"]!=owner,row["reopened"]
                if motion=="no-preference":entrance(p,"settled")
                close_input(p,"escape")
                row["final"]=closed(p,opener)
        # Remain beyond all former 150ms exit callbacks and pending RAF work.
        p.wait_for_timeout(180)
        row["after"]=snap(p)
        assert row["after"]["owner"] is None and not row["after"]["inert"] and not row["after"]["pendingExits"] and not row["after"]["registered"]
        row["trace"]=p.evaluate("window.__a32.finish()")
        events=close_events(row["trace"]);assert len(events)==(2 if phase in ("replace","reopen") else 1),events
        first=events[0];before=first["before"]
        assert first["trusted"] and first["action"]==method and before["owner"]==owner and not before["closing"],first
        assert all(e["trusted"] for e in events),events
        assert not row["errors"],row["errors"]
        row["findings"]={"preClose":before,"closeAction":method}
        frames=relevant_frames(row["trace"],owner,first)
        if motion=="no-preference":
            assert frames,"No actual closing frame"
            # The real input capture, not a previous polling result, proves
            # the entrance had not completed when the close was requested.
            if phase in ("early","mid"):
                animation=next((a for a in before["front"]["animations"] if a["name"]=="gallery-dialog-in"),None)
                assert animation and animation["state"]=="running" and 0<animation["time"]<220 and .001<before["front"]["opacity"]<.999,("Missed intermediate input window",before)
            else:
                assert before["front"]["opacity"]>=.999 and before["back"]["opacity"]>=.999,before
            first_frame=frames[0]
            assert any(a["name"]=="gallery-dialog-out" for a in first_frame["front"]["animations"]),first_frame
            row["findings"].update(firstClosingFrame=first_frame,delta=jump(before,first_frame),frameLatencyMs=first_frame["ms"]-first["ms"])
            scheduled=[e for e in row["trace"]["events"] if e["type"]=="exit-schedule" and e["owner"]==owner]
            delivered=[e for e in row["trace"]["events"] if e["type"]=="exit-deliver" and e["owner"]==owner]
            canceled=[e for e in row["trace"]["events"] if e["type"]=="exit-cancel" and e["owner"]==owner]
            assert len(scheduled)==1 and scheduled[0]["delay"]==150,scheduled
            if phase=="replace":assert len(canceled)==1 and not delivered and canceled[0]["handle"]==scheduled[0]["handle"],(canceled,delivered)
            else:assert len(delivered)==1 and not canceled and delivered[0]["handle"]==scheduled[0]["handle"],(canceled,delivered)
            if phase=="live-close":
                ev=next(e for e in row["trace"]["events"] if e["type"]=="preference" and e["matches"])
                assert row["beforeSwitch"]["closing"] and .1<row["beforeSwitch"]["front"]["opacity"]<.98
                post=[s for s in frames if s["ms"]>=ev["ms"] and s["reduce"]]
                row["findings"]["liveClose"]={"atPreference":ev["frame"],"retainedFrames":len(post),"inertFrames":sum(bool(s["inert"]) for s in post),"maxEffectiveOpacity":max((s["effectiveOpacity"] for s in post),default=None),"remainingUntilExitMs":delivered[0]["ms"]-ev["ms"]}
        else:
            assert not frames and not any(e["type"]=="exit-schedule" for e in row["trace"]["events"]),"Unexpected reduced-motion exit animation/timer"
        if kind=="subtitle":
            observed=[e["node"] for e in row["trace"]["events"] if e["type"]=="observe"]
            unobserved=[e["node"] for e in row["trace"]["events"] if e["type"]=="unobserve"]
            assert sorted(observed)==sorted(unobserved) and len(observed)==(2 if phase in ("replace","reopen") else 1),(observed,unobserved)
            assert not any(e["type"]=="observer-deliver" and not e["connected"] for e in row["trace"]["events"]),"Detached subtitle observer delivery"
        row["status"]="collected"
        summary={k:v for k,v in row["findings"].items() if k not in ("preClose","firstClosingFrame","liveClose")}
        if "liveClose" in row["findings"]:summary["liveClose"]={k:v for k,v in row["findings"]["liveClose"].items() if k!="atPreference"}
        print("COLLECTED",mode,motion,width,kind,phase,method,json.dumps(summary),flush=True)
    except Exception as e:
        row["status"]="harness-error";row["exception"]=str(e);row["stack"]=traceback.format_exc()
        try:row["trace"]=p.evaluate("window.__a32?.finish()")
        except Exception:pass
        print("HARNESS ERROR",mode,motion,width,kind,phase,method,str(e)[:2000],flush=True)
    finally:
        context.close();out.write_text(json.dumps(report,indent=2),encoding="utf-8")
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path=os.environ.get("GALLERY_TEST_CHROMIUM") or None,args=["--no-sandbox","--disable-dev-shm-usage"])
    for width in (1440,620):
        for kind in ("filters","subtitle"):
            for phase,method in cases:run(browser,width,kind,phase,method)
    browser.close()
expected_cases=4*len(cases)
report["summary"]={"expected":expected_cases,"collected":sum(r["status"]=="collected" for r in report["cases"]),"harnessErrors":sum(r["status"]!="collected" for r in report["cases"]),"pageErrors":sum(len(r["errors"]) for r in report["cases"])}
out.write_text(json.dumps(report,indent=2),encoding="utf-8")
print("A3.2 SUMMARY",json.dumps(report["summary"]),flush=True)
assert len(report["cases"])==expected_cases and report["summary"]["collected"]==expected_cases and not report["summary"]["pageErrors"],report["summary"]
