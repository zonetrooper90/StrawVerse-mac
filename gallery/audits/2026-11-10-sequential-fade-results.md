# Gallery — sequential fade implementation audit (2026-11-10)

## Reason for change
The user viewed the A+C implementation recording, rejected the overlapping 450ms ghosting effect and explicitly authorized trying a 150ms fade out followed by a 150ms fade in without overlap.

## Current delivered-for-testing checkpoint
- Branch: gallery/working-2026-11-10-sequential-fade
- Checkpoint folder: gallery/checkpoints/2026-11-10-sequential-fade-no-overlap
- HTML: gallery/deliverables/Gallery-Soft-Futuristic-Sequential-Fade.html
- SHA-256: 5b81d793f474fcf94bc1cd719f8a848cad66e63129b937fbd20450aa5c2d094f
- Bytes: 6941156
- Initial baseline sha: 0a31de142b1de4451de2709160860bae3aa66e33a8d2dce5a219d1e2e8355443

## Behavioral changes
The stage fades out from 1 to 0 opacity over 150ms, and the next page fades in over the following 150ms (300ms total). The incoming view stays fully transparent until the outgoing view is invisible. No transforms, blurs, or simultaneous page content. The default root snapshot and UA stage group resizing are disabled so the common header/background do not animate. Existing navigation mutations, main tab slides, detail/player/history layouts, Settings state, and feature content remain unchanged. Reduced-motion or unavailable View Transition API navigates instantly.

## Verification
- GitHub Actions source patch refused non-matching starting checksum and verified generated target hash.
- Existing browser route regression suite passed in hosted CI.
- Browser pseudo-opacity tests passed in hosted CI at 75ms and 225ms, desktop and narrow sizes, plus reduced-motion checks; Settings round trip and JS errors checked.
- Local extended route and fade checks: 150 passing, zero failures (1440x900, 620x750, reduced motion).
- GitHub workflow staged a new immutable checkpoint, pushed it and confirmed remote branch SHA.
- HTML is delivered for user evaluation; **not yet visually accepted by the user**.
