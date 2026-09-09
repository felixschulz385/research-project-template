# Research project template

This repository is a specification, not a runnable codebase: a fixed set of
structural decisions for a Python research-code project (data pipeline +
analysis), written so an agent scaffolding a new project can follow it
directly without asking which convention to use.

## How to use this

Before scaffolding a new project from this template, read every file in
[`docs/`](docs/) in order. Each file is the single source of truth for its
topic — if a decision is stated there, apply it as-is; do not re-derive or
re-litigate it. Where a file explicitly calls out a per-project choice
(clearly marked as such), make that choice and record it, rather than
picking a default silently.

Adapt naming (project name, domain names, source names) to the new project.
Do not adapt the structural decisions themselves unless the user of this
template explicitly asks for a deviation — and if so, update the relevant
`docs/*.md` file to reflect the new decision so it stays the one source of
truth for the next project too.

## Reading order

1. [`docs/01-entrypoint-and-cli.md`](docs/01-entrypoint-and-cli.md) — CLI entry point, command shape, Slurm/dependency-chain flags
2. [`docs/02-source-pipeline-architecture.md`](docs/02-source-pipeline-architecture.md) — the data-source base class, registry, plan/execute contract
3. [`docs/03-configuration-and-orchestration.md`](docs/03-configuration-and-orchestration.md) — unified config file, orchestration directory
4. [`docs/04-environment-and-dependencies.md`](docs/04-environment-and-dependencies.md) — conda environment, packaging metadata
5. [`docs/05-testing.md`](docs/05-testing.md) — test tree layout and naming
6. [`docs/06-documentation-conventions.md`](docs/06-documentation-conventions.md) — design decision log, per-source docs, README scope
7. [`docs/07-ci-and-hooks.md`](docs/07-ci-and-hooks.md) — CI workflows, git hooks
8. [`docs/08-repository-skeleton.md`](docs/08-repository-skeleton.md) — the full directory tree
9. [`docs/09-data-and-output-storage.md`](docs/09-data-and-output-storage.md) — what's tracked in git vs. gitignored, and where
10. [`docs/10-repo-hygiene.md`](docs/10-repo-hygiene.md) — `.gitignore` contents, license, remaining per-project decisions
11. [`docs/11-verification.md`](docs/11-verification.md) — the `data summary`/`data verify` CLI verbs and the verification package backing them
