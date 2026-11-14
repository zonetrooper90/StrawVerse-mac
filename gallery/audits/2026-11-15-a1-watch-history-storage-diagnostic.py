#!/usr/bin/env python3
"""Read-only A1: exercise real Gallery HTML with synthetic isolated storage."""
import copy
import hashlib
import json
import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

ROOT = Path(__file__).resolve().parents[1]
MODE = sys.argv[1]
FILES = {
    "full": ("Gallery-current.html", "0eef4d2c7e935271a05228a54f489c47eb00461fff661c2b51865f8ad7d724e4"),
    "lightweight": ("Gallery-development.html", "4274d82b64a260340d8f7105e16760d69a58a96b0c4cd3d0005d048565c42096"),
}
name, digest = FILES[MODE]
html = ROOT / name
assert hashlib.sha256(html.read_bytes()).hexdigest() == digest, "Unexpected audited build"
KEY = "gallery.watchHistory.v100.preview"
URL = html.as_uri()

INIT = """({key,raw,blocked}) => {
  const get = Storage.prototype.getItem, set = Storage.prototype.setItem;
  const state = {error:null, before:null, seeded:false, reads:0, writes:0};
  window.__a1 = state;
  window.__a1raw = () => get.call(localStorage,key);
  try {
    if (!get.call(sessionStorage,'__a1_initialized')) {
      if(raw !== null) set.call(localStorage,key,raw);
      set.call(sessionStorage,'__a1_initialized','yes');
    }
    state.before = get.call(localStorage,key);
    state.seeded = true;
  } catch(e) { state.error = String(e); }
  if(blocked) {
    Storage.prototype.getItem = function(k) {
      if(k===key && (blocked==='read' || blocked==='both')) {state.reads++;throw new DOMException('Synthetic blocked read','SecurityError');}
      return get.call(this,k);
    };
    Storage.prototype.setItem = function(k,v) {
      if(k===key && (blocked==='write' || blocked==='both')) {state.writes++;throw new DOMException('Synthetic blocked write','QuotaExceededError');}
      return set.call(this,k,v);
    };
  }
}"""
SNAP = """() => {
  const result = {discover:!!document.querySelector('.sf-discover-page #sf-discover-explore'),
    history:!!document.querySelector('#wh-root'), recent:document.querySelectorAll('[data-wh-recent]').length,
    rows:document.querySelectorAll('[data-wh-row]').length, injected:!!document.querySelector('[data-a1-injected]'),
    body:document.body.className, storage:window.__a1, raw:window.__a1raw()};
  try {result.records=whRecords.map(r=>({id:r?.id,episodes:Array.isArray(r?.episodes)?r.episodes.length:null}));}
  catch(e){result.recordError=String(e);}
  return result;
}"""

def fixture(seed):
    a = copy.deepcopy(seed[0])
    b = copy.deepcopy(seed[1])
    a["id"] = "audit-a"
    b["id"] = "audit-b"
    a["episodes"] = [copy.deepcopy(a["episodes"][0]), copy.deepcopy(a["episodes"][1])]
    a["latestEpisode"] = a["episodes"][0]["n"]
    return a, b

