#!/usr/bin/env python3
"""Isolate A1 file-origin reload loss from application logic and timing."""
import copy,hashlib,json,sys,tempfile,threading,time,traceback
from pathlib import Path
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from playwright.sync_api import sync_playwright
mode,origin,output=sys.argv[1:]
out=Path(output)
root=Path(__file__).resolve().parents[1]
html=root/("Gallery-current.html" if mode=="full" else "Gallery-development.html")
digest=hashlib.sha256(html.read_bytes()).hexdigest()
assert digest=={"full":"dd93f30c2bc170d08f43ceaa459205bd4b157e8d40d2df8f29e0133de10134d3","lightweight":"76ede7481d40dfc3b0e674c4808de45df468818792e5d4dd937ae205cb953da3"}[mode]
fixture=root/"audits/2026-11-15-a1-watch-history-resilience-regression.py"
raw=fixture.read_bytes()
assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()=="6d988f3e04e7637bae5e3f7649e02087004c88d4"
ns={}
saved=sys.argv
sys.argv=[str(fixture),str(html)]
exec(compile(fixture.read_text().split("with sync_playwright() as pw:")[0],str(fixture),"exec"),ns)
sys.argv=saved
KEY=ns["KEY"];BACKUP=ns["BACKUP"]
# Exact fixture initializer, with passive pre-app storage snapshot appended.
INIT=ns["INIT"]
pre_app="""([k,b])=>{window.__preApp={primary:window.__a1read(k),backup:window.__a1read(b),
 marker:sessionStorage.getItem('__a1_initialized')};}"""
control=b"<!doctype html><meta charset=utf-8><title>Local storage control</title><p>Browser-only synthetic fixture</p>"
app=html.read_bytes()
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ("/app.html","/control.html"):
            self.send_error(404);return
        data=app if self.path=="/app.html" else control
        self.send_response(200);self.send_header("Content-Type","text/html; charset=utf-8")
        self.send_header("Content-Length",str(len(data)));self.end_headers();self.wfile.write(data)
    def log_message(self,*args):pass
report={"mode":mode,"origin":origin,"sha256":digest,"trials":[]}
def emit(row):
    report["trials"].append(row);out.write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print("TRIAL",json.dumps({k:v for k,v in row.items() if k not in ("before","after","pre_app","expected","actual")}),flush=True)
def storage(page,kind):
    return page.evaluate("""([k,b,kind])=>({primary:window.__a1read(k),backup:window.__a1read(b),
      marker:sessionStorage.getItem('__a1_initialized'),counts:window.__a1,pre:window.__preApp,
      loaded:kind==='app'?whLoadedRaw:null,needs:kind==='app'?whNeedsRecovery:null})""",[KEY,BACKUP,kind])
