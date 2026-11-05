# Gallery v102 — Recently Watched Soft Glide

**Status:** complete interactive Gallery HTML prototype for user review. Built from the exact persistent Library v101 snapshot; v101 and all animation labs remain unmodified. Not yet a packaged native macOS app.

## Chosen animation
The user selected **Soft Glide** from Animation Lab 03 after reviewing the corrected pointer targeting and coordinated list movement.

- Opening: **550 ms**, `cubic-bezier(.35,0,.13,1)`
- Closing: **375 ms**, `cubic-bezier(.25,0,.22,1)`
- First idle hover intent: **100 ms**; switching between covers starts immediately.
- Info fade-in: **290 ms**, beginning after **115 ms**.
- Fixed 66 × 96 px foreground cover; the independent, vertically centered info card remains 84 px tall.
- Flex width is controlled by a *single coordinated* animation: panel space moves between covers while the trailing **View History** tile stays still. No accordion/bounce caused by independent animations.
- Hover selection responds only to genuine pointer motion, protecting against the wrong cover opening as its neighbors move underneath a stationary cursor.
- Keyboard focus works; reduced-motion users do not receive motion. No native `title` tooltip on preview covers.
- Responsive card count continues reserving room for the full info panel plus the final, cover-sized View History shortcut; no horizontal carousel scrolling or pagination.

## Recover v102

- Complete HTML: persistent ChatGPT Library `/Gallery Backups/2026-11-04/Gallery-v102.html`.
- Complete base: persistent Library `/Gallery Backups/2026-11-04/Gallery-v101.html`.
- [Exact v101 → v102 patch](Gallery-v101-to-v102.patch), committed to GitHub here and saved in Library at `/Gallery Backups/2026-11-04/v102-source/Gallery-v101-to-v102.patch`.
- Apply from a directory with both `Gallery-v101.html` and the patch:
  ```bash
  patch -o Gallery-v102.html Gallery-v101.html Gallery-v101-to-v102.patch
  ```
- v101: **6,815,378 bytes**, SHA-256 `a49f991b6db185cf90774a446eb45904ba14b2ece2d3c7eec424749a866c2048`.
- v102: **6,821,465 bytes**, SHA-256 `4c11d051ade4cc34dc558e643b71cb59198f9ece522e17139b4a8125baea29c6`.
- Patch: **20,624 bytes**, SHA-256 `dec514beb59f58c9e330d074d98383215661406ee69c34a0801d30531b2859f8`.
- The patch was applied to the exact stored v101 file and the output compared byte-for-byte with the complete v102 file: **match**.

## Testing and scope

- Full Chromium interaction regression passed at **1440, 1100, 900, 760, 560 px** viewport widths, including rapid and reversed hover targeting, stationary View History tile during cover switches, centered card height, focus, full Watch History navigation, and non-rebuilding Pokémon episode toggles.
- Narrow-width smoke tests passed at **390 and 320 px**, including no clipping or horizontal overflow, cover hover, and Watch History navigation.
- No JavaScript page errors in these tested flows. The existing player scrollbar implementation and source integrations are inherited unchanged from v101.
- **Source scope:** uses sample records and limited browser local-video playback tracking from v101, not live provider integration. The 6.8MB full HTML is backed up in Library; **GitHub contains the reproducible source patch, not the complete HTML file**.
