#!/usr/bin/env python3
"""Read-only, fail-closed sequential Gallery lightweight iterations.

Never changes tracked release HTML, images, checkpoints, publisher or remote refs.
Run only inside a disposable exact-commit checkout; outputs live outside Git.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import runpy
import subprocess
import sys

STATE=Path('gallery/development/iterations.json')
STAGE2=Path('gallery/development/provisional.json')
POINTER=Path('gallery/checkpoints/current.json')
FULL=Path('gallery/Gallery-current.html')
LIGHT=Path('gallery/Gallery-development.html')
SHA=re.compile(r'[0-9a-f]{40}\Z')
H256=re.compile(r'[0-9a-f]{64}\Z')
SLUG=re.compile(r'20[0-9]{2}-[0-9]{2}-[0-9]{2}-[a-z0-9-]+\Z')

def require(value, reason):
    if not value:
        raise AssertionError('Gallery iteration preflight: '+reason)

def sha256(raw):
    return hashlib.sha256(raw).hexdigest()

def blob(raw):
    return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()

def git(*args):
    return subprocess.check_output(['git',*args],text=True).strip()

def run_python(*args):
    subprocess.run([sys.executable,'-B',*args],check=True)

def validate(state, stage2):
    require(isinstance(state,dict) and set(state)==
            {'schema','status','baseline','iterations','promotion'},'schema keys')
    require(state['schema']==1 and
            state['status']=='provisional-iterations-not-release','schema/status')
    require(isinstance(stage2,dict) and stage2.get('schema')==1 and
            stage2.get('status')=='provisional-development-not-release','Stage 2 baseline')
    require(state['baseline']==stage2['baseline'],'verified Stage 2 baseline changed')
    require(isinstance(state['promotion'],dict) and
            state['promotion']=={'status':'not-approved','promoted_commit':None},
            'release promotion not allowed')
    stages=state['iterations']
    require(isinstance(stages,list) and 1<=len(stages)<=16,
            '1 to 16 explicitly approved stages required')
    slugs=set()
    for index,step in enumerate(stages):
        require(isinstance(step,dict) and set(step)==
                {'slug','preview_script','preview_script_blob',
                 'approved_script','approved_script_blob','source_blobs',
                 'lightweight_sha256','lightweight_bytes'},'step keys')
        slug=step['slug']
        require(isinstance(slug,str) and SLUG.fullmatch(slug) and slug not in slugs,
                'unique approved date-prefixed slug')
        slugs.add(slug)
        require(step['preview_script']==f'gallery/changes/previews/{slug}.py' and
                step['approved_script']==f'gallery/changes/pending/{slug}.py',
                'immutable request script paths')
        require(all(isinstance(step[k],str) and SHA.fullmatch(step[k]) for k in
                    ('preview_script_blob','approved_script_blob')),'request blob SHAs')
        paths=step['source_blobs']
        require(isinstance(paths,dict) and 0<len(paths)<=128,
                'explicit cumulative source snapshot required')
        for path,value in paths.items():
            require(isinstance(path,str) and path.startswith('gallery/src/') and
                    '..' not in Path(path).parts and
                    Path(path).suffix in {'.css','.js','.html','.json'} and
                    isinstance(value,str) and SHA.fullmatch(value),
                    'source path and SHA')
        require(isinstance(step['lightweight_sha256'],str) and
                H256.fullmatch(step['lightweight_sha256']) and
                type(step['lightweight_bytes']) is int and step['lightweight_bytes']>0,
                'exact lightweight artifact size/hash')
        if index==0:
            first,candidate=stage2['request'],stage2['candidate']
            require(slug==first['slug'] and
                    step['preview_script']==first['file'] and
                    step['preview_script_blob']==first['git_blob_sha'] and
                    step['approved_script']==first['approved_request_file'] and
                    step['approved_script_blob']==first['approved_request_git_blob_sha'] and
                    paths==candidate['changed_source_git_blobs'] and
                    step['lightweight_sha256']==candidate['lightweight_sha256'] and
                    step['lightweight_bytes']==candidate['lightweight_bytes'],
                    'first iteration must reproduce independently verified Stage 2')
    return stages

def check_artifact(path,manifest_path,state,commit):
    """Validate exact candidate bytes before installing/running Chromium."""
    manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    stage=validate(state,json.loads(STAGE2.read_text(encoding='utf-8')))[-1]
    raw=path.read_bytes()
    require(manifest.get('status')=='Development Preview — Not a Verified Release' and
            manifest.get('exact_commit')==commit and
            manifest.get('promotion_authorized') is False and
            manifest.get('release_changed') is False and
            manifest.get('final_slug')==stage['slug'] and
            manifest.get('lightweight_bytes')==len(raw)==stage['lightweight_bytes'] and
            manifest.get('lightweight_sha256')==sha256(raw)==stage['lightweight_sha256'] and
            len(manifest.get('iterations',[]))==len(state['iterations']),
            'artifact provenance/hash differs from approved exact iteration stack')
    require(all(m.get('slug')==s['slug'] and
                m.get('lightweight_sha256')==s['lightweight_sha256']
                for m,s in zip(manifest['iterations'],state['iterations'])),
            'iteration manifest mismatch')
    return manifest

def generate(state,stage2,base,output):
    stages=validate(state,stage2)
    require(SHA.fullmatch(base) and git('rev-parse','HEAD')==base,
            'not exact GitHub commit')
    require(not git('status','--porcelain'),'worktree must start clean')
    require(not output.resolve().is_relative_to(Path.cwd().resolve()),
            'output must be outside repository')
    run_python('gallery/tools/restore-checkpoint.py','--verify-only')
    run_python('gallery/tools/build-gallery.py','--check')
    old_pointer,old_full,old_light=POINTER.read_bytes(),FULL.read_bytes(),LIGHT.read_bytes()
    baseline=state['baseline']
    ptr=json.loads(old_pointer)
    require(ptr['folder']==baseline['checkpoint_folder'] and
            ptr['sha256']==baseline['full_sha256'] and
            ptr['bytes']==baseline['full_bytes'] and
            sha256(old_full)==baseline['full_sha256'] and
            len(old_full)==baseline['full_bytes'] and
            sha256(old_light)==baseline['lightweight_sha256'] and
            len(old_light)==baseline['lightweight_bytes'],
            'immutable release baseline differs from verified Stage 2')
    builder=runpy.run_path('gallery/tools/build-gallery.py')
    preview_api=runpy.run_path('gallery/tools/lightweight-preview.py')
    records=[]
    prior_sha=sha256(old_light)
    for step in stages:
        for key,hash_key in (('preview_script','preview_script_blob'),
                             ('approved_script','approved_script_blob')):
            path=Path(step[key])
            require(path.is_file(),'approved script missing: '+str(path))
            raw=path.read_bytes()
            require(blob(raw)==step[hash_key],'immutable script changed: '+str(path))
            compile(raw,str(path),'exec')
        audit=Path('gallery/audits/'+step['slug']+'-compare.py')
        anchors=preview_api['preflight_audit'](audit) if audit.is_file() else 0
        runpy.run_path(step['preview_script'],run_name='__main__')
        changed=git('diff','--name-only','HEAD').splitlines()
        require(set(changed)==set(step['source_blobs']),
                'unexpected cumulative source change after '+step['slug'])
        require(not git('ls-files','--others','--exclude-standard'),
                'untracked files in candidate worktree')
        for name,expected in step['source_blobs'].items():
            require(blob(Path(name).read_bytes())==expected,
                    'candidate source blob mismatch: '+name)
        require(POINTER.read_bytes()==old_pointer and FULL.read_bytes()==old_full
                and LIGHT.read_bytes()==old_light,'tracked release or pointer modified')
        raw=builder['build']('development')
        this_sha=sha256(raw)
        require(this_sha==step['lightweight_sha256'] and
                len(raw)==step['lightweight_bytes'] and this_sha!=prior_sha,
                'preview hash differs from approved step')
        require(b'data:image/png;base64,' not in raw and
                b'__GALLERY_STYLE_BLOCK__' not in raw,
                'preview embeds artwork or unresolved token')
        prior_sha=this_sha
        records.append({'slug':step['slug'],'lightweight_sha256':this_sha,
                        'lightweight_bytes':len(raw),'source_paths':changed,
                        'static_audit_anchors':anchors})
    require(raw==builder['build']('development'),'preview is not deterministic')
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_bytes(raw)
    require(output.read_bytes()==raw,'preview readback mismatch')
    manifest={'status':'Development Preview — Not a Verified Release',
              'exact_commit':base,'final_slug':stages[-1]['slug'],
              'iterations':records,'lightweight_sha256':sha256(raw),
              'lightweight_bytes':len(raw),
              'baseline_checkpoint':baseline['checkpoint_folder'],
              'baseline_full_sha256':baseline['full_sha256'],
              'release_changed':False,'promotion_authorized':False}
    mp=output.parent/'iteration-manifest.json'
    mp.write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    check_artifact(output,mp,state,base)
    print('PASS sequential source iteration and fail-fast exact hashes:',
          json.dumps(manifest,sort_keys=True),flush=True)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base',required=True)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--check-artifact',type=Path)
    parser.add_argument('--manifest',type=Path)
    args=parser.parse_args()
    state=json.loads(STATE.read_text(encoding='utf-8'))
    stage2=json.loads(STAGE2.read_text(encoding='utf-8'))
    validate(state,stage2)
    require(SHA.fullmatch(args.base),'exact commit SHA required')
    if args.check_artifact:
        require(args.manifest and not args.output,'artifact verification arguments')
        check_artifact(args.check_artifact,args.manifest,state,args.base)
        print('PASS Stage 3 artifact proof matches exact-commit iteration stack',flush=True)
    else:
        require(args.output and not args.manifest,'output path required')
        generate(state,stage2,args.base,args.output)

if __name__=='__main__':
    main()
