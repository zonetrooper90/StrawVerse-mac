#!/usr/bin/env python3
"""A2.1: read-only Player session diagnostic. Findings are not mandatory-test verdicts."""
import base64, hashlib, io, json, sys, traceback, wave
from pathlib import Path
from playwright.sync_api import sync_playwright

mode,motion,out=sys.argv[1:]
assert mode in ("full","lightweight") and motion in ("no-preference","reduce")
root=Path(__file__).resolve().parents[1]
html=root/("Gallery-current.html" if mode=="full" else "Gallery-development.html")
expected={"full":"9e5366a1e54a7719eeff8c7127298bf9371808a2c2749a704fcacc2634dbc37a","lightweight":"fb2c515b0ef9efc6e65b870b726c602cd48659872a4bc467504187a95e465dbf"}[mode]
source=html.read_bytes()
assert hashlib.sha256(source).hexdigest()==expected
# Real, silent PCM media; no image, user file, network or external playback.
buf=io.BytesIO()
with wave.open(buf,"wb") as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(8000);w.writeframes(b"\0"*8000*2*32)
media=buf.getvalue()
media_url="data:audio/wav;base64,"+base64.b64encode(media).decode()
origin="http://gallery-a2.invalid/"
results=[]
snapshot=r"""()=>{const v=document.getElementById('local-video'),o=window.__oldVideo, rec=whRecords.find(r=>r.galleryId===state.detailId&&r.installmentId===state.playback?.installmentId);
const media=e=>e?{connected:e.isConnected,paused:e.paused,seeking:e.seeking,time:e.currentTime,duration:Number.isFinite(e.duration)?e.duration:null,ready:e.readyState,network:e.networkState,hasSrc:!!e.getAttribute('src')}:null;
return {episode:state.playback?.episode??null,installment:state.playback?.installmentId??null,detail:state.detailId,video:media(v),old:media(o),
sameVideo:!!v&&v===o,ready:isLocalVideoReady,label:document.getElementById('local-file-label')?.textContent??null,notice:document.getElementById('player-notice')?.textContent??null,
empty:document.getElementById('player-empty')?.hidden??null,session:whPlayerSession?{...whPlayerSession}:null,
history:rec?{id:rec.id,latest:rec.latestEpisode,episode:rec.episodes.find(e=>e.n===state.playback?.episode)||null}:null,
historyJson:JSON.stringify(whRecords),demo:{active:sfPlayerDemo.active,playing:sfPlayerDemo.playing,frame:!!sfPlayerDemo.frame},morph:!!sfPlayMorph.frame,nextMorph:!!playNextMorph.frame,
timer:!!playerControlsTimer,controller:!!playerEventController,oldAborted:window.__oldController?.signal.aborted??null,objectURL:!!sfPlayerLocalObjectURL,urls:window.__urlEvents||[],events:window.__mediaEvents||[]};}"""
def snap(page):
    s=page.evaluate(snapshot)
    # Report change fingerprint instead of dumping every seed record or cover.
    s["historyDigest"]=hashlib.sha256(s.pop("historyJson").encode()).hexdigest()
    return s

def settled(page):
    page.wait_for_function("()=>!galleryStageTransition&&!galleryStageFadeInProgress&&!galleryStagePending",timeout=10000)
def open_player(page):
    page.locator('[data-detail]').first.click()
    page.wait_for_selector('#detail-back');settled(page)
    enter_player(page)
def enter_player(page):
    page.locator('.detail-actions [data-episode-action="watch"]').first.click()
    page.wait_for_selector('#player-area');settled(page)
    assert page.evaluate("state.playback.episode") == 5
    assert page.locator('#next-episode').is_visible()
def next_episode(page):
    old=page.evaluate("state.playback.episode")
    page.locator('#next-episode').click()
    page.wait_for_function("(n)=>state.playback?.episode!==n",arg=old,timeout=10000)
    settled(page)
    assert page.evaluate("state.playback.episode")==old+1
