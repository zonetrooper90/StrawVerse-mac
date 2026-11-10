# Gallery — GitHub working checkpoint

This branch is a protected-by-workflow **development workspace** for Gallery. It is separate from `main`, `feature/native-macos-*`, and the original `gallery/development-archive`.

The canonical **current prototype** is the checkpoint referenced by [`gallery/checkpoints/current.json`](gallery/checkpoints/current.json).

Restore it from this checkout:

```sh
python3 gallery/tools/restore-checkpoint.py --output Gallery-current.html
```

Validate the committed archive without extracting an output:

```sh
python3 gallery/tools/restore-checkpoint.py --verify-only
```

The archive is gzip-compressed, base64-encoded and split into parts solely to transfer the exact, self-contained HTML reliably. Each part and the original HTML have independent SHA-256 hashes in the manifest. This is an **archived design/prototype build**; it is not yet merged into native Gallery runtime sources. Before new changes, **restore this exact baseline**, change it, test it, and commit a new immutable checkpoint plus an updated current pointer.

Mandatory process: [`gallery/WORKFLOW.md`](gallery/WORKFLOW.md).