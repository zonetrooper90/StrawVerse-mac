#!/usr/bin/env python3
"""A2.5 read-only baseline diagnostic: background operation vs view ownership."""
import hashlib,json,os,sys,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright
mode,motion,out=sys.argv[1:]
assert mode in ("full","lightweight") and motion in ("no-preference","reduce")
root=Path(__file__).resolve().parents[1]
path=root/("Gallery-current.html" if mode=="full" else "Gallery-development.html")
source=path.read_bytes()
size,digest={"full":(6939095,"c52a8c8a8a75c1ae5187fbb577c0ea146a36db9d45aae97320d6638c598be009"),"lightweight":(623405,"54c69064ac691fa3b191a19741390a4efcd7f492f09cf91ca9ccb441671bded3")}[mode]
assert len(source)==size and hashlib.sha256(source).hexdigest()==digest
origin="https://gallery-a25.invalid/"
report={"mode":mode,"motion":motion,"sha256":digest,"cases":[]}
# Install after normal initialization; preserve native timing and callback results.
# Distinguish exact phase delays/call sites from unrelated render/route timers.
instrument=r"""()=>{
 const t={events:[],pending:new Map(),active:null};window.__a25=t;
 const ctx=()=>({token:sourceDemoOpToken,busy:sourceDemoBusy,phase:sourceDemoPhase,
  settings:document.body.classList.contains('settings-view'),closing:settingsClosing,
  section:settingsLastSection,view:state.view,shell:!!settingsPage.querySelector('#sources-shell')});
 const model=()=>JSON.stringify({state:sourceDemoState,busy:sourceDemoBusy,action:sourceDemoBusyAction,
  phase:sourceDemoPhase,feedback:sourcesFeedback,tab:sourcesTab,token:sourceDemoOpToken});
 const dlModel=()=>JSON.stringify({entries:downloadDemo.entries,fullAt:[...downloadDemo.fullAt],
  timers:[...downloadDemo.timers],dismissed:[...downloadDemo.dismissed]});
 const log=(type,data={})=>t.events.push({type,t:performance.now(),...ctx(),...data});
 const set=window.setTimeout.bind(window),clear=window.clearTimeout.bind(window);
 window.setTimeout=function(cb,delay,...args){
  const stack=new Error().stack||'';
  const kind=delay===3000&&stack.includes('simulateNextDownload')?'download-completion':
   [700,850,900,950].includes(delay)&&(stack.includes('beginPreviewUpdate')||stack.includes('advance')||stack.includes('previewSourceAction'))?'source-operation':null;
  if(!kind||typeof cb!=='function')return set(cb,delay,...args);
  let handle;const token=sourceDemoOpToken;
  handle=set(function(...a){
   t.pending.delete(handle);const old=t.active;t.active={kind,handle,token};
   const before=model(),dlBefore=dlModel();
   log('deliver',{kind,handle,scheduledToken:token,stale:kind==='source-operation'&&token!==sourceDemoOpToken});
   try{return cb.apply(this,a)}finally{
    log('return',{kind,handle,scheduledToken:token,stale:kind==='source-operation'&&token!==sourceDemoOpToken,
      modelChanged:before!==model(),downloadChanged:dlBefore!==dlModel()});t.active=old;
   }
  },delay,...args);
  t.pending.set(handle,{kind,token,delay});log('schedule',{kind,handle,scheduledToken:token,delay,stack});return handle;
 };
 window.clearTimeout=function(handle){
  if(t.pending.has(handle)){log('cancel',{handle,...t.pending.get(handle)});t.pending.delete(handle)}
  return clear(handle);
 };
 const renderSources=renderSourcesPreview;
 renderSourcesPreview=function renderSourcesPreview(){
  if(t.active)log('sources-render',{kind:t.active.kind,handle:t.active.handle,scheduledToken:t.active.token});
  return renderSources.apply(this,arguments);
 };
 const refreshDiscover=refreshDiscoverFromSourcePreview;
 refreshDiscoverFromSourcePreview=function refreshDiscoverFromSourcePreview(){
  if(t.active)log('discover-refresh',{kind:t.active.kind,handle:t.active.handle,scheduledToken:t.active.token});
  return refreshDiscover.apply(this,arguments);
 };
 t.snapshot=()=>({ ...ctx(),events:t.events.length,pending:[...t.pending].map(([handle,x])=>({handle,...x})),
  sources:JSON.parse(model()),catalogue:getSourceCataloguePreview().titles.map(x=>x.id),
  discoverCards:tabPages.discover.querySelectorAll('[data-detail]').length,
  downloadTimers:[...downloadDemo.timers],downloadFullAt:[...downloadDemo.fullAt],
  quints:downloadProgress(allAnimeDownloadEntries('demo:quints')),
  legacyPercentNodes:tabPages.downloads.querySelectorAll('.download-group-percent').length,
  currentPercent:tabPages.downloads.querySelector('[data-download-group="demo:quints"] .sf-dl-series-percent')?.textContent??null,
  importEnabled:GALLERY_COLLECTION_TRANSFER_UI_ENABLED,importButtons:tabPages.library.querySelectorAll('#import,#sharetag').length});
}"""
def settled(page):
    page.wait_for_function("()=>!galleryStageTransition&&!galleryStageFadeInProgress&&!galleryStagePending&&!gallerySettingsOpening&&!settingsClosing",timeout=10000)
    page.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
