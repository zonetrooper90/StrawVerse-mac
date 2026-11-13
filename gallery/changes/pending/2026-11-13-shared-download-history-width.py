#!/usr/bin/env python3
"""Approved shared content-width standard for Downloads and Watch History."""
import hashlib
import json
from pathlib import Path

p=json.loads(Path('gallery/checkpoints/current.json').read_text())
assert p['folder']=="2026-11-13-discover-search-collapse-syntax"
assert p['sha256']=="02c2268062fe7000b58d55794c27e01b546e8ee60ad72877a347d04bf98d0566"

def checked(path, blob_sha):
    data=path.read_bytes()
    actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert actual==blob_sha, (str(path),actual,blob_sha)
    return data.decode('utf-8')

changes = [
    ("gallery/src/styles/17-watch-history.css", "12266a8bce8ba7b097e41b546279e345692089ae", "#wh-root{max-width:1120px;margin:0 auto;min-width:0}\n", ""),
    ("gallery/src/styles/21-themed-downloads.css", "21f68d35277caa2194b3ceef6f41e8dad603754d", "body[data-theme] .sf-dl-list{display:grid;gap:13px;max-width:1220px;margin:0 auto}", "body[data-theme] .sf-dl-list{display:grid;gap:13px}"),
    ("gallery/src/styles/28-unified-headers-and-history-frame.css", "f32a02fa69935f1307be717ecfc9f82985acc19a", "/* Watch History: restore the approved full-width content frame. Settings uses\n   max-width:none inside the workspace; Watch History had retained an older\n   1120px clamp. Match Settings' available width and its existing workspace\n   gutters without changing season cards, controls, scroll behavior or headers. */\n#wh-root {\n  display:block;\n  box-sizing:border-box;\n  width:100%;\n  max-width:none;\n  margin-inline:0;\n  min-width:0;\n}", "/* Shared full-width list frame: Downloads and Watch History use the available\n   page content width and existing page gutters. Keep feature-specific display,\n   card styling, row spacing and scroll behavior in their own rules. */\n#wh-root,\nbody[data-theme] .sf-dl-list {\n  box-sizing:border-box;\n  width:100%;\n  max-width:none;\n  margin:0;\n  min-width:0;\n}\n#wh-root {display:block}"),
    ("gallery/tests/test_history_row_maintenance.py", "23fa99309779a4c2fff4e8bb3e59a3cbd64e2579", "    # Discover Search must collapse only the mounted Recently Watched wrapper,\n", "    # Shared content frame: compare actual outer card bounds with each other\n    # and with the respective page-header bounds, not just declared CSS widths.\n    def frame_bounds(page, header_selector, card_selector):\n        return page.evaluate('''({header,card}) => {\n            const bounds=e=>{const r=e.getBoundingClientRect();return [r.left,r.right,r.width]};\n            const rows=[...document.querySelectorAll(card)];\n            return {header:bounds(document.querySelector(header)),rows:rows.map(bounds)};\n        }''',{'header':header_selector,'card':card_selector})\n    def same_frame(a,b,label):\n        assert all(abs(x-y)<=1 for x,y in zip(a,b)),(label,a,b)\n    def stable_route(page):\n        page.wait_for_function('() => !galleryStageTransition && !galleryStageFadeInProgress',timeout=6000)\n        page.wait_for_timeout(80)\n    for width,height,motion in ((1600,950,'no-preference'),(1440,900,'reduce'),\n                                (1280,900,'reduce'),(1100,850,'reduce'),\n                                (751,850,'reduce'),(750,850,'reduce'),\n                                (620,850,'reduce'),(420,850,'reduce')):\n        width_page=browser.new_page(viewport={'width':width,'height':height},reduced_motion=motion)\n        width_errors=[]\n        width_page.on('pageerror',lambda exc: width_errors.append(str(exc)))\n        width_page.set_content(source,wait_until='domcontentloaded')\n        width_page.wait_for_selector('#wh-view-history')\n        width_page.locator('.tab[data-view=\"downloads\"]').click()\n        width_page.wait_for_function('() => state.view===\"downloads\" && !galleryStageTransition && !galleryStageFadeInProgress',timeout=6000)\n        # Primary tab slides are independent of secondary-stage transitions.\n        width_page.wait_for_timeout(600 if motion=='no-preference' else 100)\n        dl_frame=frame_bounds(width_page,'.page-header-downloads','.sf-dl-list .sf-dl-card')\n        assert dl_frame['rows'],('Downloads rows missing',width)\n        for row in dl_frame['rows']:\n            same_frame(row,dl_frame['header'],('Downloads/header',width))\n        width_page.locator('.tab[data-view=\"discover\"]').click()\n        width_page.wait_for_timeout(600 if motion=='no-preference' else 100)\n        width_page.locator('#wh-view-history').click()\n        width_page.wait_for_function('() => whOpen && document.querySelector(\"#wh-root\") && !galleryStageTransition && !galleryStageFadeInProgress',timeout=6000)\n        stable_route(width_page)\n        wh_frame=frame_bounds(width_page,'#wh-root > .wh-page-header','#wh-root .wh-season')\n        assert wh_frame['rows'],('Watch History rows missing',width)\n        for row in wh_frame['rows']:\n            same_frame(row,wh_frame['header'],('Watch History/header',width))\n        same_frame(dl_frame['header'],wh_frame['header'],('Shared header width',width))\n        same_frame(dl_frame['rows'][0],wh_frame['rows'][0],('Shared row width',width))\n        assert not width_errors,width_errors\n        print('PASS: shared Downloads/Watch History row bounds',width,motion,dl_frame['rows'][0],wh_frame['rows'][0])\n        width_page.close()\n    # Discover Search must collapse only the mounted Recently Watched wrapper,\n"),
]
updates=[]
for filename,sha,old,new in changes:
    path=Path(filename)
    text=checked(path,sha)
    assert text.count(old)==1, filename
    updates.append((path,text.replace(old,new,1)))
for path,text in updates:
    path.write_bytes(text.encode('utf-8'))
print('Applied shared full-width list frame; removed both legacy width clamps; added rendered-width regression.')
