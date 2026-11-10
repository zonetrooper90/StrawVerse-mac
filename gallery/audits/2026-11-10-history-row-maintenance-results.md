# Gallery unnumbered maintenance — 2026-11-10

## User-approved scope
- Hide unfinished Library Import and Share/Export controls and related transfer help text behind `GALLERY_COLLECTION_TRANSFER_UI_ENABLED=false`; retain the complete handlers and implementation for future redesign.
- Watch History: use a wide, keyboard-accessible summary click target like Downloads. Preserve distinct cover/title links to anime details and independent Remove/Undo.
- Watch History: make the entire episode row activate the existing watched/unwatched toggle while retaining fixed-width status, row hover, scroll position, filtering and update-in-place.
- Preserve the accepted coordinated fades, six themes, native/app constraints, library behavior, downloads and existing navigation.

## Source and exact integrity
- Previous verified GitHub checkpoint: `2026-11-10-coordinated-fade-route-fixes`, SHA-256 `1d83bea4249345198d91730524fda609edb1d9734196bd274225a6a5f67c9a4c`.
- New immutable checkpoint: `2026-11-10-history-rows-hidden-transfers`.
- New HTML SHA-256: `ca85c7184dc5feb958677fce208c6e6d48b19c1e97a2a9cdc3d8bf74bcebb530`, bytes: `6948256`.
- Canonical pointer: `gallery/checkpoints/current.json`.
- Complete deliverable: `gallery/deliverables/Gallery-History-Row-Maintenance.html`, same SHA-256.
- GitHub checkpoint commit: `4df2a60825e4b3c68e496cc757de7f3fc5b1fa0f`.

## Verification
- GitHub Actions workflow `42918982630`: **success**, with authoritative checkpoint preflight, exact 6.9 MB output hash assertion, old route/transition suites, new interaction/keyboard suite, immutable stage, restore verification, commit/push and upload-artifact.
- Local Chromium: Library controls hidden but New Tag intact; summary background expands; episode number-area click and Space toggle watched state; title opens details and returns to Watch History; remove and undo independent; Downloads still interactive.
- Tested responsive widths 370 px, 700 px and 1440 px with reduced motion.
- The GitHub Actions artifact and ChatGPT-deliverable HTML were compared byte-for-byte with the committed SHA-256 pointer.

This is an HTML/UI checkpoint delivered for user visual review, **not** an assertion of native Mac app integration. No existing checkpoint was modified.
