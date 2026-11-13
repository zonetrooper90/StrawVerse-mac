# Gallery JavaScript source map — M4

44 ordered source fragments reassemble the original 333,383-byte classic script exactly. `../build-manifest.json` is the sole assembly order; the builder adds zero bytes. No imports, exports, wrappers, module runtime, or changes to global scope, initialization order or hoisting.

M4 partitions existing feature blocks in place. Numeric prefixes and suffixes describe assembly order, not independent runtime modules; several features remain in multiple nonadjacent files because initialization and execution order must stay exact. Core preferences/navigation, shared render, settings navigation state and startup remain candidates for separately approved M5. Sample fixtures and dormant transfers remain unchanged.

| Order / file | Original script lines | Bytes | Responsibility |
|---|---:|---:|---|
| `01-startup-preamble.js` | 1–11 | 1,129 | Strict mode and initial focus-modality listeners |
| `02-shared-icons-and-escaping.js` | 12–14 | 3,277 | SVG dictionary, icon renderer and HTML escaping |
| `03-data-anime-catalogue.js` | 15–30 | 3,828 | Demo title catalogue |
| `04-core-preferences-and-navigation.js` | 31–557 | 28,065 | Existing preferences, state, route and tab lifecycles (M4/M5 follow-up) |
| `05-shared-cards-and-headers.js` | 558–566 | 1,476 | Shared cards, gallery, search and page header helpers |
| `06-data-watch-history.js` | 567–584 | 3,114 | History storage key, seed generator and sample records |
| `07a-watch-history.js` | 585–974 | 30,990 | History lifecycle, recent preview, episode status and local playback tracking |
| `07b-discover.js` | 975–991 | 1,922 | Discover page |
| `07c-library.js` | 992–1026 | 4,480 | Library page, search cards and dormant transfer flag |
| `07d-downloads-state.js` | 1027–1073 | 4,473 | Download simulation and state |
| `08-shared-timeline.js` | 1074–1080 | 409 | Shared moving-gap timeline calculation |
| `09-downloads-remainder.js` | 1081–1284 | 16,521 | Download progress rendering, actions and grouped notifications |
| `10-data-release-metadata.js` | 1285–1328 | 4,951 | Episode names and connected releases |
| `11a-anime-detail.js` | 1329–1631 | 23,370 | Installment rail, episode controls and detail rendering |
| `11b-player-page.js` | 1632–1688 | 9,255 | Playback entry, page markup and return |
| `11c-detail-dialogs.js` | 1689–1721 | 4,909 | Episode actions, tags and source dialogs |
| `11d-desktop-bridge.js` | 1722–1743 | 1,473 | Desktop settings bridge |
| `11e-player-subtitles.js` | 1744–1800 | 3,820 | Player subtitle tracks and settings |
| `11f-player-motion.js` | 1801–1971 | 8,726 | Play/pause and next morphs, playback neighbors |
| `11g-player-playback.js` | 1972–2146 | 9,311 | Demo/local playback, next state, volume and UI |
| `11h-player-controls.js` | 2147–2273 | 9,624 | Player controls and initialization |
| `11i-core-render.js` | 2274–2359 | 5,877 | Shared render and page event binding; M5 follow-up |
| `11j-dialog-lifecycle.js` | 2360–2517 | 8,207 | Shared dialogs, focus and keyboard scrolling |
| `11k-detail-and-download-entry-points.js` | 2518–2529 | 1,098 | Detail navigation and Downloads folder dialog |
| `11l-settings-navigation-state.js` | 2530–2538 | 380 | Settings navigation state; M5 follow-up |
| `12-subtitle-presets.js` | 2539–2586 | 3,090 | Original image tokens, presets, font definitions and reference-size calculations |
| `13-subtitle-preferences-and-settings-sections.js` | 2587–2617 | 1,558 | Subtitle preference lifecycle and Settings navigation definitions |
| `14-data-source-providers.js` | 2618–2624 | 688 | Simulated source provider and repository records |
| `15-source-state-initialization.js` | 2625–2650 | 1,278 | Source simulation initialization |
| `16-data-source-listings.js` | 2651–2657 | 553 | Simulated provider catalogue IDs |
| `17a-sources.js` | 2658–3009 | 30,378 | Source catalogue, manager, simulated updates and repositories |
| `17b-about.js` | 3010–3149 | 13,219 | About and legal pages and navigation |
| `17c-subtitle-settings-markup.js` | 3150–3205 | 7,022 | Subtitle controls markup and Playback tab |
| `17d-subtitle-preview.js` | 3206–3321 | 6,568 | Subtitle preview geometry, scene and expanded view |
| `17e-color-popover-state.js` | 3322–3324 | 201 | Color editor cancellation state |
| `18-shared-color-conversion.js` | 3325–3343 | 825 | HEX/HSV conversion helpers |
| `19a-color-popover.js` | 3344–3524 | 10,675 | Live color editor and explicit commit/cancel |
| `19b-subtitle-controls.js` | 3525–3650 | 8,066 | Subtitle bindings and preview updates |
| `19c-settings-markup.js` | 3651–3691 | 13,895 | Settings page markup |
| `19d-settings-search.js` | 3692–3788 | 10,851 | Settings search index, results and navigation |
| `19e-settings-navigation.js` | 3789–4019 | 13,909 | Settings lifecycle, section changes, focus and scroll |
| `19f-contextual-search.js` | 4020–4178 | 9,648 | Discover filters and contextual search |
| `19g-library-dialogs.js` | 4179–4206 | 8,918 | Library tag and collection transfer dialogs |
| `19h-bootstrap.js` | 4207–4208 | 1,356 | Final global event registration and startup; M5 follow-up |

M4 baseline: `36c97fc3f9ab924bf23df6bab3b30157c5c785a2`. All four split blocks reconstruct their prior contents exactly; other 15 files retain their existing bytes and manifest positions. Existing image tokens remain in `12-subtitle-presets.js`. Preserve all six themes, navigation, motion, persistence, separate scrollbars, modal lifecycles, native bridge, tests and approved behavior. Actual runtime modules, shared-state refactors or reordering require separate approval.
