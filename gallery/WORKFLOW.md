# Gallery development workflow — mandatory GitHub source of truth

> Adopted 2026-11-10 after discovering several days of HTML changes had been delivered without a GitHub backup.

## Mandatory preflight: **before editing**

1. Check out the dedicated Gallery development branch, currently `gallery/working-2026-11-10-ac-micro-depth`. Never edit `main` or a stable Mac build branch to experiment.
2. Read `AGENTS.md`, this file, `gallery/PROJECT-CONTINUITY.md`, and `gallery/APPROVED-DECISIONS.md`.
3. Reconstruct the exact current source from the repository, using `python gallery/tools/restore-checkpoint.py --output Gallery-current.html`; confirm that the SHA-256 shown agrees with `gallery/checkpoints/current.json`.
4. If a separate local/downloaded HTML file is proposed as the new base, compare it to the verified GitHub checkpoint and account for **every** difference. Never silently substitute an older standalone HTML file.
5. If GitHub/restore/verification is inaccessible, say so **before editing**. Do not claim the branch is current or backed up.

## Mandatory postflight: **for each approved change**

1. Follow the user's approval rule: discuss changes before generating a new *numbered* build; do not generate/edit images without explicit prior approval.
2. Keep earlier checkpoints immutable. To stage a new full HTML, run `python3 gallery/tools/stage-checkpoint.py --input <tested>.html --id YYYY-MM-DD-slug --status delivered-for-user-testing` (or `user-approved` only after the user verifies it). This creates a new exact archive and verifies its bytes locally. Never replace older chunks.
3. Commit the newly staged `gallery/checkpoints/current.json` **in the same commit** as the new archive. The staging script sets the SHA-256, byte count and review status automatically. The staging script does **not** push or commit anything itself.
4. Update `gallery/APPROVED-DECISIONS.md` if a design/behavior decision has been explicitly approved, and document meaningful code changes in the commit message.
5. Run the restoration integrity script and relevant UI/behavior tests. Require the GitHub Actions integrity workflow to pass. Never treat an HTML prototype as proof of native playback integration.
6. Commit the approved build to the development branch, then verify the remote branch head, checkpoint pointer, hashes, and CI status. Only **after** verification, link the new HTML to the user and report the commit.
7. If upload or CI verification fails, explicitly report **not backed up**, retain a downloadable local artifact, and do not advance the canonical GitHub pointer.

## Mandatory downloadable Gallery file delivery

For every completed Gallery HTML build, UI experiment, or updated prototype delivered for user testing:

1. **Provide a real ChatGPT download attachment for the complete `.html` file** and a clickable, verified `sandbox:/mnt/data/...` link in the final answer. A ZIP containing the same HTML may be included as an alternative; the direct HTML is preferred.
2. Verify that the exact attachment exists in the current container/session and that its SHA-256 and byte count match the committed, checksum-verified GitHub checkpoint. Never reuse an unverified sandbox path, older downloaded HTML, or chat attachment as a development baseline.
3. **GitHub raw-file links, blob/source-code viewers, GitHub commit URLs, and GitHub Actions artifact pages are not substitutes for a downloadable ChatGPT attachment.** Keep the GitHub commit link separately for provenance.
4. The commit, immutable checkpoint/pointer, integrity verification, and required CI checks must all succeed **before** the new HTML is handed off. If creating or verifying the attachment fails, state clearly that the user has **not** received the required download; never mark delivery as complete or invent a link.
5. Documentation-only changes do not create a new numbered Gallery build or require a new HTML checkpoint. They still require a verified GitHub commit on the dedicated development branch.

## Safety and retention

- No force pushes, branch rewrites, or overwriting previous checkpoints.
- No unreviewed automatic merge to `main` or native Mac app branches.
- Numbered releases and experimentation stay separate from the native app integration.
- Before each work session, use **GitHub as source of truth**, not chat memory, screenshots, or yesterday's download folder.
- Every response delivering a new build should give **the exact GitHub commit hash, checkpoint hash, and verification outcome**. Missing any of these is a workflow failure, not an acceptable shortcut.
- GitHub Actions can detect corrupted committed backups, but cannot magically save an HTML file that nobody pushed. The mandatory commit-and-verify step is therefore essential.

## Current checkpoint

`gallery/checkpoints/current.json` points to the latest immutable Gallery HTML checkpoint on this development branch (A+C Crossfade + Micro Depth, 2026-11-10). This is a **development checkpoint pending user visual confirmation**, not a new approved numbered release or proof of native app integration.