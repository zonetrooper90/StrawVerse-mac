#!/usr/bin/env python3
"""Read-only A2.2: observe real ResizeObserver ownership without changing app HTML."""
import hashlib,json,os,sys,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright

mode,motion,out=sys.argv[1:]
assert mode in ("full","lightweight") and motion in ("no-preference","reduce")
path=Path(__file__).resolve().parents[1]/("Gallery-current.html" if mode=="full" else "Gallery-development.html")
source=path.read_bytes()
expected={"full":"0fcf22fa2a3d391203f5dd1f3e5cce16c63c605798570d61b2904607b76e6173","lightweight":"de9deb1b16de50fa7966c6dfeb4baec2368f448c95b6768d27ef2e336576be3b"}[mode]
assert hashlib.sha256(source).hexdigest()==expected
origin="https://gallery-a22.invalid/"
# Preserve native observer delivery. Weak references avoid keeping detached rail
# targets alive solely because the ledger is observing them. Record registration
# until explicit unobserve/disconnect; this is NOT a heap-size or GC measurement.
instrument=r"""(()=>{
 const Native=window.ResizeObserver,ids=new WeakMap(),owners=new WeakMap(),records=new Map();let next=0,nodeNext=0;
 const nodeId=e=>{if(!ids.has(e))ids.set(e,++nodeNext);return ids.get(e)};
 const isRail=e=>e?.id==='inline-installment-rail'||e?.classList?.contains('inline-installment-card');
 const route=()=>({settings:document.body?.classList.contains('settings-view')??false,hidden:document.getElementById('screen')?.hidden??null,detail:typeof state!=='undefined'?state.detailId:null,player:typeof state!=='undefined'?!!state.playback:false,history:typeof whOpen!=='undefined'?whOpen:false});
 class Traced extends Native {
  constructor(callback){
   const r={id:++next,rail:false,targets:new Map(),observe:0,disconnect:0,calls:0,departedCalls:0,suspendedCalls:0,foreignCalls:0,events:[]};
   super((entries,observer)=>{
    if(r.rail){
     const current=document.querySelector('#screen #inline-installment-rail'),s=route();
     const foreign=entries.some(e=>!current||(e.target!==current&&!current.contains(e.target)));
     r.calls++;if(s.settings)r.suspendedCalls++;else if(!s.detail||s.player||s.history||s.hidden)r.departedCalls++;
     if(foreign)r.foreignCalls++;
     r.events.push({t:performance.now(),route:s,foreign,entries:entries.map(e=>({id:nodeId(e.target),connected:e.target.isConnected,width:e.contentRect.width,height:e.contentRect.height}))});
    }
    callback(entries,observer);
   });
   owners.set(this,r);
  }
  observe(target,options){const result=super.observe(target,options),r=owners.get(this);
   if(isRail(target)){r.rail=true;r.observe++;r.targets.set(nodeId(target),new WeakRef(target));records.set(r.id,r)}
   return result;
  }
  unobserve(target){const result=super.unobserve(target);owners.get(this).targets.delete(nodeId(target));return result}
  disconnect(){const result=super.disconnect(),r=owners.get(this);r.disconnect++;r.targets.clear();return result}
 }
 window.ResizeObserver=Traced;
 window.__a22snapshot=()=>{
  const rail=document.querySelector('#screen #inline-installment-rail'),current=typeof activeInstallmentRailObserver!=='undefined'?activeInstallmentRailObserver:null;
  const rows=[...records.values()].map(r=>({id:r.id,registered:r.targets.size,connected:[...r.targets.values()].filter(x=>x.deref()?.isConnected).length,detached:[...r.targets.values()].filter(x=>x.deref()&&!x.deref().isConnected).length,collected:[...r.targets.values()].filter(x=>!x.deref()).length,observe:r.observe,disconnect:r.disconnect,calls:r.calls,departedCalls:r.departedCalls,suspendedCalls:r.suspendedCalls,foreignCalls:r.foreignCalls}));
  const vp=rail?.closest('.inline-release-viewport');
  return {route:route(),owner:current?owners.get(current)?.id??null:null,rail:rail?{id:nodeId(rail),cards:rail.children.length,x:rail.scrollLeft,max:rail.scrollWidth-rail.clientWidth,visible:!!rail.getClientRects().length,selected:rail.querySelector('[aria-current="true"]')?.dataset.inlineInstallment??null,canLeft:vp.classList.contains('can-left'),canRight:vp.classList.contains('can-right')}:null,rows,active:rows.filter(r=>r.registered>0).length,registered:rows.reduce((a,r)=>a+r.registered,0)};
 };
 window.__a22events=()=>[...records.values()].map(r=>({id:r.id,events:r.events}));
})()"""
report={"mode":mode,"motion":motion,"sha256":expected,"cases":[]}
def settled(page):
    page.wait_for_function("()=>!galleryStageTransition&&!galleryStageFadeInProgress&&!galleryStagePending&&!gallerySettingsOpening&&!settingsClosing",timeout=10000)
    page.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
