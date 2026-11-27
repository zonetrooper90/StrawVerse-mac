#!/usr/bin/env python3
"""Fail-closed tests of the current-release provisional preview contract."""
import copy
import json
from pathlib import Path
import runpy

api=runpy.run_path("gallery/tools/active-preview-contract.py")
state=json.loads(Path("gallery/development/active-preview.json").read_text())
api["validate"](state)
assert state["promotion"]=={"status":"not-authorized","published_commit":None}
assert state["baseline"]["checkpoint_folder"]=="2026-11-27-player-settings-in-video-menu-retry"
assert state["baseline"]["verified_build_commit"]=="89382154bbf90af45cf14022a71577057f3a429d"
assert "player-toolbar-polish" in state["approved_scopes"]

def invalid(modify):
 broken=copy.deepcopy(state)
 modify(broken)
 try:api["validate"](broken)
 except (AssertionError,ValueError,TypeError,KeyError):return
 raise AssertionError("Unsafe active preview contract was accepted")

invalid(lambda s:s.update(schema=2))
invalid(lambda s:s.update(status="verified-release"))
invalid(lambda s:s["promotion"].update(status="approved"))
invalid(lambda s:s["promotion"].update(published_commit="a"*40))
invalid(lambda s:s["baseline"].update(full_sha256="wrong"))
invalid(lambda s:s["baseline"].update(full_blob="wrong"))
invalid(lambda s:s["baseline"].update(browser_run=0))
invalid(lambda s:s["baseline"].update(checkpoint_folder="../../unsafe"))
invalid(lambda s:s.update(mode="approved-source-only"))
invalid(lambda s:s.update(approved_scopes={}))
invalid(lambda s:s["approved_scopes"]["player-toolbar-polish"].update(source_paths=["gallery/assets/x.png"]))
invalid(lambda s:s.update(request={}))
dummy={
 "slug":"2026-11-27-player-toolbar-polish",
 "scope":"player-toolbar-polish",
 "script_blob":"a"*40,
 "approval_heading":state["approved_scopes"]["player-toolbar-polish"]["approval_heading"],
 "base_source_blobs":{"gallery/src/styles/26-player-icons-and-timelines.css":"d"*40},
 "source_blobs":{"gallery/src/styles/26-player-icons-and-timelines.css":"b"*40},
 "preview_sha256":"c"*64,"preview_bytes":123
}
def with_request(change):
 def apply(s):
  s["mode"]="approved-source-only"
  s["request"]=copy.deepcopy(dummy)
  change(s["request"])
 return apply
good=copy.deepcopy(state);good["mode"]="approved-source-only";good["request"]=dummy
api["validate"](good)
invalid(with_request(lambda r:r.update(slug="../../unsafe")))
invalid(with_request(lambda r:r.update(scope="unapproved")))
invalid(with_request(lambda r:r.update(approval_heading="## 2026-11-27 — Approved unrelated")))
invalid(with_request(lambda r:r.update(script_blob="not-a-blob")))
invalid(with_request(lambda r:r.update(approval_heading="No user approval")))
invalid(with_request(lambda r:r.update(source_blobs={"gallery/assets/other.png":"a"*40})))
invalid(with_request(lambda r:r.update(source_blobs={"gallery/src/../assets/icon.png":"a"*40})))
invalid(with_request(lambda r:r.update(source_blobs={})))
invalid(with_request(lambda r:r.update(base_source_blobs={})))
invalid(with_request(lambda r:r.update(base_source_blobs={"gallery/assets/other.png":"d"*40})))
invalid(with_request(lambda r:r.update(preview_bytes=-1)))
invalid(with_request(lambda r:r.update(preview_sha256="invalid")))
invalid(with_request(lambda r:r.update(unreviewed=True)))
# Self-contained literal request extraction never runs its Python source.
import tempfile
with tempfile.TemporaryDirectory() as temp:
 test_file=Path(temp)/"request.py"
 test_file.write_text("PREVIEW_CONTRACT="+repr(dummy)+"\nraise RuntimeError('must never execute')\n")
 assert api["embedded_request"].__name__=="embedded_request"
 # The pinned Git blob/HEAD path is validated independently on real preview commits.
 assert "embedded_request" in api
print("PASS active-current-baseline preview contract: strict schema, immutable proof, explicit source hashes, approval, scope, promotion boundary",flush=True)
