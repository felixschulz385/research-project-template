# Data verification and completeness summary

## CLI verbs

Two verbs under the `data` domain, alongside `fetch`/`prepare`/`assemble`:

- `python -m src.cli data summary [--config ...]` — a completeness overview
  across **every** registered source: for each source, which of its
  declared pipeline steps have complete output. Takes no `--source` — it
  iterates the whole registry.
- `python -m src.cli data verify --source <name> [--config ...]` — deeper,
  per-source verification: schema conformance, expected variables, value
  ranges, row/tile-count sanity bounds. Goes beyond "does the output file
  exist" into "is the output actually correct."

Both verbs share one parser-configuration function so they can't drift
apart in accepted flags: implemented as a `configure_parser(parser,
include_action)` / `run(args)` pair in `src/data/verification/__main__.py`,
with the `data` domain's handler setting `args.action` to `"summary"` or
`"verify"` before dispatching into it, exactly as any other CLI verb
dispatches into its backing module (see
[`01-entrypoint-and-cli.md`](01-entrypoint-and-cli.md)).

## `src/data/verification/` package

```
src/data/verification/
├── __init__.py
├── __main__.py        # configure_parser(parser, include_action) + run(args) — dispatches summary vs. verify
├── core.py             # run_summary() / run_verify(source) — the two verbs' actual logic
├── checks.py           # check functions: existence, schema conformance, row/tile counts, value ranges
├── fingerprint.py       # content fingerprinting of an output artifact, to detect staleness
├── sources.py           # per-source verification rules: which checks apply to which source, expected values
└── constants.py
```

This package sits alongside `src/data/sources/` and `src/data/assemble/` —
a third first-class member of `src/data/`, not a subfolder of either.

## Completeness comes from the registry, never a second hand-maintained list

`data summary` iterates `registry.all_specs()` (see
[`02-source-pipeline-architecture.md`](02-source-pipeline-architecture.md))
and, for each source's declared `STEPS`, uses that source's own
`_plan_<step>()` targets and completion markers to determine whether output
is present. The verification package never maintains its own separate list
of "which sources exist and what stages they have" — that would be exactly
the two-places-to-update problem the registry pattern exists to avoid.
What `verification/` adds on top of the registry is *judgment about
correctness*, not a second record of *what exists*.

## Per-source verification rules

`sources.py` holds, per source id, the specific checks `data verify
--source <name>` runs beyond mere existence: expected columns/variables,
physical value ranges, row-count sanity bounds. Key these rules by the same
source `ID` the registry uses. A source with no rules registered yet is a
named, visible gap — `data verify --source <name>` must say plainly "no
verification rules defined for this source" rather than silently reporting
success with nothing actually checked.

## Fingerprinting

`fingerprint.py` computes a content fingerprint for a source's output at
verification time — a hash over key output columns/metadata, or a
combination of file mtimes/sizes/row counts, whichever is enough to detect
that the output no longer matches what its current inputs would produce.
`data verify` treats a stale fingerprint as a failure, not as a pass on the
grounds that a file happens to exist on disk — "does the file exist" and
"is the file still valid" are different questions, and only the second one
is what `verify` exists to answer.

## Exit behavior

Both verbs return a non-zero exit code and print an itemized list of
failures — not a bare "verification failed" — when something is wrong,
consistent with the error-reporting convention in
[`01-entrypoint-and-cli.md`](01-entrypoint-and-cli.md).
