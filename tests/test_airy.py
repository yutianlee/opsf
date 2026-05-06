import json

from certsf import airy


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
    else:
        assert "error" in result.diagnostics
