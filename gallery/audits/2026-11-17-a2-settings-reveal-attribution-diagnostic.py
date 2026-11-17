#!/usr/bin/env python3
"""Read-only A2.4: separate exact Settings reveal from shared overlay RAF."""
import hashlib,json,os,sys,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright
variant,mode,root,out=sys.argv[1:]
assert variant in ("baseline","candidate") and mode in ("full","lightweight")
root=Path(root).resolve()
source=(root/"gallery"/("Gallery-current.html" if mode=="full" else "Gallery-development.html")).read_bytes()
expected={
 "baseline":{"full":"6f558d22ec21047a978af0d262277c508366a37e6d3d63f8bf1952016aa33ae5","lightweight":"fccd6b1dae4595eef6ff201c1e30912376745240fd452f8ba3e121ec93b92060"},
 "candidate":{"full":"c52a8c8a8a75c1ae5187fbb577c0ea146a36db9d45aae97320d6638c598be009","lightweight":"54c69064ac691fa3b191a19741390a4efcd7f492f09cf91ca9ccb441671bded3"}
}[variant][mode]
assert hashlib.sha256(source).hexdigest()==expected
origin="https://gallery-a24-attribution.invalid/"
report={"variant":variant,"mode":mode,"sha256":expected,"cases":[]}
# Runtime observation only: no alteration of input bytes or scheduling policy.
# Original stack classifier retained alongside precise callback identity.
instrument=r"""()=>{
 const t={events:[],pending:new Map(),active:null,probing:false,serial:0,callbackIds:new WeakMap()};
 window.__attr=t;
 const context=()=>({closing:settingsClosing,settings:document.body.classList.contains('settings-view'),
   workspaceTop:workspace.scrollTop});
 const log=(type,data={})=>t.events.push({type,t:performance.now(),...context(),...data});
 const raf=window.requestAnimationFrame.bind(window),cancel=window.cancelAnimationFrame.bind(window);
 const overlay=updateTabScrollOverlay;
 const originalReveal=revealSettingsControl;
 revealSettingsControl=function revealSettingsControl(el){
  log('reveal-call',{handle:t.active?.handle??null,kind:t.active?.kind??null,target:el?.id,connected:el?.isConnected??false,
    mounted:settingsPage.contains(el),ownerFrame:typeof settingsJumpFrame==='undefined'?null:settingsJumpFrame});
  return originalReveal(el);
 };
 const d=Object.getOwnPropertyDescriptor(Element.prototype,'scrollTop');
 if(d?.set&&d.configurable)Object.defineProperty(Element.prototype,'scrollTop',{...d,set(value){
   if(this===workspace&&t.active)log('scroll-write',{handle:t.active.handle,kind:t.active.kind,value});
   return d.set.call(this,value);
 }});
 t.scrollInstrumented=!!d?.set&&d.configurable;
 window.requestAnimationFrame=function(cb){
  const stack=new Error().stack||'';
  const oldKind=stack.includes('revealModalControl')?'modal-scroll':
    stack.includes('revealSettingsControl')?'settings-scroll':
    stack.includes('navigateToSettingsResult')?'settings-reveal':t.active?.legacy??null;
  const body=Function.prototype.toString.call(cb);
  const kind=cb===overlay?'shared-overlay':
    oldKind==='settings-reveal'&&body.includes('revealSettingsControl(el)')?'actual-reveal':
    oldKind==='settings-scroll'?'settings-scroll':
    oldKind==='settings-reveal'?'unclassified-legacy-reveal':'other';
  if(!t.probing&&!oldKind&&!t.active)return raf(cb);
  if(!t.callbackIds.has(cb))t.callbackIds.set(cb,++t.serial);
  const meta={handle:null,callbackId:t.callbackIds.get(cb),name:cb.name,source:body.slice(0,700),
    stack:stack.slice(0,1600),legacy:oldKind,kind,overlayIdentity:cb===overlay};
  const handle=raf(function(now){
    t.pending.delete(handle);
    const prev=t.active;t.active=meta;
    log('deliver',meta);
    try{return cb(now)}finally{t.active=prev}
  });
  meta.handle=handle;t.pending.set(handle,meta);log('schedule',meta);return handle;
 };
 window.cancelAnimationFrame=function(handle){
  if(t.pending.has(handle)){log('cancel',t.pending.get(handle));t.pending.delete(handle)}
  return cancel(handle);
 };
 t.snapshot=label=>{
  const state={label,...context(),pending:[...t.pending.values()].map(x=>({handle:x.handle,kind:x.kind,legacy:x.legacy})),
   jumpFrame:typeof settingsJumpFrame==='undefined'?null:settingsJumpFrame,
   jumpTarget:typeof settingsJumpTarget==='undefined'?null:settingsJumpTarget?.id??null,
   scrollFrame:settingsScrollFrame,highlight:!!document.querySelector('.settings-search-target'),
   oldConnected:t.old?.isConnected??null,oldHighlight:t.old?.classList.contains('settings-search-target')??null};
  log('snapshot',state);return state;
 };
}"""
def settle(page):
    page.wait_for_function("()=>!galleryStageTransition&&!galleryStageFadeInProgress&&!galleryStagePending&&!gallerySettingsOpening&&!settingsClosing",timeout=10000)
    page.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
