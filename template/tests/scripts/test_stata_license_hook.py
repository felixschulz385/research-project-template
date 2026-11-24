"""Tests for the Stata licence pre-commit guard and notebook scrub tool (synthetic JSON only)."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _load_hook(name: str, filename: str):
    path = ROOT / ".githooks" / filename
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


check_mod = _load_hook("check_stata_license", "check-stata-license.py")
scrub_mod = _load_hook("scrub_stata_license", "scrub-stata-license.py")


def _synthetic_notebook(extra_licensee_lines: list[str] | None = None) -> dict:
    licensee_cont = (
        ["               Dept of Economics\n"]
        if extra_licensee_lines is None
        else extra_licensee_lines
    )
    banner = [
        "\n",
        "  ___  ____  ____  ____  ____ ®\n",
        " /__    /   ____/   /   ____/      Stata 18.0\n",
        "___/   /   /___/   /   /___/       MP—Parallel Edition\n",
        "\n",
        " Statistics and Data Science       Copyright 1985-2023 StataCorp LLC\n",
        "                                   College Station, Texas 77845 USA\n",
        "\n",
        "Stata license: Single-user 2-core  perpetual\n",
        "Serial number: 000000000000\n",
        "  Licensed to: Example University\n",
        *licensee_cont,
        "\n",
        "Notes:\n",
        "      1. Unicode is supported; see help unicode_advice.\n",
        "\n",
    ]
    return {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["# Synthetic notebook\n"],
            },
            {
                "cell_type": "code",
                "execution_count": 1,
                "metadata": {},
                "outputs": [{"name": "stdout", "output_type": "stream", "text": banner}],
                "source": ["start_stata()\n"],
            },
            {
                "cell_type": "code",
                "execution_count": 2,
                "metadata": {},
                "outputs": [
                    {
                        "name": "stdout",
                        "output_type": "stream",
                        "text": ["ATT = -0.051 (N = 71,574)\n"],
                    }
                ],
                "source": ["print('ATT = -0.051 (N = 71,574)')\n"],
            },
        ],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def test_guard_flags_before_scrub_and_passes_after():
    nb = _synthetic_notebook()
    assert check_mod.has_stata_license(nb) is True

    removed = scrub_mod.scrub_notebook(nb)
    assert removed == 4
    assert check_mod.has_stata_license(nb) is False

    text = nb["cells"][1]["outputs"][0]["text"]
    assert any("Stata 18.0" in ln for ln in text)
    assert any("College Station" in ln for ln in text)
    assert any("Notes:" in ln for ln in text)
    assert not any("Stata license:" in ln for ln in text)
    assert not any("Serial number:" in ln for ln in text)
    assert not any("Licensed to:" in ln for ln in text)
    assert not any("Example University" in ln for ln in text)
    assert not any("Dept of Economics" in ln for ln in text)
    assert nb["cells"][2]["outputs"][0]["text"] == ["ATT = -0.051 (N = 71,574)\n"]


def test_scrub_removes_two_indented_licensee_lines():
    nb = _synthetic_notebook(
        extra_licensee_lines=[
            "               Department of Economics\n",
            "               Example City\n",
        ]
    )
    removed = scrub_mod.scrub_notebook(nb)
    assert removed == 5
    assert check_mod.has_stata_license(nb) is False
    joined = "".join(nb["cells"][1]["outputs"][0]["text"])
    assert "Department of Economics" not in joined
    assert "Example City" not in joined
    assert "Notes:\n" in joined


def test_guard_is_case_insensitive_and_checks_display_data():
    nb = {
        "cells": [
            {
                "cell_type": "code",
                "outputs": [
                    {
                        "output_type": "display_data",
                        "data": {"text/plain": ["serial number: 123\n"]},
                    }
                ],
                "source": [],
            }
        ]
    }
    assert check_mod.has_stata_license(nb) is True
    assert scrub_mod.scrub_notebook(nb) == 1
    assert check_mod.has_stata_license(nb) is False


def test_scrub_file_roundtrip_and_idempotence(tmp_path: Path):
    nb_path = tmp_path / "sample.ipynb"
    nb = _synthetic_notebook()
    nb_path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    assert scrub_mod.scrub_file(nb_path) == 4
    raw = nb_path.read_text(encoding="utf-8")
    assert raw.endswith("\n")
    parsed = json.loads(raw)
    assert raw == json.dumps(parsed, indent=1, ensure_ascii=False) + "\n"
    assert check_mod.has_stata_license(parsed) is False

    # Second run is a no-op
    assert scrub_mod.scrub_file(nb_path) == 0
