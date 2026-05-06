import json
from math import isclose

import pytest

from certsf import pbdv, pcfd, pcfu, pcfv, pcfw

mp = pytest.importorskip("mpmath")


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


def test_pcfd_matches_pbdv_value_high_precision():
    pbdv_result = pbdv("2.5", "1.25", dps=60, mode="high_precision")
    pcfd_result = pcfd("2.5", "1.25", dps=60, mode="high_precision")
    assert pcfd_result.backend == "mpmath"
    assert pcfd_result.value == json.loads(pbdv_result.value)["value"]


@pytest.mark.parametrize(
    ("function", "expected", "rel_tol"),
    [
        (pcfd, -0.28107627169873172077, 1e-14),
        (pcfu, 0.07856658180821960253, 1e-14),
        (pcfv, 3.02169215840356796854, 1e-14),
        (pcfw, 0.08935157001860056478, 1e-12),
    ],
)
def test_parabolic_cylinder_family_fast(function, expected, rel_tol):
    result = function(2.5, 1.25, mode="fast")
    assert result.backend == "scipy"
    assert not result.certified
    assert isclose(float(result.value), expected, rel_tol=rel_tol)


@pytest.mark.parametrize(
    ("function", "reference"),
    [
        (pcfd, mp.pcfd),
        (pcfu, mp.pcfu),
        (pcfv, mp.pcfv),
        (pcfw, mp.pcfw),
    ],
)
def test_parabolic_cylinder_family_high_precision_complex(function, reference):
    result = function("2.5", "1.25+0.5j", dps=60, mode="high_precision")
    expected = complex(reference(mp.mpf("2.5"), mp.mpc("1.25", "0.5")))
    assert result.backend == "mpmath"
    assert not result.certified
    assert abs(_complex_value(result.value) - expected) < 1e-14


@pytest.mark.parametrize("function", [pbdv, pcfd, pcfu, pcfv, pcfw])
def test_parabolic_cylinder_certified_is_clean_phase6_failure(function):
    result = function("2.5", "1.25", dps=50, mode="certified")
    assert result.backend == "python-flint"
    assert not result.certified
    assert result.value == ""
    assert "Certified parabolic-cylinder backend" in result.diagnostics["error"]
    assert "hypergeometric or ODE enclosure path" in result.diagnostics["error"]


def test_mcp_parabolic_cylinder_family_wrappers_return_dicts():
    from certsf.mcp_server import special_pbdv, special_pcfd, special_pcfu, special_pcfv, special_pcfw

    assert special_pbdv("2.5", "1.25", dps=40, mode="high_precision")["function"] == "pbdv"
    assert special_pcfd("2.5", "1.25", dps=40, mode="high_precision")["function"] == "pcfd"
    assert special_pcfu("2.5", "1.25", dps=40, mode="high_precision")["function"] == "pcfu"
    assert special_pcfv("2.5", "1.25", dps=40, mode="high_precision")["function"] == "pcfv"
    assert special_pcfw("2.5", "1.25", dps=40, mode="high_precision")["function"] == "pcfw"


def _complex_value(value):
    return complex(str(value).strip().strip("()").replace(" ", ""))
