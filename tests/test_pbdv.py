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


@pytest.mark.parametrize(
    ("function", "parameter", "z", "reference", "formula"),
    [
        (pcfd, "2.5", "1.25", mp.pcfd, "pcfd_via_pcfu"),
        (pcfd, "2.5", "1.25+0.5j", mp.pcfd, "pcfd_via_pcfu"),
        (pcfu, "2.5", "1.25", mp.pcfu, "pcfu_1f1_global"),
        (pcfu, "2.5", "-1.25", mp.pcfu, "pcfu_1f1_global"),
        (pcfu, "2.5", "1.25+0.5j", mp.pcfu, "pcfu_1f1_global"),
        (pcfv, "2.5", "1.25", mp.pcfv, "pcfv_dlmf_connection"),
        (pcfv, "2.5", "1.25+0.5j", mp.pcfv, "pcfv_dlmf_connection"),
        (pcfw, "2.5", "1.25", mp.pcfw, "pcfw_dlmf_12_14_real_connection"),
        (pcfw, "2.5", "-1.25", mp.pcfw, "pcfw_dlmf_12_14_real_connection"),
    ],
)
def test_certified_parabolic_cylinder_core_covers_mpmath(function, parameter, z, reference, formula):
    result = function(parameter, z, dps=70, mode="certified")
    assert result.backend == "python-flint"
    if not result.certified:
        pytest.skip(result.diagnostics.get("error", "certified backend unavailable"))

    value = _complex_value(result.value)
    bound = float(result.abs_error_bound)
    with mp.workdps(90):
        expected = complex(reference(mp.mpf(parameter), _mp_number(z)))
    expected_scope = (
        "phase8_parabolic_cylinder_connections"
        if function in {pcfv, pcfw}
        else "phase7_hypergeometric_parabolic_cylinder"
    )
    assert result.diagnostics["certificate_scope"] == expected_scope
    assert result.diagnostics["parameter"] == parameter
    assert result.diagnostics["parameter_domain"] == "real"
    assert result.diagnostics["formula"] == formula
    assert abs(value - expected) <= max(bound, 1e-65)


def test_certified_pbdv_returns_value_and_derivative_bounds():
    result = pbdv("2.5", "1.25", dps=70, mode="certified")
    assert result.backend == "python-flint"
    if not result.certified:
        pytest.skip(result.diagnostics.get("error", "certified backend unavailable"))

    values = json.loads(result.value)
    bounds = json.loads(result.abs_error_bound)
    z = mp.mpf("1.25")
    expected_value = mp.pcfd(mp.mpf("2.5"), z)
    expected_derivative = (z / 2) * expected_value - mp.pcfd(mp.mpf("3.5"), z)
    assert result.diagnostics["certificate_scope"] == "phase7_hypergeometric_parabolic_cylinder"
    assert set(values) == {"value", "derivative"}
    assert set(bounds) == {"value", "derivative"}
    assert abs(float(values["value"]) - float(expected_value)) <= max(float(bounds["value"]), 1e-65)
    assert abs(float(values["derivative"]) - float(expected_derivative)) <= max(float(bounds["derivative"]), 1e-65)


def test_certified_parabolic_cylinder_rejects_complex_parameter():
    result = pcfu("2.5+1j", "1.25", dps=50, mode="certified")
    assert result.backend == "python-flint"
    assert not result.certified
    assert result.value == ""
    if "python-flint is not installed" in result.diagnostics["error"]:
        pytest.skip(result.diagnostics["error"])
    assert "real parameters" in result.diagnostics["error"]


def test_certified_pcfw_rejects_complex_argument():
    result = pcfw("2.5", "1.25+0.5j", dps=50, mode="certified")
    assert result.backend == "python-flint"
    assert not result.certified
    assert result.value == ""
    if "python-flint is not installed" in result.diagnostics["error"]:
        pytest.skip(result.diagnostics["error"])
    assert "real arguments" in result.diagnostics["error"]


def test_mcp_parabolic_cylinder_family_wrappers_return_dicts():
    from certsf.mcp_server import special_pbdv, special_pcfd, special_pcfu, special_pcfv, special_pcfw

    assert special_pbdv("2.5", "1.25", dps=40, mode="high_precision")["function"] == "pbdv"
    assert special_pcfd("2.5", "1.25", dps=40, mode="high_precision")["function"] == "pcfd"
    assert special_pcfu("2.5", "1.25", dps=40, mode="high_precision")["function"] == "pcfu"
    assert special_pcfv("2.5", "1.25", dps=40, mode="high_precision")["function"] == "pcfv"
    assert special_pcfw("2.5", "1.25", dps=40, mode="high_precision")["function"] == "pcfw"


def test_mcp_pbdv_returns_nested_component_payloads():
    from certsf.mcp_server import special_pbdv

    payload = special_pbdv("2.5", "1.25", dps=40, mode="high_precision")
    assert set(payload["value"]) == {"value", "derivative"}


def _complex_value(value):
    return complex(str(value).strip().strip("()").replace(" ", ""))


def _mp_number(value):
    text = str(value).replace("i", "j")
    if "j" in text.lower():
        parsed = complex(text)
        return mp.mpc(parsed.real, parsed.imag)
    return mp.mpf(text)
