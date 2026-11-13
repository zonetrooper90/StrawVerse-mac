# Gallery development workflow — source-first (2026-11-13)

## Branches and files

- Active working branch: `gallery/development-clean`. Do not modify the prior working branch, stable branches or `main` without explicit approval.
- Authoritative editable source: `gallery/src/` (HTML shell, ordered CSS/JS manifest and fragments), and original `gallery/assets/`.
- Generated standalone deliverables: `gallery/Gallery-current.html` (full, artwork-enabled) and `gallery/Gallery-development.html` (lightweight). Never edit either directly.
- Persistent development handoff: `gallery/DEVELOPMENT-STATE.md` (small Markdown file; records task progress and user-testing status, not a substitute for the actual pointer and CI).
- One immutable backup pointer: `gallery/checkpoints/current.json`, referencing the full, independently reconstructible archived checkpoint under `gallery/checkpoints/`.
- Earlier complete HTML deliverables and compressed historical checkpoints are retained unchanged for recovery.
- Two read-only checks: `gallery-checkpoint-integrity.yml` (content and archive integrity) and `gallery-transition-ui.yml` (navigation, motion and Watch History browser regressions).
- Old feature-specific mutating workflows are removed only from this new branch. Their Git history and the prior development branch are preserved. Do not dispatch legacy workflow scripts against a current checkpoint.

## Before editing source

1. Read `AGENTS.md`, this file, `gallery/PROJECT-CONTINUITY.md`, `gallery/DEVELOPMENT-STATE.md`, `gallery/APPROVED-DECISIONS.md` and `gallery/checkpoints/current.json`.
2. From a fresh checkout of this exact branch, run `python3 gallery/tools/restore-checkpoint.py --verify-only`.
3. SHA-256 and byte-count verify `gallery/Gallery-current.html` against the current pointer:
   `python3 -c "import hashlib,json,pathlib; p=json.loads(pathlib.Path('gallery/checkpoints/current.json').read_text()); b=pathlib.Path('gallery/Gallery-current.html').read_bytes(); assert len(b)==p['bytes'] and hashlib.sha256(b).hexdigest()==p['sha256']; print('Gallery baseline verified')"`
4. Run `python3 gallery/tools/build-gallery.py --check` to verify authoritative source reconstructs both tracked outputs exactly. Stop if source, generated output or archive disagree. Never start from previous chat attachments, historical deliverables, or old checkpoints.

## After an approved source edit

1. Make the smallest approved change to the authoritative source files. Run `python3 gallery/tools/build-gallery.py --write-deliverables` to generate both tracked HTML files and run relevant existing tests; do not modify UI/behavior for infrastructure cleanup. For byte-identical output, use an infrastructure-only commit and do not stage a checkpoint.
2. Use `python3 gallery/tools/stage-checkpoint.py --input gallery/Gallery-current.html --id YYYY-MM-DD-description --status delivered-for-user-testing` to create a NEW immutable archive and advance the LOCAL pointer.
3. Commit authoritative source, both generated HTML files, the new checkpoint folder, and `gallery/checkpoints/current.json` together; update `gallery/APPROVED-DECISIONS.md` for actual user-approved decisions. Existing archive folders remain immutable.
4. Verify the remote branch head, pointer, byte count and SHA-256. Require both GitHub Actions integrity and browser regression checks to succeed. The checks only verify; they never make commits or regenerate builds.
5. Only then provide the immutable GitHub file-page permalink `https://github.com/zonetrooper90/StrawVerse-mac/blob/<verified-build-commit>/gallery/Gallery-current.html`, with instructions to use **Download raw file** on GitHub, and the separate exact build commit URL. The linked file must be the verified canonical HTML at that commit, not a moving branch URL or a raw-code viewer alone. No ChatGPT attachment or duplicated file transfer is required. A raw link may be supplementary; do not present it as a guaranteed download. Record the checkpoint ID, SHA-256, byte count and verification result. The user can save the HTML from GitHub even if ChatGPT file storage is unavailable.
6. Update `gallery/DEVELOPMENT-STATE.md` after verification and before ending the task. Record the verified build, completed task, actual CI outcomes, delivery link availability, pending user testing/approval, and next proposed step. This small documentation-only update does not create a new HTML checkpoint.
7. If a commit, CI check or GitHub download-link verification fails, say exactly what failed. Recover from actual remote evidence and the verified last pointer, not a guessed baseline. A failure to display an attachment is no longer a development blocker.

