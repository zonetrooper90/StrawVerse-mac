# Gallery — Three Visual Directions · Design Study 01

Date: 2026-11-05. **Status: approved standalone design-concept experiment, not a Gallery release.** The current stable Gallery app remains **v103**, unchanged.

## Why

After testing daisyUI inside Gallery, the user clarified the real goal: **Gallery needs a memorable, genuinely ownable visual identity that does not look or feel like stock Windows, macOS or Linux software**. The user is open to a substantial change in appearance while keeping the refined Gallery behaviors. Ultimately they will choose on gut feeling, not component-by-component scoring.

The user agreed to explore three directions (Cinematic / Editorial / Soft Futuristic) as interactive HTML concepts and explicitly requested concepts of **all three**.

## The artifact

[Gallery-Three-Visual-Directions-01.html](Gallery-Three-Visual-Directions-01.html) — **56,082 bytes**, SHA-256 `e166118ef214d39170793673d43179e563bd39ad9c2d499553baafffb1efa8c6`.

Saved in persistent ChatGPT Library at:
`/Gallery Backups/Design Experiments/2026-11-05/Gallery-Three-Visual-Directions-01.html`

The complete HTML is stored in this GitHub branch and fetched back byte-for-byte for verification. The HTML is **fully self-contained and offline-capable**, with no CDN, no third-party JS, no external font dependency, no React, and no runtime image requests. Original artwork was **not generated or edited**: all cards use stylized CSS poster placeholders adapted from **Gallery v103's existing demo gradients**, and the featured and card titles and summaries are from v103's demo content.

## The three deliberately distinct systems

1. **Cinematic** — theatrical widescreen feature, charcoal/amber palette, restrained serif editorial feature typography, minimal line-based navigation, thin section dividers, film-presentation storytelling.
2. **Editorial** — warm paper magazine, high-contrast oversized typography, square/angular components, deliberate rules and issue labels, asymmetrical cover-feature layout, curated index cards.
3. **Soft Futuristic** — matte ocean/sea-glass palette (not Apple Liquid Glass), sculpted soft panels, rounded floating segmented navigation, signature orbit mark, stylized orbital featured composition, softly raised controls.

They share the **same demo shows** and are accessible through one three-way switcher. The purpose is to judge identity, visual rhythm, layout hierarchy, interactions and emotional reaction—not to compare daisyUI themes or commit to one.

The concepts permit interaction with Discover / Library / Downloads, integrated Search (results replace Discover content), title details, add/remove from a simulated Library, a visual-only playback dialog, Watch History reveal, and a short About panel. Arrow left/right switches design concepts; Esc closes overlays or search. No changes persist to Gallery's actual settings or source code. Playback, download operations, Watch History and repository sources remain illustrative; these are **not functional alternative Gallery builds**.

## Verification

Playwright / Chromium tests passed for **all 3 concepts** at **1440, 1024, 768, 390 and 320px** viewports: concept switching, Search/results, title details, Library add/remove, Library navigation, Downloads placeholder, Watch History expansion, no horizontal document overflow, no page JavaScript errors, and **zero external network requests**. Screenshots visually inspected for all three designs on desktop and mobile.

## Important scope constraints

- The approved stable Gallery remains **v103**; no new numbered version has been requested.
- No existing Gallery source, content, assets, or image files were modified.
- This is a **fresh visual exploration**, not a commitment to daisyUI, and does not use daisyUI.
- It is okay for one direction, or selected aspects of several, to be rejected. User's aesthetic reaction guides the next iteration.
- If the user wants real Gallery artwork incorporated later, discuss asset selection and technical constraints first. Do not generate images without explicit user consent.


## Soft Futuristic — Six Palettes 01 (2026-11-05)

- The user selected **Soft Futuristic** as their favorite visual direction. They liked both its soft, rounded geometry and possibly the teal palette. After comparing Ocean, Twilight, Ember and Slate, they decided to keep all four; subsequently asked to try **two more distinct themes: Glacier and Solstice**.
- The prior Palette Study 02 was reported visually close to the original concept except for its overly wide frame. This experiment builds **directly on Palette Study 02**, retains the identical component layout, colors of existing four themes, typography, demo content, artwork and interactions, adds Glacier (deep blue/icy highlights) and Solstice (bronze/champagne), and restores a narrower centered viewport to match the first-round proportions.
- [Full self-contained HTML](Gallery-Soft-Futuristic-Six-Themes-01.html): **39,859 bytes**, SHA-256 `90eb446bf39f8e94213311e3de649439102a63f7c6b3b88fa3cb073a5565d30b`. Persistent Library backup `/Gallery Backups/Design Experiments/2026-11-05/Soft Futuristic/Gallery-Soft-Futuristic-Six-Themes-01.html`. GitHub copy fetched back and byte-verified.
- Interactive palette selector includes **Ocean, Twilight, Ember, Slate, Glacier, Solstice**. All six are deliberate app themes, not automatic light/dark OS-mode selections. Palette styles change only colors. Experiment shell's centered max-width changed to `1160px` with original-like 26px responsive padding; CSS min-width grid correction fixes 320px/390px horizontal overflow.
- Browser tests passed at **1440×900, 1024×768, 760×900, 390×844, and 320×700**: all six palettes change successfully, exactly one pressed option, feature area remains the same width/height among choices, Discover/Library, title details, escape, Search, no JavaScript page errors, no external requests, no horizontal page overflow. The maximum one-pixel x-position difference on 390px-width test is due to fractional grid rounding; dimensions remain identical.
- This is **not a replacement Gallery version**; Gallery **v103 remains stable and untouched**. User has not yet selected the default palette or approved integration.


