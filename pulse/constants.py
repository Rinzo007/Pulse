"""Single source of truth for Pulse Standard runtime constants."""

from dataclasses import dataclass
from typing import Final

from .model import MODEL_PROFILE, MODEL_VERSION


@dataclass(frozen=True, slots=True)
class Constant:
    id: str
    value: float
    unit: str
    source: str
    profile: str = MODEL_PROFILE
    version: int = 1


CONSTANTS: Final[dict[str, Constant]] = {
    "mode.wait.headway_multiplier": Constant(
        id="mode.wait.headway_multiplier", value=0.40, unit="dimensionless", source="W26|SB"
    ),
}


def get_constant(constant_id: str) -> Constant:
    try:
        return CONSTANTS[constant_id]
    except KeyError as exc:
        raise KeyError(f"Unknown Pulse Standard constant: {constant_id}") from exc


def constant_value(constant_id: str) -> float:
    return get_constant(constant_id).value


def registry_metadata() -> dict[str, object]:
    return {
        "profile": MODEL_PROFILE,
        "model_version": MODEL_VERSION,
        "constants": {
            key: {
                "id": item.id,
                "value": item.value,
                "unit": item.unit,
                "source": item.source,
                "profile": item.profile,
                "version": item.version,
            }
            for key, item in sorted(CONSTANTS.items())
        },
    }
