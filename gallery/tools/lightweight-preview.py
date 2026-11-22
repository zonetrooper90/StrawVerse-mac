#!/usr/bin/env python3
"""Read-only lightweight Gallery preview from a checksum-guarded source request.

Run inside a disposable detached worktree of the exact GitHub commit. Never
modifies committed HTML, images, archive, release pointer or remote Git refs.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import runpy
import subprocess
import sys

SHA = re.compile(r"[0-9a-f]{40}")
SLUG = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}-[a-z0-9-]+")
ROOT = Path.cwd()
FULL = Path("gallery/Gallery-current.html")
LIGHT = Path("gallery/Gallery-development.html")
POINTER = Path("gallery/checkpoints/current.json")
PREVIEW_DIR = "gallery/changes/previews/"


class PreviewError(AssertionError):
    pass


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT).decode("utf-8").strip()


def python(*args):
    subprocess.run([sys.executable, "-B", *args], cwd=ROOT, check=True)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def reject(message):
    raise PreviewError(message)


def validate_name(request):
    if request != "baseline" and not SLUG.fullmatch(request):
        reject("Expected baseline or a date-prefixed approved request slug")
    return request


def detect_request(manual, previous, base):
    """A push activates only one newly ADDED preview script; no guessing."""
    if manual:
        return validate_name(manual)
    if not previous or not SHA.fullmatch(previous) or previous == "0" * 40:
        return "baseline"
    added = git("diff", "--name-only", "--diff-filter=A",
                previous, base, "--", PREVIEW_DIR).splitlines()
    touched = git("diff", "--name-only",
                  previous, base, "--", PREVIEW_DIR).splitlines()
    if added != touched or len(added) > 1:
        reject("Preview scripts are immutable: expected at most one newly added request")
    if not added:
        return "baseline"
    path = added[0]
    request = validate_name(Path(path).stem)
    if path != PREVIEW_DIR + request + ".py":
        reject("Unapproved preview request location")
    return request


def request_path(request, manual):
    if request == "baseline":
        return None
    preview = Path(PREVIEW_DIR + request + ".py")
    pending = Path("gallery/changes/pending/" + request + ".py")
    if preview.is_file():
        return preview
    # Existing approved publisher requests may be inspected manually without
    # replaying, retrying or triggering their publication workflow.
    if manual and pending.is_file():
        return pending
    reject("No approved source request available for lightweight preview")


def preflight_audit(wrapper, root=ROOT):
    """Check literal inherited-audit anchors BEFORE Chromium or large suites.

    Replays only static source substitutions; never runs original audit code.
    Complex/dynamic comparisons still require their full verification later.
    """
    code = wrapper.read_text(encoding="utf-8")
    parsed = ast.parse(code, filename=str(wrapper))
    original = None
    for stmt in parsed.body:
        if not isinstance(stmt, ast.Assign):
            continue
        if not any(isinstance(t, ast.Name) and t.id == "original"
                   for t in stmt.targets):
            continue
        expr = stmt.value
        if (isinstance(expr, ast.Call) and isinstance(expr.func, ast.Name)
                and expr.func.id == "Path" and len(expr.args) == 1
                and isinstance(expr.args[0], ast.Constant)
                and isinstance(expr.args[0].value, str)):
            original = expr.args[0].value
    calls = []
    for stmt in parsed.body:
        if not isinstance(stmt, ast.Expr) or not isinstance(stmt.value, ast.Call):
            continue
        call = stmt.value
        if not isinstance(call.func, ast.Name) or call.func.id != "replace_once":
            continue
        if len(call.args) != 2 or not all(
            isinstance(a, ast.Constant) and isinstance(a.value, str)
            for a in call.args
        ):
            reject("Dynamic inherited-audit replacement requires separate review")
        calls.append(tuple(a.value for a in call.args))
    if not calls:
        return 0
    if not original:
        reject("Inherited audit substitutions have no statically identifiable original")
    source_file = (root / original).resolve()
    if not source_file.is_relative_to(root.resolve()) or not source_file.is_file():
        reject("Invalid inherited-audit source reference: " + original)
    source = source_file.read_text(encoding="utf-8")
    for old, new in calls:
        if source.count(old) != 1:
            reject("Inherited-audit source anchor missing or duplicated: " + repr(old[:100]))
        source = source.replace(old, new, 1)
    return len(calls)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True)
    parser.add_argument("--previous", default="")
    parser.add_argument("--request", default="")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not SHA.fullmatch(args.base) or git("rev-parse", "HEAD") != args.base:
        reject("Preview worktree is not at the exact requested GitHub commit")
    if git("status", "--porcelain"):
        reject("Preview worktree must start clean")
    output = args.output.resolve()
    if output.is_relative_to(ROOT.resolve()):
        reject("Preview must be outside repository/worktree")

    request = detect_request(args.request, args.previous, args.base)
    patch_script = request_path(request, bool(args.request))
    # Verify the established full release and both baseline outputs *before*
    # editing isolated source. This does not publish or write a full HTML.
    python("gallery/tools/restore-checkpoint.py", "--verify-only")
    python("gallery/tools/build-gallery.py", "--check")
    pointer_bytes = POINTER.read_bytes()
    full_bytes = FULL.read_bytes()
    light_bytes = LIGHT.read_bytes()
    pointer = json.loads(pointer_bytes)
    if len(full_bytes) != pointer["bytes"] or sha256(full_bytes) != pointer["sha256"]:
        reject("Immutable full release checkpoint does not match canonical HTML")

    script_blob = None
    anchor_count = 0
    if patch_script:
        code = patch_script.read_bytes()
        compile(code, str(patch_script), "exec")
        script_blob = sha256(code)
        # Catch known deterministic inherited audit mistakes before running
        # a browser or expensive matrix. No assertion is changed or skipped.
        audit = Path("gallery/audits/" + request + "-compare.py")
        if audit.is_file():
            anchor_count = preflight_audit(audit)
        runpy.run_path(str(patch_script), run_name="__main__")
    if POINTER.read_bytes() != pointer_bytes or FULL.read_bytes() != full_bytes:
        reject("Preview request touched full release or immutable pointer")
    if LIGHT.read_bytes() != light_bytes:
        reject("Preview request modified tracked lightweight deliverable")
    paths = git("diff", "--name-only", "HEAD").splitlines()
    if patch_script:
        if not paths or not all(x.startswith("gallery/src/") for x in paths):
            reject("Preview source patch must modify only authoritative gallery/src files")
    elif paths:
        reject("Baseline rehearsal unexpectedly modified tracked files")
    if git("ls-files", "--others", "--exclude-standard"):
        reject("Untracked files created inside the preview worktree")

    builder = runpy.run_path("gallery/tools/build-gallery.py")
    preview = builder["build"]("development")
    if preview != builder["build"]("development"):
        reject("Non-deterministic lightweight preview")
    if patch_script and preview == light_bytes:
        reject("Source patch produces byte-identical lightweight preview")
    if not patch_script and preview != light_bytes:
        reject("Baseline preview differs from verified tracked development HTML")
    if b"data:image/png;base64," in preview or b"__GALLERY_STYLE_BLOCK__" in preview:
        reject("Unexpected embedded artwork or unresolved build token")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(preview)
    if output.read_bytes() != preview:
        reject("Preview artifact failed read-back")
    manifest = {
        "status": "Development Preview — Not a Verified Release",
        "github_commit": args.base,
        "request": request,
        "request_sha256": script_blob,
        "changed_source_files": paths,
        "source_diff_sha256": sha256(subprocess.check_output(
            ["git", "diff", "--binary", "--no-ext-diff", "--", "gallery/src"], cwd=ROOT)),
        "lightweight_filename": output.name,
        "lightweight_bytes": len(preview),
        "lightweight_sha256": sha256(preview),
        "verified_full_baseline_bytes": len(full_bytes),
        "verified_full_baseline_sha256": sha256(full_bytes),
        "immutable_checkpoint": pointer["folder"],
        "preflight_audit_literal_anchors": anchor_count,
        "full_release_rebuilt_or_published": False,
    }
    (output.parent / "preview-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PASS lightweight-only immutable-release-preserving preview:", json.dumps(manifest), flush=True)


if __name__ == "__main__":
    main()
