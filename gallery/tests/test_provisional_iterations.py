#!/usr/bin/env python3
"""Positive and negative fail-closed provisional iteration contract checks."""
import copy
import json
from pathlib import Path
import runpy
import tempfile

api=runpy.run_path('gallery/tools/provisional-iterations.py')
state=json.loads(Path('gallery/development/iterations.json').read_text())
stage2=json.loads(Path('gallery/development/provisional.json').read_text())
assert len(api['validate'](state,stage2))==1

def invalid(change):
    broken=copy.deepcopy(state)
    change(broken)
    try:
        api['validate'](broken,stage2)
    except (AssertionError,KeyError,TypeError,ValueError):
        return
    raise AssertionError('Unsafe provisional iteration state accepted')

invalid(lambda x:x.update(schema=2))
invalid(lambda x:x.update(status='released'))
invalid(lambda x:x['promotion'].update(status='approved'))
invalid(lambda x:x['baseline'].update(full_sha256='f'*64))
invalid(lambda x:x['iterations'].clear())
invalid(lambda x:x['iterations'][0].update(preview_script='../escape.py'))
invalid(lambda x:x['iterations'][0].update(preview_script_blob='a'*40))
invalid(lambda x:x['iterations'][0].update(lightweight_bytes=1))
invalid(lambda x:x['iterations'][0].update(lightweight_sha256='a'*64))
invalid(lambda x:x['iterations'][0].update(source_blobs={'gallery/assets/icon.png':'a'*40}))
invalid(lambda x:x['iterations'].append(copy.deepcopy(x['iterations'][0])))
invalid(lambda x:x['iterations'][0].update(slug='../../../oops'))

# Multi-step sequential contracts are allowed only with complete provenance.
future=copy.deepcopy(state['iterations'][0])
future['slug']='2026-12-01-future-approved-step'
future['preview_script']='gallery/changes/previews/'+future['slug']+'.py'
future['approved_script']='gallery/changes/pending/'+future['slug']+'.py'
more=copy.deepcopy(state)
more['iterations'].append(future)
assert len(api['validate'](more,stage2))==2

# A tampered Actions artifact must be rejected before installing Chromium.
with tempfile.TemporaryDirectory() as d:
    target=Path(d)/'preview.html'
    target.write_bytes(b'not-the-approved-HTML')
    mf=Path(d)/'iteration-manifest.json'
    mf.write_text(json.dumps({
        'status':'Development Preview — Not a Verified Release',
        'exact_commit':'a'*40,'promotion_authorized':False,
        'release_changed':False,'final_slug':state['iterations'][-1]['slug'],
        'lightweight_bytes':len(target.read_bytes()),
        'lightweight_sha256':api['sha256'](target.read_bytes()),
        'iterations':[]}))
    try:
        api['check_artifact'](target,mf,state,'a'*40)
    except AssertionError:
        pass
    else:
        raise AssertionError('Tampered preview passed')
print('PASS Stage 2 adoption, multiple-step schema, tamper and promotion rejection')