def back(page):
    page.locator('#back-from-playback').click()
    page.wait_for_selector('#detail-back');settled(page)
    assert page.evaluate("!state.playback&&!document.getElementById('local-video')")
def hold_old(page):
    page.evaluate("""()=>{window.__oldVideo=document.getElementById('local-video');window.__oldController=playerEventController;
      const v=window.__oldVideo;window.__mediaEvents=[];
      for(const type of ['timeupdate','seeked','loadedmetadata','error','play','pause','emptied','ended'])v.addEventListener(type,e=>{
        window.__mediaEvents.push({type,trusted:e.isTrusted,connected:v.isConnected,time:v.currentTime,paused:v.paused,active:state.playback?.episode??null});
      });}""")
def cdp_listeners(page):
    cdp=page.context.new_cdp_session(page)
    answer={}
    try:
        for name,expr in (("oldVideo","window.__oldVideo"),("oldTracks","window.__oldVideo?.textTracks"),("currentVideo","document.getElementById('local-video')"),("document","document")):
            obj=cdp.send("Runtime.evaluate",{"expression":expr,"objectGroup":"a2-inspect"})["result"]
            if "objectId" not in obj: answer[name]=None;continue
            items=cdp.send("DOMDebugger.getEventListeners",{"objectId":obj["objectId"]})["listeners"]
            counts={}
            for item in items: counts[item["type"]]=counts.get(item["type"],0)+1
            answer[name]=counts
    finally:
        cdp.send("Runtime.releaseObjectGroup",{"objectGroup":"a2-inspect"})
        cdp.detach()
    return answer
def load_local(page):
    page.locator('#sf-player-browser-file').set_input_files({"name":"synthetic-silence.wav","mimeType":"audio/wav","buffer":media})
    page.wait_for_function("()=>isLocalVideoReady&&document.getElementById('local-video').readyState>=1",timeout=10000)
    assert page.evaluate("document.getElementById('local-video').duration")>=31
def start_local(page):
    load_local(page)
    page.locator('#pause-play').click()
    page.wait_for_function("()=>!document.getElementById('local-video').paused&&document.getElementById('local-video').currentTime>0.2",timeout=10000)
def bridge(page):
    # Add the stub after app bootstrap so desktop settings initialization is not involved.
    page.evaluate("""()=>{window.__picker=[];window.__vlc=[];window.galleryDesktop={
      openVideo:()=>new Promise((resolve,reject)=>window.__picker.push({resolve,reject})),
      openInVLC:()=>new Promise((resolve,reject)=>window.__vlc.push({resolve,reject}))
    };}""")
def choose(page,i,name):
    page.evaluate("({i,name,url})=>window.__picker[i].resolve({name,fileURL:url})",{"i":i,"name":name,"url":media_url})
def observe(case,label,page):
    s=snap(page);case["trace"].append({"stage":label,"snapshot":s});return s
def finding(case,name,observed,detail=""):
    case["findings"].append({"name":name,"observed":bool(observed),"detail":detail})
