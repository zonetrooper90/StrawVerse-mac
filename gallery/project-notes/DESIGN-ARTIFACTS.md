# Gallery design artifacts — verified inventory

This file tracks **approved sketches, HTML mockups, animation experiments, asset SVGs and design notes** independently of numbered Gallery builds.

## Recovery source and scope (2026-11-04)

The exact files below have been verified **inside** the locally integrity-checked `Gallery-HTML-Backup-2026-11-04.zip`, which is saved in the persistent ChatGPT Library at:

`/Gallery Backups/2026-11-04/Gallery-HTML-Backup-2026-11-04.zip`

Its SHA-256 and size are in [VERSION-INDEX.md](VERSION-INDEX.md). **The individual experiment source files are not yet committed to GitHub**; these hashes identify archive members, not GitHub blobs.

| File inside ZIP | Purpose / status | Bytes | SHA-256 |
|---|---|---:|---|
| `Gallery-Player-UI-Experiment.html` | Early player UI sketch / experiment | 25229 | `05514c341f4b18e183602182f6ea8fae2c175ea69eff1b5696ed2831d43c4a65` |
| `Gallery-Player-UI-Experiment-r2.html` | Subsequent player mockup; archive file happens to have same hash as previous | 25229 | `05514c341f4b18e183602182f6ea8fae2c175ea69eff1b5696ed2831d43c4a65` |
| `Gallery-Icon-Morph-Experiment.html` | First icon-morph experiment | 16815 | `34a0a8de95f17d49a16beb33aabd29b8177d243254320c59f02fb308b14873df` |
| `Gallery-Icon-Morph-TrackNext-to-SkipForward.html` | **Approved morph**: Tabler Player Track Next ↔ Player Skip Forward, reversible | 13818 | `f0301976e4af4b3a533a34d0d701fa73b4e426cbf7597615e1dcbafadf7faed9` |
| `player-skip-forward.svg` | Supplied next-episode icon | 373 | `6e4c0c27aadceef4c204aeafa8d7b61d6f4aa66541d90b2669fb265902b28cd5` |
| `player-track-next.svg` | Supplied forward 10-second icon | 378 | `f13b25c9ac378cdf0b6a51da5ad312f61e469e17d32fe67f8e01769113636b7f` |
| `player-track-prev.svg` | Supplied backward 10-second icon | 379 | `f211bae6646a3e7e33d5838fa4580ebc6e2c73ace579869dd5d34f1a290c7425` |
| `Gallery-Watch-History-Locked-Decisions.md` | **Agreed** Recently Watched / Watch History decisions (not a visual mockup) | 2144 | `ba82c1b53e3b5b64b78a2b26171fadf9cdca796e5f71e688e33c4a42eb2c08de` |
| `Gallery-v97-Settings-Handoff.md` | Settings and subtitle design handoff | 6017 | `3932b0746dcb9b03ecdcae62ea6919b43a7f4f7a181df9aea2ac85b432768cac` |
| `Gallery-v97-Integration-Notes.md` | Settings integration notes | 3008 | `6143a0bb2c74f7bcbb34bec3d6bea9bf0efc3ed6d3c76cb922adab198064d9e9` |
| `Gallery-v98-Player-Morph-Notes.md` | Player-morph integration notes | 3110 | `d086fe6725443e544ed2b777c5e0dae469bdbf7178a5a65a4c7bdbc1b23e3ed1` |

## Watch History design state

- Agreed requirements are preserved in the dedicated Markdown file above and in `DECISIONS.md`.
- **No standalone Watch History HTML visual sketch is included in the verified archive.**
- The full Watch History page layout remains **undecided**; do not infer a finalized layout from notes.

## Ongoing backup rule

Whenever the user approves a sketch, design experiment, animation, or relevant source asset:
1. Save an immutable copy under a descriptive filename, including required asset dependencies.
2. Record **what was approved**, what remains exploratory, and what it is related to.
3. Record SHA-256, size and verified storage location here.
4. Prefer committing the actual files to `gallery/design-checkpoints`; if the GitHub transfer is unavailable, store in persistent Library and explicitly document the gap.
5. Continue keeping **numbered Gallery versions** and **standalone experiments** separate. Creating an experiment does not authorize a new numbered build.
6. Never generate/edit images without explicit user approval.

