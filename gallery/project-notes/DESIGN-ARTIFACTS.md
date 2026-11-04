# Gallery design artifacts — verified inventory

This file tracks **approved sketches, HTML mockups, animation experiments, asset SVGs and design notes** independently of numbered Gallery builds.

## Recovery source and scope (2026-11-04)

The exact files below have been verified **inside** the locally integrity-checked `Gallery-HTML-Backup-2026-11-04.zip`, which is saved in the persistent ChatGPT Library at:

`/Gallery Backups/2026-11-04/Gallery-HTML-Backup-2026-11-04.zip`

Its SHA-256 and size are in [VERSION-INDEX.md](VERSION-INDEX.md). **The individual experiment source files are not yet committed to GitHub**; these hashes identify archive members, not GitHub blobs.

| File inside ZIP | Purpose / status | Bytes | SHA-256 |
|---|---|---:|---|
| `Gallery-Player-UI-Experiment.html` | Early player UI sketch / experiment | 25229 | `05514c341f4b18e183602182f6ea8fae2c175ea69eff1b5696ed2831d43c4a65` |
| `Gallery-Player-UI-Experiment-r2.html` | Subsequent player mockup; archive file happens to have same hash as previous | 25229 | `05514c341f4b18e183602182f6ea8fae2c175ea69eff1b5696ed2831d43c4a65` |
| `Gallery-Icon-Morph-Experiment.html` | First icon-morph experiment | 16815 | `34a0a8de95f17d49a16beb33aabd29b8177d243254320c59f02fb308b14873df` |
| `Gallery-Icon-Morph-TrackNext-to-SkipForward.html` | **Approved morph**: Tabler Player Track Next ↔ Player Skip Forward, reversible | 13818 | `f0301976e4af4b3a533a34d0d701fa73b4e426cbf7597615e1dcbafadf7faed9` |
| `player-skip-forward.svg` | Supplied next-episode icon | 373 | `6e4c0c27aadceef4c204aeafa8d7b61d6f4aa66541d90b2669fb265902b28cd5` |
| `player-track-next.svg` | Supplied forward 10-second icon | 378 | `f13b25c9ac378cdf0b6a51da5ad312f61e469e17d32fe67f8e01769113636b7f` |
| `player-track-prev.svg` | Supplied backward 10-second icon | 379 | `f211bae6646a3e7e33d5838fa4580ebc6e2c73ace579869dd5d34f1a290c7425` |
| `Gallery-Watch-History-Locked-Decisions.md` | **Agreed** Recently Watched / Watch History decisions (not a visual mockup) | 2144 | `ba82c1b53e3b5b64b78a2b26171fadf9cdca796e5f71e688e33c4a42eb2c08de` |
| `Gallery-v97-Settings-Handoff.md` | Settings and subtitle design handoff | 6017 | `3932b0746dcb9b03ecdcae62ea6919b43a7f4f7a181df9aea2ac85b432768cac` |
| `Gallery-v97-Integration-Notes.md` | Settings integration notes | 3008 | `6143a0bb2c74f7bcbb34bec3d6bea9bf0efc3ed6d3c76cb922adab198064d9e9` |
| `Gallery-v98-Player-Morph-Notes.md` | Player-morph integration notes | 3110 | `d086fe6725443e544ed2b777c5e0dae469bdbf7178a5a65a4c7bdbc1b23e3ed1` |

## Watch History design state

- Agreed requirements are preserved in the dedicated Markdown file above and in `DECISIONS.md`.
- **No standalone Watch History HTML visual sketch is included in the verified archive.**
- The full Watch History page layout remains **undecided**; do not infer a finalized layout from notes.

## Ongoing backup rule

Whenever the user approves a sketch, design experiment, animation, or relevant source asset:
1. Save an immutable copy under a descriptive filename, including required asset dependencies.
2. Record **what was approved**, what remains exploratory, and what it is related to.
3. Record SHA-256, size and verified storage location here.
4. Prefer committing the actual files to `gallery/design-checkpoints`; if the GitHub transfer is unavailable, store in persistent Library and explicitly document the gap.
5. Continue keeping **numbered Gallery versions** and **standalone experiments** separate. Creating an experiment does not authorize a new numbered build.
6. Never generate/edit images without explicit user approval.

## New Watch History layout experiment — pending user review (2026-11-04)

- File: [Gallery-Watch-History-Layout-Experiment-01.html](../design-experiments/watch-history/Gallery-Watch-History-Layout-Experiment-01.html)
- Status: **interactive prototype for review, NOT yet approved or integrated**; not a numbered Gallery release.
- Backups: complete HTML committed to this `gallery/design-checkpoints` branch **and** saved to persistent ChatGPT Library at `/Gallery Backups/Design Experiments/2026-11-04/Gallery-Watch-History-Layout-Experiment-01.html`.
- Source file size: **37,987 bytes**
- SHA-256: `ab170c5716b773832ac963201266a5ab7d77a33d3e15c9022b3d0b31a5f5c737`
- Contains: full season-level list, short/long expandable episode management (100-episode test season), two custom fading draggable scrollbar overlays (main page and inner episode lists) matching Gallery v99 behavior, sort/status filters, historical year/title search priority, separate-season completed status, explicit Remove and session-long Undo, and representative Library/Discover routing notices.
- Browser checks (Chromium): long-list capped at 252px with all 100 rows available; hidden native scrollbar and fading overlay; manual status toggles; sorting; date-search grouping with deduplication; filters; removal/Undo; reset on navigation; 390px width without horizontal overflow; no JavaScript page errors.
- Scope: illustrative offline demo data only; does **not** modify Gallery v99 or implement real playback-history persistence.

## Watch History layout experiment 02 — two-column episode list (2026-11-04)

- File: [Gallery-Watch-History-Layout-Experiment-02.html](../design-experiments/watch-history/Gallery-Watch-History-Layout-Experiment-02.html)
- Status: **awaiting user visual review**; standalone experiment only, not integrated into Gallery v99.
- Exact HTML also saved to ChatGPT Library at `/Gallery Backups/Design Experiments/2026-11-04/Gallery-Watch-History-Layout-Experiment-02.html`.
- Source file size: **38,815 bytes**
- SHA-256: `01d6d8d983c95f1aff0c6b39e74be41af512c78de7274ba69ad8a9f98fb7046a`
- Differences from Experiment 01: two equal-width, unboxed episode columns with episode numbers flowing left-to-right across rows; subtle central divider with padding, constrained to the episode list; paired rows share the same 252px (six-row) scrolling region; responsive one-column fallback under 821px; scroll-to-latest now calculates a row index from the actual column count. Original disappearing overlay scrollbar, playback progress markings, interactive status corrections, Undo, search, sorting, and filters stay intact.
- Checks: Node syntax validation; Chromium at widths 1400, 900, 760 and 390px with no JavaScript errors or horizontal overflow; two-column vs one-column threshold; center-divider visibility; 100 episodes reachable; 12-episode list shows without an inner scrollbar on desktop; thumb appears while scrolling and fades away; episode status toggles, removal/Undo, sorting and filters work.
