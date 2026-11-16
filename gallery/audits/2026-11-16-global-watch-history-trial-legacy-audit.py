#!/usr/bin/env python3
"""Run unchanged legacy-rail assertions using the explicit diagnostic URL."""
import hashlib,re,sys
from pathlib import Path
allowed={"2026-11-15-a1-watch-history-loopback-regression.py":"16c6378a72880b1ba05cef87fdf8c3172ed82ee5","2026-11-15-watch-history-animated-progress-retry-regression.py":"19050ab4e22c6cd2657e95992946d045e158c585","2026-11-15-anime-detail-search-return-synchronized-regression.py":"eec2ad5a9fd33c8dbbd3985e4fb9fb7357a1f053","2026-11-15-recently-watched-directional-stack-regression.py":"691b4af6bd9ab260ebc35f3c7006450605f49844"}
assert len(sys.argv)==3
name,html=sys.argv[1:]
assert name in allowed,name
path=Path(__file__).with_name(name)
raw=path.read_bytes()
assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==allowed[name],name
source=raw.decode("utf-8")
if name.endswith("loopback-regression.py"):
    marker='url=f"http://127.0.0.1:{server.server_port}/{html.name}"'
    assert source.count(marker)==1
    source=source.replace(marker,marker[:-1]+'#recently-watched-legacy"')
else:
    source,count=re.subn(r'(?m)^( +)(page)\.set_content\(',r'\1\2.goto("about:blank#recently-watched-legacy");\2.set_content(',source)
    assert count==(2 if name.endswith("directional-stack-regression.py") else 1),(name,count)
sys.argv=[str(path),html]
exec(compile(source,str(path),"exec"),{"__name__":"__main__","__file__":str(path)})
