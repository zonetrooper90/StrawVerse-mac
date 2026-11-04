# Gallery project continuity for coding assistants

This branch is the dedicated Gallery development and backup branch. Before answering questions or editing Gallery:

1. Read `gallery/PROJECT-CONTINUITY.md` (mandatory approval and backup workflow).
2. Read `gallery/APPROVED-DECISIONS.md` (settled design and behavior decisions).
3. Use the latest approved snapshot from `gallery/archive/html/`. As of 2026-11-04 the latest is `Gallery-v99.html`; verify the manifest/checksums rather than guessing.
4. Commit **each explicitly approved decision** to the decision record during the active conversation. Back up **each user-approved numbered HTML build** as a new immutable snapshot, and verify its GitHub presence. Never silently overwrite older versions.
5. Keep the original native Mac app source and other branches intact. Do not create new numbered builds or generate/edit images without the user's prior explicit approval.
6. If GitHub is unavailable, state that the commit did not happen and provide a local backup. Never promise an upload will occur asynchronously.

Complete HTML versions v96 A28 through v99, standalone experiments, original design decisions and SHA-256 manifests are archived here. Snapshot reconstruction from chunked uploads is handled by `gallery/archive/assemble.py` and the dedicated GitHub Actions workflow.
