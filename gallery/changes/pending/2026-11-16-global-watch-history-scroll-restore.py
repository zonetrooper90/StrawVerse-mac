#!/usr/bin/env python3
"""Approved History navigation trial, with explicit pre-hide scroll capture."""
import hashlib,runpy,json
from pathlib import Path
GUARDS={
    "gallery/changes/pending/2026-11-16-global-watch-history-trial-retry.py": "86605783e81c8055e3b0d7fcdd09cea7926ccf34",
    "gallery/audits/2026-11-16-global-watch-history-trial-retry-dense-legacy-audit.py": "9032152d7f73d29e9c98f09b427951a8b3bbb28c",
    "gallery/audits/2026-11-16-global-watch-history-trial-retry-compare.py": "dd6dff25cdb282767a57a3b6a60340c9a2971ad7",
    "gallery/audits/2026-11-16-global-watch-history-trial-regression.py": "5a1259c814787d0f75b6b62a4dd534b136bfbe4d",
    "gallery/src/js/09-downloads-remainder.js": "49916f2a06fa6ff6b120c48a0bc35116b8bf27d2"
}
for name,expected in GUARDS.items():
    raw=Path(name).read_bytes()
    assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==expected,name
runpy.run_path("gallery/changes/pending/2026-11-16-global-watch-history-trial-retry.py",run_name="__main__")
path=Path("gallery/src/js/07a-watch-history.js")
source=path.read_text(encoding="utf-8")
PATCHES=json.loads("[[\"let whSuspended=null,whParentView='discover',whOriginDetail=null;\",\"let whSuspended=null,whParentView='discover',whOriginDetail=null,whOriginTabs=null;\"],[\"function whEnter(){\\n\",\"// Capture the real primary-page positions before hiding tabs or changing\\n// header height; hidden DOM and the expanded History viewport can clamp them.\\nfunction whCapturePrimaryScroll(){\\n if(tabPagesViewport.hidden||!workspace.classList.contains('tab-pages-visible'))return null;\\n captureDownloadScroll();\\n return {tops:new Map(tabOrder.map(view=>[view,tabPages[view].scrollTop])),\\n  libraryRail:tabPages.library.querySelector('.tagbar')?.scrollLeft||0,\\n  downloads:new Map(sfDownloadScrollPositions)};\\n}\\nfunction whRestorePrimaryScroll(saved){\\n if(!saved)return;\\n // render() has restored the normal header, all tab DOM and track position.\\n // Reapply only saved positions, at the fully transparent route midpoint.\\n const rail=tabPages.library.querySelector('.tagbar');\\n if(rail){rail.scrollLeft=saved.libraryRail;rail.galleryRefresh?.();}\\n for(const [id,top] of saved.downloads)sfDownloadScrollPositions.set(id,top);\\n restoreDownloadScroll();\\n for(const [view,top] of saved.tops)tabPages[view].scrollTo({top,behavior:'instant'});\\n}\\nfunction whEnter(){\\n\"],[\"  whOriginDetail=state.detailId?captureSearchDetailReturn():null;\\n  whParentView=state.view;\",\"  whOriginDetail=state.detailId?captureSearchDetailReturn():null;\\n  whOriginTabs=whOriginDetail?null:whCapturePrimaryScroll();\\n  whParentView=state.view;\"],[\"  const origin=whOriginDetail;whOriginDetail=null;\",\"  const origin=whOriginDetail,primaryScroll=whOriginTabs;whOriginDetail=null;whOriginTabs=null;\"],[\"   }else{state.detailId=null;render();}\",\"   }else{state.detailId=null;render();whRestorePrimaryScroll(primaryScroll);}\"]]")
for old,new in PATCHES:
    assert source.count(old)==1,old
    source=source.replace(old,new)
path.write_text(source,encoding="utf-8")
runner=Path("gallery/tests/test_history_row_maintenance.py")
raw=runner.read_text(encoding="utf-8")
hook="\n# Mandatory global Watch History primary scroll and nested Downloads restoration.\nsubprocess.run([sys.executable,str(Path(__file__).resolve().parents[1]/'audits'/'2026-11-16-global-watch-history-scroll-restore-regression.py'),sys.argv[1]],check=True)\n"
assert hook not in raw
assert Path("gallery/audits/2026-11-16-global-watch-history-scroll-restore-regression.py").is_file()
runner.write_text(raw+hook,encoding="utf-8")
print("PASS guarded original trial and primary scroll capture/restore correction",flush=True)
