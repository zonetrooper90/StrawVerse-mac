# Queue 2 — identical-value declaration review (2026-11-13)

Read-only review completed. Proposed Q2-A only: no CSS removals approved or applied yet.

Baseline: verified DS01 build `41383b618be8c7dc92511a8d7370e359db3e9465`, reviewed at documentation head `9b020b533506635ce0a0e83a43f4efba68012f88`; immutable checkpoint `2026-11-13-shared-download-history-width`, full HTML SHA-256 `6d62486f67526e5e310d08bf2cbcbf14f7a466e9df79edf8b562b6b3b057881d`. Both exact-build checks passed; the visual approval documentation commit's browser check was still running at review. No source or checkpoint changes.

## Screening

Scan the current assembled lightweight stylesheet in order, respecting comments, quotes, parentheses, brackets, nested conditional contexts and top-level selector lists. Compare exact selector branch, context, property, value and importance; exclude keyframes and other non-qualified at-rules. This is a source-level lexical screen, not browser proof or a replacement for the tinycss2 audit. No CSSOM rule manipulation references found in the inline application script.

- 2,085 qualified rules; 7,151 declarations; no scanner errors.
- 360 repeated selector/property/context chains: 121 identical-value and 239 different-value (Queue 1: 122 and 240 before Search and DS01).
- 105 distinct earlier declaration occurrences have a later identical declaration with the **entire exact selector list**, enclosing condition, value and priority matched. Eight complete earlier rules (11 declarations) are Q2-A; 94 additional occurrences are in partial rules and remain untouched.
- 18 earlier branch-level occurrences fail the stricter full-selector matching filter; counts can overlap. Examples: grouped search reduced-motion transitions, grouped Player control alignment, grouped Settings search-state rules. Preserve until individually reviewed.
- All 239 differing-value chains remain untouched. Preserve responsive, theme, state and accessibility exceptions.

## Proposed Q2-A — eight complete earlier rules

Every earlier block below has all its declarations reproduced later under the same entire selector and condition. Preserve later copies, intervening rules and conditional boundaries. Remove only the exact block, not its surrounding compact source line. Locations are fragment-local at the reviewed head.

| Earlier file:line | Exact earlier block | Surviving location | Condition |
|---|---|---|---|
| `01-base-and-page-headers.css:24` | `.demo-download-footer .tip{margin:0}` | `08-downloads.css:36` | base |
| `03-player-and-desktop-frame.css:34` | `.player-controls .controls-middle{justify-content:center}` | `27-player-navigation-and-header-refinements.css:121` | base |
| `03-player-and-desktop-frame.css:60` | `.player-episode-nav .btn{font-size:12px;min-width:0;max-width:100%}` | `27-player-navigation-and-header-refinements.css:12–14` | base |
| `10-settings.css:25` | `.settings-panel-head .description{font-size:13px;line-height:1.5}` | `12-about-and-settings-refinements.css:87` | base |
| `10-settings.css:59` | `.settings-back{padding:8px}` | `12-about-and-settings-refinements.css:113` | max-width:440px |
| `21-themed-downloads.css:94` | `body[data-theme] .sf-dl-episode-name{grid-area:name}` | same file:220 | max-width:760px |
| `21-themed-downloads.css:95` | `body[data-theme] .sf-dl-episode-control{grid-area:control}` | same file:223 | max-width:760px |
| `21-themed-downloads.css:96` | `body[data-theme] .sf-dl-episode-percent{grid-area:percent}` | same file:224 | max-width:760px |

Exact source contexts and surviving declarations inspected individually. Keep Player responsive 720/560/390px rules ordered; Settings description and Back retain their later extra margin/min-width; Downloads retains all later named grid areas and layout definitions. DS01 shared frame is not a candidate.

## Required validation before publication

1. Obtain explicit approval of these eight specific blocks. Verify exact baseline and source hashes/unique context.
2. Compare original and hypothetical stylesheet on actual Gallery DOM: computed styles and geometry for affected elements and descendants, all six themes, desktop and compact widths around 760, 720, 560, 440 and 390px; normal and reduced motion, hover/focus, Player, Settings and expanded Downloads. Stop on any sampled difference. Static screening and sampled comparisons are not proof of every browser/state.
3. Controlled publisher; both build modes and existing regression suite including DS01 and Search; new immutable checkpoint if bytes change; both independent exact-build checks; user visual review. No assets, native branches or numbered release.
4. Stop for discussion of partial rules. Differing-value chains and dithering remain separate.

No application or generated files changed in this review.
