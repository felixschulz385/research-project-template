# CLAUDE.md

Working notes for coding agents in this repository. Keep it to rules and pointers: status lives
in the docs (`docs/conventions.md`), and the State table below is generated from the line
charters. Update this file in the same commit as any change to the layout or rules below.

## State

Generated from the line charters (`docs/lines/<slug>/README.md`) by `python scripts/docs.py
index`; edit a charter, not this table. Each line's next step is in its charter.

<!-- docs:begin lines -->
| Line of work | State | Branch | Updated | Summary |
|---|---|---|---|---|
<!-- docs:end -->

- **Start of a session:** read the charter of the line you work on, then its `results.md`.
- **New work** starts as a new line: `python scripts/docs.py new line <slug>`, a branch
  `line/<slug>` from `main`, and a pre-spec (`new prespec <slug> <step>`) before anything runs.

## Hard rules

- **Restricted data** (<name the licensed or confidential sources>): nothing at record level in
  any commit: file contents, notebook outputs, figures, docs or commit messages. Figures that
  show restricted records go to `output/figures/restricted/` (git-ignored). Enforcement:
  `.githooks/` (configure `restricted-patterns.txt`).
- **Pre-specification:** every analysis block has rules (◇) written down before it runs; change
  them only through the pre-spec's change log, never after seeing a result the change could be
  fitted to (`docs/conventions.md`).
- Commit only when asked. On `main`, branch first for anything that is not documentation.

## Environment

- <cluster, login vs compute nodes, network limits, where large downloads run>
- **Python:** `<env>` (`environment.yml`). The data root (git-ignored) is resolved by
  `orchestration/configs/<project>.local.yaml`.

## Data pipeline

- Every new dataset is a module in `src/data/sources/`, registered in `registry.py`, with a
  config block and a page (`python scripts/docs.py new source <key>`).
- CLI: `python -m src.cli data run --source <key> --step fetch|prepare [--slurm]`.
- Cross-source inputs are read by artefact path, never by importing another source's class.
  Ordering goes in `REQUIRES`; a dependency points at a PREPARE step (a FETCH target is never
  "complete").

## Analysis

- **Specification:** `src/analysis/spec.py` (outcome, FE, clusters, sample). One module per line
  of work: `src/analysis/<slug>*.py`.
- **Notebooks:** `output/notebooks/<slug>/`; they find the project root by searching upward for
  `pyproject.toml` and keep their outputs (runs of record) unless they read restricted data.

## Docs conventions

The rules are in [`docs/conventions.md`](docs/conventions.md): docs by line of work, front
matter on every doc, generated tables (`python scripts/docs.py index`), `depends_on` for derived
docs, and `python scripts/docs.py check` in the pre-commit hook and CI.
