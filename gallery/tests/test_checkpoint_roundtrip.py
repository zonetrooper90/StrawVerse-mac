#!/usr/bin/env python3
"""Dry-run Gallery's edit -> immutable checkpoint -> restore process without changing GitHub HTML."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
GALLERY = ROOT / "gallery"
SOURCE = GALLERY / "Gallery-current.html"
POINTER = GALLERY / "checkpoints" / "current.json"
ID = "2026-11-11-infrastructure-transfer-dry-run"


def checksum(blob):
    return hashlib.sha256(blob).hexdigest()


def run(*args):
    subprocess.run(args, check=True, text=True)


def main():
    pointer_bytes = POINTER.read_bytes()
    ptr = json.loads(pointer_bytes)
    original = SOURCE.read_bytes()
    assert len(original) == ptr["bytes"], "GitHub working HTML length mismatch"
    assert checksum(original) == ptr["sha256"], "GitHub working HTML checksum mismatch"
    assert not (GALLERY / "checkpoints" / ID).exists(), "Dry-run checkpoint must not be committed"

    with tempfile.TemporaryDirectory(prefix="gallery-checkpoint-dry-run-") as td:
        tmp = Path(td) / "gallery"
        tools = tmp / "tools"
        backups = tmp / "checkpoints"
        tools.mkdir(parents=True)
        backups.mkdir()
        shutil.copyfile(GALLERY / "tools" / "stage-checkpoint.py", tools / "stage-checkpoint.py")
        shutil.copyfile(GALLERY / "tools" / "restore-checkpoint.py", tools / "restore-checkpoint.py")
        (backups / "current.json").write_bytes(pointer_bytes)
        shutil.copytree(GALLERY / "checkpoints" / ptr["folder"], backups / ptr["folder"])

        # A non-visual HTML comment tests the real source-transfer and backup machinery.
        changed = original + b"\n<!-- Temporary Gallery infrastructure checkpoint dry run; never publish. -->\n"
        assert checksum(changed) != checksum(original)
        candidate = tmp / "Gallery-dry-run.html"
        candidate.write_bytes(changed)
        run(sys.executable, str(tools / "stage-checkpoint.py"),
            "--input", str(candidate), "--id", ID,
            "--status", "experiment")
        run(sys.executable, str(tools / "restore-checkpoint.py"), "--verify-only")
        restored = tmp / "Gallery-restored.html"
        run(sys.executable, str(tools / "restore-checkpoint.py"), "--output", str(restored))
        assert restored.read_bytes() == changed, "Staged checkpoint did not restore exactly"
        staged = json.loads((backups / "current.json").read_text())
        assert staged["bytes"] == len(changed)
        assert staged["sha256"] == checksum(changed)
        assert len(original) == ptr["bytes"] and checksum(original) == ptr["sha256"]
        assert POINTER.read_bytes() == pointer_bytes, "Unexpected real checkpoint mutation"
        assert SOURCE.read_bytes() == original, "Unexpected real working HTML mutation"
        print("PASS: large HTML loaded, nonvisual edit applied, immutable checkpoint staged,")
        print("      new pointer verified, exact HTML restored, original GitHub source unchanged.")
        print("Original:", len(original), checksum(original))
        print("Dry-run: ", len(changed), checksum(changed))


if __name__ == "__main__":
    main()
