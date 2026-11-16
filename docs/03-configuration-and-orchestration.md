# Configuration and orchestration

## One unified configuration file

The project has exactly one configuration file format and, normally, one
default instance of it: `orchestration/configs/<project>.yaml`. Every
source, every domain handler, and the assembly/build step all read their
settings from this one file via `--config` (see
[`01-entrypoint-and-cli.md`](01-entrypoint-and-cli.md)'s `add_config_arg`).

Do not let per-source or per-module CLI flag defaults become a de facto
second configuration mechanism — a flag may *override* a config value for
one invocation, but the config file is where defaults live. If a value is
needed by more than one source or module, it belongs in the config file,
not copy-pasted as a matching default in each module's argparse setup.

Back the config file with a small typed config object (e.g. a
`SourceConfig`/`PipelineContext`-style dataclass pair: one object for
"this source's own settings," one for "the run's shared context" — data
root, grid/target parameters, override flags). Parse the YAML into these
objects once, near the top of the CLI dispatch path, and pass the objects
down — do not re-parse the YAML file independently in multiple places.

## `orchestration/` directory

```
orchestration/
├── configs/
│   ├── <project>.yaml        # the unified config
│   ├── slurm_jobs.yaml       # per-job-key Slurm resource specs
│   └── debug/                 # local override configs for debugging, not used in production runs
└── scripts/
    ├── <maintenance-task>.sh  # one-off / recurring maintenance scripts (cleanup, migration, rechunking)
    └── LOGGING.md             # notes on how orchestration scripts handle/redirect logs
```

## Slurm job specs

`orchestration/configs/slurm_jobs.yaml` has one entry per job key. A job
key is `<source>.<step>` (or `<source>.<step>.<phase>` for a source whose
step has sub-phases), plus dedicated keys for non-source jobs like the
assembly/build step (keyed per output granularity, e.g. per grid
resolution, if resource needs vary by that). Each entry specifies at least
time, memory, CPU count, and — if the cluster requires them — QOS and
partition. The CLI's `--slurm` flag (see
[`01-entrypoint-and-cli.md`](01-entrypoint-and-cli.md)) looks up the
relevant job key here to render the sbatch script; per-invocation
`--slurm-*` flags override the looked-up defaults for that one submission
only.

## Per-machine settings

Machine-specific values (the data root, scratch locations) go in
`orchestration/configs/<project>.local.yaml`, git-ignored, read on top of the unified config. The
unified config never hard-codes an absolute path.

## Local override configs

Debug/local config variants (`orchestration/configs/debug/`) exist for
iterating without touching the shared production config. Never let a
handler or source silently prefer a debug config over the one passed via
`--config` — the caller always states explicitly which config file it
wants.
