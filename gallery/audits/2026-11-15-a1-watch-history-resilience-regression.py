#!/usr/bin/env python3
"""A1 fail-closed regression using isolated synthetic file-origin storage."""
import copy
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

HTML=Path(sys.argv[1]).resolve()
KEY="gallery.watchHistory.v100.preview"
BACKUP=KEY+".recovery-original"
INIT="""({key,backup,raw,existing,blocked})=>{
 const get=Storage.prototype.getItem,set=Storage.prototype.setItem;
 window.__a1={reads:0,writes:0,backupWrites:0};
 window.__a1read=k=>get.call(localStorage,k);
 if(!get.call(sessionStorage,'__a1_initialized')){
  if(raw!==null)set.call(localStorage,key,raw);
  if(existing!==null)set.call(localStorage,backup,existing);
  set.call(sessionStorage,'__a1_initialized','yes');
 }
 Storage.prototype.getItem=function(k){
  if(k===key&&blocked==='read'){window.__a1.reads++;throw new DOMException('blocked','SecurityError');}
  return get.call(this,k);
 };
 Storage.prototype.setItem=function(k,v){
  if(k===key){window.__a1.writes++;if(blocked==='primary')throw new DOMException('blocked','QuotaExceededError');}
  if(k===backup){window.__a1.backupWrites++;if(blocked==='backup')throw new DOMException('blocked','QuotaExceededError');}
  return set.call(this,k,v);
 };
}"""
def dumped(x):return json.dumps(x,ensure_ascii=False,separators=(",",":"))
def modified(r,**kw):return {**copy.deepcopy(r),**kw}
def missing(r,key):
    r=copy.deepcopy(r);r.pop(key,None);return r
def eps(r,**kw):
    r=copy.deepcopy(r);r["episodes"][0].update(kw);return r
def context_for(browser,raw,width,blocked=None,existing=None):
    ctx=browser.new_context(viewport={"width":width,"height":900},reduced_motion="reduce")
    page=ctx.new_page();errors=[]
    page.on("pageerror",lambda exc:errors.append(str(exc)))
    page.add_init_script("("+INIT+")("+dumped(dict(key=KEY,backup=BACKUP,raw=raw,existing=existing,blocked=blocked))+")")
    page.goto(HTML.as_uri(),wait_until="load")
    page.locator("#wh-view-history").wait_for(state="visible")
    assert page.evaluate("k=>window.__a1read(k)",KEY)==raw
    assert page.evaluate("k=>window.__a1read(k)",BACKUP)==existing
    assert page.evaluate("window.__a1.writes===0&&window.__a1.backupWrites===0")
    return ctx,page,errors
def records(page):return page.evaluate("JSON.parse(JSON.stringify(whRecords))")
def history(page):
    page.locator("#wh-view-history").click()
    page.locator("#wh-root").wait_for(state="visible")
def search(page,query):
    page.locator("#search").click()
    page.locator("#header-search-input").fill(query)
    page.wait_for_timeout(40)
    ids=page.locator("[data-wh-row]").evaluate_all("nodes=>nodes.map(n=>n.dataset.whRow)")
    page.locator("#header-search-input").press("Escape")
    return ids
def toggle(page,rid):
    row=page.locator("[data-wh-row]").filter(has=page.locator("[data-wh-expand]")).filter(has=page.locator(f'[data-wh-expand="{rid}"]'))
    assert row.count()==1
    row.locator("[data-wh-expand]").click()
    btn=row.locator("[data-wh-episode]").first
    before=btn.get_attribute("aria-pressed")
    btn.click()
    assert btn.get_attribute("aria-pressed")!=before
def raw_at(page,k=KEY):return page.evaluate("k=>window.__a1read(k)",k)

