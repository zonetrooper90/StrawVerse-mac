#!/usr/bin/env python3
"""A2.3 read-only native listener counts, transitions and History suspension."""
import hashlib,json,os,sys,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright

mode,motion,out=sys.argv[1:]
assert mode in ("full","lightweight") and motion in ("no-preference","reduce")
path=Path(__file__).resolve().parents[1]/("Gallery-current.html" if mode=="full" else "Gallery-development.html")
source=path.read_bytes()
expected={"full":"8d5f336085058725f49d4fd97cdbc6cddf1a1d9b1afe19f643bdca062c7297f4","lightweight":"fa25eb4f63486966775ff3b3a7817898859e1d7520713ed1304f77f5ebc7aecd"}[mode]
assert hashlib.sha256(source).hexdigest()==expected
origin="https://gallery-a23.invalid/"
report={"mode":mode,"motion":motion,"sha256":expected,"cases":[]}
# Record native events, not an implementation of once-listener semantics.
# Actual registered listeners are counted by Chrome DevTools on the same node.
instrument=r"""()=>{
 window.__a23={events:[],ticks:0,overlay:0};
 for(const type of ['transitionrun','transitionstart','transitioncancel','transitionend']){
  document.addEventListener(type,e=>{
   if(e.target.matches?.('.wh-episodes,.wh-episodes-inner,.wh-inner-overlay')){
    window.__a23.events.push({type,property:e.propertyName,target:e.target.className,id:e.target.closest('[data-wh-row]')?.dataset.whRow,t:performance.now(),settings:document.body.classList.contains('settings-view')});
   }
  },true);
 }
 const tick=whProgressTick,overlay=updateTabScrollOverlay;
 whProgressTick=function(now){window.__a23.ticks++;return tick(now)};
 updateTabScrollOverlay=function(...args){window.__a23.overlay++;return overlay(...args)};
 window.__a23hold=id=>{
  window.__a23panel=document.querySelector('[data-wh-row="'+id+'"] .wh-episodes');
  window.__a23row=window.__a23panel.closest('[data-wh-row]');
 };
 window.__a23snapshot=()=>{
  const panel=window.__a23panel,row=window.__a23row,inner=panel?.querySelector('.wh-episodes-inner'),area=panel?.querySelector('.wh-episode-scroll'),id=row?.dataset.whRow;
  return {open:whOpen,settings:document.body.classList.contains('settings-view'),hidden:screen.hidden,screenDisplay:getComputedStyle(screen).display,
   id,connected:panel?.isConnected??false,sameRow:!!row&&row===screen.querySelector('[data-wh-row="'+id+'"]'),expanded:!!row?.classList.contains('is-expanded'),stateExpanded:whExpanded.has(id),
   aria:row?.querySelector('.wh-summary-hit')?.getAttribute('aria-expanded'),inert:inner?.inert,ariaHidden:inner?.getAttribute('aria-hidden'),
   height:panel?.getBoundingClientRect().height,transition:panel?getComputedStyle(panel).transitionProperty:null,
   animations:panel?.getAnimations().map(a=>({state:a.playState,property:a.transitionProperty}))??[],
   scroll:area?.scrollTop,scrollMax:area?area.scrollHeight-area.clientHeight:0,focus:document.activeElement?.dataset.whExpand??null,
   scrollers:whInnerScrollers.size,frame:!!whProgressFrame,progressEntries:whProgressEntries.size,
   flowing:[...whProgressEntries.values()].filter(e=>e.flow&&e.visible).length,progressMotion:whProgressMotion.matches,
   ticks:window.__a23.ticks,overlay:window.__a23.overlay,events:window.__a23.events.length};
 };
}"""
def settled(page):
    page.wait_for_function("()=>!galleryStageTransition&&!galleryStageFadeInProgress&&!galleryStagePending&&!gallerySettingsOpening&&!settingsClosing",timeout=10000)
    page.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
def wait(page,expr):
    page.wait_for_function(expr,timeout=10000);settled(page)
def panel_settled(page):
    page.wait_for_function("()=>!window.__a23panel.getAnimations().some(a=>a.playState==='running'||a.playState==='pending')",timeout=10000)
    page.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
def listeners(cdp):
    obj=cdp.send("Runtime.evaluate",{"expression":"window.__a23panel","objectGroup":"a23-count"})["result"]
    assert "objectId" in obj,obj
    try:
        all=cdp.send("DOMDebugger.getEventListeners",{"objectId":obj["objectId"]})["listeners"]
        return {typ:sum(x["type"]==typ for x in all) for typ in ("transitionend","transitioncancel")}
    finally:cdp.send("Runtime.releaseObjectGroup",{"objectGroup":"a23-count"})
