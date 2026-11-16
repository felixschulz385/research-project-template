---
type: rule
state: current
updated: 2026-11-16
area: workflow
applies: always
summary: "A line of work is one question with its own life cycle; its slug names its docs, branch, code and notebooks"
---

# Lines of work

## Decision

A **line of work** is one research question with its own life cycle: the original project, a
fork that tries a different identification, a successor that asks a neighbouring question. A
project is organised as lines from the start.

Every line has a **slug** (`heat-island`, `pollution`), fixed when it starts and never changed.
The slug names everything that belongs to the line:

| What | Where |
|---|---|
| Charter, pre-specs, results, notes | `docs/lines/<slug>/` |
| Branch | `line/<slug>` from `main`, merged into `main` when the line completes |
| Analysis code | `src/<package>/analysis/<slug>*.py` |
| Notebooks | `notebooks/<slug>/` |
| Figures | `output/figures/<slug>/` |

**The charter** (`docs/lines/<slug>/README.md`) is the only place that states a line's status:
question, why now, scope, state (`proposed → active → complete / stopped`), next step, branch.
Everything that lists lines (the docs index, the root README, the agent instructions) is
generated from the charters.

**Ideas** not yet started are recorded in `docs/ideas.md` with a sketch, the data, a critique
and a feasibility call; once an idea starts, its entry points to its line.

**Ending a line:** set the charter to `complete` or `stopped` with a one-line answer, set its
results page to `final`, merge the branch. Later corrections are dated notes, not edits to
recorded results.

## Why

Projects rarely stay one question: an instrument fails, a result suggests a follow-up, a
reviewer asks for a different outcome. A slug that never encodes status (no `successors/`,
`old-`, `archive/`) means nothing moves when a line closes.

## How

`python scripts/docs.py new line <slug> --title "…"` creates the charter from
`docs/templates/charter.md`. Create the branch `line/<slug>`; the first pre-spec comes before any
fit ([`prespecification.md`](prespecification.md)).

## Per-project choices

- The slug of the first line (copier asks for it).

## Checked by

`scripts/docs.py check`: every folder under `docs/lines/` has a charter, and every doc in it
carries the line's slug.