## New Watch History layout experiment — pending user review (2026-11-04)

- File: [Gallery-Watch-History-Layout-Experiment-01.html](../design-experiments/watch-history/Gallery-Watch-History-Layout-Experiment-01.html)
- Status: **interactive prototype for review, NOT yet approved or integrated**; not a numbered Gallery release.
- Backups: complete HTML committed to this `gallery/design-checkpoints` branch **and** saved to persistent ChatGPT Library at `/Gallery Backups/Design Experiments/2026-11-04/Gallery-Watch-History-Layout-Experiment-01.html`.
- Source file size: **37,987 bytes**
- SHA-256: `ab170c5716b773832ac963201266a5ab7d77a33d3e15c9022b3d0b31a5f5c737`
- Contains: full season-level list, short/long expandable episode management (100-episode test season), two custom fading draggable scrollbar overlays (main page and inner episode lists) matching Gallery v99 behavior, sort/status filters, historical year/title search priority, separate-season completed status, explicit Remove and session-long Undo, and representative Library/Discover routing notices.
- Browser checks (Chromium): long-list capped at 252px with all 100 rows available; hidden native scrollbar and fading overlay; manual status toggles; sorting; date-search grouping with deduplication; filters; removal/Undo; reset on navigation; 390px width without horizontal overflow; no JavaScript page errors.
- Scope: illustrative offline demo data only; does **not** modify Gallery v99 or implement real playback-history persistence.

## Watch History layout experiment 02 — two-column episode list (2026-11-04)

- File: [Gallery-Watch-History-Layout-Experiment-02.html](../design-experiments/watch-history/Gallery-Watch-History-Layout-Experiment-02.html)
- Status: **awaiting user visual review**; standalone experiment only, not integrated into Gallery v99.
- Exact HTML also saved to ChatGPT Library at `/Gallery Backups/Design Experiments/2026-11-04/Gallery-Watch-History-Layout-Experiment-02.html`.
- Source file size: **38,815 bytes**
- SHA-256: `01d6d8d983c95f1aff0c6b39e74be41af512c78de7274ba69ad8a9f98fb7046a`
- Differences from Experiment 01: two equal-width, unboxed episode columns with episode numbers flowing left-to-right across rows; subtle central divider with padding, constrained to the episode list; paired rows share the same 252px (six-row) scrolling region; responsive one-column fallback under 821px; scroll-to-latest now calculates a row index from the actual column count. Original disappearing overlay scrollbar, playback progress markings, interactive status corrections, Undo, search, sorting, and filters stay intact.
- Checks: Node syntax validation; Chromium at widths 1400, 900, 760 and 390px with no JavaScript errors or horizontal overflow; two-column vs one-column threshold; center-divider visibility; 100 episodes reachable; 12-episode list shows without an inner scrollbar on desktop; thumb appears while scrolling and fades away; episode status toggles, removal/Undo, sorting and filters work.

### Experiment 02: user-recorded interaction defects (2026-11-04; awaiting revision approval)

- **Flashing on episode-status changes:** toggling a watched control updates the season count but causes the entire expanded episode list to re-render and replay its expansion/fade animation. A status correction should update only the necessary row and season summary without restarting the panel's animation, moving the scroll position, or affecting the fading scrollbar.
- **Shifting checkbox/status control:** the watched-state labels (`Watched`, `Not watched`, `Partially watched`) have differing text widths, causing the checkbox position to move horizontally after clicking. Keep each status control at a stable X-coordinate by reserving fixed label space (sufficient for the longest state label), without changing the existing two-column layout or icon-before-text direction.
- User identified both problems in a screen recording and confirmed both were the intended feedback. **Do not treat either fix as implemented or approved for a new numbered experiment yet.**

## Watch History layout experiment 03 — interaction fixes (2026-11-04)

