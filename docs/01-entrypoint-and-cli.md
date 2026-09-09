# Entry point and CLI

## Entry point

The entry point is `python -m src.cli`. There is no `run.py` wrapper script
and no other top-level launcher.

`src/cli/` is a package, not a single module:

```
src/cli/
├── __init__.py
├── __main__.py        # `python -m src.cli` runs this — imports and calls main.main()
├── main.py             # build_parser(); registers each domain's subparser; dispatch
├── common.py           # setup_logging(), add_config_arg(), add_source_arg(), shared helpers
└── <domain>/
    ├── __init__.py
    ├── commands.py     # argparse wiring for this domain's subcommands
    └── handlers.py     # the actual dispatch logic the commands call into
```

`__main__.py` exists purely so `python -m src.cli` works
(`python -m <package>` runs that package's `__main__.py`) while the parser
construction and dispatch logic stay organized in `main.py` and the
per-domain modules. Keep `__main__.py` to an import and a `sys.exit(main())`
call — no logic of its own.

## Command shape

Verb-first, domain-scoped:

```
python -m src.cli <domain> <verb> [--source <name>] [flags...]
```

`main.py`'s `build_parser()` creates one top-level subparser per domain
(e.g. `data`, `assemble`, `analysis` — name domains after the project's
actual pipeline stages, not necessarily these three), each domain
registering its own subcommands via a `register(subparsers)` function that
`main.py` calls. Domains do not share a subparser tree beyond this
registration point.

Within a domain, `commands.py` builds the argparse subparsers and their
flags; `handlers.py` holds the functions those subcommands call. Do not
fold parser construction and dispatch logic into one file — keep the two
concerns in separate files even for a domain with only one or two verbs.

## Shared CLI helpers (`common.py`)

Define once, in `src/cli/common.py`, and import everywhere else — never
redefine any of the following in a domain module or a source module:

- `setup_logging(level="INFO", debug=False)` — configures the root logger
  once. Called at the very start of `main()`, before argument parsing, so
  early errors are visible; re-called once flags are known if `--log-level`/
  `--debug` change the effective level.
- `add_logging_args(parser)` — adds `--log-level` and `--debug` to a parser.
- `add_config_arg(parser, default=DEFAULT_PIPELINE_CONFIG)` — adds
  `--config`, defaulting to the project's one unified config file path (see
  [`03-configuration-and-orchestration.md`](03-configuration-and-orchestration.md)).
  Pass `default=None` to make `--config` required instead of defaulted.
- `add_source_arg(parser)` — adds a required `--source` argument whose help
  text says it names a source defined in the configuration file.

## Slurm submission flags

Any domain/verb that can run as a batch job supports:

- `--slurm` — instead of running locally, re-serialize the same argv (minus
  `--slurm` itself) into an sbatch script and submit it. Resource
  parameters (time/memory/CPUs/QOS/partition) come from one YAML file of
  per-job-key resource specs (see
  [`03-configuration-and-orchestration.md`](03-configuration-and-orchestration.md));
  expose `--slurm-time`/`--slurm-mem`/`--slurm-cpus`/`--slurm-qos`/
  `--slurm-partition` as optional CLI overrides of those defaults.
- `--dry-run` — print the sbatch command/script that would be submitted,
  without submitting it. Pairs with `--slurm`.
- `--chain` — before running the requested step, auto-run any unmet
  prerequisite steps first (in dependency order, resolved from each
  source's declared requirements — see
  [`02-source-pipeline-architecture.md`](02-source-pipeline-architecture.md)).
  Prerequisite steps always run **locally**, even when the originally
  requested step is submitted via `--slurm` — only the step the user
  actually asked for goes to Slurm.
- `--skip-dependency-check` — bypass the prerequisite check entirely and
  run even if prerequisites are unmet. An escape hatch for when the check
  is wrong or a partial rerun is intentional; use it deliberately, not as a
  default habit.

When prerequisites are unmet and neither `--chain` nor
`--skip-dependency-check` is given, fail with a clear, itemized list of what
is missing and how to fix it (name the missing `(source, step)` pairs and
mention both escape hatches in the error message).

## Error handling

`main()` returns an integer exit code (0 success, 1 error) rather than
raising past the top level. Catch `SystemExit` raised by handlers
(treat its code as the CLI's own) and catch any other `Exception` at the
top of `main()`, logging it and returning 1 — a single command should never
produce an unhandled traceback as its final output.
