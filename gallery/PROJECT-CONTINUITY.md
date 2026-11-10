# Gallery development continuity

Approved 2026-11-04; revised 2026-11-10. Historical archive: `gallery/development-archive`. Active checkpoint/work branch: `gallery/working-2026-11-10`.

1. Every explicitly **approved** design or behavior decision must be recorded in `gallery/APPROVED-DECISIONS.md` on GitHub, clearly separated from proposed ideas and open questions.
2. Every approved new numbered Gallery HTML build must be committed as a **complete, exact, immutable, SHA-256-verified** snapshot (direct HTML or a byte-exact reconstructible archive). New checkpoints live under `gallery/checkpoints/` with an updated `gallery/checkpoints/current.json`; never overwrite an earlier version. Archive experiments separately.
3. Discuss changes before implementing them and get the user's explicit approval before creating a new numbered version. Do not use a standalone experiment as the new app build.
4. Verify every GitHub upload. If upload fails, do not claim the version is backed up. Give the user a downloadable local backup and disclose the failure.
5. At the start of future Gallery conversations, read `AGENTS.md`, `gallery/WORKFLOW.md`, this file, `gallery/APPROVED-DECISIONS.md`, and **restore/checksum-verify the checkpoint named by `gallery/checkpoints/current.json`**. Never guess which downloaded HTML was the latest. GitHub is the source of truth.
6. No image generation or image editing without the user's **explicit prior approval**. For UI changes, use actual HTML/CSS rather than generating visual stand-ins.
7. Protect stable versions and experiments. Do not overwrite `main`, native Mac build branches, or earlier HTML versions. Keep Apple Silicon-only Mac build compatibility and StrawVerse source/repository compatibility.
8. This is a per-session working rule, **not a background automation**. GitHub commits must be performed and verified during a conversation while the connection is available.
9. **Mandatory user download:** after GitHub checkpoint verification, provide the actual SHA-256-verified HTML as a downloadable ChatGPT attachment (ZIP optional). Raw GitHub code links are not a substitute. If attachment verification fails, disclose incomplete delivery; see `gallery/WORKFLOW.md`.

Old HTML history: `Gallery-v96.html`, `Gallery-v97.html`, `Gallery-v98.html`, `Gallery-v99.html`, plus standalone experiments. The 2026-11-10 Settings Transition Fix HTML is saved as an immutable, reconstructible checkpoint pending user validation. Follow `gallery/WORKFLOW.md` on every future build.
