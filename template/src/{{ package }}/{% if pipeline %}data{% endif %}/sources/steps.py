"""The pipeline's stages and what a step plans."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class Step(str, Enum):
    """Named after the project's real stages; rename and extend as needed."""

    FETCH = "fetch"
    PREPARE = "prepare"


@dataclass
class Target:
    """One unit of work a step would produce: its output, its inputs, its completion marker."""

    output: Path
    inputs: list[Path] = field(default_factory=list)
    meta: dict = field(default_factory=dict)

    @property
    def marker(self) -> Path:
        return self.output.with_name(self.output.name + ".complete")
