"""Read the unified config and its local overrides once (template rule: docs/pipeline/configuration.md)."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml


def _merge(base: dict, over: dict) -> dict:
    out = dict(base)
    for k, v in over.items():
        out[k] = _merge(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else v
    return out


@dataclass
class RunContext:
    data_root: Path
    sources: dict = field(default_factory=dict)
    override: bool = False


def load(path: str | Path) -> RunContext:
    """The config at *path*, with ``<stem>.local.yaml`` next to it applied on top."""
    path = Path(path)
    cfg = yaml.safe_load(path.read_text()) or {}
    local = path.with_name(f"{path.stem}.local.yaml")
    if local.exists():
        cfg = _merge(cfg, yaml.safe_load(local.read_text()) or {})
    return RunContext(data_root=Path(cfg.get("data_root", "data_nobackup")),
                      sources=cfg.get("sources", {}))
