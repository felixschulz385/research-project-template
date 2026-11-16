# CI and git hooks

## CI

`.github/workflows/tests.yml` has two jobs on every push and pull request:

- **docs:** `python scripts/docs.py check` with a plain Python 3.11, no environment;
- **pytest:** the conda environment from `environment.yml` (micromamba), then `pytest -q` from
  the repository root.

Anything published (a rendered site, a package release) gets its own workflow that builds and
publishes on push. Add it only once there is something to publish.

## Opt-in git hooks

`.githooks/` holds the hooks and an `install.sh` that sets `git config core.hooksPath
.githooks`. Hooks are opt-in: a fresh clone does not get them, so the README's quick start runs
`./.githooks/install.sh`. All checks need only the Python standard library (3.11+), so they
run outside the project environment.

```
.githooks/
├── install.sh
├── pre-commit                      # runs the three checks below
├── check-notebook-outputs.py
├── check-restricted.py
├── notebook-output-whitelist.txt   # notebooks allowed to keep outputs ('!' re-blocks)
├── restricted-patterns.txt         # regexes naming restricted sources, ids, file words
├── restricted-allowlist.txt        # data files known to hold only aggregate results
└── README.md                       # what each check blocks and how to fix it
```

| Check | Blocks |
|---|---|
| `check-notebook-outputs.py` | outputs in staged notebooks that are not whitelisted, and in any notebook whose code matches `restricted-patterns.txt`. Notebooks under `output/notebooks/` are runs of record and are whitelisted by default. |
| `check-restricted.py` | staged files under a `restricted/` directory, data files (csv, parquet, …) unless allow-listed, and figures or documents whose path matches `restricted-patterns.txt`. |
| `scripts/docs.py check` | the documentation conventions ([`06-documentation-conventions.md`](06-documentation-conventions.md)). |

## Restricted data

If a project uses licensed or confidential data, state the rule in the agent instructions
(nothing at record level in any commit: contents, notebook outputs, figures, docs, commit
messages), name the sources in `restricted-patterns.txt`, and send figures that show records to
`output/figures/restricted/` (git-ignored). The hooks are a backstop, not a guarantee: they
cannot read every file's content. Write the rule and the patterns before the first commit that
touches the data; a leak in history is expensive to undo.

Add other hooks (formatting, linting) only with a concrete reason to enforce them at commit time
rather than in CI.