## For infrastructure-only maintenance

Documentation, workflows and test-runner changes require a GitHub commit and passing read-only checks, but do not create a new HTML checkpoint or numbered release. Retain separate secure permissions: checks use `contents: read`; only explicitly authorized development operations write commits.

## Source-first modular build

M1 extraction was independently verified. The user subsequently approved making the smaller files authoritative before M2; there is no reverse synchronization. Use the explicit ordered `src/build-manifest.json` to preserve CSS cascade and JS execution order; output remains one inline style block and one classic script. Normal preview builds write under `gallery/dist/`, never tracked HTML or source. `--write-deliverables` is reserved for approved source changes and verifies the prior full HTML against the immutable pointer before generating both tracked files. No checkpoint is written by the builder. `--check` and source assembly tests are read-only on the actual checkout. M2+ source reorganizations require separate approval and byte-identical verification.

## Historical source

All old compressed checkpoints remain available. `gallery/tools/restore-checkpoint.py` is the recovery/verification path, while `gallery/Gallery-current.html` is the generated full deliverable. The archive, generated full HTML and source-first reconstruction must match exactly. The current HTML is a prototype, not proof of native player integration. User visual approval is separate from automated tests.

## Controlled publishing when GitHub HTML exceeds connector upload limits

The optional generic `.github/workflows/gallery-controlled-publish.yml` runs when a newly approved, narrowly scoped change script is committed under `gallery/changes/pending/`. It verifies the existing authoritative source, generated HTML and immutable baseline, applies a checksum-guarded patch to source files, rejects direct changes to generated files, assets and checkpoints, builds both HTML modes, runs browser regressions, stages a new immutable archive, and commits source, generated HTML, checkpoint and pointer together. Only a newly added request may run; byte-identical reorganizations are infrastructure-only commits, not publisher requests. This avoids transferring a multi-megabyte source file through an API that rejects large requests. The publisher explicitly dispatches both read-only verification workflows after pushing because GitHub's own workflow token does not trigger push-based workflows. Never treat the publisher's test pass as a substitute for both completed remote read-only checks. If any publishing step fails, inspect the branch head and current pointer before retrying. This is a generic publishing path, not a feature-specific workflow.

## Resume after interruption

1. Read the required documents and inspect the remote branch head, checkpoint pointer, immutable manifest and GitHub Actions runs for the actual build commit. The state document is a handoff, not an authority over these facts.
2. Before starting approved work, record its scope, expected baseline and pending status in `gallery/DEVELOPMENT-STATE.md`. Keep the record small; update it when a meaningful milestone completes, not for each tool operation. If using the controlled publisher, a state update may be included in the same commit as the approved new request. Do not touch previously applied request scripts.
3. If an operation reports Unknown Error, first check the branch head, pointer, relevant request file and workflow status. If a publisher is still queued/running, do not submit a duplicate; if it finished, verify its actual output. If it failed, diagnose from logs and the unchanged or advanced pointer before any retry.
4. If the build is verified but a conversation failed before delivery, provide the commit-pinned GitHub file link directly; do not regenerate or republish the HTML. Reconcile a stale handoff record with the verified remote state. If verification cannot be established, stop and report the blocker.
5. Only continue with a previously approved unfinished scope; otherwise propose the next change and await approval. Never infer visual acceptance or new authorization from a completed CI run.

## Approved read-only investigation queue