- File: [Gallery-Watch-History-Layout-Experiment-03.html](../design-experiments/watch-history/Gallery-Watch-History-Layout-Experiment-03.html)
- Status: **awaiting user review**; standalone experiment, not integrated into Gallery v99.
- Backed up to GitHub `gallery/design-checkpoints` and persistent ChatGPT Library at `/Gallery Backups/Design Experiments/2026-11-04/Gallery-Watch-History-Layout-Experiment-03.html`.
- Verified source file size: **40,372 bytes**; SHA-256: `4a02f2834ac84869ef03f82eb83a1a838feb9a8367a374e3bf4084cf367f4508`.
- Relative to Experiment 02: **(1)** toggling an episode changes only the relevant episode DOM/state, the season summary and expanded header count; no full-page/expanded-list reconstruction, no panel flash, and preserved episode scroll instance/position/focus. **(2)** fixed 151px status control with consistent icon-before-text placement across `Watched`, `Partially watched`, `Not watched` so the checkbox does not shift.
- Retains two-column layout with center divider, six-row scroll cap, responsive single-column layout, fading custom overlay scrollbars, search, filters, sorting, separate removal and Undo.
- Chromium interaction tests passed at 1400, 900, 760, and 390px: no horizontal overflow or JavaScript exceptions, status controls maintain pixel position after toggling, panel node identity persists, scroll position remains stable, correct one/two-column responsive behavior. Also tested switching a season between Completed and In Progress without collapsing the panel.
- Do not assume visually approved until the user reviews it.

## Gallery v100 — approved integration of Watch History Experiment 03 (2026-11-04)

- The user approved integrating the Experiment 03 Watch History UI into a new **Gallery-v100.html** based on v99, plus correcting the player page's persistent scrollbar.
- The full **Gallery-v100.html** is preserved in personal Library at `/Gallery Backups/2026-11-04/Gallery-v100.html`; size **6,812,924 bytes**, SHA-256 `0aac13b097dc0a10b19699704687c09ffc5f3fe9407f757e3695ea45b57fe283`.
- Full v100 GitHub upload was unsuccessful and path verified absent. Reconstructible JS, CSS, build script and [README](../releases/v100-integration/README.md) are committed in GitHub under `gallery/releases/v100-integration/` and duplicated in Library under `/Gallery Backups/2026-11-04/v100-source/`.
- Implemented: Recently Watched strip and View History tile on Discover; full Watch History integrated into Gallery header/navigation/search, episode status interaction without panel flashing or moving checkbox, two-column layout with center divider and scroll cap, searchable viewing years, history status filtering, chronological sorting, pending removals and session-long Undo.
- Player-page `scrollbar-gutter:stable` removed; native permanent scrollbar hidden and existing window-level overlay scrollbar used (fades on inactivity). Verified in Chromium for active scrolling/fade and no width shift.
- Chromium verified viewports: History **1400/900/760/390 px**; player **1400/900/500 px**. No JavaScript page errors. Other v99 behaviors were preserved by modifying the checked v99 snapshot rather than remaking the UI.
- Prototype caveats: initial Watch History fixture rows are **simulated**, video provider sources are not connected, and actual provider playback / macOS app packaging have not been implemented. Local-video playback integration in this HTML can record positions on the device only.
- User has authorized **v100 creation**, not retroactive rewriting of v99 or automatic approval of any future v101 design changes.

## Recently Watched Animation Lab 01 — timing and easing comparison (2026-11-05)

- Full standalone HTML: [Gallery-Recently-Watched-Animation-Lab-01.html](../design-experiments/recently-watched/Gallery-Recently-Watched-Animation-Lab-01.html) (verified against persistent Library source).
- Backup: `/Gallery Backups/Design Experiments/2026-11-05/Gallery-Recently-Watched-Animation-Lab-01.html` (21,938 bytes).
- **Status:** user requested comparative animation experiment. Four presets: original v101 (320/320ms, no intent delay); Balanced (460/330ms, 85ms intent); Soft Glide (550/375ms, 100ms intent); Gentle Spring (490/335ms, 85ms intent), plus custom duration/intent sliders and easing choices. User has **not selected/approved a winner**.
- CSS-only placeholder covers (no image generation); cover dimensions 66×96px, emerging info panel 84px high vertically centered, adjacent items and equal-size View History tile move aside without scroll/pagination. Transitions interrupt rather than queue; per-preset Sweep demo tests rapid switching. Keyboard focus and reduced-motion rules included.
- Validated with Chromium at 1440/900/560/390/320 widths, zero JS errors/overflow, steady cover position, 84px panel height, History tile stays in bounds, sweep actions complete, and custom slider updates work. Gallery v101 untouched.

