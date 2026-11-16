# <Project>

<One paragraph: the research question and why it matters.>

## Lines of work

Generated from each line's charter in [`docs/lines/`](docs/lines/):

<!-- docs:begin lines -->
| Line of work | State | Branch | Updated | Summary |
|---|---|---|---|---|
<!-- docs:end -->

## Quick start

```bash
conda env create -f environment.yml && conda activate <env>
pip install -e .
./.githooks/install.sh            # pre-commit: notebooks, restricted data, docs
python scripts/docs.py check      # documentation conventions
python -m src.cli data summary    # what the pipeline has built
```

Everything else is in [`docs/`](docs/README.md).
