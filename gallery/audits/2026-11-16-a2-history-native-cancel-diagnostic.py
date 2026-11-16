#!/usr/bin/env python3
"""Read-only A2.3: trace native cancellation on exact baseline and failed candidate."""
import hashlib,json,os,sys,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright

variant,mode,root,out=sys.argv[1:]
assert variant in ("baseline","candidate") and mode in ("full","lightweight")
root=Path(root).resolve()
path=root/"gallery"/("Gallery-current.html" if mode=="full" else "Gallery-development.html")
source=path.read_bytes()
expected={
 "baseline":{"full":"8d5f336085058725f49d4fd97cdbc6cddf1a1d9b1afe19f643bdca062c7297f4","lightweight":"fa25eb4f63486966775ff3b3a7817898859e1d7520713ed1304f77f5ebc7aecd"},
 "candidate":{"full":"6f558d22ec21047a978af0d262277c508366a37e6d3d63f8bf1952016aa33ae5","lightweight":"fccd6b1dae4595eef6ff201c1e30912376745240fd452f8ba3e121ec93b92060"}
}[variant][mode]
assert hashlib.sha256(source).hexdigest()==expected
origin="https://gallery-a23-cancel.invalid/"
report={"variant":variant,"mode":mode,"sha256":expected,"cases":[]}
# Native event observers and CSSAnimation inspection; no synthesized transition
# event is used to establish browser behavior. Overlay calls are counted, not changed.
instrument=r"""()=>{
 const p=document.querySelector('[data-wh-row="pkm"] .wh-episodes');
 window.__cancelPanel=p;window.__cancelTrace={events:[],stages:[],overlay:0,frames:[]};
 const t=window.__cancelTrace,counts=new WeakMap(),old=updateTabScrollOverlay;
 updateTabScrollOverlay=function(...args){t.overlay++;return old(...args)};
 const snapshot=()=>{const cs=getComputedStyle(p),row=p.closest('[data-wh-row]');
  return {t:performance.now(),reduce:matchMedia('(prefers-reduced-motion: reduce)').matches,
    transition:cs.transitionProperty,duration:cs.transitionDuration,grid:cs.gridTemplateRows,height:p.getBoundingClientRect().height,
    expanded:row.classList.contains('is-expanded'),inert:p.querySelector('.wh-episodes-inner').inert,
    animations:p.getAnimations().map(a=>({property:a.transitionProperty,state:a.playState,time:a.currentTime,start:a.startTime,
       duration:a.effect?.getTiming().duration,progress:a.effect?.getComputedTiming().progress})),overlay:t.overlay};
 };
 window.__cancelSnap=label=>{const s=snapshot();t.stages.push({label,...s});return s};
 for(const type of ['transitionrun','transitionstart','transitionend','transitioncancel']){
  document.addEventListener(type,e=>{
   if(e.target!==p)return;
   counts.set(e,t.overlay);t.events.push({where:'capture',type,property:e.propertyName,elapsed:e.elapsedTime,trusted:e.isTrusted,...snapshot()});
  },true);
  p.addEventListener(type,e=>{
   if(e.target===p)t.events.push({where:'target',type,property:e.propertyName,elapsed:e.elapsedTime,trusted:e.isTrusted,overlay:t.overlay,t:performance.now()});
  });
  screen.addEventListener(type,e=>{
   if(e.target===p)t.events.push({where:'screen',type,property:e.propertyName,elapsed:e.elapsedTime,trusted:e.isTrusted,refreshes:t.overlay-counts.get(e),t:performance.now()});
  });
 }
 window.__cancelFrames=()=>{const start=performance.now();function step(){t.frames.push(snapshot());if(performance.now()-start<1200)requestAnimationFrame(step)}requestAnimationFrame(step)};
}"""
def settle_route(page):
    page.wait_for_function("()=>!galleryStageTransition&&!galleryStageFadeInProgress&&!galleryStagePending",timeout=10000)
    page.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
def panel_settled(page):
    # Preserve the original failure's exact settling predicate.
    page.wait_for_function("()=>!window.__cancelPanel.getAnimations().some(a=>a.playState==='running'||a.playState==='pending')",timeout=10000)
    page.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
