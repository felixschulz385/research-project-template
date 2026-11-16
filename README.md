# Research project template

A fixed set of structural decisions for a Python research project (data pipeline, analysis,
documentation), written so a person or a coding agent scaffolding a new project can follow it
without asking which convention to use. It has two parts:

- **[`docs/`](docs/)**: the specification, one topic per file. Each file is the single source of
  truth for its topic.
- **[`scaffold/`](scaffold/)**: files copied verbatim into a new project: the documentation
  scaffold (`docs/` with templates, conventions and `docs.toml`), the docs tool
  (`scripts/docs.py` and its test), the git hooks, the CI workflow, and skeletons of `README.md`,
  `CLAUDE.md`, `.gitignore`, `tests/conftest.py` and `output/notebooks/README.md`.

## How to use this

1. Read every file in `docs/` in order. Apply each decision as stated; where a file marks a
   per-project choice, make it and record it (in a design record or the first line's charter).
2. Copy `scaffold/` into the new repository's root, replace the `<placeholders>` in `README.md`
   and `CLAUDE.md`, and fill in `.githooks/restricted-patterns.txt` if the project uses restricted
   data.
3. `./.githooks/install.sh`, then `python scripts/docs.py new line <slug> --title "…"` for the
   first line of work, `python scripts/docs.py index`, and `python scripts/docs.py check`.

Adapt names (project, domains, sources, slugs) to the project. Do not adapt the structural
decisions unless the template's owner asks for a deviation; if so, update the relevant
`docs/*.md` (and `scaffold/`) so it stays the source of truth for the next project.

## Reading order

1. [`01-entrypoint-and-cli.md`](docs/01-entrypoint-and-cli.md): CLI entry point, command shape, Slurm and dependency-chain flags
2. [`02-source-pipeline-architecture.md`](docs/02-source-pipeline-architecture.md): the data-source base class, registry, plan/execute contract, cross-source inputs, limited networks
3. [`03-configuration-and-orchestration.md`](docs/03-configuration-and-orchestration.md): unified config, per-machine settings, orchestration directory
4. [`04-environment-and-dependencies.md`](docs/04-environment-and-dependencies.md): conda environment, packaging metadata, stdlib-only repository tools
5. [`05-testing.md`](docs/05-testing.md): test tree layout and naming
6. [`06-documentation-conventions.md`](docs/06-documentation-conventions.md): docs by line of work, doc types, front matter, generated tables, the checker, design records, data pages
7. [`07-ci-and-hooks.md`](docs/07-ci-and-hooks.md): CI jobs, git hooks, restricted data
8. [`08-repository-skeleton.md`](docs/08-repository-skeleton.md): the full directory tree
9. [`09-data-and-output-storage.md`](docs/09-data-and-output-storage.md): what is tracked in git and what is not, and where
10. [`10-repo-hygiene.md`](docs/10-repo-hygiene.md): `.gitignore`, cleaning up, license, remaining per-project decisions
11. [`11-verification.md`](docs/11-verification.md): the `data summary` / `data verify` verbs
12. [`12-lines-of-work-and-prespecification.md`](docs/12-lines-of-work-and-prespecification.md): lines of work, slugs, branches, pre-specs and their discipline, the results record, ending a line
13. [`13-agent-instructions.md`](docs/13-agent-instructions.md): what goes in `CLAUDE.md` and what stays out
14. [`14-analysis-and-notebooks.md`](docs/14-analysis-and-notebooks.md): the specification module, one module per line, notebooks of record, figures

## Changes

- **2026-11:** documentation by line of work with front matter, generated tables and a checker
  (`scaffold/scripts/docs.py`); pre-specification and lines of work (12); agent instructions
  (13); analysis code and notebooks (14); restricted-data hooks; the analysis batch framework
  and `src/experiments/` removed from the skeleton; CI checks the docs. Learned from running the
  growth-and-temperature project through a retirement, a fork and two successors.
- **2026-09:** first version.
