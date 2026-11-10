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
