#!/usr/bin/env python3
"""Guard and execute original Q2-B9 gate with only the confirmed scroll assertion corrected."""
import hashlib,runpy
from pathlib import Path
ORIGINAL="gallery/audits/2026-11-14-q2b9-search-comparison.py"
REQUEST="gallery/changes/pending/2026-11-14-q2b9-search.py"
EXPECTED={"full":"20720ad2357c910abab55d800ade47dc2dc9a03b43c78994e51ed55c4c9d8bec","lightweight":"75165538c7da503fb697a45738e89c7639f7399f79cfa1d2d8522922a4991c00"}
PATCHES=[
  [
    "def run(mode,motion):",
    "# Read only: measure the actual scroll surface and observe the real close click.\n# The earlier diagnostic established initial restoration followed by a 162px\n# shift while Recently Watched expands. Do not hard-code the shift or alter CSS.\ndef retry_scroll(page):\n    return page.evaluate(\"\"\"()=>{\n      const e=tabPages.discover,s=e.querySelector('.continue-shell');\n      return {top:e.scrollTop,max:e.scrollHeight-e.clientHeight,shell:s.getBoundingClientRect().height,\n        saved:searchScrollBefore,open:searchOpen,focus:document.activeElement?.id};\n    }\"\"\")\ndef retry_watch_close(page):\n    page.evaluate(\"\"\"()=>{\n      window.__retryImmediate=null;\n      const button=document.querySelector('#header-search-close');\n      const listener=e=>{\n        if(!button.contains(e.target))return;\n        document.removeEventListener('click',listener);\n        const p=tabPages.discover,s=p.querySelector('.continue-shell');\n        window.__retryImmediate={top:p.scrollTop,max:p.scrollHeight-p.clientHeight,\n          saved:searchScrollBefore,shell:s.getBoundingClientRect().height,open:searchOpen,focus:document.activeElement?.id};\n      };\n      document.addEventListener('click',listener);\n    }\"\"\")\ndef retry_close_evidence(page,before):\n    now=page.evaluate(\"window.__retryImmediate\")\n    after=retry_scroll(page)\n    assert now is not None and not now['open'] and now['focus']=='search',now\n    assert abs(now['saved']-before['top'])<=1 and abs(now['top']-before['top'])<=1,(before,now)\n    assert not after['open'] and after['focus']=='search' and abs(after['saved']-before['top'])<=1,(before,after)\n    assert abs(after['max']-before['max'])<=1 and abs(after['shell']-before['shell'])<=1,(before,after)\n    return {'before':before,'immediate':now,'after':after}\ndef retry_baseline_probe(make,theme,w,old_html,baseline):\n    pg,errs=make(theme,w,old_html)\n    pg.evaluate(\"(s)=>window.__q2candidate=s\",baseline)\n    def same(stage):\n        result=pg.evaluate(COMPARE)\n        assert 'error' not in result and result['nodes']>20,('accepted',theme,w,stage,result)\n    try:\n        context(pg,'discover');remember(pg,'discover')\n        ids=result_ids(pg,'discover');q,wanted=query_for(pg,'discover')\n        pg.evaluate(\"(s)=>{const p=tabPages[s];p.scrollTo({top:Math.min(100,p.scrollHeight-p.clientHeight),behavior:'instant'});}\",'discover')\n        settle(pg)\n        before=retry_scroll(pg)\n        assert before['top']>0,before\n        opening(pg,keyboard=True);same('empty')\n        fill(pg,q);assert wanted in result_ids(pg,'discover')\n        assert geo(pg)['sameShell'];same('matching')\n        fill(pg,'zzzz-no-gallery-match-zzzz');assert result_ids(pg,'discover')==[]\n        same('no match');clear(pg);same('cleared')\n        retry_watch_close(pg);close(pg,kind='button')\n        assert result_ids(pg,'discover')==ids\n        evidence=retry_close_evidence(pg,before)\n        same('closed')\n        assert not errs,errs\n        return evidence\n    finally:pg.close()\ndef retry_assert_parity(accepted,actual,theme,w):\n    for phase in ('before','after'):\n        for k in ('top','max','shell'):\n            assert abs(accepted[phase][k]-actual[phase][k])<=1,(theme,w,phase,k,accepted,actual)\n    for k in ('top','saved'):\n        assert abs(accepted['immediate'][k]-actual['immediate'][k])<=1,(theme,w,k,accepted,actual)\n    print('PASS: Discover scroll parity',theme,w,'accepted',accepted,'candidate',actual,flush=True)\n\ndef run(mode,motion):"
  ],
  [
    "    count=0;motion_count=0",
    "    count=0;motion_count=0;scroll_count=0"
  ],
  [
    "            for w in (1440,370):\n                page,errors=make(theme,w)",
    "            for w in (1440,370):\n                accepted_scroll=retry_baseline_probe(make,theme,w,old_html,baseline) if motion=='no-preference' else None\n                page,errors=make(theme,w)"
  ],
  [
    "                    opening(page,keyboard=True)\n                    if scope in ('library','downloads'):",
    "                    scroll_before=retry_scroll(page) if scope=='discover' else None\n                    opening(page,keyboard=True)\n                    if scope in ('library','downloads'):"
  ],
  [
    "                    close(page,kind='button');assert result_ids(page,scope)==ids,(scope,ids,result_ids(page,scope))\n                    if scope in ('discover','library','downloads','settings'):\n                        assert abs(page.evaluate(\"(s)=>s==='settings'?workspace.scrollTop:tabPages[state.view].scrollTop\",scope)-old_scroll)<=1",
    "                    if scope=='discover':retry_watch_close(page)\n                    close(page,kind='button');assert result_ids(page,scope)==ids,(scope,ids,result_ids(page,scope))\n                    if scope=='discover':\n                        actual_scroll=retry_close_evidence(page,scroll_before)\n                        if motion=='no-preference':\n                            assert accepted_scroll is not None\n                            retry_assert_parity(accepted_scroll,actual_scroll,theme,w)\n                            scroll_count+=1\n                        else:\n                            assert abs(actual_scroll['after']['top']-old_scroll)<=1,actual_scroll\n                    elif scope in ('library','downloads','settings'):\n                        actual=page.evaluate(\"(s)=>s==='settings'?workspace.scrollTop:tabPages[state.view].scrollTop\",scope)\n                        assert abs(actual-old_scroll)<=1,(theme,w,scope,old_scroll,actual)"
  ],
  [
    "    assert count==EXPECTED==624 and motion_count==24,(mode,motion,count,motion_count)",
    "    assert count==EXPECTED==624 and motion_count==24,(mode,motion,count,motion_count)\n    assert scroll_count==(12 if motion=='no-preference' else 0),(mode,motion,scroll_count)\n    print('PASS: Q2-B9 retry scroll checks',mode,motion,scroll_count,'paired Discover cases; immediate restore verified in all Discover cases',flush=True)"
  ]
]
def checked(path,sha):
    raw=Path(path).read_bytes()
    assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==sha,path
    return raw
def run(mode,motion):
    checked(REQUEST,"203e195e537fb3b08164c6dfcb71ea7c16ce0880")
    S=runpy.run_path(REQUEST)
    for key,(path,_) in S["FILES"].items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==EXPECTED[key],key
    source=checked(ORIGINAL,"6a9c241bf2b3f4508aa3e185227a329af971598f").decode()
    for old,new in PATCHES:
        assert source.count(old)==1,old
        source=source.replace(old,new,1)
    scope={"__name__":"q2b9_retry_guarded","__file__":ORIGINAL}
    exec(compile(source,ORIGINAL,"exec"),scope)
    scope["run"](mode,motion)
