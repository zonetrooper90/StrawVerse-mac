# Gallery HTML version index

Snapshot inventory verified locally on **2026-11-04**. These hashes identify **actual files**, but this index alone does **not** mean their bytes are committed to GitHub.

| File | Bytes | SHA-256 |
|---|---:|---|
| `Gallery-v96-Layout-Experiment-A28-Three-Subtitle-Fonts(1).html` | 6762915 | `b60f882a7b0528d28d00810e1983c48e2d98f7ad7f619d89ddd5f575517fd32c` |
| `Gallery-v97.html` | 6763831 | `b948e845bb7d4f23119cd62f21481b4f046c27e64ea98b8c1bf657463ab094f7` |
| `Gallery-v98.html` | 6773168 | `7e5238b8e27072242eb7cf0911dcdf88864de00d9bbaced4ee3a8178178f470c` |
| `Gallery-v99.html` | 6776286 | `34719245efcf1b128b7ec44df4eaffc876b3ce894a043ad1b1b23b58367108f4` |
| `Gallery-v100.html` | 6812924 | `0aac13b097dc0a10b19699704687c09ffc5f3fe9407f757e3695ea45b57fe283` |
| `Gallery-v101.html` | 6815378 | `a49f991b6db185cf90774a446eb45904ba14b2ece2d3c7eec424749a866c2048` |

## Existing verified recovery archive

- Filename: `Gallery-HTML-Backup-2026-11-04.zip`
- Size: **19,618,309 bytes**
- SHA-256: `ce938215c9207efcbcaa2ea3a66839c8f84f4dfbda923ea3962d840906dcb161`
- Zip integrity check: passed (15 entries).
- Includes all four full HTML milestones (v96–v99), two player-UI experiments, two morph experiments, settings/design notes, and the three supplied SVG icons.
- This initial index was created as part of a recovery effort; do not imply the ZIP itself is in GitHub unless an upload is independently verified.

## Backup policy

- Store each immutable numbered HTML version in GitHub under `gallery/html-versions/vNN/` or, if GitHub size or tooling prevents upload, in the personal persistent Library with this index pointing to its name/checksum and an explicit notice.
- The source code in `gallery/app/` on existing Gallery branches is an older native-app prototype; **do not mistake it for v99**.
- Always verify retrieval/restore, not just upload, especially for >6 MB self-contained HTML files.
- A single archive is a recovery aid. Keep source snapshots individually accessible as well when possible.

## v100 — Watch History integration (2026-11-04)

- Latest complete standalone Gallery HTML milestone: **`Gallery-v100.html`**.
- Preserved as complete **6,812,924-byte** snapshot in persistent ChatGPT Library: `/Gallery Backups/2026-11-04/Gallery-v100.html`. This was uploaded and the Library metadata size was verified.
- SHA-256 of complete local HTML: `0aac13b097dc0a10b19699704687c09ffc5f3fe9407f757e3695ea45b57fe283`.
- Based on the byte-verified Gallery v99 snapshot. Integrates approved Watch History Experiment 03 (Discover Recently Watched, season-level list, expandable 2-column episode management with non-moving controls, bounded disappearing scrollbars, search, status filters, chronological sort, per-visit reset, dedicated removal and session-long Undo). Player workspace's native persistent scrollbar / stable gutter removed; shares Gallery's original transient overlay scrollbar.
- Tested in Chromium at 1400, 900, 760, and 390px for history interactions, search, Undo, navigation, responsive layout and non-flashing status changes; player tested at 1400, 900, and 500px with its overlay fading correctly and no reserved scrollbar gutter; no JavaScript page errors.
- Data scope: initial records are **sample fixtures** for design evaluation; local-video playback in the HTML demo can update local history records, but provider streams and production persistence/integration remain unavailable in this browser prototype. Do not claim this is a fully working native Mac release.
- **The full 6.8 MB v100 HTML is not committed to GitHub**: direct GitHub content upload was attempted but failed, and a missing-path check verified it was not created.
- Verified smaller source integration files are committed on `gallery/design-checkpoints` under `gallery/releases/v100-integration/`: `_gallery_v100_history.js`, `_gallery_v100_styles.css`, `_build_gallery_v100.py`. Together with the verified Library v99 HTML they reproduce v100.
- `Gallery-HTML-Backup-2026-11-04.zip` predates v100 and still contains v96–v99, **not v100**.

## v101 — Recently Watched preview slide-out (2026-11-04)

- Complete browser HTML prototype for **user visual review**: `Gallery-v101.html` at `/Gallery Backups/2026-11-04/Gallery-v101.html` in persistent ChatGPT Library. Full file **6,815,378 bytes**, SHA-256 `a49f991b6db185cf90774a446eb45904ba14b2ece2d3c7eec424749a866c2048`.
- Based on the current verified v100 baseline (6,812,924 bytes, SHA-256 `0aac13b097dc0a10b19699704687c09ffc5f3fe9407f757e3695ea45b57fe283`), retaining its Library/Discover Watch History navigation correction and player fixes.
- Replaces only the Discover Recently Watched preview: fixed portrait cover, shorter panel slides from behind it, neighbors move to make room, View History tile has same dimensions and follows last visible cover.
- Chromium checks at seven window widths and keyboard focus pass, including no horizontal clipping and persistent existing History interactions. Awaiting user visual acceptance; v100 remains previously approved baseline.
- Verified reproducible [v100→v101 patch](../releases/v101-integration/Gallery-v100-to-v101.patch) and [README](../releases/v101-integration/README.md) in GitHub `gallery/design-checkpoints/gallery/releases/v101-integration/`.
- **The complete 6.8 MB v101 HTML is not committed to GitHub.** Full v100 and v101 snapshots are preserved in Library; GitHub holds the reconstruction patch, not the full file.
