# Gallery development — clean branch rules

Authoritative development branch: `gallery/development-clean`.
Historical recovery branch (never modify): `gallery/working-2026-11-10-coordinated-fades`.
Stable/native application branches remain untouched.

Before any Gallery changes:
1. Read `AGENTS.md`, `gallery/WORKFLOW.md`, `gallery/PROJECT-CONTINUITY.md`, `gallery/APPROVED-DECISIONS.md`, and `gallery/checkpoints/current.json`.
2. Retrieve `gallery/Gallery-current.html` from this branch and verify byte count and SHA-256 against `gallery/checkpoints/current.json`. Run `python3 gallery/tools/restore-checkpoint.py --verify-only` to independently check the immutable backup.
3. Never use old attachments, remembered files, or an earlier chat's HTML as baseline. If either integrity check fails, do not edit.

For each user-approved HTML change:
1. Preserve all approved UI/functionality, all six themes and motion decisions. Discuss before creating numbered versions; never generate/edit images without explicit approval.
2. Edit and test the complete HTML, commit it as `gallery/Gallery-current.html`, and stage a NEW immutable checkpoint with `gallery/tools/stage-checkpoint.py`. Advance `current.json` in the same commit; never rewrite old checkpoints.
3. Run relevant tests, confirm remote commit and SHA-256, and require both read-only GitHub Actions checks to pass. Never assume a GitHub error means a commit did not occur; inspect remote state.
4. Only after verification, deliver a directly downloadable, matching HTML attachment in ChatGPT, plus the GitHub commit link. GitHub links alone are not file delivery.

Infrastructure/documentation-only edits require a verified development-branch commit and passing checks, but no new HTML checkpoint or downloadable build.
If GitHub or verification fails, report exactly what failed; never claim a build was backed up.
