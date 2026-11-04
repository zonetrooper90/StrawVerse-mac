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
