import pytest

from pulse.constants import CONSTANTS, constant_value, get_constant, registry_metadata
from pulse.model import MODEL_PROFILE, MODEL_VERSION
from pulse.units import Unit, require_unit
from pulse.validation import normalized_rmse, relative_error_percent


def test_single_runtime_profile():
    assert MODEL_PROFILE == "pulse-standard"
    assert all(c.profile == MODEL_PROFILE for c in CONSTANTS.values())


def test_registry_has_no_duplicate_ids():
    ids = [c.id for c in CONSTANTS.values()]
    assert len(ids) == len(set(ids))


def test_constant_lookup():
    c = get_constant("mode.wait.headway_multiplier")
    assert c.value == pytest.approx(0.40)
    assert c.unit == Unit.DIMENSIONLESS
    assert constant_value(c.id) == pytest.approx(0.40)


def test_unknown_constant_fails():
    with pytest.raises(KeyError):
        get_constant("does.not.exist")


def test_registry_metadata_is_versioned():
    metadata = registry_metadata()
    assert metadata["profile"] == MODEL_PROFILE
    assert metadata["model_version"] == MODEL_VERSION
    assert metadata["constants"]["mode.wait.headway_multiplier"]["version"] == 1


def test_units_are_explicit():
    require_unit("km", Unit.KM)
    with pytest.raises(ValueError):
        require_unit("m", Unit.KM)


def test_relative_error_zero_fact_rejected():
    with pytest.raises(ValueError):
        relative_error_percent(1, 0)


def test_normalized_rmse():
    assert normalized_rmse([100, 200], [100, 100]) == pytest.approx(0.70710678118)


def test_normalized_rmse_rejects_no_positive_fact():
    with pytest.raises(ValueError):
        normalized_rmse([0], [0])
