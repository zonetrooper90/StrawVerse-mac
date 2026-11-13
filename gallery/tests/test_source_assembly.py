#!/usr/bin/env python3
"""Read-only source assembly and source-first publication regression checks."""
import hashlib
import json
from pathlib import Path
import runpy
import shutil
import tempfile
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
builder = runpy.run_path(str(root / "tools/build-gallery.py"))
canonical = (root / "Gallery-current.html").read_bytes()
light = (root / "Gallery-development.html").read_bytes()
pointer = (root / "checkpoints/current.json").read_bytes()
builder["check"]()
assert builder["build"]("full") == canonical == builder["build"]("subtitle-preview")
assert builder["build"]("development") == light
assert hashlib.sha256(canonical).hexdigest() == json.loads(pointer)["sha256"]
assert builder["build"]("full") == builder["build"]("full")
# Check the exact asset-tokenized source, including whitespace and block ordering.
tokenized = canonical
for name, token in builder["TOKENS"].items():
    tokenized = builder["replace_once"](tokenized, builder["asset_url"](name), token)
assert builder["read_template"]() == tokenized
shell, blocks = builder["split_template"](tokenized)
assert builder["assemble_template"](shell, blocks) == tokenized


def fails(action):
    try:
        action()
    except ValueError:
        return
    raise AssertionError("Expected rejected source assembly")


for token in builder["BLOCKS"].values():
    fails(lambda: builder["assemble_template"](shell.replace(token, b""), blocks))
    fails(lambda: builder["assemble_template"](shell.replace(token, token + token), blocks))
    fails(lambda: builder["assemble_template"](shell, {**blocks, "script": blocks["script"] + token}))

# Test source-first generation in a disposable copy, never the real checkout.
with tempfile.TemporaryDirectory(prefix="gallery-source-first-") as td:
    tmp = Path(td) / "gallery"
    tmp.mkdir()
    shutil.copytree(root / "src", tmp / "src")
    shutil.copytree(root / "assets", tmp / "assets")
    (tmp / "tools").mkdir()
    for filename in ("build-gallery.py", "stage-checkpoint.py", "restore-checkpoint.py"):
        shutil.copyfile(root / "tools" / filename, tmp / "tools" / filename)
    (tmp / "Gallery-current.html").write_bytes(canonical)
    (tmp / "Gallery-development.html").write_bytes(light)
    (tmp / "checkpoints").mkdir()
    (tmp / "checkpoints/current.json").write_bytes(pointer)
    isolated = runpy.run_path(str(tmp / "tools/build-gallery.py"))
    path = tmp / "src/build-manifest.json"
    original_manifest = path.read_bytes()
    layout = json.loads(original_manifest)
    # Edit actual source files, not the tracked HTML.
    css_path = tmp / "src" / layout["style"][-1]
    js_path = tmp / "src" / layout["script"][-1]
    css_path.write_bytes(css_path.read_bytes() + b"/* temporary CSS source smoke test */")
    js_path.write_bytes(js_path.read_bytes() + b"/* temporary JS source smoke test */")
    expected = canonical.replace(b"</style>", b"/* temporary CSS source smoke test */</style>", 1)
    expected = expected.replace(b"</script>", b"/* temporary JS source smoke test */</script>", 1)
    expected_light = light.replace(b"</style>", b"/* temporary CSS source smoke test */</style>", 1)
    expected_light = expected_light.replace(b"</script>", b"/* temporary JS source smoke test */</script>", 1)
    assert isolated["build"]("full") == expected
    assert isolated["build"]("development") == expected_light
    fails(isolated["check"])  # Unpublished source cannot masquerade as a verified build.
    # Ordered multiple fragments must work with the same source-first publisher.
    first = tmp / "src" / layout["script"][-1]
    raw = first.read_bytes()
    first.write_bytes(raw[:len(raw)//2])
    second = first.with_name("source-first-smoke-second.js")
    assert not second.exists()
    second.write_bytes(raw[len(raw)//2:])
    multiple = {**layout, "script": layout["script"] + [str(second.relative_to(tmp / "src"))]}
    path.write_text(json.dumps(multiple), encoding="utf-8")
    assert isolated["build"]("full") == expected
    reversed_layout = {**multiple, "script": multiple["script"][:-2] + list(reversed(multiple["script"][-2:]))}
    path.write_text(json.dumps(reversed_layout), encoding="utf-8")
    assert isolated["build"]("full") != expected
    path.write_text(json.dumps(multiple), encoding="utf-8")
    # Preview writes only a dist output; old reverse synchronization is rejected.
    command = [sys.executable, str(tmp / "tools/build-gallery.py")]
    subprocess.run(command, check=True)
    assert (tmp / "dist/Gallery-development.html").read_bytes() == expected_light
    assert (tmp / "Gallery-development.html").read_bytes() == light
    for args in (["--sync-from-canonical"], ["--output", str(tmp / "Gallery-current.html")],
                 ["--output", str(tmp / "Gallery-development.html")], ["--output", str(css_path)]):
        assert subprocess.run(command + args, capture_output=True).returncode != 0
    assert (tmp / "Gallery-current.html").read_bytes() == canonical
    # Reject manual edits to old generated full HTML before any publication writes.
    (tmp / "Gallery-current.html").write_bytes(canonical + b"<!-- tampered generated HTML -->")
    fails(isolated["write_deliverables"])
    assert (tmp / "Gallery-development.html").read_bytes() == light
    (tmp / "Gallery-current.html").write_bytes(canonical)
    source_before = {p: p.read_bytes() for p in (tmp / "src").rglob("*") if p.is_file()}
    isolated["write_deliverables"]()
    assert (tmp / "Gallery-current.html").read_bytes() == expected
    assert (tmp / "Gallery-development.html").read_bytes() == expected_light
    assert (tmp / "checkpoints/current.json").read_bytes() == pointer
    assert all(p.read_bytes() == data for p, data in source_before.items())
    fails(isolated["check"])  # A changed build requires a new immutable checkpoint.
    # Exercise the existing staging and restore tools on the generated candidate.
    subprocess.run([sys.executable, str(tmp / "tools/stage-checkpoint.py"),
                    "--input", str(tmp / "Gallery-current.html"),
                    "--id", "2026-11-13-source-first-smoke", "--status", "experiment"], check=True)
    subprocess.run([sys.executable, str(tmp / "tools/restore-checkpoint.py"), "--verify-only"], check=True)
    isolated["check"]()
    for bad in ({**multiple, "style": ["../outside.css"]},
                {**multiple, "style": ["styles/missing.css"]},
                {**multiple, "script": multiple["script"] + multiple["script"]}):
        path.write_text(json.dumps(bad), encoding="utf-8")
        fails(lambda: isolated["build"]("full"))


assert (root / "Gallery-current.html").read_bytes() == canonical
assert (root / "Gallery-development.html").read_bytes() == light
assert (root / "checkpoints/current.json").read_bytes() == pointer
print("PASS: exact ordered assembly, source-first edits, multi-fragment publication, stale/tampered output rejection, isolated checkpoint round trip.")
