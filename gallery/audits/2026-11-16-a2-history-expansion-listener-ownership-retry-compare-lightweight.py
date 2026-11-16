#!/usr/bin/env python3
"""Exact A2.3 retry candidate and positive native-cancellation comparison gate."""
import hashlib,json,subprocess,sys,tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[2]
original=root/"gallery/audits/2026-11-16-a2-history-native-cancel-diagnostic.py"
raw=original.read_bytes()
assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()=="6c2a555dcf25fb8382a28b61199f31f46846cb82",original
expected={"Gallery-current.html":"6f558d22ec21047a978af0d262277c508366a37e6d3d63f8bf1952016aa33ae5","Gallery-development.html":"fccd6b1dae4595eef6ff201c1e30912376745240fd452f8ba3e121ec93b92060"}
for name,digest in expected.items():
    assert hashlib.sha256((root/"gallery"/name).read_bytes()).hexdigest()==digest,name
with tempfile.TemporaryDirectory() as tmp:
    out=Path(tmp)/"cancel.json"
    subprocess.run([sys.executable,str(original),"candidate","lightweight",str(root),str(out)],check=True)
    report=json.loads(out.read_text())
    summary=report["summary"]
    assert summary["cases"]==32 and not summary["harness_errors"] and not summary["page_errors"],summary
    # Original early-change scenario need not emit a cancel; it must reach
    # the correct final state and any native delivery must refresh exactly once.
    early=summary["by_kind"]["original"]
    assert early["completed"]==8 and all(v==1 for v in early["cancel_refreshes"]),early
    for kind in ("media-after-start","reversal","native-cancel"):
        result=summary["by_kind"][kind]
        assert result["completed"]==result["early_cancel"]==result["late_cancel"]==result["capture_cancel"]==8,result
        assert result["cancel_refreshes"]==[1]*8,result
    assert any(e["type"]=="transitioncancel" and e["property"]=="grid-template-rows" and e["trusted"] for e in report["control"]["events"]),report["control"]
print("PASS A2.3 byte-identical lightweight candidate: 32 native cancellation contexts, 24 positive cancellations, early-change state and browser-only control",flush=True)
