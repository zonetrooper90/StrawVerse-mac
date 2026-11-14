# Gallery — Approved Decisions

Last updated: 2026-11-04. This document records settled decisions; experiments and open questions are not automatically approved.

## Core product
- macOS native app, Apple Silicon-only builds; fork/alternative client compatible with StrawVerse repositories and sources.
- Main tabs: Discover / Library / Downloads. Opening Settings hides/disables normal navigation.
- English-language app UI. Fonts available in subtitle styling: System (macOS), Atkinson Hyperlegible Next, Inter.
- Gallery itself collects no user data; do not promise external sources collect none.
- No image generation/editing without explicit user permission; prefer direct HTML/CSS implementation.
- Discuss and obtain explicit consent before creating any new numbered version. Preserve the latest stable/previous version.

## Settings and subtitles
- Full-page Settings UI.
- Subtitle appearance: preview scene with synchronized day/night views; preserve the approved original artwork and preview dimensions; sticky preview plus expanded view.
- Preview text: “The quick brown fox jumps over the lazy dog.”
- Subtitle controls include font, size presets XS / S / Normal / L / XL, colors including soft white default #F8F8F8, styles and effect intensity. Subtitle position selector removed.
- User selects audio language before entering the player. Audio switching is **not** in the player.
- Subtitle track/language selection and Off are in **Player Settings**, not a separate control-bar button. Appearance customization stays in main Gallery Settings. Keep the previously selected language available when toggled off.
- Playback speed is in Player Settings.

## Player control layout
- Left: Volume. Center: Back 10s / Play-Pause / Forward 10s. Right: Settings / Fullscreen.
- Player controls do not jump or change center alignment when Play Next appears.
- Player UI scales **down** with shrinking video viewport; **never scales up** above 100%, even in fullscreen. For extremely tiny players show only Play/Pause. Timeline remains width-responsive.
- Use Tabler Player Track Previous and Player Track Next for 10-second controls; use Tabler Player Skip Forward for Play Next.
- Forward 10s icon morphs continuously/reversibly into Player Skip Forward, including interruption mid-transition; do not use simple cross-fade instead of actual morph.
- Seek bar visually matches Downloads: two rounded contrasting progress segments separated by a small gap (5px in HTML prototype), **no circular ball handle**. Seeking still works.

## Play Next and Autoplay
- When Autoplay **enabled**, entering final 20 seconds of video automatically reveals controls and Play Next area with upcoming episode title/countdown and Cancel.
- Play Next information fades and slides **from the right**, not up from below; reverse motion on hide. Keep other controls stationary. It is integrated into the bottom controls area, not a separate subtitle-obstructing overlay.
- Forward 10s morphs into Next Episode for immediate manual skip when countdown is visible.
- Countdown follows remaining video playback: freezes on pause, responds to seeking and speed changes, no independent wall-clock race.
- Cancelling stops automatic advancement for that episode, restores normal controls and auto-hide; reversing back across 20-second boundary reverses animation smoothly.
- When Autoplay **disabled**, nothing special happens in final 20s: no control reveal, countdown, Play Next or automatic transition.
- Native next-episode source loading still requires integration; HTML demonstration is not proof of real media integration.

## Resume and history (planned)
- For shows in history, Play offers Resume or Start Over; Resume seeks approximately 7 seconds earlier than recorded and uses whole-second positioning.
- Existing Continue Watching in Discover will become a bounded Recently Watched strip of portrait anime covers, ordered by actual recent playback, each show once, newest on left. No scrolling or pagination; show as many as fit.
- A View History shortcut at the end opens full Watch History; full History layout remains to be designed.
- Watch History follows player work; do not silently merge it into prior versions.

## Archived milestones
- Gallery v96 A28: latest approved subtitle-layout experiment that fed v97.
- v97: subtitle/settings integration into consolidated HTML.
- v98: Tabler skip controls plus reversible icon morph.
- v99: subtitle selection moved into Player Settings, Play Next horizontal entrance, two-tone handle-free timeline.
- The HTML builds are development artifacts, not proof that native macOS playback features are complete.

See `gallery/PROJECT-CONTINUITY.md` for backup/approval workflow and `gallery/archive/README.md` for file hashes and paths.

## 2026-11-10 — current prototype decisions and delivery state

