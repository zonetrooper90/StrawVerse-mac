# Gallery × daisyUI — Component Lab 01 (2026-11-05)

**Status:** approved *experiment*, not an app version. Current approved Gallery v103 remains completely unchanged.

## Direction / user preferences

- The user reviewed Basecoat, daisyUI, and other systems and **prefers daisyUI** for its colorful theme support, distinct component styling, and breadth of components.
- User is **open to retiring Gallery's current themes** if custom themes designed around daisyUI prove preferable. **No replacement theme has been selected or integrated.** The existing theme system must remain intact in v103 until a future change is discussed and approved.
- Avoid an Apple-like Liquid Glass identity. The objective is a Gallery-owned visual language that retains the existing macOS-friendly interactions and carefully refined Recently Watched / Watch History behavior.

## The experiment

[Gallery-daisyUI-Component-Lab-01.html](Gallery-daisyUI-Component-Lab-01.html) — **40,084 bytes**, SHA-256 `f4a86d2f705b75168ea0cf29d326c5a7795151ba42e17810f62a180dcff79f09`.

- Uses the **actual daisyUI v5.7.48 CSS** from two version-pinned jsDelivr URLs: `daisyui.css` for components, `themes.css` for the additional official themes. No imitation of the component CSS and no React or runtime Tailwind JS dependency.
- **Online connection required for the component styles.** This HTML is a single standalone design document, but **not self-contained for offline viewing**. The file detects absent styles and explicitly warns rather than claiming they loaded. For real Gallery app integration, build and bundle only the approved CSS modules locally: the app must not require network access to render its interface.
- Compare a simplified Gallery v103 Neon reference with actual daisyUI **Tabs**, a joined **button** segmented control, and **Buttons**.
- Browse 12 more Gallery-oriented component shelves: button variants, tab variants, toggles, checkbox, search input, select, dropdown menu, badges, range, progress, card, alerts, loading, steps, stats, keyboard hints, radio, textarea, and an anime action panel.
- Seven theme choices: **Gallery Violet** (custom CSS theme mapped from v103 neon), **Night**, **Dim**, **Dracula**, **Abyss**, **Synthwave**, **Silk**. Gallery Violet offers editable primary/secondary/accent tokens and a viewable CSS token snippet.
- All interactions are demo-only: choices, buttons, filters, settings switches, search, progress, dropdown, and theme switching do not affect Gallery or persist user data.
- The left Gallery v103-inspired reference is a simplified visual comparator, **not the actual v103 code or animation**; do not claim pixel parity.
- **Testing:** Chromium interaction tests passed at viewport widths 1440, 1050, 850, 620, 390 and 320px; 0 horizontal overflow, no page JS errors, and selection, theme, input, settings, progress, dropdown, token editor, and reset functions work in tested paths. Test runtime had no external network and deliberately blocked the CDN, so **actual CSS visual rendering could not be verified in-browser in this session**. User must inspect it connected to the internet; the HTML displays a clear warning if CSS is unavailable.

## Recovery and files

- Full, byte-verified GitHub source: `gallery/design-experiments/daisyui/Gallery-daisyUI-Component-Lab-01.html` on `gallery/design-checkpoints`.
- Persistent ChatGPT Library backup: `/Gallery Backups/Design Experiments/2026-11-05/Gallery-daisyUI-Component-Lab-01.html`.
- v103 full HTML remains in Library at `/Gallery Backups/2026-11-04/Gallery-v103.html`. No v104 authorized.
- daisyUI license is MIT; any eventual copied local distribution should retain appropriate license notices.

## Next decisions (not yet made)

1. User to evaluate actual daisyUI components and themes, identify preferred control variants.
2. Agree whether to keep current Gallery top-nav animation and only update surfaces, or adopt a daisyUI tab style.
3. Choose Gallery-owned daisyUI-compatible theme palette(s), including accessible contrast and light mode if desired.
4. Test a **local bundled CSS** build in the actual macOS WebKit target before considering an approved new numbered Gallery version.


## Component Lab 02 — offline exporter and diagnostic fix (2026-11-05)

[Gallery-daisyUI-Component-Lab-02.html](Gallery-daisyUI-Component-Lab-02.html) — **49,466 bytes**, SHA-256 `4005cefb79022083154a551c3decf3f323d9f3ef91aa24e298d8ca6c0ffd7119`.