def cases(seed):
    a,b = fixture(seed)
    def variant(**kwargs):
        return [{**copy.deepcopy(a), **kwargs}, copy.deepcopy(b)]
    def missing(field):
        x=copy.deepcopy(a); x.pop(field,None); return [x,copy.deepcopy(b)]
    def ep_variant(**kwargs):
        x=copy.deepcopy(a); x["episodes"][0].update(kwargs); return [x,copy.deepcopy(b)]
    def raw(value):
        return json.dumps(value,ensure_ascii=False)
    return [
        ("no_saved_data",None,None),
        ("valid_seed",raw(seed),None),
        ("valid_subset",raw([a,b]),None),
        ("empty_history",raw([]),None),
        ("invalid_json","{not-json",None),
        ("non_array",raw({"id":"bad"}),None),
        ("null_record",raw([None]),None),
        ("missing_id",raw(missing("id")),None),
        ("minimal_record",raw([{"id":"audit-min","episodes":[]}]),None),
        ("missing_last",raw(missing("last")),None),
        ("numeric_last",raw(variant(last=123)),None),
        ("missing_dates",raw(missing("dates")),None),
        ("invalid_date_entries",raw(variant(dates=[None,23])),None),
        ("missing_title",raw(missing("title")),None),
        ("missing_group",raw(missing("group")),None),
        ("missing_cover",raw(missing("cover")),None),
        ("empty_episodes",raw(variant(episodes=[])),None),
        ("null_episode",raw(variant(episodes=[None])),None),
        ("missing_episode_number",raw(variant(episodes=[{"started":True}])),None),
        ("duplicate_record_id",raw([a,{**b,"id":a["id"]}]),None),
        ("duplicate_episode_number",raw(variant(episodes=[a["episodes"][0],a["episodes"][0]])),None),
        ("invalid_progress",raw(ep_variant(watched="false",started="true",progressSeconds="not-a-number",duration=-1)),None),
        ("invalid_manual_status",raw(ep_variant(manualStatus="unexpected")),None),
        ("inert_markup_in_cover",raw(variant(cover='red"><span data-a1-injected="yes"></span><span style="')),None),
        ("inert_markup_in_episode_number",raw(ep_variant(n='1"><span data-a1-injected="yes"></span><span data-n="')),None),
        ("storage_read_blocked",raw([a,b]),"read"),
        ("storage_write_blocked",raw([a,b]),"write"),
        ("storage_both_blocked",raw([a,b]),"both"),
    ]

def snapshot(page, errors):
    result=page.evaluate(SNAP)
    raw=result.pop("raw")
    # Record hashes, not complete history payloads. All inputs are synthetic.
    result["raw_sha256"]=hashlib.sha256(raw.encode()).hexdigest() if raw is not None else None
    storage=result["storage"]
    before=storage.pop("before",None)
    result["initial_raw_sha256"]=hashlib.sha256(before.encode()).hexdigest() if before is not None else None
    result["errors"]=list(errors)
    return result