The historical v99 notes above are not the current design. **Source of truth:** the SHA-256-verified checkpoint named by \`gallery/checkpoints/current.json\`; each new checkpoint is **delivered for user testing unless explicitly user-approved**, and an HTML prototype is not proof of native Gallery runtime integration.

- Soft Futuristic design direction with six retained color themes; keep themes and pre-approved layout/style consistent unless user authorizes changes.
- The shared top Gallery header uses the same width and spacing on primary/secondary pages. Main navigation tabs are visible only on Discover, Library and Downloads. Hide tabs on Anime details, Watch History, Player and Settings while keeping the Gallery brand/header. Back buttons return to the correct prior destination.
- **Page headers:** Copy the structural header band, spacing and divider geometry from Library/Downloads. Titles are **optically** centered; Back/action buttons stay **mathematically** centered independently. Do not make per-page conflicting offset guesses.
- **Watch History:** full-width layout (same available content width as Settings), stable episode lists, expandable rows and filters. Title-left, Back-to-Discover-right header using the shared geometry.
- **Player:** anime title + Back to episodes in its simplified header. Do not repeat season/episode number or audio-language metadata there. Under player show **Episode X** then **Season Y**, not Episode X of Y.
- **Previous and Next episode navigation:** context-aware labels, equal/fixed button dimensions with reserved invisible slots so the center Episode/Season label never shifts. Crossing into an identified next/previous season is explicit manual navigation to that season's first/final episode. Movies/specials only if explicitly ordered; never guess.
- **Autoplay:** the 20-second Play Next countdown continues only within the same season. It never starts the next season or a movie automatically; at the season finale the Play Next countdown is suppressed even when more content exists.
- **Player control polish:** Rewind/Play-Pause/Forward symmetrical and optically balanced; preserve the continuous icon morph and keep the Play triangle free of the internal seam.
- The Settings transition adjustment addresses the blank-on-open and flash-on-return animation regressions, but is **awaiting user confirmation**. Do not mark as approved without that confirmation.
- **GitHub workflow:** all future changed builds must be verified, committed, and linked to their GitHub checkpoint before delivery; see \`gallery/WORKFLOW.md\`. Main/native branches stay untouched.

## 2026-11-10 — transition regression fixes, delivered for testing

The user explicitly authorized repair of all gaps found by the 2026-11-10 transition audit. The new HTML checkpoint implements secondary-page entrances/exits (without replacing the approved main-tab slide), consistent revisits to the same Anime page, correct return to Watch History from Settings/linked Anime, animated nested About pages, and motion-preference cleanup. Preserve navigation provenance, History filters/expanded rows/scroll, the existing header geometry, and reduced-motion behavior. These fixes are **delivered for user testing, not yet visually confirmed**. Refer to `gallery/audits/2026-11-10-transition-fix-results.md` and the automated `gallery/tests/test_transitions.py` route matrix before further changes.
## 2026-11-10 — A+C page motion selected and implemented for testing

The user chose **A+C (Crossfade + Micro Depth)** after comparing the standalone transition experiments and explicitly authorized integration into the full Gallery development HTML. The design choice is **approved**, while the integrated HTML checkpoint remains **delivered for user testing**, not yet user-visually approved.

- Secondary page routes (Anime details, Watch History and Player) and entry/return from Settings use the same overlapping 450 ms A+C crossfade. Opacity eases together while the old page scales 1 → .994 and the arriving page scales 1.008 → 1 (under one percent depth).
- The shared Gallery header and background remain stationary; the original Discover / Library / Downloads horizontal tab-slide behavior remains unchanged.
- Preserve Back navigation, Watch History filters and scroll position, Settings history/provenance and the existing shared header geometry. Reduced-motion preference disables the A+C capture.
- The new checkpoint is `gallery/checkpoints/2026-11-10-ac-crossfade-micro-depth/`, SHA-256 `0a31de142b1de4451de2709160860bae3aa66e33a8d2dce5a219d1e2e8355443`, based strictly on the previously verified Gallery full-app checkpoint. Automated browser tests have passed, but visual user acceptance is still outstanding. No native macOS build was changed.
- See `gallery/audits/2026-11-10-ac-micro-depth-results.md` and `gallery/tests/test_ac_motion.py`.

## 2026-11-10 — nonoverlapping sequential fade trial

After viewing the full-app A+C screen recording, the user rejected the 450ms overlapping crossfade because it ghosted complete pages. The user approved trying a simple, strictly sequential fade: outgoing workspace opacity 1 to 0 for 150ms, page change at full transparency, then incoming workspace 0 to 1 for 150ms (300ms total). No overlap, scaling, blur or automatic view-transition group resizing. Main tab slides, shared header and background, all Gallery layouts, route state and keyboard navigation must stay as before. Reduced motion and browser fallback switch instantly.

This replaces A+C as the current **trial**, not as a user-visually accepted release. Retain the old immutable A+C checkpoint for audit. New immutable HTML checkpoint is 2026-11-10-sequential-fade-no-overlap; user approval is still pending.

## 2026-11-10 — coordinated fade and Recently Watched navigation repair, for testing

The user demonstrated layout jumps and incorrect destinations in the sequential-fade trial, identified **Anime Details ↔ Player** as the *only* satisfactory transition, and explicitly approved the corrective implementation. Preserve the existing Anime ↔ Player snapshot transition untouched. All other secondary/Settings routes now use coordinated 150ms fade-out, a real DOM/header/nav/layout switch **only after opacity reaches zero**, then a 150ms fade-in. Fade the main tabs and header divider alongside page content, keeping Gallery branding stationary; do not disturb primary-tab horizontal sliding. Respect reduced-motion preference and preserve Watch History state.

In Discover's Recently Watched strip, anime covers open their linked detail pages **directly** and Back returns to Discover. Only links opened *from the full Watch History page* may return to Watch History; preserve season context where available. Unlinked sample cards use a local explanatory dialog rather than a false route.

This is a **development HTML delivered for user testing, not yet user-visually approved**. New immutable checkpoint: gallery/checkpoints/2026-11-10-coordinated-fade-route-fixes. Both the established route matrix and new DOM-midpoint/layout-state browser tests must pass. The preceding A+C and sequential-fade checkpoints remain immutable.

## 2026-11-10 — coordinated fades visually accepted

The user tested the latest **Coordinated Fades** full Gallery HTML and reported that the behavior looks better, with no remaining transition issues observed. They explicitly chose to **keep this implementation**. Treat the coordinated 150ms outgoing / 150ms incoming no-overlap secondary-page and Settings transitions, together with the preserved Anime Details ↔ Player transition and Discover/Library/Downloads primary slides, as the **current accepted HTML motion baseline**. Keep navigation provenance, stationary branding, synchronized nav/divider fades, Watch History state and reduced-motion support unchanged. Do not reopen or retune transition timing unless new issues arise or the user requests it.

This is user visual acceptance of the existing immutable checkpoint `2026-11-10-coordinated-fade-route-fixes` (SHA-256 `1d83bea4249345198d91730524fda609edb1d9734196bd274225a6a5f67c9a4c`), **not** a new numbered build or proof of native macOS implementation. The existing archive, checkpoint pointer and HTML bytes remain unchanged.

## 2026-11-10 — Library transfer UI hidden; Watch History row parity with Downloads

User approved hiding the unfinished collection Import and Share/Export UI while preserving all implementation code for later redesign. Library's New Tag action remains; no transfer affordances or obsolete transfer help text are shown. A single disabled feature flag can restore them.
User also approved applying Downloads' full-row interaction design to Watch History: tapping/clicking the season summary background expands/collapses episodes, while its cover and title still open anime details and Remove is independent. Each episode row is an accessible full-width button for toggling watched status, with no episode-list rebuild or scroll jump. Keyboard focus is accent-visible; hover uses existing theme colors. Preserve all six themes, coordinated navigation fades, playback, provenance, filtering, undo and reduced-motion support.
This unnumbered maintenance checkpoint is delivered for user visual testing, not native app integration.

## 2026-11-11 — Watch History animated expansion correction, for user testing

After testing the previous maintenance build, the user reported that Watch History expanded and collapsed instantly despite Downloads using a smooth transition. User approved correcting that mismatch without a numbered build. Watch History now uses Downloads' 280ms reversible grid-height animation and matching chevron transition; panels remain in the DOM, so clicking to expand/collapse does not rebuild the entire page or reset episode and scroll state. Closed panels are inert and inaccessible to keyboard navigation. Respect Reduce Motion (instant), preserve existing click targets, filtering, undo, all six themes, and approved navigation fades. This behavior is in checkpoint `2026-11-11-history-smooth-expand`, pending user visual review. No native app runtime was changed.

## 2026-11-11 — Watch History expansion visually approved

The user tested the complete Gallery HTML in a browser and explicitly approved the Watch History expand/collapse behavior. The first expansion initially appeared to stutter once, but later expansions were smooth; after reopening the file, the **first** expansion was smooth too. Treat the existing **280 ms reversible Downloads-style expansion and collapse**, chevron rotation, retained episode panels and Reduce Motion behavior as **approved and locked**. No further animation changes or speculative performance fixes are requested.

This approval applies to the existing immutable checkpoint `2026-11-11-history-smooth-expand` (SHA-256 `c850b767a00c1749d56d52468e23c01d31afd27edc225f74b3ec9440b1db1717`). The full HTML bytes are unchanged. This is visual approval of the prototype behavior, **not** a new HTML version or proof of native macOS integration.

## 2026-11-11 — Nested episode scrolling parity, implementation approved

The user reported that scrolling on an expanded episode list in Watch History stops moving the main page once the inner list reaches its end. They explicitly approved making Watch History and Downloads behave consistently. The approved correction allows **vertical scroll chaining at both the top and bottom** of each nested episode list, so further wheel/trackpad scrolling moves the enclosing Watch History or Downloads page. Preserve inner scrolling until the boundary, horizontal containment, card layouts, all six themes, the visually approved 280 ms Watch History expansion, and all navigation animation rules. This is an unnumbered maintenance change, awaiting visual user testing after its new GitHub checkpoint is published; approval of this change does not revoke the earlier Watch History animation approval.

## 2026-11-11 — Watch History wheel boundary handoff correction, awaiting visual review

The user tested the first scroll-chaining checkpoint and confirmed Downloads scrolls both ways, but Watch History continued scrolling upward and still trapped downward gestures at the episode-list end. This unnumbered correction installs a narrowly scoped Watch History-only wheel boundary fallback: native scrolling inside episodes remains unchanged, but any unconsumed vertical wheel/trackpad delta at either boundary is transferred to the parent workspace. The fallback handles a single movement crossing the boundary and preserves horizontal gestures. Downloads stays unchanged. Preserve the approved 280 ms expansion/collapse, card layout, six themes, keyboard interactions, and route animations. The user must visually test downward behavior before approving this correction; the prior expansion animation remains approved.

## 2026-11-11 — continuous scroll momentum refinement, approved for trial

The user confirmed the prior Watch History wheel handoff works but feels jerky and requires a pause (roughly until the episode scrollbar fades) before page scrolling continues. They explicitly authorized an improved trial build. Preserve Downloads' existing native scrolling, Watch History's approved 280 ms expansion, all themes and previous routes. The proposed correction stops canceling wheel events, including non-cancelable follow-up events during a continuous trackpad/wheel gesture; it lets the browser perform native scroll chaining first and only forwards an unconsumed delta when the parent actually remained stationary. It batches rapid events briefly to avoid competing with browser wheel momentum and avoids double-scrolling. This is unnumbered maintenance, **awaiting user testing** rather than visually approved.

## 2026-11-11 — Watch History native scroll chaining trial, user-authorized

User confirms the prior delayed wheel fallback made scrolling more natural but still jerky when moving between the episode and parent page. They explicitly approved a **structural native-scroll trial**. Watch History removes all custom wheel handoff logic (including the 36ms delayed scrollTop correction); its season and episode-animation clipping wrappers switch from `overflow:hidden` to `overflow:clip`, preventing those wrappers from acting as scroll containers while maintaining visual clipping and the **approved, unchanged 280ms grid-height expansion**. Normal nested scrolling and natural browser scroll chaining handle the handoff. The custom episode scrollbar remains with its existing fade and drag behavior. Downloads and primary/secondary navigation remain untouched. The regression suite tests continuous wheel gestures in both directions, native boundary crossover and the absence of double-scroll. This unnumbered trial needs the user's visual confirmation before it is marked approved.

## 2026-11-11 — Restore original Downloads scroll containment, user-authorized

The user reported that Downloads lost its previously working scrolling behavior, even after deleting and freshly downloading the latest HTML and opening Downloads directly without visiting Watch History. They explicitly approved restoring Downloads' pre-scroll-experiment CSS: `overscroll-behavior:contain` on `.sf-dl-viewport`. Only this Downloads declaration is changed; Watch History's current native-scroll trial, approved 280 ms expand/collapse, themes, animations, and all other UI remain untouched. Regression tests now assert native inner Downloads scrolling and scroll containment, while the separate Watch History scroll-chaining tests remain in place. This is an unnumbered corrective build **awaiting user testing**, not yet visually accepted.

## 2026-11-11 — Shared native episode scrolling and three-state Watch History toggle (trial)

The user approved merging Downloads and Watch History under **one shared native scrolling policy**, rather than adding custom wheel-interception workarounds. Both episode viewports now use the same `gallery-episode-scroll` rule: vertical overflow auto, horizontal overflow hidden, vertical overscroll auto for two-way page handoff, horizontal containment. Downloads' verified working handoff returns, and Watch History retains its independent layout and fading scrollbar. Keep the approved 280ms Watch History expansion and Downloads visual treatment unchanged. Both pages are now checked by the same browser boundary-scroll tests.

User also reported the loss of a three-state episode-status toggle. A full-width episode button now cycles **Not watched → Partially watched → Watched → Not watched** on click or keyboard activation. The status indicator uses appropriate ARIA pressed values false/mixed/true. A persisted manual status override is separate from real playback timestamps; changing watched state never invents a playback position, and new actual playback returns to automatic tracking. Watch counts reflect visible status. This is an unnumbered trial pending user visual/interaction confirmation; no native macOS build was changed.

## 2026-11-11 — Shared scrolling and three-way Watch History status visually accepted

After hands-on testing of the unnumbered shared-native-scrolling + three-state Watch History build, the user explicitly confirmed **scrolling feels equally smooth in both Downloads and Watch History** and **the three-way episode watched-state toggle works as intended**. Mark both features as **approved and locked**. Preserve the single shared native `gallery-episode-scroll` overflow/overscroll policy, two-way seamless vertical handoff, absence of custom wheel interception, Downloads' existing layout, Watch History's fading scrollbar and approved 280 ms reversible expansion, and all six themes. The Watch History full-row status cycle remains **Not watched → Partially watched → Watched → Not watched**, with keyboard activation, accessibility semantics and manual-status separation from genuine playback progress. Do not revert Downloads to `overscroll-behavior:contain` or reintroduce manual wheel handoff without explicit user discussion and approval.

Visual acceptance applies to immutable checkpoint `gallery/checkpoints/2026-11-11-shared-native-scroll-three-state/` (SHA-256 `7f9922d18f2ddd8b61035f5d2a524d3482fa3df5ea84045cf75be12c004eff45`; 6,951,729 bytes), GitHub build commit `b4ae88c67741860b3c1257571c496cf80aa3e61b`. This is an approval record only; the authoritative HTML and checkpoint bytes are unchanged. It is not a native macOS app integration claim.

## 2026-11-12 — Subtitle default white and intensity restoration, approved for trial

Following the Player/Settings regression audit, the user approved correcting both identified subtitle appearance differences. Restore the approved **Soft White default and preset to `#F8F8F8`** (from `#F5F5F5`) and restore **four intensity labels: Low, Medium, High, Max** for Outline, Shadow, and Background. The existing `light`, `normal`, `strong` stored IDs retain their existing numeric values, relabeled Low, Medium, High respectively, to preserve existing saved settings and their visual results; a new `max` ID provides the upper value (outline 6 subject to its approved font-size cap, shadow 10, background opacity 100). Medium remains the default. Prior user-chosen custom text colors remain custom; historical default whites migrate to the corrected Soft White preset.

