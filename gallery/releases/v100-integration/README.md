# Gallery v100 integration and recovery

**Approved by user (2026-11-04)**: integrate Watch History Layout Experiment 03 into Gallery v99 and give the player screen the disappearing overlay scrollbar already used by Discover / Library.

## Full HTML snapshot (primary recovery file)

- **File:** `Gallery-v100.html`
- **Location:** persistent ChatGPT Library `/Gallery Backups/2026-11-04/Gallery-v100.html`
- **Size:** 6,812,924 bytes
- **SHA-256:** `0aac13b097dc0a10b19699704687c09ffc5f3fe9407f757e3695ea45b57fe283`
- **Parent:** `Gallery-v99.html`, SHA-256 `34719245efcf1b128b7ec44df4eaffc876b3ce894a043ad1b1b23b58367108f4`.
- The complete v100 HTML is **not** in GitHub. Attempt to commit the 6.8 MB file was blocked by the connection. A follow-up path lookup confirmed it was absent. Do not confuse these integration source files with a full-version snapshot.

## Source integration files committed here

- [`_gallery_v100_history.js`](_gallery_v100_history.js) — complete Watch History model and UI integration, preview data and local-video tracking.
- [`_gallery_v100_styles.css`](_gallery_v100_styles.css) — scoped Watch History and Recently Watched styles, stable two-column episode controls, inner fading scrollbar, player scrollbar override.
- [`_build_gallery_v100.py`](_build_gallery_v100.py) — applies approved changes to the exact Gallery v99 HTML.

To reproduce the full HTML, place these three files alongside **`Gallery-v99.html`** in a single folder and run:

```bash
python3 _build_gallery_v100.py
```

The build script writes `Gallery-v100.html`. Check its SHA-256 against the checksum above. The source files are also backed up in the Library under `/Gallery Backups/2026-11-04/v100-source/`.

## Features and testing

- Discover **Recently Watched** compact cover strip (one recent season per anime) with fixed View History tile.
- Dedicated **Watch History** full page with per-season rows; expanding episodes, marking/unmarking, stable checkboxes, two-column layout with center divider, capped height + fading inner scrollbar, responsive single column.
- Search scoped to history with viewing date/year priority; In Progress / Completed filter; newest/oldest sorting; resets on leave.
- Separate season removal with session-long Undo until leaving the history page.
- Existing Gallery detail route for titles present in the v99 demo; unsupported fixture titles clearly identify themselves as samples.
- Player screen uses the **existing shared overlay scrollbar** with fade-on-idle and no native permanent gutter.
- Chromium checks passed for history at 1400, 900, 760, 390 px, and player at 1400, 900, 500 px. Player thumb appeared and faded after scroll. No JavaScript page errors or horizontal overflow.

**Scope limitation:** This is a full self-contained **HTML design/development preview**, not a compiled macOS app. The initial Watch History rows are sample fixtures. Local-video playback in this preview can record viewing progress, but real source-stream integrations are not connected.
