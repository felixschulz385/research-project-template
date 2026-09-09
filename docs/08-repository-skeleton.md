# Repository skeleton

The full directory tree a new project starts from. Adapt names in angle
brackets (`<project>`, `<domain>`, `<source>`) to the actual project;
otherwise use this structure as-is.

```
.
├── README.md                       # short: purpose, quick start, install — see 06-documentation-conventions.md
├── LICENSE
├── environment.yml                 # conda — the dependency source of truth — see 04-environment-and-dependencies.md
├── pyproject.toml                  # build-backend + package discovery only, no dependency list
├── .env                            # PYTHONPATH=. if needed
├── .gitignore                      # see 10-repo-hygiene.md
├── .github/
│   └── workflows/                  # CI: tests at minimum; docs/output publishing if applicable
├── .githooks/
│   ├── install.sh
│   ├── pre-commit
│   └── check-notebook-outputs.py   # see 07-ci-and-hooks.md
├── docs/
│   ├── design/
│   │   ├── 00-overview.md          # numbered decision log — see 06-documentation-conventions.md
│   │   └── NN-<topic>.md
│   └── data/
│       ├── README.md               # index of every registered source
│       └── <source>/README.md      # one page per source
├── orchestration/
│   ├── configs/
│   │   ├── <project>.yaml          # unified config — see 03-configuration-and-orchestration.md
│   │   ├── slurm_jobs.yaml
│   │   └── debug/
│   └── scripts/
│       └── <maintenance-task>.sh
├── src/
│   ├── __init__.py
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── __main__.py             # `python -m src.cli` entry point — see 01-entrypoint-and-cli.md
│   │   ├── main.py
│   │   ├── common.py
│   │   └── <domain>/
│   │       ├── __init__.py
│   │       ├── commands.py
│   │       └── handlers.py
│   ├── config/                     # typed config objects (SourceConfig / PipelineContext-equivalent)
│   ├── data/
│   │   ├── __init__.py
│   │   ├── pipeline/                # config/context plumbing shared across sources
│   │   ├── sources/
│   │   │   ├── __init__.py
│   │   │   ├── base.py             # the DataSource base class — see 02-source-pipeline-architecture.md
│   │   │   ├── registry.py         # self-registration + lazy import
│   │   │   ├── layout.py           # the one module that builds every on-disk path
│   │   │   ├── steps.py            # PipelineStep enum, StepTarget, completion helpers
│   │   │   ├── verify.py
│   │   │   └── <source>.py | <source>/   # one file, promoted to a package as complexity requires
│   │   ├── common/                 # shared infra: fetch, hpc, dask/spark clients, geobox, etc.
│   │   └── assemble/                # the join/build step producing analysis-ready output
│   ├── analysis/
│   │   ├── core/
│   │   ├── execution/
│   │   ├── io/
│   │   ├── orchestration/
│   │   ├── rendering/
│   │   └── subsets/
│   ├── viz/                         # standalone plotting helpers, if the project needs them separately
│   └── experiments/                 # flat, unmaintained scratch space for exploratory notebooks
├── scripts/                        # maintenance/one-off scripts, not tied to one source
├── tests/                          # mirrors src/ 1:1 — see 05-testing.md
│   ├── conftest.py                 # states the __init__.py convention explicitly
│   ├── cli/
│   ├── data/
│   └── analysis/
└── output/
    ├── figures/                    # tracked
    ├── documents/                  # tracked
    ├── tables/                     # tracked
    ├── presentations/              # tracked
    └── analysis/                   # gitignored, regeneratable
```

## What each top-level directory is for

| Directory | Purpose |
|---|---|
| `docs/` | Decision log + per-source reference docs. See [`06-documentation-conventions.md`](06-documentation-conventions.md). |
| `orchestration/` | Configuration files and HPC/Slurm scripts. See [`03-configuration-and-orchestration.md`](03-configuration-and-orchestration.md). |
| `src/cli/` | The CLI package. See [`01-entrypoint-and-cli.md`](01-entrypoint-and-cli.md). |
| `src/data/sources/` | One module/package per pluggable data source. See [`02-source-pipeline-architecture.md`](02-source-pipeline-architecture.md). |
| `src/data/common/` | Infrastructure shared across sources (not source-specific logic). |
| `src/data/assemble/` | Joins prepared sources into the analysis-ready dataset. |
| `src/analysis/` | Estimation, orchestration, and rendering of analysis results. |
| `src/experiments/` | Exploratory notebooks, deliberately unmaintained and separate from the pipeline. |
| `scripts/` | Standalone maintenance/one-off scripts not owned by any one source. |
| `tests/` | Mirrors `src/`. See [`05-testing.md`](05-testing.md). |
| `output/` | Deliverables. See [`09-data-and-output-storage.md`](09-data-and-output-storage.md). |
