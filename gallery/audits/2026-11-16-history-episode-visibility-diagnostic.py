#!/usr/bin/env python3
"""Read-only diagnostic of the exact accepted History regression sequence."""
import hashlib,json,sys,traceback
from pathlib import Path
mode,variant,out=sys.argv[1:]
assert mode in ("full","lightweight") and variant in ("original","settled")
root=Path(__file__).resolve().parents[1]
test=root/"tests/test_history_row_maintenance.py"
raw=test.read_bytes()
assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()=="d91267a7ad252515bdf3f905ad21cc80d86b8671"
html=root/("Gallery-current.html" if mode=="full" else "Gallery-development.html")
expected={"full":"9e5366a1e54a7719eeff8c7127298bf9371808a2c2749a704fcacc2634dbc37a","lightweight":"fb2c515b0ef9efc6e65b870b726c602cd48659872a4bc467504187a95e465dbf"}[mode]
assert hashlib.sha256(html.read_bytes()).hexdigest()==expected
lines=raw.decode("utf-8").splitlines(keepends=True)
assert lines[108].strip()=="page=browser.new_page(viewport={'width':1200,'height':850})"
assert lines[243].strip().startswith("assert page.locator(")
# Exact main scenario through the failed click and all episode-status assertions.
# Earlier independent width/search cases and later wheel tests are outside this focused audit.
source="".join(lines[:11]+lines[108:244])
def replace(old,new):
    global source
    assert source.count(old)==1,old
    source=source.replace(old,new)
replace("    errors=[]\n","    _diag_setup(page)\n    errors=[]\n")
entry="    page.locator('#wh-view-history').click()\n    page.wait_for_timeout(400)\n    history=page.locator('.wh-season').nth(1)\n    history.locator('[data-wh-expand]').click()\n    page.wait_for_timeout(330)\n"
wait="    page.wait_for_function(\"()=>whOpen&&!galleryStageFadeInProgress&&!galleryStageTransition&&!galleryStagePending\",timeout=8000)\n" if variant=="settled" else ""
replace(entry,"    _diag_mark(page,'before-history-entry')\n    page.locator('#wh-view-history').click()\n    page.wait_for_timeout(400)\n"+wait+"    history=page.locator('.wh-season').nth(1)\n    _diag_mark(page,'before-expand')\n    history.locator('[data-wh-expand]').click()\n    page.wait_for_timeout(330)\n    _diag_mark(page,'after-expand')\n")
replace("    original_seconds=page.evaluate(","    _diag_mark(page,'before-episode-click')\n    original_seconds=page.evaluate(")
replace("    episode76.click()\n    assert episode76.get_attribute('aria-pressed')=='mixed' and","    episode76.click()\n    _diag_mark(page,'after-episode-click')\n    assert episode76.get_attribute('aria-pressed')=='mixed' and")
# Keep the complete original preceding route, wheel and status assertions.
# Capture real DOM clicks before Gallery's app-level input gate; no forced clicks,
# no app-state mutations and no retries within a case.
snapshot="""()=>{const row=document.querySelector('[data-wh-row="pkm"]'),inner=row?.querySelector('.wh-episodes-inner'),ep=row?.querySelector('[data-wh-episode="pkm:76"]'),list=row?.querySelector('.wh-episode-scroll');
 const box=e=>e?{height:e.getBoundingClientRect().height,visibility:getComputedStyle(e).visibility,display:getComputedStyle(e).display,scroll:e.scrollTop}:null;
 return {time:performance.now(),view:state.view,whOpen,fade:galleryStageFadeInProgress,mutating:galleryStageMutating,busy:document.querySelector('.app').getAttribute('aria-busy'),expanded:[...whExpanded],rowClass:row?.className,aria:row?.querySelector('.wh-summary-hit')?.getAttribute('aria-expanded'),inert:inner?.inert,inner:box(inner),list:box(list),episode:box(ep),outer:workspace.scrollTop,events:window.__diagEvents||[]};}"""
results=[]
for rate in (1,4):
 for repeat in range(6):
    trace=[]
    def setup(page):
        if rate!=1:
            page.context.new_cdp_session(page).send("Emulation.setCPUThrottlingRate",{"rate":rate})
        page.on("pageerror",lambda err:trace.append({"pageerror":str(err)}))
        page.add_init_script("""()=>{}""")
        # set_content retains this fresh document; install observer after loading below.
    def mark(page,label):
        if label=="before-history-entry":
            page.evaluate("""()=>{window.__diagEvents=[];document.addEventListener('click',e=>{
              const b=e.target.closest('button');if(!b)return;
              window.__diagEvents.push({time:performance.now(),id:b.id,expand:b.dataset.whExpand||null,episode:b.dataset.whEpisode||null,fade:galleryStageFadeInProgress,mutating:galleryStageMutating,open:whOpen,trusted:e.isTrusted});
            },true);}""")
        trace.append({"stage":label,"snapshot":page.evaluate(snapshot)})
    # Execute in a function-like scope with the Playwright context managed by the
    # original with-block. Capture failure while browser is still alive.
    body=source.splitlines(keepends=True)
    assert body[9].startswith("with sync_playwright()") and "browser=pw.chromium" in body[10]
    instrumented="".join(body[:11])+"    try:\n"+"".join("    "+line if line.strip() else line for line in body[11:])+"    except Exception as exc:\n        _diag_failure(exc,locals().get('page'))\n    finally:\n        browser.close()\n"
    outcome={"mode":mode,"variant":variant,"cpu":rate,"repeat":repeat,"trace":trace,"passed":True}
    def failure(exc,page):
        outcome["passed"]=False
        outcome["error"]=str(exc)
        outcome["traceback"]=traceback.format_exc()
        if page:
            try: mark(page,"failure")
            except Exception as snapshot_error: trace.append({"snapshot_error":str(snapshot_error)})
    oldargv=sys.argv
    try:
        sys.argv=[str(test),str(html)]
        exec(compile(instrumented,str(test),"exec"),{"__name__":"__main__","__file__":str(test),"_diag_setup":setup,"_diag_mark":mark,"_diag_failure":failure})
    finally:
        sys.argv=oldargv
    results.append(outcome)
    print("CASE",json.dumps(outcome,ensure_ascii=False),flush=True)
    Path(out).write_text(json.dumps(results,indent=2,ensure_ascii=False))
print("SUMMARY",json.dumps({"mode":mode,"variant":variant,"cases":len(results),"passes":sum(r["passed"] for r in results),"failures":sum(not r["passed"] for r in results)}),flush=True)
assert len(results)==12
