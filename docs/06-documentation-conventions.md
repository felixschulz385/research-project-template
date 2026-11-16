# Documentation conventions

The documentation is organised by **line of work** (see
[`12-lines-of-work-and-prespecification.md`](12-lines-of-work-and-prespecification.md)), every
doc has a **type** and **states its own status** in a front-matter header, and every index or
status table is **generated** from those headers by `scripts/docs.py`, which also checks them in
the pre-commit hook and in CI. The files to copy are in [`../scaffold/`](../scaffold/): the tool,
its configuration, one template per doc type, and `docs/conventions.md`, the project-side copy
of these rules.

Why: status written by hand into several places (README, an index table, the agent
instructions, the doc itself) drifts within days, and folders named after a project's history
(`successors/`, `analysis/`) force moves and link rewrites every time the history changes.

## Root `README.md` stays short

A pitch, not a manual: the research question, the generated table of lines of work, a short
quick start (install, hooks, one or two commands), and a link into `docs/`. Exhaustive CLI
usage, per-source instructions and architectural reasoning go into `docs/`.

## Layout

```
docs/
  README.md            entry point; its tables are generated
  conventions.md       the project's copy of these rules
  docs.toml            doc types and their states, extra files, notebook folders
  templates/           one template per doc type
  ideas.md             unscheduled ideas; each points to its line once started
  lines/<slug>/        one folder per line of work
    README.md          the charter (the line's only status)
    prespec-NN-<step>.md
    results.md         the record
    outline.md         (optional) the story, derived from results.md
    literature.md      (optional)
    notes/             dated notes: checks, plans, data options, handoffs
  data/<key>/README.md one page per data source
  design/NN-<topic>.md numbered infrastructure decisions
```

## Doc types and states

| Type | Where | States |
|---|---|---|
| charter | `lines/<slug>/README.md` | proposed → active → complete / stopped |
| results | `lines/<slug>/results.md` | current → final |
| outline | `lines/<slug>/outline.md` | current → final |
| prespec | `lines/<slug>/prespec-NN-*.md` | draft → confirmed → run → recorded (or withdrawn) |
| literature | `lines/<slug>/literature.md` | current → final |
| note | `lines/<slug>/notes/*.md`, or next to what it documents | current → record / superseded |
| source | `data/<key>/README.md` | current / superseded |
| design | `design/NN-*.md` | proposed → current / implemented → historical / superseded |
| index | navigation pages, `conventions.md`, `ideas.md` | current |

The types, their states and their order (which is the reading order of the generated tables)
are configured in `docs/docs.toml`; a project may add types there.

## Front matter

```yaml
---
type: prespec
state: recorded
updated: 2026-01-31          # last change of substance
line: example                # required under docs/lines/<slug>/
summary: "One line: what it is, or what came out"
step: 4                      # optional (prespec)
depends_on: [results.md]     # optional: docs this one is derived from
note: "…"                    # optional qualifier shown next to the state
branch: line/example         # charter
---
```

## Generated tables

```markdown
<!-- docs:begin lines -->                         one row per line (from the charters)
<!-- docs:begin docs dir=design -->               one row per doc in a folder
<!-- docs:begin docs dir=data recursive sort=path -->
<!-- docs:end -->
```

`python scripts/docs.py index` rewrites them; `check` fails if one is out of date. Put them in
`docs/README.md`, each charter, the root README and the agent instructions. Never type status
into a table.

## The checker

`python scripts/docs.py check` (standard library, Python 3.11+) fails on missing or invalid
metadata, a line folder without a charter, a broken relative link (in `docs/`, the extra files,
and notebook Markdown cells), a doc older than a doc it `depends_on`, and an out-of-date
generated table. `python scripts/docs.py new <kind> …` starts a doc from its template.

## Design records

For any nontrivial architectural decision (a storage format, a grid system, a rework, a
migration), a numbered record `docs/design/NN-<topic>.md`: the decision, the reasoning, the
rejected alternatives, the consequences. Code cites them by path, so they are **never
renumbered or renamed**. The log is history, not a living spec: when a decision is superseded,
write a new record and set the old one's `state` (with a `note`, and a dated banner under its
title). The current truth lives in code, module docstrings and the data pages.

## Data pages

`docs/data/<key>/README.md` for every registered source, plus the index `docs/data/README.md`
(module, steps, prerequisites, config keys, sourced from the registry and the config). Each page
covers what the dataset is, where each stage's output lands (per the path module), its columns,
and its caveats. They are written from code and configuration; a fact only a real run can
confirm (coverage, counts, value ranges, sizes) is marked **needs live data** until confirmed.

## Local reasoning stays in code

Reasoning that concerns one module (why a function does something non-obvious, which bug a line
prevents) goes in that module's docstring or a comment, not in `docs/`. Mechanics (how FETCH
discovers files, retry logic) live in docstrings; data pages describe what the data is.

## Temporary notes

An in-flight rework or a handoff between agents is a `note` in the relevant line's `notes/` (or
next to the design record it concerns). When the work lands, set it to `record`, or fold its
durable content into a design record and set it to `superseded`. No loose `.md` files at the
repository root.
