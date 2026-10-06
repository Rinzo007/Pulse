"""P0.1 model-quality contract."""
from dataclasses import dataclass, asdict
from math import sqrt
from statistics import mean

@dataclass(frozen=True, slots=True)
class QualityReport:
    model_version: str
    city_package_version: str
    scenario_id: str
    status: str
    metrics: dict
    data_quality: dict
    generated_at: str


def pearson(pred: list[float], fact: list[float]) -> float | None:
    if len(pred) != len(fact) or len(pred) < 2:
        return None
    mp, mf = mean(pred), mean(fact)
    num = sum((p-mp)*(f-mf) for p, f in zip(pred, fact))
    den = sqrt(sum((p-mp)**2 for p in pred) * sum((f-mf)**2 for f in fact))
    return None if den == 0 else num / den


def geh(pred: float, fact: float) -> float:
    if pred + fact == 0:
        return 0.0
    return sqrt(2 * (pred-fact)**2 / (pred+fact))


def evaluate_quality(*, model_version: str, city_package_version: str, scenario_id: str,
                     pred: list[float], fact: list[float], generated_at: str,
                     modal_pred: list[float] | None = None, modal_fact: list[float] | None = None,
                     satisfaction_pred: float | None = None, satisfaction_fact: float | None = None) -> QualityReport:
    if len(pred) != len(fact):
        raise ValueError("pred and fact must have equal length")
    comparable = [(p, f) for p, f in zip(pred, fact) if f > 0]
    metrics = {}
    total_fact, total_pred = sum(fact), sum(pred)
    total_error = None if total_fact == 0 else 100 * (total_pred-total_fact) / total_fact
    metrics["total_passenger_flow_error_percent"] = total_error
    metrics["pearson_r"] = pearson(pred, fact)
    metrics["normalized_rmse"] = None if not comparable else sqrt(mean(((p-f)/f)**2 for p,f in comparable))
    gehs = [geh(p,f) for p,f in comparable]
    metrics["geh_share_le_5"] = None if not gehs else sum(x <= 5 for x in gehs) / len(gehs)
    if modal_pred is not None and modal_fact is not None:
        if len(modal_pred) != len(modal_fact): raise ValueError("modal shares must have equal length")
        metrics["modal_share_max_abs_diff"] = max((abs(p-f) for p,f in zip(modal_pred,modal_fact)), default=0.0)
    if satisfaction_pred is not None and satisfaction_fact is not None:
        metrics["satisfaction_diff_pp"] = abs(satisfaction_pred-satisfaction_fact)
    gates = []
    if total_error is not None: gates.append(abs(total_error) <= 15)
    r = metrics["pearson_r"]
    if r is not None and len(comparable) >= 20: gates.append(r >= .90)
    elif len(comparable) < 20: gates.append(False)
    nrmse = metrics["normalized_rmse"]
    if nrmse is not None: gates.append(nrmse <= .30)
    if gehs: gates.append(metrics["geh_share_le_5"] >= .85)
    if "modal_share_max_abs_diff" in metrics: gates.append(metrics["modal_share_max_abs_diff"] <= .10)
    if "satisfaction_diff_pp" in metrics: gates.append(metrics["satisfaction_diff_pp"] <= 5)
    status = "PASS" if gates and all(gates) else ("NO_DATA" if not comparable else "FAIL")
    if status == "FAIL" and r is not None and .85 <= r < .90 and all(g for g in gates if g is not False): status = "WARN"
    return QualityReport(model_version, city_package_version, scenario_id, status, metrics, {"comparable_observations": len(comparable)}, generated_at)
