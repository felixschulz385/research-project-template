---
type: rule
state: current
updated: 2026-11-16
area: pipeline
applies: pipeline projects
summary: "A console script <package> with verb-first, domain-scoped commands; parser and handlers in separate files; integer exit codes"
---

# Command line

## Decision

The entry point is a **console script named after the package**, declared in `pyproject.toml`
(`[project.scripts] <package> = "<package>.cli.main:main"`); `python -m <package>` runs the same
`main()` through `src/<package>/__main__.py`.

```
src/<package>/cli/
├── __init__.py
├── main.py            # build_parser(); registers each domain; dispatch; integer exit code
├── common.py          # setup_logging(), add_logging_args(), add_config_arg(), add_source_arg()
└── <domain>/
    ├── __init__.py    # register(subparsers)
    ├── commands.py    # argparse wiring
    └── handlers.py    # what the commands do
```

**Command shape:** `<package> <domain> <verb> [--source <name>] [flags]`. Domains are named after
the pipeline's stages (`data`, `assemble`). **Analysis is not a CLI domain:** it runs in
`<package>.analysis` modules called from notebooks. Add a domain only for work that runs
unattended as a batch job.

**Shared helpers** live once in `common.py` and are imported everywhere: logging setup (called
before parsing, so early errors show), `--log-level`/`--debug`, `--config` (defaulting to the
unified config, see [`configuration.md`](configuration.md)), `--source`.

**Prerequisites:** `--chain` runs unmet prerequisite steps first (resolved from each source's
`REQUIRES`); `--skip-dependency-check` bypasses the check deliberately. Without either, unmet
prerequisites fail with an itemised list naming the missing `(source, step)` pairs and both
escape hatches. Cluster submission flags are in [`../modules/hpc-slurm.md`](../modules/hpc-slurm.md).

**Errors:** `main()` returns 0 or 1; it catches `SystemExit` from handlers (keeping its code) and
any other exception (logging it and returning 1). No command ends in an unhandled traceback.

## Why

A named console script works from any directory and does not depend on `src` being importable
from the current one. Separate parser and handler files keep a growing domain readable.

## How

The template's pipeline option creates `cli/` with a `data` domain and a `list` verb.

## Per-project choices

- The domains (named after the project's real stages).

## Checked by

`tests/cli/test_cli_data_list.py` in the template runs the console entry point.
