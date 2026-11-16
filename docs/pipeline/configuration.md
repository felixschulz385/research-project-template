---
type: rule
state: current
updated: 2026-11-16
area: pipeline
applies: pipeline projects
summary: "One unified YAML config read once into typed objects; per-machine values in a git-ignored local file"
---

# Configuration

## Decision

- **One unified config**, `orchestration/configs/<package>.yaml`: one block per source and the
  settings of the build steps. Every command reads it through `--config`. A flag may override a
  value for one run; defaults never live in argparse.
- **Per-machine values** (the data root, scratch) go in `orchestration/configs/<package>.local.yaml`,
  git-ignored, read on top of the unified config. No absolute path in the unified config.
- **Typed objects.** The YAML is parsed once, near the top of dispatch, into a source-settings
  object and a run-context object (data root, override flags), which are passed down.
- **Debug configs** (`orchestration/configs/debug/`) exist for iteration; nothing prefers them
  silently over the `--config` the caller passed.

## Why

Defaults copied into several modules' argparse setups become a second, inconsistent
configuration. Absolute paths in a shared config break on the next machine.

## How

The pipeline option creates the config, an example local file and `<package>/config/`.

## Per-project choices

- Where the data root lives on each machine.

## Checked by

Review.