def snap(page,label):return page.evaluate("label=>window.__cancelSnap(label)",label)
def grid_events(trace,kind,where="screen"):
    return [e for e in trace["events"] if e["where"]==where and e["type"]==kind and e["property"]=="grid-template-rows" and e["trusted"]]
def run_case(browser,width,initial,kind,repeat):
    context=browser.new_context(viewport={"width":width,"height":850},reduced_motion=initial)
    page=context.new_page();errors=[];page.on("pageerror",lambda e:errors.append(str(e)))
    row={"width":width,"initial":initial,"kind":kind,"repeat":repeat,"status":"completed","errors":errors}
    try:
        page.route("**/*",lambda r:r.fulfill(status=200,content_type="text/html; charset=utf-8",body=source) if r.request.url==origin else r.abort())
        page.goto(origin,wait_until="domcontentloaded")
        page.locator("#header-watch-history").click()
        page.wait_for_function("()=>whOpen&&!!document.querySelector('#wh-root')",timeout=10000);settle_route(page)
        page.evaluate(instrument)
        hit=page.locator('[data-wh-expand="pkm"]')
        hit.press("Enter");panel_settled(page);opened=snap(page,"first open")
        assert opened["expanded"] and not opened["inert"] and opened["height"]>1,opened
        page.emulate_media(reduced_motion="no-preference")
        page.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
        snap(page,"normal before close")
        if kind!="original":page.evaluate("window.__cancelFrames()")
        hit.press("Enter")
        if kind=="original":
            # Exactly the failed regression's running predicate and CDP work
            # between it and emulate_media, followed by the same settle.
            page.wait_for_function("()=>window.__cancelPanel.getAnimations().some(a=>a.playState==='running')",timeout=5000)
            running=snap(page,"original running")
            cdp=context.new_cdp_session(page)
            obj=cdp.send("Runtime.evaluate",{"expression":"window.__cancelPanel","objectGroup":"cancel-count"})["result"]
            cdp.send("DOMDebugger.getEventListeners",{"objectId":obj["objectId"]})
            cdp.send("Runtime.releaseObjectGroup",{"objectGroup":"cancel-count"})
            cdp.detach()
            page.emulate_media(reduced_motion="reduce");panel_settled(page)
        elif kind=="media-after-start":
            # Synchronize on a genuine grid transitionstart, not any animation.
            page.wait_for_function("""()=>window.__cancelTrace.events.some(e=>e.where==='capture'&&e.type==='transitionstart'&&e.property==='grid-template-rows'&&!e.expanded)&&window.__cancelPanel.getAnimations().some(a=>a.transitionProperty==='grid-template-rows'&&a.playState==='running')""",timeout=5000)
            running=snap(page,"grid start observed")
            page.emulate_media(reduced_motion="reduce");panel_settled(page)
        elif kind in ("reversal","native-cancel"):
            # Perform action inside one browser turn immediately after a trusted
            # start. This avoids round-trip latency exhausting a 280 ms transition.
            running=page.evaluate("""async kind=>{
             const p=window.__cancelPanel,t=window.__cancelTrace;
             const start=performance.now();
             while(performance.now()-start<3000){
              const a=p.getAnimations().find(a=>a.transitionProperty==='grid-template-rows'&&a.playState==='running'&&Number(a.currentTime)>0);
              if(a){
               const before=window.__cancelSnap('native active before '+kind);
               if(kind==='reversal')p.closest('[data-wh-row]').querySelector('.wh-summary-hit').click();
               else a.cancel();
               return before;
              }
              await new Promise(r=>requestAnimationFrame(r));
             }throw Error('No active grid transition');
            }""",kind)
            panel_settled(page)
        else:raise AssertionError(kind)
        early=snap(page,"original settle boundary")
        early_trace=page.evaluate("window.__cancelTrace")
        page.wait_for_timeout(650)
        late=snap(page,"late boundary")
        trace=page.evaluate("window.__cancelTrace")
        row["trace"]=trace
        row["running"]=running
        row["early"]={k:early[k] for k in ("reduce","expanded","height","animations","transition","duration")}
        row["late"]={k:late[k] for k in ("reduce","expanded","height","animations","transition","duration")}
        row["findings"]={
            "early_cancel":len(grid_events(early_trace,"transitioncancel")),
            "late_cancel":len(grid_events(trace,"transitioncancel")),
            "captured_cancel":len(grid_events(trace,"transitioncancel","capture")),
            "target_cancel":len(grid_events(trace,"transitioncancel","target")),
            "grid_end":len(grid_events(trace,"transitionend")),
            "cancel_refreshes":[e["refreshes"] for e in grid_events(trace,"transitioncancel")],
            "end_refreshes":[e["refreshes"] for e in grid_events(trace,"transitionend")],
            "final_expanded":late["expanded"],"final_inert":late["inert"]
        }
        assert late["expanded"]==(kind=="reversal") and late["inert"]!=late["expanded"],late
        assert (late["height"]>1)==late["expanded"],late
        # Independent positive completion after restoration, no altered CSS.
        if late["reduce"]:page.emulate_media(reduced_motion="no-preference")
        page.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
        hit.press("Enter");panel_settled(page);page.wait_for_timeout(350)
        row["post_restore"]=snap(page,"normal completion after trial")
        row["trace"]=page.evaluate("window.__cancelTrace")
    except Exception:
        row["status"]="harness_error";row["exception"]=traceback.format_exc()
        try:row["trace"]=page.evaluate("window.__cancelTrace||{}")
        except Exception:pass
    finally:
        context.close()
        report["cases"].append(row);Path(out).write_text(json.dumps(report,indent=2))
        print("A2.3 CANCEL CASE",json.dumps({k:v for k,v in row.items() if k!="trace"}),flush=True)
