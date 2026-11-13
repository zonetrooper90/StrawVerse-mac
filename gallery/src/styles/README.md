# Gallery CSS source map — M2

The stylesheet is split into **28 contiguous fragments**. `../build-manifest.json` is the only assembly order. Numbered names reflect the current cascade, not an invitation to sort or move declarations. Later files can override earlier files for the same feature; inspect the full manifest when changing shared styles. Each slice starts at a top-level comment or the initial stylesheet start. Concatenation adds zero bytes and reproduces the verified pre-M2 stylesheet exactly. Do not autoformat, reorder or merge overrides as part of an extraction.

| Order / file | Original stylesheet lines | Bytes |
|---|---:|---:|
| `01-base-and-page-headers.css` | 1–81 | 13,599 |
| `02-anime-detail.css` | 82–316 | 16,838 |
| `03-player-and-desktop-frame.css` | 317–430 | 11,508 |
| `04-motion-and-focus.css` | 431–487 | 3,844 |
| `05-navigation-and-dialogs.css` | 488–543 | 2,704 |
| `06-library-and-workspace-scroll.css` | 544–645 | 5,178 |
| `07-anime-detail-refinements.css` | 646–849 | 13,051 |
| `08-downloads.css` | 850–915 | 4,974 |
| `09-search.css` | 916–989 | 6,610 |
| `10-settings.css` | 990–1077 | 8,695 |
| `11-sources.css` | 1078–1194 | 12,135 |
| `12-about-and-settings-refinements.css` | 1195–1383 | 12,205 |
| `13-typography.css` | 1384–1459 | 8,093 |
| `14-subtitle-preview-and-controls.css` | 1460–1778 | 11,591 |
| `15-subtitle-color-popover.css` | 1779–1924 | 7,337 |
| `16-player-navigation.css` | 1925–1990 | 3,389 |
| `17-watch-history.css` | 1991–2133 | 16,434 |
| `18-theme-palettes-and-foundation.css` | 2134–2318 | 15,666 |
| `19-themed-settings.css` | 2319–2434 | 5,472 |
| `20-themed-primary-pages.css` | 2435–2654 | 11,947 |
| `21-themed-downloads.css` | 2655–2894 | 15,569 |
| `22-stationary-backdrop.css` | 2895–2907 | 614 |
| `23-themed-subtitle-workbench.css` | 2908–3015 | 11,193 |
| `24-themed-headers-and-player.css` | 3016–3135 | 6,670 |
| `25-themed-anime-audio-and-episodes.css` | 3136–3226 | 4,325 |
| `26-player-icons-and-timelines.css` | 3227–3367 | 9,164 |
| `27-player-navigation-and-header-refinements.css` | 3368–3524 | 8,090 |
| `28-unified-headers-and-history-frame.css` | 3525–3641 | 5,027 |

Original stylesheet: 251,922 bytes. Original verified source-first commit: `d82055b2fcca800d491149c39169d5487bca7828`. No CSS rules, comments, whitespace, themes, breakpoints or animation declarations changed. Some base files intentionally contain multiple feature areas and later themed/override fragments repeat those areas. Logical regrouping across the cascade requires separate review and equivalence testing.

Historical M2 anomaly (original line 979, `09-search.css:64` before correction): a duplicate bare transition declaration with an unmatched closing brace caused Chromium to discard the following `.continue-shell .continue-clip` rule. After the read-only Queue 1 investigation, the user approved removing only that malformed line. The correction restores clipping and minimum height for the Recently Watched search collapse; the original M2 byte/line table remains historical. Existing empty conditional blocks remain unchanged.

For application changes edit the appropriate source fragment, then use the approved source-first build/publish workflow. Never independently edit generated HTML.