with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True)
    clean=browser.new_page();clean.goto(HTML.as_uri(),wait_until="load")
    seed=clean.evaluate("JSON.parse(JSON.stringify(whSeed))");clean.close()
    a=copy.deepcopy(seed[0]);a["id"]="audit-a";a["episodes"]=a["episodes"][:2];a["latestEpisode"]=a["episodes"][0]["n"]
    a["compatibleExtra"]={"retain":True};a["episodes"][0]["compatibleExtra"]="retain"
    b=copy.deepcopy(seed[1]);b["id"]="audit-b"
    cases=[
      ("missing",None,seed),
      ("valid",dumped([a,b]),[a,b]),
      ("valid_empty","[]",[]),
      ("invalid_json","{broken",[]),
      ("non_array",dumped({"bad":True}),[]),
      ("null_record",dumped([None,b]),[b]),
      ("missing_id",dumped([missing(a,"id"),b]),[b]),
      ("minimal",dumped([{"id":"minimal","episodes":[]},b]),[b]),
      ("missing_last",dumped([missing(a,"last"),b]),[a,b]),
      ("numeric_last",dumped([modified(a,last=123),b]),[a,b]),
      ("missing_dates",dumped([missing(a,"dates"),b]),[modified(a,dates=[a["last"]]),b]),
      ("invalid_dates",dumped([modified(a,dates=[None,23,"2026-02-30",a["last"]]),b]),[modified(a,dates=[a["last"]]),b]),
      ("unknown_date",dumped([modified(a,last=None,dates=[]),b]),[modified(a,last="",dates=[]),b]),
      ("missing_title",dumped([missing(a,"title"),b]),[modified(a,title=a["short"]),b]),
      ("missing_group",dumped([missing(a,"group"),b]),[modified(a,group=a["id"]),b]),
      ("missing_cover",dumped([missing(a,"cover"),b]),[modified(a,cover="linear-gradient(145deg,#414753,#737b87)"),b]),
      ("empty_episodes",dumped([modified(a,episodes=[]),b]),[b]),
      ("null_episode",dumped([modified(a,episodes=[None]),b]),[b]),
      ("missing_episode_number",dumped([modified(a,episodes=[{"started":True}]),b]),[b]),
      ("duplicate_record_id",dumped([a,modified(b,id=a["id"]),b]),[b]),
      ("duplicate_episode_number",dumped([modified(a,episodes=[a["episodes"][0],a["episodes"][0]]),b]),[b]),
      ("invalid_progress",dumped([eps(a,watched="false",started="true",progressSeconds="bad",duration=-1),b]),[b]),
      ("out_of_range_progress",dumped([eps(a,progressSeconds=a["episodes"][0]["duration"]+1),b]),[b]),
      ("invalid_manual_status",dumped([eps(a,manualStatus="unexpected"),b]),[a,b]),
      ("markup_cover",dumped([modified(a,cover='red"><span data-a1-injected="yes"></span><span style="'),b]),[modified(a,cover="linear-gradient(145deg,#414753,#737b87)"),b]),
      ("markup_episode",dumped([eps(a,n='1"><span data-a1-injected="yes"></span><span data-n="'),b]),[b]),
      ("external_cover",dumped([modified(a,cover="url(https://example.invalid/cover.png)"),b]),[modified(a,cover="linear-gradient(145deg,#414753,#737b87)"),b]),
      ("markup_title",dumped([modified(a,title='<span data-a1-injected="yes">Title</span>'),b]),[modified(a,title='<span data-a1-injected="yes">Title</span>'),b]),
    ]
    # All 28 cases must load Discover, render History and support both date and title search.
    for width in (1440,620):
        for label,raw,expected in cases:
            ctx,page,errors=context_for(browser,raw,width)
            try:
                assert records(page)==expected,(label,width,records(page),expected)
                assert not page.locator("[data-a1-injected]").count(),label
                history(page)
                assert page.locator("[data-wh-row]").count()==len(expected),(label,width)
                assert not page.locator("[data-a1-injected]").count(),label
                expected_date={r["id"] for r in expected if any(d.startswith("2026") for d in r["dates"]) or "2026" in r["title"]}
                assert set(search(page,"2026"))==expected_date,(label,width)
                expected_title={r["id"] for r in expected if "pokémon" in r["title"].lower()}
                assert set(search(page,"Pokémon"))==expected_title,(label,width)
                assert raw_at(page)==raw and raw_at(page,BACKUP) is None,label
                assert not errors,(label,width,errors)
                if label=="unknown_date":assert "Last watched Unknown" in page.locator('[data-wh-row="audit-a"]').inner_text()
            finally:ctx.close()
        # Real toggle/save/reload, valid and repaired data, exact original and unknown compatible fields.
        for label,raw,blocked,existing,expected,save_ok in [
            ("valid_save",dumped([a,b]),None,None,[a,b],True),
            ("recovery_save",dumped([None,a,b]),None,None,[a,b],True),
            ("backup_already_exact",dumped([None,a,b]),None,dumped([None,a,b]),[a,b],True),
            ("backup_conflict",dumped([None,a,b]),None,"earlier original",[a,b],False),
            ("backup_write_failure",dumped([None,a,b]),"backup",None,[a,b],False),
            ("primary_write_failure",dumped([None,a,b]),"primary",None,[a,b],False),
            ("read_blocked",dumped([a,b]),"read",None,seed,False),
            ("valid_write_blocked",dumped([a,b]),"primary",None,[a,b],False),
        ]:
            ctx,page,errors=context_for(browser,raw,width,blocked,existing)
            try:
                assert records(page)==expected,label
                history(page);rid=expected[0]["id"]
                toggle(page,rid)
                edited=records(page)
                assert edited[0]["episodes"][0]["manualStatus"] in ("never","partial","watched"),label
                assert edited[0]["episodes"][0]["progressSeconds"]==expected[0]["episodes"][0]["progressSeconds"],label
                assert edited[0]["episodes"][0]["duration"]==expected[0]["episodes"][0]["duration"],label
                if save_ok:
                    assert json.loads(raw_at(page))==edited,label
                    expected_backup=raw if label!="valid_save" else None
                    assert raw_at(page,BACKUP)==expected_backup,label
                    page.reload(wait_until="load")
                    assert records(page)==edited,label
                    assert raw_at(page,BACKUP)==expected_backup,label
                else:
                    assert raw_at(page)==raw,label
                    expected_backup=raw if label=="primary_write_failure" else existing
                    assert raw_at(page,BACKUP)==expected_backup,label
                    if label=="read_blocked":assert page.evaluate("window.__a1.writes===0&&window.__a1.reads>0"),label
                assert not errors,(label,width,errors)
            finally:ctx.close()
        # Another window has changed the primary since load: do not overwrite.
        raw=dumped([a,b]);ctx,page,errors=context_for(browser,raw,width)
        try:
            replacement=dumped([b]);page.evaluate("([k,v])=>localStorage.setItem(k,v)",[KEY,replacement])
            history(page);toggle(page,a["id"])
            assert raw_at(page)==replacement and raw_at(page,BACKUP) is None and not errors
        finally:ctx.close()
        # Invalid top-level data has no visible records; later explicit save must back up exact bytes.
        raw="{broken";ctx,page,errors=context_for(browser,raw,width)
        try:
            page.evaluate("r=>{whRecords.push(r);whSave();}",a)
            assert json.loads(raw_at(page))==[a] and raw_at(page,BACKUP)==raw and not errors
        finally:ctx.close()
        print("A1 mandatory recovery regression passed:",HTML.name,width,"38 cases",flush=True)
    browser.close()
