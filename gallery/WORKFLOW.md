# Gallery development workflow — simplified (2026-11-12)

## Branches and files

- Active working branch: `gallery/development-clean`. Do not modify the prior working branch, stable branches or `main` without explicit approval.
- One plain HTML editing baseline: `gallery/Gallery-current.html` (complete, directly readable in a Git checkout).
- Persistent development handoff: `gallery/DEVELOPMENT-STATE.md` (small Markdown file; records task progress and user-testing status, not a substitute for the actual pointer and CI).
- One immutable backup pointer: `gallery/checkpoints/current.json`, referencing the full, independently reconstructible archived checkpoint under `gallery/checkpoints/`.
- Earlier complete HTML deliverables and compressed historical checkpoints are retained unchanged for recovery.
- Two read-only checks: `gallery-checkpoint-integrity.yml` (content and archive integrity) and `gallery-transition-ui.yml` (navigation, motion and Watch History browser regressions).
- Old feature-specific mutating workflows are removed only from this new branch. Their Git history and the prior development branch are preserved. Do not dispatch legacy workflow scripts against a current checkpoint.

## Before editing HTML

1. Read `AGENTS.md`, this file, `gallery/PROJECT-CONTINUITY.md`, `gallery/DEVELOPMENT-STATE.md`, `gallery/APPROVED-DECISIONS.md` and `gallery/checkpoints/current.json`.
2. From a fresh checkout of this exact branch, run `python3 gallery/tools/restore-checkpoint.py --verify-only`.
3. SHA-256 and byte-count verify `gallery/Gallery-current.html` against the current pointer:
   `python3 -c "import hashlib,json,pathlib; p=json.loads(pathlib.Path('gallery/checkpoints/current.json').read_text()); b=pathlib.Path('gallery/Gallery-current.html').read_bytes(); assert len(b)==p['bytes'] and hashlib.sha256(b).hexdigest()==p['sha256']; print('Gallery baseline verified')"`
4. Stop if the two representations disagree. Never start from previous chat attachments, historical deliverables, or old checkpoints.

## After an approved HTML edit

1. Make the smallest approved change to the canonical complete HTML and run relevant existing tests; do not modify UI/behavior for infrastructure cleanup.
2. Use `python3 gallery/tools/stage-checkpoint.py --input gallery/Gallery-current.html --id YYYY-MM-DD-description --status delivered-for-user-testing` to create a NEW immutable archive and advance the LOCAL pointer.
3. Commit `gallery/Gallery-current.html`, the new checkpoint folder, and `gallery/checkpoints/current.json` together; update `gallery/APPROVED-DECISIONS.md` for actual user-approved decisions. Existing archive folders remain immutable.
4. Verify the remote branch head, pointer, byte count and SHA-256. Require both GitHub Actions integrity and browser regression checks to succeed. The checks only verify; they never make commits or regenerate builds.
5. Only then provide the immutable GitHub file-page permalink `https://github.com/zonetrooper90/StrawVerse-mac/blob/<verified-build-commit>/gallery/Gallery-current.html`, with instructions to use **Download raw file** on GitHub, and the separate exact build commit URL. The linked file must be the verified canonical HTML at that commit, not a moving branch URL or a raw-code viewer alone. No ChatGPT attachment or duplicated file transfer is required. A raw link may be supplementary; do not present it as a guaranteed download. Record the checkpoint ID, SHA-256, byte count and verification result. The user can save the HTML from GitHub even if ChatGPT file storage is unavailable.
6. Update `gallery/DEVELOPMENT-STATE.md` after verification and before ending the task. Record the verified build, completed task, actual CI outcomes, delivery link availability, pending user testing/approval, and next proposed step. This small documentation-only update does not create a new HTML checkpoint.
7. If a commit, CI check or GitHub download-link verification fails, say exactly what failed. Recover from actual remote evidence and the verified last pointer, not a guessed baseline. A failure to display an attachment is no longer a development blocker.

## For infrastructure-only maintenance

Documentation, workflows and test-runner changes require a GitHub commit and passing read-only checks, but do not create a new HTML checkpoint or numbered release. Retain separate secure permissions: checks use `contents: read`; only explicitly authorized development operations write commits.

## Historical source

All old compressed checkpoints remain available. `gallery/tools/restore-checkpoint.py` is the recovery/verification path, while `gallery/Gallery-current.html` is the everyday editing baseline. Their hashes must match. The current HTML is a prototype, not proof of native player integration. User visual approval is separate from automated tests.

## Controlled publishing when GitHub HTML exceeds connector upload limits

The optional generic `.github/workflows/gallery-controlled-publish.yml` runs when a newly approved, narrowly scoped change script is committed under `gallery/changes/pending/`. It reads the GitHub working HTML, checks the current immutable baseline, applies a checksum-guarded patch, runs browser regressions, stages a new immutable archive, and commits the HTML, checkpoint and pointer together. This avoids transferring a multi-megabyte source file through an API that rejects large requests. The publisher explicitly dispatches both read-only verification workflows after pushing because GitHub's own workflow token does not trigger push-based workflows. Never treat the publisher's test pass as a substitute for both completed remote read-only checks. If any publishing step fails, inspect the branch head and current pointer before retrying. This is a generic publishing path, not a feature-specific workflow.

## Resume after interruption

1. Read the required documents and inspect the remote branch head, checkpoint pointer, immutable manifest and GitHub Actions runs for the actual build commit. The state document is a handoff, not an authority over these facts.
2. Before starting approved work, record its scope, expected baseline and pending status in `gallery/DEVELOPMENT-STATE.md`. Keep the record small; update it when a meaningful milestone completes, not for each tool operation. If using the controlled publisher, a state update may be included in the same commit as the approved new request. Do not touch previously applied request scripts.
3. If an operation reports Unknown Error, first check the branch head, pointer, relevant request file and workflow status. If a publisher is still queued/running, do not submit a duplicate; if it finished, verify its actual output. If it failed, diagnose from logs and the unchanged or advanced pointer before any retry.
4. If the build is verified but a conversation failed before delivery, provide the commit-pinned GitHub file link directly; do not regenerate or republish the HTML. Reconcile a stale handoff record with the verified remote state. If verification cannot be established, stop and report the blocker.
5. Only continue with a previously approved unfinished scope; otherwise propose the next change and await approval. Never infer visual acceptance or new authorization from a completed CI run.
