---
type: rule
state: current
updated: 2026-11-16
area: analysis
applies: always
summary: "One specification module, one analysis module per line, notebooks of record per line, figures written by code"
---

# Analysis code and notebooks

## Decision

**Code.**

- One **specification module**, `<package>/analysis/spec.py`: the outcome, fixed effects,
  clusters, sample, and the function that builds and caches the analysis panel. Lines import it
  instead of restating the specification.
- One **module per line of work**, `<package>/analysis/<slug>*.py` (several for a long line),
  each with a docstring naming its pre-spec. It holds construction (no outcome), fits, rules and
  figure functions for its steps.
- **Shared helpers live once** (multiple-testing adjustment, region names, plotting style), in
  `spec.py` or the line's base module.
- **No batch-estimation framework.** Fits run in plain Python (e.g. `pyfixest`) called from
  notebooks.
- **Caches** of derived panels go under the data root (`_<slug>_<what>.parquet`), built on first
  use.

**Notebooks.**

- `notebooks/<slug>/`, numbered in run order across the project; `notebooks/README.md` has one
  row per folder.
- They are **runs of record** and keep their outputs, unless they read restricted data.
- They find the project root by searching upward for `pyproject.toml`, never by a fixed `../..`.
- Links to docs in Markdown cells are relative to the notebook and checked by the docs tool.
- Execution: `jupyter nbconvert --to notebook --execute --inplace <nb>`; record long run times in
  the results page.
- Exploration happens in a notebook in the line's folder and is deleted or promoted when its step
  is recorded. There is no `src/experiments/`.

**Figures** are written by functions in the line's module (not by notebook cells) to
`output/figures/<slug>/<name>.{pdf,png}`, in one project-wide style set in a single function.

## Why

A framework for configuring models in spreadsheets, submitting them and rendering tables was
built once and removed unused; plain modules and notebooks were what the research used. Notebook
links broke silently when notebooks moved, until the docs tool checked them.

## How

The template creates `analysis/spec.py` and `notebooks/README.md`.

## Per-project choices

- The figure style (journal, column widths, font).
- The estimation library.

## Checked by

`scripts/docs.py check` (notebook links); `ruff check` (the modules).
