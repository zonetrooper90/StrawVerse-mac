# Gallery × daisyUI — Full-App Preview 02

Date: 2026-11-05. **Status: standalone design experiment, not Gallery v104.** The approved baseline is still **Gallery v103**.

## Why Preview 02 exists

After trying Full-App Preview 01, the user reported **alignment issues that made it difficult to judge daisyUI**. They explicitly approved these three corrections:
1. Isolate daisyUI's classes so its CSS cannot override Gallery's same-named `.tabs`, `.tab` or `.btn`.
2. Preserve v103 navigation positions, spacing, card sizes, and Settings alignment.
3. Move experimental theme controls out of the header and normal document flow.

## Where the actual files live

- Full working HTML, complete with the original Gallery v103 embedded content and images: **ChatGPT persistent Library** `/Gallery Backups/Design Experiments/2026-11-05/Gallery-daisyUI-Full-App-Preview-02.html`.
  - Exact size: **6,845,441 bytes**.
  - SHA-256: `03a52324bbf5801c63e9851d8f0bad6d0082a6429cb19246089809a75dba3370`.
- Reproducible [v103 → Preview 02 unified patch](Gallery-v103-to-daisyUI-Full-App-Preview-02.patch), stored both in GitHub and in the same Library folder. SHA-256 `5f748ee0a2d8d37ddef1d6b6fde5bf7403d3e9151b4cb42a54bf715bf61c394c`.
- Baseline v103: `/Gallery Backups/2026-11-04/Gallery-v103.html`; 6,821,581 bytes, SHA-256 `8af8456d73ea216b355622d144024c31bd6cdb149f14627abb4006b3f001e3d1`.
- Original Full-App Preview 01 and component labs remain archived separately.

To reconstruct from the exact v103 file and this patch: copy v103 into a working directory as `Gallery-v103.html`; run `patch -p0 < Gallery-v103-to-daisyUI-Full-App-Preview-02.patch` in that directory; rename the patched file to `Gallery-daisyUI-Full-App-Preview-02.html`. **Confirmed byte-for-byte identical with `cmp` after applying this patch.** Do not patch the stable v103 file in its archival location.

## Scope / behavior

- Built directly on the exact v103 HTML **without modifying native Gallery navigation, Settings rendering logic, Recently Watched, player, or watch-history interactions**. The original embedded image payloads are unchanged.
- A second experiment-only script maps the seven preview palette choices onto Gallery's existing CSS color variables. Built-in daisyUI v5.7.48 palette token sets: Gallery Violet (Gallery-owned mapping), Night, Dim, Dracula, Abyss, Neutral Dark (custom grayscale), and Silk. The original Neon Reel, Midnight Cinema, and Paper Lantern remain selectable from the floating control.
- The theme controls are housed in a fixed bottom-right **Shadow DOM**, do not enter normal document flow, and change **only experimental in-memory theme state**, not user preferences. The panel does not appear over the video player.
- **Original v103 geometry preserved.** No vendor stylesheet is imported into the document's global CSS. The base navigation still uses the original grid and animated indicator; CSS does not override padding, margin, dimensions, flex/grid/display, border width, or animations. Optional daisyUI corner-radius experiment (off by default) is restricted to border radii, so sizes stay locked.
- The **actual compiled daisyUI v5.7.48 component CSS** is loaded only inside a second Shadow DOM showcase in Settings → Appearance → Theme → **Components ◇**. It includes actual `btn`, `tabs`, `toggle`, `checkbox`, `badge`, `input`, and `select` class demonstrations. The showcase is collapsed by default, so Settings' content heights and existing alignment are unchanged until the user explicitly opens examples.
- The component CSS requires an internet connection and loads from the version-pinned jsDelivr URL, falling back to unpkg. The lab's original Color theme tokens remain usable without this download. CSP allows **stylesheets only** from these CDN domains (no remote JavaScript and `connect-src 'none'`). Neither source code nor runtime uses React. This is **not a completely offline vendor CSS bundle**; be transparent about that limitation.
- The original v103 Appearance theme tiles remain unchanged and functional. Choosing a tile restores its classic Gallery theme; the preview panel synchronizes to it.
- The demo is **a selective, reversible hybrid of Gallery controls and daisyUI styling, not a complete wholesale component replacement**. Actual vendor components are isolated on purpose to eliminate class collisions.
- daisyUI is MIT-licensed, Copyright © 2020 Pouya Saadeghi. Palette variables come from the v5.7.48 original CSS theme source.

## Verification

- Baseline geometry comparison between v103 and Preview 02 at viewport sizes **1440×900, 1050×800, 850×750, 620×780, 390×844 and 320×700** showed **zero bounding-box differences** for app frame, header, brand row, navigation tabs, workspace and settings button.
- **Settings alignment comparison** at widths **1440, 1000, 620, 390 and 320px** showed **zero bounding-box differences** for the Settings page header, layout, sidebar, content pane, original theme card/list/tiles and workspace **while the optional component showcase is collapsed**.
- Browser tests checked navigation clicks, opening Settings and Appearance, theme control changes, optional radius toggle, demo opening and interactions, legacy theme tile behavior, and no document horizontal overflow. No JS page errors were observed.
- A simulated third-party CSS response intentionally set `.tabs{display:flex!important}` and `.btn{height:66px!important}`; Gallery's real global nav remained on its original grid (or hidden by native Settings behavior), while the Shadow DOM demo received the injected styles, confirming isolation.
- **Important verification limit:** automated tests used a **stand-in CSS response** for the vendor stylesheet because the test environment could not retrieve the CDN content. The actual daisyUI CSS rendering still needs visual inspection on the user's computer. This limitation does not affect the verified v103 layout stability.
- The reconstruction patch was tested with `patch --dry-run`, applied and compared byte-for-byte with the Preview 02 HTML.

## Next step

User visually reviews Preview 02, reports any remaining alignment or styling issues, and chooses which individual daisyUI controls/themes are improvements. No new Gallery app version or adoption of replacement themes is approved yet.
