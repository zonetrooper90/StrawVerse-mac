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
- User approved switching to GitHub file-page permalinks, recording this handoff, and updating the repository workflow rules. This documentation-only change leaves the working HTML and checkpoint pointer untouched. Inspect the actual documentation commit and its CI runs to establish completion; this file alone does not claim the new documentation CI passed.
- ChatGPT project instructions must be kept consistent with `AGENTS.md` and `gallery/WORKFLOW.md`; project settings may require manual editing by the user.

## Pending / next step
- No additional HTML change is authorized by the infrastructure task.
- User can download and visually test the existing C1 cleanup build before further changes.
- Suggested next maintenance task: review audit C2 (retired theme-only CSS), then C3 (duplicate cascade/keyframe candidates), one narrow approved scope at a time. See `gallery/audits/2026-11-12-maintainability-audit.md`. The audit's old migration and attachment requirements are superseded by current decisions.
- After the agreed code cleanup, separately discuss/approve direct background dithering integration (Light preferred trial, Fine alternative). Keep all six themes and the stationary backdrop.
- No known in-flight publisher request for this checkpoint; inspect remote Actions and pointer before assuming this remains true.

## Recovery procedure
Read `AGENTS.md`, `gallery/WORKFLOW.md`, `gallery/PROJECT-CONTINUITY.md`, this file, `gallery/APPROVED-DECISIONS.md` and `gallery/checkpoints/current.json`. Verify the actual remote working HTML/checkpoint and CI. If the remote head or pointer advanced, reconcile this handoff with commits, manifests and workflow runs; never rebuild or duplicate an existing request because a conversation failed. Resume only the recorded approved unfinished scope; otherwise ask for approval of the next proposed change. Update this file at meaningful milestones.
