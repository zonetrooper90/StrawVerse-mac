# StrawVerse macOS (community build)

This fork adds experimental **standalone macOS builds** to StrawVerse. Your Mac does **not** need Homebrew, MPV, FFmpeg, Node.js, or developer tools.

## Download

1. Open [the macOS build workflow](https://github.com/zonetrooper90/StrawVerse-mac/actions/workflows/build-macos.yml).
2. Open the newest **successful** run of *Build standalone macOS apps*.
3. Under **Artifacts**, choose **StrawVerse-Apple-Silicon** for an M-series Mac, or **StrawVerse-Intel** for an Intel Mac.
4. Extract the downloaded GitHub artifact ZIP (it contains only the DMG), open the DMG, and drag StrawVerse into Applications.

GitHub may require you to sign in before downloading workflow artifacts.

## Notes

- The apps are **ad-hoc code signed but not Apple notarized**, so macOS Gatekeeper may block the first launch. The hosted build verifies signature integrity, but an ad-hoc signature does not establish an Apple-trusted publisher. If you trust the source, check **System Settings → Privacy & Security** for **Open Anyway**. Do **not** disable Gatekeeper system-wide.
- If macOS reports that the app is *damaged*, do not assume that proves corruption, but also do not bypass a failed integrity check blindly. Re-download the newest successful build and review the build provenance. If the integrity check passed and macOS still blocks the app because it was downloaded from the internet, removal of the quarantine attribute **for this app only** can be considered by the user who trusts the code. Proper Developer ID signing and notarization remain the friction-free solution.
- MPV 0.41.0 and the project's FFmpeg dependency are placed **inside the app bundle**. No separate media programs are needed.
- Automatic macOS updates are not offered because the upstream release feed does not publish compatible Mac packages; download fresh builds from this fork instead.
- This is a first macOS port and remains **untested on an end-user Mac**. The workflow verifies packaging and binary execution on GitHub's Mac runners, but user-facing playback/download behavior still needs testing.
- The bundled Intel MPV targets macOS 15 or later; the Apple Silicon MPV binary targets macOS 14 or later.

## Development / licensing

Code changes and the build workflow are part of this fork. The upstream project's [GPL-3.0 license](LICENSE) continues to apply. MPV and FFmpeg have their own licenses; review them when redistributing the installers.

[Original StrawVerse](https://github.com/TheYogMehta/StrawVerse)