def run_case(browser,kind,repeat):
    case={"mode":mode,"motion":motion,"case":kind,"repeat":repeat,"trace":[],"findings":[],"errors":[],"status":"completed"}
    context=browser.new_context(viewport={"width":1440,"height":900},reduced_motion=motion)
    page=context.new_page()
    page.on("pageerror",lambda e:case["errors"].append(str(e)))
    try:
        page.route("**/*",lambda r:r.fulfill(status=200,content_type="text/html; charset=utf-8",body=source) if r.request.url==origin else r.abort())
        page.add_init_script("""()=>{window.__urlEvents=[];const create=URL.createObjectURL.bind(URL),revoke=URL.revokeObjectURL.bind(URL);
          URL.createObjectURL=(obj)=>{const url=create(obj);window.__urlEvents.push({type:'create',url});return url;};
          URL.revokeObjectURL=url=>{window.__urlEvents.push({type:'revoke',url});return revoke(url);};}""")
        page.goto(origin,wait_until="domcontentloaded")
        open_player(page)
        observe(case,"initial",page)
        if kind in ("advance-local","back-local"):
            start_local(page)
            hold_old(page)
            before=observe(case,"playing",page)
            case["listenersBefore"]=cdp_listeners(page)
            if kind=="advance-local":next_episode(page)
            else:back(page)
            # Do not dispatch events here: observe only native playback and browser events.
            after=observe(case,"departed",page)
            page.wait_for_timeout(900)
            late=observe(case,"natural-late",page)
            case["listenersAfter"]=cdp_listeners(page)
            finding(case,"old media still playing",not late["old"]["paused"],"real media element after route exit")
            finding(case,"old media source still attached",late["old"]["hasSrc"])
            finding(case,"old media advanced",late["old"]["time"]>after["old"]["time"]+.1)
            finding(case,"history changed after departure",late["historyDigest"]!=after["historyDigest"],"natural-only observation; inspect trace for originating event")
            finding(case,"old controller not aborted",late["oldAborted"] is not True)
            if kind=="advance-local":
                finding(case,"new episode has local readiness",late["ready"] or late["empty"] is True)
            else:
                finding(case,"player resources remain after Back",late["demo"]["frame"] or late["morph"] or late["nextMorph"] or late["timer"] or late["controller"] or late["objectURL"])
            created={e["url"] for e in late["urls"] if e["type"]=="create"}
            revoked={e["url"] for e in late["urls"] if e["type"]=="revoke"}
            finding(case,"unrevoked browser object URL",bool(created-revoked))
        elif kind=="injected-old-events":
            load_local(page);hold_old(page);next_episode(page)
            before=observe(case,"new-player-before-injection",page)
            case["listenersAfter"]=cdp_listeners(page)
            # Explicit synthetic delivery to retained old node, not a claim of natural timing.
            page.evaluate("window.__oldVideo.dispatchEvent(new Event('loadedmetadata'))")
            meta=observe(case,"injected-metadata",page)
            finding(case,"old metadata modified current readiness",meta["ready"]!=before["ready"] or meta["empty"]!=before["empty"])
            page.evaluate("window.__oldVideo.dispatchEvent(new Event('error'))")
            error=observe(case,"injected-error",page)
            finding(case,"old error modified current notice",error["notice"]!=meta["notice"])
            page.evaluate("window.__oldVideo.dispatchEvent(new Event('seeked'))")
            seek=observe(case,"injected-seek",page)
            finding(case,"old seek modified current session",seek["session"]!=error["session"])
            # Controlled stale event with explicit plausible media state. No native
            # scheduling claim: proves whether the old listener can write the new episode.
            page.evaluate("""()=>{const old=window.__oldVideo;
              for(const [key,value] of Object.entries({paused:false,seeking:false,duration:32,currentTime:7}))Object.defineProperty(old,key,{configurable:true,value});
              old.dispatchEvent(new Event('timeupdate'));}""")
            tick=observe(case,"injected-timeupdate",page)
            finding(case,"old timeupdate modified current history",tick["historyDigest"]!=seek["historyDigest"],"synthetic stale callback with injected media properties")
        elif kind=="picker-after-next":
            bridge(page);hold_old(page)
            page.locator('#open-local-video').click()
            page.wait_for_function("window.__picker.length===1")
            next_episode(page)
            before=observe(case,"new-episode-before-picker",page)
            choose(page,0,"stale-selection.wav")
            page.wait_for_timeout(700)
            after=observe(case,"late-picker-result",page)
            finding(case,"stale picker loaded new episode",after["label"]!=before["label"] or after["video"]["hasSrc"]!=before["video"]["hasSrc"])
        elif kind=="picker-reordered":
            bridge(page)
            page.locator('#open-local-video').click();page.wait_for_function("window.__picker.length===1")
            page.locator('#open-local-video').click();page.wait_for_function("window.__picker.length===2")
            choose(page,1,"newest-selection.wav")
            page.wait_for_function("document.getElementById('local-file-label').textContent==='newest-selection.wav'")
            before=observe(case,"newer-picker-first",page)
            choose(page,0,"older-selection.wav")
            page.wait_for_timeout(700)
            after=observe(case,"older-picker-late",page)
            finding(case,"older picker overwrote latest selection",after["label"]!=before["label"])
        elif kind=="vlc-after-next":
            bridge(page)
            page.locator('#open-local-video').click();page.wait_for_function("window.__picker.length===1")
            choose(page,0,"vlc-selection.wav")
            page.wait_for_function("isLocalVideoReady")
            page.locator('.player-dev-tools summary').click()
            page.locator('#open-external-vlc').click();page.wait_for_function("window.__vlc.length===1")
            next_episode(page)
            before=observe(case,"new-episode-before-vlc",page)
            page.evaluate("window.__vlc[0].resolve({ok:true})")
            page.wait_for_timeout(200)
            after=observe(case,"late-vlc-result",page)
            finding(case,"old VLC result modified new notice",after["notice"]!=before["notice"])
        elif kind=="repeated-demo":
            baseline=cdp_listeners(page)
            case["listenerBaseline"]=baseline
            for i in range(5):
                page.locator('#sf-player-demo-start').click()
                page.locator('#pause-play').click()
                page.wait_for_function("sfPlayerDemo.active&&sfPlayerDemo.playing")
                hold_old(page)
                next_episode(page)
                observe(case,f"cycle-{i}-next",page)
                page.locator('#sf-player-demo-start').click()
                page.locator('#pause-play').click()
                hold_old(page);back(page)
                after=observe(case,f"cycle-{i}-back",page)
                finding(case,f"cycle-{i} resources after Back",after["demo"]["frame"] or after["morph"] or after["nextMorph"] or after["timer"] or after["controller"] or after["objectURL"])
                # Returning to Details selects the last episode; reopen through real watch button.
                page.locator('.detail-actions [data-episode-action="watch"]').first.click()
                page.wait_for_selector('#player-area');settled(page)
                assert page.locator('#next-episode').is_visible()
                now=cdp_listeners(page)
                finding(case,f"cycle-{i} document listener growth",sum(now["document"].values())>sum(baseline["document"].values()))
            case["listenerFinal"]=cdp_listeners(page)
        else: raise AssertionError(kind)
    except Exception:
        case["status"]="harness-error";case["exception"]=traceback.format_exc()
        try:observe(case,"harness-error",page)
        except Exception:pass
    finally:
        context.close()
    return case
kinds=("advance-local","back-local","injected-old-events","picker-after-next","picker-reordered","vlc-after-next","repeated-demo")
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True)
    for repeat in range(2):
        for kind in kinds:
            case=run_case(browser,kind,repeat);results.append(case)
            Path(out).write_text(json.dumps(results,indent=2,ensure_ascii=False))
            print("CASE",json.dumps({k:v for k,v in case.items() if k!="trace"},ensure_ascii=False),flush=True)
            for t in case["trace"]:
                print("TRACE",json.dumps({"case":kind,"repeat":repeat,**t},ensure_ascii=False),flush=True)
    browser.close()
summary={"mode":mode,"motion":motion,"cases":len(results),"completed":sum(c["status"]=="completed" for c in results),"harnessErrors":sum(c["status"]!="completed" for c in results),"observedFindings":sum(f["observed"] for c in results for f in c["findings"]),"pageErrors":sum(len(c["errors"]) for c in results)}
print("SUMMARY",json.dumps(summary),flush=True)
assert len(results)==14 and summary["harnessErrors"]==0,summary