def snap(page,cdp,row,stage):
    s=page.evaluate("window.__a23snapshot()");s["listeners"]=listeners(cdp)
    row["trace"].append({"stage":stage,"snapshot":s});return s
def check_state(s,opening):
    assert s["expanded"]==s["stateExpanded"]==opening and s["aria"]==str(opening).lower() and s["inert"]== (not opening),s
    assert s["ariaHidden"]==(None if opening else "true"),s
def open_history(page):
    page.locator("#header-watch-history").click();wait(page,"()=>whOpen&&!!document.querySelector('#wh-root')")
def run_case(browser,width,kind):
    context=browser.new_context(viewport={"width":width,"height":850},reduced_motion=motion)
    page=context.new_page();errors=[];page.on("pageerror",lambda e:errors.append(str(e)))
    cdp=context.new_cdp_session(page)
    row={"width":width,"kind":kind,"trace":[],"findings":{},"errors":errors,"status":"completed"}
    try:
        page.route("**/*",lambda r:r.fulfill(status=200,content_type="text/html; charset=utf-8",body=source) if r.request.url==origin else r.abort())
        page.goto(origin,wait_until="domcontentloaded")
        page.evaluate(instrument)
        open_history(page)
        page.evaluate("window.__a23hold('pkm')")
        hit=page.locator('[data-wh-expand="pkm"]')
        start=snap(page,cdp,row,"initial")
        check_state(start,False)
        assert start["listeners"]["transitionend"]==0 and start["sameRow"],start
        if kind=="settled":
            # Real keyboard toggles with each CSS transition allowed to finish.
            for i in range(20):
                hit.press("Enter");panel_settled(page)
                s=snap(page,cdp,row,"toggle "+str(i+1))
                check_state(s,i%2==0)
                assert s["sameRow"] and s["focus"]=="pkm",s
            end=snap(page,cdp,row,"settled end")
            row["findings"]["settled_pending"]=end["listeners"]["transitionend"]
            row["findings"]["settled_peak"]=max(x["snapshot"]["listeners"]["transitionend"] for x in row["trace"])
        elif kind=="rapid":
            # Genuine keyboard activation. No forced clicks or artificial transition events.
            for i in range(100):
                hit.press("Enter")
                if (i+1)%10==0:
                    s=snap(page,cdp,row,"rapid "+str(i+1));check_state(s,False)
            panel_settled(page)
            end=snap(page,cdp,row,"rapid settled")
            row["findings"]["rapid_pending"]=end["listeners"]["transitionend"]
            row["findings"]["rapid_peak"]=max(x["snapshot"]["listeners"]["transitionend"] for x in row["trace"])
            # Controlled same-task burst: deliberately no intervening layout.
            # Explicitly synthetic activation, not a natural timing claim.
            page.evaluate("""()=>{const b=window.__a23row.querySelector('.wh-summary-hit');for(let i=0;i<100;i++)b.click()}""")
            panel_settled(page)
            burst=snap(page,cdp,row,"same task burst settled");check_state(burst,False)
            row["findings"]["burst_pending"]=burst["listeners"]["transitionend"]
        elif kind=="motion-change":
            # Start in the requested mode; test cancellation in both directions.
            hit.press("Enter");panel_settled(page)
            s=snap(page,cdp,row,"first open");check_state(s,True)
            page.emulate_media(reduced_motion="no-preference")
            page.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
            hit.press("Enter")
            page.wait_for_function("()=>window.__a23panel.getAnimations().some(a=>a.playState==='running')",timeout=5000)
            running=snap(page,cdp,row,"normal closing active")
            page.emulate_media(reduced_motion="reduce");panel_settled(page)
            canceled=snap(page,cdp,row,"motion changed to reduce");check_state(canceled,False)
            row["findings"]["pending_after_cancel"]=canceled["listeners"]["transitionend"]
            for i in range(10):hit.press("Enter")
            panel_settled(page)
            reduced=snap(page,cdp,row,"ten reduced toggles");check_state(reduced,False)
            row["findings"]["pending_reduced"]=reduced["listeners"]["transitionend"]
            page.emulate_media(reduced_motion="no-preference")
            page.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
            hit.press("Enter");panel_settled(page)
            restored=snap(page,cdp,row,"normal motion restored");check_state(restored,True)
            row["findings"]["pending_after_restore"]=restored["listeners"]["transitionend"]
            row["findings"]["overlay_refreshes_on_restore"]=restored["overlay"]-reduced["overlay"]
        elif kind=="settings":
            hit.press("Enter");panel_settled(page)
            page.evaluate("()=>{const a=window.__a23panel.querySelector('.wh-episode-scroll');a.scrollTop=Math.min(220,a.scrollHeight-a.clientHeight)}")
            # Bring a partial-progress row into view; observe ticks over equal windows.
            page.evaluate("()=>window.__a23row.scrollIntoView({block:'center'})")
            page.wait_for_timeout(350)
            before=snap(page,cdp,row,"visible before sample")
            page.wait_for_timeout(600)
            visible=snap(page,cdp,row,"visible after sample")
            row["findings"]["visible_ticks"]=visible["ticks"]-before["ticks"]
            row["findings"]["visible_flowing"]=visible["flowing"]
            page.locator("#settings").click();wait(page,"()=>document.body.classList.contains('settings-view')")
            page.wait_for_timeout(350)
            hidden=snap(page,cdp,row,"settings before sample")
            page.wait_for_timeout(600)
            hidden_late=snap(page,cdp,row,"settings after sample")
            row["findings"]["settings_ticks"]=hidden_late["ticks"]-hidden["ticks"]
            row["findings"]["settings_flowing"]=hidden_late["flowing"]
            row["findings"]["settings_frame_pending"]=hidden_late["frame"]
            page.locator("#settings-back").click();wait(page,"()=>!document.body.classList.contains('settings-view')")
            panel_settled(page)
            returned=snap(page,cdp,row,"settings returned");check_state(returned,True)
            assert returned["sameRow"] and abs(returned["scroll"]-visible["scroll"])<=1,(visible,returned)
            row["findings"]["settings_same_row"]=returned["sameRow"]
            row["findings"]["settings_scroll_delta"]=returned["scroll"]-visible["scroll"]
        # Check both destruction by rerender and true exit. The diagnostic
        # retains old panel explicitly so CDP can inspect its listeners.
        pre=snap(page,cdp,row,"before sort")
        page.locator('[data-wh-sort]').click();settled(page)
        after=snap(page,cdp,row,"old panel after sort")
        assert not after["connected"] and not after["sameRow"],after
        row["findings"]["old_listener_count_after_sort"]=after["listeners"]["transitionend"]
        page.evaluate("window.__a23hold('pkm')")
        fresh=snap(page,cdp,row,"new panel")
        assert fresh["sameRow"] and fresh["listeners"]["transitionend"]==0,fresh
        # Leave with an outstanding listener under reduced motion, without
        # synthesizing any transition completion.
        page.emulate_media(reduced_motion="reduce")
        page.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
        page.locator('[data-wh-expand="pkm"]').press("Enter");panel_settled(page)
        exiting=snap(page,cdp,row,"before exit")
        page.locator('#wh-root [data-wh-exit]').click();wait(page,"()=>!whOpen&&screen.hidden")
        after_exit=snap(page,cdp,row,"after exit")
        page.wait_for_timeout(250)
        late=snap(page,cdp,row,"after exit late")
        assert not late["open"] and late["scrollers"]==0 and not late["frame"] and late["progressEntries"]==0,late
        row["findings"]["listener_count_after_exit"]=late["listeners"]["transitionend"]
        row["findings"]["post_exit_ticks"]=late["ticks"]-after_exit["ticks"]
        row["events"]=page.evaluate("window.__a23.events")
    except Exception:
        row["status"]="harness_error";row["exception"]=traceback.format_exc()
        try:row["events"]=page.evaluate("window.__a23?.events||[]")
        except Exception:pass
    finally:
        cdp.detach();context.close()
        report["cases"].append(row);Path(out).write_text(json.dumps(report,indent=2))
        print("A2.3 CASE",json.dumps({k:v for k,v in row.items() if k not in ("trace","events")}),flush=True)
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path=os.environ.get("GALLERY_TEST_CHROMIUM") or None,args=["--no-sandbox"])
    for width in (1440,620):
        for kind in ("settled","rapid","motion-change","settings"):
            run_case(browser,width,kind)
    browser.close()
summary={"cases":len(report["cases"]),"harness_errors":sum(r["status"]!="completed" for r in report["cases"]),"page_errors":sum(bool(r["errors"]) for r in report["cases"])}
report["summary"]=summary;Path(out).write_text(json.dumps(report,indent=2))
print("A2.3 SUMMARY",mode,motion,json.dumps(summary),flush=True)
assert summary["cases"]==8 and not summary["harness_errors"] and not summary["page_errors"],summary
