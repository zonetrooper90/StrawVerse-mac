# Gallery maintainability audit — 2026-11-12

## Scope and baseline

Read-only inspection of the current Gallery prototype, not the native app. Branch: gallery/development-clean. Reviewed repository commit f94ee84453ef77add4dbac69c59d265b4f016e3e. Canonical HTML blob b525462cf9686a26d580f980d99d26e43d251022. Immutable checkpoint 2026-11-12-subtitle-simple-intensity-custom-palette. SHA-256 8cd1f045580b32d98d5d70e2da6e0a9f2dcac744c7a011f2ff850d1a6ddc45fb; 6,952,404 bytes. Both existing GitHub CI checks passed on the reviewed commit. Local read-only inspection used the exact SHA-256- and Git-blob-matched delivered bytes; no edits to a chat attachment or canonical HTML. Source and immutable archive are unchanged.

## Method and limits

Parsed CSS using tinycss2 (qualified rules, including nested media/supports/container/layer blocks; keyframes counted separately). Compared exact selectors within identical conditional contexts and declaration lists. Lexically compared CSS class names with the non-CSS source, including dynamically generated markup. Parsed JavaScript function declarations and identifiers with the TypeScript parser. Inspected the actual rendering and migration code. Reviewed the live GitHub tree and workflow inventory. Sampled Chromium CSS rule usage at 1600x1000 and 700x850 using reduced motion, all six themes, primary pages, search, Watch History, anime details, demo Player, Settings sections, subtitle styles, Custom color picker and expanded preview. Each viewport completed 28 scripted interactions with no page errors after correcting the exploration's selector choices. The sandbox blocked navigation to a routed test origin; the successful browser sampling loaded the same unmodified bytes into an in-memory document. This was not a persistence, full animation, native macOS or visual-equivalence audit. Browser CSS usage is supporting evidence only: a rule absent from sampled usage may still support hover, focus, rare data, modal, responsive or accessibility states. JS profiler results included tooling scripts and are not used as a dead-code count.

## Inventory

- 2,484 CSS qualified rules; 8,345 parsed declarations; 13 keyframes.
- 232 groups with repeated selector and conditional context, including 17 groups with identical ordered declaration lists. Repetition alone is not redundancy: an intervening rule can intentionally reset a property.
- 711 distinct CSS class tokens; 162 not found as literal standalone tokens outside CSS. These are candidates, not proof of dead code: generated names can evade literal matching.
- 278 named JavaScript function declarations; every declaration name has at least one other identifier occurrence in the parsed source. No safe bulk function deletion inferred; identifier references do not prove reachability.
- Two embedded PNG data URLs (3,442,084 + 2,873,648 base64 characters): approximately 90.8% of total HTML bytes. Both are required shrine preview art. Preserve the original assets.
- Browser sampling matched 1,322 distinct CSS rule ranges across the two viewports. This is not an unused-rule percentage: browser reporting and parser scopes are not identical, and rare routes were not exhausted.

## Candidate register and proposed order

### C1 — Obsolete subtitle layout CSS (highest priority)

Source around lines 1505–2466 contains historical v82–v96 and A2–A27 workbench rules; current Soft Futuristic subtitle workbench begins around line 3455, actual markup around line 7408. Old .subtitle-workbench, .subtitle-preview-card, .subtitle-experiment-font-panel, .subtitle-experiment-preview-layout and .subtitle-settings-grid classes are absent as standalone names in non-CSS source. They are strong candidates for individual selector removal. Do not delete the whole historical block: .subtitle-stage, .subtitle-stage-image, .subtitle-stage-night, .subtitle-preview-caption, color popover, expanded preview modal and shared rendering styles still participate in active markup. Prove each selector branch; split mixed selector lists, preserving any live branches. Preserve exact A7/A28 stage dimensions, both responsive layouts, three intensity choices, palette indicator, old saved preference migration, day/night synchronization, and expanded preview.

### C2 — Retired theme CSS

Old body[data-theme="neon"], body[data-theme="midnight"] and body[data-theme="paper"] definitions at lines 5–7, Player remaining-track colors around 390–393, and Paper Lantern dialog/tab overrides around 526–554. The active SOFT_FUTURISTIC_THEMES array contains ocean, twilight, ember, slate, glacier and verdant; theme reading and desktop preference import validate against it. Settings only offers the six current themes. Candidate remove old-theme-only rules from the prototype, after confirming no dynamic source assigns retired names. Do not remove separate native app theme support or change migration behavior. Test all six themes and invalid stored theme fallback.

### C3 — Exact duplicate rules / unused keyframe

17 exact duplicate groups, including .episode-copy (min-width:0, lines 174 and 848), .episode-toolbar .episode-heading h2 (799/856), .settings-back:hover (1045/1302), #playback-subtitles-pane (1954/3455), and repeated mobile Downloads status/track grid-area declarations (3293/3421 and 3294/3422). Verify intervening cascade before merging even exact duplicates; preserve source-order and responsive specificity. The settings-enter keyframe (around line 1080) has no reference outside its definition in CSS or JS, so is a particularly small removal candidate. Do not remove gallery-surface-in: render() still adds surface-enter when applicable.

### C4 — Legacy Downloads and Anime detail CSS

