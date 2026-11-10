# Gallery development workflow — mandatory GitHub source of truth

> Adopted 2026-11-10 after discovering several days of HTML changes had been delivered without a GitHub backup.

## Mandatory preflight: **before editing**

1. Check out the dedicated Gallery development branch, currently `gallery/working-2026-11-10`. Never edit `main` or a stable Mac build branch to experiment.
2. Read `AGENTS.md`, this file, `gallery/PROJECT-CONTINUITY.md`, and `gallery/APPROVED-DECISIONS.md`.
3. Reconstruct the exact current source from the repository, using `python gallery/tools/restore-checkpoint.py --output Gallery-current.html`; confirm that the SHA-256 shown agrees with `gallery/checkpoints/current.json`.
4. If a separate local/downloaded HTML file is proposed as the new base, compare it to the verified GitHub checkpoint and account for **every** difference. Never silently substitute an older standalone HTML file.
5. If GitHub/restore/verification is inaccessible, say so **before editing**. Do not claim the branch is current or backed up.

## Mandatory postflight: **for each approved change**

1. Follow the user's approval rule: discuss changes before generating a new *numbered* build; do not generate/edit images without explicit prior approval.
2. Keep earlier checkpoints immutable. Save the new, complete HTML as a new uniquely named checkpoint. Never replace or rewrite the old checkpoint/chunks.
3. Update `gallery/checkpoints/current.json` **in the same commit** to point to that new checkpoint. Record SHA-256, exact byte length, source name, and a truthful review status (`delivered`, `user-approved`, etc.).
4. Update `gallery/APPROVED-DECISIONS.md` if a design/behavior decision has been explicitly approved, and document meaningful code changes in the commit message.
5. Run the restoration integrity script and relevant UI/behavior tests. Require the GitHub Actions integrity workflow to pass. Never treat an HTML prototype as proof of native playback integration.
6. Commit the approved build to the development branch, then verify the remote branch head, checkpoint pointer, hashes, and CI status. Only **after** verification, link the new HTML to the user and report the commit.
7. If upload or CI verification fails, explicitly report **not backed up**, retain a downloadable local artifact, and do not advance the canonical GitHub pointer.

## Safety and retention

- No force pushes, branch rewrites, or overwriting previous checkpoints.
- No unreviewed automatic merge to `main` or native Mac app branches.
- Numbered releases and experimentation stay separate from the native app integration.
- Before each work session, use **GitHub as source of truth**, not chat memory, screenshots, or yesterday's download folder.
- Every response delivering a new build should give **the exact GitHub commit hash, checkpoint hash, and verification outcome**. Missing any of these is a workflow failure, not an acceptable shortcut.
- GitHub Actions can detect corrupted committed backups, but cannot magically save an HTML file that nobody pushed. The mandatory commit-and-verify step is therefore essential.

## Current checkpoint

`gallery/checkpoints/current.json` points to the last handed-off HTML (Settings Transition Fix, 2026-11-10). This is a **development checkpoint pending user visual confirmation**, not a new approved numbered release or proof of native app integration.