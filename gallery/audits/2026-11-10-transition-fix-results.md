# Gallery — page transition fixes, 2026-11-10

Status: **implemented for user testing** (not yet visually approved).

Baseline: exact, SHA-256-verified GitHub checkpoint `2026-11-10-settings-transition-fix`, checksum `4480f964efe6e6117daeb1edd29447e1689772b7d64ab17364755dd807df5118`.

## Fixed

- Secondary page navigation (main tabs ↔ Anime, Discover ↔ Watch History, Anime ↔ Player) uses coordinated, interruptible workspace transitions, leaving the shared Gallery header static. Existing main-tab slide animation is unchanged.
- Re-entering the same Anime page after Back now transitions consistently; routine in-place rerenders do not trigger a new page transition.
- Watch History → Settings → Back returns to History, with the current filter, expanded season and scroll retained rather than resetting to Discover.
- Watch History → Anime → Back returns to Watch History, preserving the History state and correcting the destination button label.
- Nested Settings → About and About subpage → parent have subtle reversible entrance motions.
- Reduced-motion support clears stale animation classes, including when macOS motion preferences are switched live. Older browsers without the View Transitions API get a simple local fallback entrance animation instead of a hard snap.

## Tests

- 55 route and interaction assertions across Chromium desktop (1440×900), narrow (620×750), and reduced-motion modes: **pass**.
- Player routing (Anime → Player → Anime), rapid History → Settings, and JavaScript error checks at desktop and narrow widths: **pass**.
- No image generation or UI redesign in this change. Native macOS integration remains out of scope.

The complete resulting HTML source is stored as a new, immutable, checksum-verified checkpoint. Previous checkpoints are unchanged. Run `gallery/tests/test_transitions.py` for a repeatable route check alongside GitHub Actions checkpoint integrity.