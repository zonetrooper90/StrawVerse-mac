#!/usr/bin/env python3
"""Approved contextual Search detail-return correction; no CSS or History changes."""
import hashlib,json,runpy
from pathlib import Path
SLUG="2026-11-15-anime-detail-search-return-verified-retry"
BASE_FULL="dd93f30c2bc170d08f43ceaa459205bd4b157e8d40d2df8f29e0133de10134d3"
BASE_LIGHT="76ede7481d40dfc3b0e674c4808de45df468818792e5d4dd937ae205cb953da3"
PATCHES=json.loads("[[\"gallery/src/js/19f-contextual-search.js\",\"12703ae676f1d9df0aa5e236cd3aa926bf2ec4d3\",[[\"let searchScrollBefore=0;\",\"let searchScrollBefore=0;\\nlet searchDetailReturn=null;\\n// Save only the detail route's context, not global preferences or catalogue data.\\nfunction captureSearchDetailReturn(){\\n const keys=['detailId','detailSeason','detailRelated','detailEpisode','detailAudio','detailEpisodeFilter','detailReturnHistory','detailReturnView','detailReturnScroll'];\\n const rail=screen.querySelector('#inline-installment-rail');\\n return {view:state.view,fields:Object.fromEntries(keys.map(key=>[key,state[key]])),\\n  scroll:workspace.scrollTop,railScroll:rail?.scrollLeft||0};\\n}\\nfunction restoreSearchDetail(saved){\\n transitionGalleryStage(()=>{\\n  // The catalogue is now invisible; no pending Discover scroll animation may\\n  // write into the detail route. The original Back destination is independent.\\n  finishDiscoverSearchRestore();\\n  state.view=saved.view;state.playback=null;\\n  Object.assign(state,saved.fields);updateActiveTab(state.view);\\n  // Pass the saved offset into reconstruction, before its first scroll write.\\n  render({searchRailScroll:saved.railScroll});\\n  workspace.scrollTo({top:saved.scroll,behavior:'instant'});\\n  configureHeaderSearchContext();updateTabScrollOverlay();\\n });\\n}\\n\",1],[\" if(state.detailId&&!searchingSettings)setView(state.view); // Return to the active tab, not always Discover.\",\" if(state.detailId&&!searchingSettings){\\n  const saved=captureSearchDetailReturn();\\n  // Open the ordinary contextual search only after the coordinated route midpoint.\\n  transitionGalleryStage(()=>{searchDetailReturn=saved;setView(saved.view);openInlineSearch();});\\n  return;\\n }\",1],[\" const searchingSettings=document.body.classList.contains('settings-view');\\n const hadQuery=Boolean(state.query.trim());\",\" const searchingSettings=document.body.classList.contains('settings-view');\\n const saved=restoreFocus&&!searchingSettings&&!whOpen&&!state.detailId&&!state.playback&&searchDetailReturn?.view===view?searchDetailReturn:null;\\n searchDetailReturn=null; // Result selection, tab changes and other navigation discard the origin.\\n const hadQuery=Boolean(state.query.trim());\",1],[\" if(restoreFocus)searchToggle.focus({preventScroll:true});\\n requestAnimationFrame(updateTabScrollOverlay);\\n}\",\" if(restoreFocus)searchToggle.focus({preventScroll:true});\\n if(saved)restoreSearchDetail(saved);\\n requestAnimationFrame(updateTabScrollOverlay);\\n}\",1]]],[\"gallery/src/js/11k-detail-and-download-entry-points.js\",\"2306e70e73f9e16f8a84e2a953dc35420a19d7ef\",[[\" const x=demo.find(t=>t.id===id);if(!x)return;\\n transitionGalleryStage(()=>{\",\" const x=demo.find(t=>t.id===id);if(!x)return;\\n if(searchOpen&&searchDetailReturn)closeInlineSearch(false);\\n transitionGalleryStage(()=>{\",1]]],[\"gallery/src/js/11i-core-render.js\",\"c8753322cc8081466961cb91285da9736938959d\",[[\"function render(){\",\"function render(options={}){\",1],[\"     rail.addEventListener('scroll',refreshInstallmentArrows,{passive:true});\",\"     // Search return alone must restore the exact offset, not the nearest snap point.\\n     // Disable snapping before any scroll write or observer/layout initialization.\\n     const searchRailScroll=options?.searchRailScroll;\\n     const restoringSearchRail=Number.isFinite(searchRailScroll);\\n     if(restoringSearchRail){\\n       rail.style.scrollSnapType='none';\\n       void rail.offsetWidth;\\n       rail.scrollTo({left:searchRailScroll,behavior:'instant'});\\n     }\\n     rail.addEventListener('scroll',refreshInstallmentArrows,{passive:true});\",1],[\"     rail.scrollLeft=priorRailScroll;\",\"     if(!restoringSearchRail)rail.scrollLeft=priorRailScroll;\\n     else refreshInstallmentArrows();\",1]]]]")
HOOK="\n# Mandatory Anime Details Search return and navigation isolation regression (both builds).\nsubprocess.run([sys.executable,str(Path(__file__).resolve().parents[1]/'audits'/'2026-11-15-anime-detail-search-return-synchronized-regression.py'),sys.argv[1]],check=True)\n"
def guard(path,sha):
    raw=Path(path).read_bytes()
    assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==sha,path
    return raw
