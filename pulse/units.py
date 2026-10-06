"""Small runtime unit contract used by Pulse Standard."""

from enum import StrEnum


class Unit(StrEnum):
    KM = "km"
    MIN = "min"
    KM_H = "km/h"
    PASSENGER = "passenger"
    PASSENGER_DAY = "passenger/day"
    PASSENGER_TRIP = "passenger/trip"
    CURRENCY = "currency"
    CURRENCY_PER_MIN = "currency/min"
    DIMENSIONLESS = "dimensionless"
    PASSENGER_PER_M2 = "passenger/m²"


def require_unit(actual: str, expected: Unit | str) -> None:
    expected_value = expected.value if isinstance(expected, Unit) else expected
    if actual != expected_value:
        raise ValueError(f"Expected unit {expected_value!r}, got {actual!r}")
