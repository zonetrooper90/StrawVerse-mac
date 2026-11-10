# Gallery — A+C Crossfade + Micro Depth integration, 2026-11-10

Status: **committed development HTML for user visual testing**, not native macOS app integration.

## Source-of-truth and provenance

- GitHub repository: `zonetrooper90/StrawVerse-mac`
- Dedicated development branch: `gallery/working-2026-11-10-ac-micro-depth`; main and the prior Gallery development branch are unchanged.
- **Only baseline:** byte-exact reconstructed and integrity-verified `gallery/checkpoints/2026-11-10-page-transition-route-fixes/` (SHA-256 `3fc012a9251d1fe77dab164831c9c65d993a3a5631d4f0302f1e9a9e2d48659b`; 6,942,169 bytes).
- New immutable checkpoint: `gallery/checkpoints/2026-11-10-ac-crossfade-micro-depth/`.
- New reconstructed HTML: `gallery/deliverables/Gallery-Soft-Futuristic-AC-Micro-Depth.html`.
- New HTML **SHA-256**: `0a31de142b1de4451de2709160860bae3aa66e33a8d2dce5a219d1e2e8355443`, **bytes**: 6,941,554. Pointer, manifest and recovered HTML agree.

## Behavior

- Secondary routes through Anime, Watch History, Player and Settings use a coordinated 450 ms overlapping opacity crossfade with depth no greater than 0.8%.
- Existing main Discover / Library / Downloads tab-track horizontal animation retained verbatim.
- Header/background stay outside the captured workspace. Settings entry/exit preserve the underlying page, focus/inert states, scroll restoration and History routing. Contextual Sources entry is updated inside the capture callback, avoiding a stale Settings section.
- Reduced motion skips the A+C animation; browser fallback uses gentle opacity/scale.
- No images changed; no native macOS project code changed.

## Verification

- `gallery/tools/restore-checkpoint.py --verify-only` passed before and after modification.
- Existing `gallery/tests/test_transitions.py` route and Watch History suite passed in Chromium on Ubuntu 24.04.
- New `gallery/tests/test_ac_motion.py`: **43 assertions passed**, desktop, narrow layout and reduced motion, including Settings and Sources deep link.
- Integration/checkpoint and commit workflow: [Gallery A+C implementation and checkpoint — success](https://github.com/zonetrooper90/StrawVerse-mac/actions/runs/42834192628).
- Standard Gallery checkpoint and route workflow verification should be checked against the final development branch commit before declaring delivery finished.

User visual approval of the integrated HTML remains pending.
