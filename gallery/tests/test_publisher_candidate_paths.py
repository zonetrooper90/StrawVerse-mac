#!/usr/bin/env python3
"""Regression for NUL-delimited Git path parsing, including explicit pathspecs."""
import os
from pathlib import Path
import runpy
import subprocess
import tempfile

helper=Path(__file__).resolve().parents[1]/"tools/publisher-candidate.py"
names=runpy.run_path(str(helper))["names"]
def git(*args):
    return subprocess.check_output(["git",*args]).decode().strip()
with tempfile.TemporaryDirectory() as tmp:
    previous=Path.cwd()
    try:
        os.chdir(tmp)
        git("init","-q")
        git("config","user.name","Gallery fixture")
        git("config","user.email","gallery-fixture@example.invalid")
        Path("initial").write_text("baseline")
        git("add",".")
        git("commit","-qm","baseline")
        base=git("rev-parse","HEAD")
        request="gallery/changes/pending/2026-11-13-test.py"
        Path(request).parent.mkdir(parents=True)
        Path(request).write_text("pass\n")
        Path("unrelated").write_text("not a request")
        git("add",".")
        git("commit","-qm","request")
        head=git("rev-parse","HEAD")
        assert names("diff","--name-only","--diff-filter=AM",base,head,"--","gallery/changes/pending/")==[request]
        assert names("diff","--name-only","--diff-filter=A",base,head,"--",request)==[request]
        assert names("diff","--name-only",base,head,"--","missing")==[]
        Path("with space.txt").write_text("test")
        git("add","with space.txt")
        assert names("diff","--cached","--name-only","--no-renames")==["with space.txt"]
        assert names("diff","--cached","--name-only","--diff-filter=MD","--no-renames",head,"--","with space.txt")==[]
    finally:
        os.chdir(previous)
print("PASS: publisher Git path parsing, exact request and staged path filters")
