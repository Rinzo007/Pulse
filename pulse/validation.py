"""Mathematical and model-contract validation helpers."""

from math import sqrt
from statistics import mean


def relative_error_percent(pred: float, fact: float) -> float:
    if fact == 0:
        raise ValueError("Relative error is undefined when fact is zero")
    return 100.0 * (pred - fact) / fact


def normalized_rmse(pred: list[float], fact: list[float]) -> float:
    if len(pred) != len(fact):
        raise ValueError("pred and fact must have equal length")
    values = [((p - f) / f) ** 2 for p, f in zip(pred, fact) if f > 0]
    if not values:
        raise ValueError("No positive observations available for normalized RMSE")
    return sqrt(mean(values))