The four buttons use a responsive four-column row, without changing the locked subtitle preview sizing, day/night images, animation behavior, themes, Player, Downloads or Watch History. Permanent browser regressions now cover all intensity values, the corrected white, Reset and narrow layouts. This is an **unnumbered corrective build for user visual testing**, not user-visually accepted yet.

## 2026-11-12 — Simplified subtitle intensity and Custom color indicator, approved for trial

After testing the four-level intensity version, the user approved simplifying to **Low / Medium / High** because None is already a separate style. Preserve Low and Medium values and make High use the former Max values (outline 6 subject to font-size cap, shadow 10, background opacity 100). Migrate old Max IDs to High; prior High intentionally becomes stronger. Medium remains default. The Soft White preset/default stays #F8F8F8. Custom displays the existing palette icon until a custom color has been explicitly saved; thereafter show its saved swatch even when another preset is selected. Preserve the existing color picker, live preview, Cancel/Done, recall and Reset behavior. No artwork, preview geometry, theme, navigation, scrolling or playback changes. The existing browser regressions are updated for the approved three-level choice and test palette/swatch, cancel, recall, reset and legacy Max migration. This is an unnumbered build awaiting visual confirmation.

## 2026-11-12 — Background banding experiments and deferred integration

The user observed color banding in Gallery on a work monitor. The first standalone experiment (0/2/4/6% SVG overlay noise) did not resolve it. In the second experiment (commit f94ee84453ef77add4dbac69c59d265b4f016e3e; gallery/experiments/2026-11-12-gradient-techniques.html), the original CSS gradient, 15% overlay and 8% normal-blended noise still showed banding. The user confirmed direct pixel-level dithering hides/removes it; Fine and Light were acceptable, while Standard and Strong introduced visible noise. **Direct dithering is the chosen direction; Light (step 2) is the preferred integration trial, with Fine (step 1) an alternative if it proves sufficient.** Do not treat the exact final strength as locked without integration testing. Preserve all six theme colors, backdrop geometry and stationary behavior; keep texture out of text, icons, artwork and controls. The user approved recording this result and auditing old/redundant/unused code first. Integrate only after separately approved cleanup; no Gallery HTML changes or background implementation in this documentation commit.


