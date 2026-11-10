# Gallery Motion Lab — standalone UI experiments

This directory holds separate experiments for comparing page transitions. It is **not the Gallery application baseline**, and no app code or approved look/behavior changes are implied. The full Gallery baseline remains in `gallery/checkpoints/current.json`.

## Current experiment

- `current.json` identifies the latest motion-comparison experiment.
- `2026-11-10-motion-comparison/` is immutable and contains the full self-contained HTML plus its SHA-256 `manifest.json`.
- Experiment shows four independent styles with shared navigation and timing: Gentle Crossfade, Layered Drift, Soft Depth, Soft Reveal.
- Use `tests/test_motion_lab.py` to check animation triggering, reversible navigation, replay, focus mode, responsive layouts and reduced-motion support.
- No external assets, internet calls or image generation. The preview uses simple CSS gradients for artwork placeholders.

## Workflow

Review styles with the user before changing Gallery. Do not change the full-app current pointer when updating a **standalone** experiment. For a new experiment, create an immutable directory, update this experiment's `current.json`, commit, and verify its checksum and CI run.