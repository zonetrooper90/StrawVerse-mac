#!/usr/bin/env python3
"""Read-only reproduction of the failed Q2-B9 scroll assertion. Never publish."""
import hashlib,json,runpy,sys
from pathlib import Path
from playwright.sync_api import sync_playwright

def checked_script(path,sha):
    b=Path(path).read_bytes()
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==sha,path
    return runpy.run_path(path)
S=checked_script('gallery/changes/pending/2026-11-14-q2b9-search.py','203e195e537fb3b08164c6dfcb71ea7c16ce0880')
G=checked_script('gallery/audits/2026-11-14-q2b9-search-comparison.py','6a9c241bf2b3f4508aa3e185227a329af971598f')
EXPECTED={'full':'20720ad2357c910abab55d800ade47dc2dc9a03b43c78994e51ed55c4c9d8bec','lightweight':'75165538c7da503fb697a45738e89c7639f7399f79cfa1d2d8522922a4991c00'}
SCROLL=r"""scope=>{
 const e=(scope==='settings'||scope==='history')?workspace:tabPages[state.view];
 const shell=tabPages.discover.querySelector('.continue-shell');
 return {top:e.scrollTop,max:e.scrollHeight-e.clientHeight,scrollHeight:e.scrollHeight,clientHeight:e.clientHeight,
   saved:searchScrollBefore,shell:shell?.getBoundingClientRect().height,open:searchOpen,active:document.activeElement?.id,
   query:state.query};
}"""
HOOK=r"""scope=>{
 window.__q2closeNow=null;
 const button=document.querySelector('#header-search-close');
 const listener=e=>{
   if(!button.contains(e.target))return;
   document.removeEventListener('click',listener);
   const target=(scope==='settings'||scope==='history')?workspace:tabPages[state.view];
   const shell=tabPages.discover.querySelector('.continue-shell');
   window.__q2closeNow={top:target.scrollTop,max:target.scrollHeight-target.clientHeight,
     saved:searchScrollBefore,shell:shell?.getBoundingClientRect().height,open:searchOpen,active:document.activeElement?.id};
 };
 document.addEventListener('click',listener);
}"""
def scroll(page,scope):return page.evaluate(SCROLL,scope)
def measure(browser,source,baseline,active,motion,w,variant):
    page=browser.new_page(viewport={'width':w,'height':950},reduced_motion=motion)
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.set_content(source,wait_until='domcontentloaded')
    page.evaluate("""({baseline,active})=>{
      window.__q2baseline=baseline;window.__q2candidate=active;
      state.theme='ocean';document.body.dataset.theme='ocean';
      window.__searchShell=tabPages.discover.querySelector('.continue-shell');
    }""",{'baseline':baseline,'active':active})
    G['blur'](page)
    def compare(scope,stage):
        r=page.evaluate(G['COMPARE'])
        assert 'error' not in r,(variant,w,scope,stage,r)
    out={}
    for scope in ('discover','library','downloads','history','settings'):
        G['context'](page,scope)
        if scope=='library':page.locator('[data-tag="Watching"]').click();G['settle'](page)
        if scope=='downloads':page.locator('[data-download-filter="Completed"]').click();G['settle'](page)
        if scope=='history':page.locator('[data-wh-filter="progress"]').click();G['settle'](page)
        G['remember'](page,scope)
        ids=G['result_ids'](page,scope);q,wanted=G['query_for'](page,scope)
        if scope in ('discover','library','downloads'):
            page.evaluate("(s)=>{const p=tabPages[s];p.scrollTo({top:Math.min(100,p.scrollHeight-p.clientHeight),behavior:'instant'});}",scope)
            G['settle'](page)
        row={'before':scroll(page,scope)}
        G['opening'](page,keyboard=True)
        row['opened']=scroll(page,scope)
        compare(scope,'empty')
        G['fill'](page,q)
        assert wanted in G['result_ids'](page,scope),(scope,q,wanted)
        if scope=='library':
            page.locator('#header-search-input').press('ArrowDown')
            assert page.evaluate("document.activeElement.dataset.detail")==wanted
            page.keyboard.press('ArrowUp');assert page.evaluate("document.activeElement===searchInput")
        row['matching']=scroll(page,scope)
        compare(scope,'matching')
        G['fill'](page,'zzzz-no-gallery-match-zzzz')
        assert G['result_ids'](page,scope)==[]
        row['noMatch']=scroll(page,scope)
        compare(scope,'no match')
        G['clear'](page)
        row['cleared']=scroll(page,scope)
        compare(scope,'cleared')
        page.evaluate(HOOK,scope)
        G['close'](page,kind='button')
        row['immediateClose']=page.evaluate("window.__q2closeNow")
        assert row['immediateClose'] is not None
        row['settled']=scroll(page,scope)
        row['restored']=abs(row['before']['top']-row['settled']['top'])<=1
        assert G['result_ids'](page,scope)==ids,(scope,ids,G['result_ids'](page,scope))
        compare(scope,'closed')
        out[scope]=row
        print('SCROLL EVIDENCE',variant,w,scope,json.dumps(row,sort_keys=True),flush=True)
        G['depart'](page,scope)
    assert not errors,errors
    page.close()
    return out
def main(mode,motion):
    path,digest=S['FILES'][mode]
    original=Path(path).read_bytes()
    assert hashlib.sha256(original).hexdigest()==digest
    patched=S['transform'](original)
    assert hashlib.sha256(patched).hexdigest()==EXPECTED[mode]
    pre,base,post=G['unpack'](original);cp,css,ct=G['unpack'](patched)
    assert (pre,post)==(cp,ct)
    print('Verified exact accepted and previously prepared candidate hashes',mode,digest,EXPECTED[mode],flush=True)
    mismatches=[];existing=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
        for w in (1440,370):
            a=measure(browser,original.decode(),base.decode(),base.decode(),motion,w,'accepted')
            b=measure(browser,patched.decode(),base.decode(),css.decode(),motion,w,'candidate')
            for scope in a:
                x,y=a[scope],b[scope]
                # Compare identical input and settled result, not instantaneous
                # animation geometry measured at slightly different wall times.
                diffs=[]
                for phase in ('before','opened','matching','noMatch','cleared','settled'):
                    for prop in ('top','max','scrollHeight','clientHeight'):
                        if abs(x[phase][prop]-y[phase][prop])>1:diffs.append((phase,prop,x[phase][prop],y[phase][prop]))
                    for prop in ('open','query','active'):
                        if x[phase][prop]!=y[phase][prop]:diffs.append((phase,prop,x[phase][prop],y[phase][prop]))
                if x['restored']!=y['restored']:diffs.append(('restored',x['restored'],y['restored']))
                summary={'width':w,'scope':scope,'acceptedBefore':x['before']['top'],'acceptedAfter':x['settled']['top'],'candidateBefore':y['before']['top'],'candidateAfter':y['settled']['top'],'acceptedImmediate':x['immediateClose'],'candidateImmediate':y['immediateClose'],'differences':diffs}
                print('SCROLL COMPARISON',mode,motion,json.dumps(summary,sort_keys=True),flush=True)
                if diffs:mismatches.append(summary)
                elif not x['restored']:existing.append(summary)
        browser.close()
    print('DIAGNOSTIC RESULT',mode,motion,json.dumps({'mismatches':mismatches,'preExistingNonRestoration':existing},sort_keys=True),flush=True)
    assert not mismatches,'Behavior differs between accepted and candidate; do not retry automatically'
if __name__=='__main__':main(*sys.argv[1:])