## 2026-11-12 — No legacy preference migration for unreleased prototypes

The user confirmed they are the sole tester and have no legacy preferences to carry forward. During pre-release Gallery development, do not maintain backwards compatibility with superseded prototype preference formats or storage keys. Preserve current preference persistence, defaults, validation, Reset behavior and safe fallback for invalid or malformed values. Remove obsolete migration paths when identified; do not remove intentionally dormant features or compatibility with StrawVerse sources, and do not change the native app or its settings schema without separate approval. Before the first public release, establish a supported settings schema and migration strategy for subsequent public updates.

The approved maintenance change removes historical subtitle numeric-size, raw numeric intensity, Max, background-selector, hex-only color, shadow-color and experimental storage-key migrations; it also removes the old fixed-volume mode alias and experimental font storage-key fallback. Current theme validation was already correct and remains unchanged. Current stored subtitle and volume IDs remain intact; no visual layout or feature change is intended. Tests now cover current preference round-trips and safe fallbacks rather than preservation of obsolete formats. This supersedes earlier audit guidance to retain legacy prototype preference migrations, including the legacy Max migration requirement, and does not supersede any approved current UI values. HTML checkpoint `2026-11-12-remove-prototype-preference-migrations`, build commit `cc2c920def8fda0937272ea744d13afdf5f18c7f`; awaiting user visual testing.


