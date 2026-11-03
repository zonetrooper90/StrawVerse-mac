# Gallery Playback Test — Apple Silicon (isolated build)

This branch is a disposable **local-video and subtitle testing build** of Gallery's older v0.2.0 player. It is not Gallery v96, the current Settings experiment, or a streaming player. The original `gallery/v0.2.0-preview`, `main`, and StrawVerse branches remain untouched.

## Download and run

Open [the Gallery Playback Test workflow runs](https://github.com/zonetrooper90/StrawVerse-mac/actions/workflows/gallery-preview-macos.yml?query=branch%3Agallery%2Fplayback-subtitle-test). Choose a successful run, download the `Gallery-Playback-Test-Apple-Silicon` artifact, unpack it, and unpack `Gallery-Playback-Test-Apple-Silicon.zip` to obtain **Gallery Playback Test.app**.

The app is built for **Apple Silicon only**. The build workflow now distinguishes **ad-hoc development signing** from **Developer ID signing and notarization**. Until valid Apple credentials are configured, macOS Gatekeeper can still block the downloaded app. You may need to approve it manually; do not disable Gatekeeper globally. An ad-hoc signature does not make an app trusted on another Mac.

## Test the player controls with subtitles

1. Open **Gallery Playback Test.app** and navigate to any fictional sample anime, then **Watch**.
2. Choose **Open local video…** and select your existing video file. The built-in Chromium player supports only codecs available to Electron; H.264 MP4 is generally the safest local test.
3. Below the video, choose either:
   - **Sample subtitles** — creates temporary example captions near your current playback position. No subtitle file is needed.
   - **Load .srt/.vtt…** — opens a native macOS file picker and loads an external SRT or WebVTT text file (up to 5 MiB).
4. Test the **CC** button to show/hide the captions. Seek, pause, use fullscreen, and inspect the caption position relative to the real player controls.

The local subtitle file is read only after you choose it. Its text is converted to WebVTT in memory, attached to the active video, and removed when the video is changed. No file is uploaded.

**Important limitations:** No real streaming providers, no source scraping, no embedded MPV, no Up Next UI, no playback-history logic, and no connection yet to the newer Subtitle Appearance settings. External VLC playback opens in a separate VLC window and does not use Gallery's custom controls or subtitle test track. This branch is intentionally limited to verifying the old built-in player's layout.

## Safety and isolation

- Bundle identifier: `dev.gallery.anime.playback-test`
- App name: `Gallery Playback Test.app`
- Settings: `~/Library/Application Support/GalleryAnimePlaybackTest`
- Original preview settings: `~/Library/Application Support/GalleryAnime` (not touched)
- Build branch: `gallery/playback-subtitle-test`

GitHub Actions runs `npm run check` (including subtitle conversion tests) before packaging the ARM64 app.

## Warning-free macOS distribution

A standard GitHub Actions ZIP cannot by itself prevent macOS Gatekeeper's quarantine prompts. **Normal first-launch without an exception requires an Apple Developer ID Application certificate and Apple notarization**, including a stapled ticket. A personal Apple ID or an ad-hoc signature is insufficient.

If you have an Apple Developer Program account, set these **repository Actions secrets** (never commit them or paste them in chat):

- `GALLERY_MAC_CERT_P12`: base64-encoded export of your Developer ID Application certificate and private key in a .p12 file
- `GALLERY_MAC_CERT_PASSWORD`: password for the exported .p12
- `GALLERY_APPLE_ID`: Apple ID used for notarization
- `GALLERY_APP_SPECIFIC_PASSWORD`: an app-specific password for the Apple ID
- `GALLERY_APPLE_TEAM_ID`: Apple Developer Team ID

The workflow automatically selects the signed/notarized path only when **all five secrets** exist. It enables Hardened Runtime, requests notarization, and verifies the app signature, Gatekeeper assessment and notarization ticket before publishing the ZIP. Incomplete credentials fail the build instead of silently publishing an untrusted app.

Without those secrets, GitHub Actions creates a clearly marked **ad-hoc development build** and verifies the resulting code signature for packaging integrity, but **this cannot eliminate Gatekeeper warnings for downloaded apps**. The workflow does not and must not remove the security quarantine attribute on the user's Mac.
