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
