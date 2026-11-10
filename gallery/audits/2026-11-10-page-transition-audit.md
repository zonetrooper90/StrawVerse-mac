# Gallery page-transition audit — 2026-11-10

**Scope:** complete standalone Gallery HTML prototype, *not* proof of the native macOS runtime. **Audit only:** no HTML modifications or change to the current checkpoint pointer.

## Authoritative baseline

- Repository: `zonetrooper90/StrawVerse-mac`
- Branch: `gallery/working-2026-11-10`
- Checkpoint: `gallery/checkpoints/2026-11-10-settings-transition-fix/` (current pointer)
- Source: `Gallery-Soft-Futuristic-Settings-Transition-Fix.html`
- SHA-256: `4480f964efe6e6117daeb1edd29447e1689772b7d64ab17364755dd807df5118` (6,937,266 bytes)
- Preflight: remote AGENTS.md, WORKFLOW.md, pointer and approved decisions read; 27-part archive reconstructed with the repository restore tool. All part, compressed and output checksums passed. Previously committed GitHub integrity job passed.

## Test method

Chromium with Playwright, real UI button clicks and DOM/WAAPI animation sampling shortly after navigation. Tested desktop **1440×900**, narrow **620×750**, and **prefers-reduced-motion: reduce**. Verified primary-tab interruption with a rapid Discover→Downloads→Library redirect. The first 30 desktop route checks completed without JavaScript errors, along with targeted narrow and reduced-motion checks. This tests the standalone prototype's reachable navigation and CSS/WAAPI behavior; it does not replace manual visual testing on macOS/Electron.

## Route-by-route results

| From → to | Animation? | Evidence / concern |
| --- | --- | --- |
| Discover ⇄ Library, Library ⇄ Downloads, Discover ⇄ Downloads (all six directions) | **Yes** | Persistent-page track WAAPI slide, 310 ms adjacent / ~497 ms across two tabs; rapid redirect resolves correctly. |
| Discover, Library, Downloads → Settings | **Yes** | Settings page 280 ms entrance; primary surface is immediately hidden but Settings does not start transparent in the current fix. |
| Settings → Discover, Library, Downloads | **Yes** | 140 ms exit followed by 140 ms Gallery return animation. |
| Discover → Anime detail (first visit) | **Yes** | `gallery-surface-in` 240 ms; fade-in starts at opacity zero with no coordinated outgoing-page animation. |
| Library → Anime detail | **Inconsistent** | Same 240 ms entrance only when `#screen.dataset.surfaceKey` differs. Reopening the same anime after returning to a main tab can hard-cut (reproduced). |
| Anime detail → Discover / Library | **No** | `showTabPages()` snaps track and hides `#screen` immediately. Both directions reproduced. |
| Anime detail → Player | **Yes** | 240 ms `gallery-surface-in` (fade-in only). |
| Player → Anime detail | **Yes** | 240 ms `gallery-surface-in`. |
| Anime / Player → Settings → same page | **Yes** | Settings entrance/exit and `gallery-return`; previous double-fade fix present. |
| Discover → Watch History | **No page transition** | `whEnter()` swaps tab viewport for `#screen` immediately. Individual history cards can animate, but the *page change* does not. |
| Watch History → Discover | **No** | `whExit()` restores tabs immediately without page exit animation. |
| Watch History → linked Anime detail | **Yes** | Anime `gallery-surface-in`; still fades from zero without outgoing surface animation. |
| Linked Anime detail → Watch History (Back) | **Incorrect destination** | Returns to the underlying Library/Discover tab instead of the Watch History page that opened the anime (reproduced). |
| Watch History → Settings | **Settings animates, History discarded** | `showSettings()` calls `whExit()` before showing Settings; Watch History is destroyed and underlying tab substituted. |
| Settings → Watch History (Back) | **Incorrect destination** | Returns to Discover, not Watch History (reproduced). |
| Settings main sections (Appearance, Playback, Downloads, Sources, About) | **Yes** | `.settings-panel:not([hidden])` has a 190 ms entrance; outgoing section swaps instantly. |
| Settings → nested About / legal / credits page | **No** | `setAboutView()` toggles `hidden` instantly. |
| Nested About page → About parent | **No content transition** | Content switches instantly; the Back button may animate its hover/focus feedback only. |

## Reduced-motion and interruption

- **Pass:** Main tab tracks snap under reduced motion; Settings/page entry animations disabled as intended.
- **Bug:** The `#screen.surface-enter` class persists under `prefers-reduced-motion: reduce` because its cleanup relies on `animationend`. Switching preference back to normal while an Anime page is open *restarts the animation* and temporarily resets the content's opacity to 0. Reproduced in Chromium.
- **Pass:** Rapid redirection of an in-progress main-tab animation keeps one active WAAPI trajectory and reaches the requested target (no extra hard snap observed).

## Proposed correction order (not implemented)

1. Introduce coordinated, interruptible secondary-page enter/exit transitions for both main-tab↔Anime and Discover↔Watch History, reusing the existing subdued Gallery motion language. Avoid a fully blank workspace, retain static shared header/background, maintain scroll/keyboard focus and navigation visibility.
2. Reset/advance `surfaceKey` when exiting a secondary page so re-entering the *same* anime reliably animates; do not animate ordinary in-page rerenders and player-state updates.
3. Preserve secondary-page provenance: Settings opened from Watch History returns to History; Anime opened from History returns to History. Do not lose its list/filter/expanded-row/scroll state if possible.
4. Add a modest, reversible transition for nested Settings About screens. Decide whether outgoing Settings section content also needs a coordinated exit, rather than piling on independent fades.
5. Eliminate stale `surface-enter` classes under reduced motion, including on live preference changes; verify transitions at 1440, 620 and motion-preference switching.
6. Add a repeatable route-matrix automated test and require it alongside GitHub checkpoint integrity on Gallery changes. Check static shared-header geometry and the separate main-tab slide behavior.

**No source files were modified during this audit.** The immutable current HTML checkpoint remains the source of truth. Changes require normal Gallery review, GitHub commit/checkpoint and successful integrity verification before handing out a new HTML build.