def run_case(browser,width,motion,kind,repeat):
    context=browser.new_context(viewport={"width":width,"height":700},reduced_motion=motion)
    page=context.new_page();errors=[];page.on("pageerror",lambda e:errors.append(str(e)))
    row={"width":width,"motion":motion,"kind":kind,"repeat":repeat,"status":"completed","errors":errors}
    try:
        page.route("**/*",lambda r:r.fulfill(status=200,content_type="text/html; charset=utf-8",body=source) if r.request.url==origin else r.abort())
        page.goto(origin,wait_until="domcontentloaded");settle(page)
        page.locator("#settings").click()
        page.wait_for_function("()=>document.body.classList.contains('settings-view')",timeout=10000);settle(page)
        page.locator("#search").click();page.locator("#header-search-input").fill("starting volume")
        page.locator('[data-settings-search-key="starting-volume"]').wait_for()
        page.evaluate(instrument)
        assert page.evaluate("window.__attr.scrollInstrumented")
        # Same-task reproduction ensures the close precedes queued RAF delivery.
        # Positive live control uses an ordinary Playwright click and no close.
        if kind=="race":
            page.evaluate("""()=>{const t=window.__attr;t.probing=true;
              document.querySelector('[data-settings-search-key="starting-volume"]').click();
              t.old=document.getElementById('settings-starting-volume-card');
              t.snapshot('after result before close');closeSettings();t.snapshot('after close request');t.probing=false;}""")
            page.wait_for_function("()=>!document.body.classList.contains('settings-view')",timeout=10000);settle(page)
            page.wait_for_timeout(500)
            final=page.evaluate("window.__attr.snapshot('after departure and scroll interval')")
        else:
            page.evaluate("window.__attr.probing=true")
            page.locator('[data-settings-search-key="starting-volume"]').click()
            page.evaluate("()=>{const t=window.__attr;t.old=document.getElementById('settings-starting-volume-card');t.snapshot('live result');t.probing=false}")
            page.wait_for_function("()=>window.__attr.events.some(e=>e.type==='reveal-call')",timeout=3000)
            page.wait_for_function("()=>settingsScrollFrame===null",timeout=3000)
            final=page.evaluate("window.__attr.snapshot('live settled')")
            assert page.evaluate("()=>{const r=document.getElementById('settings-starting-volume-card').getBoundingClientRect(),v=workspace.getBoundingClientRect();return r.bottom>v.top&&r.top<v.bottom}"),"Live target not visible"
        ev=page.evaluate("window.__attr.events")
        row["events"]=ev;row["final"]=final
        scheduled=[e for e in ev if e["type"]=="schedule" and e["legacy"]=="settings-reveal"]
        actual=[e for e in scheduled if e["kind"]=="actual-reveal"]
        shared=[e for e in scheduled if e["kind"]=="shared-overlay"]
        assert len(actual)==1 and len(shared)==1,(actual,shared)
        assert not [e for e in scheduled if e["kind"] not in ("actual-reveal","shared-overlay")],scheduled
        aid=actual[0]["handle"];sid=shared[0]["handle"]
        before=next((e for e in ev if e["type"]=="snapshot" and e["label"]=="after result before close"),None)
        if variant=="candidate" and before:assert before["jumpFrame"]==aid,before
        def count(typ,pred):return sum(e["type"]==typ and pred(e) for e in ev)
        row["findings"]={
          "legacy_closing_deliveries":count("deliver",lambda e:e["legacy"]=="settings-reveal" and e["closing"]),
          "shared_closing_deliveries":count("deliver",lambda e:e["handle"]==sid and e["closing"]),
          "actual_closing_deliveries":count("deliver",lambda e:e["handle"]==aid and e["closing"]),
          "actual_deliveries":count("deliver",lambda e:e["handle"]==aid),
          "actual_cancel":count("cancel",lambda e:e["handle"]==aid),
          "shared_deliveries":count("deliver",lambda e:e["handle"]==sid),
          "reveal_calls":count("reveal-call",lambda e:True),
          "stale_reveal_calls":count("reveal-call",lambda e:e["closing"] or not e["settings"]),
          "stale_scroll_writes":count("scroll-write",lambda e:e["kind"]=="settings-scroll" and (e["closing"] or not e["settings"])),
          "owned_reveal_handle":aid,"shared_overlay_handle":sid,
          "final_jump_frame":final["jumpFrame"],"final_scroll_frame":final["scrollFrame"],
          "final_old_highlight":final["oldHighlight"]}
        if kind=="live":
            assert row["findings"]["actual_deliveries"]==1 and row["findings"]["reveal_calls"]==1 and not row["findings"]["stale_reveal_calls"],row["findings"]
        else:
            assert not final["settings"] and not final["closing"],final
    except Exception:
        row["status"]="harness_error";row["exception"]=traceback.format_exc()
        try:row["events"]=page.evaluate("window.__attr?.events||[]")
        except Exception:pass
    finally:
        context.close();report["cases"].append(row);Path(out).write_text(json.dumps(report,indent=2))
        print("A2.4 ATTR CASE",json.dumps({k:v for k,v in row.items() if k!="events"}),flush=True)
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path=os.environ.get("GALLERY_TEST_CHROMIUM") or None,args=["--no-sandbox"])
    for width in (1440,620):
        for motion in ("no-preference","reduce"):
            for kind in ("race","live"):
                for repeat in range(2):run_case(browser,width,motion,kind,repeat)
    browser.close()
summary={"cases":len(report["cases"]),"harness_errors":sum(r["status"]!="completed" for r in report["cases"]),"page_errors":sum(bool(r["errors"]) for r in report["cases"])}
for kind in ("race","live"):
    rows=[r["findings"] for r in report["cases"] if r["kind"]==kind and r["status"]=="completed"]
    summary[kind]={"completed":len(rows),**{key:sum(r[key] for r in rows) for key in ("legacy_closing_deliveries","shared_closing_deliveries","actual_closing_deliveries","actual_deliveries","actual_cancel","shared_deliveries","reveal_calls","stale_reveal_calls","stale_scroll_writes")}}
report["summary"]=summary;Path(out).write_text(json.dumps(report,indent=2))
print("A2.4 ATTR SUMMARY",variant,mode,json.dumps(summary),flush=True)
assert summary["cases"]==16 and not summary["harness_errors"] and not summary["page_errors"],summary
