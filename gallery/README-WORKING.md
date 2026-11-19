# Gallery — clean development workspace

Active branch: `gallery/development-clean`. Previous verified branch `gallery/working-2026-11-10-coordinated-fades` and all original history are preserved.

- **Edit only approved authoritative fragments in `gallery/src/`**, never generated `Gallery-current.html` or `Gallery-development.html`.
- Verify the current immutable checkpoint and exact source assembly before any change; preserve old archives.
- Follow [WORKFLOW.md](WORKFLOW.md), [MAINTENANCE-GUIDE.md](MAINTENANCE-GUIDE.md), [src/README.md](src/README.md), approved decisions and current development state.
- Use the controlled publisher for approved changed HTML; require both independent checks before pinned HTML delivery. Documentation-only changes do not create a new checkpoint.

From repository root, verify without editing:

```sh
python3 gallery/tools/restore-checkpoint.py --verify-only
python3 gallery/tools/build-gallery.py --check
python3 - <<'PY'
from pathlib import Path
import hashlib, json
p=json.loads(Path('gallery/checkpoints/current.json').read_text())
b=Path('gallery/Gallery-current.html').read_bytes()
assert len(b)==p['bytes'] and hashlib.sha256(b).hexdigest()==p['sha256']
print('Current HTML matches immutable checkpoint:',p['sha256'])
PY
```

Preview using `python3 gallery/tools/build-gallery.py` (development) or `--mode full` (original artwork); output defaults to `gallery/dist/`. The compressed archive chunks are recovery snapshots, not editing inputs. Historical deliverables and native preview branch documentation remain separate. 
