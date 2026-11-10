# Gallery — clean development workspace

Active branch: `gallery/development-clean`.
Previous verified branch `gallery/working-2026-11-10-coordinated-fades` and all original history are preserved.

- Edit **`gallery/Gallery-current.html`** after verifying it against `gallery/checkpoints/current.json`.
- Keep a NEW immutable checkpoint for each completed HTML change; old checkpoint folders are never edited.
- Use the read-only GitHub Actions checks for source integrity and browser regressions.
- Keep downloadable HTML delivery and exact GitHub commit provenance.

To verify this working checkout:

```sh
python3 gallery/tools/restore-checkpoint.py --verify-only
python3 - <<'PY'
from pathlib import Path
import hashlib, json
p=json.loads(Path('gallery/checkpoints/current.json').read_text())
b=Path('gallery/Gallery-current.html').read_bytes()
assert len(b)==p['bytes'] and hashlib.sha256(b).hexdigest()==p['sha256']
print('Current HTML matches immutable checkpoint:',p['sha256'])
PY
```

The compressed chunks under `gallery/checkpoints/` are retained for immutable backups and recovery; they are not the editing source. The standalone deliverable under `gallery/deliverables/` is a historical snapshot, not the current editing path. See `gallery/WORKFLOW.md`.
