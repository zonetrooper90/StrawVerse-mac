# Gallery project continuity for coding assistants

This branch is a dedicated Gallery development/backup workspace. The older `gallery/development-archive` branch remains an immutable historical base. Before answering questions or editing Gallery:

1. Read `gallery/PROJECT-CONTINUITY.md` (mandatory approval and backup workflow).
2. Read `gallery/APPROVED-DECISIONS.md` (settled design and behavior decisions).
3. **Mandatory preflight:** read `gallery/WORKFLOW.md` and reconstruct `gallery/checkpoints/current.json` with `python3 gallery/tools/restore-checkpoint.py --verify-only` before editing. This current pointer supersedes the historical `gallery/archive/html/Gallery-v99.html` source for new development. Never start from an older download.
4. **Mandatory postflight:** update the decision record when a decision is approved. Commit each user-approved build as a new immutable complete, hash-verified checkpoint and advance `gallery/checkpoints/current.json` in the same commit. Verify branch head, checksum, and GitHub Actions before handing it off. Never silently overwrite older versions.
5. Keep the original native Mac app source and other branches intact. Do not create new numbered builds or generate/edit images without the user's prior explicit approval.
6. If GitHub is unavailable, state that the commit did not happen and provide a local backup. Never promise an upload will occur asynchronously.

Historical HTML versions v96 A28 through v99 remain archived under `gallery/archive/`. Newer checkpoints are under `gallery/checkpoints/` and are reconstructed with `gallery/tools/restore-checkpoint.py`; GitHub Actions checks the exact bytes. The 2026-11-10 current checkpoint is **delivered, not yet visually approved by the user**; do not imply native app integration.
