---
type: rule
state: current
updated: 2026-11-16
area: workflow
applies: research profile
summary: "Each step's rules are written and confirmed before it loads an outcome; changes go through a dated change log"
---

# Pre-specification

## Decision

A line runs as **steps**. Each step has a **pre-spec**, `docs/lines/<slug>/prespec-<name>.md`,
written and confirmed before anything that loads an outcome runs. Its `step` field orders it;
the file name does not. Its sections:

0. **Decisions for the author:** each open choice with a recommended option, the reasoning in
   plain language, and the decision once taken ("Decided YYYY-MM-DD: …").
1. **Questions**, block by block.
2. **Data:** samples, sources, years, anything built for the step.
3. **Specification:** outcome, regressors, fixed effects, clusters, sample.
4. **◇ Rules:** for each claim, what must hold, at what threshold, after which multiple-testing
   correction, and how a result is labelled otherwise. Construction checks (◇ G…) come first
   and load no outcome.
5. **Outcomes**, filled in after the fits.
6. **Change log**, dated.

Life cycle: `draft → confirmed → run → recorded` (or `withdrawn`).

**Discipline:**

- Change a rule only through the change log, with a date and a reason, and never after seeing a
  result the change could be fitted to. Checks that load no outcome may change construction
  rules; log them anyway.
- Log the implementation choices the pre-spec leaves open (multiple-testing families, support
  thresholds, how an ambiguous sentence is read) **before the first fit**.
- A step written after earlier results were seen says so and labels which blocks are
  confirmatory and which descriptive.
- Test code paths on a placebo outcome (random noise), so debugging never involves looking at
  real results.

**The record.** `docs/lines/<slug>/results.md` holds every step's outcome side by side: what is
supported, what is recorded but not to build on, what is not supported, limitations, next
steps, reproduction. It adds no estimate of its own. A derived doc (a story outline, a slide
narrative) declares `depends_on: [results.md]`.

## Why

Descriptive research with many specifications invites fitting the rules to the results. Rules
written first, labels decided in advance and a dated change log make the record auditable, by
the author as much as by a reader. Naming pre-specs by step number made "step 4" and
`prespec-04` drift apart once a step 0 was added; the `step` field orders them instead.

## How

`python scripts/docs.py new prespec <slug> <name>` creates `prespec-<name>.md` with the next
step number; `new results <slug>`, `new outline <slug>`.

## Per-project choices

- The multiple-testing correction used by default (Holm in the source project).

## Checked by

`scripts/docs.py check`: an outline older than its results page fails; generated tables order
pre-specs by `step`. Rule discipline itself is checked by review, not by code.
