#!/usr/bin/env python3
"""Deterministic standalone Gallery HTML builds from authoritative modular source."""
import argparse
import base64
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "src"
TEMPLATE = SOURCE_DIR / "Gallery.template.html"
MANIFEST = SOURCE_DIR / "build-manifest.json"
BLOCKS = {"style": b"__GALLERY_STYLE_BLOCK__", "script": b"__GALLERY_SCRIPT_BLOCK__"}
CANONICAL = ROOT / "Gallery-current.html"
DEVELOPMENT = ROOT / "Gallery-development.html"
ASSETS = ROOT / "assets/subtitle-preview"
MODES = ("development", "subtitle-preview", "full")
TOKENS = {
    "day": b"__GALLERY_SHRINE_DAY_DATA_URL__",
    "night": b"__GALLERY_SHRINE_NIGHT_DATA_URL__",
}
COLORS = {"day": b"#d5dbe2", "night": b"#091b2c"}
LIGHT_PATCHES = (
    (b"stage.querySelector('.subtitle-stage-day').src=SHRINE_DAY_IMAGE;",
     b"stage.querySelector('.subtitle-stage-day').style.backgroundColor=SHRINE_DAY_IMAGE;"),
    (b"stage.querySelector('.subtitle-stage-night').src=SHRINE_NIGHT_IMAGE;",
     b"stage.querySelector('.subtitle-stage-night').style.backgroundColor=SHRINE_NIGHT_IMAGE;"),
    (b"d.src=SHRINE_DAY_IMAGE;n.src=SHRINE_NIGHT_IMAGE;",
     b"d.style.backgroundColor=SHRINE_DAY_IMAGE;n.style.backgroundColor=SHRINE_NIGHT_IMAGE;"),
)

def replace_once(source, old, new):
    if source.count(old) != 1:
        raise ValueError(f"Expected exactly one occurrence: {old[:100]!r}")
    return source.replace(old, new, 1)

def source_layout():
    """Validate the ordered, explicit fragment list. Never glob or sort source."""
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or set(data) != {"schema", *BLOCKS} or data["schema"] != 1:
        raise ValueError("Invalid source manifest schema")
    paths = {}
    seen = set()
    for kind in BLOCKS:
        names = data[kind]
        if not isinstance(names, list) or not names:
            raise ValueError(f"Missing {kind} fragments")
        paths[kind] = []
        for name in names:
            if not isinstance(name, str):
                raise ValueError("Fragment path must be a string")
            relative = Path(name)
            directory, suffix = ("styles", ".css") if kind == "style" else ("js", ".js")
            if relative.is_absolute() or ".." in relative.parts or not relative.parts or relative.parts[0] != directory or relative.suffix != suffix:
                raise ValueError(f"Invalid {kind} fragment path: {name!r}")
            path = (SOURCE_DIR / relative).resolve()
            if not path.is_relative_to((SOURCE_DIR / directory).resolve()) or not path.is_relative_to(SOURCE_DIR.resolve()) or path in seen:
                raise ValueError(f"Invalid or repeated fragment: {name!r}")
            if not path.is_file():
                raise ValueError(f"Missing fragment: {name!r}")
            seen.add(path)
            paths[kind].append(path)
    return paths


def assemble_template(shell, blocks):
    """Replace exact block tokens; concatenate fragments with zero added bytes."""
    for kind, token in BLOCKS.items():
        if shell.count(token) != 1:
            raise ValueError(f"Expected exactly one {kind} block token")
        if any(marker in blocks[kind] for marker in BLOCKS.values()):
            raise ValueError(f"Unexpected assembly token inside {kind} source")
    result = shell
    for kind, token in BLOCKS.items():
        result = replace_once(result, token, blocks[kind])
    if any(token in result for token in BLOCKS.values()):
        raise ValueError("Unresolved assembly token")
    return result


def read_template():
    layout = source_layout()
    blocks = {kind: b"".join(path.read_bytes() for path in paths)
              for kind, paths in layout.items()}
    return assemble_template(TEMPLATE.read_bytes(), blocks)


def asset_url(name):
    raw = (ASSETS / f"shrine-{name}.png").read_bytes()
    if not raw.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError(f"Invalid original PNG: {name}")
    return b"data:image/png;base64," + base64.b64encode(raw)


def render_template(template, mode):
    if mode not in MODES:
        raise ValueError(f"Unknown build mode: {mode}")
    result = template
    for name, token in TOKENS.items():
        if mode == "development":
            value = COLORS[name]
        else:
            value = asset_url(name)
        result = replace_once(result, token, value)
    if mode == "development":
        for old, new in LIGHT_PATCHES:
            result = replace_once(result, old, new)
        if b"data:image/png;base64," in result:
            raise ValueError("Unexpected embedded PNG in development mode")
    return result

