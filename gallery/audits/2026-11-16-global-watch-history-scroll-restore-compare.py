#!/usr/bin/env python3
"""Run the focused new regression early, in parallel with the mandatory complete suite."""
import subprocess,sys
from pathlib import Path
for name in ("Gallery-current.html","Gallery-development.html"):
    subprocess.run([sys.executable,str(Path(__file__).with_name("2026-11-16-global-watch-history-scroll-restore-regression.py")),"gallery/"+name],check=True)