def run_case(browser,case,seed,width):
    label,raw,blocked=case
    context=browser.new_context(viewport={"width":width,"height":900},reduced_motion="reduce")
    page=context.new_page()
    errors=[]
    page.on("pageerror",lambda exc: errors.append(str(exc)))
    page.add_init_script("("+INIT+")("+json.dumps({"key":KEY,"raw":raw,"blocked":blocked})+")")
    result={"case":label,"width":width,"mode":MODE,"stages":{},"actions":{}}
    try:
        page.goto(URL,wait_until="load")
        page.wait_for_timeout(100)
        initial=snapshot(page,errors)
        assert initial["storage"]["seeded"] and not initial["storage"]["error"], ("fixture injection failed",label,initial)
        assert initial["initial_raw_sha256"]==(hashlib.sha256(raw.encode()).hexdigest() if raw is not None else None), ("fixture mismatch",label)
        result["stages"]["startup"]=initial
        if initial["discover"] and page.locator("#wh-view-history").is_visible():
            try:
                page.locator("#wh-view-history").click(timeout=1500)
                page.wait_for_timeout(100)
                result["stages"]["history"]=snapshot(page,errors)
                if result["stages"]["history"]["history"]:
                    # Exercise actual date search, which assumes well-formed date arrays.
                    page.locator("#search").click(timeout=1500)
                    page.locator("#header-search-input").fill("2026",timeout=1500)
                    page.wait_for_timeout(100)
                    result["stages"]["date_search"]=snapshot(page,errors)
                    page.locator("#header-search-input").press("Escape",timeout=1500)
                    page.wait_for_timeout(100)
                    result["stages"]["search_closed"]=snapshot(page,errors)
                    if label in ("valid_subset","storage_write_blocked","storage_both_blocked","storage_read_blocked"):
                        row=page.locator("[data-wh-row]").first
                        if row.count():
                            row.locator("[data-wh-expand]").click(timeout=1500)
                            button=row.locator("[data-wh-episode]").first
                            before=button.get_attribute("aria-pressed",timeout=1500)
                            button.click(timeout=1500)
                            after=button.get_attribute("aria-pressed",timeout=1500)
                            result["actions"]["toggle"]={"before":before,"after":after}
                            result["stages"]["toggle"]=snapshot(page,errors)
                            if label=="valid_subset":
                                page.reload(wait_until="load")
                                page.wait_for_timeout(100)
                                result["stages"]["reload"]=snapshot(page,errors)
                                result["actions"]["persisted"]=page.evaluate("whRecords.some(r=>r.episodes.some(e=>typeof e.manualStatus==='string'))")
            except PlaywrightTimeout as exc:
                result["actions"]["timeout"]=str(exc).splitlines()[0]
        result["final_errors"]=list(errors)
        # Expected-good controls distinguish a harness failure from an application defect.
        if label in ("no_saved_data","valid_seed","valid_subset","empty_history","invalid_json","non_array","null_record","missing_id","storage_read_blocked","storage_write_blocked","storage_both_blocked"):
            assert initial["discover"] and result["stages"].get("history",{}).get("history"), ("control failed",result)
            assert not errors and "timeout" not in result["actions"], ("control failed",result)
            if label=="empty_history":
                assert initial["records"]==[] and result["stages"]["history"]["rows"]==0, result
            if label in ("no_saved_data","invalid_json","non_array","null_record","missing_id","storage_read_blocked","storage_both_blocked"):
                assert len(initial["records"])==len(seed), ("fallback control",result)
            if label=="valid_subset":
                assert len(initial["records"])==2 and result["actions"]["persisted"] and result["actions"]["toggle"]["before"]!=result["actions"]["toggle"]["after"],result
            if label in ("storage_read_blocked","storage_both_blocked"):
                assert initial["storage"]["reads"]>0,result
            if label in ("storage_write_blocked","storage_both_blocked"):
                assert result["stages"]["toggle"]["storage"]["writes"]>0,result
        return result
    finally:
        context.close()

def classify(r):
    stages=r["stages"]
    if not stages["startup"]["discover"]:return "startup_failure"
    if not stages.get("history",{}).get("history"):return "history_failure"
    if r["final_errors"] or "timeout" in r["actions"]:return "interaction_failure"
    if any(v["injected"] for v in stages.values()):return "unexpected_markup"
    return "no_runtime_failure_observed"

with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True)
    clean=browser.new_page()
    clean.goto(URL,wait_until="load")
    seed=clean.evaluate("JSON.parse(JSON.stringify(whSeed))")
    assert len(seed)>1 and len(seed[0]["episodes"])>1
    clean.close()
    results=[]
    for width in (1440,620):
        for case in cases(seed):
            r=run_case(browser,case,seed,width)
            r["classification"]=classify(r)
            print("A1 "+json.dumps({"case":r["case"],"width":width,"mode":MODE,"classification":r["classification"],"errors":r["final_errors"],"stages":{k:{"discover":v["discover"],"history":v["history"],"rows":v["rows"],"recent":v["recent"],"injected":v["injected"]} for k,v in r["stages"].items()},"actions":r["actions"]},ensure_ascii=False),flush=True)
            results.append(r)
    browser.close()
assert len(results)==56
counts={}
for r in results:
    k=r["classification"];counts[k]=counts.get(k,0)+1
summary=f"A1 {MODE}: {len(results)} isolated real-browser cases; {json.dumps(counts,sort_keys=True)}. Diagnostic completion is not a bug-fix pass."
print(summary,flush=True)
out=Path(os.environ["RUNNER_TEMP"])/f"a1-{MODE}.json"
out.write_text(json.dumps({"mode":MODE,"sha256":digest,"summary":counts,"results":results},indent=2,ensure_ascii=False)+"\n")
if os.environ.get("GITHUB_STEP_SUMMARY"):
    with open(os.environ["GITHUB_STEP_SUMMARY"],"a",encoding="utf-8") as s:
        s.write(summary+"\n")
