#!/usr/bin/env python3
"""Apply the approved Watch History animation fix to verified GitHub working HTML."""
from pathlib import Path
import hashlib

p=Path("gallery/Gallery-current.html")
before=p.read_bytes()
assert len(before)==6948256 and hashlib.sha256(before).hexdigest()=="ca85c7184dc5feb958677fce208c6e6d48b19c1e97a2a9cdc3d8bf74bcebb530", "STOP: baseline mismatch"
s=before.decode("utf-8")
def one(a,b):
    global s
    assert s.count(a)==1, f"Unique replacement anchor missing: {a[:80]}"
    s=s.replace(a,b)
one("""#wh-root .wh-expand .icon{transition:transform .2s}
#wh-root .is-expanded .wh-expand .icon{transform:rotate(180deg)}
#wh-root .wh-episodes{border-top:1px solid var(--line);background:color-mix(in srgb,var(--raised) 34%,var(--surface));padding:13px 18px 15px 87px;animation:wh-expand .2s ease both}
@keyframes wh-expand{from{opacity:.45;transform:translateY(-4px)}to{opacity:1;transform:none}}""","""/* Match Downloads' 280ms grid-height expansion: panel remains mounted and reversible. */
#wh-root .wh-expand .icon{transition:transform .28s cubic-bezier(.22,.7,.25,1)}
#wh-root .is-expanded .wh-expand .icon{transform:rotate(180deg)}
#wh-root .wh-episodes{display:grid;grid-template-rows:0fr;background:color-mix(in srgb,var(--raised) 34%,var(--surface));transition:grid-template-rows .28s cubic-bezier(.22,.7,.25,1)}
#wh-root .wh-season.is-expanded .wh-episodes{grid-template-rows:1fr}
#wh-root .wh-episodes-inner{min-height:0;overflow:hidden;visibility:hidden;transition:visibility 0s linear .28s}
#wh-root .wh-season.is-expanded .wh-episodes-inner{visibility:visible;transition:visibility 0s}
#wh-root .wh-episodes-content{border-top:1px solid var(--line);padding:13px 18px 15px 87px}""")
one("#wh-root .wh-episodes{padding-left:14px}","#wh-root .wh-episodes-content{padding-left:14px}")
one("@media(prefers-reduced-motion:reduce){#wh-root .wh-episodes{animation:none}#wh-root .wh-inner-overlay{transition:none}}","@media(prefers-reduced-motion:reduce){#wh-root .wh-episodes,#wh-root .wh-expand .icon,#wh-root .wh-episodes-inner,#wh-root .wh-inner-overlay{transition:none!important}}")
start=s.index("function whRowMarkup(r){")
end=s.index("\nfunction whPageMarkup(){",start)
s=s[:start]+"""function whRowMarkup(r){const open=whExpanded.has(r.id);return `<section class="wh-season ${open?'is-expanded':''}" data-wh-row="${escapeHTML(r.id)}" aria-label="${escapeHTML(r.title)}">${whSummaryMarkup(r)}<div class="wh-episodes"><div class="wh-episodes-inner" ${open?'':'inert aria-hidden="true"'}><div class="wh-episodes-content"><div class="wh-episode-head"><strong>Episodes</strong><span>${whCount(r)} / ${r.episodes.length} watched</span></div><div class="wh-episode-shell" data-wh-shell="${escapeHTML(r.id)}"><div class="wh-episode-scroll" role="region" tabindex="0" aria-label="Scrollable episodes for ${escapeHTML(r.title)}">${r.episodes.map(ep=>whEpisodeMarkup(r,ep)).join('')}</div><div class="wh-inner-overlay" aria-hidden="true"><div class="wh-inner-thumb"></div></div></div><p class="wh-episode-hint">Mark or unmark individual episodes here. Saved playback position is kept separately.</p></div></div></div></section>`;}"""+s[end:]
toggler="""/* Expand/collapse in place so DOM, scroll position and animated height remain stable. */
function whToggleRow(id){
 const row=[...screen.querySelectorAll('[data-wh-row]')].find(el=>el.dataset.whRow===id);
 if(!row)return;
 const opening=!whExpanded.has(id);
 if(opening)whExpanded.add(id);else whExpanded.delete(id);
 row.classList.toggle('is-expanded',opening);
 const hit=row.querySelector('.wh-summary-hit');
 const record=whRecords.find(r=>r.id===id);
 hit.setAttribute('aria-expanded',String(opening));
 hit.setAttribute('aria-label',`${opening?'Collapse':'Expand'} episodes for ${record?.title||''}`);
 hit.title=opening?'Collapse episodes':'View episodes';
 const inner=row.querySelector('.wh-episodes-inner');
 inner.inert=!opening;
 if(opening)inner.removeAttribute('aria-hidden');else inner.setAttribute('aria-hidden','true');
 if(opening&&!whInnerScrollers.has(id)){
  const shell=row.querySelector('[data-wh-shell]');
  const area=shell.querySelector('.wh-episode-scroll');
  const scroller=whAttachInner(area,shell.querySelector('.wh-inner-overlay'));
  whInnerScrollers.set(id,scroller);
  const last=record&&whLastEpisode(record);
  const columns=matchMedia('(max-width:820px)').matches?1:2;
  if(record&&record.episodes.length>6*columns&&last)
   area.scrollTop=Math.max(0,(Math.floor((last.n-1)/columns)-2)*42);
 }
 if(opening)requestAnimationFrame(()=>{if(whExpanded.has(id))whInnerScrollers.get(id)?.update();});
 row.querySelector('.wh-episodes').addEventListener('transitionend',event=>{
  if(event.propertyName==='grid-template-rows')updateTabScrollOverlay();
 },{once:true});
 requestAnimationFrame(updateTabScrollOverlay);
}
"""
one("function whRender({keepScroll=true}={}){",toggler+"function whRender({keepScroll=true}={}){")
one("if(b.dataset.whExpand){const id=b.dataset.whExpand;whExpanded.has(id)?whExpanded.delete(id):whExpanded.add(id);whRender();return;}","if(b.dataset.whExpand){whToggleRow(b.dataset.whExpand);return;}")
out=s.encode("utf-8")
assert len(out)==6950393 and hashlib.sha256(out).hexdigest()=="c850b767a00c1749d56d52468e23c01d31afd27edc225f74b3ec9440b1db1717", "STOP: patched file does not match tested result"
p.write_bytes(out)

