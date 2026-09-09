# Documentation conventions

## Root `README.md` stays short

The root `README.md` is a pitch, not a manual: research question/purpose,
a short quick-start (install + one or two example commands), and a link
into `docs/` for everything else. Do not let exhaustive CLI usage,
per-source workflow instructions, or architectural reasoning accumulate in
the root README — push all of that into `docs/` as described below. A
README that has grown past roughly one screen of prose plus a quick-start
block is a sign that detail belongs in `docs/` instead.

## `docs/design/`: a numbered decision log

For any nontrivial architectural decision — a storage format choice, a
coordinate/grid system choice, a rework of an existing subsystem, a
migration — write a numbered file:

```
docs/design/00-overview.md
docs/design/01-<topic>.md
docs/design/02-<topic>.md
...
```

Each design doc states:

1. **The decision** — what was chosen, stated as fact, not as a proposal.
2. **The reasoning** — why, including the concrete problem it solves.
3. **Rejected alternatives** — what else was considered and why it lost,
   so the reasoning doesn't have to be reconstructed from scratch if the
   same question resurfaces later.

`00-overview.md` ends with a "Document map" section linking to every other
design doc in the set, in reading order, so the whole decision history is
navigable from one entry point. Cross-link related docs to each other
directly (`See [`03-x.md`](03-x.md) for ...`) rather than only linking back
to the overview.

Treat this log as append-only history, not a living spec: once a decision
is superseded, add a new numbered doc recording the change and why,
rather than editing the old one to erase what used to be true. The
current, authoritative state of the system lives in code plus the
per-module docs described below — the design log is *why*, not *what is
true right now*.

## `docs/data/<source>/README.md`: one page per source

Every registered pipeline source (or, more generally, every registered
pluggable module) gets one documentation page:
`docs/data/<source>/README.md`, plus one index page,
`docs/data/README.md`, listing every source with its module path, the
pipeline steps it implements, its prerequisites, and its config key(s) —
sourced directly from each source's own `STEPS`/`REQUIRES` class
attributes and the registry, cross-checked against the config file, not
inferred from one or the other alone.

Each per-source page covers: what the source is, where each of its stages'
output lands on disk (per
[`02-source-pipeline-architecture.md`](02-source-pipeline-architecture.md)'s
path module), its output schema/variables, and known data-quality caveats
found in the code or config comments.

These pages are derived from reading code and configuration, not from
inspecting live data output. Any fact that can only be confirmed by
running the pipeline and looking at real output (actual date coverage,
row/tile counts, empirically observed value ranges, on-disk size) must be
marked explicitly, e.g.:

```
**TODO (needs live data):** actual row count once a full run completes.
```

Never state such a fact as if verified when it was only inferred from code.

## Ad hoc rework notes

A single root-level `.md` file documenting an in-flight rework or migration
(e.g. `some_subsystem_rework.md`) is acceptable as a temporary scratchpad
while that specific piece of work is active. Once it lands, either fold its
durable content into a `docs/design/NN-*.md` entry (if it recorded a real
decision) or delete it — do not let it sit at the repository root
indefinitely once the rework it describes is finished.

## Module-level docstrings carry local reasoning

For reasoning that's local to one module (why this function does something
non-obvious, what bug a particular line prevents, what an earlier version
did differently) prefer a comment or docstring in that file over a
prose paragraph in `docs/` — file-local reasoning should live next to the
code it explains so it can't drift out of sync unnoticed. Reserve
`docs/design/` for decisions that span multiple modules or files.
