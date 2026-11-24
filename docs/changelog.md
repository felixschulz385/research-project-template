---
type: index
state: current
updated: 2026-11-24
summary: "What changed in the template, and why"
---

# Changelog

- **2026-11-24.** The `start-line` and `end-line` skills name the default branch from
  `AGENTS.md` instead of `main` (noise-pollution uses `master`). CI checks the skills of both
  rendered projects: the `.claude/skills` symlink, `name` equal to the folder, a non-empty
  `description`, and no leftover Jinja.
- **2026-11-24.** Added a Stata licence guard to `.githooks/` (`check-stata-license.py` in
  `pre-commit`, `scrub-stata-license.py` to strip licence lines from existing notebooks in place,
  and `tests/scripts/test_stata_license_hook.py`), and documented starting `pystata` with
  `config.init(edition, splash=False)` in `docs/repository/hooks-and-ci.md` and `AGENTS.md`.
  Learned in noise-pollution: Stata's startup banner printed the licence serial number into
  notebook outputs that reached a public repository.

- **2026-11-23.** Added Agent Skills in rendered projects (`.agents/skills/<name>/SKILL.md`,
  symlinked from `.claude/skills`, with `_preserve_symlinks: true` in `copier.yml` and an
  exception in `.gitignore`): `start-line`, `write-prespec` (research profile), `add-source`
  (pipeline projects), `end-line`, and `tidy-repo`. Documented the decision in
  `docs/workflow/agent-skills.md` and pointed `AGENTS.md` and `docs/repository/layout.md` to it.
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
