# Gallery development workflow — simplified (2026-11-11)

## Branches and files

- Active working branch: `gallery/development-clean`. Do not modify the prior working branch, stable branches or `main` without explicit approval.
- One plain HTML editing baseline: `gallery/Gallery-current.html` (complete, directly readable in a Git checkout).
- One immutable backup pointer: `gallery/checkpoints/current.json`, referencing the full, independently reconstructible archived checkpoint under `gallery/checkpoints/`.
- Earlier complete HTML deliverables and compressed historical checkpoints are retained unchanged for recovery.
- Two read-only checks: `gallery-checkpoint-integrity.yml` (content and archive integrity) and `gallery-transition-ui.yml` (navigation, motion and Watch History browser regressions).
- Old feature-specific mutating workflows are removed only from this new branch. Their Git history and the prior development branch are preserved. Do not dispatch legacy workflow scripts against a current checkpoint.

## Before editing HTML

1. Read `AGENTS.md`, this file, `gallery/PROJECT-CONTINUITY.md`, `gallery/APPROVED-DECISIONS.md` and `gallery/checkpoints/current.json`.
2. From a fresh checkout of this exact branch, run `python3 gallery/tools/restore-checkpoint.py --verify-only`.
3. SHA-256 and byte-count verify `gallery/Gallery-current.html` against the current pointer:
   `python3 -c "import hashlib,json,pathlib; p=json.loads(pathlib.Path('gallery/checkpoints/current.json').read_text()); b=pathlib.Path('gallery/Gallery-current.html').read_bytes(); assert len(b)==p['bytes'] and hashlib.sha256(b).hexdigest()==p['sha256']; print('Gallery baseline verified')"`
4. Stop if the two representations disagree. Never start from previous chat attachments, historical deliverables, or old checkpoints.

## After an approved HTML edit

1. Make the smallest approved change to the canonical complete HTML and run relevant existing tests; do not modify UI/behavior for infrastructure cleanup.
2. Use `python3 gallery/tools/stage-checkpoint.py --input gallery/Gallery-current.html --id YYYY-MM-DD-description --status delivered-for-user-testing` to create a NEW immutable archive and advance the LOCAL pointer.
3. Commit `gallery/Gallery-current.html`, the new checkpoint folder, and `gallery/checkpoints/current.json` together; update `gallery/APPROVED-DECISIONS.md` for actual user-approved decisions. Existing archive folders remain immutable.
4. Verify the remote branch head, pointer, byte count and SHA-256. Require both GitHub Actions integrity and browser regression checks to succeed. The checks only verify; they never make commits or regenerate builds.
5. Only then provide a directly downloadable HTML attachment in the ChatGPT conversation, checksum-verified to match the committed checkpoint, and include the exact GitHub commit URL. An Actions artifact or raw source URL is not sufficient.
6. If a commit, CI check, or attachment fails, say what failed and do not claim successful delivery. Recover from the verified last pointer, not a guessed baseline.

## For infrastructure-only maintenance

Documentation, workflows and test-runner changes require a GitHub commit and passing read-only checks, but do not create a new HTML checkpoint or numbered release. Retain separate secure permissions: checks use `contents: read`; only explicitly authorized development operations write commits.

## Historical source

All old compressed checkpoints remain available. `gallery/tools/restore-checkpoint.py` is the recovery/verification path, while `gallery/Gallery-current.html` is the everyday editing baseline. Their hashes must match. The current HTML is a prototype, not proof of native player integration. User visual approval is separate from automated tests.

## Controlled publishing when GitHub HTML exceeds connector upload limits

The optional generic `.github/workflows/gallery-controlled-publish.yml` runs when a newly approved, narrowly scoped change script is committed under `gallery/changes/pending/`. It reads the GitHub working HTML, checks the current immutable baseline, applies a checksum-guarded patch, runs browser regressions, stages a new immutable archive, and commits the HTML, checkpoint and pointer together. This avoids transferring a multi-megabyte source file through an API that rejects large requests. The publisher explicitly dispatches both read-only verification workflows after pushing because GitHub's own workflow token does not trigger push-based workflows. Never treat the publisher's test pass as a substitute for both completed remote read-only checks. If any publishing step fails, inspect the branch head and current pointer before retrying. This is a generic publishing path, not a feature-specific workflow.