Downloads: .download-row, .download-group-art, .download-episode-main, .download-episode-actions are absent as standalone tokens outside CSS, while current downloads markup uses sf-dl-* (around line 5436). Anime Details: .connected-season-card, .connected-season-list, .connected-related-button, .playback-screen, .playback-screen-center and similar earlier layout selectors are candidates. Inspect generated names and mixed selectors first. Protect actual progress tracks, hover/focus, pause/cancel/retry/dismiss/undo states, season selection, Sub/Dub, small viewport layout and keyboard interactions. Do not revisit approved scroll handoff/expansion.

### C5 — JavaScript and shared mechanisms (investigation, not deletion)

No isolated unreferenced named functions identified. Two independent custom scrollbar visual/lifecycle implementations (main workspace overlay, around 4461 onward; Watch History inner overlay, whAttachInner around 5028) use similar fade/drag math, but target different scroll containers and approved native behavior. Their similarity is not a defect. Defer consolidation unless evidence supports a simpler implementation with identical behavior. Separate Player snapshot and coordinated secondary page fades are deliberate approved behavior, not redundant. Keep disabled GALLERY_COLLECTION_TRANSFER_UI_ENABLED and transfer handlers, sample data and demo controls, legacy subtitle/color/volume migration, provider simulations and optional desktop bridge. Investigate icons, data and nested callbacks only after coverage improves; do not delete based on the profiler.

### C6 — Assets and repository infrastructure

Two PNGs are intentional. No evidence for deleting artwork; no optimization/reencoding without explicit approval. Standalone historical HTML, archive chunks, deliverables, immutable checkpoint parts and experiments are recovery artifacts and not runtime payload. Preserve all historical files. Existing applied change requests under gallery/changes/pending may be confusingly named, but editing them triggers the publisher; leave untouched until a separately approved infrastructure plan. Historical test_ac_motion.py tests a superseded animation checkpoint, not a current regression. Preserve historical test and do not run it as a current requirement. Current read-only workflows and generic controlled publisher remain necessary. Native build/diagnostic/preview workflows and gallery/app + electron files are a separate integration surface, not dead prototype code. PROJECT-CONTINUITY.md still names the old branch; README/native playback docs refer to older app builds, and the visible Watch History note says v103. Correct documentation separately; don't silently change app behavior or version.

## Proposed cleanup process (not yet authorized)

1. Stage 1: only strongly supported obsolete subtitle selector branches, old-theme-only CSS and the unreferenced settings-enter keyframe; separate or narrow patches. First capture relevant pre-change browser computed styles and geometry; compare equivalent states after changes at both full and compact widths and all six themes.
2. Stage 2: exact duplicate cascade review, then obsolete Downloads/Anime detail selectors with additional state/viewport regression tests.
3. Stage 3: JS investigation, asset and infrastructure review; no speculative refactoring of scrolling or animation. Keep intentionally retained functionality.
4. After cleanup, implement the selected direct dithering approach as a separate approved change; keep stationary background geometry and theme colors. Light is preferred trial, Fine fallback. See experiment commit f94ee84453ef77add4dbac69c59d265b4f016e3e.
5. Each actual HTML change requires approval, pre-change verified checkout, narrow patch, regression tests, new immutable checkpoint, both independent remote checks and checksum-matched attachment. Compare normal and reduced-motion behavior, persistence/migrations and manual macOS display feel as appropriate. No numbered build or cleanup has been made here.

This report is an initial prioritized audit, not a comprehensive proof of all possible unused code. No HTML code, image assets, workflows or tests were changed.


## Follow-up re-audit — accepted adaptive preview baseline
Reviewed active commit `4589c3602cc204fedb145055c3be6cf4a542d07a`, immutable checkpoint `2026-11-12-adaptive-subtitle-preview-controls` (SHA-256 `6dbb668ae63dea26bd1ed03c70db20596c2b96f85a6466c428fdc3b9741aba55`). Integrity logs and the exact build's two independent checks passed. C1 already removed 262 rules. Current structural scan: 2,230 ordinary CSS rules, 205 repeated selector/context groups, 14 identical-declaration groups, 13 keyframes. C2: 15 exclusive retired-theme rules (2,284 source characters excluding whitespace between rules): 3 theme definitions, 4 Player rules, 3 tab rules, 5 dialog scrollbar rules. Active theme selection only supports ocean/twilight/ember/slate/glacier/verdant; retired IDs still appear in Settings search terms and unrelated demo titles/data, which remain intact. C3: settings-enter has only its definition, no other textual reference; retain all other keyframes. The user approved only C2 and the unused C3 keyframe. The 14 duplicate groups remain for separate cascade review; do not bulk deduplicate. No source authority change. Proposed comparison uses immutable before/after full and lightweight HTML across all six active themes at 1600 and 700px, sampling navigation, Player and expanded dialog computed styles, in addition to existing regressions. Notification work deferred.


## C2 and C3 keyframe — implementation verified
Build `bac24f367ff7ad087b03ed674269b00feafed8db`, checkpoint `2026-11-12-retired-theme-css`, SHA-256 `062e6a921b2f252c069c50159f1170ce4ef172bb5bc879b2871c6d0cef0dc5ae`, 6,915,281 bytes. Removed exactly 15 retired-theme CSS rules and the unreferenced settings-enter keyframe, 2,407 bytes in each build. Publisher run 43322672385 and independent integrity/browser runs 43323510875/43323514826 passed. Exact sampled computed styles matched prior immutable checkpoint in navigation, Player and expanded dialog across all six themes, two widths and both build modes. Original asset hashes unchanged. User visual acceptance pending; no additional duplicate-rule removal authorized.
