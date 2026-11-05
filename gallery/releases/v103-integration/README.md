# Gallery v103 — Top navigation indicator synchronization

**Status:** complete standalone HTML prototype, available for user review. Based on the immutable Gallery v102 snapshot, which remains unchanged. Not a packaged macOS application.

## Bug and fix

- **User-reported regression in v102:** clicking a Recently Watched anime already in the Library opened its details with the correct Library tab class/state, but the **animated top navigation pill remained on Discover** until the user moved the pointer over the nav bar.
- **Root cause:** `whOpenTitle(r)` switched `state.view` and called `updateActiveTab(targetView)`, then rendered the detail page, but **never called `updateTabIndicator()`**, unlike `setView(view)`. The nav's pointer event later called `updateTabIndicator()`, which explained the delayed visual correction.
- **Scoped fix:** call `updateTabIndicator()` at the end of `whOpenTitle(r)` after the destination detail and season render. This immediately targets the correct pill position while retaining Gallery's existing animated navigation transition.
- Browser document title and sample-data note updated to v103. No changes to Recently Watched Soft Glide, Watch History data handling/scrollbars, or playback.

## Recovery

- **Full standalone HTML:** `/Gallery Backups/2026-11-04/Gallery-v103.html` in persistent ChatGPT Library.
- **Source base:** `/Gallery Backups/2026-11-04/Gallery-v102.html` (immutable previous version).
- **Reproducible source patch:** [Gallery-v102-to-v103.patch](Gallery-v102-to-v103.patch), saved here and at `/Gallery Backups/2026-11-04/v103-source/Gallery-v102-to-v103.patch` in Library.
- Rebuild with `patch -o Gallery-v103.html Gallery-v102.html Gallery-v102-to-v103.patch`.
- v102 SHA-256: `4c11d051ade4cc34dc558e643b71cb59198f9ece522e17139b4a8125baea29c6` (6,821,465 bytes).
- v103 SHA-256: `8af8456d73ea216b355622d144024c31bd6cdb149f14627abb4006b3f001e3d1` (**6,821,581 bytes**).
- Patch SHA-256: `a9f843c5b82174b6659446faa9e450e9493356fedaeeae9b581f14bf072cda6f` (4,110 bytes).
- Patch reapplication to the exact backed-up v102 HTML **reproduced v103 byte-for-byte**.
- GitHub holds this exact patch and README, **not** the entire 6.8 MB v103 HTML. Full HTML backup lives in Library.

## Tested

- Chromium A/B repro at 1440px: v102 leaves indicator visually positioned on Discover after opening *The Quintessential Quintuplets ∬* (Library anime), while v103 immediately moves pill to Library without cursor interaction.
- v103 regression checks at **1440px, 900px and 390px**, for both Discover → Library and Library → Watch History → Discover routes. Pill position, active tab and detail all agreed, with no JavaScript page errors.
- Watch History navigates and page stays within viewport without horizontal overflow in tested widths.
- v102 design and Soft Glide implementation otherwise unchanged.
