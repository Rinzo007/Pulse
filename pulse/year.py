"""P0.3 deterministic year-calculation orchestration."""
from dataclasses import dataclass
import hashlib, json
from typing import Callable

STAGES = ("validate_network","service_schedule","demand_generation","trip_distribution","route_choice","mode_choice","capacity_crowding","aggregation","economics","model_validation")

@dataclass(frozen=True, slots=True)
class StageResult:
    name: str
    stage_version: str
    input_hash: str
    output_hash: str
    status: str
    duration_ms: int = 0

@dataclass(frozen=True, slots=True)
class StateSnapshot:
    state: dict
    state_hash: str

@dataclass(frozen=True, slots=True)
class YearReport:
    model_version: str
    package_version: str
    state_hash: str
    stages: tuple[StageResult, ...]
    result: dict


def _hash(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",",":"), ensure_ascii=False, default=str).encode()).hexdigest()


def snapshot(state: dict) -> StateSnapshot:
    frozen = json.loads(json.dumps(state, sort_keys=True, ensure_ascii=False, default=str))
    return StateSnapshot(frozen, _hash(frozen))


class YearCalculation:
    def __init__(self, model_version: str, package_version: str, stages: dict[str, Callable[[dict], dict]]):
        self.model_version, self.package_version, self.stages = model_version, package_version, stages

    def run(self, state: dict, *, cancel: Callable[[], bool] | None = None) -> YearReport:
        snap = snapshot(state); current = snap.state; results = []
        for name in STAGES:
            if cancel and cancel(): raise RuntimeError("YEAR-CANCELLED")
            fn = self.stages.get(name)
            if fn is None: raise RuntimeError(f"YEAR-STAGE-MISSING: {name}")
            inp = _hash(current); output = fn(current)
            if not isinstance(output, dict): raise TypeError(f"Stage {name} must return dict")
            results.append(StageResult(name, "1", inp, _hash(output), "success")); current = output
        return YearReport(self.model_version, self.package_version, snap.state_hash, tuple(results), current)
