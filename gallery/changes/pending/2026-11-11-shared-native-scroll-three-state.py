#!/usr/bin/env python3
"""Apply tested shared native-scrolling and watched-state tri-toggle diff to GitHub canonical HTML."""
from pathlib import Path
import base64,hashlib,subprocess,tempfile,zlib
p=Path("gallery/Gallery-current.html")
before=p.read_bytes()
assert len(before)==6950513 and hashlib.sha256(before).hexdigest()=="4f5d93335155cd56a47248fd19866d5f1ad69ce7a7435ca287ff8606651a9987", "STOP: authoritative GitHub HTML mismatch"
diff=zlib.decompress(base64.b64decode("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")).decode("utf-8")
assert diff.startswith("--- verified-github-baseline\n+++ trial\n"),"STOP: invalid patch"
diff=diff.replace("--- verified-github-baseline\n+++ trial\n","--- gallery/Gallery-current.html\n+++ gallery/Gallery-current.html\n",1)
with tempfile.NamedTemporaryFile("w",encoding="utf-8",delete=False) as t:
 t.write(diff)
 patch_name=t.name
try:
 subprocess.run(["patch","-p0","--batch","--forward","--fuzz=0","--no-backup-if-mismatch","-i",patch_name],check=True)
finally:
 Path(patch_name).unlink(missing_ok=True)
after=p.read_bytes()
assert len(after)==6951729 and hashlib.sha256(after).hexdigest()=="7f9922d18f2ddd8b61035f5d2a524d3482fa3df5ea84045cf75be12c004eff45","STOP: patched HTML differs from browser-tested trial"
tests=Path("gallery/tests/test_history_row_maintenance.py")
s=tests.read_text(encoding="utf-8")
old="""    episode=first.locator('.wh-episode-row').first
    assert episode.count()==1 and episode.get_attribute('role') is None
    before=episode.get_attribute('aria-pressed')
    episode.locator('.wh-episode-number').click()
    assert episode.get_attribute('aria-pressed')!=before
    episode.focus()
    episode.press('Space')
    assert episode.get_attribute('aria-pressed')==before"""
new="""    episode=first.locator('.wh-episode-row').first
    assert episode.count()==1 and episode.get_attribute('role') is None
    before=episode.get_attribute('aria-pressed')
    next_status={'false':'mixed','mixed':'true','true':'false'}
    assert before in next_status,('Episode three-state baseline',before)
    episode.locator('.wh-episode-number').click()
    assert episode.get_attribute('aria-pressed')==next_status[before]
    episode.focus()
    episode.press('Space')
    assert episode.get_attribute('aria-pressed')==next_status[next_status[before]]
    episode.click()
    assert episode.get_attribute('aria-pressed')==before
    assert first.locator('.wh-episodes').count()==1"""
assert s.count(old)==1, "STOP: episode regression anchor changed"
s=s.replace(old,new)
start="    # Downloads deliberately retains its original scroll containment."
end='    page.locator(\'[data-view="discover"]\').first.click()'
assert s.count(start)==1 and s.count(end)==1, "STOP: Downloads regression anchors changed"
a=s.index(start);b=s.index(end,a)
new="""    # Shared native scroll behavior, including Downloads' approved two-way handoff.
    dl_inner=dl.locator('.sf-dl-viewport')
    dl_outer=page.locator('.tab-page[data-tab-page="downloads"]')
    assert dl_inner.get_attribute('class').split().count('gallery-episode-scroll')==1
    assert_episode_scroll_chains(dl_inner,dl_outer,'Downloads')
    def scroll_policy(el):
        return el.evaluate('(e)=>{const s=getComputedStyle(e);return [s.overflowY,s.overflowX,s.overscrollBehaviorY,s.overscrollBehaviorX]}')
    downloads_policy=scroll_policy(dl_inner)
    assert downloads_policy==['auto','hidden','auto','contain'],downloads_policy
"""
s=s[:a]+new+s[b:]
anchor="""    assert_episode_scroll_chains(history.locator('.wh-episode-scroll'),page.locator('.workspace'),'Watch History')"""
assert s.count(anchor)==1, "STOP: Watch History regression anchor changed"
extra="""    assert history.locator('.wh-episode-scroll').get_attribute('class').split().count('gallery-episode-scroll')==1
    assert scroll_policy(history.locator('.wh-episode-scroll'))==downloads_policy,'Both lists must share native scrolling'
    episode76=history.locator('[data-wh-episode="pkm:76"]')
    assert episode76.count()==1 and episode76.get_attribute('aria-pressed')=='false'
    original_seconds=page.evaluate('whRecords.find(r=>r.id==="pkm").episodes.find(e=>e.n===76).progressSeconds')
    episode76.click()
    assert episode76.get_attribute('aria-pressed')=='mixed' and episode76.locator('.wh-episode-label').inner_text()=='Partially watched'
    episode76.click()
    assert episode76.get_attribute('aria-pressed')=='true' and episode76.locator('.wh-episode-label').inner_text()=='Watched'
    episode76.click()
    assert episode76.get_attribute('aria-pressed')=='false' and episode76.locator('.wh-episode-label').inner_text()=='Not watched'
    assert page.evaluate('whRecords.find(r=>r.id==="pkm").episodes.find(e=>e.n===76).progressSeconds')==original_seconds
    episode76.click()
    assert episode76.get_attribute('aria-pressed')=='mixed'
    page.evaluate('whRender()')
    assert page.locator('[data-wh-row="pkm"] [data-wh-episode="pkm:76"]').get_attribute('aria-pressed')=='mixed','Partial status must survive a re-render'
"""
s=s.replace(anchor,anchor+"\n"+extra)
tests.write_text(s,encoding="utf-8")
print("Verified exact HTML build and updated common-scroll/three-state browser regressions")
