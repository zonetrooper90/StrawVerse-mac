#!/usr/bin/env python3
"""Current verified-release Gallery lightweight preview contract; never publishes.

Historical G3.1 contracts remain independent. This new contract binds the
latest independently verified full release, an exact source-only patch, and a
byte-identical provisional preview. It fails closed if the release advances
without a separate reviewed baseline reconciliation.
"""
import argparse
import ast
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess

CONTRACT=Path("gallery/development/active-preview.json")
POINTER=Path("gallery/checkpoints/current.json")
FULL=Path("gallery/Gallery-current.html")
LIGHT=Path("gallery/Gallery-development.html")
APPROVALS=Path("gallery/APPROVED-DECISIONS.md")
SHA40=re.compile(r"[0-9a-f]{40}\Z")
SHA256=re.compile(r"[0-9a-f]{64}\Z")
SLUG=re.compile(r"20\d\d-\d\d-\d\d-[a-z0-9-]+\Z")

def must(value,reason):
 if not value: raise AssertionError("Gallery active preview: "+reason)

def digest(raw):return hashlib.sha256(raw).hexdigest()
def blob(raw):return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
def git(*args):
 return subprocess.check_output(["git",*args],text=True).strip()

def validate(state):
 must(type(state) is dict and set(state)=={"schema","status","baseline","mode","request","promotion","approved_scopes"},"state schema")
 must(state["schema"]==1 and state["status"]=="active-development-preview-not-release","state version")
 must(state["promotion"]=={"status":"not-authorized","published_commit":None},"no release promotion")
 base=state["baseline"]
 must(type(base) is dict and set(base)=={
  "verified_build_commit","checkpoint_folder","pointer_blob","full_blob","full_sha256",
  "full_bytes","lightweight_blob","lightweight_sha256","lightweight_bytes",
  "manifest_blob","archive_manifest_blob","integrity_run","browser_run"},"baseline schema")
 must(SHA40.fullmatch(base["verified_build_commit"]) and
      all(SHA40.fullmatch(base[x]) for x in
          ("pointer_blob","full_blob","lightweight_blob","manifest_blob","archive_manifest_blob")),
      "Git object identities")
 must(all(SHA256.fullmatch(base[x]) for x in ("full_sha256","lightweight_sha256")) and
      all(type(base[x]) is int and base[x]>0 for x in
          ("full_bytes","lightweight_bytes","integrity_run","browser_run")),
      "verified release checksums and workflow references")
 must(type(base["checkpoint_folder"]) is str and SLUG.fullmatch(base["checkpoint_folder"]),
      "immutable archive folder")
 scopes=state["approved_scopes"]
 must(type(scopes) is dict and 1<=len(scopes)<=12,"explicit reviewed preview scopes")
 for key,scope in scopes.items():
  must(type(key) is str and re.fullmatch(r"[a-z0-9-]+",key) and
       type(scope) is dict and set(scope)=={"approval_heading","slug_prefix","source_paths"},
       "approved scope schema")
  must(type(scope["approval_heading"]) is str and
       re.fullmatch(r"## 20\d\d-\d\d-\d\d — Approved [^\n]+",scope["approval_heading"]),
       "scope references an explicit user decision")
  must(type(scope["slug_prefix"]) is str and SLUG.fullmatch(scope["slug_prefix"]),
       "approved dated preview slug family")
  allowed=scope["source_paths"]
  must(type(allowed) is list and 1<=len(allowed)<=32 and
       len(allowed)==len(set(allowed)) and all(type(p) is str and
       p.startswith("gallery/src/") and ".." not in Path(p).parts and
       Path(p).suffix in (".html",".css",".js",".json") for p in allowed),
       "approved scoped source-only allowlist")
 mode,request=state["mode"],state["request"]
 must(mode in ("baseline-only","approved-source-only"),"known mode")
 if mode=="baseline-only":
  must(request is None,"baseline rehearsal cannot apply a source patch")
 else:
  must(type(request) is dict and set(request)=={
   "slug","scope","approval_heading","base_source_blobs","source_blobs","preview_sha256","preview_bytes"} or
       set(request)=={"slug","script_blob","scope","approval_heading","base_source_blobs",
                      "source_blobs","preview_sha256","preview_bytes"}),
   "explicit approved source request schema")
  must(type(request["slug"]) is str and SLUG.fullmatch(request["slug"]),"unique dated request")
  if "script_blob" in request:
   must(type(request["script_blob"]) is str and SHA40.fullmatch(request["script_blob"]),
        "immutable script SHA")
  must(type(request["approval_heading"]) is str and
       re.fullmatch(r"## 20\d\d-\d\d-\d\d — Approved [^\n]+",
                    request["approval_heading"]),"approved decision heading")
  chosen=scopes.get(request["scope"])
  must(chosen is not None and
       request["approval_heading"]==chosen["approval_heading"] and
       request["slug"].startswith(chosen["slug_prefix"]),
       "request must match one specifically user-approved work package")
  changes=request["source_blobs"]
  must(set(changes).issubset(chosen["source_paths"]),
       "request changes only approved source files")
  prior=request["base_source_blobs"]
  must(type(prior) is dict and set(prior)==set(changes) and all(
       type(value) is str and SHA40.fullmatch(value) for value in prior.values()),
       "exact pre-change authoritative source blobs")
  must(type(changes) is dict and 1<=len(changes)<=32 and all(
       type(path) is str and path.startswith("gallery/src/") and
       ".." not in Path(path).parts and Path(path).suffix in (".css",".js",".html",".json") and
       type(checksum) is str and SHA40.fullmatch(checksum)
       for path,checksum in changes.items()),"scoped source blob hashes")
  must(SHA256.fullmatch(request["preview_sha256"]) and
       type(request["preview_bytes"]) is int and request["preview_bytes"]>0,
       "pinned lightweight preview bytes and SHA-256")
 return base,request