### Animation Lab 01 — incorrect hover target during retraction (reported 2026-11-05)

- The user showed that, after hovering cover 1 and moving to cover 2 during retraction, **cover 4 sometimes opens instead** in the **Balanced** and **Soft Glide** presets; the original v101 hover behavior does not exhibit this. This is a **hover-targeting defect**, not accidental retraction or the browser tooltip. Do not describe it as merely too fast/too slow.
- Potential mechanism verified in lab source: Balanced waits **85ms** and Soft Glide **100ms** before calling `activate(slot)` on `pointerenter`. Simultaneously each active `.slot` animates its flex-basis, shifting the positions of other covers under the pointer. These two mechanisms can allow stale or unintended pointerenter targets during layout movement. The exact browser event sequence still needs explicit regression testing.
- **Fix direction for next test (NOT YET IMPLEMENTED):** make cover selection immediately responsive and robust to cover positions changing during retraction; remove or confine initial hover delay, guard against stale timers and activations, and check current real pointer target when necessary. Keep the selected easing/duration interruptible; avoid queued animations. Remove unwanted native browser `title` tooltips from covers while retaining accessible labels.
- User has not approved a new numbered Gallery version or a specific animation preset; Gallery v101 is unchanged.

## Recently Watched Animation Lab 02 — cursor-targeting corrections (2026-11-05)

- Full standalone source: [Gallery-Recently-Watched-Animation-Lab-02.html](../design-experiments/recently-watched/Gallery-Recently-Watched-Animation-Lab-02.html)
- Backed up to Library: `/Gallery Backups/Design Experiments/2026-11-05/Gallery-Recently-Watched-Animation-Lab-02.html` (**24,512 bytes**, SHA-256 `543c3ce15a3710e1105cd6ca6046c82568d69f04d2e52a3a165685b2642bd93a`). The complete GitHub HTML was fetched and verified identical to Library source.
- **Status: new interactive experiment awaiting user review; v101 is unchanged**. No animation preset has yet been selected as final.
- Presets retain the original four timing/easing comparisons plus live custom controls. Balanced uses 460ms open / 330ms close / 85ms **initial idle hover**; Soft Glide 550ms / 375ms / 100ms initial idle hover. Switching between covers is immediate, even while another panel retracts; motion still uses the chosen curves.
- Fix: do not use pointerenter on moving poster elements as a signal to activate them; `pointermove` from the **actual moving pointer** sets the target. Small incidental movements during layout transitions are ignored until sufficient genuine pointer travel. A pending initial-hover callback is canceled or validity-checked against the currently pointed-at poster before activation. This prevents the demonstrated cover-2-targeted / cover-4-opens defect.
- Removed native browser `title` tooltips from posters and View History while retaining `aria-label` accessible names.
- Automated Chromium checks at 1440, 900, 560, 390, 320 pixels: first-to-second transition remains targeted correctly after retraction finishes (where two covers fit); no unexpected later switch, no horizontal overflow, no page JS errors. Balanced and Soft Glide checked by direct pointer movement; sweep demo still completes. Do not claim native app integration or final user acceptance.


## Recently Watched Animation Lab 03 — coordinated row expansion (2026-11-05)

