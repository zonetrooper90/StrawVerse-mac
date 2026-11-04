# Gallery HTML version index

Snapshot inventory verified locally on **2026-11-04**. These hashes identify **actual files**, but this index alone does **not** mean their bytes are committed to GitHub.

| File | Bytes | SHA-256 |
|---|---:|---|
| `Gallery-v96-Layout-Experiment-A28-Three-Subtitle-Fonts(1).html` | 6762915 | `b60f882a7b0528d28d00810e1983c48e2d98f7ad7f619d89ddd5f575517fd32c` |
| `Gallery-v97.html` | 6763831 | `b948e845bb7d4f23119cd62f21481b4f046c27e64ea98b8c1bf657463ab094f7` |
| `Gallery-v98.html` | 6773168 | `7e5238b8e27072242eb7cf0911dcdf88864de00d9bbaced4ee3a8178178f470c` |
| `Gallery-v99.html` | 6776286 | `34719245efcf1b128b7ec44df4eaffc876b3ce894a043ad1b1b23b58367108f4` |

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
