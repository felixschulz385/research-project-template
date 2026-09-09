# Data and output storage

## What's tracked in git vs. gitignored

| Path | Tracked? | Why |
|---|---|---|
| `output/figures/`, `output/documents/`, `output/tables/`, `output/presentations/` | Tracked | Citable/shippable deliverables — figures, papers, tables, slides. |
| `output/analysis/` | Gitignored | Regeneratable model-run output (results, manifests, summaries) — reproducible from source + the pipeline, not archived. |
| `output/webpage/` (if present) | Tracked, except its own build artifacts | The site source is tracked; its generated `_site/`/cache directories are gitignored. |
| `/data` (raw + processed pipeline data) | Gitignored | Bulk data never belongs in git; regenerate via the pipeline or fetch from source. |
| `scratch_nobackup/` (or equivalent large-scratch dir) | Gitignored | Disposable working files (spill files, part files, temp extraction dirs). |
| `src/experiments/*.ipynb` | Tracked, but hook-checked | Exploratory notebooks are kept, but a pre-commit hook (see [`07-ci-and-hooks.md`](07-ci-and-hooks.md)) strips or blocks committed cell outputs unless the notebook is explicitly whitelisted. |

## Raw/processed data directory convention

All pipeline data lives under one gitignored root (`/data`, or a
project-specific name), laid out consistently across every source through
the single `layout.py` path-builder (see
[`02-source-pipeline-architecture.md`](02-source-pipeline-architecture.md)).
Pick one physical layout convention and state it in `layout.py`'s own
module docstring, e.g. a stage-name-first tree:

```
<data_root>/raw/<source>/...
<data_root>/prepared/<source>/<aggregation-bucket>/...
```

Whatever the chosen shape, every source must go through the same
convention — a source should never invent its own ad hoc subdirectory
naming under the data root.

## Scratch space

Bulky, disposable working files (database spill files, intermediate
Parquet part files, temporary extraction directories) go in a dedicated
large-scratch directory at the project root (e.g. `scratch_nobackup/`),
**not** the system temp directory (`/tmp`, `tempfile`'s default). On a
shared HPC cluster, a job's working directory is typically the project
directory itself, and `/tmp` there is often small and shared — writing
large spill files there risks `ENOSPC`/OOM failures that a
project-root scratch directory avoids. Make the scratch directory location
overridable via an environment variable (e.g.
`<PROJECT>_SCRATCH_DIR`) so a job can point it at a node-local fast disk
(`$TMPDIR`-equivalent) when the cluster provides one.

## Exploratory notebooks

`src/experiments/` is a flat, deliberately unmaintained space for
exploratory notebooks, one-off analysis scripts, and diagnostic images. It
is not refactored to match the maintained pipeline's conventions and is
not covered by the test suite. Keep it clearly separated from
`src/analysis/` (the maintained analysis pipeline) and `src/data/` (the
maintained data pipeline) — never let exploratory code get imported by
maintained code, and never let maintained code live inside
`src/experiments/` "temporarily."
