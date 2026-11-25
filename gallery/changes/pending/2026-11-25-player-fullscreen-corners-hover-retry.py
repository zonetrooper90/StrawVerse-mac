#!/usr/bin/env python3
"""Guarded correction of the fullscreen comparison's real Player entry path.

The approved Player four-piece SVG, hover motion and source mutation are
replayed byte-identically from the immutable first request. Only the
independently authored browser comparison is corrected: wait for the stage
transition to settle, then start the actual Player simulation to expose
controls, as Gallery's existing Player regression already does.
"""
import hashlib
from pathlib import Path
import runpy

def git_blob(raw):
    return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()

original=Path('gallery/changes/pending/2026-11-25-player-fullscreen-corners-hover.py')
assert git_blob(original.read_bytes())=='38afc4eb1a0da13a0f454cc8de897a991c1531e7', 'Original approved fullscreen patch drift'
prior=Path('gallery/audits/2026-11-25-player-fullscreen-corners-hover-compare.py')
assert git_blob(prior.read_bytes())=='95afc502a293bca69774167e0fa4d767710135e6', 'Prior failed comparison was rewritten'
correction=Path('gallery/audits/2026-11-25-player-fullscreen-corners-hover-retry-compare.py')
assert git_blob(correction.read_bytes())=='96c0b675114575657054e95c8dde38ca708e3418', 'Corrected comparison changed'
audit=correction.read_text(encoding='utf-8')
for anchor in (
    '!!state.detailId&&!galleryStageFadeInProgress&&!galleryStageTransition',
    '!!state.playback&&!!document.getElementById',
    "page.locator('#sf-player-demo-start').click()",
    "page.wait_for_selector('#fullscreen .g4-fullscreen-piece',state='visible'",
):
    assert audit.count(anchor)==1, ('Missing corrected Player entry assertion',anchor)
runpy.run_path(str(original),run_name='__main__')
for path, expected in (
 ('gallery/src/js/11b-player-page.js','d13791c0c18fe1b79964f9dc19b6fb02a7a04782'),
 ('gallery/src/js/11h-player-controls.js','720bafd0b7a6dbfc59afebbef6532cdbee7b66aa'),
 ('gallery/src/styles/26-player-icons-and-timelines.css','5eb8ab5e2be345d80451fdee671cb7ee5cc2fb5a'),
):
    actual=git_blob(Path(path).read_bytes())
    assert actual==expected, (path,'Original approved source differs',actual,expected)
print('PASS: exact first-approved Player fullscreen source; only dedicated browser entry/audit corrected',flush=True)