def verify(state,artifact,manifest):
 base,request=validate(state)
 must(manifest.get("status")=="Development Preview — Not a Verified Release" and
      manifest.get("full_release_rebuilt_or_published") is False,
      "provisional artifact only")
 commit=git("rev-parse","HEAD")
 must(manifest.get("github_commit")==commit and
      subprocess.run(["git","merge-base","--is-ancestor",
                      base["verified_build_commit"],commit],check=False).returncode==0,
      "exact descendant of verified published build")
 ptr=json.loads(POINTER.read_text(encoding="utf-8"))
 must(ptr["folder"]==base["checkpoint_folder"] and
      ptr["sha256"]==base["full_sha256"] and ptr["bytes"]==base["full_bytes"] and
      blob(POINTER.read_bytes())==base["pointer_blob"],"unchanged immutable pointer")
 must(len(FULL.read_bytes())==base["full_bytes"] and
      digest(FULL.read_bytes())==base["full_sha256"],"unchanged full HTML")
 must(len(LIGHT.read_bytes())==base["lightweight_bytes"] and
      digest(LIGHT.read_bytes())==base["lightweight_sha256"],"unchanged tracked lightweight HTML")
 for path,key in (
  ("gallery/checkpoints/current.json","pointer_blob"),
  ("gallery/Gallery-current.html","full_blob"),
  ("gallery/Gallery-development.html","lightweight_blob"),
  ("gallery/src/build-manifest.json","manifest_blob"),
  (f"gallery/checkpoints/{base['checkpoint_folder']}/manifest.json","archive_manifest_blob")):
  must(git("rev-parse",f"HEAD:{path}")==base[key] and
       git("rev-parse",f"{base['verified_build_commit']}:{path}")==base[key],
       "published release identity drift: "+path)
 must(manifest.get("verified_full_baseline_sha256")==base["full_sha256"] and
      manifest.get("verified_full_baseline_bytes")==base["full_bytes"] and
      manifest.get("immutable_checkpoint")==base["checkpoint_folder"],
      "manifest release proof")
 data=artifact.read_bytes()
 must(manifest.get("lightweight_bytes")==len(data) and
      manifest.get("lightweight_sha256")==digest(data) and
      manifest.get("lightweight_filename")==artifact.name and
      b"data:image/png;base64," not in data and
      b"__GALLERY_STYLE_BLOCK__" not in data,
      "provisional HTML artifact checksum/contents")
 actual=set(filter(None,git("diff","--name-only","HEAD").splitlines()))
 must(not git("ls-files","--others","--exclude-standard"),
      "untracked files in temporary worktree")
 if request is None:
  must(manifest.get("request")=="baseline" and not actual and
       data==LIGHT.read_bytes() and
       manifest.get("request_sha256") is None,
       "baseline-only preview not identical to verified lightweight build")
 else:
  slug=request["slug"]
  script=Path("gallery/changes/previews")/(slug+".py")
  must(script.is_file() and
       git("rev-parse","HEAD:"+script.as_posix())==blob(script.read_bytes()),
       "script must match the exact immutable triggering Git commit")
  if "script_blob" in request:
   must(blob(script.read_bytes())==request["script_blob"],"immutable approved script blob")
  must(APPROVALS.read_text(encoding="utf-8").splitlines().count(
      request["approval_heading"])==1,"explicit user approval must be recorded once")
  must(manifest.get("request")==slug and
       manifest.get("request_sha256")==digest(script.read_bytes()) and
       actual==set(request["source_blobs"]),"source patch identity and scope")
  for path,expected in request["source_blobs"].items():
   must(git("rev-parse","HEAD:"+path)==request["base_source_blobs"][path],
        "unexpected previous source version: "+path)
   must(Path(path).is_file() and blob(Path(path).read_bytes())==expected,
        "changed source blob mismatch: "+path)
  must(len(data)==request["preview_bytes"] and
       digest(data)==request["preview_sha256"] and data!=LIGHT.read_bytes(),
       "immutable expected changed preview")
  must(manifest.get("changed_source_files")==sorted(actual),"preview changed-source manifest")
 print("PASS current-release source-only provisional preview contract:",
       json.dumps({"commit":commit,"mode":state["mode"],
                   "request":manifest["request"],"preview_bytes":len(data),
                   "preview_sha256":digest(data),"checkpoint":base["checkpoint_folder"],
                   "promotion_authorized":False},sort_keys=True),flush=True)

