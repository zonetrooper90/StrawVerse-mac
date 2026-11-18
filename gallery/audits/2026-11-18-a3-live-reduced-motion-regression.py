#!/usr/bin/env python3
"""Mandatory A3.1 regression: unchanged verified diagnostic plus strict candidate settlement."""
import hashlib,json,sys,tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
original=root/"audits/2026-11-18-a3-live-motion-diagnostic-retry.py"
raw=original.read_bytes()
assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()=="f6148d2b063dc95f7e295530e3cf965759d733e7",original
html=Path(sys.argv[1]).resolve()
assert html in (root/"Gallery-current.html",root/"Gallery-development.html"),html
mode="full" if html.name=="Gallery-current.html" else "lightweight"
payload=html.read_bytes()
candidate_identity=(len(payload),hashlib.sha256(payload).hexdigest())
source=raw.decode("utf-8")
for old,new in json.loads("[[\"expected={\\\"full\\\":(6938816,\\\"e7ebd13cb49423448f3878e5f163d74840a7c5691f65708d036028cb8dd7650d\\\"),\\\"lightweight\\\":(623126,\\\"088a6d31cee139e9e7f7fad5f00cd54692a0192ac2d9616c83f3c313375d55e4\\\")}[mode]\\nassert (len(raw),hashlib.sha256(raw).hexdigest())==expected\",\"assert path.resolve()==expected_html\\nexpected=(len(raw),hashlib.sha256(raw).hexdigest())\\nassert expected==candidate_identity\"],[\"   inert:a.inert,railX:rail?.scrollLeft??null,railMax:rail?rail.scrollWidth-rail.clientWidth:null,\",\"   inert:a.inert,railX:rail?.scrollLeft??null,railMax:rail?rail.scrollWidth-rail.clientWidth:null,\\n   railOwned:activeInstallmentScroll?.rail===rail,railGoal:activeInstallmentScroll?.left??null,\"],[\"        row[\\\"status\\\"]=\\\"collected\\\"\",\"        # Strict requirements for the candidate; the original diagnostic remains intact.\\n        assert not f[\\\"railOwned\\\"] and not f[\\\"trackActive\\\"] and not f[\\\"playFrame\\\"] and not f[\\\"nextFrame\\\"] and not f[\\\"modalFrame\\\"] and not f[\\\"settingsFrame\\\"] and not f[\\\"searchActive\\\"] and not f[\\\"whMotion\\\"],f\\n        if kind==\\\"rail\\\":\\n            assert abs(f[\\\"railX\\\"]-(298 if width==1440 else 248))<2,f\\n        if policy==\\\"live\\\":\\n            v=row[\\\"findings\\\"]\\n            assert v[\\\"activeAfterTwoFrames\\\"]==0 and v[\\\"distinctValuesAfterTwoFrames\\\"]==1,(kind,v)\\n            assert len(later)>=2 and all(value(s,kind)==value(f,kind) for s in later),(kind,later)\\n            assert not v[\\\"replayActive\\\"] and v[\\\"replayValue\\\"]==v[\\\"valueFinal\\\"],(kind,v)\\n            if kind in (\\\"fade-out\\\",\\\"fade-in\\\"):\\n                assert all(not s[\\\"busy\\\"] and not s[\\\"stage\\\"] and not s[\\\"pending\\\"] and s[\\\"settings\\\"] and s[\\\"opacity\\\"]==1 for s in later),(kind,later)\\n                seq=[s[\\\"settings\\\"] for s in row[\\\"trace\\\"][\\\"frames\\\"]]\\n                assert sum(a!=b for a,b in zip(seq,seq[1:]))==1,(kind,seq)\\n            if kind==\\\"rail\\\":\\n                assert row[\\\"beforeSwitch\\\"][\\\"railOwned\\\"] and not any(s[\\\"railOwned\\\"] for s in later),row\\n        elif policy==\\\"reduce\\\":\\n            assert row[\\\"findings\\\"][\\\"activeReducedFrames\\\"]==0 and not row[\\\"findings\\\"][\\\"replayActive\\\"],row[\\\"findings\\\"]\\n            assert value(row[\\\"reenabled\\\"],kind)==value(f,kind),(kind,row[\\\"reenabled\\\"],f)\\n        row[\\\"status\\\"]=\\\"collected\\\"\"]]"):
    assert source.count(old)==1,(old,source.count(old))
    source=source.replace(old,new)
compiled=compile(source,str(original),"exec")
with tempfile.TemporaryDirectory(prefix="gallery-a31-") as temp:
    saved=sys.argv[:]
    try:
        for policy in ("live","reduce","normal"):
            sys.argv=[str(original),mode,policy,str(Path(temp)/(policy+".json"))]
            exec(compiled,{"__file__":str(original),"__name__":"__main__","expected_html":html,"candidate_identity":candidate_identity})
    finally:
        sys.argv=saved
print("PASS A3.1 strict 72 contexts for",mode,flush=True)
