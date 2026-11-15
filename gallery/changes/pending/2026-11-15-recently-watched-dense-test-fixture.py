#!/usr/bin/env python3
"""Approved opt-in dense sample history for Recently Watched visual testing."""
import hashlib,json
from pathlib import Path
SLUG="2026-11-15-recently-watched-dense-test-fixture"
PATCHES=json.loads("[[\"gallery/src/js/06-data-watch-history.js\",\"c3b1df0dfff2b2835344ce2c25c8566eeea66389\",[[\"];\\n\",\"];\\n\\n/* Opt-in dense sample history for Recently Watched visual testing only.\\n * Keep the ordinary seed and stored preview history unchanged. */\\nconst whRecentTestMode=location.hash==='#recently-watched-test';\\nfunction whRecentTestRecords(){\\n const extraTitles=['demo:long','demo:03','demo:04','demo:05','demo:06','demo:07','demo:08','demo:09','demo:10'].map(id=>demo.find(x=>x.id===id));\\n const extraSamples=['Amber Horizon','Cloudbound','Midnight Archive','Copper Moon','Ocean Echoes','Starfall Garden','Winter Lanterns'].map((name,i)=>({name,art:extraTitles[i].art,episodes:12,id:null}));\\n const extras=[...extraTitles,...extraSamples].map((x,i)=>{\\n  const id='recent-test-'+(i+1),last='2024-01-'+String(28-i).padStart(2,'0');\\n  const total=x.episodes,watched=i%3===0?total:Math.min(total-1,2+i%5);\\n  return {id,library:false,group:id,galleryId:x.id,installmentId:null,title:x.name,short:x.name.split(' ').slice(0,2).join(' '),cover:x.art,\\n   last,dates:[last],episodes:whMakeEpisodes(total,watched,watched<total?watched+1:null,watched<total?420:0)};\\n });\\n return [...whSeedRecords(),...extras];\\n}\\n\",1]]],[\"gallery/src/js/07a-watch-history.js\",\"764be14cef537e1c6e600c9e3018bb46120caa1d\",[[\"function whLoadRecords(){\\n try{whLoadedRaw=localStorage.getItem(whStorageKey);whStorageReadable=true;}\",\"function whLoadRecords(){\\n // The opt-in dense fixture neither reads nor writes the real preview history.\\n if(whRecentTestMode)return whRecentTestRecords();\\n try{whLoadedRaw=localStorage.getItem(whStorageKey);whStorageReadable=true;}\",1],[\"<div class=\\\"wh-recent-header\\\">Recently Watched</div>\",\"<div class=\\\"wh-recent-header\\\">Recently Watched${whRecentTestMode?' · Test data':''}</div>\",1]]]]")
def guard(path,sha):
    raw=Path(path).read_bytes()
    assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==sha,path
    return raw
def main():
    p=json.loads(Path("gallery/checkpoints/current.json").read_text())
    assert (p["folder"],p["sha256"],p["bytes"])==("2026-11-15-recently-watched-directional-stack","ef824f1289993fe22f9bfbd6fd5c4d2f95d815edd987e9493665b77c5a7c810f",6923816)
    for name,digest in [("gallery/Gallery-current.html","ef824f1289993fe22f9bfbd6fd5c4d2f95d815edd987e9493665b77c5a7c810f"),("gallery/Gallery-development.html","3cf6d91869f4269b947fdb028ed44215131c9c6e78d03ca0f6f69a7e222aac59")]:
        assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==digest,name
    for name,sha,replacements in PATCHES:
        raw=guard(name,sha)
        for old,new,count in replacements:
            old,new=old.encode(),new.encode()
            assert raw.count(old)==count,name
            raw=raw.replace(old,new,1)
        Path(name).write_bytes(raw)
    name="gallery/tests/test_history_row_maintenance.py"
    raw=guard(name,"1e94df158b21e59264fecabd8a09465b121b47d4")
    assert Path("gallery/audits/"+SLUG+"-regression.py").is_file()
    Path(name).write_bytes(raw+"\n# Mandatory dense Recently Watched opt-in fixture isolation and packing regression.\nsubprocess.run([sys.executable,str(Path(__file__).resolve().parents[1]/'audits'/'2026-11-15-recently-watched-dense-test-fixture-regression.py'),sys.argv[1]],check=True)\n".encode())
    print("PASS exact dense fixture patch and mandatory regression hook",flush=True)
if __name__=="__main__":main()
