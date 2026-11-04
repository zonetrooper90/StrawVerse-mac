# Gallery development continuity

Approved 2026-11-04. Persistent development branch: `gallery/development-archive`.

1. Every explicitly **approved** design or behavior decision must be recorded in `gallery/APPROVED-DECISIONS.md` on GitHub, clearly separated from proposed ideas and open questions.
2. Every approved new numbered Gallery HTML build must be committed as a **complete, unmodified, immutable** file under `gallery/archive/html/`. Never overwrite an earlier version; archive experiments separately under `gallery/archive/experiments/`.
3. Discuss changes before implementing them and get the user's explicit approval before creating a new numbered version. Do not use a standalone experiment as the new app build.
4. Verify every GitHub upload. If upload fails, do not claim the version is backed up. Give the user a downloadable local backup and disclose the failure.
5. At the start of future Gallery conversations, read this file, `gallery/APPROVED-DECISIONS.md`, and the most recent HTML archive snapshot. GitHub, not ephemeral chats, is the canonical source of truth.
6. No image generation or image editing without the user's **explicit prior approval**. For UI changes, use actual HTML/CSS rather than generating visual stand-ins.
7. Protect stable versions and experiments. Do not overwrite `main`, native Mac build branches, or earlier HTML versions. Keep Apple Silicon-only Mac build compatibility and StrawVerse source/repository compatibility.
8. This is a per-session working rule, **not a background automation**. GitHub commits must be performed and verified during a conversation while the connection is available.

Current HTML archive plan: `Gallery-v96.html`, `Gallery-v97.html`, `Gallery-v98.html`, `Gallery-v99.html`, plus preserved standalone player experiments.
