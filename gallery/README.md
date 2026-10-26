# Gallery v0.2.0 — temporary Apple Silicon preview branch

This folder contains Gallery's **separate application source**, temporarily hosted in the StrawVerse-mac repository's `gallery/v0.2.0-preview` branch at the owner's request. It does **not** modify the existing StrawVerse application. The Gallery files live under `gallery/`; the temporary CI workflow lives at `.github/workflows/gallery-preview-macos.yml`.

## Download the Mac application without npm

1. Open the [Gallery workflow runs](https://github.com/zonetrooper90/StrawVerse-mac/actions/workflows/gallery-preview-macos.yml?query=branch%3Agallery%2Fv0.2.0-preview).
2. Open the successful **Gallery v0.2.0 | Apple Silicon preview** run for branch `gallery/v0.2.0-preview`.
3. Download its `Gallery-v0.2.0-Apple-Silicon` artifact. Unzip that artifact, then unzip `Gallery-v0.2.0-Apple-Silicon.zip` to obtain `Gallery.app`.
4. Move `Gallery.app` to `/Applications` or another folder and open it in Finder. Because this is unsigned and not notarized, macOS may require approving it in **System Settings → Privacy & Security → Open Anyway**. Do not disable Gatekeeper globally.

There is no requirement to install Node.js or npm on the testing Mac. All build steps run in GitHub Actions on an Apple Silicon macOS runner.

## What you can test

Gallery v0.2.0 is an **early, local-video-only preview** with the custom player controls, split timeline, three themes, demo anime pages and season selector. It allows local videos to be selected using a native picker, plus local VLC playback where VLC is installed. Streaming providers, production downloads and embedded MPV are **not implemented yet**.

The app uses a separate development bundle ID, `dev.gallery.anime`, and separate user settings, `~/Library/Application Support/GalleryAnime`. It must never modify StrawVerse settings, caches or application files.

## Branch policy

- Do not merge this temporary branch into `main` or `feature/native-macos-build`.
- Move the `gallery/` source into a new dedicated Gallery repository when one is created.
- The temporary workflow triggers on changes to this branch only.
- The Mac app is a development preview, not a signed public release.
