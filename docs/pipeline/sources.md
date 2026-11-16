---
type: rule
state: current
updated: 2026-11-16
area: pipeline
applies: pipeline projects
summary: "One class per data source with declared steps and prerequisites, a plan/execute split, a lazy registry and one path module"
---

# Data sources

## Decision

**One base class.** Every source subclasses `DataSource` (`<package>/data/sources/base.py`):

```python
class DataSource:
    ID: str                                   # unique source id, e.g. "gadm"
    STEPS: tuple[Step, ...]                   # the stages this source implements
    REQUIRES: tuple[tuple[Step, str, Step], ...] = ()   # (my step, other source, its step)

    def plan(self, step) -> list[Target]: ...      # cheap, side-effect free
    def execute(self, step, target) -> bool: ...   # skips complete targets unless overridden
```

**Steps** are an enum named after the project's real stages (`FETCH`, `PREPARE`, …).

**Plan / execute split.** Planning lists the targets a step would produce (output path, inputs,
completion marker) without writing or downloading, so listing and dry runs need no duplicate
logic.

**Prerequisites** are declared by the source itself in `REQUIRES`; no hand-written dependency
graph exists elsewhere. A prerequisite points at a step that produces a complete, final artefact
(a PREPARE step): a FETCH target is never "complete" in the sense a consumer needs.

**Registry.** `registry.py` keeps one tuple of source module paths; each module registers itself
at import. Listing imports the light registration only; a source's heavy dependencies load only
when that source runs.

**One path module.** `layout.py` builds every on-disk path; no source constructs a path inline.

**File or package.** A source is one file until it needs internal structure (a scraper, a
multi-stage parser); then a package.

**Cross-source inputs** are read by artefact path through `layout.py`, never by importing another
source's class.

**Derived aggregations** of prepared data for one analysis (a region mean, a population-weighted
sum) live in that line's analysis module and cache their result; they are not new sources.

**A new source** comes with its config block and its data page
(`python scripts/docs.py new source <key>`).

## Why

Declared steps and prerequisites let one command answer "what would this do, and what is
missing?"; the path module keeps the on-disk tree changeable from one place.

## How

The pipeline option creates `base.py`, `steps.py`, `registry.py` and `layout.py` with working
minimal code.

## Per-project choices

- The step names.

## Checked by

The template's CLI test lists the registered sources.
