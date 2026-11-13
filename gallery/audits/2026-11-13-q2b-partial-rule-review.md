# Q2-B — partial-rule review and first proposed batch (2026-11-13)

Read-only review completed after the user's approval to investigate. **No CSS removals approved or applied.** Baseline visually accepted DS02b build `e108c7c892eab7e41d892ae06874c78f58160011`, immutable checkpoint `2026-11-13-ds02b-stronger-back-accent`, SHA-256 `333498a79e7ef34f1d85fd3049d599013c24f1d3b5ff81b80d13f8bf1bf7fee3`. Both exact-build independent checks passed. Review at documentation head `ea21750eb82a39f8e734562517a4641e87196b5d`; documentation integrity passed, browser status at review: in_progress. DS01, Q2-A and DS02b visually accepted.

## Updated screening

Rescan current assembled lightweight stylesheet in original source order, with comments/quoted values/parentheses/brackets and enclosing conditional context respected, splitting top-level selector branches, excluding keyframes and non-qualified at-rules. As in Q2-A, require exact full selector list, condition, property, value and importance for a later matching declaration, with all occurrences of that branch/property/context chain having the same value/priority. Lexical screen only; no universal runtime proof.

- 2,075 qualified rules, 7,136 declarations; no scanner errors.
- 110 identical-value selector/property/context chains, 239 differing-value chains.
- 94 distinct earlier matching occurrences in 47 partial rules; no complete earlier redundant rules remain under this filter.
- 18 earlier branch-level occurrences fail the full-selector match; may overlap other counts. Hold grouped-selector cases and all 239 differing-value chains for later review.
- Select a coherent first feature batch: 16 declarations within six Downloads rules. Hold the other 78 earlier occurrences (Anime details/episode toolbar, Player including fullscreen, search transitions, Settings/About/font tiles and shared headers) for separate review. In particular, do not touch the accepted DS02b Back-button treatment, shared width standard, or search-motion rules.

## Proposed Q2-B1 — Downloads only

Each proposed earlier declaration is matched by a later declaration under the exact same complete selector, conditional context and priority. Preserve the entire earlier rule with its remaining declarations, every later declaration, all intervening rules, selector order and media boundaries. Locations are fragment-local at review. Exact old source snippets below include punctuation to make the later edit checksum-guarded and unambiguous.

| Earlier source / line | Exact selector and condition | Earlier declarations to remove | Later surviving location |
|---|---|---|---|
| `01-base-and-page-headers.css:23` | `.demo-download-footer`, base | `display:flex;` `align-items:center;` `flex-wrap:wrap;` | `08-downloads.css:35` |
| `21-themed-downloads.css:56–60` | `body[data-theme] .sf-dl-list .sf-dl-episode`, base | `gap:12px;` `min-height:48px;` `border:0;` | same file:145,147,149 |
| `21-themed-downloads.css:66` | `body[data-theme] .sf-dl-episode-track`, base | `min-width:0;` | same file:187 |
| `21-themed-downloads.css:68` | `body[data-theme] .sf-dl-control-button`, base | `border-radius:16px;` `font-size:11px;` `align-items:center;` `justify-content:center;` | same file:164,166 |
| `21-themed-downloads.css:71` | `body[data-theme] .sf-dl-episode-percent`, base | `width:44px;` `justify-self:end;` `text-align:right;` `;font-variant-numeric:tabular-nums` (last declaration, no trailing semicolon) | same file:186 |
| `21-themed-downloads.css:77` | `body[data-theme] .sf-dl-list .sf-dl-episode`, `@media(max-width:1120px)` | `;gap:9px` (last declaration) | same file:205–208 |

Source SHA-1 blob guards at reviewed head: `01-base-and-page-headers.css` = `9cf3c3fb7989f7bb0033c9a15b8c154bc7c6485b`; `21-themed-downloads.css` = `ac62184c58ee4b7d2f7c0d5b24ed67883e10f2f2`; later footer in `08-downloads.css` = `4714451f762cef05e820bb48c5405547f08323d6`.

Preserve the footer's earlier gap and margin-top; episode display/grid template, align-items/min-width/padding/color; track display/align-items/width; control height/min-width/padding/background/border/color/font-weight/display/gap/cursor; percent font-size/font-weight/color; responsive 1120px grid template. In particular later episode border shorthand and border-bottom, sibling and last-child exceptions, state and responsive grid-area/column-gap/row-gap rules remain in place. Do not remove any different-value declarations (even if apparently overridden), change responsive dimensions or touch shared Watch History scroll policy.

## Required validation after specific approval

1. Verify baseline full/lightweight digests and immutable archive, builder round trip; guard exact source blobs and exact original rule strings; change only listed declaration occurrences in two source fragments. No new selector, rule order change or JS/assets/markup edits.
2. Dedicated controlled-publisher gate: prove the exact intended CSS declaration deletions and unchanged non-CSS bytes in both generated HTML modes. Use actual mounted Downloads DOM, same-page baseline/candidate stylesheet swap, all enumerable computed properties, pseudo styles and geometry on footer, all episode rows, track, control and percent elements plus descendants and layout ancestors. Include all six themes, both motion preferences, expanded/collapsed groups, mixed transfer statuses, pause/resume/retry/dismiss affordances, filter/search states, actual row/control hover and keyboard focus; sample desktop and widths around 1120, 760, 450 and 370px. Check actual DS01 width alignment and shared native scrolling through existing permanent tests. Keep all declarations after the removed ones intact; stop on any sampled difference or error. Sampling is not proof for all possible browser states.
3. Existing full/lightweight regression suites, immutable checkpoint if bytes change, both independent exact-build checks, then user visual review. Keep DS02b permanent checks. No numbered release or native changes.
4. Stop before the remaining 78 partial-rule occurrences and grouped/different-value chains. Next feature batch only after review and specific approval.

No application, source, asset, workflow or generated HTML changes in this review.
