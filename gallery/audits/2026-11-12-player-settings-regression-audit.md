# Player and Settings — read-only regression audit

**Date:** 2026-11-12  
**Repository:** zonetrooper90/StrawVerse-mac, branch gallery/development-clean  
**Authoritative working HTML:** gallery/Gallery-current.html  
**Immutable checkpoint:** 2026-11-11-shared-native-scroll-three-state  
**Source SHA-256:** 7f9922d18f2ddd8b61035f5d2a524d3482fa3df5ea84045cf75be12c004eff45  
**Byte count:** 6,951,729  
**Git blob:** 72451a49d976480719c7b37d6a778d1e17db7083  
**User-approved HTML build commit:** b4ae88c67741860b3c1257571c496cf80aa3e61b

## Method

A read-only exploratory browser audit exercised the checksum- and Git-blob-matched HTML in Chromium, against approved GitHub decisions and earlier subtitle design discussions. The audit completed **51 checks: 49 passed, 2 discrepancies**. No HTML was modified or used as a development baseline. The separate permanent regression script protects the currently passing behaviors. No real source streaming or macOS integration was tested.

## Confirmed passing behaviors

**Player:** available demo title opens with preselected Sub audio and default 70% volume; episode/season label and equal reserved navigation slots; Player Settings includes playback speed and subtitle Off; subtitle Off persists while the menu is reopened. Player simulation exercises play/seek, 25%-step volume icon changes, mute/unmute, Play Next at 20 seconds with countdown and forward-to-Next morph, cancellation, seeking away/back, autoplay disabled, and demo Resume starting eight seconds before saved position. No JavaScript errors in these tests.

**Settings:** hides Discover/Library/Downloads navigation; shows Appearance/Playback/Downloads/Sources/About; six selectable themes (Ocean, Twilight, Ember, Slate, Glacier, Verdant); subtitle editor has three font options, five size presets, four effect styles, approved text sentence, day/night layers, working font/size and Reset; full inline preview retains 16:9. Responsive testing at 1600, 1280, 800, 440, and 340 CSS-pixel widths confirms exactly one of full preview and compact shortcut is visible; compact shortcut opens expanded preview. No JavaScript errors were observed.

## Findings — do not change until discussed

**F1: Confirmed design mismatch — soft white default.** GitHub APPROVED-DECISIONS.md specifies subtitle soft-white default **#F8F8F8**. Current HTML subtitle defaults and white preset use **#F5F5F5**. This is a specific low-risk design discrepancy, not an excuse to rework the preview artwork or layout.

**F2: Needs design confirmation — effect intensity.** Earlier design discussions specified four levels (Low, Medium, High, Max); current HTML shows three (Light, Normal, Strong). The current GitHub decisions document confirms effect intensity but does not specify names/count. Confirm the old four-level choice before modifying.

## Not newly established regressions

Real provider playback, source loading, automatic next-episode media loading, native macOS playback/history integration and real codec compatibility are beyond the HTML demo; simulation behavior is not proof of these integrations. Responsive subtitle layout animation remains a previously discussed, not-yet-implemented polish item. Real Mac trackpad feel and visual transition smoothness still need hands-on confirmation.

## Regression protection

The new test_player_settings_regression.py runs through the existing read-only gallery-transition-ui.yml workflow alongside the established navigation, motion and Watch History tests. It guards the passing behaviors without adjusting expectations to hide F1 or F2. These findings remain documented for user review.

**Scope:** this Markdown audit report, a browser regression test and an existing workflow call only. Gallery-current.html, current.json and every immutable checkpoint stay unchanged. No numbered build.
