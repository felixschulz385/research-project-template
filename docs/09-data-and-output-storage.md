# Data and output storage

## What's tracked in git vs. gitignored

| Path | Tracked? | Why |
|---|---|---|
| `output/notebooks/<slug>/` | Tracked, with outputs | Runs of record. Notebooks that read restricted data are committed without outputs (pre-commit hook, see [`07-ci-and-hooks.md`](07-ci-and-hooks.md)). |
| `output/figures/`, `output/tables/`, `output/documents/`, `output/presentations/` | Tracked | Citable deliverables. |
| `output/figures/restricted/` (any `restricted/`) | Gitignored | Figures that show restricted records. |
| `output/webpage/` (if present) | Tracked, except its build artifacts | The site source is tracked; `_site/` and caches are not. |
| `<data_root>/` (`data_nobackup/`) | Gitignored | Raw and prepared pipeline data, derived analysis caches, literature PDFs (`literature/<topic>/`). Regenerate via the pipeline or fetch from source. |
| `scratch_nobackup/` | Gitignored | Disposable working files. |

## Raw/processed data directory convention

All pipeline data lives under one gitignored root (`data_nobackup/`, or a
project-specific name, resolved per machine by `orchestration/configs/<project>.local.yaml`), laid out consistently across every source through
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

## Exploratory work

There is no `src/experiments/`. Exploration happens in a notebook in the line's
`output/notebooks/<slug>/` folder; when the step is recorded, it is deleted or promoted into the
line's analysis module ([`14-analysis-and-notebooks.md`](14-analysis-and-notebooks.md)). An
unmaintained scratch folder accumulates code nobody can run and outputs nobody can trust.

## Literature

PDFs of the papers a line reads are kept (git-ignored) under
`<data_root>/literature/<topic>/`, named by a citation key that the line's `literature.md` uses.