def snap(page,row,label):
    s=page.evaluate("window.__a25.snapshot()");row["trace"].append({"label":label,"snapshot":s});return s
def tab(page,name):
    page.locator(f'.tab[data-view="{name}"]').click()
    page.wait_for_function("v=>state.view===v",arg=name);settled(page)
def sources(page):
    page.locator("#settings").click()
    page.wait_for_function("()=>document.body.classList.contains('settings-view')");settled(page)
    page.locator('[data-settings-section="sources"]').click()
    page.locator('#sources-shell').wait_for()
def close_settings(page):
    page.keyboard.press("Escape")
    page.wait_for_function("()=>!document.body.classList.contains('settings-view')");settled(page)
def update(page,id="anikoto"):
    page.locator(f'[data-source-action="update"][data-source-id="{id}"]').click()
    page.wait_for_function("id=>sourceDemoBusy===id",arg=id)
def outcome(page,health,result):
    page.locator('#sources-installed-region .sources-scenario:not(.sources-catalogue-preview) > summary').click()
    page.locator('#sources-scenario-provider').select_option('anikoto')
    page.locator('#sources-scenario-state').select_option(health)
    page.locator('#sources-scenario-outcome').select_option(result)
    page.locator('[data-source-action="simulate"]').click()
def wait_source(page):
    page.wait_for_function("()=>sourceDemoBusy===null",timeout=10000)
    page.wait_for_timeout(1100)
