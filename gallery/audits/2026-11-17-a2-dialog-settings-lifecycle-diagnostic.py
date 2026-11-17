#!/usr/bin/env python3
"""A2.4 read-only resource ownership diagnostic; exact published A2.3 HTML."""
import hashlib,json,os,sys,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright

mode,motion,out=sys.argv[1:]
assert mode in ("full","lightweight") and motion in ("no-preference","reduce")
path=Path(__file__).resolve().parents[1]/("Gallery-current.html" if mode=="full" else "Gallery-development.html")
source=path.read_bytes()
expected={"full":"6f558d22ec21047a978af0d262277c508366a37e6d3d63f8bf1952016aa33ae5","lightweight":"fccd6b1dae4595eef6ff201c1e30912376745240fd452f8ba3e121ec93b92060"}[mode]
assert hashlib.sha256(source).hexdigest()==expected
origin="https://gallery-a24.invalid/"
report={"mode":mode,"motion":motion,"sha256":expected,"cases":[]}
# Preserve native scheduling, observer delivery and DOM setters. Tag only
# relevant call sites, propagate tags to recursive RAF steps, and log writes.
# Weak references avoid keeping an otherwise collectible observer target alive.
init=r"""(()=>{
 const trace={events:[],observers:[],raf:new Map(),timers:new Map(),ids:new WeakMap(),serial:0,active:null};
 window.__a24=trace;
 const id=x=>{if(!x)return null;if(!trace.ids.has(x))trace.ids.set(x,++trace.serial);return trace.ids.get(x)};
 trace.id=id;
 const log=(type,info={})=>trace.events.push({type,t:performance.now(),...info});
 const context=()=>({settings:document.body?.classList.contains('settings-view')??false,
  closing:typeof settingsClosing!=='undefined'&&settingsClosing,
  modal:!!document.querySelector('#modal-host .overlay,.overlay[role="presentation"]'),
  modalClosing:!!document.querySelector('.overlay.is-closing')});
 const nativeRAF=window.requestAnimationFrame.bind(window),nativeCancel=window.cancelAnimationFrame.bind(window);
 const nativeSet=window.setTimeout.bind(window),nativeClear=window.clearTimeout.bind(window);
 function tag(){
  const stack=new Error().stack||'';
  if(stack.includes('revealModalControl'))return 'modal-scroll';
  if(stack.includes('revealSettingsControl'))return 'settings-scroll';
  if(stack.includes('navigateToSettingsResult'))return 'settings-reveal';
  return trace.active;
 }
 window.requestAnimationFrame=function(cb){
  const kind=tag();if(!kind)return nativeRAF(cb);
  let handle;handle=nativeRAF(function(now){
   trace.raf.delete(handle);const old=trace.active;trace.active=kind;
   log('raf-deliver',{kind,handle,...context()});
   try{return cb(now)}finally{trace.active=old}
  });
  trace.raf.set(handle,kind);log('raf-schedule',{kind,handle,...context()});return handle;
 };
 window.cancelAnimationFrame=function(handle){
  if(trace.raf.has(handle)){log('raf-cancel',{handle,kind:trace.raf.get(handle),...context()});trace.raf.delete(handle)}
  return nativeCancel(handle);
 };
 window.setTimeout=function(cb,delay,...args){
  const kind=(new Error().stack||'').includes('navigateToSettingsResult')?'settings-highlight':null;
  if(!kind||typeof cb!=='function')return nativeSet(cb,delay,...args);
  let handle;handle=nativeSet(function(...a){
   trace.timers.delete(handle);log('timer-deliver',{kind,handle,...context()});return cb(...a);
  },delay,...args);
  trace.timers.set(handle,kind);log('timer-schedule',{kind,handle,delay,...context()});return handle;
 };
 window.clearTimeout=function(handle){
  if(trace.timers.has(handle)){log('timer-cancel',{handle,kind:trace.timers.get(handle),...context()});trace.timers.delete(handle)}
  return nativeClear(handle);
 };
 const d=Object.getOwnPropertyDescriptor(Element.prototype,'scrollTop');
 if(d?.set&&d.configurable)Object.defineProperty(Element.prototype,'scrollTop',{...d,set(value){
  if(trace.active&&(this.matches('.dialog-scroll,.workspace')))log('scroll-write',{kind:trace.active,node:id(this),connected:this.isConnected,value,...context()});
  return d.set.call(this,value);
 }});
 trace.scrollInstrumented=!!d?.set&&d.configurable;
 const Native=window.ResizeObserver;
 window.ResizeObserver=class extends Native{
  constructor(cb){
   const row={id:++trace.serial,targets:new Map(),observes:0,unobserves:0,disconnects:0};
   super((entries,observer)=>{
    const subtitle=entries.filter(e=>e.target.matches('#subtitle-preview-stage,#subtitle-expanded-stage'));
    if(subtitle.length)log('observer-deliver',{owner:row.id,targets:subtitle.map(e=>({id:id(e.target),connected:e.target.isConnected,registered:row.targets.has(id(e.target))})),...context()});
    return cb(entries,observer);
   });
   this.__a24row=row;trace.observers.push(row);
  }
  observe(target,...args){
   if(target.matches('#subtitle-preview-stage,#subtitle-expanded-stage')){
    const row=this.__a24row;row.targets.set(id(target),{ref:new WeakRef(target),role:target.id});row.observes++;
    log('observe',{owner:row.id,node:id(target),role:target.id,...context()});
   }
   return super.observe(target,...args);
  }
  unobserve(target){
   const row=this.__a24row;
   if(row.targets.delete(id(target))){row.unobserves++;log('unobserve',{owner:row.id,node:id(target),...context()})}
   return super.unobserve(target);
  }
  disconnect(){
   const row=this.__a24row;if(row.targets.size){row.disconnects++;log('disconnect',{owner:row.id,...context()})}
   row.targets.clear();return super.disconnect();
  }
 };
 trace.snapshot=()=>{
  const overlay=modalHost.querySelector('.overlay'),active=document.activeElement;
  return {t:performance.now(),eventCount:trace.events.length,settings:document.body.classList.contains('settings-view'),
   settingsClosing,modal:!!overlay,modalClosing:overlay?.classList.contains('is-closing')??false,
   modalFrame:modalScrollFrame!==null,modalOwner:id(modalScrollContainer),modalOwnerConnected:modalScrollContainer?.isConnected??null,
   settingsFrame:settingsScrollFrame!==null,highlightTimer:trace.timers.has(settingsJumpTimer),
   highlightCount:settingsPage.querySelectorAll('.settings-search-target').length,
   raf:[...trace.raf.values()],timers:[...trace.timers.values()],workspaceTop:workspace.scrollTop,
   opener:id(modalReturnFocus),focus:id(active),focusId:active?.id,appInert:galleryApp.inert,
   popover:!!document.querySelector('.gallery-color-popover'),
   observers:trace.observers.filter(r=>r.observes).map(r=>({id:r.id,observes:r.observes,unobserves:r.unobserves,disconnects:r.disconnects,
     targets:[...r.targets].map(([id,v])=>({id,role:v.role,connected:v.ref.deref()?.isConnected??false,collected:!v.ref.deref()}))}))};
 };
})()"""
def settled(page):
    page.wait_for_function("()=>!galleryStageTransition&&!galleryStageFadeInProgress&&!galleryStagePending&&!gallerySettingsOpening&&!settingsClosing",timeout=10000)
    page.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