def main():
    p=json.loads(Path("gallery/checkpoints/current.json").read_text())
    assert (p["folder"],p["sha256"],p["bytes"])==("2026-11-15-watch-history-animated-progress-retry",BASE_FULL,6922344)
    for name,digest in [("gallery/Gallery-current.html",BASE_FULL),("gallery/Gallery-development.html",BASE_LIGHT)]:
        assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==digest,name
    plan=runpy.run_path("gallery/tools/publisher-candidate.py")["plan"](SLUG)["include"]
    assert len(plan)==4 and {(g["kind"],g["mode"]) for g in plan}=={("regression","full"),("regression","lightweight"),("assets","both"),("comparison","both")},plan
    guard("gallery/changes/pending/2026-11-15-anime-detail-search-return.py","64dfe796724d935b55b72fd446343e39083e200b")
    guard("gallery/audits/2026-11-15-anime-detail-search-return-regression.py","5a1e4b3bfb7f66b4cfa478c6d39684987a8fdd92")
    guard("gallery/changes/pending/2026-11-15-anime-detail-search-return-rail-retry.py","1ab3806c0b6b9bbd19212a7dee97244b4fbe2df7")
    guard("gallery/audits/2026-11-15-anime-detail-search-return-rail-retry-regression.py","b469c7ee3274a996252cef5c11dae7f35372dda7")
    guard("gallery/audits/2026-11-15-anime-detail-search-return-synchronized-regression.py","eec2ad5a9fd33c8dbbd3985e4fb9fb7357a1f053")
    guard("gallery/audits/2026-11-15-a1-watch-history-loopback-regression.py","16c6378a72880b1ba05cef87fdf8c3172ed82ee5")
    guard("gallery/audits/2026-11-15-a1-watch-history-resilience-regression.py","6d988f3e04e7637bae5e3f7649e02087004c88d4")
    for name,sha,replacements in PATCHES:
        raw=guard(name,sha)
        for old,new,count in replacements:
            old,new=old.encode(),new.encode()
            assert raw.count(old)==count,old
            raw=raw.replace(old,new)
        Path(name).write_bytes(raw)
    name="gallery/tests/test_history_row_maintenance.py"
    raw=guard(name,"b8ace0bb26c05ec8507a7e1795165580f39d1dc6")
    assert Path("gallery/audits/2026-11-15-anime-detail-search-return-synchronized-regression.py").is_file()
    assert Path("gallery/audits/"+SLUG+"-compare.py").is_file()
    Path(name).write_bytes(raw+HOOK.encode())
    print("PASS exact approved Search return patch and mandatory regression hook",flush=True)
if __name__=="__main__":main()
