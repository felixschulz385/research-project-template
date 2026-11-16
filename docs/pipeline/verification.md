---
type: rule
state: current
updated: 2026-11-16
area: pipeline
applies: pipeline projects
summary: "data summary reports completeness from the registry; data verify checks correctness per source; both itemise failures"
---

# Verification

## Decision

Two verbs in the `data` domain:

- **`<package> data summary`**: for every registered source and each of its declared steps,
  whether the output is complete, from the source's own planned targets and completion markers.
  It iterates the registry; it never keeps its own list of sources.
- **`<package> data verify --source <name>`**: correctness beyond existence: expected columns or
  variables, value ranges, count bounds, and whether the output is stale against its inputs.

Behaviour that matters:

- a source with no verification rules reports **"no rules defined"**, never success;
- a stale output fails, even though the file exists;
- both exit non-zero with an itemised list of failures.

Where the code lives (one module or a package of several) is up to the project; start with one
module and split it when it grows.

## Why

"Does the file exist" and "is the file still right" are different questions, and only the second
one is worth a verb. The earlier version of this rule prescribed a six-file package that the
project it was written from never built; the behaviour is the decision, the layout is not.

## How

The pipeline option's `data` domain has `list`; `summary` and `verify` are added with the first
source.

## Per-project choices

- Which checks each source needs.

## Checked by

Tests of the verbs, once they exist.
