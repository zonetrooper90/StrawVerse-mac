#!/usr/bin/env python3
"""Deterministic standalone Gallery HTML builds; canonical checkpoint stays authoritative."""
import argparse
import base64
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "src/Gallery.template.html"
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

def build(mode):
    if mode not in MODES:
        raise ValueError(f"Unknown build mode: {mode}")
    result = TEMPLATE.read_bytes()
    for name, token in TOKENS.items():
        if mode == "development":
            value = COLORS[name]
        else:
            raw = (ASSETS / f"shrine-{name}.png").read_bytes()
            if not raw.startswith(b"\x89PNG\r\n\x1a\n"):
                raise ValueError(f"Invalid original PNG: {name}")
            value = b"data:image/png;base64," + base64.b64encode(raw)
        result = replace_once(result, token, value)
    if mode == "development":
        for old, new in LIGHT_PATCHES:
            result = replace_once(result, old, new)
        if b"data:image/png;base64," in result:
            raise ValueError("Unexpected embedded PNG in development mode")
    return result

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
    print("All build modes verified; canonical HTML and checkpoint untouched.")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=MODES, default="development")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", action="store_true", help="Verify all modes without writing files")
    args = parser.parse_args()
    if args.check:
        if args.output:
            parser.error("--check does not accept --output")
        check()
        return
    output = args.output or (DEVELOPMENT if args.mode == "development" else ROOT / "dist" / f"Gallery-{args.mode}.html")
    output = output.resolve()
    # Prevent this transitional builder from writing the checkpoint or canonical source.
    protected = (CANONICAL.resolve(), TEMPLATE.resolve())
    if output in protected or any(p in output.parents for p in (ROOT / "checkpoints", ROOT / "assets", ROOT / "src")):
        parser.error("Output cannot overwrite canonical source, assets or checkpoints")
    result = build(args.mode)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(result)
    print(f"{output}: {len(result)} bytes, SHA-256 {hashlib.sha256(result).hexdigest()}")

if __name__ == "__main__":
    main()
