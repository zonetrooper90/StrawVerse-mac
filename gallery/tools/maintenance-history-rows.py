#!/usr/bin/env python3
"""Gallery maintenance: hide unfinished collection transfer, activate History rows.
Only accepts the GitHub-verified Coordinated Fades checkpoint.
"""
import argparse, hashlib
from pathlib import Path
BASE='1d83bea4249345198d91730524fda609edb1d9734196bd274225a6a5f67c9a4c'

def change(s,old,new):
    n=s.count(old)
    if n!=1: raise ValueError(f'Expected 1 exact match, got {n}: {old[:110]!r}')
    return s.replace(old,new,1)

def patch(s):
    s=change(s,'function library(){','// Keep unfinished JSON collection transfers for a future redesign.\nconst GALLERY_COLLECTION_TRANSFER_UI_ENABLED=false;\nfunction library(){')
    s=change(s,'const actions=`<button class="btn" id="import">${icon(\'import\',16)} <span>Import</span></button><button class="btn primary" id="newtag">',
             'const actions=`${GALLERY_COLLECTION_TRANSFER_UI_ENABLED?`<button class="btn" id="import">${icon(\'import\',16)} <span>Import</span></button>`:\'\'}<button class="btn primary" id="newtag">')
    s=change(s,"const shareAction=isAll?'':", "const shareAction=isAll||!GALLERY_COLLECTION_TRANSFER_UI_ENABLED?'':")
    s=change(s,'${!isSearching&&!isAll?\'<p class="tip">Shared collections', '${GALLERY_COLLECTION_TRANSFER_UI_ENABLED&&!isSearching&&!isAll?\'<p class="tip">Shared collections')
    # The existing cover and anime-title buttons must continue to open details.
    # A full-surface button sits behind them; the trash action stays independent.
    s=change(s,'return `<div class="wh-summary">\n <button class="wh-cover-button"',
             'return `<div class="wh-summary">\n <button class="wh-summary-hit" type="button" data-wh-expand="${escapeHTML(r.id)}" aria-expanded="${open}" aria-label="${open?\'Collapse\':\'Expand\'} episodes for ${escapeHTML(r.title)}" title="${open?\'Collapse episodes\':\'View episodes\'}"></button>\n <button class="wh-cover-button"')
    s=change(s,'<div class="wh-actions"><button class="wh-action wh-expand" type="button" data-wh-expand="${escapeHTML(r.id)}" aria-expanded="${open}" aria-label="${open?\'Collapse\':\'Expand\'} episodes for ${escapeHTML(r.title)}" title="${open?\'Collapse episodes\':\'Manage watched episodes\'}">',
             '<div class="wh-actions"><span class="wh-action wh-expand" aria-hidden="true">')
    s=change(s,"${whSmallIcon('chevron')}</button><button class=\"wh-action wh-trash\"",
             "${whSmallIcon('chevron')}</span><button class=\"wh-action wh-trash\"")
    # Convert each episode's existing status-only button to one full-width
    # button. The update-in-place handler and scrollbar retain their identity.
    s=change(s,'return `<div class="wh-episode"><div class="wh-episode-main">',
             'return `<button type="button" class="wh-episode wh-episode-row" data-wh-episode="${escapeHTML(r.id)}:${ep.n}" aria-pressed="${ep.watched}" title="${ep.watched?\'Unmark as Watched\':\'Mark as Watched\'}"><span class="wh-episode-main">')
    s=change(s,'</div><button type="button" class="wh-episode-toggle" data-wh-episode="${escapeHTML(r.id)}:${ep.n}" aria-pressed="${ep.watched}" title="${ep.watched?\'Unmark as Watched\':\'Mark as Watched\'}">',
             '</span><span class="wh-episode-toggle">')
    s=change(s,'<span class="wh-episode-label">${label}</span></button></div>`;',
             '<span class="wh-episode-label">${label}</span></span></button>`;')
    css='''
/* Watch History follows Downloads' large click targets and keyboard-only focus. */
#wh-root .wh-summary{position:relative;transition:background-color .16s ease}
#wh-root .wh-summary:hover{background:var(--raised)}
#wh-root .wh-summary-hit{position:absolute;inset:0;z-index:1;width:100%;height:100%;margin:0;padding:0;border:0;background:transparent;cursor:pointer}
#wh-root .wh-summary-hit:focus-visible{outline:2px solid var(--accent);outline-offset:-3px;border-radius:14px}
#wh-root .wh-cover-button,#wh-root .wh-anime-title{position:relative;z-index:2}
#wh-root .wh-actions{position:relative;z-index:2;pointer-events:none}
#wh-root .wh-trash{pointer-events:auto}
#wh-root .wh-season:has(.wh-summary-hit:focus-visible){border-color:var(--accent)}
#wh-root .wh-season:hover:not(.is-expanded){border-color:var(--line)}
/* Entire episode is the interactive button; fixed-width status slot remains. */
#wh-root .wh-episode-row{appearance:none;box-sizing:border-box;width:100%;border:0;border-bottom:1px solid color-mix(in srgb,var(--line) 62%,transparent);background:transparent;color:var(--ink);font:inherit;text-align:left;cursor:pointer}
#wh-root .wh-episode-row:hover{background:var(--hover)}
#wh-root .wh-episode-row:focus-visible{outline:2px solid var(--accent);outline-offset:-2px;position:relative;z-index:1}
#wh-root .wh-episode-row .wh-episode-toggle{cursor:inherit}
#wh-root .wh-episode-row .wh-episode-toggle:hover{background:transparent;color:inherit}
#wh-root .wh-episode-row[aria-pressed="true"] .wh-episode-toggle{color:var(--accent)}
@media(prefers-reduced-motion:reduce){#wh-root .wh-summary{transition:none!important}}
'''
    marker='@media(prefers-reduced-motion:reduce){#wh-root .wh-episodes{animation:none}#wh-root .wh-inner-overlay{transition:none}}'
    return change(s,marker,marker+css)

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--input',type=Path,required=True);a.add_argument('--output',type=Path,required=True);opt=a.parse_args()
    source=opt.input.read_bytes();digest=hashlib.sha256(source).hexdigest()
    if digest!=BASE:raise SystemExit(f'Base checkpoint mismatch: {digest}')
    output=patch(source.decode()).encode()
    opt.output.write_bytes(output)
    print('SHA-256:',hashlib.sha256(output).hexdigest(),'bytes:',len(output))
