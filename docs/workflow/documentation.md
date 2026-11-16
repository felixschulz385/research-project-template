---
type: rule
state: current
updated: 2026-11-16
area: workflow
applies: always
summary: "Docs by line of work, a type and a state in every doc's header, generated tables, and a checker in the hook and CI"
---

# Documentation

## Decision

**Layout.**

```
docs/
  README.md            entry point; its tables are generated
  conventions.md       the project's copy of these rules
  docs.toml            doc types, their states, extra files, notebook folders
  templates/           one template per doc type
  ideas.md
  lines/<slug>/        charter README.md, prespec-<name>.md, results.md, outline.md, notes/
  data/<key>/README.md one page per data source (pipeline projects)
  design/              YYYY-MM-<topic>.md infrastructure decisions, plus overview.md
```

**Front matter on every doc:** `type`, `state`, `updated` (last change of substance),
`summary`, and `line` under `docs/lines/`; optionally `step`, `depends_on`, `note`, `branch`.

**Types** come from `docs/docs.toml`, in reading order:

| Profile | Types |
|---|---|
| research | charter, results, outline, prespec, literature, note, source, design, index |
| software | charter, spec, runbook, note, source, design, index |

**Generated tables** (`<!-- docs:begin lines -->`, `<!-- docs:begin docs dir=… -->`,
`<!-- docs:begin collect section=… -->`) in `docs/README.md`, each charter, the root README
and `AGENTS.md`. `python scripts/docs.py index` rewrites them; never type status into a table.

**Design records** are named `YYYY-MM-<topic>.md`: chronological, and two branches never collide
on a number. Code cites them by path, so they are never renamed. A superseded record gets a
`state`, a `note` and a dated banner; the new decision gets a new record.

**Data pages** describe what a dataset is, where each stage's output lands, its columns and its
caveats, written from code and configuration; a fact only a real run can confirm is marked
**needs live data**. Mechanics live in module docstrings, and local reasoning in comments next
to the code.

**Temporary notes** (a rework in flight, a handoff between agents) are `note`s in the line's
`notes/`; when done they become `record` or `superseded`. No loose `.md` files at the root.

**The root README** is a pitch: the question, the generated table of lines, a quick start.

## Why

Status written by hand into several places drifts within days; numbered files collide between
branches; folders named after history force moves. Metadata in the doc plus generated tables
gives one home for each fact, and the checker makes it hold.

## How

The template ships `scripts/docs.py` (check, index, new; standard library only),
`docs/docs.toml`, the templates for the chosen profile, and `docs/conventions.md`.

## Per-project choices

- The documentation profile: `research` or `software` (copier asks). A project may add types in
  `docs/docs.toml`; the order of the types is the reading order of the tables.

## Checked by

`python scripts/docs.py check` in the pre-commit hook and in CI: metadata, a charter per line,
relative links in docs and in notebook Markdown cells, `depends_on` staleness, generated tables.
