import json
import math

import pytest

from certsf import ai, airyai, airy, airybi, bi

mp = pytest.importorskip("mpmath")


def test_airy_fast_returns_all_components():
    result = airy(1.0, mode="fast")
    values = json.loads(result.value)
    assert set(values) == {"ai", "aip", "bi", "bip"}
    assert values["ai"].startswith("0.135292416312881")
    assert result.backend == "scipy"
    assert not result.certified


def test_airy_high_precision_returns_all_components():
    result = airy("1.0", dps=60, mode="high_precision")
    values = json.loads(result.value)
    assert values["bi"].startswith("1.20742359495287125943")
    assert result.backend == "mpmath"
    assert not result.certified


def test_airy_certified_returns_bounds_or_clean_failure():
    result = airy("1.0", dps=50, mode="certified")
    assert result.backend == "python-flint"
    if result.certified:
        values = json.loads(result.value)
        bounds = json.loads(result.abs_error_bound)
        assert values["ai"].startswith("0.13529241631288141552")
        assert set(bounds) == {"ai", "aip", "bi", "bip"}
        assert result.diagnostics["domain"] == "real"
        assert result.diagnostics["certificate_scope"] == "phase3_real_airy"
    else:
        assert "error" in result.diagnostics


def test_airy_component_fast_and_high_precision():
    fast = ai(1.0, mode="fast")
    high_precision = bi("1.0", dps=60, mode="high_precision")
    assert fast.function == "ai"
    assert fast.backend == "scipy"
    assert high_precision.function == "bi"
    assert high_precision.backend == "mpmath"
    assert fast.value.startswith("0.135292416312881")
    assert high_precision.value.startswith("1.20742359495287125943")


@pytest.mark.parametrize("z", ["-8", "-1.25", "0", "1", "8"])
@pytest.mark.parametrize(
    ("component", "derivative", "reference"),
    [
        (ai, 0, lambda x: mp.airyai(x)),
        (ai, 1, lambda x: mp.airyai(x, derivative=1)),
        (bi, 0, lambda x: mp.airybi(x)),
        (bi, 1, lambda x: mp.airybi(x, derivative=1)),
    ],
)
def test_certified_real_airy_components_cover_mpmath(z, component, derivative, reference):
    result = component(z, derivative=derivative, dps=70, mode="certified")
    assert result.backend == "python-flint"
    if not result.certified:
        pytest.skip(result.diagnostics.get("error", "certified backend unavailable"))

    value = float(result.value)
    bound = float(result.abs_error_bound)
    expected = float(reference(mp.mpf(z)))
    assert result.diagnostics["domain"] == "real"
    assert result.diagnostics["certificate_scope"] == "phase3_real_airy"
    assert result.diagnostics["derivative"] == derivative
    assert abs(value - expected) <= max(bound, 1e-65)


def test_certified_real_airy_wronskian_identity_is_within_bounds():
    z = "2.5"
    results = {
        "ai": ai(z, dps=80, mode="certified"),
        "aip": ai(z, derivative=1, dps=80, mode="certified"),
        "bi": bi(z, dps=80, mode="certified"),
        "bip": bi(z, derivative=1, dps=80, mode="certified"),
    }
    if not all(result.certified for result in results.values()):
        pytest.skip("certified backend unavailable")

    values = {name: float(result.value) for name, result in results.items()}
    bounds = {name: float(result.abs_error_bound) for name, result in results.items()}
    wronskian = values["ai"] * values["bip"] - values["aip"] * values["bi"]
    propagated = (
        abs(values["bip"]) * bounds["ai"]
        + abs(values["ai"]) * bounds["bip"]
        + abs(values["bi"]) * bounds["aip"]
        + abs(values["aip"]) * bounds["bi"]
    )
    assert abs(wronskian - 1 / math.pi) <= max(propagated, 1e-14)


def test_airy_aliases_and_invalid_derivative():
    assert airyai("1.0", mode="fast").value == ai("1.0", mode="fast").value
    assert airybi("1.0", mode="fast").value == bi("1.0", mode="fast").value
    with pytest.raises(ValueError):
        ai("1.0", derivative=2)
    with pytest.raises(ValueError):
        bi("1.0", derivative=-1)


def test_mcp_airy_component_wrappers_return_dicts():
    from certsf.mcp_server import special_ai, special_bi

    ai_payload = special_ai("1.0", dps=40, mode="certified")
    bi_payload = special_bi("1.0", derivative=1, dps=40, mode="certified")
    assert ai_payload["function"] == "ai"
    assert bi_payload["function"] == "bip"
