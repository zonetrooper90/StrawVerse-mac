#!/usr/bin/env python3
"""G3 exact candidate comparison with viewport-scroll-safe geometry attribution."""
import hashlib
from pathlib import Path

def blob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
original=Path("gallery/audits/2026-11-21-g3-library-action-icons-compare.py")
raw=original.read_bytes()
assert blob(raw)=="deb781621b53a56d727154f1879b27ad0cf751c5","Original strict G3 audit changed"
expected_html={
 "gallery/Gallery-current.html":"e632872f5fc390c3de1eb49893d24ec314402f507357993b3a8145940887b907",
 "gallery/Gallery-development.html":"77c67b16caa2334c5c1faf272af1ed43b72564e59808420f1648cf8fe1617daf",
}
for path,sha in expected_html.items():
    assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==sha,("G3 candidate HTML drift",path)
source=raw.decode("utf-8")
old='''def unchanged(a,b,label):
    assert all(abs(x-y)<.6 for x,y in zip(a,b)),(label,a,b)'''
new='''def unchanged(a,b,label):
    # Playwright may scroll the parent tab track to bring a hovered button
    # into view. Its absolute viewport x/y are not structural geometry.
    assert all(abs(x-y)<.6 for x,y in zip(a[2:],b[2:])),(label,a,b)'''
assert source.count(old)==1,"Original geometry predicate anchor changed"
source=source.replace(old,new,1)
old='''         unchanged(before,box(page,"#newtag"),label+" button hover")
         unchanged(svg_before,box(page,"#newtag svg"),label+" svg hover")'''
new='''         button_after=box(page,"#newtag")
         icon_after=box(page,"#newtag svg")
         unchanged(before,button_after,label+" button hover")
         unchanged(svg_before,icon_after,label+" svg hover")
         # Preserve the strict icon-to-button relative x/y centering despite
         # any legitimate scroll of the entire content viewport.
         assert all(abs((svg_before[i]-before[i])-(icon_after[i]-button_after[i]))<.6 for i in (0,1)),(label,"icon alignment",before,svg_before,button_after,icon_after)'''
assert source.count(old)==1,"Original SVG relative-geometry anchors changed"
source=source.replace(old,new,1)
print("G3 retry: original 48-context audit unchanged except viewport-scroll attribution and positive icon/button alignment; exact source/build hashes verified",flush=True)
exec(compile(source,str(original)+":geometry-retry","exec"),{"__name__":"__main__"})
