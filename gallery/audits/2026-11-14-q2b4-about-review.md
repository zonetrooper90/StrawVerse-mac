# Q2-B4 — About & Legal partial-rule review (2026-11-14)

Read-only audit approved; proposed application change NOT approved. Accepted baseline build `5cc1750e8199ec525587f1ac7f449e7826248b97`, checkpoint `2026-11-14-q2b3-anime-details-retry`, full SHA-256 `17f0af64a3f1ada057557327c9e26feeeb676a801be319fd23e2f1905b29cd5b` (6,903,147 bytes), lightweight SHA-256 `4c17191d059b4492bb4cae0eff22669559dd12410e7b2bf8af6f7c8c56c9d5dc` (587,457 bytes). Exact-build independent integrity 43560470875 and browser 43560472829 passed. Review at acceptance head `47302bfe29e458c9aba82b4d04f23bef568c8ed9`: integrity 43583441062 verified identical archive and deterministic source assembly; browser 43583441060 in progress at review. Pointer and manifest agree. No application or checkpoint changes.

## Rescan
Read verified assembled lightweight style block in cascade order; handle comments, quotes, escapes, parentheses/brackets, enclosing condition, top-level selector branches; exclude keyframes/non-qualified at-rules. Require identical values and priority in all occurrences of a branch/property/condition chain, plus later identical full selector list. 2,075 qualified rules, 7,091 declarations, 65 identical-value and 239 differing-value repeated chains, 49 earlier matching occurrences in 27 partial rules, no scanner errors. Lexical screen, not universal browser proof.

| Group | Candidates | Earlier stylesheet lines (relative to extracted style text) | Relative review risk |
|---|---:|---|---|
| About & Legal | 5 | 1195,1208,1213,1317,1345 | Low |
| Subtitle font tiles | 6 | 1388,1413 | Low–medium |
| Anime release arrow hover | 1 | 734 | Medium (interaction) |
| Settings layout/navigation | 18 | 998,1001,1002,1004,1015,1046 (three rules) | Medium (shared layout, Back, responsive side navigation) |
| Player and fullscreen | 8 | 341,375,406,407,3432 | Medium–high (fullscreen and shared Back) |
| Search/header transitions | 11 | 919,920,928,929,930,940 | Higher (visibility, width, opacity, responsive transition timing) |

Risk ratings are qualitative prioritization, not observed defects. Keep differing-value chains and grouped-selector-only cases outside this scope. Preserve accepted DS02b and prior cleanups.

## Proposed Q2-B4: exactly five About declarations
All in `gallery/src/styles/12-about-and-settings-refinements.css`, Git blob `26613146f5fa98d841b3f0e0b3e18ce958a60b7d`. Exact unique earlier rule snippets checked using in-memory replacements only; 74 ASCII bytes total. Later copies in same fragment.

| Earlier line | Complete selector | Condition | Delete only | Later surviving line |
|---|---|---|---|---|
| 2 | `.about-shell` | base | `;min-width:0` | 122 |
| 15 | `.about-menu-item .about-menu-copy strong` | base | `font-size:13px;` | 133 |
| 20 | `.about-detail-title` | base | `font-size:20px;` | 135 |
| 124 | `.about-identity` | base | `align-items:center;` | 158 |
| 152 | `.about-identity` | max-width:700px | `padding:17px;` | 173 |

Preserve entire remaining earlier rules, later copies, grouped width rule at 157, all different-value declarations, all media boundaries (1050/700/520/440), 440px align-items:flex-start exception, neighboring compact rules on line 152, privacy/legal text, About navigation/focus and shared Back behavior. Do not remove any complete rule or touch Settings/font/Search/Player/Anime release selector/JS/assets/native/numbered releases. Hold other 44 candidates.

## Required verification after explicit approval
- Guard baseline HTML hashes, exact source blob and each unique full original rule; delete only these five declarations, 74 bytes in both modes, prove all non-CSS bytes unchanged. Source-first build, exact candidate artifact/tree checks and immutable checkpoint.
- Real mounted Settings > About DOM in both HTML modes, all six themes and both motion preferences; sample desktop and both sides of 1050, 710 (Settings side nav), 700, 520 and 440px, plus narrow 370px. Compare computed styles, pseudo styles and geometry on shell, identity and facts, menu labels, detail titles, all visible descendants and layout ancestors. Exercise Overview, Acknowledgements, Third-Party Components, Open Source Licenses, Legal & Privacy, Terms, Privacy Policy, Copyright & Disclaimer, contextual Back and keyboard focus/hover. Verify correct nested Back labels and destinations, scroll reset, text/links and visible/hidden view state, narrow layout and focus. Include Settings search entry to About if supported by actual UI. Keep DS02b and all existing regressions. Use four independent mode/motion shards with exact required counts and complete matrix; preserve all three standard test groups and both post-publish independent checks. Stop on mismatch; visual approval separate. Sampling is not universal proof.
- No application change made during review. No new checkpoint or numbered release.
