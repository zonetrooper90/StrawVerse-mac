# Gallery — coordinated fade and route repair (2026-11-10)

## Approved scope and preserved reference
User rejected the visible overlap and navigation jumps of the prior Gallery fade. **Anime Details ↔ Player was identified as satisfactory and preserved unchanged.** The user authorized synchronizing remaining page, navigation and Settings fades, and fixing the Recently Watched → Anime → Back provenance.

## Changes
- On all non-Player secondary/Settings routes: fade outgoing live workspace, main navigation if present, and bottom header divider over 150ms.
- Mutate the actual DOM, page and navigation classes only after the outgoing opacity reaches 0, and fade the destination in over 150ms. Never show two page layouts together.
- Brand and toolbar remain at fixed positions; the secondary-page navigation remains absent at rest. Main Discover/Library/Downloads horizontal slides remain as approved.
- In reduced-motion environments or without the Web Animations API, navigate instantly.
- During the fade, guard interactions and clean up inline opacity/animation state when complete.
- Discover's Recently Watched cards open matched anime details directly and return to Discover, not Watch History. Only actual Watch History links return there. Retain installment/season context where present.

## Source of truth and integrity
- Dedicated development branch: `gallery/working-2026-11-10-coordinated-fades`
- Last baseline checkpoint SHA-256: `5b81d793f474fcf94bc1cd719f8a848cad66e63129b937fbd20450aa5c2d094f`
- New immutable checkpoint: `gallery/checkpoints/2026-11-10-coordinated-fade-route-fixes/`
- Full HTML: `gallery/deliverables/Gallery-Soft-Futuristic-Coordinated-Fades.html`
- Reconstructed HTML SHA-256: `1d83bea4249345198d91730524fda609edb1d9734196bd274225a6a5f67c9a4c`
- File length: 6,946,304 bytes
- HTML application source modifications originate from `gallery/tools/integrate-coordinated-fades.py`, which rejects nonmatching baseline SHA.
- Previously delivered checkpoints remain immutable; no native Gallery/macOS source branch was modified.

## Browser checks
- Full pre-existing transition/navigation suite: **55 checks passed** in hosted GitHub Actions, including secondary routes, About subpages, reduced motion and History restoration.
- New phase/visual layout and provenance suite: **319 checks passed**, including desktop 1440×900, narrow 620×750 and reduced motion.
- Verified outgoing DOM persists while fading, nav and workspace both fully transparent during DOM/class mutations, header brand coordinates unchanged, incoming destination correct, and restored Season/History state.
- Working Anime ↔ Player snapshot implementation retains its own path and is tested in both directions.
- Full downloadable HTML tested against the same SHA as the GitHub checkpoint, verified by the staging/restore scripts and CI.
- GitHub build workflow: https://github.com/zonetrooper90/StrawVerse-mac/actions/runs/42906527117

**Review status:** delivered for user testing; the user has not yet confirmed the visual result. Do not mark approved.