- Standalone source: [Gallery-Recently-Watched-Animation-Lab-03.html](../design-experiments/recently-watched/Gallery-Recently-Watched-Animation-Lab-03.html), committed in full on `gallery/design-checkpoints`, fetched back and verified byte-for-byte against the Library source.
- Library backup: `/Gallery Backups/Design Experiments/2026-11-05/Gallery-Recently-Watched-Animation-Lab-03.html` — **28,777 bytes**; SHA-256 `3ebc20654c0d22a586fbe62f87d0991933b681057a7ed44ba599c410520f9db6`.
- **Status: awaiting user review; Gallery v101 unchanged**. The user has approved fixing the accordion motion but has not yet approved a particular animation preset or a Gallery v102 version.
- Fixes Lab 02's row-wide accordion/bounce: a single coordinated frame-by-frame transition *conserves total expanded width* when switching between covers. The space formerly occupied by one info panel transfers to the next, so the trailing covers and View History tile stay still. Row expansion occurs on initial hover; contraction occurs on exit from the active-cover area.
- When a user switches while the row is still initially opening, its total expansion proceeds smoothly toward the full width rather than shrinking first; switching is interruptible and does not queue. A single easing progress drives redistribution, honoring each preset's opening curves. The Spring curve is bounded in the width distribution to prevent overshoot/overflow, while the individual panel remains able to use spring easing.
- Preserves the earlier pointer-movement targeting correction, no browser tooltips, keyboard focus, reduced-motion support, 66×96px fixed covers, 84px vertically centered panels, equal-size View History tile, and four comparison presets plus custom controls.
- Chromium validation: Balanced and Soft Glide cover-1-to-cover-2 transitions at 1440px kept trailing tile X and total extra width constant within **0.02px** throughout the switch. Gentle Spring rapid switches checked at 1100/900/560/320px. At 1440/390px, responsive and hover target checks passed; Sweep demo and custom duration/easing controls passed; no JavaScript errors.
- This is an **animation lab**, not a macOS app release or a native playback integration.

### v102: stale top navigation pill after opening Library anime via Recently Watched (reported 2026-11-05)

- User confirms Gallery v102 visual experience looks good, but clicking a **Recently Watched** cover for an anime already in **Library** correctly navigates to its details while the selected top navigation indicator stays on the previous tab until the user moves their cursor over the top navigation.
- **Cause verified in v102 HTML:** the preview click delegates to `whEnter(); whOpenTitle(r)`. `whOpenTitle` selects `r.library ? 'library' : 'discover'`, updates `state.view` and calls `updateActiveTab(targetView)`, then `showDetail(r.galleryId)` and possibly `render()`. Unlike the ordinary `setView(view)` navigation path, it **does not call `updateTabIndicator()`**, which controls the animated top-nav pill's target/position. Pointer-enter/move on the nav then calls `updateTabIndicator()`, explaining the late visual correction.
- **Proposed narrowly scoped correction (NOT YET IMPLEMENTED):** synchronize the nav pill immediately with the newly selected view in `whOpenTitle`, using the existing indicator update path, without requiring a pointer event. Verify the analogous Discover route, keyboard focus, no misplaced animation/label, and that the Recently Watched Soft Glide mechanics are untouched.
- **Superseded by v103:** user authorized the fix, which was implemented and verified in the new v103 HTML; v102 itself remains unchanged.


### v103: stale nav pill correction implemented and tested (2026-11-05)

- User explicitly approved the isolated fix, and v103 now calls `updateTabIndicator()` after `whOpenTitle` has rendered the destination anime detail; the top selected tab and pill move together without moving the pointer.
- A/B reproduction: v102 opening a Library anime via Recently Watched left the pill on Discover; v103 targeted Library immediately. Also verified the reverse Discover route from Watch History at three viewport widths.
- The full v103 HTML is in persistent Library and the exact reproducible [v102→v103 patch](../releases/v103-integration/Gallery-v102-to-v103.patch) on GitHub. v102 is untouched. This is a verified fix in an HTML prototype, not yet a packaged native app.


### Gallery × Glisse — three-component study (2026-11-05)

