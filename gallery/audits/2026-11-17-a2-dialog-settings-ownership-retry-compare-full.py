#!/usr/bin/env python3
"""Exact A2.4 retry candidate hashes and positive precise attribution gate."""
import hashlib,json,subprocess,sys,tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[2]
original=root/"gallery/audits/2026-11-17-a2-settings-reveal-attribution-diagnostic.py"
raw=original.read_bytes()
assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()=="413e5b2b6aa7d81125e797166e5413a39fda7c88",original
for name,(size,digest) in json.loads("{\"Gallery-current.html\":[6939095,\"c52a8c8a8a75c1ae5187fbb577c0ea146a36db9d45aae97320d6638c598be009\"],\"Gallery-development.html\":[623405,\"54c69064ac691fa3b191a19741390a4efcd7f492f09cf91ca9ccb441671bded3\"]}").items():
    data=(root/"gallery"/name).read_bytes()
    assert len(data)==size and hashlib.sha256(data).hexdigest()==digest,name
with tempfile.TemporaryDirectory() as tmp:
    out=Path(tmp)/"attribution.json"
    subprocess.run([sys.executable,str(original),"candidate","full",str(root),str(out)],check=True)
    report=json.loads(out.read_text());summary=report["summary"]
    assert summary["cases"]==16 and not summary["harness_errors"] and not summary["page_errors"],summary
    race=summary["race"];live=summary["live"]
    assert race["completed"]==race["actual_cancel"]==race["shared_deliveries"]==8,race
    assert race["legacy_closing_deliveries"]==race["shared_closing_deliveries"]==4,race
    assert not any(race[k] for k in ("actual_closing_deliveries","actual_deliveries","reveal_calls","stale_reveal_calls","stale_scroll_writes")),race
    assert live["completed"]==live["actual_deliveries"]==live["reveal_calls"]==8,live
    assert not any(live[k] for k in ("actual_cancel","actual_closing_deliveries","stale_reveal_calls","stale_scroll_writes")),live
    for row in report["cases"]:
        result=row["findings"];assert row["status"]=="completed" and not row["errors"],row
        if row["kind"]=="race":
            assert result["actual_cancel"]==result["shared_deliveries"]==1 and not result["actual_deliveries"] and not result["reveal_calls"],result
            assert result["owned_reveal_handle"]!=result["shared_overlay_handle"],result
            assert result["final_jump_frame"] is None and result["final_scroll_frame"] is None and result["final_old_highlight"] is False,result
        else:
            assert result["actual_deliveries"]==result["reveal_calls"]==1 and not result["stale_reveal_calls"],result
print("PASS A2.4 byte-identical full candidate: 8 owned cancellations, 8 positive live reveals, zero stale invocations/writes",flush=True)