def control(browser):
    # Browser-only control uses the same transition property/duration/curve
    # and reduced-motion rule, with no Gallery JS or app state.
    p=browser.new_page(reduced_motion="no-preference")
    p.set_content("""<style>#panel{display:grid;grid-template-rows:1fr;transition:grid-template-rows .28s cubic-bezier(.22,.7,.25,1)}#panel.closed{grid-template-rows:0fr}#panel>div{min-height:0;overflow:hidden}@media(prefers-reduced-motion:reduce){#panel{transition:none!important}}</style><div id="panel"><div style="min-height:0"><div style="height:200px">control</div></div></div>""")
    p.evaluate("""()=>{window.events=[];const panel=document.getElementById('panel');for(const type of ['transitionrun','transitionstart','transitionend','transitioncancel'])panel.addEventListener(type,e=>window.events.push({type,property:e.propertyName,trusted:e.isTrusted,t:performance.now()}));void panel.offsetHeight;panel.classList.add('closed')}""")
    p.wait_for_function("()=>window.events.some(e=>e.type==='transitionstart'&&e.property==='grid-template-rows')",timeout=5000)
    p.emulate_media(reduced_motion="reduce");p.wait_for_timeout(650)
    result=p.evaluate("()=>({events:window.events,height:document.getElementById('panel').getBoundingClientRect().height,transition:getComputedStyle(document.getElementById('panel')).transitionProperty})")
    p.close();return result
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path=os.environ.get("GALLERY_TEST_CHROMIUM") or None,args=["--no-sandbox"])
    report["control"]=control(browser)
    print("A2.3 CANCEL CONTROL",json.dumps(report["control"]),flush=True)
    for width in (1440,620):
        for initial in ("no-preference","reduce"):
            for kind in ("original","media-after-start","reversal","native-cancel"):
                for repeat in range(2):run_case(browser,width,initial,kind,repeat)
    browser.close()
summary={"cases":len(report["cases"]),"harness_errors":sum(r["status"]!="completed" for r in report["cases"]),"page_errors":sum(bool(r["errors"]) for r in report["cases"]),"by_kind":{}}
for kind in ("original","media-after-start","reversal","native-cancel"):
    rows=[r for r in report["cases"] if r["kind"]==kind and r["status"]=="completed"]
    summary["by_kind"][kind]={"completed":len(rows),"early_cancel":sum(r["findings"]["early_cancel"]>0 for r in rows),"late_cancel":sum(r["findings"]["late_cancel"]>0 for r in rows),"capture_cancel":sum(r["findings"]["captured_cancel"]>0 for r in rows),"cancel_refreshes":[v for r in rows for v in r["findings"]["cancel_refreshes"]]}
report["summary"]=summary;Path(out).write_text(json.dumps(report,indent=2))
print("A2.3 CANCEL SUMMARY",variant,mode,json.dumps(summary),flush=True)
assert summary["cases"]==32 and not summary["harness_errors"] and not summary["page_errors"],summary
