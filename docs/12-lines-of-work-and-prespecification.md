# Lines of work and pre-specification

How research is organised over time. The documentation that records it is in
[`06-documentation-conventions.md`](06-documentation-conventions.md); the files to start from
are in [`../scaffold/`](../scaffold/).

## Lines of work

A **line of work** is one research question with its own life cycle: the original project, a
fork that tries a different identification, a successor that asks a neighbouring question.
Projects rarely stay one line: an instrument fails, a result suggests a follow-up, a reviewer
asks for a different outcome. Treat each as a line from the start.

Every line has a **slug** (`heat-island`, `pollution`), fixed when the line starts and never
changed. The slug names everything that belongs to the line:

| What | Where |
|---|---|
| Charter, pre-specs, results, notes | `docs/lines/<slug>/` |
| Branch | `line/<slug>`, from `main`; merged into `main` when the line completes |
| Analysis code | `src/analysis/<slug>*.py` |
| Notebooks | `output/notebooks/<slug>/` |
| Figures | `output/figures/<slug>/` |

A slug never encodes status (no `successors/`, `archive/`, `old-`), so nothing moves when a line
closes. Start a line with `python scripts/docs.py new line <slug>`; record unstarted ideas in
`docs/ideas.md` and point them to their line once started.

**The charter** (`docs/lines/<slug>/README.md`) is the only place that states a line's status:
its question, why now, scope, state (`proposed → active → complete / stopped`), the next step
and the branch. Everything that lists lines (the docs index, the root README, the agent
instructions) is generated from the charters.

## Steps and pre-specs

A line runs as numbered **steps**. Each step has a **pre-spec**
(`docs/lines/<slug>/prespec-NN-<name>.md`) written and confirmed before anything that loads an
outcome runs. Its fixed sections:

0. **Decisions for the author:** each open choice, with a recommended option, the reasoning in
   plain language, and the decision once taken ("Decided YYYY-MM-DD: …").
1. **Questions**, block by block.
2. **Data:** samples, sources, years, anything built for the step.
3. **Specification:** outcome, regressors, fixed effects, clusters, sample, per block.
4. **◇ Rules:** for each claim, what must hold, at what threshold, after which multiple-testing
   correction, and how a result is labelled otherwise. Construction checks (◇ G…) come first
   and load no outcome.
5. **Outcomes:** filled in after the fits, with the numbers the rules use.
6. **Change log:** every change, dated, with its reason.

Its life cycle is `draft → confirmed → run → recorded` (or `withdrawn`).

**Discipline.**

- Change a rule only through the change log, with a date and a reason, and never after seeing a
  result the change could be fitted to.
- Construction checks that load no outcome may change construction rules; log them anyway.
- Implementation choices the pre-spec leaves open (Holm families, support thresholds, the
  reading of an ambiguous sentence) are logged **before the first fit**.
- A step written after earlier results were seen says so, and labels which blocks are
  confirmatory and which descriptive.
- Test code paths on a placebo outcome (random noise), so debugging never involves looking at
  real results.

## The record

`docs/lines/<slug>/results.md` is the record of the line: every step's outcome side by side,
what is supported, what is recorded but not a finding to build on, what is not supported,
limitations, next steps, reproduction. It summarises the pre-specs and adds no estimate of its
own.

Derived documents (a story outline for a paper, a slide narrative) declare
`depends_on: [results.md]`; the docs checker fails when the results page is newer, so both
change in the same commit.

## Ending a line

- Set the charter's state to `complete` or `stopped`, with a one-line summary of the answer.
- Set the results page to `final` when nothing more will be added; later corrections are dated
  notes, not edits to recorded results.
- Merge the branch into `main`. If code is removed in a cleanup afterwards, tag the tree first
  (`archive/YYYY-MM-<what>`), so it stays one checkout away.
