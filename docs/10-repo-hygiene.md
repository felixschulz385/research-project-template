# Repository hygiene

## `.gitignore` baseline

Start every new project's `.gitignore` from this set, adding project-specific
entries as needed:

```gitignore
# Data (regenerate via the pipeline; never commit bulk data)
/data
scratch_nobackup/

# Logs
/log
*.log

# Secrets and local-only config
**/secrets
*.local.yaml
.env.local

# Editor / agent artifacts
.vscode/
.codex
.claude/
.DS_Store

# Python build artifacts
__pycache__/
*.pyc
*.egg-info/
.pytest_cache/
.venv/

# Regeneratable analysis output (see 09-data-and-output-storage.md)
/output/analysis/
```

Carve back in, with a `!` negation and a comment explaining why, any
specific path that would otherwise be caught by a broad rule above but
must be tracked (e.g. a generated site under `output/webpage/` that is
tracked while its own build cache is not).

## License

Add a `LICENSE` file to the repository root explicitly — do not rely on
prose in the README to state licensing terms. Pick the license before the
first commit that adds real content, not retroactively.

## Project-specific decisions

The right answer to these two depends on the specific project rather than
being a fixed convention:

- **Published output site.** Only add `output/webpage/` plus its publishing
  CI workflow (see [`07-ci-and-hooks.md`](07-ci-and-hooks.md)) if there is
  an actual intended audience for a live rendered output. Do not scaffold
  this by default.
- **License choice.** MIT, a Creative Commons variant for written
  materials, or another license — pick based on what the project's outputs
  actually are (code vs. papers/figures) and any institutional
  requirements; state the choice in `LICENSE` and, if code and written
  materials need different licenses, say so explicitly in the README.
