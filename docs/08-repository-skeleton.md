# Repository skeleton

The full directory tree a new project starts from. Names in angle brackets are adapted to the
project; otherwise use this structure as-is. Files marked ⧉ are copied from
[`../scaffold/`](../scaffold/).

```
.
├── README.md                       # ⧉ short: question, lines of work (generated), quick start
├── CLAUDE.md                       # ⧉ agent instructions — see 13-agent-instructions.md
├── LICENSE
├── environment.yml                 # conda: the dependency source of truth — see 04
├── pyproject.toml                  # build backend + package discovery only, no dependency list
├── .env                            # PYTHONPATH=. if needed
├── .gitignore                      # ⧉ see 10-repo-hygiene.md
├── .github/workflows/tests.yml     # ⧉ docs check + pytest — see 07-ci-and-hooks.md
├── .githooks/                      # ⧉ notebook outputs, restricted data, docs check — see 07
├── docs/                           # ⧉ see 06-documentation-conventions.md
│   ├── README.md                   #   entry point; generated tables
│   ├── conventions.md              #   the project's copy of the docs rules
│   ├── docs.toml                   #   doc types and states
│   ├── templates/                  #   one template per doc type
│   ├── ideas.md
│   ├── lines/<slug>/               #   one folder per line of work — see 12
│   │   ├── README.md               #     charter
│   │   ├── prespec-NN-<step>.md
│   │   ├── results.md
│   │   └── notes/
│   ├── data/
│   │   ├── README.md               #   index of every registered source
│   │   └── <source>/README.md
│   └── design/
│       ├── 00-overview.md
│       └── NN-<topic>.md
├── orchestration/
│   ├── configs/
│   │   ├── <project>.yaml          # the unified config — see 03
│   │   ├── <project>.local.yaml    # per-machine overrides (data root), git-ignored
│   │   ├── slurm_jobs.yaml
│   │   └── debug/
│   └── scripts/
│       ├── <task>.sh               # SLURM wrappers for maintenance, transfer-node fetches
│       └── LOGGING.md
├── scripts/
│   ├── docs.py                     # ⧉ the docs tool (check / index / new)
│   └── <tool>.py                   # standalone maintenance tools, each with a test
├── src/
│   ├── __init__.py
│   ├── cli/                        # `python -m src.cli` — see 01
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   ├── main.py
│   │   ├── common.py
│   │   └── <domain>/{__init__,commands,handlers}.py
│   ├── config/                     # typed config objects
│   ├── data/
│   │   ├── pipeline/               # config/context plumbing shared across sources
│   │   ├── sources/                # base.py, registry.py, layout.py, steps.py, <source>.py | <source>/ — see 02
│   │   ├── common/                 # shared infra: fetch, hpc, grid/geobox, ...
│   │   ├── assemble/               # the join/build step
│   │   └── verification/           # `data summary` / `data verify` — see 11
│   ├── analysis/
│   │   ├── spec.py                 # the specification and the analysis panel — see 14
│   │   └── <slug>*.py              # one module (or a few) per line of work
│   └── viz/                        # shared plotting helpers, if needed
├── tests/                          # mirrors src/ (and scripts/) — see 05
│   ├── conftest.py                 # ⧉ states the __init__.py convention
│   └── scripts/test_docs_tool.py   # ⧉
└── output/
    ├── notebooks/<slug>/           # ⧉ README; runs of record, one folder per line — see 14
    ├── figures/<slug>/             # tracked
    ├── tables/                     # tracked
    ├── documents/                  # tracked
    └── presentations/              # tracked
```

## What each top-level directory is for

| Directory | Purpose |
|---|---|
| `docs/` | Lines of work, data pages, design records, generated indexes. See [`06`](06-documentation-conventions.md), [`12`](12-lines-of-work-and-prespecification.md). |
| `orchestration/` | Configuration and HPC/SLURM scripts. See [`03`](03-configuration-and-orchestration.md). |
| `scripts/` | Standalone tools not owned by one source (the docs tool, maintenance). One-off migrations are deleted once done. |
| `src/cli/` | The CLI package. See [`01`](01-entrypoint-and-cli.md). |
| `src/data/` | Sources, shared infrastructure, assembly, verification. See [`02`](02-source-pipeline-architecture.md), [`11`](11-verification.md). |
| `src/analysis/` | The specification and one module per line of work. See [`14`](14-analysis-and-notebooks.md). |
| `tests/` | Mirrors `src/` and `scripts/`. See [`05`](05-testing.md). |
| `output/` | Notebooks of record and deliverables. See [`09`](09-data-and-output-storage.md). |

There is no `src/experiments/` and no analysis batch framework: exploration happens in a line's
notebook folder and is deleted or promoted ([`14`](14-analysis-and-notebooks.md)).
