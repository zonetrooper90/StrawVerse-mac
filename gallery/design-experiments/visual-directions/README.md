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