def trial(browser,urls,kind,width,label,delay,repeat,a,b):
    raw=ns["dumped"]([a,b] if label=="valid" else [None,a,b])
    existing=raw if label=="backup_already_exact" else None
    expected_backup=raw if label!="valid" else None
    ctx=browser.new_context(viewport={"width":width,"height":900},reduced_motion="reduce")
    page=ctx.new_page();errors=[];page.on("pageerror",lambda e:errors.append(str(e)))
    row={"kind":kind,"width":width,"label":label,"delay_ms":delay,"repeat":repeat}
    try:
        payload=ns["dumped"](dict(key=KEY,backup=BACKUP,raw=raw,existing=existing,blocked=None))
        # One init script guarantees fixture initialization precedes the snapshot.
        page.add_init_script("("+INIT+")("+payload+");("+pre_app+")("+json.dumps([KEY,BACKUP])+");")
        page.goto(urls[kind],wait_until="load")
        assert page.evaluate("k=>window.__a1read(k)",KEY)==raw
        assert page.evaluate("k=>window.__a1read(k)",BACKUP)==existing
        if kind=="app":
            assert ns["records"](page)==[a,b]
            ns["history"](page);ns["toggle"](page,a["id"]);edited=ns["records"](page)
        else:
            edited=copy.deepcopy([a,b]);edited[0]["episodes"][0]["manualStatus"]="never"
            page.evaluate("""([key,backup,original,oldBackup,edited])=>{
              if(original!==null&&oldBackup!==original)localStorage.setItem(backup,original);
              localStorage.setItem(key,edited);
            }""",[KEY,BACKUP,expected_backup,existing,ns["dumped"](edited)])
        row["expected"]=edited
        before=storage(page,kind);row["before"]=before
        row["save_match"]=json.loads(before["primary"])==edited
        row["backup_before_match"]=before["backup"]==expected_backup
        assert row["save_match"] and row["backup_before_match"],"write/readback failed before reload"
        if delay:page.wait_for_timeout(delay)
        start=time.monotonic()
        page.reload(wait_until="load")
        row["reload_elapsed_ms"]=round((time.monotonic()-start)*1000)
        after=storage(page,kind);row["after"]=after
        row["primary_match"]=after["primary"]==before["primary"]
        row["backup_match"]=after["backup"]==expected_backup
        row["pre_app_match"]=after["pre"]["primary"]==before["primary"]
        row["marker"]=after["marker"];row["writes_after"]=after["counts"]
        row["reverted_original"]=after["primary"]==raw
        actual=ns["records"](page) if kind=="app" else json.loads(after["primary"])
        row["actual"]=actual;row["records_match"]=actual==edited
        row["ok"]=all(row[k] for k in ("save_match","backup_before_match","primary_match","backup_match","pre_app_match","records_match"))
        if not row["ok"]:
            page.wait_for_timeout(300)
            row["late_match"]=page.evaluate("k=>window.__a1read(k)",KEY)==before["primary"]
    except Exception as e:
        row["exception"]=str(e);row["traceback"]=traceback.format_exc();row["ok"]=False
    finally:
        row["page_errors"]=errors;emit(row);ctx.close()
with tempfile.TemporaryDirectory(prefix="gallery-a1-origin-") as tmp:
    control_file=Path(tmp)/"control.html";control_file.write_bytes(control)
    server=None
    if origin=="http":
        server=ThreadingHTTPServer(("127.0.0.1",0),Handler)
        threading.Thread(target=server.serve_forever,daemon=True).start()
        base=f"http://127.0.0.1:{server.server_port}"
        urls={"app":base+"/app.html","control":base+"/control.html"}
    else:
        assert origin=="file"
        urls={"app":html.as_uri(),"control":control_file.as_uri()}
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            seed_page=browser.new_page();seed_page.goto(urls["app"],wait_until="load")
            seed=seed_page.evaluate("JSON.parse(JSON.stringify(whSeed))");seed_page.close()
            a=copy.deepcopy(seed[0]);a["id"]="audit-a";a["episodes"]=a["episodes"][:2];a["latestEpisode"]=a["episodes"][0]["n"]
            a["compatibleExtra"]={"retain":True};a["episodes"][0]["compatibleExtra"]="retain"
            b=copy.deepcopy(seed[1]);b["id"]="audit-b"
            for width in (1440,620):
                for label in ("valid","recovery","backup_already_exact"):
                    for delay in (0,250,6000):
                        for repeat in range(8):trial(browser,urls,"app",width,label,delay,repeat,a,b)
            for delay in (0,250,6000):
                for repeat in range(10):trial(browser,urls,"control",1440,"recovery",delay,repeat,a,b)
            browser.close()
    finally:
        if server:server.shutdown();server.server_close()
groups={}
for row in report["trials"]:
    key=f'{row["kind"]}/{row["label"]}/{row["delay_ms"]}'
    group=groups.setdefault(key,{"n":0,"fail":0,"pre_app_mismatch":0,"reverted_original":0,"exceptions":0,"page_errors":0})
    group["n"]+=1;group["fail"]+=not row["ok"]
    group["pre_app_mismatch"]+=row.get("pre_app_match") is False
    group["reverted_original"]+=row.get("reverted_original",False)
    group["exceptions"]+="exception" in row;group["page_errors"]+=bool(row["page_errors"])
report["summary"]=groups;out.write_text(json.dumps(report,ensure_ascii=False,indent=2))
print("A1 ORIGIN TIMING SUMMARY",mode,origin,json.dumps(groups),flush=True)
assert len(report["trials"])==174
