#!/usr/bin/env python3
"""Read-only, exact-build rail and A1 reload investigation; no application edits."""
import copy,hashlib,json,os,sys,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright
variant,mode,root,out=sys.argv[1:]
root=Path(root).resolve();out=Path(out)
HTML=root/"gallery"/("Gallery-current.html" if mode=="full" else "Gallery-development.html")
digests={
 "accepted":("dd93f30c2bc170d08f43ceaa459205bd4b157e8d40d2df8f29e0133de10134d3","76ede7481d40dfc3b0e674c4808de45df468818792e5d4dd937ae205cb953da3"),
 "original":("a47793b23c95ce24780a7daf0b42a7a4d36b98693e440ac62209f93b691d9558","65a9ac42fb20395ad4bc2108c9f82f51e867a2bfdee2668a5478d375caa7ad83"),
 "retry":("c6a0cd867be620287cc21cc9ce8d2060635ae0be97f024c2fcd7b40d1a6fa2dd","772f46684ccdd99ddbd4196eefdac73f942c4ad63d03bc64316e35275ec6b0e1")}
digest=hashlib.sha256(HTML.read_bytes()).hexdigest()
assert digest==digests[variant][mode=="lightweight"],(variant,mode,digest)
original_a1=root/"gallery/audits/2026-11-15-a1-watch-history-resilience-regression.py"
original_rail=root/"gallery/audits/2026-11-15-anime-detail-search-return-rail-retry-regression.py"
def blob(p):
    b=p.read_bytes();return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
assert blob(original_a1)=="6d988f3e04e7637bae5e3f7649e02087004c88d4"
# Reuse unmodified synthetic fixture and test helpers, not the original main loop.
ns={}
saved_argv=sys.argv
sys.argv=[str(original_a1),str(HTML)]
exec(compile(original_a1.read_text().split("with sync_playwright() as pw:")[0],str(original_a1),"exec"),ns)
sys.argv=saved_argv
report={"variant":variant,"mode":mode,"sha256":digest,"rail":[],"a1":[]}
source=HTML.read_text(encoding="utf-8")
def emit(key,row):
    report[key].append(row)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2))
    small={k:v for k,v in row.items() if k not in ("frames","storage_before","storage_after","expected","actual","backup_before","backup_after")}
    print(key,json.dumps(small,ensure_ascii=False),flush=True)
def settle(page):
    page.wait_for_function("()=>!galleryStageTransition&&!galleryStageFadeInProgress&&!galleryStagePending",timeout=8000)
def snapshot(page):
    return page.evaluate("""()=>{
      const r=screen.querySelector('#inline-installment-rail'), c=r?.querySelector('[aria-current="true"]');
      return {t:performance.now(),x:r?.scrollLeft??null,snap:r?getComputedStyle(r).scrollSnapType:null,
        inlineSnap:r?.style.scrollSnapType??null,scroll:workspace.scrollTop,detail:state.detailId,
        season:state.detailSeason,search:searchOpen,visible:!screen.hidden,
        saved:typeof searchDetailReturn!=='undefined'?searchDetailReturn?.railScroll??null:null,
        card:c?.dataset.inlineInstallment??null,railWidth:r?.clientWidth??null,railMax:r?r.scrollWidth-r.clientWidth:null};
    }""")
