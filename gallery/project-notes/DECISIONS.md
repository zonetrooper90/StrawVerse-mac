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
- **Discover Recently Watched preview:** one cover per anime, ordered by most recent playback/resume. New/replayed anime move left; older anime may leave the Discover preview but remain in the full history.
- **Full Watch History:** one row per **anime season**, rather than one row per episode or one row for all seasons combined. Separate seasons of the same anime get separate entries. Each row summarizes where the viewer reached within that season (latest reached episode and playback position/progress), without displaying a separate chronological row for every episode.
- **Season identity and titles:** season entries must preserve their own anime/release titles rather than be automatically collapsed under a franchise title or renamed merely 'Season 1/2/3'. Anime sequels often have distinct titles (example in Gallery: *The Quintessential Quintuplets*). Use stable per-season/source identity where available so differently named seasons remain separate, even when related to the same franchise.
- **Completed seasons are permanent history entries:** when every episode has been marked Watched (regardless of order), the season becomes Completed and remains in full history. Starting another season creates/updates its *own* entry, never replaces or removes an earlier one. The bounded Discover preview may show only recent anime, but that never deletes older/completed records.
- **Episode Watched rule (agreed):** mark an episode Watched when active video playback naturally reaches its final 20 seconds (the same time boundary used by Play Next). Scrubbing directly to that range must not by itself mark the episode Watched. This status is independent of the Autoplay setting and persists after rewatching.
- **Season Completed rule (agreed):** a season is Completed only when **every episode belonging to that season** is marked Watched, **in any order**. Users may watch episode 8 before episode 2; no sequence or finale-first requirement. The finale alone never completes a season unless all other episodes are already Watched. Completion does not erase the season's history entry.
- **Manual corrections (agreed):** from an existing season's Watch History entry, users can mark individual episodes Watched or Unwatched to fix missed tracking or playback that continued after they stopped watching (e.g., fell asleep). These corrections persist, recalculate season completion, and do not change saved resume positions. Keep per-episode controls in a 'Manage Watched Episodes' detail view instead of displaying an episode log in the main list.
- **No manual addition to Watch History (current design direction):** new season entries arise from actual playback, not a generic 'Add anime' control. Editing watched flags should not silently create a never-played history entry. Future explicit history-import/migration flows may be considered separately; they are not part of the current scope.
- **Watch History navigation (agreed):** clicking a season's history row navigates to its **existing anime detail page in Library** (for that season's own distinct title/identity). Do not create a separate Watch History-specific anime details page and do not automatically start playback just from clicking the row. Confirm fallback behavior if a watched anime is not in Library before implementation.


- Full-history rows remain ordered by their most recent viewing activity. Keep older season entries when the viewer progresses to another season.
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
