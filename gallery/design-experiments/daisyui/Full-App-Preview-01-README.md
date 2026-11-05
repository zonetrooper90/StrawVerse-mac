# Gallery × daisyUI — Full-App Design Preview 01

**Date:** 2026-11-05. **Status:** user-requested design experiment; user has not reviewed/approved its styling. **Stable Gallery v103 is unchanged**. This is *not* v104, not a native macOS build, and not a full rewrite.

## Scope

- Based byte-for-byte on the verified Library `Gallery-v103.html` baseline before making isolated preview changes. Preserves the existing Discover/Library/Downloads app structure, Watch History / Recently Watched Soft Glide mechanics, tab-pill animation and navigation, playback logic, and Settings.
- Maps daisyUI v5 theme variables (`--color-base-100`, `--color-primary`, etc.) onto Gallery's existing CSS variables so real Gallery surfaces, backgrounds, navigation, card containers, filters, inputs, and buttons can be viewed together.
- Includes the **official daisyUI v5.7.48 theme token values** for Night, Dim, Dracula, Abyss and Silk, as well as two explicitly **custom** themes: Gallery Violet and Neutral Dark.
- Component geometry (radii, border and depth) can follow the selected theme or be held constant with **Lock component shapes**.
- Adds a disposable live theme selector below Gallery's navigation, mirrors the same seven themes in **Settings → Appearance**, and provides an inline button/toggle/badge sample in Settings.
- Uses the **actual pinned official daisyUI 5.7.48 component CSS and themes** via CDN links (`https://cdn.jsdelivr.net/npm/daisyui@5.7.48/daisyui.css` and `themes.css`). No React dependency or third-party JS. The CSP is adjusted to allow just this stylesheet origin. An inline diagnostic tests whether the real `.toggle` component styling applied, rather than merely trusting the presence of a stylesheet object.
- **This is selective integration, not wholesale daisyUI rendering.** Most established Gallery controls retain their HTML and behaviors, with surfaces and styles adapted to daisyUI tokens. The Settings component sample uses daisyUI classes, but Gallery's legacy `.btn` rules and preview overrides still influence the buttons. Do not misrepresent it as a total daisyUI transformation.
- **Internet required for actual vendor component CSS** in this preview. Theme palette values are embedded for offline color inspection, but CDN-based component visuals and their availability must be tested in the user's own browser; browser tests in the development environment had to block network access.
- Real Gallery art sample assets/data remain inlined from v103. No generated images, no React, no production data changes or provider integration. The theme selector is prototype-only.

## Tests

- Chromium interaction checks with network/CSS unavailable at 1440, 900, 560, 390 and 320px: theme tokens, selector changes, shape lock, three-tab navigation, Settings entry and seven theme cards, sample buttons; no JavaScript page errors or document horizontal overflow.
- Additional regression test in Chromium at 1440px: click all three main tabs, select Abyss with its 0.25rem field radius, lock shapes to 0.5rem, select Silk in Settings and verify toolbar synchronizes; sample Save button updates demo status; no JS page errors.
- The resulting full HTML is 6,841,601 bytes; SHA-256 `0595c6e02f39203266da7e9b4e21c5a7c4d84e02cd232afd949a296e1488a431`.
- Original v103 exact file: 6,821,581 bytes; SHA-256 `8af8456d73ea216b355622d144024c31bd6cdb149f14627abb4006b3f001e3d1`.
- A local unified diff patch, 31,507 bytes, was applied to a copy of the exact v103 snapshot and **reproduced the new preview byte-for-byte**. The patch is local to the conversation; it is not in this GitHub directory.

## Recovery

- **Full preview HTML backed up in persistent ChatGPT Library**: `/Gallery Backups/Design Experiments/2026-11-05/Gallery-daisyUI-Full-App-Preview-01.html` (6,841,601 bytes).
- Source base: `/Gallery Backups/2026-11-04/Gallery-v103.html` (unchanged).
- GitHub contains **this documentation**, not the complete large preview HTML or patch. Complete byte-faithful recovery is via the full Library backup. Do not claim this README alone reconstructs the preview.
- daisyUI theme source licensed MIT (Copyright 2020 Pouya Saadeghi); retain applicable notices when redistributing any copied theme definitions.