TRACE="""()=>{
 const traces=[];window.__railTrace=traces;
 const add=(type)=>{
  const r=screen.querySelector('#inline-installment-rail');
  traces.push({type,t:performance.now(),x:r?.scrollLeft??null,visible:!screen.hidden,search:searchOpen,
   detail:state.detailId,scroll:workspace.scrollTop,snap:r?getComputedStyle(r).scrollSnapType:null,
   saved:typeof searchDetailReturn!=='undefined'?searchDetailReturn?.railScroll??null:null});
 };
 for(const type of ['pointerdown','click','keydown']){
  document.addEventListener(type,e=>{if(e.target.closest?.('#search,#header-search-input,#header-search-close'))add(type+':'+(e.key||e.target.id));},true);
 }
 document.addEventListener('scroll',e=>{if(e.target.id==='inline-installment-rail')add('rail-scroll');},true);
 document.addEventListener('scrollend',e=>{if(e.target.id==='inline-installment-rail')add('rail-scrollend');},true);
 let start=performance.now();
 function step(){add('frame');if(performance.now()-start<8000)requestAnimationFrame(step);}
 requestAnimationFrame(step);
}"""
def rail_trial(browser,width,motion,scenario,repeat):
    page=browser.new_page(viewport={"width":width,"height":850},reduced_motion=motion)
    errors=[];page.on("pageerror",lambda e:errors.append(str(e)))
    row={"width":width,"motion":motion,"scenario":scenario,"repeat":repeat}
    try:
        page.set_content(source,wait_until="domcontentloaded")
        page.locator("#nav-library").click();page.wait_for_timeout(500)
        page.locator('.tab-page[data-tab-page="library"] [data-detail="demo:long"]').first.click();settle(page)
        assert page.evaluate("state.detailId")=="demo:long"
        page.evaluate(TRACE)
        page.locator('[data-inline-installment="long-s10"]').evaluate("e=>e.click()")
        if scenario=="early":page.wait_for_timeout(150)
        elif scenario=="original500":page.wait_for_timeout(500)
        elif scenario=="async_poll":
            page.wait_for_timeout(500)
            # Reproduce the exact previous test's async predicate (compare against frames).
            handle=page.wait_for_function("""async()=>{
             const rail=screen.querySelector('#inline-installment-rail'),x=rail.scrollLeft;
             for(let i=0;i<8;i++){await new Promise(r=>requestAnimationFrame(r));if(Math.abs(rail.scrollLeft-x)>.5)return false;}
             return true;
            }""",timeout=5000)
            row["poll_result"]=handle.json_value()
        elif scenario=="settled":
            row["stable"]=page.evaluate("""async()=>{
             const r=screen.querySelector('#inline-installment-rail');let x=r.scrollLeft,stable=0,start=performance.now();
             while(performance.now()-start<4000){await new Promise(a=>requestAnimationFrame(a));
              const next=r.scrollLeft;stable=Math.abs(next-x)<.25?stable+1:0;x=next;
              if(stable>=16)return {ok:true,x,ms:performance.now()-start};}
             return {ok:false,x,ms:performance.now()-start};
            }""")
        elif scenario=="instant":
            page.evaluate("""()=>{const r=screen.querySelector('#inline-installment-rail');
             r.style.scrollSnapType='none';void r.offsetWidth;
             r.scrollTo({left:Math.min(1237,r.scrollWidth-r.clientWidth),behavior:'instant'});}""")
            page.wait_for_timeout(300)
        page.evaluate("()=>workspace.scrollTo({top:Math.min(230,workspace.scrollHeight-workspace.clientHeight),behavior:'instant'})")
        before=snapshot(page);row["before"]=before
        page.locator("#search").click()
        page.wait_for_function("()=>searchOpen&&!state.detailId&&!galleryStageFadeInProgress",timeout=8000)
        row["opened"]=snapshot(page)
        page.locator("#header-search-input").fill("Solo Leveling")
        page.locator("#header-search-input").press("Escape");settle(page)
        page.wait_for_timeout(500)
        row["after"]=snapshot(page)
        row["capture_delta"]=None if row["opened"]["saved"] is None else row["opened"]["saved"]-before["x"]
        row["restore_delta"]=None if row["opened"]["saved"] is None or not row["after"]["detail"] else row["after"]["x"]-row["opened"]["saved"]
        row["frames"]=page.evaluate("window.__railTrace")
    except Exception as e:
        row["exception"]=str(e);row["traceback"]=traceback.format_exc()
        try:row["frames"]=page.evaluate("window.__railTrace||[]")
        except Exception:pass
    finally:
        row["page_errors"]=errors;emit("rail",row);page.close()
