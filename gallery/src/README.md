# Gallery transitional modular source — M1

The full canonical `gallery/Gallery-current.html` and its immutable checkpoint **remain authoritative**. The asset-separated source has now been split losslessly into:

- `Gallery.template.html`: HTML shell with one style-block and one classic-script-block token.
- `styles/gallery.css`: exact existing CSS block, including original whitespace and cascade order.
- `js/gallery.js`: exact existing classic JavaScript block, including original whitespace and execution order.
- `build-manifest.json`: explicit ordered fragment paths. The builder concatenates file bytes without separators or transformations.
- Original PNGs remain in `gallery/assets/subtitle-preview/`; the two image tokens remain in JavaScript.

No library, bundler, module runtime, minification, reformatting, code cleanup, native integration or change to either delivered HTML is part of M1.

Run from repository root (Python 3 standard library only):

```sh
python3 gallery/tools/build-gallery.py
python3 gallery/tools/build-gallery.py --mode subtitle-preview
python3 gallery/tools/build-gallery.py --mode full
python3 gallery/tools/build-gallery.py --check
python3 gallery/tests/test_source_assembly.py
```

Development writes the tracked `Gallery-development.html` with solid scene colors. Full and subtitle-preview write standalone HTML under `gallery/dist/` with original artwork. `--output PATH` overrides the output; do not commit incidental dist builds. `--check` verifies both full modes, checkpoint and committed lightweight output byte-for-byte, without writing.

## Canonical-first change workflow (transitional)

Do not independently edit derivative fragments while canonical HTML is authoritative. For a newly approved change, patch the checksum-verified canonical HTML; run:

```sh
python3 gallery/tools/build-gallery.py --sync-from-canonical
```

This regenerates the shell, single CSS/JS files and lightweight output from the canonical bytes, preserving the exact asset substitutions. The controlled publisher invokes it after the approved patch and stages all of `gallery/src/`. If a future request needs candidate outputs within the script, use the builder's `sync_from_canonical()` function; do not write the old monolithic template. The sync command never writes canonical HTML, assets or checkpoints; it validates assembly before writes and refuses multiple fragments. The checkpoint is updated only by the existing approved publisher/staging process, and both independent checks still must pass.

M2 CSS fragmentation needs a separately approved reversible synchronization strategy (explicit fragment boundaries or a different agreed canonical-first mechanism). The manifest already supports ordered multiple fragments, but M1 sync intentionally fails closed for that layout. Source-authority transition and JS module interfaces remain separate decisions. All historical checkpoints and native branches stay untouched.
