#!/usr/bin/env python3
"""Remove only the retired subtitle layout selector branches."""
import base64,gzip,hashlib,json,re
from pathlib import Path
p=Path("gallery/Gallery-current.html")
raw=p.read_bytes()
expected="12001b0ec4915bc3971380bc8c4b5348f1581743c08548f4e559ec3b169c242a"
assert len(raw)==6949666 and hashlib.sha256(raw).hexdigest()==expected,"STOP: baseline mismatch"
s=raw.decode("utf-8")
start=s.index("<style>")+len("<style>")
end=s.index("</style>",start)
css=s[start:end]
outside=s[:start]+s[end:]
names=("subtitle-workbench","subtitle-preview-card","subtitle-preview-top","subtitle-preview-caveat","subtitle-options-header","subtitle-settings-grid","subtitle-options-card","subtitle-experiment-preview-layout","subtitle-experiment-font-panel","subtitle-experiment-size-heading","subtitle-experiment-text-color-field","subtitle-experiment-style-group","subtitle-experiment-style-field","subtitle-experiment-effect-controls","subtitle-experiment-utilities")
for name in names:
    assert not re.search(r"(?<![\w-])"+re.escape(name)+r"(?![\w-])",outside),name
target=re.compile(r"\.(?:"+"|".join(map(re.escape,names))+r")(?![\w-])")
prefix=re.compile(r"(?:\s|/\*[\s\S]*?\*/)*")
counts=[0,0,0]
def remove(m):
    prelude,body=m.groups()
    leading=prefix.match(prelude).group()
    selector=prelude[len(leading):].strip()
    if not target.search(selector):
        return m.group()
    assert "/*" not in selector and not re.search(r":(?:not|is|where|has)\([^)]*"+target.pattern,selector),selector
    # The reviewed candidates contain no commas inside functional selectors.
    assert not re.search(r"\([^)]*,[^)]*\)|\[[^\]]*,[^\]]*\]",selector),selector
    branches=selector.split(",")
    keep=[b for b in branches if not target.search(b)]
    counts[0]+=1
    counts[1]+=len(branches)-len(keep)
    if not keep:
        return leading
    counts[2]+=1
    assert selector==".subtitle-stage,.subtitle-preview-card",selector
    return leading+ ",".join(keep)+"{"+body+"}"
cleaned=re.sub(r"([^{}]+)\{([^{}]*)\}",remove,css)
assert counts==[263,294,1],counts
# Only remove now-empty media/container blocks; keep historical comments and
# all declarations for live selectors in their original source order.
cleaned=re.sub(r"@(?:media|container)\b[^{};]*\{\s*\}","",cleaned)
assert not target.search(re.sub(r"/\*[\s\S]*?\*/","",cleaned))
out=(s[:start]+cleaned+s[end:]).encode("utf-8")
assert len(out)<len(raw)
p.write_bytes(out)
new_sha=hashlib.sha256(out).hexdigest()
print("Removed 262 entire rules and one branch from a shared rule;",len(raw)-len(out),"bytes; new SHA-256",new_sha)

# Compare this exact cleanup against the immutable predecessor in the existing
# browser suite (only for this build, not future intentional visual changes).
tests=Path("gallery/tests/test_player_settings_regression.py")
t=tests.read_text(encoding="utf-8")
addition=r'''
 # Exact before/after equivalence for the retired subtitle selector cleanup.
 import hashlib,base64,gzip,json
 if hashlib.sha256(html.encode("utf-8")).hexdigest()=="NEW_SHA":
  old_dir=Path(__file__).resolve().parents[1]/"checkpoints"/"2026-11-12-remove-prototype-preference-migrations"
  manifest=json.loads((old_dir/"manifest.json").read_text())
  chunks=[]
  for part in manifest["parts"]:
   data=(old_dir/part["file"]).read_bytes()
   assert len(data)==part["encoded_chars"] and hashlib.sha256(data).hexdigest()==part["sha256"]
   chunks.append(data)
  old_raw=gzip.decompress(base64.b64decode(b"".join(chunks),validate=True))
  assert len(old_raw)==6949666 and hashlib.sha256(old_raw).hexdigest()=="12001b0ec4915bc3971380bc8c4b5348f1581743c08548f4e559ec3b169c242a"
  old_html=old_raw.decode("utf-8")
  def subtitle_snapshot(source,width,theme):
   pg=browser.new_page(viewport={"width":width,"height":900},reduced_motion="reduce")
   errs=[]
   pg.on("pageerror",lambda e:errs.append(str(e)))
   try:
    pg.set_content(source,wait_until="domcontentloaded")
    pg.wait_for_timeout(240)
    settings(pg)
    pg.locator('[data-theme-button="'+theme+'"]').click()
    pg.locator('[data-settings-section="playback"]').click()
    pg.locator('[data-playback-tab="subtitles"]').click()
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(150)
    def snap():
     return pg.evaluate("""() => {
      const props=['display','visibility','position','width','height','minWidth','maxWidth','minHeight','maxHeight','padding','margin','gap','gridTemplateColumns','gridTemplateRows','alignItems','justifyContent','border','borderRadius','backgroundColor','backgroundImage','color','fontFamily','fontSize','fontWeight','lineHeight','boxShadow','textShadow','webkitTextStroke','overflowX','overflowY','transform'];
      const roots=[document.querySelector('#playback-subtitles-pane'),document.querySelector('.subtitle-preview-dialog'),document.querySelector('.gallery-color-popover')].filter(Boolean);
      return roots.map(root=>[root,...root.querySelectorAll('*')].map(e=>{
       const r=e.getBoundingClientRect(),c=getComputedStyle(e);
       return [e.tagName,e.id,e.getAttribute('class'),[r.x,r.y,r.width,r.height].map(v=>Math.round(v*10)/10),props.map(p=>c[p])];
      }));
     }""")
    states=[snap()]
    for effect in ("none","shadow","box","outline"):
     pg.locator('[data-subtitle-effect="'+effect+'"]').click()
     states.append(snap())
    pg.locator('[data-subtitle-text-color="custom"]').click()
    pg.wait_for_selector(".gallery-color-popover")
    states.append(snap())
    pg.locator(".gallery-color-close").click()
    if pg.locator("#subtitle-compact-preview").is_visible():
     pg.locator("#subtitle-compact-preview").click()
    else:
     pg.evaluate("showExpandedSubtitlePreview()")
    pg.wait_for_selector("#subtitle-expanded-stage")
    pg.wait_for_timeout(150)
    states.append(snap())
    assert not errs,errs
    return states
   finally:
    pg.close()
  for width in (1600,700):
   for theme in ("ocean","twilight","ember","slate","glacier","verdant"):
    before=subtitle_snapshot(old_html,width,theme)
    after=subtitle_snapshot(html,width,theme)
    check(before==after,"Exact subtitle computed layout/style equivalence: "+theme+" at "+str(width))
'''.replace("NEW_SHA",new_sha)
needle=" browser.close()\n"
assert t.count(needle)==1
t=t.replace(needle,addition+needle)
compile(t,str(tests),"exec")
tests.write_text(t,encoding="utf-8")