- User wants to explore **selected Glisse enhancements** without a general Liquid Glass makeover, initially **Top Bar** (Glisse actually calls it `Tab Bar`), **Segmented Control**, and **Button**.
- [Standalone three-component comparison](../design-experiments/glisse/Gallery-Glisse-Component-Study.html) built using Gallery v103 colors and representative controls. Left: Gallery v103-styled controls; right: self-contained, animated **Glisse-inspired approximations**. It is **not an actual Glisse React integration**, does not implement the library's full optical refraction, and cannot establish real-WebKit performance or fidelity. The official live examples remain at `https://glisse.kelvinzhang.ca/`.
- Interactions: three-tab Discover/Library/Downloads navigation, Watch History All/In Progress/Completed segmented selection, primary/secondary/icon buttons; optional Gallery Neon/Midnight/Paper theme switching. The right side supports spring-lens selection, press-and-drag selection, elastic press feedback and frosted appearance. JavaScript remains self-contained without external dependencies.
- Browser tested at 1440px, 900px, 390px and 320px (buttons, tabs, segmented control, themes and overflow) and tab-bar drag selection verified separately; no JavaScript errors. No screenshots/images were generated.
- Artifact backup: `/Gallery Backups/Design Experiments/2026-11-05/Gallery-Glisse-Component-Study.html` in persistent Library, 22,747 bytes, SHA-256 `69506fd65645fc557ca7e0fe8d11f02af449f579dbea2ea706d1d157df350674`. GitHub source committed and fetched back byte-for-byte.
- **Status: exploratory, awaiting user assessment**. Keep Gallery **v103 unchanged**. No new numbered Gallery release or actual Glisse React dependency was introduced; choose specific components and integration approach only after user review.


### Gallery × daisyUI — Component Lab 01 (2026-11-05)

- User selected daisyUI for its **themes, range of styled controls and component library**, and is open to replacing the current Gallery themes with a set specifically designed for daisyUI, but has **not authorized any replacement in the actual Gallery app**.
- [Standalone design lab](../design-experiments/daisyui/Gallery-daisyUI-Component-Lab-01.html) with version-pinned **real daisyUI 5.7.48 component and theme CSS** from jsDelivr, no React or Tailwind browser script. Compare Gallery v103-style reference controls and daisyUI, switch seven themes (custom Gallery Violet, Night, Dim, Dracula, Abyss, Synthwave, Silk), and try a gallery-oriented component shelf. Gallery Violet can be color-edited interactively.
- **Important limitation:** while the HTML file itself is standalone, component styling currently **requires internet access** to fetch daisyUI stylesheets. CDN is for evaluating the library, not for final macOS distribution; a real integration must bundle selected CSS locally. Browser interaction tests passed at six widths but the present network-restricted test environment did **not** allow inspecting the actual CSS rendering. Do not claim finished production compatibility or visual verification.
- The v103-style reference is intentionally simplified, not pixel-identical or connected to the actual Gallery app.
- Archive: persistent Library `/Gallery Backups/Design Experiments/2026-11-05/Gallery-daisyUI-Component-Lab-01.html`, 40,084 bytes, SHA-256 `f4a86d2f705b75168ea0cf29d326c5a7795151ba42e17810f62a180dcff79f09`; full HTML committed and fetched back byte-for-byte on GitHub branch `gallery/design-checkpoints`. [README](../design-experiments/daisyui/README.md) captures scope and recovery.
- **Gallery v103 unchanged and approved baseline.** No v104 built or approved. Await user assessment of the theme/control options.


### Gallery × daisyUI — Component Lab 02 (2026-11-05)

- User reported Lab 01 stylesheet error in **Microsoft Edge opening a downloaded local HTML** on a work PC. They verified both pinned CDN CSS URLs directly open and display CSS. The original Lab 01's computed-style check could report a false failure, so merely showing the warning does not establish that the network is blocked.
- [Lab 02](../design-experiments/daisyui/Gallery-daisyUI-Component-Lab-02.html) replaces false computed-style detection with clearer sheet/fetch diagnostics, adds a **Save offline HTML** exporter and an optional local CSS-file importer. The exporter stores the **actual fetched daisyUI v5.7.48 component/theme CSS** verbatim inside the downloaded `Gallery-daisyUI-Component-Lab-02-Offline.html`, with no external CSS requests on later opens. The Lab 02 starter itself still needs a one-time network connection or manual file import to capture the real stylesheets.
- Browser tests simulated both successful CSS delivery and complete network failure: online bootstrap → offline export → offline reopen produced **zero network requests** and no JavaScript errors, with themes and responsive layout intact; manual import fallback also passed. Real CDN visual rendering remains to be confirmed on user's machine; tests did **not** use actual remote CSS.
- Backed up Library `/Gallery Backups/Design Experiments/2026-11-05/Gallery-daisyUI-Component-Lab-02.html` (49,466 bytes; SHA-256 `4005cefb79022083154a551c3decf3f323d9f3ef91aa24e298d8ca6c0ffd7119`). Full GitHub source byte-for-byte verified. [Lab notes](../design-experiments/daisyui/README.md).
- **Gallery v103 is unchanged**; user has not yet selected replacement daisyUI components or themes.


