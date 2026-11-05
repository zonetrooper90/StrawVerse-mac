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
