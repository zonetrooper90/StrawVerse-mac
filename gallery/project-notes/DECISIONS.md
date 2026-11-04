# Gallery decisions — durable handoff

Last reviewed: 2026-11-04. Label each new entry **AGREED**, **PROPOSED**, or **UNVERIFIED**. Do not reinterpret design discussion as approval to create a new numbered version.

## AGREED: Product foundations
- Gallery is a separate macOS-focused client/fork; keep StrawVerse source/repository compatibility; Apple Silicon builds only.
- Main sections: Discover, Library, Downloads. Settings is full-page and hides ordinary navigation while open.
- User approval is required before generating/editing any images, including mockup illustrations.
- Discuss and obtain approval before creating any new numbered Gallery build; keep earlier versions intact.

## AGREED: Subtitle configuration
- Subtitle appearance is configured in Gallery's main Settings (font choices System / Atkinson Hyperlegible Next / Inter, responsive day/night shrine preview, styles, sizes and intensity). Preview dimensions established in A7 were locked.
- Subtitle track/language selection and Off live **inside Player Settings**; there is no extra subtitle button in the player control row.
- Audio language is selected **before** entering the player, not toggled there.
- Player Settings also includes Playback Speed.
- Switching subtitles off should remember the last selected track.

## AGREED: Player layout and responsive rules
- Left: volume. Center: rewind 10s, play/pause, forward 10s. Right: Settings and Fullscreen.
- Player controls shrink with the **player viewport**, not the outer window; do not grow above normal size in fullscreen. At extremely small sizes only Play/Pause remains.
- Progress timeline: two rounded color segments separated by a small gap, styled like Downloads, **no visible circular thumb**, but still seekable.
- Tabler Player Track Previous / Player Track Next represent ±10 seconds. During Play Next, forward morphs genuinely and reversibly into Tabler Player Skip Forward.
- Fade and slide in Play Next episode info **from the right**, and reverse when hiding; keep Settings, Fullscreen and center controls stationary.

## AGREED: Play Next / Autoplay
- Autoplay enabled: during the final 20 seconds, reveal controls, display upcoming episode info + countdown + Cancel, and advance at the end if not cancelled.
- Autoplay disabled: no timed appearance, countdown, or automatic transition; regular player continues unchanged.
- Countdown tracks remaining **video playback time**; pause, resume and seek update appropriately. Cancelling blocks autoplay for the current episode and restores ordinary controls/auto-hide. Scrubbing across the threshold should reverse transitions smoothly.
- A Dev Tools preview can demonstrate the UI without real media; a preview is not proof that real next-episode loading is wired.

## AGREED: Recently Watched / Watch History (not yet implemented in v99)
- Replace Continue Watching Discover area with **Recently Watched**: portrait anime covers, reveal title/latest episode on hover, contained within existing card bounds.
- Show only the newest covers that fit without scrolling/pagination; fixed View History shortcut at the end.
- One history entry per anime, newest actual playback/resume first. New/replayed items move left; older items may leave the Discover preview but remain in complete history.
- **Full Watch History view: chronological list of entries, not a poster grid.** A list intentionally distinguishes History from the cover-driven Discover and Library views and provides space for episode progress, last-watched times and other useful context. Exact row fields and grouping are still **UNDECIDED**; don't treat the illustrative layout as finalized.
- The Discover Recently Watched area still uses the previously agreed compact portrait-cover strip; the list decision applies to the **dedicated full Watch History page only**.

## Current HTML status
- v96 A28: main Settings/subtitle preview reference.
- v97: Settings integration.
- v98: Tabler icons, player morph / Play Next experiment integration.
- v99: player refinements (subtitle selection moved into Player Settings, rightward Play Next transitions, two-tone timeline without knob).
- The latest complete HTML milestone is **v99**, but see VERSION-INDEX.md and backup location for whether its actual bytes have been committed. Keep GitHub source branches and standalone HTML milestones distinct.

## Next-session startup checklist
1. Read WORKFLOW.md and this file.
2. Verify actual latest HTML is accessible before making edits, using its SHA-256 from VERSION-INDEX.md.
3. State which branch/file is being modified.
4. Discuss and confirm intended UI changes before creating a new numbered version.
5. After an approved change, commit updated decisions and verified artifacts; explicitly state what is and is not backed up.
