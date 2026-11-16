#!/usr/bin/env python3
"""Byte-identical retry of the approved global Watch History trial, test setup only."""
import hashlib,runpy
from pathlib import Path
GUARDS={
    "gallery/changes/pending/2026-11-16-global-watch-history-trial.py": "b42b590060c0b9d1b58022c3e8a2d4424ad322bd",
    "gallery/audits/2026-11-16-global-watch-history-trial-regression.py": "5a1259c814787d0f75b6b62a4dd534b136bfbe4d",
    "gallery/audits/2026-11-16-global-watch-history-trial-legacy-audit.py": "264eeeaa9a182a1aab1634f92bca19fc32f86957",
    "gallery/audits/2026-11-15-recently-watched-dense-test-fixture-regression.py": "737acc302cd327c59b1c937bb8bce3d296bd95b4",
    "gallery/tests/test_history_row_maintenance.py": "764a7785d0d34a87ca323d375025259de52a23fd",
    "gallery/tests/test_discover_search_motion_margin.py": "fb82e7a622ebd05055cbe881f5843e7dfaa529ea",
    "gallery/tests/test_discover_search_motion.py": "5c8c0fde6eb3d55744de1aa96f00f11713b59f2f",
    "gallery/tests/test_discover_search_scroll.py": "1a1825fe7639511de9cc32b6b3b8e5a36a3e0f60"
}
for name,expected in GUARDS.items():
    raw=Path(name).read_bytes()
    assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==expected,name
# Run the original unchanged guarded application patch, including its new default UI regression.
runpy.run_path("gallery/changes/pending/2026-11-16-global-watch-history-trial.py",run_name="__main__")
runner=Path("gallery/tests/test_history_row_maintenance.py")
source=runner.read_text(encoding="utf-8")
old="str(Path(__file__).resolve().parents[1]/'audits'/'2026-11-15-recently-watched-dense-test-fixture-regression.py'),sys.argv[1]"
new="str(Path(__file__).resolve().parents[1]/'audits'/'2026-11-16-global-watch-history-trial-retry-dense-legacy-audit.py'),sys.argv[1]"
assert source.count(old)==1
assert Path("gallery/audits/2026-11-16-global-watch-history-trial-retry-dense-legacy-audit.py").is_file()
runner.write_text(source.replace(old,new),encoding="utf-8")
print("PASS identical original application patch with legacy dense audit setup",flush=True)