### Gallery × daisyUI — Neutral Component Lab 03 (2026-11-05)

- User requested a **completely neutral theme** for judging daisyUI components, without approving a permanent theme change. This experiment builds on Lab 02 rather than integrating anything into Gallery.
- Full HTML: [Neutral Component Lab 03](../design-experiments/daisyui/Gallery-daisyUI-Neutral-Component-Lab-03.html). Default Neutral Dark, alternate Neutral Light. Both use all-grayscale daisyUI-compatible custom tokens and the same geometric/radius/depth values, so differences in shapes do not confound the light/dark color comparison. Surrounding lab and Gallery-style comparison surface also neutralized. Previous seven themes retained.
- Same actual v5.7.48 vendor CSS loader + offline export from Lab 02; starter is not fully offline until vendor CSS is captured and embedded. The test environment could not fetch the CDN, so visual rendering with actual daisyUI CSS still awaits user review. Tested five widths for neutral tokens, theme switch, interaction, editor isolation, and no overflow/JS errors.
- Library backup `/Gallery Backups/Design Experiments/2026-11-05/Gallery-daisyUI-Neutral-Component-Lab-03.html` (**54,738 bytes**, SHA-256 `da8541926be0f257f6ecc87edb50f86e1cc2fa47b44d2363be136d1291409e87`). Full HTML committed to GitHub and fetched back byte-for-byte; see [experiment README](../design-experiments/daisyui/README.md). Gallery **v103 remains unchanged**.


### Gallery × daisyUI — Full-App Design Preview 01 (2026-11-05)

- The user requested an actual **version of Gallery with daisyUI** because isolated component labs were difficult to judge. Explicitly created as an **unnumbered standalone full-app preview**, not v104. Approved current baseline **v103** remains untouched.
- [Full-App Preview documentation](../design-experiments/daisyui/Full-App-Preview-01-README.md). Full HTML in persistent Library: `/Gallery Backups/Design Experiments/2026-11-05/Gallery-daisyUI-Full-App-Preview-01.html` (6,841,601 bytes, SHA-256 `0595c6e02f39203266da7e9b4e21c5a7c4d84e02cd232afd949a296e1488a431`). GitHub only stores the experiment documentation, **not the complete HTML or patch**.
- Based on the exact verified v103 HTML; overlays daisyUI v5.7.48 custom/official theme tokens and component geometry onto the existing app, changes the Settings theme choices to Gallery Violet, Night, Dim, Dracula, Abyss, Neutral Dark and Silk, and adds a compact experimental theme selector + theme-shape lock. Real daisyUI 5.7.48 CSS linked from version-pinned jsDelivr (CSP allowlisted), with a small actual daisyUI class-based control sample in Settings. **Most Gallery component markup and navigation/animation logic remains unchanged** and uses theme-linked adaptations; this is not a complete daisyUI conversion.
- Main app navigation, Settings, and theme behavior pass offline Chromium checks at five viewport widths; no JS errors or document overflow. Remote CSS fidelity cannot be verified from the network-limited test environment, and the preview needs an internet connection for real daisyUI vendor component styling. The embedded official token values allow offline palette inspection.
- The local 31,507-byte unified patch from v103 was applied and produced the exact preview SHA-256; the complete prototype was backed up to Library. The user has **not yet reviewed or selected any style or theme**. Future integrations require discussion and approval.
