---
type: rule
state: current
updated: 2026-11-16
area: principles
applies: always
summary: "The ideas every rule follows from"
---

# Principles

Every rule in this template follows from a handful of ideas. When a situation is not covered,
decide by these.

## Decision

1. **One home for every fact.** Status, results, configuration, dependencies and paths each
   live in exactly one place; everything else points there or is generated from it.
2. **Status lives with the thing it describes.** A doc states its own status in its header; a
   line of work states its status in its charter. Lists of status are generated, never typed.
3. **Rules before results.** Every analysis step has its rules written down before it loads an
   outcome, and changes to them are logged with a date and a reason.
4. **Names never encode status or order.** A path says what a thing is, not whether it is
   current or where it falls in a sequence. Order comes from metadata (`step`, dates); status
   from metadata (`state`).
5. **Checks, not reminders.** A rule that matters is enforced by a hook or CI job; a rule only
   written down in prose is a wish.
6. **Small, explicit, removable.** Prefer plain modules and notebooks to frameworks; tag the
   tree before removing code; delete one-off scripts once they have run.
7. **Agents are readers too.** Instructions for coding agents are short, current and generated
   where they would otherwise go stale.

## Why

These are the lessons of a research project that ran through a retirement, a fork and two
successor lines: status copied by hand into five places drifted within days; folders named
after the project's history (`successors/`, `analysis/`) forced moves and link rewrites; a
batch-estimation framework and an experiments folder went unused and had to be removed; numbered
files collided between branches.

## How

Each rule doc in this folder states one decision, why it was taken, how to apply it (with the
template files that implement it), the choices it leaves to a project, and what checks it.

## Per-project choices

None.

## Checked by

`python template/scripts/docs.py --root . check` checks these rule docs themselves.
