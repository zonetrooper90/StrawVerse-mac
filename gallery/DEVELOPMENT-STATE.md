# Gallery development state

Last updated: 2026-11-12. This is a handoff record, not a substitute for GitHub verification or explicit user approval.

## Current verified HTML build
- Active branch: `gallery/development-clean`.
- Checkpoint: `2026-11-12-retired-subtitle-layout-css`.
- HTML build commit: `881e81eda806da1eac4d901fd2a2a75803e74980`.
- SHA-256: `64942fe6416fcd07de902b24c46cc20414af3ff5ba48a7e67a7f5f729c8370c5`.
- Bytes: 6,916,467.
- [Download exact HTML (use GitHub Download raw file)](https://github.com/zonetrooper90/StrawVerse-mac/blob/881e81eda806da1eac4d901fd2a2a75803e74980/gallery/Gallery-current.html).
- [Build commit](https://github.com/zonetrooper90/StrawVerse-mac/commit/881e81eda806da1eac4d901fd2a2a75803e74980).
- [Integrity and archive round-trip: passed](https://github.com/zonetrooper90/StrawVerse-mac/actions/runs/43220117546). Logs confirm the canonical HTML and immutable archive have the same SHA-256 and size.
- [Browser regression: passed](https://github.com/zonetrooper90/StrawVerse-mac/actions/runs/43220122405).
- User visual acceptance: **pending** for the maintenance build. The previous ChatGPT attachment attempt was interrupted; the commit-pinned GitHub file is now the approved delivery route. A checkpoint status of delivered-for-user-testing is not evidence of actual user receipt or visual approval.

## Last completed HTML work
- Remove obsolete pre-release preference migrations (previous checkpoint; user approved removal, not backwards compatibility).
- Maintainability audit C1: remove retired subtitle-layout selector branches only, preserving the active shared subtitle preview rules and current responsive layouts. The patch removes 262 full rules plus one retired branch from a shared rule; existing browser regression includes before/after subtitle layout comparison. No artwork or native application changes.

## Current infrastructure task
- GitHub permalink delivery and recoverable handoff completed at documentation commit `238b2c624b2cd9b33c35f7aba68a861f2857cb3e`. Both read-only checks passed: [integrity](https://github.com/zonetrooper90/StrawVerse-mac/actions/runs/43226076109) and [browser](https://github.com/zonetrooper90/StrawVerse-mac/actions/runs/43226076367). Integrity logs confirm canonical HTML and restored archive match the current pointer's SHA-256 and 6,916,467 bytes.
- User approved a fresh ChatGPT project and staged modularization investigation to reduce large-file handling and historical context. Unknown Error root cause remains unconfirmed. Keep old ChatGPT project as archive; new project setup is a manual user action.
- Approved sequence: verify baseline (done), establish fresh project, audit HTML structure/assets/dependencies, propose deterministic build system, then extract modules incrementally with tests. First modular build should reproduce the existing HTML byte-for-byte where feasible. Do not change canonical HTML, checkpoint format, source authority or approved behavior until a specific architecture/migration is agreed. Keep standalone HTML delivery.
- No new HTML checkpoint, numbered version, image changes or publisher request is authorized by this handoff alone.

## Approved pending milestone — asset separation
- User approved on 2026-11-12: default lightweight development HTML without the two embedded shrine PNGs; an opt-in subtitle-preview/full HTML with original artwork; full native macOS builds will include the original assets when native integration is separately undertaken. Retain the preview layout, overlay, controls, day/night behavior and animations; use plain day/night backgrounds in the lightweight variant. No artwork generation, editing or reencoding.
- Baseline: checkpoint `2026-11-12-retired-subtitle-layout-css`, SHA-256 `64942fe6416fcd07de902b24c46cc20414af3ff5ba48a7e67a7f5f729c8370c5`. Keep canonical full HTML and immutable checkpoint unchanged during this infrastructure milestone. Introduce deterministic source extraction/build, prove full byte-for-byte round trip, and test lightweight/full modes before delivery. Do not switch canonical source authority yet. Status: implemented in `1dcc590a37517ef82f4c37417b68383c4b67c8a3`; [integrity](https://github.com/zonetrooper90/StrawVerse-mac/actions/runs/43266204511) passed, proving exact full reconstruction and 600,785-byte lightweight output (SHA-256 `16430b06dc17a9e2de022bc97ca94d71ac338eeaadd0e58f6330c3cd0236961d`). [Browser run](https://github.com/zonetrooper90/StrawVerse-mac/actions/runs/43266204599) passed the existing regression suites on both HTML variants but failed the new live reduced-motion assertion on the original full HTML first. The test-only correction loads the actual local file with explicit initial motion preference and reports media-query/layer diagnostics if the live switch still fails; no application code changed and no reduced-motion assertion removed. Both verification workflows must pass before lightweight delivery. Files: `gallery/src/Gallery.template.html`, `gallery/assets/subtitle-preview/shrine-day.png`, `shrine-night.png`, `gallery/tools/build-gallery.py`, `gallery/Gallery-development.html`. Full and subtitle-preview modes reconstruct the canonical HTML; the lightweight variant has CSS color layers instead of PNG payloads. Keep source authority unchanged and do not run legacy publisher requests until the source synchronization workflow is agreed. See `gallery/src/README.md`.

## Pending / next step
- Next: complete both verification workflows for the implemented asset-separation milestone; diagnose any remaining browser failure before delivery. Continue structural audit and CSS/JS extraction discussion afterwards. Keep the existing C1 cleanup visual test pending.
- User can download and visually test the existing C1 cleanup build before further changes.
- Suggested next maintenance task: review audit C2 (retired theme-only CSS), then C3 (duplicate cascade/keyframe candidates), one narrow approved scope at a time. See `gallery/audits/2026-11-12-maintainability-audit.md`. The audit's old migration and attachment requirements are superseded by current decisions.
- After the agreed code cleanup, separately discuss/approve direct background dithering integration (Light preferred trial, Fine alternative). Keep all six themes and the stationary backdrop.
- No known in-flight publisher request for this checkpoint; inspect remote Actions and pointer before assuming this remains true.

## Recovery procedure
Read `AGENTS.md`, `gallery/WORKFLOW.md`, `gallery/PROJECT-CONTINUITY.md`, this file, `gallery/APPROVED-DECISIONS.md` and `gallery/checkpoints/current.json`. Verify the actual remote working HTML/checkpoint and CI. If the remote head or pointer advanced, reconcile this handoff with commits, manifests and workflow runs; never rebuild or duplicate an existing request because a conversation failed. Resume only the recorded approved unfinished scope; otherwise ask for approval of the next proposed change. Update this file at meaningful milestones.
