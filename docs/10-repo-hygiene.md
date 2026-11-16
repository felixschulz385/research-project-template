# Repository hygiene

## `.gitignore` baseline

Start every new project's `.gitignore` from this set (also in
[`../scaffold/.gitignore`](../scaffold/.gitignore)), adding project-specific
entries as needed:

```gitignore
# Data (regenerate via the pipeline; never commit bulk data)
/data_nobackup/
scratch_nobackup/

# Restricted data: figures and files that show restricted records
restricted/

# Logs
/log
*.log

# Secrets and local-only config
**/secrets
*.local.yaml
.env.local

# Editor / agent / OS artifacts (._* are macOS metadata files on network mounts)
.vscode/
.codex
.claude/
.DS_Store
._*

# Python build artifacts
__pycache__/
*.pyc
*.egg-info/
.pytest_cache/
.venv/
```

Carve back in, with a `!` negation and a comment explaining why, any
specific path that would otherwise be caught by a broad rule above but
must be tracked (e.g. a generated site under `output/webpage/` that is
tracked while its own build cache is not).

## Cleaning up

- **Tag before removing code.** Before deleting a framework, a folder of old outputs or a set of
  one-off scripts, tag the tree (`git tag -a archive/YYYY-MM-<what>`) and push the tag, so the
  removed code stays one checkout away. Say in the commit which tag holds it.
- **Delete one-off scripts once they have run.** A migration or a cleanup script that has done
  its job is noise for the next reader; keep only tools that are run again.
- **Status before cleanup.** A cleanup that touches docs runs `python scripts/docs.py check`
  afterwards; moved files keep their front matter, and every link must resolve.
- **macOS metadata.** Copying a repository through a Mac network mount leaves `._*` files, also
  inside `.git/` (git reports them as garbage). They are 4 KB AppleDouble files (magic bytes
  `00 05 16 07`) and safe to delete; ignore them in `.gitignore`.

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
