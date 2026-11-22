#!/usr/bin/env python3
"""G3.1 passive audit static preflight: exact inherited source, no weakening."""
from pathlib import Path
import runpy
api=runpy.run_path("gallery/audits/2026-11-22-g31-more-actions-smooth-ripple-passive-corrected-compare.py")
compiled=api["materialize"]()
assert compiled.count("window.__g31FrameSamples")==4
assert compiled.count("assert cases==48")==1
assert ".pause()" not in compiled and ".currentTime=" not in compiled
assert "opts.click()" in compiled and "menu geometry" in compiled
assert "105ms rise stagger" in compiled and "105ms dip stagger" in compiled
assert "for motion in (\"no-preference\",\"reduce\"):" in compiled
assert "for theme in THEMES:" in compiled
assert "for width in (1100,390):" in compiled
original=Path("gallery/audits/2026-11-22-g31-more-actions-smooth-ripple-compare.py").read_text()
legacy=Path("gallery/audits/2026-11-22-g31-more-actions-smooth-ripple-passive-retry-compare.py").read_text()
assert original.count('         opts=page.locator("#tag-options")\n         opts.hover()')==0
assert compiled.count('         opts=page.locator("#tag-options")')==1
assert legacy.count('G3.1 immutable audit anchor missing or duplicated')==1
for invalid,count in [('replace_once("old", bad_variable)',1),
                      ('replace_once("before","after")',2)]:
    try:
        api["literal_replacements"](invalid,"invalid-wrapper",count)
    except AssertionError:
        continue
    raise AssertionError("Rejected wrong or dynamic literal replacement")
print("PASS historical wrapper anchor correction, 48 cases and all test invariants")
