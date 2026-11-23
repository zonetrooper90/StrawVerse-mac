#!/usr/bin/env python3
"""Fail closed on unsafe fixture status, patch identity or published output."""
import json
from pathlib import Path
import runpy

api = runpy.run_path("gallery/tools/changed-build-parity-fixture.py")
assert api["FIXTURE_ID"] == "2026-11-23-dynamic-regression-scratch-parity"
assert api["PROBE_BLOB"] == "1aec46b0807562bf7b6bb746e22f0e9a53ea0c01"
assert api["CANDIDATE_CSS_BLOB"] == "8fbefc98cba2123482963db830de36289a591ef1"
assert api["FULL"] != api["LIGHT"]
assert api["NOTE"].startswith(b"/*") and api["NOTE"].endswith(b"*/\n")
assert api["BASE_FULL_SHA"] != api["BASE_LIGHT_SHA"]
assert Path("gallery/checkpoints/current.json").is_file()
base = json.loads(Path("gallery/checkpoints/current.json").read_text())
assert base["folder"] != api["FIXTURE_ID"]
assert base["sha256"] == api["BASE_FULL_SHA"]
assert api["PROBE"] not in ("gallery/changes/pending", "gallery/changes/previews")
assert api["FIXED_DATE"] == "2026-11-23T12:00:00+01:00"
print("PASS: scratch-only nonvisual source patch, unchanged release pointer and explicit experimental archive contract.")
