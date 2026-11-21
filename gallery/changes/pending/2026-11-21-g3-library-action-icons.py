#!/usr/bin/env python3
"""G3 approved Library action SVG motion; checksum-guarded source-only publisher patch."""
from pathlib import Path
import hashlib

def gitblob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

def patch(path, expected, changes=(), extra=""):
    p=Path(path)
    prior=p.read_bytes()
    assert gitblob(prior)==expected, ("G3 authoritative source drift",path)
    src=prior.decode("utf-8")
    for before,after in changes:
        assert src.count(before)==1, ("G3 missing/ambiguous anchor",path,before)
        src=src.replace(before,after,1)
    updated=src.encode("utf-8")+extra.encode("utf-8")
    assert updated!=prior, ("G3 unchanged source",path)
    p.write_bytes(updated)
    assert p.read_bytes()==updated
    print("G3 patched",path,gitblob(updated),flush=True)

patch("gallery/src/js/07c-library.js",
      "7da17ba5f639a15bfbfb00fdb9c66dbbcccb8516",(
      ("icon('plus',17)",
       """icon('plus',17).replace('<path ','<g class="g3-plus-mark"><path ').replace('</svg>','</g></svg>')"""),
      ("icon('dots',19)",
       """icon('dots',19).replaceAll('<circle','<circle class="g3-thinking-dot"')"""),
      ))
patch("gallery/src/js/04h-tab-rendering-and-events.js",
      "ff98bd6b9a1b581a83edeee6578613431d86f99d",(
      (" on('openfolder',showFolderInfo);", """ // G3: bind only to this Library render's controls; no stale listeners on rerender.
 if(view==='library'){
  const plus=content.querySelector('#newtag');
  const mark=plus?.querySelector('.g3-plus-mark');
  if(mark){
   let turns=0;
   const turn=()=>{mark.style.transform='rotate('+(++turns*90)+'deg)';};
   plus.addEventListener('pointerenter',e=>{if(e.pointerType!=='touch')turn()});
   plus.addEventListener('focus',()=>{if(plus.matches(':focus-visible'))turn()});
  }
  const options=content.querySelector('#tag-options');
  if(options){
   const wave=()=>{
    if(options.getAttribute('aria-expanded')==='true' || window.matchMedia('(prefers-reduced-motion: reduce)').matches)return;
    options.classList.remove('g3-waving');
    void options.offsetWidth;
    options.classList.add('g3-waving');
   };
   options.addEventListener('pointerenter',e=>{if(e.pointerType!=='touch')wave()});
   options.addEventListener('focus',()=>{if(options.matches(':focus-visible'))wave()});
   options.addEventListener('click',()=>options.classList.remove('g3-waving'));
   const last=options.querySelector('.g3-thinking-dot:last-child');
   const clear=e=>{if(e.animationName==='g3-thinking-wave')options.classList.remove('g3-waving');};
   last?.addEventListener('animationend',clear);
   last?.addEventListener('animationcancel',clear);
  }
 }
 on('openfolder',showFolderInfo);"""),
      ))
patch("gallery/src/styles/28-unified-headers-and-history-frame.css",
      "7cc37fc911586b2cd700bd06dbe367a8956d3761",extra="""

/* G3 — approved Library action icon motion. Preserve original paths, button
   geometry, palette, focus, menu actions and all other tab/icon behavior. */
.page-header-library #newtag .g3-plus-mark{
 transform-box:view-box;transform-origin:12px 12px;transform:rotate(0deg);
 transition:transform .4s cubic-bezier(.22,.72,.2,1);
}
/* JS retains each +90deg target across hover exit (never reverses). */
.library-collection #tag-options.g3-waving .g3-thinking-dot{
 animation:g3-thinking-wave .45s cubic-bezier(.22,.72,.2,1) 1 both;
 transform-box:fill-box;transform-origin:center;
}
.library-collection #tag-options.g3-waving .g3-thinking-dot:nth-child(2){animation-delay:.105s}
.library-collection #tag-options.g3-waving .g3-thinking-dot:nth-child(3){animation-delay:.21s}
/* Only position changes; the three dots always remain fully opaque. */
@keyframes g3-thinking-wave{
 0%,100%{transform:translateY(0)}
 38%{transform:translateY(-3px)}
 64%{transform:translateY(-1px)}
}
@media(prefers-reduced-motion:reduce){
 .page-header-library #newtag .g3-plus-mark{transition:none!important}
 .library-collection #tag-options.g3-waving .g3-thinking-dot{animation:none!important}
}
""")
print("G3 source patch complete; guarded publisher owns full/lightweight builds and new archive.",flush=True)
