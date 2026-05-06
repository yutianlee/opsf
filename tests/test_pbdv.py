import json
from math import isclose

from certsf import pbdv


def test_pbdv_fast():
    result = pbdv(2.5, 1.25, mode="fast")
    values = json.loads(result.value)
    assert result.backend == "scipy"
    assert isclose(float(values["value"]), -0.2810762716987306, rel_tol=1e-14)
    assert isclose(float(values["derivative"]), 2.01418601055005, rel_tol=1e-14)


def test_pbdv_high_precision():
    result = pbdv("2.5", "1.25", dps=60, mode="high_precision")
    values = json.loads(result.value)
    assert result.backend == "mpmath"
    assert values["value"].startswith("-0.28107627169873172077")
    assert values["derivative"].startswith("2.0141860105500499514")


def test_pbdv_certified_is_clean_phase1_failure():
    result = pbdv("2.5", "1.25", dps=50, mode="certified")
    assert result.backend == "python-flint"
    assert not result.certified
    assert result.value == ""
    assert "Certified backend unavailable" in result.diagnostics["error"]
