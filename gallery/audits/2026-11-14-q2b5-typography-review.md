# Q2-B5 — Application typography font tiles partial-rule review (2026-11-14)

Read-only audit approved; exact application change requires separate approval. Correction to the Q2-B4 review's feature label: these six candidates are application-wide font tiles in Settings > Appearance > Typography, NOT subtitle font selection in Playback > Subtitles. The actual subtitle font select is separate and excluded. Historical audit unchanged.

Accepted Q2-B4 build `f17c79f13fe5948f724cde1b6f1b44702273cd89`, checkpoint `2026-11-14-q2b4-about`, full SHA-256 `0a3a9f474ad454b99e758a70a3c93d3bd03ac3f2c4ddf92aaa3ca536e28b6bbd` (6,903,073 bytes), lightweight `9c2b205045ee5fd6c462743ecb7707f44a8d7e322bdc8502ae5688fe7a6c1646` (587,383 bytes). Independent exact-build integrity 43585243719 and browser 43585245698 passed. Acceptance head `b9ec0d0dd53f6443a5eca90271471f07c9f98266`: both independent checks 43589476010 and 43589475987 passed; integrity logs confirm archive, exact full/lightweight bytes and source reconstruction. Pointer and manifest agree.

## Rescan and exact proposed removal
Scan verified assembled lightweight stylesheet in cascade order, respecting comments, quoted values, escaped characters, parentheses/brackets, conditional contexts and top-level selector branches; exclude keyframes/non-qualified at-rules. Require identical values/priority throughout branch/property/context chain and later full-selector match. 2,075 rules, 7,086 declarations, 60 identical-value and 239 differing-value chains, 44 distinct earlier candidates in 22 partial rules, no scanner errors. Six candidates within two retained rules; hold remaining 38 (1 Anime release hover, 18 Settings, 8 Player, 11 Search). Lexical screen, not universal runtime proof.

All six from `gallery/src/styles/13-typography.css`, source Git blob `038938c774b7bc872f62aa7a0eaad511f5a66878`.

| Earlier line | Complete selector | Condition | Delete only | Later surviving line |
|---|---|---|---|---|
| 6 | `.settings-font-tile` | base | `display:flex;` `flex-direction:column;` `align-items:stretch;` `border-radius:13px;` | 64 |
| 31 | `.settings-font-tile` | max-width:530px | `flex-direction:column;` `align-items:stretch;` | 74 |

Unique exact earlier rule strings verified with in-memory replacements; 74 + 42 = 116 ASCII bytes. Preserve every other declaration, later copies, all media rules including 1100px row alignment and 530px layout, 700px specimen grid, gaps/padding, selected border/background/check opacity, inactive hover, keyboard focus, specimen family declarations and reduced-motion rules. Retain entire earlier compact rule and adjacent specimen rule. Do not change differing-value chains, CSS order, other features, typography specimen text or font loading.

## Actual component and behavior
`19c-settings-markup.js` mounts the only .settings-font-tile markup inside #appearance-typography-pane, three [data-font-choice] buttons (system, atkinson, inter). `04c-font-preferences.js` sets state.font, body[data-font], localStorage gallery.font, selected aria-pressed state, local font availability notice and native preference bridge. Specimens use distinct locally installed font families, English uppercase/lowercase/numbers/symbols/similar-looking characters. `19d-settings-search.js` supports real Settings search key font to Typography. Playback > Subtitles uses #subtitle-font in `17c-subtitle-settings-markup.js`; its style and preference state are separate and excluded. No font files or online font requests introduced.

## Required verification after specific approval
- Hash guard both accepted baseline deliverables, exact source blob, two unique full earlier rule strings. Verify only six declarations (116 bytes) removed, all non-CSS bytes and all other source unchanged; exact candidate artifact/tree, deterministic build, immutable checkpoint and independent checks.
- Real mounted Settings > Appearance > Typography in both HTML modes, six themes, both motion preferences. Desktop and both sides of 1100, 710 (Settings side navigation), 700, 530, 440px and narrow 370px. All three actual selected font states at each width; compare all enumerable computed properties, pseudo styles and geometry for three tiles, top/check/specimen and descendants, font notice, card, ancestors, shared navigation. Verify specimen text, font family, selected aria-pressed/check, actual font-change body attribute, fallback notice consistent with local availability, selected/unselected hover, keyboard focus and real activation. Verify actual Settings search deep link, appearance tab keyboard navigation, close/reopen and persisted preference on actual same-origin reload. Do not install fonts or claim native Mac font rendering validated by Linux Chromium; preserve existing locally installed/fallback semantics. Existing Playback/Subtitles regression retained.
- Four mandatory mode/motion shards with exact counts, all three standard groups, both independent post-publish checks, visual review separate. Stop on any mismatch. No other CSS, markup, JS, assets, font files, native branches or numbered release.

No application changes or new checkpoint during review.
