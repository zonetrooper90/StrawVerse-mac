#!/usr/bin/env python3
"""G2 narrowly approved source-only icon-motion patch for the guarded publisher."""
from pathlib import Path
import hashlib

def blob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

def apply(path, expected, result, old=None, replacement=None, append=None):
    p=Path(path)
    previous=p.read_bytes()
    if blob(previous)!=expected: raise RuntimeError("G2 baseline drift: "+path)
    if append is None:
        source=previous.decode("utf-8")
        if source.count(old)!=1: raise RuntimeError("G2 anchor not unique: "+path)
        raw=source.replace(old,replacement,1).encode("utf-8")
    else: raw=previous+append.encode("utf-8")
    if raw==previous or blob(raw)!=result: raise RuntimeError("G2 altered source mismatch: "+path)
    p.write_bytes(raw)
    if blob(p.read_bytes())!=result: raise RuntimeError("G2 readback mismatch: "+path)
    print("Verified G2 patch:",path,result,flush=True)

apply("gallery/src/js/19h-bootstrap.js","e25a6ad879fcd869cbbb87d2cb8937445b91253a","08ef24222d42057b7a4964943e6d497cf44c0c4b",old="for(const [name,ico] of [['discover','compass'],['library','library'],['downloads','download']])document.getElementById('nav-'+name).innerHTML=`<span class=\"tab-label-wrap\">${icon(ico,19)}<span>${name[0].toUpperCase()+name.slice(1)}</span></span>`;",replacement="const galleryNavSvg={\n discover:'<svg class=\"icon g2-nav-icon\" width=\"19\" height=\"19\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.7\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\"><circle cx=\"12\" cy=\"12\" r=\"9\"/><path class=\"g2-compass-needle\" d=\"m16 8-3 5-5 3 3-5 5-3z\"/></svg>',\n library:'<svg class=\"icon g2-nav-icon\" width=\"19\" height=\"19\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\"><path class=\"g2-library-line g2-library-first\" d=\"M6 5v14\"/><path class=\"g2-library-line g2-library-second\" d=\"M2 7v10\"/><rect height=\"18\" rx=\"2\" width=\"12\" x=\"10\" y=\"3\"/></svg>',\n downloads:'<svg class=\"icon g2-nav-icon\" width=\"19\" height=\"19\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.7\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\"><g class=\"g2-download-arrow\"><path d=\"M12 2v13m-5-5 5 5 5-5\"/></g><path d=\"M4 18v3h16v-3\"/></svg>'\n};\nfor(const name of ['discover','library','downloads'])document.getElementById('nav-'+name).innerHTML=`<span class=\"tab-label-wrap\">${galleryNavSvg[name]}<span>${name[0].toUpperCase()+name.slice(1)}</span></span>`;")
apply("gallery/src/styles/28-unified-headers-and-history-frame.css","e808e4caaa890008dc968e185116c8d952741085","7cc37fc911586b2cd700bd06dbe367a8956d3761",append="\n\n/* G2 — Approved hover/focus-only main-navigation motion. No tab geometry,\n   navigation, active highlight or global-toolbar changes. */\n#nav-discover .g2-compass-needle{\n transform-box:view-box;transform-origin:12px 12px;\n transform:rotate(0deg);transition:transform .78s cubic-bezier(.22,.72,.2,1);\n}\n#nav-discover:is(:hover,:focus-visible) .g2-compass-needle{transform:rotate(270deg)}\n#nav-downloads .g2-download-arrow{\n transform-box:view-box;transform-origin:12px 12px;\n transform:translateY(0);transition:transform .64s cubic-bezier(.22,.72,.2,1);\n}\n#nav-downloads:is(:hover,:focus-visible) .g2-download-arrow{transform:translateY(2.25px)}\n#nav-library .g2-library-line{transform:translateX(0);opacity:1}\n@keyframes g2-library-first-enter{\n from{transform:translateX(4px);opacity:0}\n to{transform:translateX(0);opacity:1}\n}\n@keyframes g2-library-second-enter{\n from{transform:translateX(2px);opacity:0}\n to{transform:translateX(0);opacity:1}\n}\n/* Exact supplied Horizontal End SVG, with an immediate first line followed\n   by a second line after 250ms. One-shot entrance, no invented reversal. */\n#nav-library:is(:hover,:focus-visible) .g2-library-first{\n animation:g2-library-first-enter .38s cubic-bezier(.22,.72,.2,1) 0s both;\n}\n#nav-library:is(:hover,:focus-visible) .g2-library-second{\n animation:g2-library-second-enter .38s cubic-bezier(.22,.72,.2,1) .25s both;\n}\n@media(prefers-reduced-motion:reduce){\n #nav-discover .g2-compass-needle,#nav-discover:is(:hover,:focus-visible) .g2-compass-needle,\n #nav-downloads .g2-download-arrow,#nav-downloads:is(:hover,:focus-visible) .g2-download-arrow{\n  transform:none!important;transition:none!important;\n }\n #nav-library:is(:hover,:focus-visible) .g2-library-line{animation:none!important}\n}\n")
print("G2 source patch complete; publisher owns builds and immutable checkpoint.",flush=True)