def open_settings(page):
    page.locator("#settings").click()
    page.wait_for_function("()=>document.body.classList.contains('settings-view')",timeout=10000);settled(page)
def subtitles(page):
    open_settings(page)
    page.locator('[data-settings-section="playback"]').click()
    page.locator('[data-playback-tab="subtitles"]').click()
    page.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
def snap(page,row,label):
    s=page.evaluate("window.__a24.snapshot()");row["trace"].append({"label":label,"snapshot":s});return s
def events(page,start=0):return page.evaluate("n=>window.__a24.events.slice(n)",start)
def targets(s,role=None):
    return [t for o in s["observers"] for t in o["targets"] if role is None or t["role"]==role]
def writes(ev,kind):return [e for e in ev if e["type"]=="scroll-write" and e["kind"]==kind]
def close_modal(page):
    page.keyboard.press("Escape")
    page.wait_for_function("()=>!modalHost.firstElementChild",timeout=3000)
def close_settings(page):
    page.keyboard.press("Escape")
    page.wait_for_function("()=>!document.body.classList.contains('settings-view')",timeout=10000);settled(page)
def fixture(page):
    # Deliberately controlled overflowing dialog, using the real modal API and
    # native keyboard wrap. No production markup or source is altered.
    page.evaluate("""()=>{document.getElementById('settings').focus();modal('A2.4 diagnostic scroll fixture',
       '<div style="min-height:1600px"><button id="a24-first">First</button></div>',
       '<button id="a24-last">Last</button>');document.getElementById('close-dialog').focus({preventScroll:true})}""")
    page.locator('#close-dialog').wait_for()
    page.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
