# Gallery maintenance guide — A3.3, A6 and A7
**Reference baseline:** `4e7f4eeeed62114b844bf65b057a95bd707f24ba`; application `040572b2a440e7afafdc7b07191cebd620d444c0`, checkpoint `2026-11-19-a3-dialog-completion`. Baseline verification: 44501601979 and 44501601954 passed (2026-11-19 11:37 CET); immutable full 6,943,973 bytes SHA-256 421e0301f43bb1d56b6be913e58b3e8ee5464576ab3edf951f20e0689cd446df; lightweight 628,283 bytes SHA-256 faabf8cf2bca16c12b172e3a99d5661cdc4aecac036ab15273b6c72b2d8cccc7. This reference records existing approved architecture, behavior and maintenance rules; it does not redesign or change application code. Read [approved decisions](APPROVED-DECISIONS.md) chronologically (later scoped decisions supersede earlier ones), [current state](DEVELOPMENT-STATE.md) and [workflow](WORKFLOW.md) before each change. Source and actual current checkpoint remain authoritative.

## A6 — Architecture and maintenance

### Source, build, and recovery boundaries

| Location | Responsibility / rule |
|---|---|
| [src/Gallery.template.html](src/Gallery.template.html) | Persistent app shell: brand/toolbar, main tabs, three tab-page containers, secondary screen, Settings and scroll-overlay host; modal host outside inert app. Single inline style and classic script tokens. |
| [src/build-manifest.json](src/build-manifest.json) | Sole ordered list of 28 CSS and 53 JS fragments. Concatenate exact bytes; no glob, sort, runtime module loader, minification, or bundler. |
| [src/styles/README.md](src/styles/README.md), [src/js/README.md](src/js/README.md) | Original M2/M5 source maps; file responsibilities remain useful, historical byte/line counts are not present-day offsets. |
| `src/styles/` | Base/page headers and shared controls, feature rules, typography, late theme and responsive refinements. Later rules can intentionally override earlier ones. Preserve order and specificity. |
| `src/js/` | Classic shared lexical scope; source fragments are not isolated runtime modules. Hoisting, top-level initialization, and declaration order matter. |
| `assets/subtitle-preview/` | Original shrine-day/night PNGs. Full/subtitle-preview embed exact original bytes; development substitutes solid colors (#d5dbe2, #091b2c) and exact builder-owned image assignment patches, not new art. |
| `tools/build-gallery.py` | Standard-library deterministic builder; preview defaults to `dist/`; `--check` verifies all modes without writing; approved `--write-deliverables` writes only generated HTML after old canonical integrity check. |
| `Gallery-current.html`, `Gallery-development.html` | Generated full/lightweight deliverables. Never edit directly. Full and subtitle-preview output identical. |
| `checkpoints/current.json`, immutable archive | Byte count/hash plus named reconstructible full checkpoint; older checkpoints never overwritten. `restore-checkpoint.py --verify-only` verifies archive independently; `stage-checkpoint.py` creates only new archive after approved change. |
| `changes/pending/`, `audits/`, `tests/` | Guarded one-use publisher requests, historical evidence and mandatory regression entry points. Never rerun old requests or delete old failures. |

The standalone prototype uses a restrictive CSP (inline local styles/scripts, data images, file/blob media, no network connections). No production network/provider, embedded native player, or backend integration is proved by HTML tests. Native preview README describes an older separate Apple Silicon branch; never treat it as the development source. A4 persistence abstraction and A5 broader feature architecture stay deferred pending upstream StrawVerse assessment.

### Navigation and source map

All JS paths below are relative to `src/js/`. CSS prefix references refer to the exact manifest.

| Area | Entry/owner and related files | Contract |
|---|---|---|
| Initialization/shared utilities | 01 startup; 02 icons/escaping; 04a–c preferences/state; 04d–j route/tab DOM, scroll, rendering and motion; 05 cards/headers; 08 timeline; 18 color conversion; 19h bootstrap | Keep shared shell stationary, initialize dependencies before bootstrap; use existing escaping and shared controls. |
| Primary pages | 07b Discover, 07c Library, 07d/09 Downloads, 04g–j tab lifecycle | Three persistent tab containers with scroll state; in-place updates are not route transitions. Retire secondary resources before actual departure. |
| Secondary routes | 11i render, 11k entry points, 04d transition functions | Details/History share screen; Player owns its own mounted session; Settings is a separate retained panel, can suspend underlying screen. Preserve route provenance, not merely last tab. |
| Anime Details | 10 release metadata, 11a detail/rail, 11c dialogs, 11k navigation | Native horizontal rail; observer and scroll ownership, selected release visibility, exact contextual Search return, deliberate Settings suspension. |
| History | 06 fixtures, 07a History and legacy preview, CSS 17/28 | Default global History shortcut, no normal Discover Recently Watched banner; legacy fixture only explicit opt-in. Preserve filters, expansion, return scroll, independent watched status and actual playback tracking. |
| Player | 11b page/return, 11d desktop bridge, 11e subtitles, 11f motion, 11g playback, 11h controls | Session/video identity, media/track listeners, bridge async guards, pause/unload, object URL ownership, timers and morph teardown. Preserve local/demo semantics; native integration separately tested. |
| Settings/dialogs | 11j modal lifecycle, 11l navigation state, 12/13 subtitle prefs, 17b–e About/subtitle preview/popover state, 19a–e color, bindings, markup, search, navigation | Modal focus/inert and replacement ownership; Settings own focus, scroll, search reveal and observer cleanup. Popover live preview/commit/cancel distinct from page departure. |
| Sources | 14–16 providers/fixtures/initialization, 17a sources, CSS 11 | Simulated update operation survives valid UI navigation; reset or catalogue replacement cancels pending phase. No actual transfers claimed. |
| Contextual Search | 19f, CSS 09/20 | Search contexts primary pages/History, not Player; Settings uses own search. Preserve precise saved positions, user scroll priority and detail origin. |
| Library dialogs | 19g, 11j | Use shared modal lifecycle for tag/collection operations. |

### Resource ownership contracts (A2 retained)

Before introducing any listener, timer, RAF, animation, observer, promise callback, media or URL, identify its owner, start, replacement/departure, cancellation/settlement and stale callback guard. Do not infer leaks merely from finite callbacks or detached-node listeners. Retire at actual destruction or departure, not at deliberate suspension. Verify a positive uninterrupted operation as well as canceled/stale cases.

| Owner | Cleanup and positive behavior | Regression evidence |
|---|---|---|
| Player session | `sfPlayerTeardown` before replacing DOM; abort owned events, cancel timers/RAF, pause/unload old media, revoke URLs, guard old async bridge results and history attribution. | A2.1 nested Player/Settings suite; local/demo and stubbed bridge, not native picker. |
| Details rail | `retireInstallmentRail` at actual render/departure; owned observer/listeners/native scroll; no stale observation or snap after replacement; Settings retains rail. | A2.2 rail and Search return; real selected-release reveal. |
| History row/page | Owned expansion completion; destroy row scrollers/observers on departure; visibility-aware progress loop and explicit legacy preview cleanup. | A2.3, History row maintenance and repeated normal/reduced toggles. |
| Modal overlay | Retire keyboard scroll/reveal and expanded preview observation on close/replacement. `cancelModalExit` aborts old listener/timer; only current overlay can restore app input/focus; preserve original opener. | A2.4, A3.1, A3.2. |
| Settings instance | Cancel jump/scroll/reveal/highlight and observer at close; preserve active section and underlying route as intended. Close color popover with its own cleanup. | A2.4 precise callback attribution, A3.1 scroll. |
| Download/source operation | No obsolete completion timer at 100%; source phase timer/generation tied to valid operation, reset/catalogue replacement cancels; valid update can finish outside Settings. | A2.5 background operation ownership. |

### Practical maintenance checklist

1. Recover remote active branch and current immutable pointer; read mandatory docs. Confirm exact HEAD's integrity and browser runs, reconstruct archive and source; stop on disagreement.
2. Locate the responsible file using this map and the manifest, then inspect actual callers, cascade and state. Do not rely on historical line numbers. Keep unrelated changes separate; approved scope first, record pending work.
3. For UI edits prefer shared base/component rule; classify overrides (theme, responsive, state, accessibility, deliberate feature, legacy corrective). Only remove after actual equivalence or separately approved design change. Test effective geometry/styles, not declaration counts alone.
4. For runtime edits use owner-local cleanup, trusted-input tests and exact rendered/settled state, including interruption and reduced-motion preference changes. Avoid global timer hacks and fixed sleeps as sole proof of completion.
5. Build only through source-first tools. Full/light candidate tests must pass, then publish exact tested tree + new immutable checkpoint atomically; both independent read-only checks must pass. No new numbered release without discussion, no art edits without explicit permission.
6. Record exact build commit, hashes, actual results and user-testing status in DEVELOPMENT-STATE. Deliver commit-pinned HTML and separate commit link. An independent pass is not visual acceptance/native integration.
7. If error or interruption, inspect remote HEAD/pointer/request/Actions before retry. Never duplicate publication or silently relax tests. Historical tests and archived checkpoints remain immutable.

### Verification map

Independent integrity: `gallery-checkpoint-integrity.yml` (Ubuntu 26.04, 10 min): archive/canonical/hash, reconstruction smoke, checkpoint roundtrip, exact source/mode assembly and publisher matrix. Independent browser: `gallery-transition-ui.yml` (Ubuntu 24.04, 45 min, pinned Playwright 1.57.0 Chromium): full and lightweight route/coordination/History/Player-Settings jobs and cross-build subtitle asset/geometry job. Controlled publisher: exact candidate preparation, artifact digest/tree guard, same mandatory regressions + any approved comparison shards, publication and then exact-build independent checks. Preserve all suites:
- `test_transitions.py`, `test_coordinated_fades.py`, `test_history_row_maintenance.py`, `test_player_settings_regression.py`, `test_asset_build_modes.py`; nested mandatory A1/A2/A3, Search, release reveal, geometry and ownership gates remain active.
- A3.1 72 contexts/build, A3.2 48/build including four deliberate fallback contexts/build; independently verified on current application. Diagnostics are separate evidence, not replacements for gates. Historical exact comparison and audit files are retained.
- Test real routes/DOM, both builds, six themes and relevant viewport widths, normal/reduced motion and live preference changes as applicable. Keep pinned test origin for persistence. Visual checks at actual scale and native macOS integration remain distinct from Chromium assertions.
- The approved one-package retry supervisor may only rerun eligible failed jobs on the same documentation commit; no modified files, waived tests or new checkpoint. Both original checks retain their names, permissions and contents.

## A3.3 — Animation timing and ownership

Current reference updates the historical [A3 audit](audits/2026-11-18-a3-motion-audit.md) for the A3.1/A3.2 corrections. Listed values are declared/known active paths, not a complete computed cascade matrix. Do not unify durations just because values match. Functional playback time, operation phase timers, hover intent and safety deadlines are not decorative motion.

| Motion | Current normal timing / source | Ownership and reduced-motion contract |
|---|---|---|
| Main tabs | WAAPI track 160–520 ms, 310 ms for one page; cubic-bezier(.32,.08,.22,1), 04i | Freeze rendered transform before retarget. Live reduce snaps to latest destination; no replay. |
| Secondary route | 150 ms outgoing ease-in then 150 ms incoming ease-out; 04d | Workspace/tabs/divider coordinated; no layout mutation until invisible midpoint; input gate and latest pending route; reduce finishes current phase, mutates exactly once, skips incoming as needed and releases gate. |
| Details ↔ Player | Native View Transition snapshot 150+150 ms, CSS 04 / JS 04d | Exclusive existing Player path; no overlapping ghosting/depth. Reduced/no API direct switch; keep native behavior separate. |
| Surface/About | CSS 240 ms surface, 220 ms directional About, CSS 04 | Only actual entry/change, not routine render. Clear entrance class at completion/preference change. |
| Discover Search | Flyout width/padding 320 ms, opacity 200 ms; grid/margin and scroll 420 ms cubic-bezier(.22,.72,.2,1); CSS 09/20, JS 19f | Native grid clock with 420 ms fallback; saved position/reversal and manual input priority; live reduce settles, no replay. Default Discover no legacy banner. |
| Selected pills | Stationary selection fade 260 ms; CSS 18/25 | Shared main tabs, Sub/Dub, Day/Night treatment; state/hover distinct; reduced rules include pseudo-elements. |
| Details rail/releases | Native smooth scroll, instant reduced; 230 ms release fade, 420 ms episode visibility; JS 11a, CSS 07 | Minimum selected-card reveal; active rail owner/scrollend, manual input wins, live reduce clamps to target. Preserve native snap and exact Search-return exception. |
| Downloads | 280 ms grid, chevron base 260/themed 240, progress basis 280; CSS 08/21 | Separate simulation from visual feedback; reduced CSS; no obsolete completion timeout. |
| History expansion/progress | 280 ms grid/chevron/delayed visibility; 280 ms ease progress; partial capsule 1100 ms/13px, Completed 150 ms; CSS 17, JS 07a | One owned completion per row, no stale callback under reversal/reduce. Visible/intersection-aware progress; instant static under reduce. |
| Legacy Recently Watched | Open 550, close 375, transfer 300, pane fade 140, hover intent 100 ms; CSS 17, JS 07a | Explicit legacy-only controller; reset on preference/input capability change and departure. Not default Discover. |
| Player controls | Play/Pause 260, Forward/Next 280 ms scaled by remaining amount, cubic ease-in-out; Up Next 280, overlay show 300/hide 620, volume fade 150; JS 11f / CSS 03/16/26 | Reversible geometry/optical morph, stable labels and centers, owned player RAF; live reduce settles intended endpoint immediately. Autoplay uses media clock, never decorative timer. |
| Dialog entrance | Backdrop 180 ease-out, dialog 220 cubic-bezier(.2,.8,.2,1); CSS 04, JS 11j | Sample actual rendered opacity/transform before interrupted close; settled entrances keep default exit keyframes. |
| Dialog exit | Both 140 ms ease-in forwards; dialog to 0 opacity, translateY(4px), scale(.995); CSS 04/JS 11j | Both trusted target/name-specific animationend events required for normal removal. Owner guard + AbortController; 300 ms safety fallback settles remaining animations and removes only current owner. Cancel on replacement/reduce. Reduced-at-start immediate; live reduce CSS suppresses flash before handler then releases inert/focus in same task. **Former fixed 150 ms cleanup is retired.** |
| Keyboard scroll | Dialog 220–410, Settings 190–380 ms ease-out cubic; JS 11j/19e; Settings panel entrance 190 ms CSS 10 | Owned target/generation, focus immediate, scroll smooth; live reduce settles intended scroll, close cancels obsolete work. |
| Scroll overlay/Sources | Overlay opacity 400, hide delay 950; Sources visual progress 340 ms; JS 04f, CSS 06/11 | Keep display feedback distinct from operation lifetime/phase clock. |

A3.1 tests actual in-flight normal→reduce, pre-enabled reduce, reversal, no replay, exact destination and ownership. A3.2 tests interrupted starts, real exit events/endpoint, live preference, replacement/reopen and suppressed-event fallback. Do not use last RAF alone as proof of final frame: exact endpoint investigation found old fixed timer removed all 144 sampled dialogs before formal completion. Do not use a global animation framework or wholesale native scrolling replacement. If future timing consolidation is proposed, demonstrate equivalent semantic contract, rendered geometry and tests first. Tab WAAPI compatibility outside pinned browser remains an observation, not a proven native defect.

## A7 — Design standards and deliberate exceptions

These summarize existing approvals, not additional redesign permission. For new work consult APPROVED-DECISIONS for precise scope and most recent superseding decision.

| Standard | Approved baseline and checks |
|---|---|
| Theme and surfaces | Soft Futuristic: ocean, twilight, ember, slate, glacier, verdant; existing semantic palette tokens (accent/panel/panel2/hover and related foundation). Shared stationary background and consistent shell. Theme override only if necessary; no retired palette revival or image edits. |
| Shared geometry | Primary and secondary headers share width/gutters, divider and band alignment; titles optical, Back/actions independently mathematical. Prefer even structural dimensions where practical, not forced even glyph dimensions. DS01 Downloads/History full available width and alignment, including headers. |
| Back buttons (DS02b) | Shared theme-aware pill: accent icon/text; rest 20% accent/panel fill, 72% accent/panel2 border; hover 24% fill, 82% border. Preserve geometry/focus/route. Existing tests enforce >=4.5:1 text, >=3:1 border against representative panel2. Supersedes older DS02 percentages. |
| Compact Player exception | 46 px title/Back band, equal 3 px gaps above/below, no page divider or vertical padding; existing title-only 1 px optical adjustment, Back mathematically centered. Preserve video budget/gutters and all other headers. |
| Global toolbar | Search, History, Settings 40 px circular containers, gap 8 px, center separation 48 px; glyphs unchanged (Search 21, History existing 21, Settings 23). Search expands left; other controls stationary. History disabled on Player/Settings by design. Main tabs only Discover/Library/Downloads. |
| Icon rule | Mathematically aligned containers, hit areas, centerlines, focus rings; optically centered glyphs, shape/weight/perceived size and stroke balance. Prefer shared glyph fix over per-page offsets, preserve throughout morphs/reversals/reduced motion. Assess actual-size visual balance across themes/states/widths. No automatic redesign. |
| Typography | System (macOS), Atkinson Hyperlegible Next, Inter. Application Typography and subtitle font choices remain distinct. Preserve current preferences/fallback and optical alignment; no arbitrary uniform font sizes. |
| Segmented controls | Stationary selected gradient, distinct inactive hover; Sub/Dub and Day/Night share treatment, no movement of surrounding geometry. Day/Night two directly selectable options, no action clicking active option; instant scene change, synchronized main/expanded. |
| Subtitle preview | Preserve original day/night artwork, 16:9, exact 1280×720 actual-size mode with scroll, Fit mode; hide 100% when Fit already actual size, safely retain focus. Expanded 12 px inner padding, one header (title, actual size/Fit, Day/Night, close), narrow wrap. Soft White #F8F8F8; Low/Medium/High intensity; current stored IDs and custom-color saved swatch behavior. No auto scene cycling. |
| Player controls | Volume left, Back10/Play-Pause/Forward10 center, Settings/Fullscreen right. Stable center when Next appears; scale down never up; tiny player Play/Pause only. Forward ↔ Next true reversible morph, not simple crossfade. Timeline two contrasting rounded segments/5 px gap, no ball. Subtitle selection/speed in Player Settings; audio choice before Player. |
| Episode navigation | Fixed/equal Prev/Next slots, reserve invisible slots; center Episode X / Season Y stays stationary. Same-season autoplay final 20 seconds tied to playback, pause/seek/speed; no automatic cross-season/movie jump. Preserve labels and explicit manual boundary navigation. |
| History and Downloads | Shared full-row expandable summary, cover/title navigate separately, action buttons independent. History episode button cycles Not watched → Partially watched → Watched, false/mixed/true ARIA; manual status separate from actual timestamps. History Option A solid watched + moving partial capsules (8×5 px with 5 px spacing, 1 px transparent overlap cutout, stationary endpoint, 280 ms reversible progress); Downloads ordinary progress separate. |
| Release rail | Reveal selected obscured card only as far as needed taking arrows into account; no unnecessary centering/vertical shift. Preserve arrows, guards, native horizontal scroll, selection and return position. |
| Focus/accessibility | Keyboard focus visible; pointer focus treatment as existing, controls remain keyboard-operable and labeled, inert/aria-busy released correctly. Do not remove reduced-motion support or disable functional media behavior. |
| Navigation provenance | Shared header stationary, sequential fades, Details↔Player special snapshot, correct originating page/back/detail/History/Settings scroll. No default Recently Watched empty region; legacy fixture isolated. |

### Override review and future design changes

An override is justified for responsive constraints, theme, interaction/state, accessibility or an approved feature-specific exception. Record selector/property, earlier/later source locations, actual rendered reason, approved decision and test cases. Corrective overrides without a reason are **review candidates**, not permission to delete. See `tools/audit-design-system.py` and historical Q2 review files; exact duplicate declaration or unobserved CSS is not proof of redundancy. Use shared component semantics and effective computed-style/geometry comparisons before moving/removing declarations. For intentionally changed design, separately discuss expected appearance, interactions and exceptions, then test and obtain user review.

**Open proposals, not approved changes:** broader icon optical/motion refinement, Search-bar motion polish, backdrop dithering trial, persistence abstraction, feature architecture and upstream/native integration. Maintenance completion does not authorize implementation. A1/A2/A3 runtime work is verified; remaining user visual reviews and native macOS tests are independent obligations.
