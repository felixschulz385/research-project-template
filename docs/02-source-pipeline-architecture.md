# Data-source pipeline architecture

## The base class

Every data source (or, more generally, every pluggable pipeline unit)
subclasses one abstract base class, e.g. `src/data/sources/base.py`:

```python
class DataSource:
    ID: str                                    # unique source id, e.g. "gadm"
    STEPS: tuple[PipelineStep, ...]             # which pipeline steps this source implements
    REQUIRES: tuple[tuple[PipelineStep, str, PipelineStep], ...] = ()
    #   (my_step, prerequisite_source_id, prerequisite_step) triples

    def _plan_<step>(self) -> list[StepTarget]: ...
    def _execute_<step>(self, target: StepTarget) -> bool: ...
```

Capabilities are declared as class attributes, not registered separately
elsewhere. A source that needs a piece of shared infrastructure (a Dask
client, an HPC push helper, credentials) gets it from a method on the base
class or a shared helper module — never duplicates that setup per source.

## Pipeline steps

Name the pipeline's stages explicitly as an enum (`PipelineStep.FETCH`,
`PREPARE`, `GRID`/`ASSEMBLE`, or whatever stages the project's actual
pipeline has — the names should match the project's real processing
stages, not be copied blindly). A source's `STEPS` tuple states which of
these stages it implements; not every source implements every stage (a
source with no automated acquisition step, for instance, only implements
the stages after data is placed manually).

## Plan / execute split

Each implemented step is split into two methods:

- `_plan_<step>()` — returns the list of `StepTarget`s this step *would*
  produce if run: `output_path`, `inputs` (the files/artifacts it reads),
  a completion marker convention, and any metadata a caller might need
  without doing the actual work. Planning must be cheap and side-effect
  free (no writes, no network calls) — it exists so a `data plan`/`data list`
  command can answer "what would running this do?" without running it.
- `_execute_<step>(target)` — does the actual work for one planned target,
  returning `True`/`False` for success. Checks `is_complete(target)` first
  and skips (returning `True`) unless an override flag forces a rerun.

Do not collapse this into a single `run()` method — the separation is what
makes dry-run/listing commands possible without duplicating logic.

## Prerequisites

A source states its own prerequisites via `REQUIRES`, as
`(my_step, prerequisite_source_id, prerequisite_step)` triples. Nothing
outside the source module needs to be updated when a source's dependencies
change — do not maintain a separate, hand-written dependency-graph module.
The CLI layer resolves `REQUIRES` transitively to build a `--chain`
execution order and to produce the "prerequisites not satisfied" error
message described in
[`01-entrypoint-and-cli.md`](01-entrypoint-and-cli.md).

## Registry

`src/data/sources/registry.py` holds a `SourceSpec` (id, aliases, module
path, class name, steps, requires) per source. Each source module calls
`registry.register(...)` at import time, at the bottom of its own file:

```python
registry.register(GadmSource.ID, __name__, GadmSource.__name__, GadmSource.STEPS)
```

The registry's own module never imports a source's implementation module
eagerly — `resolve()`/`all_specs()` only need every source module imported
once (to run its `register()` call), which is cheap; `load()`/`create()`
import a *specific* source's module only when that source is actually
requested, so the registry never pulls in a source's heavy dependencies
(a browser driver, a database client, a domain-specific SDK) as a side
effect of listing or planning.

Maintain the list of source modules to import for registration in one
place in the registry module (a tuple of dotted module paths), added to
one at a time as sources are implemented.

## File vs. package per source

Default to a single file per source: `src/data/sources/<name>.py`. Promote
it to a package, `src/data/sources/<name>/`, only once it actually needs
internal subdivision — e.g. a separate module per pipeline step, a nested
subsystem (a scraper, a multi-stage parser), or enough constants/schema
code to warrant their own files. Do not scaffold a package for a source
that doesn't need one yet; do not force a source that has grown a scraper
subsystem or several hundred lines back into one file either. Both shapes
coexist in the same project — the decision is per-source, made when the
source is written or when it outgrows a single file.

## Path construction

One module, `src/data/sources/layout.py`, owns every on-disk path the
pipeline produces. No source module constructs an output path inline —
every path is built by calling a function in `layout.py`. This is what
keeps the physical on-disk tree changeable from one place, and it is where
[`08-repository-skeleton.md`](08-repository-skeleton.md)'s data-directory
structure is actually implemented, not just documented.