## 2026-11-12 — Simplified GitHub delivery and recoverable development sessions

The user explicitly approved replacing mandatory ChatGPT HTML attachments with immutable GitHub download links to reduce large-file transfers and Unknown Error interruptions. For each verified build, link directly to `gallery/Gallery-current.html` at its exact verified GitHub build commit (GitHub file page with Download raw file control) and provide the separate commit URL. Do not require a ChatGPT attachment, ZIP, additional release, or new feature-specific workflow. Preserve checkpoint creation, SHA-256/byte-count verification, both read-only CI checks, the protected branches and all historical snapshots. `gallery/DEVELOPMENT-STATE.md` records task handoff and actual testing status; current pointer and GitHub evidence remain authoritative. No Gallery HTML, visual behavior or native app is changed by this infrastructure decision. Older historical delivery requirements are superseded by the current workflow.

## 2026-11-12 — Asset separation and lightweight development builds

The user approved separating the two original subtitle preview PNGs from everyday development builds. Default standalone development HTML uses plain day/night CSS backgrounds, preserving the preview layout, controls, expanded view and synchronized animation. Opt-in subtitle-preview and full HTML modes embed the original unmodified PNGs; future native macOS integration will include the artwork, but no native application change is authorized here. The first reversible migration leaves the canonical full HTML, immutable checkpoint, six themes and all approved functionality unchanged; full reconstruction must be byte-identical. No image generation, image editing, reencoding or numbered build. The extracted template is transitional, not a new source authority. Both existing verification workflows must pass before delivery.


## 2026-11-12 — Manual subtitle preview Day/Night switch (approved for implementation)
Replace automatic subtitle-preview cycling for all motion preferences with a single, keyboard-accessible Day/Night switch aligned above the right edge of the preview image. Rename the visible full preview heading to “Subtitle preview” and remove the automatic-cycling description. Keep the expand button, compact preview entry, existing reset and subtitle controls, original artwork and 16:9 geometry. Day is the default; the main and expanded preview share the selected scene for the current page session. Switching is instant and unaffected by Reduce Motion; no continuous cycling. The lightweight mode uses the existing plain colors, and full/preview builds retain the exact PNGs. This supersedes earlier approved automatic shrine crossfade behavior only; all other Gallery motion decisions remain locked. User visual acceptance is pending.


## 2026-11-12 — Expanded subtitle preview polish (approved for trial)
The user requested reduced padding, removal of the visible About subtitle rendering box, and outlined sun/moon icons in the shared Day/Night switch. The expanded dialog uses consistent 12px inner padding and one header with title on the left, 100% / Fit scaling control, Day/Night switch and Close on the right. On very narrow windows the control group may wrap to keep all controls accessible. Remove the lower toolbar and help text; retain an accessible label and tooltip for the actual-size control. Preserve exact 1280 × 720 actual size with scrolling as needed, fit mode aspect ratio, original PNGs, current shared scene, manual instant switching, Reset, search targeting and accessibility live status. Relocate the existing Settings search target to the subtitle heading. Preserve all six themes and unrelated approved behavior. Unnumbered HTML maintenance for user testing; no native changes.


## 2026-11-12 — Adaptive preview scaling and Sub/Dub-style Day/Night selection (approved for trial)
Hide 100% when Fit already shows the 1280 × 720 CSS-pixel preview stage, including when a window resize makes that possible. Show 100% when fit is smaller and Fit when manual actual size is selected. Retain focus safely if the control disappears, scroll-to-inspect actual-size behavior, and 16:9 geometry. Match the anime detail Sub/Dub selector's current stationary selected-button theme gradient, separate inactive hover, 260 ms gradient/color transition and reduced-motion behavior. One grouped Day/Night selector with two directly selectable options; clicking the active option does nothing. Retain sun/moon icons and synchronize both previews; switching artwork itself stays instant and hover never changes the scene. Share active styling with Sub/Dub while retaining compact preview dimensions. All six themes, original assets and unrelated behavior preserved. No numbered release or native changes; user visual approval pending.


