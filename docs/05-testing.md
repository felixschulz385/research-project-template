# Testing

## Directory structure mirrors `src/`

`tests/` mirrors `src/`'s package structure 1:1. A module at
`src/data/sources/glass.py` has its tests under `tests/data/sources/`; a
package at `src/data/sources/eog/` has its tests under
`tests/data/sources/eog/`. Do not group tests by test-type instead of by
source location (no top-level `tests/unit/`, `tests/integration/` split) —
location in `src/` is the organizing axis.

## State the `__init__.py` convention explicitly

Pick one of the following for the whole `tests/` tree and **state the
choice, with its reasoning, directly in `tests/conftest.py`** — do not
leave it implicit:

- **No `__init__.py` files anywhere in `tests/`.** Pytest then imports each
  test file by its own (unique) basename; there is no package hierarchy to
  keep in sync as directories are added. This is the default recommendation
  for a new project: it removes an entire category of upkeep (a forgotten
  `__init__.py` in a new test directory silently breaking nothing, since
  none are needed) at the cost of requiring every test file's basename to
  be unique across the whole tree.
- **`__init__.py` in every test directory**, making `tests/` an importable
  package tree. Choose this only if the project specifically needs
  package-relative imports between test modules, or non-unique test
  filenames across directories (e.g. every source's tests living in a
  same-named `test_core.py`).

Whichever is chosen, `tests/conftest.py`'s docstring or a top-of-file
comment must say which one, in one or two sentences, so a new contributor
adding a test directory doesn't have to guess whether a missing
`__init__.py` is deliberate.

## Running tests

`tests/conftest.py` should also state how to invoke the suite (typically:
run `pytest` from the project root so `from src.xxx import yyy` imports
resolve) and note the absence of a `pytest.ini`/`[tool.pytest.ini_options]`
section if rootdir detection is left to pytest's defaults rather than
configured explicitly.

## Test naming

Prefer scenario-descriptive test filenames over a strict 1:1 mirror of the
module under test — `test_gadm_prepare_completion.py`,
`test_glass_avhrr_fetch_remote_check.py` — rather than a single
`test_core.py` per source that accumulates every scenario for that source
as it grows. A test file name should tell a reader what behavior it
verifies without opening it.

## Fixtures

Add a `conftest.py` local to a test subpackage when several test files in
that subpackage share setup (e.g. `tests/data/assemble/conftest.py` for
assembly-specific fixtures) rather than lifting subpackage-specific
fixtures into the root `tests/conftest.py`. Keep the root `conftest.py`
limited to whatever every test in the tree needs (path setup, the
`__init__.py`-convention statement above).
