#!/usr/bin/env python3
"""Approved targeted search-collapse syntax correction and browser regression."""
import hashlib
import json
from pathlib import Path

ROOT=Path('gallery')
pointer=json.loads((ROOT/'checkpoints/current.json').read_text())
assert pointer['folder']=="2026-11-13-retired-anime-detail-css-retry"
assert pointer['sha256']=="1d10fb028639f3b4f04c9a9193bc5eeb0e4c25f7a5b7a71ec72de28ece56625f"

def checked(path, blob_sha):
    data=path.read_bytes()
    actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert actual==blob_sha, (str(path),actual,blob_sha)
    return data.decode('utf-8')

def replace_once(text,old,new):
    assert text.count(old)==1, 'Approved patch context missing or ambiguous'
    return text.replace(old,new,1)

css=ROOT/'src/styles/09-search.css'
test=ROOT/'tests/test_history_row_maintenance.py'
source_map=ROOT/'src/styles/README.md'
css_text=checked(css,"ad31a551c9b0b4650a80783f43ffd42019029bef")
test_text=checked(test,"eb2cca29846b1dd0f1c940b20aaa5ff87863e7ea")
map_text=checked(source_map,"1740da052f8071fdb307b7437b71e653263e99f1")
bad="  transition:grid-template-rows .42s cubic-bezier(.22,.72,.2,1),opacity .25s ease}\ntransition:grid-template-rows .42s cubic-bezier(.22,.72,.2,1),opacity .25s ease}\n.continue-shell .continue-clip{min-height:0;overflow:hidden}"
good="  transition:grid-template-rows .42s cubic-bezier(.22,.72,.2,1),opacity .25s ease}\n.continue-shell .continue-clip{min-height:0;overflow:hidden}"
new_css=replace_once(css_text,bad,good)
assert len(css_text.encode())-len(new_css.encode())==81
new_test=replace_once(test_text,"    page=browser.new_page(viewport={'width':1200,'height':850})\n","    # Discover Search must collapse only the mounted Recently Watched wrapper,\n    # clip its contents, move Explore upward, and restore it on close.\n    for width,height,motion in ((1440,900,'no-preference'),(620,750,'no-preference'),(1440,900,'reduce')):\n        search_page=browser.new_page(viewport={'width':width,'height':height},reduced_motion=motion)\n        search_errors=[]\n        search_page.on('pageerror',lambda exc: search_errors.append(str(exc)))\n        search_page.set_content(source,wait_until='domcontentloaded')\n        search_page.wait_for_selector('.sf-discover-page .continue-shell')\n        search_page.wait_for_timeout(200)\n        shell=search_page.locator('.sf-discover-page .continue-shell')\n        clip=shell.locator('.continue-clip')\n        assert clip.evaluate('(e)=>[getComputedStyle(e).minHeight,getComputedStyle(e).overflow]')==['0px','hidden'],('Search clip rule must apply',width,motion)\n        search_page.evaluate('window.__searchHistoryShell=document.querySelector(\".sf-discover-page .continue-shell\")')\n        def search_geometry():\n            return search_page.evaluate('''() => {\n                const shell=document.querySelector('.sf-discover-page .continue-shell');\n                const clip=shell.querySelector('.continue-clip');\n                const explore=document.querySelector('#sf-discover-explore');\n                const s=getComputedStyle(shell);\n                return {height:shell.getBoundingClientRect().height,clipHeight:clip.getBoundingClientRect().height,\n                    explore:explore.getBoundingClientRect().top,opacity:Number(s.opacity),\n                    pointerEvents:s.pointerEvents,transition:s.transitionProperty,\n                    sameNode:shell===window.__searchHistoryShell,open:searchOpen};\n            }''')\n        before=search_geometry()\n        assert before['height']>20 and before['opacity']==1 and not before['open'],before\n        if motion=='reduce':\n            assert before['transition']=='none',before\n        else:\n            assert 'grid-template-rows' in before['transition'],before\n        search_page.locator('#search').click()\n        search_page.wait_for_function('''() => {\n            const e=document.querySelector('.sf-discover-page .continue-shell');\n            return searchOpen && e.getBoundingClientRect().height<=1 && Number(getComputedStyle(e).opacity)<=0.01;\n        }''',timeout=5000)\n        collapsed=search_geometry()\n        assert collapsed['sameNode'] and collapsed['clipHeight']<=1 and collapsed['pointerEvents']=='none',collapsed\n        assert collapsed['explore']<before['explore']-20,(before,collapsed)\n        search_page.locator('#header-search-input').fill('anime')\n        assert search_geometry()['sameNode'],'Live search must not replace the Recently Watched wrapper'\n        search_page.locator('#header-search-input').press('Escape')\n        search_page.wait_for_function('''() => {\n            const e=document.querySelector('.sf-discover-page .continue-shell');\n            return !searchOpen && e.getBoundingClientRect().height>20 &&\n                Number(getComputedStyle(e).opacity)>=0.99 &&\n                !e.getAnimations().some(a=>a.playState==='running');\n        }''',timeout=5000)\n        restored=search_geometry()\n        assert restored['sameNode'] and abs(restored['height']-before['height'])<=2,(before,restored)\n        assert restored['explore']>collapsed['explore']+20 and restored['pointerEvents']!='none',restored\n        assert not search_errors,search_errors\n        print('PASS: Discover Search collapse/restore',width,motion,before['height'],collapsed['height'],restored['height'])\n        search_page.close()\n    page=browser.new_page(viewport={'width':1200,'height':850})\n")
new_map=replace_once(map_text,"Known pre-existing syntax anomaly: the original line 979 repeats a bare transition declaration with an unmatched closing brace after the `.continue-shell` rule. It is retained exactly in `09-search.css`; browser error recovery is unchanged. Investigate separately, including any effect on the subsequent selector, before proposing a fix. Existing empty conditional blocks are likewise retained.","Historical M2 anomaly (original line 979, `09-search.css:64` before correction): a duplicate bare transition declaration with an unmatched closing brace caused Chromium to discard the following `.continue-shell .continue-clip` rule. After the read-only Queue 1 investigation, the user approved removing only that malformed line. The correction restores clipping and minimum height for the Recently Watched search collapse; the original M2 byte/line table remains historical. Existing empty conditional blocks remain unchanged.")
css.write_bytes(new_css.encode())
test.write_bytes(new_test.encode())
source_map.write_bytes(new_map.encode())
print('Applied one approved malformed CSS line deletion; added targeted full-application regression and source-map note.')
