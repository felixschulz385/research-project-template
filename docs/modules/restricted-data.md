---
type: rule
state: current
updated: 2026-11-16
area: modules
applies: opt-in: restricted data
summary: "Licensed or confidential records never reach git: a hard rule in AGENTS.md, configured hooks, restricted/ folders"
---

# Restricted data

## Decision

If the project uses licensed or confidential data:

- **The rule** in `AGENTS.md`: nothing at record level in any commit: file contents, notebook
  outputs, figures, docs or commit messages. Aggregate results (estimates, counts, shares) are
  allowed.
- **Patterns:** `.githooks/restricted-patterns.txt` names the sources, their id columns and the
  words their file names use (regular expressions).
- **Folders:** figures or tables that show records go to a `restricted/` folder (git-ignored),
  e.g. `output/figures/restricted/`.
- **Notebooks** whose code matches a pattern are committed without outputs; a notebook that
  reaches the data indirectly (through an analysis module) gets a `!` line in the whitelist.
- Write the rule and the patterns **before the first commit that touches the data**.

## Why

The hooks are a backstop: they cannot read every file's content. In the source project, maps of
mine counts per grid cell reached history before the rule existed; the author chose not to
rewrite history, so the files remain in old commits.

## How

The restricted-data option fills `restricted-patterns.txt` from the answers and adds the rule to
`AGENTS.md`.

## Per-project choices

- The restricted sources and their patterns (copier asks).

## Checked by

`check-notebook-outputs.py` and `check-restricted.py` in the pre-commit hook.