## 2026-11-12 — Visual acceptance of refined subtitle preview
The user visually approved the full build at commit `145f98e396f9b74d33cba6a636bf942ddcf79986` ("looks great.."). Preserve the current preview layout, adaptive 100% / Fit visibility, manual Day/Night selection with shared Sub/Dub styling, icons, synchronized instant scene changes and 12px expanded padding. The latest design is accepted rather than an open trial; this does not imply separate approval of unrelated cleanup, native playback integration or the proposed publisher-notification improvement. No new HTML checkpoint.


## 2026-11-12 — C2 retired theme CSS and C3 unused keyframe cleanup
User approved removing exactly 15 CSS rules exclusively scoped to the retired Neon Reel, Midnight Cinema and Paper Lantern theme IDs (neon/midnight/paper), plus the single unreferenced settings-enter keyframe. Keep all six active themes, current theme validation/fallback, search keywords, other animation keyframes, duplicate selectors, JavaScript, HTML markup, original artwork and approved UI intact. Compare current theme computed styles in both builds against the verified prior checkpoint and retain existing regressions. No numbered release, native changes or source-authority change. Publisher notification improvement is deferred at user's request; C3 duplicate-rule cleanup and dithering require separate approval.


## 2026-11-13 — Exact duplicate CSS cleanup (C3)
User approved removal of the 14 earlier identical rules after individual source-order review. Preserve the later copy of each in its original position and conditional context; no bulk removal of non-identical selectors. Keep all six themes, responsive breakpoints, navigation and motion, markup, JavaScript, assets and source authority unchanged. Compare the exact prior stylesheet and candidate stylesheet across six themes, 14 viewport widths, normal and reduced motion and hover, and retain existing both-mode UI tests. No numbered release or native changes. C4 remains read-only until specific cleanup approval.


## 2026-11-13 — C4a retired Downloads CSS
User approved the first C4 maintenance patch: remove exactly 52 rules scoped to 20 retired Downloads class names (48 old rules, four superseded Soft Futuristic rules). Preserve all current markup and JS, shared expansion and scroll classes, existing progress and action states, responsive geometry, six themes, motion, assets, native app and source authority. Compare actual Downloads rendering and behavior against the verified prior checkpoint in both build modes. No numbered release. C4b Anime detail CSS remains a separate proposal.


## 2026-11-13 — C4b retired Anime detail CSS
User approved the second C4 patch: remove exactly 64 retired Anime detail/placeholder CSS rules and the connected-season-card branch of the shared transition rule; retain inline-installment-card styling and transition unchanged. Preserve current season and related release navigation, audio and episode filters, source matching, Player navigation, six themes, responsive layouts, motion, artwork, markup, JS and source authority. Verify before/after actual detail views in both build modes; no numbered release or native change. C5 investigation is read-only until specific changes are approved.


## 2026-11-13 — M1 lossless source-block extraction
User approved M1 after C5 audit: extract existing CSS and classic JavaScript blocks without changing any byte of full or lightweight HTML output. Use the existing dependency-free Python builder, explicit ordered manifest, original assets and single inline style/script assembly. Canonical `Gallery-current.html` and its immutable checkpoint remain authoritative; no new HTML checkpoint, numbered release, source-authority transition, module runtime or native changes. Synchronize derivative files from approved canonical edits and stage them with future publisher commits. Require exact round trip and both independent read-only checks. M2+ require further agreement; M1 canonical sync fails closed on multiple fragments.


## 2026-11-13 — Source-first authority transition before M2
User explicitly approved moving development authority to the smaller source files (`gallery/src/` including ordered manifest, plus original `gallery/assets/`) after M1 verification. Both standalone HTML files are generated deliverables; the full HTML and immutable checkpoint remain exact delivery/recovery artifacts, not independent editing inputs. Retire reverse sync. Use the existing deterministic Python builder, preview outputs under dist, explicit generation of both tracked deliverables for approved source edits, and the existing controlled publisher and two independent checks. Keep all current HTML bytes, assets, functionality, checkpoints and native branches unchanged for this infrastructure-only milestone. Future source repartitioning, behavioral changes, artwork and numbered releases require separate approval; no M2 extraction yet.


## 2026-11-13 — M2 ordered CSS fragmentation
User approved M2 after source-first transition: partition the existing stylesheet into descriptive, ordered contiguous source fragments without changing any byte of the assembled CSS or generated HTML. Preserve all rule order, whitespace, comments, conditional blocks, themes, animation and responsive styles; retain pre-existing syntax anomalies rather than silently fix them. Update explicit manifest and source map. No JavaScript, artwork, native, checkpoint or numbered release change. Require both independent verification workflows. M3+ remains separate.


## 2026-11-13 — Intentional CSS overrides and shared design standards
User agreed to the principle: define consistent global design standards, build shared components that inherit them, and use specific overrides only where genuinely justified. Responsive, theme, state, accessibility and intentional feature-specific differences remain legitimate; accumulated corrective overrides should be reviewed and consolidated into the appropriate shared/base rule only when proven equivalent or separately approved as a design change. Preserve all approved appearance, behavior, six themes, motion and historical checkpoints. This is agreement on the design-system direction, not authorization to remove any particular rule, change cascade order, correct the known search syntax anomaly or redesign features. A future read-only audit should identify override chains, classify them and propose staged changes for discussion.


## 2026-11-13 — M3 shared JavaScript utilities and data extraction
User approved proceeding with JavaScript modularization first, then the separate design-system consistency audit. M3 extracts existing shared utility and sample-data sections in place, using explicit ordered contiguous fragments and exact byte reconstruction. Preserve classic script scope and execution order, all functions, global state, events, persistence keys, original artwork tokens, CSS, generated HTML, checkpoint and native branches. No imports/exports, behavioral refactor or numbered release. Larger feature/core blocks remain for staged M4/M5 discussion; verify both independent checks. Override consolidation and search syntax correction remain unapproved.


