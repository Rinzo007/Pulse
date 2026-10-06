import json
from pathlib import Path
import pytest
from pulse.city import validate_manifest
from pulse.quality import evaluate_quality
from pulse.save import save, load
from pulse.year import YearCalculation, STAGES
from pulse.model import MODEL_VERSION

def test_quality_passes_known_good_dataset():
    values=list(range(1,21))
    report=evaluate_quality(model_version=MODEL_VERSION,city_package_version="1",scenario_id="test",pred=values,fact=values,generated_at="2026-01-01")
    assert report.status == "PASS"

def test_city_manifest_rejects_missing_fields(tmp_path):
    errors=validate_manifest(tmp_path,{})
    assert "manifest.city_uid missing" in errors

def test_year_pipeline_is_canonical():
    stages={name:(lambda state, n=name: {**state,"last":n}) for name in STAGES}
    report=YearCalculation(MODEL_VERSION,"city-1",stages).run({"x":1})
    assert tuple(x.name for x in report.stages)==STAGES
    assert report.stages[-1].status=="success"

def test_year_cancellation_does_not_publish():
    stages={name:(lambda state: state) for name in STAGES}
    with pytest.raises(RuntimeError, match="YEAR-CANCELLED"):
        YearCalculation(MODEL_VERSION,"city-1",stages).run({},cancel=lambda: True)

def test_save_round_trip(tmp_path):
    path=tmp_path/"game.wkrt"
    state={"city_uid":"test:1","network":{"routes":[]}}
    save(path,state)
    assert load(path)["state"] == state

def test_save_corruption_is_rejected(tmp_path):
    path=tmp_path/"game.wkrt"
    save(path,{"x":1})
    doc=json.loads(path.read_text())
    doc["payload"]["state"]["x"]=2
    path.write_text(json.dumps(doc),encoding="utf-8")
    with pytest.raises(ValueError,match="SAVE-CHECKSUM-001"):
        load(path)
