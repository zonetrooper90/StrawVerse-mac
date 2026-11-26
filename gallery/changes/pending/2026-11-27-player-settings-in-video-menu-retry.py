#!/usr/bin/env python3
"""Guarded retry of approved in-player Player Settings after geometry-audit failure.

Replays the EXACT original approved source/test candidate in an isolated
worktree. Only the dedicated comparison checks stable button geometry relative
to the player instead of browser screen coordinates, which legitimately change
during focus-driven workspace scrolling. No HTML, CSS, JS, original regression,
source/asset, publisher or immutable checkpoint change is introduced here.
"""
import ast
import hashlib
from pathlib import Path
import runpy

def blob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

original=Path('gallery/changes/pending/2026-11-26-player-settings-in-video-menu.py')
assert blob(original.read_bytes())=='acc828bfb917c436cdee2fb9ffe77eeeade1b8fa', 'Original approved Player Settings source patch drift'
failed=Path('gallery/audits/2026-11-26-player-settings-in-video-menu-compare.py')
assert blob(failed.read_bytes())=='58df0854b3eadb74f3452b3aaba88db860bc2834', 'Historical failed comparison must remain byte identical'
corrected=Path('gallery/audits/2026-11-27-player-settings-in-video-menu-retry-compare.py')
assert blob(corrected.read_bytes())=='39eb50bba859d656d6ca1905ae8322e8622306df', 'Retry comparison drift'
comparison=corrected.read_text(encoding='utf-8')
ast.parse(comparison, filename=str(corrected))
for required in (
 'assert total==48,total',
 "near(x,y,.5) for x,y in zip(before['rect'],returned['rect'])",
 "near(x,y,.5) for x,y in zip(before['rect'],opened['rect'])",
 "el.closest('#player-area').getBoundingClientRect()",
 'assert_anchored(page',
 "no global app dim",
):
    if required=='no global app dim':
        assert "global app must not dim/block" in comparison
    else:
        assert required in comparison,(required,'strict comparison coverage missing')
# Reconstruct the exact candidate from already-approved source and tests.
runpy.run_path(str(original),run_name='__main__')
outputs={
 'gallery/src/js/11e-player-subtitles.js':'0288fd8fc8ac36300b2e5dbd7c36df19266cb8d0',
 'gallery/src/js/11h-player-controls.js':'e690cb7dd7aeb8cfa99c35517b1124e5069b4d78',
 'gallery/src/styles/26-player-icons-and-timelines.css':'c736bb80c51b9d53b3c6d32154327cf3e5117660',
 'gallery/tests/test_player_settings_regression.py':'f1502b8a966b10d3cb92277e22a729d35ff7bdee',
}
for path,expected in outputs.items():
    actual=blob(Path(path).read_bytes())
    assert actual==expected,(path,'unapproved app/test drift',actual,expected)
print('PASS: identical approved Player settings source and original regression, 48-context relative geometry comparison pinned',flush=True)
