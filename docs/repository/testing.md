---
type: rule
state: current
updated: 2026-11-16
area: repository
applies: always
summary: "tests/ mirrors the package; no __init__.py; test files never import each other; shared setup is fixtures"
---

# Testing

## Decision

- **`tests/` mirrors the package:** `src/<package>/data/sources/gadm.py` is tested under
  `tests/data/sources/`; tools under `scripts/` are tested under `tests/scripts/`. No split by
  test kind (`unit/`, `integration/`).
- **No `__init__.py` anywhere in `tests/`.** Pytest imports each test file by its basename, so
  basenames must be unique across the tree. `tests/conftest.py` states this.
- **Test files never import each other, and never import from a `conftest.py`.** Shared setup is
  a fixture in the nearest `conftest.py`; a shared helper function is a fixture that returns the
  function.
- **Scenario-descriptive file names** (`test_gadm_prepare_completion.py`), not one `test_core.py`
  per module.
- Run `pytest` from the repository root, with the package installed editable.
- Tools under `scripts/` that are run again have tests (typically on a throwaway git repository
  in `tmp_path`); one-off scripts need none.

## Why

In the source project, test modules imported helpers with `from tests.data.assemble.conftest
import …`, which only works when `tests/` is a package; under the no-`__init__.py` rule the four
modules failed to collect, unnoticed for weeks.

## How

`tests/conftest.py` in the template states the convention.

## Per-project choices

None.

## Checked by

CI runs `pytest`; a collection error fails it.
