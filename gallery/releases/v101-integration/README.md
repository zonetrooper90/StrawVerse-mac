# Gallery v101 — Recently Watched slide-out preview

**Status:** complete standalone HTML prototype for user review. **Gallery v100 remains the approved baseline until v101 is visually accepted.** This is not a packaged macOS application.

## What changed from v100
- The portrait cover remains a stationary **66 × 96 px** foreground element.
- A separate, vertically centered **84 px-high** info panel slides rightward out from behind the portrait on hover or keyboard focus. It contains the season/anime title and the last episode (or Completed).
- Each item expands its *flex footprint* as the info panel opens; the adjacent covers and View History tile move aside as a group, with a reversible transition and no horizontal scrolling or pagination.
- View History is the final element in the row, with the **same 66 × 96 px footprint** as a cover and the same gap, not a right-anchored 106 px-wide block.
- A ResizeObserver determines how many covers can be safely shown given the current row width, reserving space for a fully opened info panel *and* the View History tile. Compact window widths reduce the visible item count and panel width. Keyboard focus and reduced-motion preferences are supported.
- No generated assets, new images, or changes to the underlying Gallery v100 Watch History/player functionality.

## Recover full HTML
- **Full file:** persistent ChatGPT Library at `/Gallery Backups/2026-11-04/Gallery-v101.html`
- **Source base:** `/Gallery Backups/2026-11-04/Gallery-v100.html` (approved baseline, unchanged)
- **Patch:** [Gallery-v100-to-v101.patch](Gallery-v100-to-v101.patch) stored in this repository
- To reconstruct from v100 and the patch:
  ```bash
  patch -o Gallery-v101.html Gallery-v100.html Gallery-v100-to-v101.patch
  ```
- Full file size: **6,815,070 bytes**
- Full file SHA-256: `d55345e62f4999fe9b4fe28589c786be70b10932a4dc58c6eb86e70d8646d959`
- The patch was applied to a copy of the exact v100 file, and the reconstructed v101 HTML was byte-for-byte identical to the output.

## Browser checks
Chromium at 1440, 1100, 900, 760, 560, 390 and 320 px: fixed cover dimensions/position, short centered panel, panel emerging to the right, adjacent covers and View History sliding without clipping, View History immediately after the last visible card, responsive counts, focus-triggered animation, proper return animation, no horizontal page overflow. Existing Watch History page, Pokémon episode toggle with stationary control/persistent panel, and View History navigation still pass. No page JavaScript errors.

**Note:** the complete ~6.8 MB HTML file is held in persistent Library, not committed in full to GitHub (GitHub has the validated patch, not full base or output). This README and the patch do not by themselves constitute a full GitHub backup.