def build(mode):
    return render_template(read_template(), mode)


def split_template(template):
    """Extract exact bytes between the single classic style/script tags."""
    shell = template
    blocks = {}
    for kind, token in BLOCKS.items():
        opening = b"<" + kind.encode("ascii") + b">"
        closing = b"</" + kind.encode("ascii") + b">"
        if shell.count(opening) != 1 or shell.count(closing) != 1 or token in shell:
            raise ValueError(f"Expected exactly one inline {kind} block")
        prefix, tail = shell.split(opening, 1)
        blocks[kind], suffix = tail.split(closing, 1)
        shell = prefix + opening + token + closing + suffix
    if assemble_template(shell, blocks) != template:
        raise ValueError("Source extraction did not round trip")
    return shell, blocks


def write_deliverables():
    """Generate both tracked HTML files after an approved source edit.

    The old full deliverable must still match the existing immutable pointer.
    This does not stage a new checkpoint or write source files.
    """
    pointer = json.loads((ROOT / "checkpoints/current.json").read_text())
    previous = CANONICAL.read_bytes()
    if len(previous) != pointer["bytes"] or hashlib.sha256(previous).hexdigest() != pointer["sha256"]:
        raise ValueError("Existing full HTML differs from checkpoint; refuse publication")
    template = read_template()
    full = render_template(template, "full")
    preview = render_template(template, "subtitle-preview")
    light = render_template(template, "development")
    if full != preview:
        raise ValueError("Artwork-enabled modes differ")
    # Validate all modes before writing; only the two tracked generated files change.
    CANONICAL.write_bytes(full)
    DEVELOPMENT.write_bytes(light)
    if CANONICAL.read_bytes() != full or DEVELOPMENT.read_bytes() != light:
        raise ValueError("Generated deliverables failed read-back")
    print(f"Generated full HTML: {len(full)} bytes, SHA-256 {hashlib.sha256(full).hexdigest()}")
    print(f"Generated development HTML: {len(light)} bytes, SHA-256 {hashlib.sha256(light).hexdigest()}")
    print("Source files and immutable checkpoint untouched; verify and stage an approved changed build separately.")


def check():
    full = build("full")
    if full != CANONICAL.read_bytes() or full != build("subtitle-preview"):
        raise ValueError("Full round trip differs from canonical HTML")
    pointer = json.loads((ROOT / "checkpoints/current.json").read_text())
    if len(full) != pointer["bytes"] or hashlib.sha256(full).hexdigest() != pointer["sha256"]:
        raise ValueError("Full round trip differs from immutable checkpoint pointer")
    light = build("development")
    if light != DEVELOPMENT.read_bytes():
        raise ValueError("Committed development HTML is stale; regenerate explicitly")
    print(f"Full and subtitle-preview builds: {len(full)} bytes, SHA-256 {hashlib.sha256(full).hexdigest()}")
    print(f"Development build: {len(light)} bytes, SHA-256 {hashlib.sha256(light).hexdigest()}")
    for name in TOKENS:
        raw = (ASSETS / f"shrine-{name}.png").read_bytes()
        print(f"Original {name} PNG: {len(raw)} bytes, SHA-256 {hashlib.sha256(raw).hexdigest()}")
    print("Ordered source fragments and all build modes verified; canonical HTML and checkpoint untouched.")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=MODES, default="development")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", action="store_true", help="Verify all modes without writing files")
    parser.add_argument("--write-deliverables", action="store_true", help="Generate both tracked HTML deliverables after an approved source edit")
    args = parser.parse_args()
    if args.write_deliverables:
        if args.check or args.output or args.mode != "development":
            parser.error("--write-deliverables cannot be combined with other options")
        write_deliverables()
        return
    if args.check:
        if args.output:
            parser.error("--check does not accept --output")
        check()
        return
    output = args.output or ROOT / "dist" / f"Gallery-{args.mode}.html"
    output = output.resolve()
    # Preview mode never overwrites tracked deliverables, source, assets or checkpoints.
    protected = (CANONICAL.resolve(), DEVELOPMENT.resolve())
    protected_dirs = tuple((ROOT / name).resolve() for name in ("checkpoints", "assets", "src"))
    if output in protected or any(output == p or p in output.parents for p in protected_dirs):
        parser.error("Preview output cannot overwrite tracked deliverables, source, assets or checkpoints")
    result = build(args.mode)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(result)
    print(f"{output}: {len(result)} bytes, SHA-256 {hashlib.sha256(result).hexdigest()}")

if __name__ == "__main__":
    main()