def run_case(browser,width,kind):
    row={"width":width,"kind":kind,"status":"completed","errors":[],"trace":[]}
    context=browser.new_context(viewport={"width":width,"height":800},reduced_motion=motion)
    context.route("**/*",lambda route:route.fulfill(status=200,content_type="text/html",body=source) if route.request.url==origin else route.abort())
    page=context.new_page();page.on("pageerror",lambda e:row["errors"].append(str(e)))
    try:
        page.goto(origin,wait_until="load");settled(page);page.evaluate(instrument)
        start=snap(page,row,"initialized")
        assert not start["importEnabled"],"Collection transfers intentionally disabled"
        if kind.startswith("download-"):
            tab(page,"downloads")
            page.locator("#demo-next-download").click()
            page.locator("#demo-next-download").click()
            active=snap(page,row,"completion scheduled")
            assert active["quints"]==100 and len(active["downloadTimers"])==1,active
            assert any(x["kind"]=="download-completion" for x in active["pending"]),active
            if kind=="download-reset":
                page.locator("#demo-reset-downloads").click()
                reset=snap(page,row,"reset")
                assert reset["quints"]<100 and not reset["downloadTimers"],reset
            else:
                tab(page,"library");snap(page,row,"departed Downloads")
            page.wait_for_timeout(3300)
            final=snap(page,row,"old completion deadline passed")
            if kind=="download-departure":
                tab(page,"downloads");snap(page,row,"returned to Downloads")
            else:
                assert final["quints"]==reset["quints"],final
        else:
            sources(page);initial=snap(page,row,"Sources mounted")
            if kind=="source-retry-departure":
                outcome(page,"offline","working")
                page.locator('[data-source-action="details"][data-source-id="anikoto"]').click()
                page.locator('[data-source-action="retry"][data-source-id="anikoto"]').click()
                page.wait_for_function("()=>sourceDemoBusy==='anikoto'")
            else:
                if kind=="source-rejected":outcome(page,"healthy","rejected")
                update(page)
            active=snap(page,row,"operation started")
            assert any(x["kind"]=="source-operation" for x in active["pending"]),active
            if kind=="source-reset-restart":
                page.locator('[data-source-action="reset"]').click()
                snap(page,row,"reset invalidated old token")
                update(page);snap(page,row,"new update")
            elif kind=="source-catalogue-replace":
                page.locator('.sources-catalogue-preview > summary').click()
                page.locator('[data-source-action="catalogue-none"]').click()
                snap(page,row,"preset invalidated old token")
                page.locator('[data-source-action="install"][data-source-id="pahe"]').click()
                snap(page,row,"new provider install")
            else:
                close_settings(page);snap(page,row,"Settings departed")
            wait_source(page);final=snap(page,row,"operation settled")
            if not final["settings"]:
                sources(page);snap(page,row,"reopened Sources")
            # Positive controls: state must reach an actual intended result, not
            # merely stop scheduling. Compare exact simulated provider versions.
            anikoto=final["sources"]["state"]["anikoto"];pahe=final["sources"]["state"]["pahe"]
            if kind=="source-rejected":
                assert anikoto["installed"]==initial["sources"]["state"]["anikoto"]["installed"] and anikoto["notice"]["kind"]=="error",final
            elif kind=="source-catalogue-replace":
                assert anikoto["installed"] is None and pahe["installed"]=="7.0.1",final
            elif kind=="source-retry-departure":
                assert anikoto["installed"]==initial["sources"]["state"]["anikoto"]["installed"] and anikoto["health"]=="healthy",final
            else:
                assert anikoto["installed"]=="7.0.0" and anikoto["health"]=="healthy",final
        ev=page.evaluate("window.__a25.events")
        stale=[e for e in ev if e["type"]=="return" and e["stale"]]
        row["events"]=ev
        row["findings"]={"scheduled":sum(e["type"]=="schedule" for e in ev),
          "delivered":sum(e["type"]=="deliver" for e in ev),"canceled":sum(e["type"]=="cancel" for e in ev),
          "stale_deliveries":len(stale),"stale_model_changes":sum(e["modelChanged"] for e in stale),
          "stale_render_calls":sum(e["type"] in ("sources-render","discover-refresh") and e["scheduledToken"]!=e["token"] for e in ev),
          "source_deliveries_outside_settings":sum(e["type"]=="deliver" and e["kind"]=="source-operation" and not e["settings"] for e in ev),
          "discover_refreshes":sum(e["type"]=="discover-refresh" for e in ev),
          "pending_at_settle":len(final["pending"]),"retained_download_handles":len(final["downloadTimers"]),
          "legacy_percent_nodes":final["legacyPercentNodes"],"current_percent":final["currentPercent"]}
    except Exception:
        row["status"]="harness_error";row["exception"]=traceback.format_exc()
        try:row["events"]=page.evaluate("window.__a25?.events||[]")
        except Exception:pass
    finally:
        context.close();report["cases"].append(row);Path(out).write_text(json.dumps(report,indent=2))
        print("A2.5 CASE",json.dumps({k:v for k,v in row.items() if k not in ("events","trace")}),flush=True)
kinds=("download-departure","download-reset","source-update-departure","source-reset-restart","source-catalogue-replace","source-retry-departure","source-rejected")
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path=os.environ.get("GALLERY_TEST_CHROMIUM") or None,args=["--no-sandbox"])
    for width in (1440,620):
        for kind in kinds:run_case(browser,width,kind)
    browser.close()
summary={"cases":len(report["cases"]),"harness_errors":sum(r["status"]!="completed" for r in report["cases"]),"page_errors":sum(bool(r["errors"]) for r in report["cases"]),"by_kind":{}}
for kind in kinds:
    rows=[r["findings"] for r in report["cases"] if r["kind"]==kind and r["status"]=="completed"]
    summary["by_kind"][kind]={"completed":len(rows),**{k:sum(r[k] for r in rows) for k in ("scheduled","delivered","canceled","stale_deliveries","stale_model_changes","stale_render_calls","source_deliveries_outside_settings","discover_refreshes","pending_at_settle","retained_download_handles","legacy_percent_nodes")}}
report["summary"]=summary;Path(out).write_text(json.dumps(report,indent=2))
print("A2.5 SUMMARY",mode,motion,json.dumps(summary),flush=True)
assert summary["cases"]==14 and not summary["harness_errors"] and not summary["page_errors"],summary
