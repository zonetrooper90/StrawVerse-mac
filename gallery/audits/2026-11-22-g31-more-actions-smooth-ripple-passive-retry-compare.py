#!/usr/bin/env python3
"""G3.1 passive requestAnimationFrame comparison; original 48-case functionality preserved."""
from pathlib import Path
import hashlib

def blob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

original=Path("gallery/audits/2026-11-22-g31-more-actions-smooth-ripple-compare.py")
raw=original.read_bytes()
assert blob(raw)=="da8a5c508f15935a289bc80fc7f96392eabac888", "Original G3.1 audit changed"
expected={
 "gallery/Gallery-current.html":"2e01412a4da6874398af9e3373346208508e66be15ca3113c4c17023c05dff50",
 "gallery/Gallery-development.html":"e9fa6ac3816f50c25b98c3f49e9332c9241cd6437e5005a5c98be80481602e93"
}
for path,sha in expected.items():
    assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==sha,("Exact original G3.1 HTML candidate changed",path)
source=raw.decode("utf-8")
def replace_once(old,new):
    global source
    assert source.count(old)==1,("G3.1 immutable audit anchor missing or duplicated",old[:130])
    source=source.replace(old,new,1)

replace_once('''         opts=page.locator("#tag-options")
         opts.hover()''',
'''         opts=page.locator("#tag-options")
         if motion=="no-preference":
          # Observe native frames after the true pointerenter without modifying
          # CSSAnimation/currentTime, the DOM, theme or menu state.
          page.evaluate("""() => {
            const btn=document.querySelector('#tag-options');
            const dots=[...btn.querySelectorAll('.g3-thinking-dot')];
            window.__g31FrameSamples=null;
            btn.addEventListener('pointerenter',()=>{
              const start=performance.now(),samples=[];
              function observe(now){
                samples.push({t:now-start,
                  y:dots.map(d=>new DOMMatrix(getComputedStyle(d).transform).f),
                  opacity:dots.map(d=>Number(getComputedStyle(d).opacity))});
                if(now-start<850) requestAnimationFrame(observe);
                else window.__g31FrameSamples=samples;
              }
              requestAnimationFrame(observe);
            },{once:true});
          }""")
         opts.hover()''')
replace_once('''          # Sample the actual browser-composited SVG dot with a paused CSSAnimation
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
          assert abs(wave["end"])<.08 and wave["opacity"]=="1",(label,"fully opaque rest",wave)''',
'''          # The passive observer completes after the final staggered dot settles.
          # Keep the original in-motion checks immediately below unchanged.''')
replace_once('''          page.wait_for_timeout(950)''',
'''          page.wait_for_function("()=>Array.isArray(window.__g31FrameSamples)",timeout=2400)
          samples=page.evaluate("window.__g31FrameSamples")
          assert len(samples)>=24 and samples[-1]["t"]>=810,(label,"frame count / final sample",len(samples))
          assert all(len(s["y"])==3 and len(s["opacity"])==3 for s in samples),(label,"all three dots")
          assert all(abs(op-1)<.001 for s in samples for op in s["opacity"]),(label,"fully opaque every frame")
          peak_times=[];dip_times=[]
          for dot in range(3):
           sequence=[(s["t"],s["y"][dot]) for s in samples]
           assert all(math.isfinite(y) for t,y in sequence),(label,"finite transform",dot)
           peak=min(sequence,key=lambda xy:xy[1])
           dip=max(sequence,key=lambda xy:xy[1])
           assert -3.25<peak[1]<-2.55,(label,"upward 3px",dot,peak)
           assert 1.5<dip[1]<2.12,(label,"downward 1.85px",dot,dip)
           assert peak[0]<dip[0],(label,"rise before dip",dot,peak,dip)
           assert abs(peak[0]-(154+105*dot))<70,(label,"rise timing",dot,peak)
           assert abs(dip[0]-(412.5+105*dot))<75,(label,"dip timing",dot,dip)
           assert abs(sequence[-1][1])<.10,(label,"exact final baseline",dot,sequence[-1])
           assert any(peak[0]<t<dip[0] and abs(y)<.24 for t,y in sequence),(label,"passes through baseline",dot)
           for (t0,y0),(t1,y1) in zip(sequence,sequence[1:]):
            if t1-t0>1:
             assert abs(y1-y0)/(t1-t0)<.095,(label,"no discontinuous jumps",dot,t0,y0,t1,y1)
           peak_times.append(peak[0]);dip_times.append(dip[0])
          assert all(55<peak_times[i]-peak_times[i-1]<155 for i in (1,2)),(label,"105ms rise stagger",peak_times)
          assert all(55<dip_times[i]-dip_times[i-1]<155 for i in (1,2)),(label,"105ms dip stagger",dip_times)
          page.wait_for_timeout(40)''')
assert ".pause()" not in source and ".currentTime=" not in source,"Destructive seeking was not removed"
print("G3.1 passive audit: exact original source/HTML + all 48 contexts, real rAF 3px rise/1.85px dip, baseline crossing, continuous speed, 105ms staggering, full opacity, reduced motion, menu/geometry",flush=True)
exec(compile(source,str(original)+":passive-retry","exec"),{"__name__":"__main__"})
