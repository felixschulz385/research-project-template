# Analysis code and notebooks

## Analysis code

- **One specification module**, `src/analysis/spec.py`: the outcome, the fixed effects, the
  clusters, the sample, and the function that builds and caches the analysis panel. Every line
  imports it rather than restating the specification.
- **One module per line of work**, `src/analysis/<slug>*.py` (several for a long line, e.g.
  `<slug>_checks.py`, `<slug>_review.py`), each with a docstring naming its pre-spec. A module
  holds construction (no outcome), fits, rules and figures for its steps.
- **Shared helpers live once** (multiple-testing adjustment, region names, plotting style) in
  the line's base module or in `spec.py`; other modules import them.
- **No batch-estimation framework.** Fits run in plain Python (e.g. `pyfixest`), called from
  notebooks. A framework for configuring models in spreadsheets, submitting them as jobs and
  rendering tables was built once and removed unused; do not scaffold one.
- **Caches** of derived panels go under the git-ignored data root with a descriptive name
  (`_<slug>_<what>_<grid>.parquet`), built on first use.

## Notebooks

- **Location:** `output/notebooks/<slug>/`, numbered in run order across the project
  (`07_pollution.ipynb`, …). `output/notebooks/README.md` has one row per folder.
- **They are runs of record** and keep their outputs, except notebooks that read restricted data
  (stripped by the pre-commit hook).
- **They find the project root** by searching upward for `pyproject.toml`
  (`next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / 'pyproject.toml').exists())`),
  never by a fixed `../..`, so they run from their own folder and survive being moved.
- **Links to docs** in Markdown cells are relative to the notebook; the docs checker verifies
  them (`notebooks` in `docs/docs.toml`).
- **Execution:** `jupyter nbconvert --to notebook --execute --inplace <nb>` in the project
  environment; record long run times in the results page's reproduction section.
- **Exploration** that is not a run of record happens in a notebook in the line's folder and is
  deleted or promoted when the step is recorded. There is no `src/experiments/`.

## Figures

Figures are written by functions in the line's analysis module (not by notebook cells), to
`output/figures/<slug>/<name>.{pdf,png}`. Fix one style per project (journal column widths,
font, font size) in a single `style()` function and use it everywhere.
