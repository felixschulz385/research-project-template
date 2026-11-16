---
type: rule
state: current
updated: 2026-11-16
area: repository
applies: always
summary: "CI runs the docs check, ruff and pytest; opt-in git hooks block notebook outputs, restricted data and inconsistent docs"
---

# Hooks and CI

## Decision

**CI** (`.github/workflows/tests.yml`) on every push and pull request:

| Job | Runs |
|---|---|
| docs | `python scripts/docs.py check` (plain Python 3.11) |
| lint | `ruff check` (configured in `pyproject.toml`) |
| tests | the environment from `conda-lock.yml` (or `environment.yml`), then `pytest -q` |

Anything published (a site, a release) gets its own workflow, added once there is something to
publish.

**Git hooks** live in `.githooks/`, enabled once per clone with `./.githooks/install.sh` (opt-in,
since `core.hooksPath` is not cloned). `pre-commit` runs three standard-library checks:

| Check | Blocks | Configure |
|---|---|---|
| `check-notebook-outputs.py` | outputs in staged notebooks not whitelisted, and in any notebook whose code reads restricted data | `notebook-output-whitelist.txt` (`notebooks/*` keep outputs) |
| `check-restricted.py` | files under `restricted/`, data files, and figures named after restricted data | `restricted-patterns.txt`, `restricted-allowlist.txt` |
| `scripts/docs.py check` | the documentation conventions | `docs/docs.toml` |

Formatting is not enforced at commit time; `ruff format` may be run by hand.

## Why

Lint in CI catches dead imports and undefined names cheaply; the source project removed them by
hand in a cleanup. Hooks catch what CI would catch too late: restricted data that has reached
history is expensive to remove.

## How

The workflow, the hooks and the ruff configuration come from the template.

## Per-project choices

- The ruff rule set (`[tool.ruff.lint] select` in `pyproject.toml`; the template selects
  pyflakes, the import-related and syntax-error rules, and isort).

## Checked by

The hooks and CI themselves.