def embedded_request(slug):
 must(type(slug) is str and SLUG.fullmatch(slug),"dated request slug")
 script=Path("gallery/changes/previews")/(slug+".py")
 must(script.is_file(),"approved request script exists at immutable preview path")
 raw=script.read_bytes()
 must(git("rev-parse","HEAD:"+script.as_posix())==blob(raw),
      "request script bytes match exact triggering commit")
 tree=ast.parse(raw,filename=str(script))
 records=[node.value for node in tree.body if isinstance(node,ast.Assign) and
          any(isinstance(t,ast.Name) and t.id=="PREVIEW_CONTRACT" for t in node.targets)]
 must(len(records)==1,"one literal self-contained preview contract")
 try:data=ast.literal_eval(records[0])
 except (SyntaxError,ValueError,TypeError) as error:
  raise AssertionError("Gallery active preview: nonliteral preview request metadata") from error
 must(type(data) is dict and data.get("slug")==slug,
      "request metadata tied to exact filename")
 return data

def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument("--request",required=True)
 ap.add_argument("--preview",type=Path,required=True)
 ap.add_argument("--manifest",type=Path,required=True)
 args=ap.parse_args()
 state=json.loads(CONTRACT.read_text(encoding="utf-8"))
 _,request=validate(state)
 # Each new source-only preview is one immutable, self-contained script under
 # the path excluded from full-release push verification. This avoids changing
 # any tracked baseline/contract/test/HTML between routine preview iterations.
 if args.request!="baseline" and request is None:
  state=copy.deepcopy(state)
  state["mode"]="approved-source-only"
  state["request"]=embedded_request(args.request)
  _,request=validate(state)
 must(args.request==("baseline" if request is None else request["slug"]),
      "unapproved or mismatched preview request")
 verify(state,args.preview,json.loads(args.manifest.read_text(encoding="utf-8")))

if __name__=="__main__":main()
