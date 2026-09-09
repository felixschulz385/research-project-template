# CI and git hooks

## CI for anything published

Any project output that gets published somewhere (a rendered `docs/` site,
an output website, a package release) has a corresponding GitHub Actions
workflow under `.github/workflows/` that builds and publishes it on push —
not a manual "remember to run the build script" step. At minimum, run the
test suite in CI on every push/PR even if nothing else is published yet;
add a publishing workflow only once there is something to publish.

## Opt-in git hooks

`.githooks/` holds hook scripts plus an `install.sh` that points
`git config core.hooksPath` at this directory (or symlinks into
`.git/hooks/`). Hooks are **opt-in** — a fresh clone does not get them
automatically; the README's quick-start section includes running
`./.githooks/install.sh` as an explicit step.

Use a pre-commit hook to catch a real, recurring hygiene problem rather
than as a default scaffold item. The concrete case to guard against:
exploratory notebooks under `src/experiments/` accumulating committed cell
outputs (embedded images, execution counts, large output blobs) that
bloat repository history. A `check-notebook-outputs.py` +
`pre-commit` script pair, with a whitelist file for notebooks that are
allowed to keep outputs (e.g. a poster/visualization notebook whose
rendered output *is* the deliverable), covers this:

```
.githooks/
├── install.sh
├── pre-commit                        # dispatches to check-notebook-outputs.py
├── check-notebook-outputs.py
├── notebook-output-whitelist.txt     # notebooks allowed to keep outputs, one path per line
└── README.md                          # what the hook checks and how to bypass it when justified
```

Only add other hooks (formatting, linting) if the project has a concrete,
stated reason to enforce them at commit time rather than in CI.
