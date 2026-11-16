---
type: rule
state: current
updated: 2026-11-16
area: repository
applies: always
summary: "environment.yml is the input, conda-lock.yml the reproducible lock; repository tools need only the standard library"
---

# Environment

## Decision

- **`environment.yml`** (conda) is the human-edited list of dependencies, the one file to change
  when adding a package. Its `pip:` section ends with `-e .`.
- **`conda-lock.yml`** is generated from it for every platform the project runs on and is what
  CI and new machines install:

  ```bash
  conda-lock lock -f environment.yml -p linux-64 -p osx-arm64
  conda-lock install -n <env> conda-lock.yml && conda activate <env> && pip install -e .
  ```

  Regenerate it in the same commit as any change to `environment.yml`.
- **`pyproject.toml`** carries build metadata, package discovery, the console script and tool
  configuration (ruff), never a dependency list.
- **Repository tools** (`scripts/docs.py`, the git hooks) use only the Python standard library
  (3.11+), so they run in a hook or CI job without the environment.
- **`.env`** holds environment variables only, never configuration values.

## Why

A geospatial or scientific stack needs conda-level binaries. A hand-written `environment.yml`
describes intent but not what ran: in the source project the HPC environment and the file
diverged, and the file had to carry a warning saying so. A lock file removes the gap instead of
documenting it. A hook that needs the project environment silently stops running when the
environment is not active.

## How

`environment.yml`, `pyproject.toml` and the CI workflow come from the template. The workflow
installs from `conda-lock.yml` when it exists and from `environment.yml` otherwise.

## Per-project choices

- The platforms in the lock (`-p linux-64 -p osx-arm64` by default).
- The Python version (copier asks; 3.11 or later).

## Checked by

CI installs from the lock and runs the tests.
