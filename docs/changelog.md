---
type: index
state: current
updated: 2026-11-16
summary: "What changed in the template, and why"
---

# Changelog

- **2026-11-16.** Rules regrouped by concern (workflow, repository, pipeline, analysis, modules)
  without numbers; every rule with the same sections and a header; the index and the list of
  per-project choices generated. The template is a copier template (`copier copy`,
  `copier update`). New: lines of work, pre-specification, documentation by line with a checker,
  agent instructions in `AGENTS.md`, analysis code and notebooks, optional modules (HPC,
  restricted data, geospatial). Changed: a named package under `src/<package>/` with a console
  script; `conda-lock.yml` as the lock; notebooks at `notebooks/<slug>/`; dated design records;
  pre-specs ordered by their `step` field; ruff in CI; test files never import each other;
  verification specified by behaviour, not file layout; SLURM moved to its module; no analysis
  batch framework and no `src/experiments/`. Learned from running the growth-and-temperature
  project through a retirement, a fork and two successor lines.
- **2026-09-09.** First version: eleven numbered specification files.
