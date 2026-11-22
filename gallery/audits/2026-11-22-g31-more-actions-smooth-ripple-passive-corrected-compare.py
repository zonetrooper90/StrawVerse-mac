#!/usr/bin/env python3
"""G3.1 corrected passive comparison, preserving all 48 inherited G3 cases.

This audit does not edit Gallery source, generated HTML, checkpoints or history.
It replaces the TWO historical wrappers' literal substitutions against the
correct transformed G3 browser source. The originals are Git-blob guarded.
"""
import argparse
import ast
import hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
AUDITS=ROOT/"gallery/audits"
FILES=[
    ("2026-11-21-g3-library-action-icons-compare.py",
     "deb781621b53a56d727154f1879b27ad0cf751c5",0),
    ("2026-11-22-g31-more-actions-smooth-ripple-compare.py",
     "da8a5c508f15935a289bc80fc7f96392eabac888",4),
    ("2026-11-22-g31-more-actions-smooth-ripple-passive-retry-compare.py",
     "a76e72a6e8d0d4bc78675b7fed18b1bfe41ac9d3",3),
]
EXPECTED={
    "gallery/Gallery-current.html":
        "2e01412a4da6874398af9e3373346208508e66be15ca3113c4c17023c05dff50",
    "gallery/Gallery-development.html":
        "e9fa6ac3816f50c25b98c3f49e9332c9241cd6437e5005a5c98be80481602e93",
}

def require(test, message):
    if not test:
        raise AssertionError("G3.1 passive audit preflight: "+message)

def git_blob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

def literal_replacements(source,filename,count):
    tree=ast.parse(source,filename=filename)
    pairs=[]
    for statement in tree.body:
        if not (isinstance(statement,ast.Expr)
                and isinstance(statement.value,ast.Call)):
            continue
        call=statement.value
        if not (isinstance(call.func,ast.Name)
                and call.func.id=="replace_once"):
            continue
        require(not call.keywords and len(call.args)==2
                and all(isinstance(x,ast.Constant) and isinstance(x.value,str)
                        for x in call.args),
                "nonliteral replacement in historical wrapper "+filename)
        pairs.append(tuple(x.value for x in call.args))
    require(len(pairs)==count,
            f"unexpected historical wrapper replacements: {filename}: {len(pairs)}")
    return pairs

def materialize():
    verified=[]
    for filename,expected,n in FILES:
        raw=(AUDITS/filename).read_bytes()
        require(git_blob(raw)==expected,"historical original changed: "+filename)
        verified.append((filename,raw.decode("utf-8"),n))
    source=verified[0][1]
    require("assert cases==48" in source,
            "original G3 complete 48-case gate absent")
    # The G3.1 wrapper's replacement anchors describe the inherited G3
    # *browser script*, not the wrapper file itself. Apply them to G3 first.
    for filename,raw,n in verified[1:]:
        for old,new in literal_replacements(raw,filename,n):
            require(source.count(old)==1,
                    "missing/ambiguous transformed G3 anchor: "+filename+" "+
                    repr(old[:110]))
            source=source.replace(old,new,1)
    # No CSSAnimation seeking/pause remains; use nondestructive real rAF
    # sampling. Retain all original menu, lifecycle, reduced-motion, geometry,
    # six-theme, two-width, two-build assertions.
    require(".pause()" not in source and ".currentTime=" not in source,
            "destructive CSSAnimation sampling remains")
    require(source.count("window.__g31FrameSamples")==4,
            "passive frame observer/capture not injected as expected")
    for preserved in ("assert cases==48","for motion in (\"no-preference\",\"reduce\")",
                      "for width in (1100,390):","for theme in THEMES:",
                      "opts.click()","page.mouse.move(0,0)","0.55s",
                      "0.105s","0.21s","105ms rise stagger",
                      "105ms dip stagger","no discontinuous jumps",
                      "fully opaque every frame","wave replay",
                      "menu geometry","second turn"):
        require(preserved in source,"historical requirement lost: "+preserved)
    compile(source,"G3.1 inherited browser comparison (passive corrected)","exec")
    return source

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preflight",action="store_true")
    args=parser.parse_args()
    source=materialize()
    sha=hashlib.sha256(source.encode("utf-8")).hexdigest()
    if args.preflight:
        print("PASS G3.1 exact historical anchors; complete 48-case inherited "
              "audit, passive rAF test; compiled SHA-256 "+sha,flush=True)
        return
    # Browser tests run from a separate temporary directory containing
    # *generated* exact-candidate HTML at gallery/Gallery-*.html. Never read
    # the tracked unchanged G3 release as a candidate.
    for path,expected in EXPECTED.items():
        candidate=Path(path).read_bytes()
        require(hashlib.sha256(candidate).hexdigest()==expected,
                "candidate HTML changed: "+path)
    print("PASS G3.1 exact original full/lightweight candidate hashes, "
          "passive rAF plus 48 inherited contexts; source "+sha,flush=True)
    exec(compile(source,"G3.1 inherited browser comparison (passive corrected)",
                 "exec"),{"__name__":"__main__"})

if __name__=="__main__":
    main()
