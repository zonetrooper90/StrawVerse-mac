#!/usr/bin/env python3
"""Approved compact Player header exception; retain all other headers."""
import hashlib,json
from pathlib import Path
GUARDS=json.loads("{\"gallery/src/styles/28-unified-headers-and-history-frame.css\":\"84477d56c9bdc646ebe4975f5ba46086bd334d5d\",\"gallery/tests/test_player_settings_regression.py\":\"2da7c1974afcb6ab0347e7b8b3b7d2bcaa6e190e\",\"gallery/src/styles/03-player-and-desktop-frame.css\":\"680ced13116f35e22a8ee9e71a666e5fbde80652\",\"gallery/src/styles/27-player-navigation-and-header-refinements.css\":\"1d5bfd4d555ab1f29001d47ddcb9a57ad82652eb\"}")
for name,expected in GUARDS.items():
    raw=Path(name).read_bytes()
    assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==expected,name
path=Path("gallery/src/styles/28-unified-headers-and-history-frame.css")
source=path.read_text(encoding="utf-8")
for old,replacement in json.loads("[[\"   Only the page-specific rows change; the approved .top brand stays intact.\",\"   Only the standard page-specific rows change; the approved .top brand stays intact.\\n   The Player is an approved compact, divider-free exception (see below).\"],[\"body[data-theme] :is(.detail-page-header, .settings-page-head),\\nbody[data-theme].player-view .playback-compactbar {\",\"body[data-theme] :is(.detail-page-header, .settings-page-head) {\"],[\"body[data-theme] :is(.detail-page-header, .settings-page-head)::after,\\nbody[data-theme].player-view .playback-compactbar::after {\",\"body[data-theme] :is(.detail-page-header, .settings-page-head)::after {\"],[\"body[data-theme].player-view .playback-compactbar {\\n  margin-top:-5px; /* player .workspace top padding = 5px */\\n  padding-inline:0; /* margin alone aligns the title + button + divider to the page inset */\",\"/* Approved Player exception: retain the original 45px flex band, existing\\n   title/Back alignment and page gutters; the video frame is the boundary. */\\nbody[data-theme].player-view .playback-compactbar {\\n  height:45px;\\n  min-height:45px;\\n  border-bottom:0;\\n  margin-top:-5px; /* player .workspace top padding = 5px */\\n  padding-inline:0; /* margin alone aligns title and Back to the page inset */\"],[\"  body[data-theme] :is(.detail-page-header, .settings-page-head),\\n  body[data-theme].player-view .playback-compactbar {\",\"  body[data-theme] :is(.detail-page-header, .settings-page-head) {\"],[\"/* The taller header must not push the player controls below the viewport.\\n   Account for the extra 49px (94px Library band minus old 45px Player band)\\n   only when the viewport height, rather than content width, limits the video. */\\nbody.player-view .playback-page {\\n  --player-frame-width:min(100%,calc((100dvh - 231px) * 16 / 9));\\n}\\nbody.player-view .player-area {max-height:calc(100dvh - 231px)}\\n@media(max-width:740px){\\n  body.player-view .playback-page {\\n    --player-frame-width:min(100%,calc((100dvh - 218px) * 16 / 9));\\n  }\\n  body.player-view .player-area {max-height:calc(100dvh - 218px)}\\n}\\n\\n\",\"/* The original compact Player video budget lives in 03-player-and-desktop-frame.css\\n   (182px desktop / 169px narrow). No tall-header override is needed. */\\n\\n\"]]"):
    assert source.count(old)==1,old
    source=source.replace(old,replacement)
path.write_text(source,encoding="utf-8")
runner=Path("gallery/tests/test_player_settings_regression.py")
hook="\n# Mandatory compact Player header exception and retained standard page headers.\nimport subprocess\nsubprocess.run([sys.executable,str(Path(__file__).resolve().parents[1]/'audits'/'2026-11-16-compact-player-header-regression.py'),sys.argv[1]],check=True)\n"
raw=runner.read_text(encoding="utf-8")
assert hook not in raw
runner.write_text(raw+hook,encoding="utf-8")
print("PASS guarded compact Player header exception",flush=True)
