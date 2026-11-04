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
- **Manual corrections (agreed):** from an existing season's **expandable row** in Watch History, users can mark individual episodes Watched or Unwatched to fix missed tracking or playback that continued after they stopped watching (e.g., fell asleep). These corrections persist, recalculate season completion, and do not change saved resume positions. Keep individual episode details collapsed by default, rather than showing every episode in the main history list.
- **No manual addition to Watch History (current design direction):** new season entries arise from actual playback, not a generic 'Add anime' control. Editing watched flags should not silently create a never-played history entry. Future explicit history-import/migration flows may be considered separately; they are not part of the current scope.
- **Watch History navigation (agreed):** clicking a season's history row opens the corresponding season's **existing anime detail page in Library if the anime is in the user's Library; otherwise it opens that anime's existing detail page in Discover**. Do not add anime to Library merely because they were watched, do not create a Watch History-specific detail page, and do not auto-start playback. Preserve the season's distinct title/identity for routing.
- **Dedicated removal action (agreed):** removal of an entire season is a deliberate, separate action via a dedicated trash button, regardless of season length. Manually unmarking all episodes **does not automatically remove** the season from history.
- **Session-long Undo (agreed):** when a user removes a season, hide it from the visible Watch History but preserve its complete data in a pending-removal state **for as long as Watch History stays open**; no expiring Undo timer. Leaving the view may commit removal. Undo restores the previous history entry and episode progress/statuses. The precise appearance of Undo and behavior for multiple pending removals still need design review.
- **Expandable episode management (agreed):** the anime cover/title navigates to its existing details page; the separate chevron expands or collapses a per-season episode list for manual watched/unwatched corrections. Use a **scrollable, height-capped area showing approximately six episode rows at a time** for long seasons (e.g., Pokémon), with every episode still accessible by scrolling and **no pagination**. Short seasons show all their episodes without an unnecessary inner scrollbar. Scrolling in the expanded area scrolls episodes, not the entire history page. On expansion, initially position the inner list near the most recently watched episode when possible, particularly for long seasons.
- No numbered Gallery version is authorized by these design decisions; the precise visual sizing and styling still need review.


- Full-history rows remain ordered by their most recent viewing activity. Keep older season entries when the viewer progresses to another season.
- **Full Watch History view: chronological list of entries, not a poster grid.** A list intentionally distinguishes History from the cover-driven Discover and Library views.
- **History row details (agreed):** for an **In Progress** season, show the anime/season's source title, latest played episode and resume position, episode completion count (e.g. 8 of 12 episodes Watched), and last-watched timestamp. For a **Completed** season, show the title, a clear Completed status and last-watched timestamp; **do not repeat the total/count (e.g. 12 of 12)**, and omit the resume position as unnecessary completed-season clutter.
- The precise visual sizing and spacing of the rows remain **UNDECIDED**, and illustrative examples are not approved HTML mockups.
- The Discover Recently Watched area still uses the previously agreed compact portrait-cover strip; the list decision applies to the **dedicated full Watch History page only**.

## AGREED: Watch History search behavior
- Reuse Gallery's existing integrated search behavior, scoped to Watch History when viewing that page.
- Match history entries by **anime/season title** and **viewing date** (year, month and supported relative dates); a year refers to **when the user watched it**, not the anime's original release year.
- Preserve enough historical viewing-date information that a season watched in 2025 can still be found by a 2025 search after being rewatched in 2026; do not rely only on the latest-watched timestamp.
- A standalone four-digit year query (e.g. `2025`) prioritizes **watched-in-that-year** results, then title matches containing the year. Title-like phrases containing a year (e.g. `Anime 2025`) prioritize title matches.
- Never exclude a valid match merely because it has lower priority. Group or clearly identify matches by reason, and show an entry only once if it matches both title and viewing year.
- This is an agreed *search ranking and coverage rule*; exact search-results presentation still requires design review before implementation.

## AGREED: Watch History sorting
- Sort full Watch History by **Last Watched** (most recent actual playback for each season).
- **Newest First** is the default. Provide a compact control to reverse direction to **Oldest First**, without introducing a larger sort-method menu.
- Keep the same newest/oldest control when using status filters or search. Reversing direction must not change the underlying episode/season history.
- Manual corrections to Watched/Unwatched flags do **not** change the last-watched timestamp or move a season in the sort order; actual viewing activity does.
- When searching for a viewing year, preserve the previously agreed search-match priority (date matches before title matches for standalone years), and use chronological order within the relevant matches.
- **Status filter reset (agreed):** leaving and reopening Watch History resets the status filter to **All**; do not persist an In Progress / Completed selection across visits. Search state should also clear when leaving the Watch History view to follow Gallery's tab-scoped search behavior.
- **Sort direction resets with filters (agreed):** treat sorting as part of the Watch History filter state. Whenever the user leaves and reopens Watch History, reset the status filter to **All**, sort direction to **Newest First**, and clear the Watch History search. Do not persist these display preferences across visits; underlying watched records remain unchanged.

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
