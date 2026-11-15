#!/usr/bin/env python3
"""Run the immutable A1 suite on an isolated loopback HTTP origin.

Only the two initial navigation URLs change. Every existing case, assertion,
fixture, reload, storage fault and browser setting remains mandatory.
"""
import hashlib
import sys
import threading
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

def main():
    assert len(sys.argv)==2, "Usage: loopback-regression.py <exact Gallery HTML>"
    html=Path(sys.argv[1]).resolve()
    assert html.name in ("Gallery-current.html","Gallery-development.html"),html
    payload=html.read_bytes()
    assert payload,html
    digest=hashlib.sha256(payload).hexdigest()
    original=Path(__file__).with_name("2026-11-15-a1-watch-history-resilience-regression.py")
    raw=original.read_bytes()
    assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()=="6d988f3e04e7637bae5e3f7649e02087004c88d4","Historical A1 regression changed"
    source=raw.decode("utf-8")
    assert source.count("HTML.as_uri()")==2,"Unexpected A1 navigation structure"
    source=source.replace("HTML.as_uri()","A1_LOOPBACK_URL")
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path!="/"+html.name:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header("Content-Type","text/html; charset=utf-8")
            self.send_header("Content-Length",str(len(payload)))
            self.send_header("Cache-Control","no-store")
            self.end_headers()
            self.wfile.write(payload)
        def log_message(self,*args):
            pass
    with ThreadingHTTPServer(("127.0.0.1",0),Handler) as server:
        worker=threading.Thread(target=server.serve_forever,daemon=True)
        worker.start()
        url=f"http://127.0.0.1:{server.server_port}/{html.name}"
        print("A1 mandatory regression: exact HTML SHA-256",digest,"private loopback origin",url,flush=True)
        try:
            exec(compile(source,str(original),"exec"),{"__name__":"__main__","__file__":str(original),"A1_LOOPBACK_URL":url})
        finally:
            server.shutdown()
            worker.join()
    assert hashlib.sha256(html.read_bytes()).hexdigest()==digest,"HTML changed during test"
    print("PASS mandatory A1 loopback: immutable assertions, exact HTML unchanged",flush=True)

if __name__=="__main__":
    main()