The explicit plan `gallery/queues/2026-11-13-infrastructure-audit.json` triggers `gallery-audit-queue.yml` only on the development branch when that plan is committed. The two unchanged independent check procedures run on the same push; the queue polls their exact-SHA push results with read-only permissions and stops on failure, cancellation, or timeout. After both succeed it rechecks assembly and runs the inventory and isolated search-syntax investigation sequentially. Output is a run summary and downloadable artifact, not a commit. No CSS correction or further publishing is automatic. A new approved plan and workflow scope are required for a later change queue. The controlled publisher retains its separate permissions and request safeguards. The archive reconstruction, macOS preview and native workflows are outside this dependency update.


## Verification efficiency — stage 1 (2026-11-13)

The independent browser workflow keeps the same workflow name, read-only permissions and exact-commit verification. All eight existing route invocations remain mandatory in two isolated runner jobs (full and lightweight); the original cross-build asset/geometry suite is a third job. All three must pass (no fail-fast or continue-on-error); each verifies checkpoint and deterministic assembly before browser tests. The shared Chromium setup installs the same pinned Playwright 1.57.0, restores/saves only an exact Ubuntu 24.04/OS/architecture/version cache, and runs the pinned install even on a hit, with one bounded retry on install failure. No fallback to another browser or skipped tests. The controlled publisher uses this setup but retains its existing sequential gate, source/checkpoint safeguards and publication logic in stage 1.

The one-off read-only benchmark runs only when `gallery/tools/benchmark-q2b1-shard.py` is added/changed on the development branch. It checksum-guards the accepted Q2-B1 full and lightweight HTML and the historical comparison gate, then executes the unchanged comparison assertions in two isolated mode shards of exactly 336 comparisons each. The historical script remains unchanged. Both jobs must pass; no candidate mutation, new checkpoint, publication or background queue. Compare measured wall time with the original 24m31s sequential comparison and 11m04s independent browser run. Consider a second stage to parallelize the publisher only after this benchmark is verified; retain fail-closed testing of the exact candidate and a single controlled checkpoint commit. No reduction in coverage or new application change.


## Verification efficiency — stage 2 (2026-11-13)

The controlled publisher invokes the read-only reusable `.github/workflows/gallery-candidate-tests.yml`. Preparation validates exactly one newly added request against its event base, verifies the immutable baseline and assembly, applies the approved patch once, builds both deliverables once, and stages only the original allowed source/build/test paths. It produces a binary Git diff, SHA-256 digest, exact candidate Git tree ID and mandatory test matrix. Every isolated runner checks out the exact request commit, downloads the same immutable artifact by ID, verifies the patch digest, applies it to its clean index, verifies the candidate tree, unchanged old pointer and byte-exact full/subtitle-preview/lightweight assembly, runs its tests, and verifies the same tree again. Standard full/lightweight route suites and cross-mode subtitle asset suite always run. The corrected historical Q2-B1 comparison is checksum-guarded and split by build mode with exactly 336 comparisons per shard; other existing single comparison gates run intact. Future approved gates may use an exact pair of `<request>-compare-full.py` and `<request>-compare-lightweight.py` or one `<request>-compare.py`; incomplete pairs and ambiguous gates fail. No historical requests or gate scripts modified.

Only after the reusable workflow succeeds may the write-permission publication job reconstruct the exact tested candidate, check the active branch still equals the request commit, stage a new immutable checkpoint, verify assembly and archive, assert that only the new checkpoint and pointer differ from the tested tree, commit once and perform a non-force push. It checks the remote head again before dispatching both independent read-only verification workflows; their success is still mandatory before delivery. No test failure is ignored. The read-only rehearsal `.github/workflows/gallery-publisher-rehearsal.yml` replays the historical corrected Q2-B1 request from its exact historical request commit, runs all five test groups, rejects a tampered patch and incorrect tree, and stages only inside a disposable worktree to reproduce the already accepted hashes. No push or remote checkpoint in rehearsal. Both independent checks and rehearsal must pass before using this pipeline for further approved work. Keep existing application, assets and checkpoints unchanged.
