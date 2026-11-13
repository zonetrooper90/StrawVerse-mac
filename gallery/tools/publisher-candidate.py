#!/usr/bin/env python3
"""Prepare, transport, verify and stage an exact Gallery publisher candidate.

Run from a clean detached worktree of the exact approved request commit.
Only prepare executes the approved patch; consumers apply the same Git diff.
Never pushes or commits. Every validation is fail-closed.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import runpy
import subprocess
import sys

FULL="gallery/Gallery-current.html"
LIGHT="gallery/Gallery-development.html"
POINTER="gallery/checkpoints/current.json"
ALLOWED=[FULL,LIGHT,"gallery/src","gallery/tools/build-gallery.py",
         "gallery/tests/test_asset_build_modes.py",
         "gallery/tests/test_history_row_maintenance.py",
         "gallery/tests/test_player_settings_regression.py",
         "gallery/tests/test_source_assembly.py"]
SLUG=re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}-[a-z0-9-]+")
SHA=re.compile(r"[0-9a-f]{40}")
HISTORICAL_SHARD="2026-11-13-q2b1-downloads-declarations-retry"

def git(*args):
    return subprocess.check_output(["git",*args])
def run(*args):
    subprocess.run(args,check=True)
def python(path,*args):
    run(sys.executable,"-B",path,*args)
def digest(data):
    return hashlib.sha256(data).hexdigest()
def names(*args):
    # Options must precede the pathspec separator (--), never follow it.
    raw=git(args[0],"-z",*args[1:])
    assert not raw or raw.endswith(b"\0"),"Git did not return NUL-delimited paths"
    return [x.decode("utf-8") for x in raw.split(b"\0") if x]
def tree():
    return git("write-tree").decode().strip()
def assert_worktree_matches_index():
    assert not git("diff","--name-only"),"Unstaged tracked changes"
    assert not git("ls-files","--others","--exclude-standard"),"Unexpected untracked files"
def assert_allowed(paths):
    assert all(p in ALLOWED or p.startswith("gallery/src/") for p in paths),paths
def verify_assembly():
    builder=runpy.run_path("gallery/tools/build-gallery.py")
    assert builder["build"]("full")==Path(FULL).read_bytes()==builder["build"]("subtitle-preview")
    assert builder["build"]("development")==Path(LIGHT).read_bytes()
def verify_baseline():
    python("gallery/tools/restore-checkpoint.py","--verify-only")
    p=json.loads(Path(POINTER).read_text())
    raw=Path(FULL).read_bytes()
    assert len(raw)==p["bytes"] and digest(raw)==p["sha256"]
    python("gallery/tools/build-gallery.py","--check")
def verify_candidate(expected_tree):
    assert SHA.fullmatch(expected_tree)
    assert_worktree_matches_index()
    assert tree()==expected_tree,("Candidate tree mismatch",tree(),expected_tree)
    assert_allowed(names("diff","--cached","--name-only","--no-renames"))
    assert Path(POINTER).read_bytes()==git("show","HEAD:"+POINTER),"Baseline pointer changed"
    assert Path(FULL).read_bytes()!=git("show","HEAD:"+FULL),"Full HTML unchanged"
    verify_assembly()
    print("Verified exact candidate tree",expected_tree,"full",digest(Path(FULL).read_bytes()),"lightweight",digest(Path(LIGHT).read_bytes()),flush=True)
def plan(request):
    groups=[{"kind":"regression","mode":"full"},{"kind":"regression","mode":"lightweight"},{"kind":"assets","mode":"both"}]
    base=Path("gallery/audits")/request
    single=Path(str(base)+"-compare.py").is_file()
    pair=[Path(str(base)+"-compare-"+m+".py").is_file() for m in ("full","lightweight")]
    assert not any(pair) or all(pair),"Incomplete comparison shard pair"
    assert not (single and any(pair)),"Ambiguous comparison gate"
    if request==HISTORICAL_SHARD:
        assert single and not any(pair),"Historical comparison gate missing"
        groups += [{"kind":"historical-comparison","mode":m} for m in ("full","lightweight")]
    elif all(pair):
        groups += [{"kind":"comparison","mode":m} for m in ("full","lightweight")]
    elif single:
        groups += [{"kind":"comparison","mode":"both"}]
    elif request in ("2026-11-13-q2a-eight-redundant-css-rules","2026-11-13-q2b1-downloads-declarations"):
        raise AssertionError("Approved historical comparison missing")
    return {"include":groups}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("command",choices=("prepare","restore","verify","stage","test"))
    p.add_argument("--base",required=True)
    p.add_argument("--request")
    p.add_argument("--previous")
    p.add_argument("--patch",type=Path)
    p.add_argument("--sha256")
    p.add_argument("--tree")
    p.add_argument("--kind")
    p.add_argument("--mode")
    p.add_argument("--shard-tool")
    a=p.parse_args()
    assert SHA.fullmatch(a.base) and git("rev-parse","HEAD").decode().strip()==a.base,"Incorrect request base"
    if a.command=="prepare":
        assert SHA.fullmatch(a.previous)
        assert not git("status","--porcelain"),"Dirty baseline"
        requests=names("diff","--name-only","--diff-filter=AM",a.previous,a.base,"--","gallery/changes/pending/")
        assert len(requests)==1,requests
        path=requests[0]
        request=Path(path).stem
        assert SLUG.fullmatch(request) and path=="gallery/changes/pending/"+request+".py"
        assert names("diff","--name-only","--diff-filter=A",a.previous,a.base,"--",path)==[path]
        assert not Path("gallery/checkpoints",request).exists(),"Checkpoint already exists"
        verify_baseline()
        python(path)
        assert not git("status","--porcelain","--",FULL,LIGHT,"gallery/checkpoints","gallery/assets"),"Patch edited protected files"
        python("gallery/tools/build-gallery.py","--write-deliverables")
        assert Path(FULL).read_bytes()!=git("show","HEAD:"+FULL),"Byte-identical output; use infrastructure-only workflow"
        run("git","add","-A","--",*ALLOWED)
        candidate_tree=tree()
        verify_candidate(candidate_tree)
        patch=git("diff","--cached","--binary","--full-index","--no-renames","--no-ext-diff")
        assert patch
        a.patch.parent.mkdir(parents=True,exist_ok=True)
        a.patch.write_bytes(patch)
        sha=digest(patch)
        matrix=json.dumps(plan(request),separators=(",",":"))
        with open(os.environ["GITHUB_OUTPUT"],"a",encoding="utf-8") as out:
            out.write(f"request={request}\ntree={candidate_tree}\nsha256={sha}\nmatrix={matrix}\n")
        print("Prepared candidate",request,candidate_tree,sha,matrix,flush=True)
    elif a.command=="restore":
        assert not git("status","--porcelain"),"Dirty consumer baseline"
        assert re.fullmatch(r"[0-9a-f]{64}",a.sha256)
        assert digest(a.patch.read_bytes())==a.sha256,"Candidate patch digest mismatch"
        run("git","apply","--index","--binary",str(a.patch.resolve()))
        verify_candidate(a.tree)
    elif a.command=="verify":
        verify_candidate(a.tree)
    elif a.command=="test":
        assert SLUG.fullmatch(a.request)
        verify_candidate(a.tree)
        assert {"kind":a.kind,"mode":a.mode} in plan(a.request)["include"],"Unexpected test shard"
        if a.kind=="regression":
            html=FULL if a.mode=="full" else LIGHT
            for script in ("test_history_row_maintenance.py","test_transitions.py","test_coordinated_fades.py","test_player_settings_regression.py"):
                python("gallery/tests/"+script,html)
        elif a.kind=="assets":
            python("gallery/tests/test_asset_build_modes.py")
        elif a.kind=="historical-comparison":
            python(a.shard_tool,a.mode)
        elif a.kind=="comparison":
            suffix="" if a.mode=="both" else "-"+a.mode
            python("gallery/audits/"+a.request+"-compare"+suffix+".py")
        else:
            raise AssertionError("Unknown test group")
        verify_candidate(a.tree)
    elif a.command=="stage":
        assert SLUG.fullmatch(a.request)
        verify_candidate(a.tree)
        folder="gallery/checkpoints/"+a.request
        assert not Path(folder).exists()
        python("gallery/tools/stage-checkpoint.py","--input",FULL,"--id",a.request,"--status","delivered-for-user-testing")
        python("gallery/tools/restore-checkpoint.py","--verify-only")
        python("gallery/tools/build-gallery.py","--check")
        run("git","add","--",POINTER,folder)
        assert_worktree_matches_index()
        changed=names("diff","--cached","--name-only","--no-renames",a.tree)
        assert POINTER in changed and any(x.startswith(folder+"/") for x in changed)
        assert all(x==POINTER or x.startswith(folder+"/") for x in changed),changed
        assert names("diff","--cached","--name-only","--diff-filter=MD","--no-renames",a.tree,"--",folder)==[]
        run("git","diff","--cached","--check","--","gallery/tests/test_history_row_maintenance.py")
        print("Staged exact tested candidate plus only new immutable checkpoint",tree(),flush=True)
if __name__=="__main__":
    main()
