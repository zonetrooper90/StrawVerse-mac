# Gallery development — clean branch rules

Authoritative development branch: `gallery/development-clean`.
Historical recovery branch (never modify): `gallery/working-2026-11-10-coordinated-fades`.
Stable/native application branches remain untouched.

Before any Gallery changes:
1. Read `AGENTS.md`, `gallery/WORKFLOW.md`, `gallery/PROJECT-CONTINUITY.md`, `gallery/DEVELOPMENT-STATE.md`, `gallery/APPROVED-DECISIONS.md`, and `gallery/checkpoints/current.json`.
2. Retrieve `gallery/Gallery-current.html` from this branch and verify byte count and SHA-256 against `gallery/checkpoints/current.json`. Run `python3 gallery/tools/restore-checkpoint.py --verify-only` to independently check the immutable backup.
3. Never use old attachments, remembered files, or an earlier chat's HTML as baseline. If either integrity check fails, do not edit.

For each user-approved HTML change:
1. Preserve all approved UI/functionality, all six themes and motion decisions. Discuss before creating numbered versions; never generate/edit images without explicit approval.
2. Edit and test the complete HTML, commit it as `gallery/Gallery-current.html`, and stage a NEW immutable checkpoint with `gallery/tools/stage-checkpoint.py`. Advance `current.json` in the same commit; never rewrite old checkpoints.
3. Run relevant tests, confirm remote commit and SHA-256, and require both read-only GitHub Actions checks to pass. Never assume a GitHub error means a commit did not occur; inspect remote state.
4. Only after verification, deliver a GitHub file-page permalink to `gallery/Gallery-current.html` at the exact verified build commit (use GitHub's Download raw file control), plus the build commit URL. The pinned file bytes must match the immutable checkpoint. ChatGPT attachments are optional, not required; never transfer the large HTML just to attach it.
5. Update `gallery/DEVELOPMENT-STATE.md` with the latest verified build, task outcome, pending user testing and next proposed step. Record pending approved work before starting it; reconcile state with the actual remote pointer, commits and CI after any interruption. Do not repeat a publisher request or commit based on an Unknown Error alone.

Infrastructure/documentation-only edits require a verified development-branch commit and passing checks, but no new HTML checkpoint or downloadable build.
If GitHub or verification fails, report exactly what failed; never claim a build was backed up.

Recovery: a new conversation saying “Continue Gallery Development” starts by reading the above documents, checking the actual remote head, current pointer and both verification runs, and resuming the recorded task. If the state document lags, reconcile it against the verified GitHub evidence. Never treat a pending state entry as proof of publication or visual approval.