## 2026-11-13 — M4 feature-specific JavaScript partition
User approved proceeding after M3 verification: partition remaining large feature blocks in place without altering any assembled script byte, execution order, global scope, CSS, assets, HTML, checkpoint or native branches. Preserve interleaved feature sections where needed; no imports, exports, deletions, refactoring or numbered release. M5 core work and design-system override changes remain separate. Require both independent checks.


## 2026-11-13 — M5 core JavaScript partition
User approved final lossless source fragmentation after verified M4. Split remaining core preferences, app state, font preferences, route transitions, scroll overlay, tab lifecycle, rendering/event binding and tab motion/navigation in place. Keep the already isolated core render and bootstrap unchanged; no splitting functions, reordering, runtime module conversion or behavior changes. Preserve exact script bytes, CSS, assets, generated HTML, immutable checkpoint and native branches. Both independent checks required. Design-system override audit follows separately; no override cleanup or syntax correction authorized.


## 2026-11-13 — Approved success-gated Queue 1
User approved dependency updates and automatic read-only inventory and syntax investigation after both checks succeed. Upgrade checkout/setup-python in the two checks and controlled publisher, preserving Python version, test commands and existing permissions. Queue runs only on the active branch from the explicit approved plan; its own permissions are read-only. It checks both independent push runs for the exact plan commit, stops on failure/timeout, performs design-system inventory and isolated in-memory anomaly investigation sequentially, stores evidence as a workflow summary/artifact, then stops for human review. Queue 2, specific CSS changes, syntax correction, dithering, native changes and any new numbered build require separate approval. No application or checkpoint mutation by this queue.


## 2026-11-13 — Discover Search collapse syntax correction
User approved the separate CSS syntax fix after discussion of the Recently Watched collapse/expand in Discover Search. Delete only the malformed duplicate transition at `styles/09-search.css:64`, restoring the valid clipping/min-height rule previously swallowed by browser error recovery. Keep approved timings, layout outside this interaction, search results, history data, all six themes and native branches unchanged. Add actual Gallery browser regression across desktop, narrow and reduced-motion contexts on both builds. Use the controlled publisher, new immutable checkpoint if bytes change, and both independent checks. This does not authorize general CSS override cleanup or dithering.


## 2026-11-13 — Shared full-width Downloads and Watch History content frame
User reported narrower Downloads rows and delegated the proposed first shared design-standard correction. Downloads must use the same available content width and horizontal gutters as Watch History, aligning with its own page header. Remove the old 1220px Downloads cap and superseded 1120px Watch History cap; use one shared width rule with no extra corrective override. Preserve Watch History as reference, individual card layouts, spacing, scrolling, expansion, all themes and existing navigation. Check rendered outer row and header left/right/width across desktop and responsive widths in both builds. Controlled publisher and both independent checks required; visual approval follows. No numbered release, general CSS consolidation or background dithering authorized.


## 2026-11-13 — Design Standard 01 visually approved
After testing the delivered checkpoint `2026-11-13-shared-download-history-width` (build commit `41383b618be8c7dc92511a8d7370e359db3e9465`), user confirmed it looks fine. Lock the shared full available content width and horizontal alignment of Downloads and Watch History, including alignment with their page headers. Preserve existing card layouts, scrolling, expansion and themes. Both independent checks passed, with rendered width/edge parity at all eight tested viewport sizes on both builds. This acceptance is scoped to the shared width correction; separate pending visual tests and approval of Queue 2 are not inferred.


## 2026-11-13 — Approved Q2-A eight whole-rule cleanup
User approved exactly the eight earlier complete CSS rules in `gallery/audits/2026-11-13-queue-2-identical-value-review.md` (11 declarations). Keep all later declarations, other rules and conditions in original order. Verify exact baseline source hashes, compare both actual generated HTMLs against DS01 with only these eight rule deletions and no non-CSS differences; gate on computed styles and geometry for affected elements and descendants across six themes, responsive widths, normal/reduced motion and hover/focus. Controlled publisher runs a request-specific read-only comparison before normal regression and checkpoint creation; any comparison failure blocks publication. Both independent checks required; visual approval remains separate. No broader CSS cleanup or numbered release authorized.


## 2026-11-13 — Q2-A visually approved
User tested checkpoint `2026-11-13-q2a-eight-redundant-css-rules` (build `e97704268953e523c459521f86ab3bbd634b3d52`) and reported no visible changes, as expected. Accept the eight-rule cleanup. Both independent checks and the 1,440-comparison gate passed. No further CSS removals, Q2-B, or new Back-button color treatment are authorized by this acceptance.


## 2026-11-13 — Design Standard 02: tinted accent Back buttons
User approved the suggested soft tinted accent treatment. Apply one shared theme-aware Back button color rule to Anime details, Watch History, Player and Settings page headers, using existing palette tokens. Accent text/icon, 12% accent/panel background, 55% accent/panel2 border; hover 20% background and 70% border. Preserve pill shape, size, position, border thickness, keyboard focus, reduced motion, navigation provenance, other buttons, all six themes and DS01. No full accent fill, changes to markup, assets, native branches or unrelated cleanup. Actual-route browser checks on both builds across six themes, three widths, normal/reduced motion, rest/hover/focus, contrast and navigation. Controlled publisher and both independent checks; separate visual approval.


## 2026-11-13 — DS02b stronger tinted Back accent
User found DS02 improved but some themes still blend into their page backgrounds. Approved one global stronger tint/border refinement before considering theme-specific exceptions. Rest: 20% accent/panel fill, 72% accent/panel2 border. Hover: 24% fill, 82% border (24% selected to preserve >=4.5:1 text contrast in Slate). Supersedes DS02 mix percentages only. Preserve text/icon, geometry, shape, focus, motion, navigation and all other controls. Update existing DS02 tests on both builds to verify exact colors, improved fill/border luminance versus DS02, >=3:1 border contrast against representative panel2 token and >=4.5:1 text contrast, geometry/focus/navigation. Actual page appearance requires separate visual approval; no per-theme exceptions or other changes authorized.


