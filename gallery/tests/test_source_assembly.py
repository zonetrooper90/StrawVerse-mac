#!/usr/bin/env python3
"""Read-only source assembly and reversible M1 sync regression checks."""
import hashlib
import json
from pathlib import Path
import runpy
import shutil
import tempfile

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

# Exercise a canonical edit and derivative synchronization only in a temporary copy.
with tempfile.TemporaryDirectory(prefix="gallery-m1-") as td:
    tmp = Path(td) / "gallery"
    tmp.mkdir()
    shutil.copytree(root / "src", tmp / "src")
    shutil.copytree(root / "assets", tmp / "assets")
    (tmp / "tools").mkdir()
    shutil.copyfile(root / "tools/build-gallery.py", tmp / "tools/build-gallery.py")
    (tmp / "Gallery-current.html").write_bytes(canonical)
    (tmp / "Gallery-development.html").write_bytes(light)
    (tmp / "checkpoints").mkdir()
    (tmp / "checkpoints/current.json").write_bytes(pointer)
    isolated = runpy.run_path(str(tmp / "tools/build-gallery.py"))
    path = tmp / "src/build-manifest.json"
    original_manifest = path.read_bytes()
    layout = json.loads(original_manifest)
    # M1 sync is deliberately limited to one file per block.
    if all(len(layout[k]) == 1 for k in ("style", "script")):
        changed = canonical.replace(b"</style>", b"/* temporary M1 CSS smoke test */</style>", 1)
        changed = changed.replace(b"</script>", b"/* temporary M1 JS smoke test */</script>", 1)
        assert changed != canonical
        (tmp / "Gallery-current.html").write_bytes(changed)
        isolated["sync_from_canonical"]()
        assert isolated["build"]("full") == changed
        assert isolated["build"]("subtitle-preview") == changed
        assert isolated["build"]("development") == (tmp / "Gallery-development.html").read_bytes()
        assert (tmp / "Gallery-current.html").read_bytes() == changed
        assert (tmp / "checkpoints/current.json").read_bytes() == pointer
        # A second fragment proves deterministic ordered byte assembly and fail-closed sync.
        first = tmp / "src" / layout["script"][0]
        raw = first.read_bytes()
        first.write_bytes(raw[:len(raw)//2])
        second = first.with_name("m1-smoke-second.js")
        second.write_bytes(raw[len(raw)//2:])
        multiple = {**layout, "script": [layout["script"][0], str(second.relative_to(tmp / "src"))]}
        path.write_text(json.dumps(multiple), encoding="utf-8")
        assert isolated["build"]("full") == changed
        fails(isolated["sync_from_canonical"])
        reversed_layout = {**multiple, "script": list(reversed(multiple["script"]))}
        path.write_text(json.dumps(reversed_layout), encoding="utf-8")
        assert isolated["build"]("full") != changed
        first.write_bytes(raw)
        second.unlink()
    else:
        fails(isolated["sync_from_canonical"])
    for bad in ({**layout, "style": ["../outside.css"]},
                {**layout, "style": ["styles/missing.css"]},
                {**layout, "script": layout["script"] + layout["script"]}):
        path.write_text(json.dumps(bad), encoding="utf-8")
        fails(lambda: isolated["build"]("full"))
    path.write_bytes(original_manifest)

assert (root / "Gallery-current.html").read_bytes() == canonical
assert (root / "Gallery-development.html").read_bytes() == light
assert (root / "checkpoints/current.json").read_bytes() == pointer
print("PASS: exact ordered assembly, repeatable builds, token/path validation, isolated canonical sync and unchanged checkpoint.")