def storage(page):
    return page.evaluate("""([k,b])=>({primary:window.__a1read(k),backup:window.__a1read(b),
      initialized:sessionStorage.getItem('__a1_initialized'),counts:window.__a1,
      needsRecovery:whNeedsRecovery,loadedRaw:whLoadedRaw,readable:whStorageReadable})""",[ns["KEY"],ns["BACKUP"]])
def a1_trial(browser,width,i,a,b):
    raw=ns["dumped"]([None,a,b]);ctx=None;page=None;errors=[]
    row={"width":width,"repeat":i}
    try:
        ctx,page,errors=ns["context_for"](browser,raw,width)
        assert ns["records"](page)==[a,b]
        ns["history"](page);ns["toggle"](page,a["id"])
        edited=ns["records"](page);row["expected"]=edited
        before=storage(page);row["storage_before"]=before
        row["save_match"]=json.loads(before["primary"])==edited
        row["backup_match_before"]=before["backup"]==raw
        page.reload(wait_until="load")
        row["actual"]=ns["records"](page);after=storage(page);row["storage_after"]=after
        row["reload_match"]=row["actual"]==edited
        row["backup_match_after"]=after["backup"]==raw
        row["primary_match_after"]=after["primary"]==before["primary"]
        row["reload_record_count"]=len(row["actual"])
        row["reload_episode_status"]=row["actual"][0]["episodes"][0].get("manualStatus") if row["actual"] else None
        if not row["reload_match"]:
            print("A1 mismatch evidence",json.dumps(row,ensure_ascii=False),flush=True)
            page.wait_for_timeout(300)
            row["late_reload_match"]=ns["records"](page)==edited
    except Exception as e:
        row["exception"]=str(e);row["traceback"]=traceback.format_exc()
    finally:
        row["page_errors"]=errors;emit("a1",row)
        if ctx:ctx.close()
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True)
    for width in (1440,620):
      for motion in ("no-preference","reduce"):
       for scenario in ("early","original500","async_poll","settled","instant"):
        for repeat in range(2):
         rail_trial(browser,width,motion,scenario,repeat)
    if variant!="original":
      clean=browser.new_page();clean.goto(HTML.as_uri(),wait_until="load")
      seed=clean.evaluate("JSON.parse(JSON.stringify(whSeed))");clean.close()
      a=copy.deepcopy(seed[0]);a["id"]="audit-a";a["episodes"]=a["episodes"][:2];a["latestEpisode"]=a["episodes"][0]["n"]
      a["compatibleExtra"]={"retain":True};a["episodes"][0]["compatibleExtra"]="retain"
      b=copy.deepcopy(seed[1]);b["id"]="audit-b"
      for width in (1440,620):
       for i in range(20):a1_trial(browser,width,i,a,b)
    browser.close()
summary={"rail_trials":len(report["rail"]),"rail_exceptions":sum("exception" in x for x in report["rail"]),
 "capture_drift":sum(x.get("capture_delta") is not None and abs(x["capture_delta"])>2 for x in report["rail"]),
 "restoration_drift":sum(x.get("restore_delta") is not None and abs(x["restore_delta"])>2 for x in report["rail"]),
 "a1_trials":len(report["a1"]),"a1_failures":sum(not all(x.get(k,False) for k in ("save_match","backup_match_before","reload_match","backup_match_after","primary_match_after")) for x in report["a1"]),
 "page_errors":sum(bool(x["page_errors"]) for x in report["rail"]+report["a1"])}
report["summary"]=summary
out.write_text(json.dumps(report,ensure_ascii=False,indent=2))
print("DIAGNOSTIC SUMMARY",variant,mode,json.dumps(summary),flush=True)
assert len(report["rail"])==40
assert len(report["a1"])==(0 if variant=="original" else 40)
