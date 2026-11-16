"""scripts/docs.py on a throwaway repository: check, index, new, staleness."""
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

TOOL = Path(__file__).resolve().parents[2] / "scripts" / "docs.py"
CONFIG = Path(__file__).resolve().parents[2] / "docs" / "docs.toml"
TEMPLATES = Path(__file__).resolve().parents[2] / "docs" / "templates"


def _run(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(repo / "scripts" / "docs.py"), *args],
                          cwd=repo, capture_output=True, text=True)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    (tmp_path / "scripts").mkdir()
    shutil.copy(TOOL, tmp_path / "scripts" / "docs.py")
    (tmp_path / "docs").mkdir()
    cfg = re.sub(r"extra = \[.*?\]\n", 'extra = ["README.md"]\n', CONFIG.read_text(), flags=re.S)
    (tmp_path / "docs" / "docs.toml").write_text(cfg)
    shutil.copytree(TEMPLATES, tmp_path / "docs" / "templates")
    (tmp_path / "README.md").write_text("# X\n\n<!-- docs:begin lines -->\n<!-- docs:end -->\n")
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    return tmp_path


def test_new_line_index_check(repo: Path):
    assert _run(repo, "new", "line", "demo", "--title", "Demo line").returncode == 0
    assert _run(repo, "new", "prespec", "demo", "first step").returncode == 0
    assert (repo / "docs/lines/demo/prespec-01-first-step.md").exists()
    assert _run(repo, "new", "results", "demo").returncode == 0
    assert _run(repo, "new", "outline", "demo").returncode == 0
    r = _run(repo, "check")
    assert r.returncode == 1 and "generated block out of date" in r.stdout
    assert _run(repo, "index").returncode == 0
    r = _run(repo, "check")
    assert r.returncode == 0, r.stdout
    readme = (repo / "README.md").read_text()
    assert "[Demo line](docs/lines/demo/)" in readme
    charter = (repo / "docs/lines/demo/README.md").read_text()
    assert "[prespec-01-first-step](prespec-01-first-step.md)" in charter


def test_check_catches_problems(repo: Path):
    _run(repo, "new", "line", "demo")
    _run(repo, "new", "results", "demo")
    _run(repo, "new", "outline", "demo")
    _run(repo, "index")
    res = repo / "docs/lines/demo/results.md"
    text = re.sub(r"^updated: .*$", "updated: 2999-01-01", res.read_text(), count=1, flags=re.M)
    res.write_text(text + "\n[gone](nowhere.md)\n")
    ch = repo / "docs/lines/demo/README.md"
    ch.write_text(ch.read_text().replace("state: proposed", "state: finished"))
    (repo / "docs/lines/orphan").mkdir()
    (repo / "docs/lines/orphan/x.md").write_text("# no front matter\n")
    out = _run(repo, "check").stdout
    assert "outline.md: stale" in out
    assert "broken link 'nowhere.md'" in out
    assert "state 'finished' not allowed for charter" in out
    assert "docs/lines/orphan: no charter" in out
    assert "orphan/x.md: no front matter" in out
