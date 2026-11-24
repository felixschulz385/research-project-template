---
type: index
state: current
updated: 2026-11-23
summary: "Every choice a new project must make, collected from the rules' Per-project choices sections"
---

# Per-project choices

Generated from the "Per-project choices" section of every rule. Copier asks for the ones marked
in the rules; record the others in the project's first design record or first charter.

<!-- docs:begin collect section=per-project-choices dir=. recursive -->
**[Analysis code and notebooks](analysis/code-and-notebooks.md)**

- The figure style (journal, column widths, font).
- The estimation library.

**[Geospatial data](modules/geospatial.md)**

- The grid, its resolution and tile size.

**[HPC and SLURM](modules/hpc-slurm.md)**

- The cluster's partitions and QOS names, the transfer node, the proxy.

**[Restricted data](modules/restricted-data.md)**

- The restricted sources and their patterns (copier asks).

**[Command line](pipeline/cli.md)**

- The domains (named after the project's real stages).

**[Configuration](pipeline/configuration.md)**

- Where the data root lives on each machine.

**[Data sources](pipeline/sources.md)**

- The step names.

**[Verification](pipeline/verification.md)**

- Which checks each source needs.

**[Environment with pixi (planned)](repository/environment-pixi.md)**

- The platforms in `pixi.toml`.
- The Python version (copier asks; 3.11 or later).

**[Environment](repository/environment.md)**

- The platforms in the lock (`-p linux-64 -p osx-arm64` by default).
- The Python version (copier asks; 3.11 or later).

**[Hooks and CI](repository/hooks-and-ci.md)**

- The ruff rule set (`[tool.ruff.lint] select` in `pyproject.toml`; the template selects
  pyflakes, the import-related and syntax-error rules, and isort).

**[Repository layout](repository/layout.md)**

- The package name (copier asks; a valid Python identifier).
- Whether the project has a data pipeline (copier asks).

**[Storage and hygiene](repository/storage-and-hygiene.md)**

- The license (copier asks: MIT, BSD-3-Clause, CC-BY-4.0 for written material, or none yet). If
  code and writing need different licenses, say so in the README.
- Whether a published output site exists (`output/webpage/` plus a publishing workflow).

**[Agent instructions](workflow/agent-instructions.md)**

- The hard rules that apply (restricted data, if any) and the environment notes.

**[Agent skills](workflow/agent-skills.md)**

- Additional project-specific skills under `.agents/skills/` (for example, domain-specific build
  or submission procedures).

**[Documentation](workflow/documentation.md)**

- The documentation profile: `research` or `software` (copier asks). A project may add types in
  `docs/docs.toml`; the order of the types is the reading order of the tables.

**[Lines of work](workflow/lines-of-work.md)**

- The slug of the first line (copier asks for it).

**[Pre-specification](workflow/prespecification.md)**

- The multiple-testing correction used by default (Holm in the source project).
<!-- docs:end -->
