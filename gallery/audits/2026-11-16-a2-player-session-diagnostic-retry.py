#!/usr/bin/env python3
"""Replay original diagnostic with CSP-compatible test predicates and fixture URLs only."""
import hashlib,json
from pathlib import Path
original=Path(__file__).with_name("2026-11-16-a2-player-session-diagnostic.py")
raw=original.read_bytes()
assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()=="398576c427f2a9d3b735d3868f7dca6c505cfd9b"
source=raw.decode("utf-8")
for old,new,count in json.loads("[[\"page.wait_for_function(\\\"window.__picker.length===1\\\")\",\"page.wait_for_function(\\\"()=>window.__picker.length===1\\\")\",3],[\"page.wait_for_function(\\\"window.__picker.length===2\\\")\",\"page.wait_for_function(\\\"()=>window.__picker.length===2\\\")\",1],[\"page.wait_for_function(\\\"document.getElementById('local-file-label').textContent==='newest-selection.wav'\\\")\",\"page.wait_for_function(\\\"()=>document.getElementById('local-file-label').textContent==='newest-selection.wav'\\\")\",1],[\"page.wait_for_function(\\\"isLocalVideoReady\\\")\",\"page.wait_for_function(\\\"()=>isLocalVideoReady&&document.getElementById('local-video').readyState>=1\\\")\",1],[\"page.wait_for_function(\\\"window.__vlc.length===1\\\")\",\"page.wait_for_function(\\\"()=>window.__vlc.length===1\\\")\",1],[\"page.wait_for_function(\\\"sfPlayerDemo.active&&sfPlayerDemo.playing\\\")\",\"page.wait_for_function(\\\"()=>sfPlayerDemo.active&&sfPlayerDemo.playing\\\")\",1],[\"page.evaluate(\\\"({i,name,url})=>window.__picker[i].resolve({name,fileURL:url})\\\",{\\\"i\\\":i,\\\"name\\\":name,\\\"url\\\":media_url})\",\"page.evaluate(\\\"\\\"\\\"({i,name,url})=>{const bytes=Uint8Array.from(atob(url.split(',')[1]),c=>c.charCodeAt(0));const fileURL=URL.createObjectURL(new Blob([bytes],{type:'audio/wav'}));window.__picker[i].resolve({name,fileURL});}\\\"\\\"\\\",{\\\"i\\\":i,\\\"name\\\":name,\\\"url\\\":media_url})\",1],[\"        page.add_init_script(\\\"\\\"\\\"()=>{window.__urlEvents=[];\",\"        page.goto(origin,wait_until=\\\"domcontentloaded\\\")\\n        page.evaluate(\\\"\\\"\\\"()=>{window.__urlEvents=[];\",1],[\"        page.goto(origin,wait_until=\\\"domcontentloaded\\\")\\n        open_player(page)\",\"        open_player(page)\",1]]"):
    assert source.count(old)==count,(old,count)
    source=source.replace(old,new)
exec(compile(source,str(original),"exec"),{"__file__":str(original),"__name__":"__main__"})
