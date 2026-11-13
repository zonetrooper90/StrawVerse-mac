# Gallery source-first development

**Authoritative editable application source:** this directory, its ordered manifest and the original assets in `gallery/assets/`. The tracked standalone `gallery/Gallery-current.html` and `gallery/Gallery-development.html` are generated deliverables, not independent editing inputs. The immutable full HTML checkpoint remains the recovery and delivery authority.

- `Gallery.template.html`: HTML shell with style/script block tokens.
- `styles/`: 28 ordered CSS fragments, see [CSS source map](styles/README.md).
- `js/`: 44 ordered JavaScript fragments, see [JavaScript source map](js/README.md).
- `build-manifest.json`: ordered fragment paths. The builder concatenates bytes without separators, reordering or transformations.
- `gallery/assets/subtitle-preview/`: original unchanged PNGs, referenced by tokens in JavaScript.

No framework, module runtime, bundler, minification or native integration. CSS cascade and classic script execution order remain exact.

## Preview and verify

Run from the repository root with Python 3 (standard library only):

```sh
python3 gallery/tools/build-gallery.py
python3 gallery/tools/build-gallery.py --mode subtitle-preview
python3 gallery/tools/build-gallery.py --mode full
python3 gallery/tools/build-gallery.py --check
python3 gallery/tests/test_source_assembly.py
```

All preview commands now write only under `gallery/dist/` by default; `--output PATH` may select another nonprotected output. The default development preview uses solid scene colors; full and subtitle-preview embed the original PNGs. Do not commit incidental dist files. `--check` is read-only and requires both tracked deliverables and the full immutable checkpoint to agree with the sources.

## Approved source changes

Verify the existing source, generated HTML and immutable archive before editing. Edit only the relevant files in `src/` (assets require explicit separate approval). New controlled publisher requests patch these files with exact baseline guards; they must not write generated HTML, assets or checkpoint files. The publisher builds both deliverables explicitly:

```sh
python3 gallery/tools/build-gallery.py --write-deliverables
```

This command refuses a stale/tampered old full HTML, validates all build modes and writes only the two tracked deliverables. It does not update the immutable pointer. Run browser regressions; stage a new immutable checkpoint only for a changed full HTML; commit source, generated files, tests and checkpoint together. Require both independent read-only checks before delivery. For a byte-identical source reorganization, commit only the infrastructure/source change and require both checks; no new checkpoint. See `gallery/WORKFLOW.md`.

The former canonical-to-source synchronization command is retired. Historical request scripts remain unchanged and must never be rerun. M2 CSS fragmentation uses the ordered manifest and preserves the exact original cascade. M3 extracts shared JS utilities and data in place while preserving the exact classic script. M4 partitions feature blocks in place with exact reconstruction; M5 core fragmentation and behavioral changes require separate approval. Native branches and historical checkpoints remain untouched.
