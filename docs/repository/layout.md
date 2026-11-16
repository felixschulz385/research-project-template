---
type: rule
state: current
updated: 2026-11-16
area: repository
applies: always
summary: "The directory tree: a real package under src/<package>/, notebooks at the top, docs by line of work"
---

# Repository layout

## Decision

```
.
├── README.md  AGENTS.md  CLAUDE.md  LICENSE  .gitignore  .copier-answers.yml
├── pyproject.toml                  # build backend, package discovery, console script, ruff
├── environment.yml                 # conda input; conda-lock.yml is the lock
├── .github/workflows/tests.yml     # docs, lint, tests
├── .githooks/                      # notebook outputs, restricted data, docs check
├── docs/                           # see workflow/documentation.md
├── src/<package>/
│   ├── __init__.py
│   ├── analysis/
│   │   ├── spec.py                 # the specification and the analysis panel
│   │   └── <slug>*.py              # one module (or a few) per line of work
│   ├── cli/                        # pipeline projects: `<package> <domain> <verb>`
│   ├── config/                     # pipeline projects: typed config objects
│   └── data/                       # pipeline projects: sources, common, assemble, verification
├── orchestration/                  # pipeline projects: configs/ (+ slurm, scripts/ with HPC)
├── scripts/                        # tools run again (docs.py); one-off scripts are deleted
├── tests/                          # mirrors src/<package>/ and scripts/
├── notebooks/<slug>/               # runs of record, one folder per line of work
└── output/
    ├── figures/<slug>/             # tracked deliverables
    ├── tables/
    ├── documents/
    └── presentations/
```

The package has the **project's name**, `src/<package>/`, installed editable
(`pip install -e .`) and imported as `from <package>.data import …`. Pipeline projects get a
console script, `<package>`, declared in `pyproject.toml`.

There is no `src/experiments/` and no analysis batch framework
([`../analysis/code-and-notebooks.md`](../analysis/code-and-notebooks.md)).

## Why

- A package literally named `src` works until two projects are installed side by side, and tools
  read `src/` as a layout folder, not a name. The src layout with a named package avoids both.
- Notebooks are code with outputs, not deliverables; at the top level they sit next to the code
  they call, and `output/` holds only what is shipped.
- An unmaintained experiments folder and a configurable batch framework were both built and
  removed unused in the source project.

## How

Copier creates the tree; directories marked "pipeline projects" appear only when the pipeline
option is on.

## Per-project choices

- The package name (copier asks; a valid Python identifier).
- Whether the project has a data pipeline (copier asks).

## Checked by

CI: `pytest` imports the package; `ruff check`; the docs check covers `docs/`, `notebooks/`
links and the generated tables.
