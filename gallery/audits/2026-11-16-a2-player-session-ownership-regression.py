#!/usr/bin/env python3
"""Strict candidate regression derived from the immutable 56-case A2.1 diagnostic."""
import hashlib,sys,tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
retry=root/"audits/2026-11-16-a2-player-session-diagnostic-retry.py"
def blob(raw):return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
raw=retry.read_bytes()
assert blob(raw)=="056edf41a5837020e1b68cc0bafa42a5d7823e17"
html=Path(sys.argv[1]).resolve()
assert html in (root/"Gallery-current.html",root/"Gallery-development.html"),html
mode="full" if html.name=="Gallery-current.html" else "lightweight"
digest=hashlib.sha256(html.read_bytes()).hexdigest()
# Exact candidate bytes are independently verified by the publisher.
# Retain all historical diagnostic scenarios; promote every finding to an assertion.
source=raw.decode()
tail='exec(compile(source,str(original),"exec"),{"__file__":str(original),"__name__":"__main__"})'
assert source.count(tail)==1
extra=r'''
def change(old,replacement,count=1):
    global source
    assert source.count(old)==count,(old,count)
    source=source.replace(old,replacement)
change('assert hashlib.sha256(source).hexdigest()==expected','assert hashlib.sha256(source).hexdigest()==candidate_digest')
change('            before=observe(case,"playing",page)','            page.wait_for_function("()=>whPlayerSession?.lastSavedAt>0",timeout=10000)\n            before=observe(case,"playing",page)\n            assert before["history"]["episode"]["started"] and before["history"]["episode"]["duration"]==32,before["history"]')
change('            case["listenersAfter"]=cdp_listeners(page)\n            finding(case,"old media still playing"','            case["listenersAfter"]=cdp_listeners(page)\n            assert late["old"]["paused"] and not late["old"]["hasSrc"] and not late["old"]["connected"],late["old"]\n            finding(case,"old media still playing"')
change('            before=observe(case,"newer-picker-first",page)','            page.wait_for_function("()=>isLocalVideoReady&&document.getElementById(\'local-video\').readyState>=1",timeout=10000)\n            before=observe(case,"newer-picker-first",page)')
change('        elif kind=="repeated-demo":',"""        elif kind=="picker-after-back":
            bridge(page);hold_old(page)
            page.locator('#open-local-video').click();page.wait_for_function("()=>window.__picker.length===1")
            back(page)
            before=observe(case,"detail-before-picker",page)
            choose(page,0,"late-after-back.wav");page.wait_for_timeout(250)
            after=observe(case,"detail-after-picker",page)
            assert after["historyDigest"]==before["historyDigest"] and not after["controller"] and after["video"] is None
            page.locator('.detail-actions [data-episode-action="watch"]').first.click()
            page.wait_for_selector('#player-area');settled(page)
            assert page.locator('#local-file-label').text_content()=="No local file selected"
        elif kind=="auto-vlc-after-next":
            bridge(page);page.evaluate("state.playerPreference='vlc'")
            page.locator('#open-local-video').click();page.wait_for_function("()=>window.__picker.length===1")
            choose(page,0,"auto-vlc.wav")
            page.wait_for_function("()=>window.__vlc.length===1")
            next_episode(page)
            before=observe(case,"new-episode-before-auto-vlc",page)
            page.evaluate("window.__vlc[0].resolve({ok:false,message:'stale auto VLC'})")
            page.wait_for_timeout(250)
            after=observe(case,"new-episode-after-auto-vlc",page)
            assert after["notice"]==before["notice"] and not after["ready"] and after["historyDigest"]==before["historyDigest"]
        elif kind=="vlc-current":
            bridge(page);page.evaluate("state.playerPreference='built-in'")
            page.locator('#open-local-video').click();page.wait_for_function("()=>window.__picker.length===1")
            choose(page,0,"current-vlc.wav")
            page.wait_for_function("()=>isLocalVideoReady&&document.getElementById('local-video').readyState>=1")
            page.locator('.player-dev-tools summary').click()
            page.locator('#open-external-vlc').click();page.wait_for_function("()=>window.__vlc.length===1")
            page.evaluate("window.__vlc[0].resolve({ok:true})")
            page.wait_for_function("()=>document.getElementById('player-notice').textContent.includes('handed to VLC')")
            assert page.locator('#local-file-label').text_content()=="current-vlc.wav"
        elif kind=="repeated-demo":""")
change('"vlc-after-next","repeated-demo")','"vlc-after-next","picker-after-back","auto-vlc-after-next","vlc-current","repeated-demo")')
change('assert len(results)==14 and summary["harnessErrors"]==0,summary','assert len(results)==20 and summary["harnessErrors"]==0 and summary["pageErrors"]==0 and summary["observedFindings"]==0,summary')
exec(compile(source,str(original),"exec"),{"__file__":str(original),"__name__":"__main__","candidate_digest":candidate_digest})
'''
with tempfile.TemporaryDirectory() as tmp:
    for motion in ("no-preference","reduce"):
        old_argv=sys.argv[:]
        try:
            sys.argv=[str(retry),mode,motion,str(Path(tmp)/"result.json")]
            exec(compile(source.replace(tail,extra),str(retry),"exec"),{"__file__":str(retry),"__name__":"__main__","candidate_digest":digest})
        finally:sys.argv=old_argv
print("PASS A2.1 strict ownership regression: 40 cases in this exact HTML mode",flush=True)