def wait(page,expr):
    page.wait_for_function(expr,timeout=10000);settled(page)
def take(page,row,stage):
    s=page.evaluate("window.__a22snapshot()");row["trace"].append({"stage":stage,"snapshot":s});return s
def open_detail(page,kind):
    if kind=="player":
        if page.evaluate("state.view")!="discover":
            page.locator("#nav-discover").click();settled(page)
        page.locator('[data-tab-page="discover"] [data-detail="demo:01"]').first.click()
        wait(page,"()=>state.detailId==='demo:01'&&!state.playback")
    else:
        if page.evaluate("state.view")!="library":
            page.locator("#nav-library").click();settled(page)
        page.locator('[data-tab-page="library"] [data-detail="demo:long"]').first.click()
        wait(page,"()=>state.detailId==='demo:long'&&!state.playback")
    page.locator("#inline-installment-rail").wait_for(state="visible")
    page.wait_for_function("()=>window.__a22snapshot().rows.some(r=>r.id===window.__a22snapshot().owner&&r.calls>0)")
def go_back(page):
    page.locator("#detail-back").click();wait(page,"()=>!state.detailId&&!state.playback&&!whOpen")
def finding(row,name,value):
    row["findings"][name]=bool(value)
def run_case(browser,width,kind):
    context=browser.new_context(viewport={"width":width,"height":850},reduced_motion=motion)
    page=context.new_page();errors=[];page.on("pageerror",lambda e:errors.append(str(e)))
    row={"width":width,"kind":kind,"trace":[],"findings":{},"errors":errors,"status":"completed"}
    try:
        page.add_init_script(instrument)
        page.route("**/*",lambda r:r.fulfill(status=200,content_type="text/html; charset=utf-8",body=source) if r.request.url==origin else r.abort())
        page.goto(origin,wait_until="domcontentloaded")
        for cycle in range(2):
            prefix=str(cycle)+":"
            open_detail(page,kind)
            before=take(page,row,prefix+"mounted")
            assert before["owner"] is not None and before["rail"]["visible"] and before["registered"]>=before["rail"]["cards"]+1,before
            # Exercise actual arrow when possible; select a visible different card
            # with a genuine click. Check preserved DOM identity, not a synthetic route.
            if kind!="player":
                page.locator('[data-inline-scroll="1"]').click()
                page.wait_for_function("()=>{const r=document.getElementById('inline-installment-rail');return r.scrollLeft>5}",timeout=10000)
                page.wait_for_timeout(450)
                page.evaluate("()=>{const r=document.getElementById('inline-installment-rail');r.style.scrollSnapType='none';r.scrollTo({left:Math.min(180,r.scrollWidth-r.clientWidth),behavior:'instant'})}")
                settled(page)
            before=take(page,row,prefix+"before departure")
            if kind=="primary" or kind=="no-rail":go_back(page)
            elif kind=="search":
                page.locator("#search").click();wait(page,"()=>searchOpen&&!state.detailId")
            elif kind=="history":
                page.locator("#header-watch-history").click();wait(page,"()=>whOpen&&!state.detailId")
            elif kind=="player":
                page.locator('.detail-actions [data-episode-action="watch"]').first.click();wait(page,"()=>!!state.playback")
            elif kind=="settings":
                page.locator("#settings").click();wait(page,"()=>document.body.classList.contains('settings-view')")
            departed=take(page,row,prefix+"departed")
            page.set_viewport_size({"width":width-70,"height":850});settled(page);page.wait_for_timeout(200)
            resized=take(page,row,prefix+"away resized")
            page.set_viewport_size({"width":width,"height":850});settled(page);page.wait_for_timeout(200)
            away=take(page,row,prefix+"away restored width")
            old=next(r for r in away["rows"] if r["id"]==before["owner"])
            oldbefore=next(r for r in before["rows"] if r["id"]==before["owner"])
            finding(row,prefix+"departed observer retained",kind!="settings" and old["registered"]>0)
            finding(row,prefix+"departed callback delivered",kind!="settings" and old["departedCalls"]>oldbefore["departedCalls"])
            finding(row,prefix+"detached registered target",kind!="settings" and old["detached"]>0)
            finding(row,prefix+"settings retained same owner",kind=="settings" and away["owner"]==before["owner"])
            if kind=="search":
                page.locator("#header-search-input").fill("Solo Leveling")
                page.locator("#header-search-input").press("Escape");wait(page,"()=>!searchOpen&&state.detailId==='demo:long'")
            elif kind=="history":
                page.locator('#wh-root [data-wh-exit]').click();wait(page,"()=>!whOpen&&state.detailId==='demo:long'")
            elif kind=="player":
                page.locator("#back-from-playback").click();wait(page,"()=>!state.playback&&state.detailId==='demo:01'")
            elif kind=="settings":
                page.locator("#settings-back").click();wait(page,"()=>!document.body.classList.contains('settings-view')")
            elif kind=="no-rail":
                page.locator("#nav-discover").click();settled(page)
                page.locator('[data-tab-page="discover"] [data-detail="demo:04"]').first.click()
                wait(page,"()=>state.detailId==='demo:04'")
                no_rail=take(page,row,prefix+"single installment")
                assert no_rail["rail"] is None,no_rail
                finding(row,prefix+"rail-free detail has no registrations",no_rail["registered"]==0)
                go_back(page)
            if kind in ("search","history","player","settings"):
                page.locator("#inline-installment-rail").wait_for(state="visible")
                returned=take(page,row,prefix+"returned")
                assert returned["rail"]["visible"] and returned["owner"] is not None,returned
                finding(row,prefix+"return same rail",returned["rail"]["id"]==before["rail"]["id"])
                finding(row,prefix+"return same owner",returned["owner"]==before["owner"])
                row[prefix+"return scroll delta"]=returned["rail"]["x"]-before["rail"]["x"]
                row[prefix+"selected preserved"]=returned["rail"]["selected"]==before["rail"]["selected"]
                go_back(page)
            end=take(page,row,prefix+"cycle end")
            finding(row,prefix+"multiple active observers",end["active"]>1)
        row["events"]=page.evaluate("window.__a22events()")
    except Exception:
        row["status"]="harness_error";row["exception"]=traceback.format_exc()
        try:row["events"]=page.evaluate("window.__a22events()")
        except Exception:pass
    finally:
        context.close()
        report["cases"].append(row)
        Path(out).write_text(json.dumps(report,indent=2))
        print("A2.2 CASE",json.dumps({k:v for k,v in row.items() if k not in ("trace","events")}),flush=True)
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path=os.environ.get("GALLERY_TEST_CHROMIUM") or None,args=["--no-sandbox"])
    for width in (1440,620):
        for kind in ("primary","search","history","player","settings","no-rail"):
            run_case(browser,width,kind)
    browser.close()
counts={}
for row in report["cases"]:
    for key,value in row["findings"].items():
        label=key.split(":",1)[1]
        entry=counts.setdefault(label,{"true":0,"observations":0})
        entry["true"]+=int(value);entry["observations"]+=1
summary={"cases":len(report["cases"]),"harness_errors":sum(r["status"]!="completed" for r in report["cases"]),"page_errors":sum(bool(r["errors"]) for r in report["cases"]),"findings":counts}
report["summary"]=summary;Path(out).write_text(json.dumps(report,indent=2))
print("A2.2 SUMMARY",mode,motion,json.dumps(summary),flush=True)
assert summary["cases"]==12 and not summary["harness_errors"] and not summary["page_errors"],summary
