#!/usr/bin/env python3
"""Approved Discover-only search scroll restoration and mandatory regression smoke."""
import hashlib,json,runpy
from pathlib import Path
SLUG="2026-11-14-discover-search-scroll-restoration"
BASE="2a79cf86119f4e6c0324e65a51c61591496ee784"
FILES={"full":("gallery/Gallery-current.html","20720ad2357c910abab55d800ade47dc2dc9a03b43c78994e51ed55c4c9d8bec"),"lightweight":("gallery/Gallery-development.html","75165538c7da503fb697a45738e89c7639f7399f79cfa1d2d8522922a4991c00")}
JS="gallery/src/js/19f-contextual-search.js"
CSS="gallery/src/styles/09-search.css"
ASSET="gallery/tests/test_asset_build_modes.py"
JS_PATCHES=[["let searchScrollBefore=0;\n","let searchScrollBefore=0;\n// Suppress native anchoring only while Discover's retained shell expands.\nlet discoverSearchRestore=null;\nfunction finishDiscoverSearchRestore(){\n const restore=discoverSearchRestore;\n if(!restore)return;\n discoverSearchRestore=null;\n cancelAnimationFrame(restore.frame);\n restore.page.classList.remove('search-scroll-restoring');\n}\nfunction releaseDiscoverSearchScroll(){\n // User scrolling wins; keep anchoring suppressed until the expansion ends.\n if(discoverSearchRestore)discoverSearchRestore.hold=false;\n}\nfor(const type of ['wheel','touchmove','pointerdown']){\n tabPages.discover.addEventListener(type,releaseDiscoverSearchScroll,{passive:true});\n}\ntabScrollThumb.addEventListener('pointerdown',releaseDiscoverSearchScroll,{passive:true});\ndocument.addEventListener('keydown',event=>{\n if(!discoverSearchRestore||currentScrollSurface()!==tabPages.discover)return;\n if(!['ArrowDown','ArrowUp','PageDown','PageUp','Home','End',' '].includes(event.key))return;\n if(event.target.closest?.('input,textarea,select,[contenteditable=\"true\"]'))return;\n releaseDiscoverSearchScroll();\n});\nfunction beginDiscoverSearchRestore(top){\n finishDiscoverSearchRestore();\n const page=tabPages.discover,shell=page.querySelector('.continue-shell');\n if(!shell)return;\n page.classList.add('search-scroll-restoring');\n const restore={page,shell,top,hold:true,frame:0,quiet:0,start:performance.now()};\n discoverSearchRestore=restore;\n const step=()=>{\n  if(discoverSearchRestore!==restore)return;\n  if(searchOpen||currentScrollSurface()!==page||!shell.isConnected){\n   finishDiscoverSearchRestore();return;\n  }\n  // A saved near-bottom offset may not fit until the shell has expanded.\n  const available=Math.max(0,page.scrollHeight-page.clientHeight);\n  if(restore.hold){\n   const wanted=Math.min(restore.top,available);\n   if(Math.abs(page.scrollTop-wanted)>.5)page.scrollTop=wanted;\n  }\n  const moving=shell.getAnimations().some(a=>a.transitionProperty==='grid-template-rows'&&\n   (a.pending||a.playState==='running'));\n  restore.quiet=moving?0:restore.quiet+1;\n  if(restore.quiet>=2||performance.now()-restore.start>1500){\n   finishDiscoverSearchRestore();updateTabScrollOverlay();return;\n  }\n  restore.frame=requestAnimationFrame(step);\n };\n restore.frame=requestAnimationFrame(step);\n}\n"],[" if(state.playback||modalHost.firstChild)return;\n const searchingSettings="," if(state.playback||modalHost.firstChild)return;\n finishDiscoverSearchRestore();\n const searchingSettings="],["  if(view==='discover'){\n   tabPages.discover.classList.remove('search-scope-open');","  if(view==='discover'){\n   beginDiscoverSearchRestore(searchScrollBefore);\n   tabPages.discover.classList.remove('search-scope-open');"]]
CSS_PATCHES=[[".tab-page.search-scope-open .continue-shell{",".tab-page.search-scroll-restoring{overflow-anchor:none}\n.tab-page.search-scope-open .continue-shell{"]]
ASSET_PATCHES=[["print(\"Both modes: manual scene switching, synchronization, geometry, keyboard and reduced motion passed.\")\n","print(\"Both modes: manual scene switching, synchronization, geometry, keyboard and reduced motion passed.\")\n\n# Mandatory cross-build smoke for Discover search scroll restoration.\nimport subprocess,sys\nsubprocess.run([sys.executable,str(Path(__file__).with_name('test_discover_search_scroll.py')),'--smoke'],check=True)\n"]]
def patch(raw,pairs):
    for old,new in pairs:
        old,new=old.encode(),new.encode()
        assert raw.count(old)==1,old
        raw=raw.replace(old,new,1)
    return raw
def transform(raw):
    return patch(patch(raw,CSS_PATCHES),JS_PATCHES)
def main():
    p=json.loads(Path("gallery/checkpoints/current.json").read_text())
    assert (p["folder"],p["sha256"],p["bytes"])==("2026-11-14-q2b9-search-retry",FILES["full"][1],6905579)
    for name,digest in FILES.values():
        assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==digest,name
    plan=runpy.run_path("gallery/tools/publisher-candidate.py")["plan"](SLUG)["include"]
    assert len(plan)==7 and {g["mode"] for g in plan if g["kind"]=="comparison"}=={"full-normal","full-reduced","lightweight-normal","lightweight-reduced"},plan
    for name,sha,pairs in [(JS,"2598bc8df3e38a9f3b8f724b110962ef071663",JS_PATCHES),(CSS,"d53e1a96de65cc319d64a73485fe0e5d4ee575dd",CSS_PATCHES),(ASSET,"9c2d7b9f99bbfad78c957f035683ea0d8b16ddee",ASSET_PATCHES)]:
        path=Path(name);raw=path.read_bytes()
        assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==sha,name
        path.write_bytes(patch(raw,pairs))
    print("PASS: exact guarded Discover-only Search source changes and mandatory test hook",flush=True)
if __name__=="__main__":main()
