# Gallery JavaScript source map — M3

These 19 ordered source fragments reassemble the pre-M3 333,383-byte classic script exactly. `../build-manifest.json` is the sole assembly order; the builder adds zero bytes. No imports, exports, wrappers, module runtime, changes to hoisting or initialization order. The output still uses one classic script and all existing browser-test globals remain available.

M3 extracts reusable utilities and safe data blocks in place, not a feature redesign. Larger transitional fragments are intentionally retained until M4/M5; do not move a declaration across fragments merely to group related code. Several sections contain stateful initialization and cross-feature references. Data files may contain constructors or constants, not new independent services; sample fixtures remain simulations.

| Order / file | Original script lines | Bytes | Responsibility |
|---|---:|---:|---|
| `01-startup-preamble.js` | 1–11 | 1,129 | Strict mode and initial focus-modality listeners |
| `02-shared-icons-and-escaping.js` | 12–14 | 3,277 | SVG dictionary, icon renderer and HTML escaping |
| `03-data-anime-catalogue.js` | 15–30 | 3,828 | Demo title catalogue |
| `04-core-preferences-and-navigation.js` | 31–557 | 28,065 | Existing preferences, state, route and tab lifecycles (M4/M5 follow-up) |
| `05-shared-cards-and-headers.js` | 558–566 | 1,476 | Shared cards, gallery, search and page header helpers |
| `06-data-watch-history.js` | 567–584 | 3,114 | History storage key, seed generator and sample records |
| `07-history-and-primary-pages.js` | 585–1073 | 41,865 | History lifecycle, Discover/Library and initial Downloads logic (M4 follow-up) |
| `08-shared-timeline.js` | 1074–1080 | 409 | Shared moving-gap timeline calculation |
| `09-downloads-remainder.js` | 1081–1284 | 16,521 | Download progress rendering, actions and grouped notifications |
| `10-data-release-metadata.js` | 1285–1328 | 4,951 | Episode names and connected releases |
| `11-detail-player-and-dialogs.js` | 1329–2538 | 86,050 | Anime detail, Player, bridge, render and dialogs (M4/M5 follow-up) |
| `12-subtitle-presets.js` | 2539–2586 | 3,090 | Original image tokens, presets, font definitions and reference-size calculations |
| `13-subtitle-preferences-and-settings-sections.js` | 2587–2617 | 1,558 | Subtitle preference lifecycle and Settings navigation definitions |
| `14-data-source-providers.js` | 2618–2624 | 688 | Simulated source provider and repository records |
| `15-source-state-initialization.js` | 2625–2650 | 1,278 | Source simulation initialization |
| `16-data-source-listings.js` | 2651–2657 | 553 | Simulated provider catalogue IDs |
| `17-sources-settings-and-preview.js` | 2658–3324 | 57,388 | Sources, About, subtitle preview and Settings logic (M4 follow-up) |
| `18-shared-color-conversion.js` | 3325–3343 | 825 | HEX/HSV conversion helpers |
| `19-settings-search-and-bootstrap.js` | 3344–4209 | 77,318 | Color popover, Settings, search, transfers and final startup (M4/M5 follow-up) |

Baseline: `3ae67a30f56918c747ef0abf92352a279bd2275b`. Strict mode, SVG geometry, HTML escaping, moving-gap timeline, HEX/HSV formulas, all catalogue and provider data, subtitle defaults, image tokens, persistence keys and event registration are unchanged. Separate route/Player transitions, scrollbars, modal lifecycles and desktop integration remain intact. No function is deleted or renamed. Existing image tokens are in `12-subtitle-presets.js`. Before future feature extraction, inspect the original boundaries and interdependencies and require exact reconstruction again. Actual module interfaces or shared-state refactors require separate approval.