def run_case(browser,width,kind,repeat):
    context=browser.new_context(viewport={"width":width,"height":700},reduced_motion=motion)
    page=context.new_page();errors=[];page.on("pageerror",lambda e:errors.append(str(e)))
    row={"width":width,"kind":kind,"repeat":repeat,"status":"completed","errors":errors,"trace":[],"findings":{}}
    try:
        page.add_init_script(init)
        page.route("**/*",lambda r:r.fulfill(status=200,content_type="text/html; charset=utf-8",body=source) if r.request.url==origin else r.abort())
        page.goto(origin,wait_until="domcontentloaded");settled(page)
        assert page.evaluate("window.__a24.scrollInstrumented"),"Missing scrollTop instrumentation"
        if kind in ("modal-close","modal-replace"):
            fixture(page)
            base=snap(page,row,"fixture ready")
            assert base["appInert"] and base["opener"],base
            page.keyboard.press("Shift+Tab")
            active=snap(page,row,"real keyboard wrap")
            assert active["focusId"]=="a24-last",active
            if motion=="no-preference":assert active["modalFrame"] and active["modalOwnerConnected"],active
            else:assert not active["modalFrame"],active
            old=page.evaluate("()=>{window.__a24Old=modalHost.querySelector('.dialog-scroll');return window.__a24.id(window.__a24Old)}")
            if kind=="modal-close":page.keyboard.press("Escape")
            else:page.evaluate("modal('A2.4 replacement','<button id=\"a24-replacement\">Replacement</button>')")
            after=snap(page,row,"departure initiated")
            if kind=="modal-close":page.wait_for_function("()=>!modalHost.firstElementChild",timeout=3000)
            else:assert page.locator("#a24-replacement").count()==1
            mid=snap(page,row,"old DOM departed")
            page.wait_for_timeout(500);late=snap(page,row,"scroll interval elapsed")
            ev=events(page,active["eventCount"])
            ww=[e for e in writes(ev,"modal-scroll") if e["node"]==old]
            row["findings"].update({"frame_at_departure":after["modalFrame"],"frame_after_dom_departure":mid["modalFrame"],
               "old_writes":len(ww),"detached_writes":sum(not e["connected"] for e in ww),
               "closing_writes":sum(e["modalClosing"] for e in ww),"frame_after_interval":late["modalFrame"]})
            if kind=="modal-replace":close_modal(page)
            final=snap(page,row,"final closed")
            assert not final["modal"] and not final["appInert"] and final["focus"]==base["opener"],final
        elif kind in ("subtitle-close","subtitle-replace"):
            subtitles(page)
            opener=page.locator("#subtitle-compact-preview") if page.locator("#subtitle-compact-preview").is_visible() else page.locator("#subtitle-expand-preview")
            opener.click();page.locator("#subtitle-expanded-stage").wait_for()
            page.wait_for_timeout(200)
            start=snap(page,row,"expanded preview active")
            expanded=targets(start,"subtitle-expanded-stage");assert len(expanded)==1,expanded
            old=expanded[0]["id"]
            page.evaluate("()=>{window.__a24Old=document.getElementById('subtitle-expanded-stage')}")
            page.set_viewport_size({"width":width-70,"height":700});page.wait_for_timeout(150)
            resized=snap(page,row,"positive live resize")
            positive=[e for e in events(page,start["eventCount"]) if e["type"]=="observer-deliver" and any(t["id"]==old for t in e["targets"])]
            if kind=="subtitle-close":close_modal(page)
            else:page.evaluate("modal('A2.4 replacement','<button id=\"a24-replacement\">Replacement</button>')")
            departed=snap(page,row,"expanded stage departed")
            page.set_viewport_size({"width":width,"height":700});page.wait_for_timeout(250)
            late=snap(page,row,"after resize")
            deliveries=[e for e in events(page,resized["eventCount"]) if e["type"]=="observer-deliver" and any(t["id"]==old for t in e["targets"])]
            row["findings"].update({"positive_resize_callbacks":len(positive),"old_registered":any(t["id"]==old for t in targets(departed)),
              "old_registered_late":any(t["id"]==old for t in targets(late)),"old_detached_callbacks":sum(any(t["id"]==old and not t["connected"] for t in e["targets"]) for e in deliveries)})
            if kind=="subtitle-replace":close_modal(page)
            # Reopen and close normally, then verify Settings owns no targets.
            opener.click();page.locator("#subtitle-expanded-stage").wait_for();page.wait_for_timeout(150)
            reopened=snap(page,row,"second expanded preview")
            row["findings"]["expanded_registrations_on_reopen"]=len(targets(reopened,"subtitle-expanded-stage"))
            close_modal(page);close_settings(page)
            final=snap(page,row,"Settings departed")
            row["findings"]["registrations_after_settings_close"]=len(targets(final))
            assert not final["settings"] and not final["modal"],final
        elif kind in ("settings-highlight","settings-reveal-race"):
            open_settings(page)
            page.locator("#search").click()
            page.locator("#header-search-input").fill("starting volume")
            result=page.locator('[data-settings-search-key="starting-volume"]');result.wait_for()
            if kind=="settings-highlight":
                result.click()
                page.locator("#settings-starting-volume-card.settings-search-target").wait_for()
                active=snap(page,row,"search target highlighted")
                assert active["highlightTimer"],active
                page.evaluate("()=>{window.__a24Old=document.getElementById('settings-starting-volume-card')}")
                close_settings(page)
            else:
                # Explicit same-task stress: execute the real result click and
                # close request before the queued reveal callback can run.
                page.evaluate("""()=>{document.querySelector('[data-settings-search-key="starting-volume"]').click();
                  window.__a24Old=document.getElementById('settings-starting-volume-card');closeSettings()}""")
                active=snap(page,row,"same-task close requested")
                page.wait_for_function("()=>!document.body.classList.contains('settings-view')",timeout=10000);settled(page)
            departed=snap(page,row,"Settings departed")
            page.wait_for_timeout(500);late=snap(page,row,"after scroll interval")
            ev=events(page,active["eventCount"])
            all_ev=events(page)
            row["findings"].update({"highlight_timer_after_close":departed["highlightTimer"],
              "highlight_class_on_old_target":page.evaluate("window.__a24Old.classList.contains('settings-search-target')"),
              "settings_frame_after_close":departed["settingsFrame"],"settings_frame_after_interval":late["settingsFrame"],
              "reveal_delivered_while_closing":sum(e["type"]=="raf-deliver" and e["kind"]=="settings-reveal" and e["closing"] for e in all_ev),
              "scroll_writes_during_close":sum(e["closing"] for e in writes(all_ev,"settings-scroll")),
              "scroll_writes_after_close":sum(not e["settings"] for e in writes(all_ev,"settings-scroll")),
              "workspace_delta_after_close":late["workspaceTop"]-departed["workspaceTop"]})
            # Reopen before original highlight lifetime expires. Old node held
            # for inspection; do not infer a real memory leak.
            open_settings(page);reopened=snap(page,row,"fresh Settings")
            page.wait_for_timeout(2350);final=snap(page,row,"old highlight deadline passed")
            row["findings"].update({"old_timer_delivered":sum(e["type"]=="timer-deliver" for e in events(page,active["eventCount"])),
              "old_highlight_after_deadline":page.evaluate("window.__a24Old.classList.contains('settings-search-target')"),
              "new_highlights":final["highlightCount"],"fresh_settings":final["settings"]})
            assert final["settings"],final
            close_settings(page)
        elif kind=="popover-control":
            subtitles(page)
            page.locator('[data-subtitle-text-color="custom"]').click()
            page.locator(".gallery-color-popover").wait_for()
            start=snap(page,row,"popover open")
            assert start["popover"],start
            page.keyboard.press("Escape")
            page.locator(".gallery-color-popover").wait_for(state="detached")
            after=snap(page,row,"popover closed")
            row["findings"]["closed_on_escape"]=not after["popover"]
            assert not after["popover"] and after["settings"],after
            close_settings(page)
            final=snap(page,row,"Settings departed")
            row["findings"]["popover_after_settings_close"]=final["popover"]
            row["findings"]["registrations_after_settings_close"]=len(targets(final))
        row["events"]=events(page)
    except Exception:
        row["status"]="harness_error";row["exception"]=traceback.format_exc()
        try:row["events"]=events(page)
        except Exception:pass
    finally:
        context.close();report["cases"].append(row);Path(out).write_text(json.dumps(report,indent=2))
        print("A2.4 CASE",json.dumps({k:v for k,v in row.items() if k not in ("trace","events")}),flush=True)
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path=os.environ.get("GALLERY_TEST_CHROMIUM") or None,args=["--no-sandbox"])
    for width in (1440,620):
        for kind in ("modal-close","modal-replace","subtitle-close","subtitle-replace","settings-highlight","settings-reveal-race","popover-control"):
            for repeat in range(2):run_case(browser,width,kind,repeat)
    browser.close()
summary={"cases":len(report["cases"]),"harness_errors":sum(r["status"]!="completed" for r in report["cases"]),"page_errors":sum(bool(r["errors"]) for r in report["cases"])}
report["summary"]=summary;Path(out).write_text(json.dumps(report,indent=2))
print("A2.4 SUMMARY",mode,motion,json.dumps(summary),flush=True)
assert summary["cases"]==28 and not summary["harness_errors"] and not summary["page_errors"],summary
