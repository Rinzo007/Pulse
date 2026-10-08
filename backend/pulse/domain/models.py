from dataclasses import dataclass, field
from enum import StrEnum


class TransitMode(StrEnum):
    BUS = "bus"
    TROLLEYBUS = "trolleybus"
    TRAM = "tram"
    METRO = "metro"
    RAIL = "rail"
    REGIONAL_RAIL = "regional_rail"


@dataclass(slots=True)
class Stop:
    id: str
    name: str
    lat: float
    lon: float
    wheelchair_accessible: bool = True


@dataclass(slots=True)
class Route:
    id: str
    name: str
    mode: TransitMode
    stop_ids: list[str] = field(default_factory=list)
    headway_seconds: int = 600
    capacity: int = 80
