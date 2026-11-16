"""The base class every data source subclasses."""
from __future__ import annotations

from .steps import Step, Target


class DataSource:
    ID: str = ""
    STEPS: tuple[Step, ...] = ()
    # (my step, prerequisite source id, its step); point prerequisites at PREPARE steps
    REQUIRES: tuple[tuple[Step, str, Step], ...] = ()

    def __init__(self, config: dict, override: bool = False):
        self.config, self.override = config, override

    def plan(self, step: Step) -> list[Target]:
        """The targets ``step`` would produce. Cheap and side-effect free."""
        return getattr(self, f"_plan_{step.value}")()

    def execute(self, step: Step, target: Target) -> bool:
        """Produce one target; skip it when complete unless overridden."""
        if self.is_complete(target) and not self.override:
            return True
        ok = getattr(self, f"_execute_{step.value}")(target)
        if ok:
            target.marker.parent.mkdir(parents=True, exist_ok=True)
            target.marker.touch()
        return ok

    @staticmethod
    def is_complete(target: Target) -> bool:
        return target.marker.exists()
