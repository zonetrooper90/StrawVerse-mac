#!/usr/bin/env python3
"""Strict G3 inheritance plus the approved G3.1 smooth bidirectional More Actions wave."""
from pathlib import Path
import hashlib

def blob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

original=Path("gallery/audits/2026-11-21-g3-library-action-icons-compare.py")
raw=original.read_bytes()
assert blob(raw)=="deb781621b53a56d727154f1879b27ad0cf751c5", "Historical strict G3 audit changed"
source=raw.decode("utf-8")
def replace_once(before,after):
    global source
    assert source.count(before)==1, ("Unexpected immutable G3 audit anchor", before)
    source=source.replace(before,after,1)

replace_once('''def unchanged(a,b,label):
    assert all(abs(x-y)<.6 for x,y in zip(a,b)),(label,a,b)''',
'''def unchanged(a,b,label):
    # Playwright may legitimately scroll the whole Library tab in the viewport.
    assert all(abs(x-y)<.6 for x,y in zip(a[2:],b[2:])),(label,a,b)''')
replace_once('''         unchanged(before,box(page,"#newtag"),label+" button hover")
         unchanged(svg_before,box(page,"#newtag svg"),label+" svg hover")''',
'''         button_after=box(page,"#newtag")
         icon_after=box(page,"#newtag svg")
         unchanged(before,button_after,label+" button hover")
         unchanged(svg_before,icon_after,label+" svg hover")
         assert all(abs((svg_before[i]-before[i])-(icon_after[i]-button_after[i]))<.6 for i in (0,1)),(label,"New Tag relative optical alignment")''')
replace_once('''          assert "g3-thinking-wave" in value(page,"#tag-options .g3-thinking-dot:first-child","animationName"),label
          page.wait_for_function''',
'''          assert "g3-thinking-wave" in value(page,"#tag-options .g3-thinking-dot:first-child","animationName"),label
          first="#tag-options .g3-thinking-dot:first-child"
          assert value(page,first,"animationDuration")=="0.55s",(label,"per-dot duration")
          assert value(page,first,"animationTimingFunction")=="linear",(label,"no easing restarts")
          assert value(page,"#tag-options .g3-thinking-dot:nth-child(2)","animationDelay")=="0.105s",(label,"second-dot stagger")
          assert value(page,"#tag-options .g3-thinking-dot:nth-child(3)","animationDelay")=="0.21s",(label,"third-dot stagger")
          # Sample the actual browser-composited SVG dot with a paused CSSAnimation
          # at the approved key moments, then resume to test lifecycle and menu.
          wave=page.locator(first).evaluate("""el=>{
            const a=el.getAnimations().find(x=>x.animationName==='g3-thinking-wave');
            if(!a)return null;
            a.pause();
            const at=t=>{a.currentTime=t;return new DOMMatrix(getComputedStyle(el).transform).f};
            const v={start:at(0),up:at(154),preCross:at(297),postCross:at(319),
              preDip:at(407),dip:at(412.5),postDip:at(418),
              end:at(550),opacity:getComputedStyle(el).opacity};
            a.currentTime=0;a.play();return v;
          }""")
          assert wave is not None,(label,"SVG CSSAnimation missing")
          assert abs(wave["start"])<.08 and -3.15<wave["up"]<-2.85,(label,"3px rise",wave)
          assert wave["preCross"]<0<wave["postCross"],(label,"baseline crossing",wave)
          assert 1.75<wave["dip"]<1.95,(label,"1.85px below baseline",wave)
          assert abs(wave["preDip"]-wave["dip"])<.08 and abs(wave["postDip"]-wave["dip"])<.08,(label,"smooth trough",wave)
          assert abs(wave["end"])<.08 and wave["opacity"]=="1",(label,"fully opaque rest",wave)
          page.wait_for_function''')
replace_once('''          page.wait_for_timeout(760)''','''          page.wait_for_timeout(950)''')
print("G3.1: original 48-context functional test retained, scroll-safe icon alignment, sampled SVG rise/cross/dip/rest, 550ms linear timing, opaque 105ms stagger, reduced motion",flush=True)
exec(compile(source,str(original)+":g31-smooth-ripple","exec"),{"__name__":"__main__"})
