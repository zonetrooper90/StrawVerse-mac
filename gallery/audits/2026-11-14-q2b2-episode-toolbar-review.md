# Q2-B2 — Anime episode toolbar proposal (2026-11-14)

Read-only review; no application change or new checkpoint. User approved resuming Q2-B review; specific deletion scope requires approval. Verified baseline Q2-B1 build `58eaad52e9cad8250341c7070aacbf4395e44b1b`, full SHA-256 `2c0dbfd0aa3ff31fd36d0f0b82ae3421351a128cd6e9c39f46fbde232d24d608`, lightweight SHA-256 `f9ca46ad2de6dfd320872b7aa529ef4b44ecfbc8507410e6dd1e9394636f2721`. Pointer and immutable manifest agree; both independent checks passed on review head `90c6b0404ec77bdfd37c19e88e1c299c35229603` (43528010493, 43528010515). Stage 2 rehearsal passed; actual write-permission publisher path remains to be exercised on first specific approved application change.

Rescanned assembled lightweight CSS with lexical scanner respecting quoted strings, comments, parentheses, brackets, nested conditional contexts and complete selector lists. 2,075 qualified rules, 7,120 declarations, 78 earlier occurrences with later identical full selector/context/property/value/priority and no differing value in branch chain. This matches prior 94 minus Q2-B1's 16. Lexical screen, not browser proof.

## Proposed exact batch
All seven earlier rules and later surviving declarations are in `gallery/src/styles/07-anime-detail-refinements.css` (Git blob `ce896087cebd15258aed9a1c2e47d13ddf75a04e`); all are unconditional base rules. Keep every rule and every other declaration.

| Earlier line | Selector | Remove only these earlier declarations | Later line |
|---|---|---|---|
| 113 | `.episode-toolbar` | `align-items:center;` `margin:0 0 13px;` `;min-width:0` (last) | 167 |
| 114 | `.episode-toolbar .episode-heading` | `align-self:center;` | 168 |
| 116 | `.episode-toolbar .episode-availability` | `min-width:0;` `align-items:center;` `gap:12px;` `padding:7px 10px 7px 14px;` `margin:0;` | 170 |
| 117 | `.episode-availability .episode-stats` | `display:flex;` `align-items:center;` `min-width:0;` | 171 |
| 118 | `.episode-availability .episode-shown` | `white-space:nowrap;` | 173 |
| 122 | `.episode-availability .episode-filter` | `flex:0 0 auto;` `margin:0;` | 174 |
| 123 | `.episode-availability .episode-filter button` | `min-height:30px;` `padding:6px 10px;` | 175 |

Total 17 declarations. Preserve all intervening rules, including media 970/790/570/390px; preserve later container rules 710/635/515/320px and reduced-motion count rule. Preserve count visibility/fade/divider, filter button selection/hover/focus, typography, responsive display/grid/spacing and all differently valued declarations. Exclude episode rows/tools, audio toggle, control panel, hero, shared Back buttons, other routes and remaining 61 partial occurrences. No markup/JS/assets/native changes.

## Required gate after specific approval
Guard exact source blob and unique complete old rule strings, both baseline HTML hashes; compare exact intended CSS-only diff in each generated mode and unchanged other bytes. Use two mandatory full/lightweight comparison shards under the parallel publisher. Real Anime detail DOM, all six themes and both motion preferences; sample desktop and actual section container widths around 710/635/515/320px, plus viewport media 970/790/570/390px. Assert actual measured container width coverage; include matched/partial/unmatched provider cases, All/Playable only and Sub/Dub changes, count shown/hidden, active and inactive buttons, real hover/keyboard focus; compare computed styles, pseudo styles and geometry for toolbar, descendants, episode rows and layout ancestors in stable states. Preserve count animation and test normal/reduced motion behavior using existing regression plus targeted interaction assertions; do not replace genuine interaction with forced clicks. Stop on any discrepancy. Exact cascade screen and sampled browser equivalence do not prove every possible state. All standard candidate and independent post-commit tests remain required; archive new checkpoint only after passing; user visual approval separate. No numbered release.

No application files changed by this review. Remaining 61 candidates held; no grouped or differing-value removals authorized.
