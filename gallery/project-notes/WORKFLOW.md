# Gallery continuity and backup rules

This branch is the source-of-truth **handoff and design-checkpoint branch** for the Gallery macOS client. It is separate from the original StrawVerse Mac app and from exploratory playback work.

## Rules for future Gallery work

1. **Discuss before coding.** Do not create a new numbered HTML build until the user explicitly approves implementation. A user can separately approve a standalone experiment without approving a new Gallery version.
2. **Capture decisions after agreement.** Following any meaningful agreed Gallery design or behavior decision, update `gallery/project-notes/DECISIONS.md` on this branch and commit it. Distinguish **agreed**, **proposed**, and **needs verification**. Never quietly replace prior decisions.
3. **Every numbered HTML milestone must have its own immutable copy** (`Gallery-vNN.html`, never overwrite a prior version), and a clear note about changes, tests, limitations, and source version. Save it in the versioned backup area and, when technically feasible, commit the actual HTML and resources to this branch.
4. **Never claim a backup exists until verified**: check the GitHub commit/ref or the saved persistent-file location and ideally a checksum. If a GitHub upload of large binary/HTML assets cannot be completed, say that clearly and provide a separately verified persistent backup, not a misleading "synced" claim.
5. **Keep the working Mac application separate.** Do not merge experiment or HTML snapshots into `main` or any native-app production branch without user approval.
6. **For a new conversation**, read this document and `DECISIONS.md` and inspect the latest versioned artifact before proposing changes. Prefer the verified artifact over remembered descriptions.
7. **No image generation or edits** for Gallery or its mockups without the user's explicit prior approval.
8. Support Apple Silicon macOS, remain compatible with StrawVerse sources/repositories, and preserve the user's approved designs.

## Restore / handoff

- Latest HTML milestone known at initial setup: **Gallery v99** (2026-11-04).
- Older HTML milestones and test experiments are recorded with SHA-256 checksums in `gallery/project-notes/VERSION-INDEX.md`.
- The Gallery HTML prototype is distinct from the native macOS app; a checked-in older Gallery app source is **not** the same as the latest HTML.
- Continuity requires both the **decisions** and the **actual source snapshot**; neither one alone is an adequate backup.

## Important limits

A document like this establishes the team's development convention, **not an unattended background sync**. Each future update still requires a successful write to GitHub and verification. This branch's notes must not be mistaken for proof that every HTML file is on GitHub.
