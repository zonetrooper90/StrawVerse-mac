#!/usr/bin/env python3
"""Approved selected-release auto-reveal; guarded exact source edits."""
import hashlib,json,runpy
from pathlib import Path
SLUG="2026-11-14-selected-release-auto-reveal"
BASE="9b35f5528b532bcf26b47ee0016f84103fb2152f"
FILES={"full":("gallery/Gallery-current.html","ea95ddd75d05367d840a00f9db54b7037841e10617a1d08488bc5ea05712618e"),
       "lightweight":("gallery/Gallery-development.html","0b222b797e48e3ebede7fb9a7cae1428632a03d2ae788d4073a9b61e59c7f54e")}
PATCHES=[
  [
    "gallery/src/styles/07-anime-detail-refinements.css",
    [
      "@media(max-width:560px){.inline-release-fade{--edge-width:54px}}",
      "@media(max-width:560px){.inline-release-fade{--edge-width:54px}}\n@media(max-width:460px){.inline-release-fade{--edge-width:min(54px,11.5%)}}"
    ]
  ],
  [
    "gallery/src/js/11a-anime-detail.js",
    [
      "/* Update only release-dependent sections; the rail itself never gets\n   destroyed, so its scroll position, pointer target and buttons survive. */",
      "/* Reveal a selected release inside the unobstructed part of the rail.\n   The arrow overlays disappear at their respective scroll boundaries. */\nfunction revealInlineInstallment(card,rail){\n const viewport=rail.closest('.inline-release-viewport');\n if(!viewport||!rail.isConnected||!rail.contains(card))return;\n const max=Math.max(0,rail.scrollWidth-rail.clientWidth);\n if(max<=3)return;\n const width=rail.clientWidth;\n const x=Math.max(0,Math.min(max,rail.scrollLeft));\n const rect=rail.getBoundingClientRect(),selected=card.getBoundingClientRect();\n const start=selected.left-rect.left+x;\n const end=selected.right-rect.left+x;\n const left=viewport.querySelector('.inline-release-fade-left').getBoundingClientRect().width;\n const right=viewport.querySelector('.inline-release-fade-right').getBoundingClientRect().width;\n // Each feasible interval accounts for the arrows that would be active\n // at the destination, not just those visible before scrolling.\n const intervals=[];\n // Integer destinations match Chromium's pixel scroll offsets. Also retain\n // the current subpixel position when it already exposes the entire card.\n for(const [lo,hi,l,r] of [[0,2,0,right],[3,max-3,left,right],[max-2,max,left,0]]){\n   intervals.push([Math.max(lo,end-width+r),Math.min(hi,max,start-l)]);\n }\n if(max<=4)intervals.push([Math.max(0,max-2,end-width),Math.min(2,start,max)]);\n const visibleLeft=x>2?left:0,visibleRight=x<max-2?right:0;\n if(start>=x+visibleLeft-0.01&&end<=x+width-visibleRight+0.01){\n   if(rail.style.scrollSnapType==='none')rail.scrollTo({left:x,behavior:'instant'});\n   return;\n }\n const targets=[];\n for(const [lo,hi] of intervals){\n   const min=Math.ceil(lo-0.01),limit=Math.floor(hi+0.01);\n   if(min<=limit)targets.push(Math.max(min,Math.min(limit,Math.round(x))));\n }\n if(!targets.length)return; // No feasible position: never alter card geometry here.\n const target=targets.reduce((a,b)=>Math.abs(b-x)<Math.abs(a-x)?b:a);\n if(Math.abs(target-x)<0.5)return;\n // Proximity snap may otherwise pull the chosen exact position back under\n // an arrow. Restore it only for the next intentional manual scroll.\n rail.style.scrollSnapType='none';\n rail.scrollTo({left:target,behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});\n}\nfunction restoreInstallmentSnap(rail){\n if(rail.style.scrollSnapType==='none'){\n   const x=rail.scrollLeft;\n   rail.scrollTo({left:x,behavior:'instant'});\n   rail.style.removeProperty('scroll-snap-type');\n }\n}\n/* Update only release-dependent sections; the rail itself never gets\n   destroyed, so its scroll position, pointer target and buttons survive. */"
    ],
    [
      " if(card.getAttribute('aria-current')==='true')return;\n const savedScroll=workspace.scrollTop;",
      " if(card.getAttribute('aria-current')==='true'){revealInlineInstallment(card,rail);return;}\n const savedScroll=workspace.scrollTop;"
    ],
    [
      "   section.replaceChildren(releaseNav,...Array.from(newSection.children).filter(node=>!node.classList.contains('inline-installments')));",
      "   // Keep the rail connected so native focus and horizontal position survive.\n   for(const child of Array.from(section.children))if(child!==releaseNav)child.remove();\n   section.append(...Array.from(newSection.children).filter(node=>!node.classList.contains('inline-installments')));"
    ],
    [
      " workspace.scrollTop=savedScroll;\n requestAnimationFrame(updateTabScrollOverlay);\n}\n\n// v27",
      " workspace.scrollTop=savedScroll;\n revealInlineInstallment(card,rail);\n requestAnimationFrame(updateTabScrollOverlay);\n}\n\n// v27"
    ]
  ],
  [
    "gallery/src/js/11i-core-render.js",
    [
      "     rail.addEventListener('scroll',refreshInstallmentArrows,{passive:true});",
      "     rail.addEventListener('scroll',refreshInstallmentArrows,{passive:true});\n     rail.addEventListener('wheel',event=>{if(event.deltaX||event.shiftKey&&event.deltaY)restoreInstallmentSnap(rail);},{passive:true});\n     rail.addEventListener('pointerdown',event=>{if(event.pointerType!=='mouse'||event.button===1)restoreInstallmentSnap(rail);},{passive:true});\n     rail.addEventListener('keydown',event=>{if(['ArrowLeft','ArrowRight','Home','End','PageUp','PageDown'].includes(event.key))restoreInstallmentSnap(rail);});"
    ],
    [
      "       if(target===undefined)return;\n       rail.scrollTo({left:Math.max(0,Math.min(target,limit)),behavior:",
      "       if(target===undefined)return;\n       restoreInstallmentSnap(rail);\n       rail.scrollTo({left:Math.max(0,Math.min(target,limit)),behavior:"
    ]
  ]
]
BLOBS={"gallery/src/styles/07-anime-detail-refinements.css":"76943d8224be75a6f92719f947d8834f9d732f5e","gallery/src/js/11a-anime-detail.js":"0b218ab5196695e504abc92d27f8f73ba851ea19","gallery/src/js/11i-core-render.js":"1c03640359569435563595859224b638d4b26d20"}
def replace(raw,pairs):
    for old,new in pairs:
        old,new=old.encode(),new.encode()
        assert raw.count(old)==1,old[:120]
        raw=raw.replace(old,new,1)
    return raw
def expected_html(raw):
    for path,*pairs in PATCHES:
        raw=replace(raw,pairs)
    return raw
def main():
    p=json.loads(Path("gallery/checkpoints/current.json").read_text())
    assert (p["folder"],p["sha256"],p["bytes"])==("2026-11-14-q2b6-release-arrow",FILES["full"][1],6902937)
    for path,digest in FILES.values():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,path
    plan=runpy.run_path("gallery/tools/publisher-candidate.py")["plan"](SLUG)["include"]
    assert len(plan)==7 and {g["mode"] for g in plan if g["kind"]=="comparison"}=={"full-normal","full-reduced","lightweight-normal","lightweight-reduced"},plan
    for name,*pairs in PATCHES:
        path=Path(name)
        raw=path.read_bytes()
        assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==BLOBS[name],name
        path.write_bytes(replace(raw,pairs))
    print("PASS: exact approved auto-reveal source edits",flush=True)
if __name__=="__main__":
    main()
