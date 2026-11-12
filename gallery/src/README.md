# Gallery asset separation — transitional build milestone

The full canonical `gallery/Gallery-current.html` and its immutable checkpoint remain authoritative. This first reversible milestone extracts only the two original subtitle preview PNGs into `gallery/assets/subtitle-preview/` and creates a template with two exact replacement tokens. No artwork is edited or reencoded. No CSS/JS extraction or native app integration is performed yet.

Run from the repository root (Python 3 standard library only):

```sh
python3 gallery/tools/build-gallery.py
python3 gallery/tools/build-gallery.py --mode subtitle-preview
python3 gallery/tools/build-gallery.py --mode full
python3 gallery/tools/build-gallery.py --check
```

- Default development mode writes the standalone tracked `gallery/Gallery-development.html`; both shrine layers use solid CSS background colors, retaining their geometry and shared animation clock.
- Subtitle-preview mode writes `gallery/dist/Gallery-subtitle-preview.html`; full mode writes `gallery/dist/Gallery-full.html`. Both reconstruct the exact canonical HTML with the original PNGs embedded, offline and without network requests for those images. These are HTML prototypes, not native macOS builds.
- `--output PATH` selects a different output. Do not commit incidental dist builds.
- `--check` is read-only: compares both full modes to the canonical bytes and checkpoint SHA-256 and verifies the committed lightweight output exactly.
- Use the commit-pinned lightweight file page for download only after both existing verification workflows pass on the build commit; use the existing canonical permalink for artwork-enabled testing.

The template and development output are transitional derivatives, not a new authority. Do not independently edit them or run an old HTML publisher without first agreeing how to keep the template, canonical HTML, derived build and checkpoint synchronized. Future incremental CSS/JS extraction and a source-authority change require a separate agreed migration. Historical checkpoints and native app branches remain untouched.
