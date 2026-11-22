#!/usr/bin/env python3
"""Fail-closed schema, immutability, provenance and no-promotion tests."""
import copy
import json
from pathlib import Path
import runpy

audit = runpy.run_path("gallery/tools/verify-development-baseline.py")
state = json.loads(Path("gallery/development/verified-baseline.json").read_text())
assert audit["validate"](state) == state["baseline"]


def reject_schema(change):
    broken = copy.deepcopy(state)
    change(broken)
    try:
        audit["validate"](broken)
    except (AssertionError, ValueError, KeyError, TypeError):
        return
    raise AssertionError("unsafe baseline schema accepted")


def reject_content(change):
    """A well-formed but wrong SHA must fail actual file/provenance verification."""
    broken = copy.deepcopy(state)
    change(broken)
    audit["validate"](broken)
    try:
        audit["verify"](broken)
    except (AssertionError, ValueError, KeyError, TypeError):
        return
    raise AssertionError("tampered baseline hash was accepted")


reject_schema(lambda p: p.update(schema=2))
reject_schema(lambda p: p.update(status="released"))
reject_schema(lambda p: p["promotion"].update(status="approved"))
reject_schema(lambda p: p["promotion"].update(published_commit="a" * 40))
reject_schema(lambda p: p["baseline"].update(verified_build_commit="../old"))
reject_schema(lambda p: p["baseline"].update(checkpoint_folder="../outside"))
reject_schema(lambda p: p["baseline"].update(full_bytes=0))
reject_schema(lambda p: p["baseline"].update(lightweight_sha256="0" * 40))
reject_schema(lambda p: p["source_blobs"].update({"gallery/assets/x.png": "a" * 40}))
reject_schema(lambda p: p["verified_runs"].update(publisher="unknown"))
reject_content(lambda p: p["release_blobs"].update(
    {"gallery/Gallery-current.html": "0" * 40}))
reject_content(lambda p: p["historical_contract_blobs"].update(
    {"gallery/development/iterations.json": "0" * 40}))
reject_content(lambda p: p["source_blobs"].update(
    {"gallery/src/build-manifest.json": "0" * 40}))
reject_content(lambda p: p["baseline"].update(full_sha256="0" * 64))
# Real-world checks are read-only and catch changed source, published bytes, archive,
# moved pointer, old metadata or ancestry after their structural checks succeed.
assert audit["verify"](state)
print("PASS schema rejection, content/provenance tamper rejection, exact G3.1 read-only checks.")