## 2026-11-13 — DS02b visually approved
User tested the stronger shared Back-button treatment in checkpoint `2026-11-13-ds02b-stronger-back-accent` (build `e108c7c892eab7e41d892ae06874c78f58160011`) and confirmed it looks better. Accept and lock the global DS02b treatment: 20% accent fill / 72% border at rest, 24% fill / 82% border on hover, accent text and icon, existing focus, motion, geometry and navigation. Both independent checks passed. No theme-specific exceptions or further Back-button refinements needed at this point. This acceptance does not approve Q2-B changes or other unrelated work.


## 2026-11-13 — Approved Q2-B1 Downloads partial-rule cleanup
User approved exactly 16 earlier declarations within six retained Downloads CSS rules, listed in `gallery/audits/2026-11-13-q2b-partial-rule-review.md`. Keep later copies, all other declarations, rule order, media contexts, DS01 width and scroll behavior, DS02b, all six themes, animation, markup, JS, assets and native branches unchanged. Gate on exact DS02b full/lightweight baseline hashes and exact CSS-only diff, actual Downloads computed-style/pseudo/geometry equivalence across six themes, ten widths, expanded/collapsed, normal/reduced motion, mixed statuses, hover/focus, filters/search. Standard regression and both independent checks required, new immutable checkpoint if changed; user visual approval separate. No remaining 78 candidates, grouped selectors, differing-value cleanup, dithering or numbered release approved.


## 2026-11-13 — Q2-B1 visually approved
User tested checkpoint `2026-11-13-q2b1-downloads-declarations-retry` (build `58eaad52e9cad8250341c7070aacbf4395e44b1b`) and confirmed no visual difference. Accept the 16-declaration Downloads cleanup; 672 actual-DOM comparisons, standard publisher regressions and both independent checks passed. Preserve DS01 and DS02b and the current Downloads appearance and behavior. No authorization for remaining 78 declarations, verification infrastructure changes or other work. No new HTML checkpoint.


## 2026-11-13 — Approved verification efficiency work
User approved parallel execution, browser caching and smarter scheduling before continuing CSS cleanup, preserving all verification coverage, pinned browser version, exact-commit checks and immutable checkpoint safeguards. Stage 1: three mandatory independent browser jobs (full routes, lightweight routes, both-mode subtitle previews), exact-version Chromium cache shared with controlled publisher and one bounded installation retry, read-only two-mode Q2-B1 benchmark at the accepted checkpoint (336 comparisons per shard). No changed application code, assets, generated bytes or historical checkpoint; no historical test rewrite, skipped tests, changed workflow permissions or native branches. Keep publisher commit/verification order unchanged until benchmark evidence supports a safe next stage. No new numbered release or further CSS removal approved.


## 2026-11-13 — Approved verification efficiency stage 2
User approved candidate-once parallel controlled publishing after verified stage 1. Exact artifact ID, SHA-256, Git tree and source assembly checks for every candidate consumer; all standard and approved comparison groups must succeed; only final publication job has write permissions. Preserve atomic source/HTML/checkpoint commit, non-force push on exact request head and both independent post-commit checks. Historical corrected Q2-B1 read-only rehearsal uses the same preparation and test workflow and disposable staging, no remote publication; verify rejection of corrupted artifact and wrong tree. No application, artwork, generated HTML, historical requests or checkpoint changes and no further cleanup authorization.


## 2026-11-14 — Approved Q2-B2 Anime episode toolbar cleanup
User confirmed the affected Episodes/Sub-Dub availability/All-Playable only toolbar in their own Gallery screenshot and explicitly approved exactly 17 earlier declarations across seven retained rules in `07-anime-detail-refinements.css` as listed in `gallery/audits/2026-11-14-q2b2-episode-toolbar-review.md`. Preserve all later copies, other declarations, all media/container layouts, count animation/visibility, audio/filter interactions, hover/focus, all themes and reduced motion. Paired full/lightweight exact-diff/real-DOM comparison gates and existing standard regressions required, plus new immutable checkpoint and both independent checks. No other CSS, markup, JS, assets, native changes or numbered release authorized. Visual acceptance separate.


## 2026-11-14 — Q2-B2 visually approved
User tested checkpoint `2026-11-14-q2b2-episode-toolbar` (build `fcc1d493b09dac7fa68703d199e3e234a33e1c37`) and confirmed no visual differences. Accept the 17-declaration Anime episode toolbar cleanup. All 1,272 actual-DOM comparisons, standard publisher regressions and both independent exact-build checks passed; first real parallel publication succeeded. Preserve the current toolbar appearance and behavior, including responsive layouts, count fades and filtering. Hold remaining 61 candidates for separate review and specific approval. No new HTML checkpoint or further application change.


## 2026-11-14 — Approved Q2-B3 remaining Anime Details cleanup
User explicitly approved exactly 12 earlier declarations across seven retained rules in `02-anime-detail.css` listed in `gallery/audits/2026-11-14-q2b3-anime-details-review.md`. Keep all later declarations, compact hero/control layouts, stationary Sub/Dub gradient, episode rows/tools/flags/actions, toolbar and count animations, media/container/state rules, DS02b and all six themes. Paired exact-scope real-DOM gates, existing regression suites and independent post-publish checks required. No other CSS, JS, markup, assets, native or numbered-release changes. Remaining 49 candidates held; visual acceptance separate.
