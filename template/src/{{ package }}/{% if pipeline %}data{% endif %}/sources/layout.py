"""Every on-disk path the pipeline produces is built here, and only here.

Layout: ``<data_root>/raw/<source>/...`` and ``<data_root>/prepared/<source>/...``.
"""
from __future__ import annotations

from pathlib import Path


def raw(data_root: Path | str, source: str) -> Path:
    return Path(data_root) / "raw" / source


def prepared(data_root: Path | str, source: str) -> Path:
    return Path(data_root) / "prepared" / source
