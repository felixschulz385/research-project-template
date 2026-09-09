# Environment and dependencies

## Conda is the dependency source of truth

`environment.yml` (conda) declares every dependency the project needs and
is the one file to consult or update when adding a package. Research
pipelines with a geospatial/scientific stack (GDAL/PROJ/raster-and-vector
libraries, compiled numerical libraries) need conda-level binary
reproducibility that pip wheels don't guarantee as tightly.

Install flow, stated in the README's quick-start section:

```bash
conda env create -f environment.yml
conda activate <project-env-name>
pip install -e .
```

## `pyproject.toml` stays minimal

`pyproject.toml` exists only for build backend + package discovery
metadata — it does **not** carry a `dependencies = [...]` list:

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "<project>"
version = "0.1.0"
requires-python = ">=3.11"

[tool.setuptools.packages.find]
where = ["."]
include = ["src", "src.*"]
```

Never let a second, competing dependency list accumulate in
`pyproject.toml` or a stray `requirements.txt` — one file states what the
project depends on; if a legacy `requirements.txt` is kept around for some
other tool's benefit, treat it as generated output, not something to edit
by hand.

## Comment the environment file with its provenance

`environment.yml` must carry a comment block stating:

- what machine/OS/Python version it was captured from, and how (e.g.
  `conda list --explicit` on a specific machine, or hand-assembled);
- whether it has been verified against the actual test suite;
- **explicitly, if true**: that it is *not* a byte-exact dump of whatever
  environment production/HPC runs actually use, and what to reconcile it
  against (the HPC environment's own `conda list --explicit`, or a
  platform-specific lock file) before trusting it for HPC/production runs.

Do not present an unverified or partially-reconstructed environment file as
if it were authoritative — say plainly what it is and isn't.

## `.env`

A project-root `.env` file may set `PYTHONPATH=.` if the project relies on
running commands from the repository root without an editable install
resolving imports otherwise. Keep `.env` to environment variables only —
it is not a place for configuration values (those belong in the unified
YAML config, see
[`03-configuration-and-orchestration.md`](03-configuration-and-orchestration.md)).