# Regression: the episodes now stay mounted when collapsed and animate in place.
t=Path("gallery/tests/test_history_row_maintenance.py")
test=t.read_text()
assert "assert first.locator('.wh-episodes').count()==0" in test
test=test.replace("assert first.locator('.wh-episodes').count()==0", """assert first.locator('.wh-episodes').count()==1
    assert first.locator('.wh-episodes-inner').get_attribute('inert') is not None
    page.evaluate('window.__historyPanel=document.querySelector(".wh-season .wh-episodes")')""")
assert "assert first.locator('.wh-summary-hit').get_attribute('aria-expanded')=='true'" in test
test=test.replace("assert first.locator('.wh-summary-hit').get_attribute('aria-expanded')=='true'", """assert first.locator('.wh-summary-hit').get_attribute('aria-expanded')=='true'
    assert first.locator('.wh-episodes-inner').get_attribute('inert') is None
    assert page.evaluate('window.__historyPanel===document.querySelector(".wh-season .wh-episodes")')
    opening_height=first.locator('.wh-episodes').evaluate('(el)=>el.getBoundingClientRect().height')
    page.wait_for_timeout(210)
    full_height=first.locator('.wh-episodes').evaluate('(el)=>el.getBoundingClientRect().height')
    assert 0 < opening_height < full_height, (opening_height,full_height)""")
assert "assert first.locator('.wh-anime-title').count()==1" in test
test=test.replace("assert first.locator('.wh-anime-title').count()==1", """first.locator('.wh-summary-hit').click()
    page.wait_for_timeout(330)
    assert first.locator('.wh-episodes').evaluate('(el)=>el.getBoundingClientRect().height')==0
    assert first.locator('.wh-episodes-inner').get_attribute('inert') is not None
    first.locator('.wh-summary-hit').click()
    page.wait_for_timeout(330)
    assert page.evaluate('window.__historyPanel===document.querySelector(".wh-season .wh-episodes")')
    assert first.locator('.wh-anime-title').count()==1""")
t.write_text(test)
print("GitHub source patched and checksum verified:",len(out),hashlib.sha256(out).hexdigest())
