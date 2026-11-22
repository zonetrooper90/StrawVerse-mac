# Gallery development — clean branch rules

**ChatGPT Project instruction location:** The version-controlled detailed instructions are at [`gallery/CHATGPT-INSTRUCTIONS.md`](gallery/CHATGPT-INSTRUCTIONS.md). Read this file on the active GitHub branch when starting or resuming Gallery work. It does not replace the mandatory safeguards below. Lightweight-first development and faster verification are approved as a **future migration**, not yet implemented; the existing dual-build/checkpoint/verification workflow remains mandatory until independently verified.

Authoritative development branch: `gallery/development-clean`.
Historical recovery branch (never modify): `gallery/working-2026-11-10-coordinated-fades`.
Stable/native application branches remain untouched.

Before any Gallery changes:
1. Read `AGENTS.md`, `gallery/WORKFLOW.md`, `gallery/PROJECT-CONTINUITY.md`, `gallery/DEVELOPMENT-STATE.md`, `gallery/APPROVED-DECISIONS.md`, and `gallery/checkpoints/current.json`.
2. Verify the authoritative editable source in `gallery/src/` and `gallery/assets/` with `python3 gallery/tools/build-gallery.py --check`. Verify generated `gallery/Gallery-current.html` byte count and SHA-256 against `gallery/checkpoints/current.json`; run `python3 gallery/tools/restore-checkpoint.py --verify-only` to independently check the immutable backup.
3. Never use old attachments, remembered files, or an earlier chat's HTML as baseline. If source, generated output or archive disagree, do not edit.

For each user-approved HTML change:
1. Preserve all approved UI/functionality, all six themes and motion decisions. Discuss before creating numbered versions; never generate/edit images without explicit approval.
2. Edit only the approved authoritative source fragments, never the generated HTML. Generate both tracked deliverables using `python3 gallery/tools/build-gallery.py --write-deliverables`, test them, and stage a NEW immutable checkpoint with `gallery/tools/stage-checkpoint.py` if full HTML bytes changed. Commit source, generated HTML and updated `current.json` together; never rewrite old checkpoints. Byte-identical source rearrangements are infrastructure-only.
3. Run relevant tests, confirm remote commit and SHA-256, and require both read-only GitHub Actions checks to pass. Never assume a GitHub error means a commit did not occur; inspect remote state.
4. Only after verification, deliver a GitHub file-page permalink to `gallery/Gallery-current.html` at the exact verified build commit (use GitHub's Download raw file control), plus the build commit URL. The pinned file bytes must match the immutable checkpoint. ChatGPT attachments are optional, not required; never transfer the large HTML just to attach it.
5. Update `gallery/DEVELOPMENT-STATE.md` with the latest verified build, task outcome, pending user testing and next proposed step. Record pending approved work before starting it; reconcile state with the actual remote pointer, commits and CI after any interruption. Do not repeat a publisher request or commit based on an Unknown Error alone.

## Permanent design rule — optical icon alignment

- Keep button/container geometry, spacing, centerlines, focus outlines and interaction areas mathematically aligned. Do not alter structural spacing to compensate for a glyph's visual imbalance.
- Icons must be optically (visually) centered within their intended containers or alignment boxes, accounting for shape, asymmetry and perceived visual weight, rather than merely centering the SVG viewBox or bounding box.
- Icons within a shared control group should have consistent perceived size and stroke weight; identical numeric glyph dimensions are not required when a deliberate optical correction is needed.
- Maintain optical centering and visual balance throughout animations and morph transitions, including interrupted/reversed motion and reduced-motion states; preserve approved interaction and accessibility behavior.
- Define optical corrections at the shared icon level wherever practical, not as conflicting page-specific layout offsets. Review rendered appearance at actual display sizes across relevant themes, states and widths; use geometry checks for structural alignment and visual review for optical alignment.
- Apply this rule to new or explicitly approved icon refinements. Do not interpret it as authorization to redesign existing approved icons, change unrelated UI, or start the deferred icon/Search-bar motion-polish milestone before maintenance is complete. Existing mathematically centered button/header rules remain in force.

Infrastructure/documentation-only edits require a verified development-branch commit and passing checks, but no new HTML checkpoint or downloadable build.
If GitHub or verification fails, report exactly what failed; never claim a build was backed up.

Recovery: a new conversation saying “Continue Gallery Development” starts by reading the above documents, checking the actual remote head, current pointer and both verification runs, and resuming the recorded task. If the state document lags, reconcile it against the verified GitHub evidence. Never treat a pending state entry as proof of publication or visual approval.