## Soft Futuristic — Six Palettes 02: original frame width (2026-11-05)

- After trying Six Palettes 01, the user reported that the centered app frame was **far too narrow** (the visible Gallery area was ~715 px in their screenshot versus ~1,060 px in the first-round comparison) and explicitly approved restoring the original width without changing the themes or styling.
- Corrected experiment: [Gallery-Soft-Futuristic-Six-Themes-02.html](Gallery-Soft-Futuristic-Six-Themes-02.html). The **only CSS change** compared with Six Palettes 01 is restoring `#canvas max-width: 1680px` from the first-round [Three Visual Directions](Gallery-Three-Visual-Directions-01.html), replacing the unnecessary `1160px` limit. Two experiment-title strings updated, but palette values, controls, animations, demo artwork, JS logic, spacing and geometry rules are unchanged.
- Browser bounding-box comparison against the first-round study at **1536×1024, 1440×900, 1280×800, 1100×840, 760×900, 390×844, 320×700** confirmed the corrected desktop design is within ~28 px of the original width due to the experiment shell padding, while the narrow layouts have no horizontal document overflow. At 1536 px, original: 1444 px; Six Palettes 01: 1068 px; Six Palettes 02: 1416 px. All six palette switches retained identical feature area geometry at the tested desktop width. Navigation, Search and title-dialog interactions passed; no JS page errors.
- The original user screenshots appear taken at browser zoom or different rendering scaling, so physical screenshot pixels may differ from CSS layout measurements; avoid promising exact screenshot pixel identity. The important correction is to use the **same original max-width CSS** and retain all six palettes.
- Full HTML retained in persistent ChatGPT Library at `/Gallery Backups/Design Experiments/2026-11-05/Soft Futuristic/Gallery-Soft-Futuristic-Six-Themes-02.html`; GitHub source fetched and verified byte-for-byte. **Stable Gallery v103 untouched.** This remains a separate design experiment, not v104.


## Soft Futuristic — Settings Study 01 (2026-11-05)

- Standalone [Settings Study 01](Gallery-Soft-Futuristic-Settings-Study-01.html) extends [Six Themes 04](Gallery-Soft-Futuristic-Six-Themes-04.html) with a full-page Settings design while preserving its corrected max-width 1680px frame, six palettes (Ocean, Twilight, Ember, Slate, frostier Glacier, Verdant), and existing Discover/Library/Downloads presentation.
- Opens Settings from the top-right gear; app navigation and app-level search are hidden in Settings. Back to Gallery restores the previous top-level tab. Sections follow **the real Gallery v103 Settings information architecture**: Appearance (Themes/Typography), Playback (General/Subtitles), Downloads, Sources (Installed/Marketplace/Repositories), About. This is a CSS/JS-only visual concept, not a v103 implementation.
- Theme tiles and external palette selector synchronize; selected app font, simulated playback choices, autoplay toggle, subtitle sizing/style/intensity/color, destination radio and sample Source install/remove interactions work locally as demonstrators. A neutral CSS-only subtitle preview is intentionally used **instead of** changing/recreating the approved Gallery v103 day/night shrine artwork or its locked preview proportions; this is not a production-level subtitle settings replacement.
- Tested in headless Chromium at **1536×960, 1440×900, 1100×800, 760×900, 390×844, and 320×700**: Settings entry, all five sections and subtabs, all six theme tile selections, controls, source demo, back navigation and returning to Library passed. No page JS exceptions or document/app horizontal overflows. Verified subtitle effect intensity changes rendered text-shadow style. HTML source fetched from GitHub and matched exactly.
- Offline only; no external assets, CDNs or network. Persistent Library backup at `/Gallery Backups/Design Experiments/2026-11-05/Soft Futuristic/Gallery-Soft-Futuristic-Settings-Study-01.html`. **Gallery v103 unchanged; new numbered application version not authorized.**
