# Gallery HTML archive

This archive preserves exact, standalone Gallery HTML snapshots. Full files are split into Git blobs under `chunks/<filename>/part-NNN` to work around the upload transport limit.

To reconstruct the original HTML files after cloning the repository and switching to `gallery/development-archive`, run:

```bash
python3 gallery/archive/assemble.py
```

The restorer verifies original byte size and SHA-256 against `manifest.json`. It writes the original intact HTML to `gallery/archive/html/`. Each previous numbered version is kept without modification. The latest approved snapshot as of November 4, 2026 is **v99**. Decisions and continuity rules are in `gallery/APPROVED-DECISIONS.md` and `gallery/PROJECT-CONTINUITY.md`.

The Mac playback implementation is separate; do not mistake HTML experiments for a native release.
