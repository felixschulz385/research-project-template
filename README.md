# Research project template

A copier template and a set of rules for Python research projects: a data pipeline, analysis by
line of work, documentation that states its own status, and checks that keep it so.

```bash
pip install copier
copier copy gh:felixschulz385/research-project-template my-project   # asks a few questions
cd my-project && copier update                                        # later: pull template changes
```

## What is here

- **[`docs/`](docs/README.md): the rules.** One decision per file, grouped by concern
  (workflow, repository, pipeline, analysis, optional modules), each with the same sections:
  Decision, Why, How, Per-project choices, Checked by. Start with
  [`docs/principles.md`](docs/principles.md); the index has reading paths by task, and
  [`docs/choices.md`](docs/choices.md) collects every choice a new project makes.
- **[`template/`](template/): what copier renders** into a new project: the package skeleton
  (`src/<package>/`), the docs scaffold with its tool (`scripts/docs.py`), the git hooks, the CI
  workflow, `AGENTS.md` and `CLAUDE.md`, `environment.yml`, `pyproject.toml`. Options switch on
  the data pipeline, HPC/SLURM and restricted-data parts and choose the documentation profile
  (research or software).
- **[`copier.yml`](copier.yml): the questions.**

## Changing the template

- A change to a rule goes into its file in `docs/` (with `updated` bumped and a line in
  [`docs/changelog.md`](docs/changelog.md)), and into `template/` if it changes what is rendered.
- `python template/scripts/docs.py --root . index` regenerates the rule index and the list of
  choices; `… check` verifies them. The `Template` workflow also renders two configurations and
  runs each project's own checks (docs, ruff, pytest).
- Projects created from the template pick up changes with `copier update`.
