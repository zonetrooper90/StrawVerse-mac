#!/usr/bin/env python3
"""Fail-closed exact POST-PUSH published SHA identity for an advisory shadow."""
import argparse
from pathlib import Path
import re
import subprocess
REPO="zonetrooper90/StrawVerse-mac"
REF="refs/heads/gallery/development-clean"
SHA=re.compile(r"[0-9a-f]{40}\Z")
def require(ok,reason):
    if not ok: raise AssertionError("Gallery advisory published shadow: "+reason)
def validate(request,target,parent,branch_head,repo,ref,event):
    for key,value in (("request",request),("target",target),("parent",parent),("branch head",branch_head)):
        require(isinstance(value,str) and SHA.fullmatch(value),"invalid "+key)
    require(repo==REPO,"wrong repository")
    require(ref==REF,"wrong branch")
    require(event=="push","wrong triggering event")
    require(request!=target,"using request SHA instead of published SHA")
    require(parent==request,"published commit is not direct child of publisher request")
    require(branch_head==target,"published commit not branch HEAD")
    return target
def git(directory,*args):
    return subprocess.check_output(["git","-C",str(directory),*args],text=True).strip()
def verify(request,target,repo,ref,event,directory):
    directory=Path(directory).resolve()
    require(git(directory,"rev-parse","HEAD")==target,"wrong checkout SHA")
    ancestors=git(directory,"rev-list","--parents","-n","1","HEAD").split()
    require(len(ancestors)==2 and ancestors[0]==target,"published commit must have one parent")
    branch=git(directory,"ls-remote","origin",REF).split()
    require(len(branch)==2 and branch[1]==REF,"cannot verify remote branch")
    result=validate(request,target,ancestors[1],branch[0],repo,ref,event)
    require(git(directory,"status","--porcelain")=="","dirty checkout")
    print("PASS exact published SHA:",result,"; advisory only, no release.")
def main():
    p=argparse.ArgumentParser(description=__doc__)
    for arg in ("request","target","repository","ref","event"):
        p.add_argument("--"+arg,required=True)
    p.add_argument("--checkout",default=".")
    a=p.parse_args()
    verify(a.request,a.target,a.repository,a.ref,a.event,a.checkout)
if __name__=="__main__": main()
