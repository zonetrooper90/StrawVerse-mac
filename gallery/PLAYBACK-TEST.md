# Gallery Playback Test — Apple Silicon (isolated build)

This branch is a disposable **local-video and subtitle testing build** of Gallery's older v0.2.0 player. It is not Gallery v96, the current Settings experiment, or a streaming player. The original `gallery/v0.2.0-preview`, `main`, and StrawVerse branches remain untouched.

## Download and run

Open [the Gallery Playback Test workflow runs](https://github.com/zonetrooper90/StrawVerse-mac/actions/workflows/gallery-preview-macos.yml?query=branch%3Agallery%2Fplayback-subtitle-test). Choose a successful run and download the **`Gallery-Playback-Test-Apple-Silicon-DMG`** artifact. Unzip the GitHub artifact to obtain **`Gallery-Playback-Test-arm64.dmg`**, open the DMG, and drag **Gallery Playback Test.app** into Applications. This matches the earlier successful StrawVerse Mac development-build workflow.

The app is built for **Apple Silicon only**. The app is **ad-hoc signed, not Apple notarized**, using the same development distribution method as the earlier StrawVerse Mac builds. GitHub Actions verifies the code signature both in the app build and after mounting the DMG. Gatekeeper may still require first-launch approval because ad-hoc signing is not Apple Developer ID signing. Do not disable Gatekeeper globally.

## Test the player controls with subtitles

1. Open **Gallery Playback Test.app** and navigate to any fictional sample anime, then **Watch**.
2. Choose **Open local video…** and select your existing video file. The built-in Chromium player supports only codecs available to Electron; H.264 MP4 is generally the safest local test.
3. Below the video, choose either:
   - **Sample subtitles** — creates temporary example captions near your current playback position. No subtitle file is needed.
   - **Load .srt/.vtt…** — opens a native macOS file picker and loads an external SRT or WebVTT text file (up to 5 MiB).
4. Test the **CC** button to show/hide the captions. During playback, stop moving the pointer for about **2.6 seconds**: the existing title and player controls should fade away, leaving subtitles visible. Move the pointer to show controls again. Pause to keep them visible, then try seeking and fullscreen.

The local subtitle file is read only after you choose it. Its text is converted to WebVTT in memory, attached to the active video, and removed when the video is changed. No file is uploaded.

**Important limitations:** No real streaming providers, no source scraping, no embedded MPV, no Up Next UI, no playback-history logic, and no connection yet to the newer Subtitle Appearance settings. External VLC playback opens in a separate VLC window and does not use Gallery's custom controls or subtitle test track. This branch is intentionally limited to verifying the old built-in player's layout.

## Safety and isolation

- Bundle identifier: `dev.gallery.anime.playback-test`
- App name: `Gallery Playback Test.app`
- Settings: `~/Library/Application Support/GalleryAnimePlaybackTest`
- Original preview settings: `~/Library/Application Support/GalleryAnime` (not touched)
- Build branch: `gallery/playback-subtitle-test`

GitHub Actions runs `npm run check` (including subtitle conversion tests) before packaging the ARM64 app.


## Distribution verification

The workflow builds **Apple Silicon only**, verifies the ad-hoc signature with `codesign --verify --deep --strict`, verifies the DMG, mounts it, and verifies the actual packaged `.app` again. It does not require Apple Developer credentials. A passed CI run guarantees the archive passed these checks on the GitHub runner, but it does not certify Apple notarization or predict all Gatekeeper prompts on the testing Mac.