- User reported **"Could not load daisyUI CSS"** when using Lab 01 locally in Microsoft Edge on a work PC despite successfully opening both CDN stylesheet URLs in Edge. Source review showed the original computed-style check could incorrectly mark styles as missing. Do **not** treat the warning as evidence that the work firewall blocks jsDelivr.
- Lab 02 retains the same seven theme choices, Gallery Violet color editor, reference controls and daisyUI component examples.
- Uses **original compiled daisyUI v5.7.48 CSS** from the pinned jsDelivr CDN, with cdnjs/UNPKG fallback. CSS is captured as text, validated with source markers and embedded into `<style>` tags; external `<link>` tags are removed on successful capture. No visual approximations. On browsers that allow the stylesheet to render but block JavaScript from reading it, the diagnostics distinguish "stylesheet displayed" from "CSS captured and ready to export".
- **One-time bootstrap requirement:** due to network restrictions in the authoring environment, the downloadable Lab 02 starter HTML itself still needs online access *once* to retrieve actual CSS; it is **not already fully offline**. Clicking **Save offline HTML** in the starter creates `Gallery-daisyUI-Component-Lab-02-Offline.html` with the **actual complete component and theme CSS embedded**, no external `<link>` dependencies, and a daisyUI MIT copyright/license notice. The generated offline copy checks for embedded CSS and skips all CDN requests on subsequent openings. A local file-picker fallback imports two original `.css` files when browser cross-origin `fetch` fails.
- Browser **test simulation** with deterministic, stand-in CSS responses (not the real CDN CSS, which could not be fetched here) verified CSS acquisition, progress status, seven-theme interaction, creating the offline file, reopening it with all network blocked (zero external requests), reexport and narrow-width layout; no JavaScript errors. A blocked-fetch simulation verified accurate error messaging and manual CSS file import/export. **The actual daisyUI v5.7.48 remote CSS fetch and visual rendering require testing on the user's PC.** Never claim the test fixture itself is the real daisyUI CSS.
- Artifact backups: full Lab 02 HTML committed and byte-verified in GitHub on `gallery/design-checkpoints`, and archived in persistent Library `/Gallery Backups/Design Experiments/2026-11-05/Gallery-daisyUI-Component-Lab-02.html`.
- The lab is a **design experiment only**, and Gallery v103 remains unchanged. No replacement themes or app integration have been approved.


## Neutral Component Lab 03 (2026-11-05)

- User asked to try a **completely neutral theme** to judge component styling independently of Gallery branding; this is an exploratory preference, **not a choice to replace Gallery's default theme**.
- [Gallery-daisyUI-Neutral-Component-Lab-03.html](Gallery-daisyUI-Neutral-Component-Lab-03.html) (**54,738 bytes**, SHA-256 `da8541926be0f257f6ecc87edb50f86e1cc2fa47b44d2363be136d1291409e87`).
- Adds **Neutral Dark** (default) and **Neutral Light** as fully grayscale daisyUI-compatible custom themes, including primary/secondary/accent and feedback colors with **matched radius, sizing, border, depth, and noise tokens**. This controls for hue and geometry to compare the actual component forms. The lab's surrounding UI and its Gallery-style comparator are also neutralized. Retains previous colorful themes, control examples, and editable Gallery Violet mode (its editor is hidden unless selected).
- Preserves Lab 02's daisyUI v5.7.48 actual CSS loading and **Save offline HTML** process: starter still fetches original vendor styles once or accepts manually imported original CSS; the exported HTML embeds the original retrieved CSS. Neither a React runtime nor third-party JS is added. The vendor CSS is **not pre-embedded in this initial starter**; do not call it independently offline.
- Chromium behavior smoke tests (offline/without CDN styles) passed at 1440, 900, 560, 390 and 320px: neutral theme token values, theme switching, Gallery Violet editor visibility and editing, nav/filters/toggles, no JS errors, no horizontal overflow. **Actual daisyUI component appearance with remote vendor CSS was not verified in this environment**; user to inspect online or by exporting an offline copy.
- Full HTML committed to GitHub and fetched back byte-for-byte; persistent Library backup at `/Gallery Backups/Design Experiments/2026-11-05/Gallery-daisyUI-Neutral-Component-Lab-03.html`. Gallery **v103 remains untouched**, and no new Gallery app version is authorized.
