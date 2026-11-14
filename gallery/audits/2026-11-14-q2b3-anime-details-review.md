# Q2-B3 — Remaining Anime Details partial-rule proposal (2026-11-14)

Read-only review; no application changes or checkpoint. User approved review of remaining Anime Details CSS; exact batch approval is still required. Baseline visually accepted Q2-B2 build `fcc1d493b09dac7fa68703d199e3e234a33e1c37`, checkpoint `2026-11-14-q2b2-episode-toolbar`, full SHA-256 `369f2ddb37e01b2ebe30901c5143157543a1c72fdbd6b850ef0829e675205e04`, lightweight SHA-256 `e174093426b9d92bad7e91239eaf644e87034d549847bd4144a666bea33b5b08`. Exact build integrity 43536185845 and browser 43536188655 passed; immutable manifest and pointer agree. Review at visual acceptance head `879ff037fca534cd36b36641c9b9bf893d1d5ddf`, integrity passed (43541614161), browser in progress at review (43541614184). No changes to generated output, source or archive.

Rescan assembled lightweight CSS in cascade order, respecting comments, quotes, parentheses, brackets, enclosing condition, top-level selector branches, complete selector list and identical value/priority chains. 2,075 qualified rules, 7,103 declarations, 61 earlier matching partial-rule candidates. Select remaining 12 Anime Details declarations in seven earlier retained rules. This is a lexical screen, not proof of all CSS/browser states.

## Exact proposed removals
All earlier rules in `gallery/src/styles/02-anime-detail.css` (Git blob `213171d142dc2339aed85cc14591dfe302018f90`). Later rules in same file unless indicated.

| Earlier line | Complete selector | Condition | Earlier declarations only | Later surviving location |
|---|---|---|---|---|
| 17 | `.detail-audio-toggle button[aria-pressed="true"]` | base | `;color:var(--accent-ink)` (last) | 80 |
| 20 | `.detail-control-panel` | max-width:1050px | `grid-row:2;` | 188–192 |
| 24 | `.detail-control-panel` | max-width:680px | `max-width:none;` | 208 |
| 51 | `.episode-item` | base | `align-items:center;` `gap:14px;` | `07-anime-detail-refinements.css:160` |
| 64 | `.detail-hero` | max-width:850px | `grid-template-columns:160px minmax(0,1fr);` | 204 |
| 65 | `.detail-hero` | max-width:570px | `grid-template-columns:114px minmax(0,1fr);` | 219 |
| 88 | `.episode-tools` | base | `grid-column:3;` `display:flex;` `align-items:center;` `justify-content:flex-end;` `;min-width:0` (last) | `07-anime-detail-refinements.css:162` |

Later episode rule fragment blob `7de22f2c9de4ab0fa46d44d6758d9e70cf7a82ac`; themed audio/episode fragment `25-themed-anime-audio-and-episodes.css` blob `6ff2781cb52f4b334b3583f59da8e08bd72b75b0` remains untouched. Preserve exact remaining declarations, all intervening and later rules, including compact hero grid/panel layouts, themed stationary selected gradient and focus/hover rules, actual episode container width rules and status markers. Preserve both compact media blocks in full apart from the specified hero declarations (other selectors share their lines). Keep earlier .episode-tools gap:12px, all differently valued declarations and media/container conditions, no grouped-selector cleanup. Do not alter accepted episode toolbar, shared Back treatment, playback, Settings, artwork, markup, JS, native branches or numbered releases. Hold remaining 49 candidates.

## Required verification after specific approval
Hash-guard reviewed source and both exact baseline HTML digests, unique exact original rule strings; delete only these 12 declarations in one CSS file. Prove exact CSS-only diff and unchanged other bytes in each mode. Mandatory paired comparison gates with all six themes and both motion preferences, real mounted Anime Details DOM. Include desktop and viewport widths around 1050, 850, 680, 620, 570, 390 and 370px, actual episode section container boundaries at 635/515/320px (and 710 for accepted toolbar regression); verify measured container coverage. Compare computed styles, pseudo styles and geometry on hero, control panel, audio toggle, episode rows, tools, flags, Watch/Download controls, descendants and layout ancestors. Test complete, partial, unavailable and unmatched provider states; actual Sub/Dub selection, All/Playable filters and release selection; active/inactive audio hover and keyboard focus, available and disabled episode actions, real row/button hover/focus and selected-gradient stability, normal/reduced motion. Keep existing regression suite and both independent exact-build checks. Stop on differences/errors; sampled comparisons are not universal proof. Stage new immutable checkpoint only after all gates pass, then visual review separate.

No application changes made.
