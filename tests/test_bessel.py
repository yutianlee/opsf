from math import isclose

from certsf import besselj


def test_besselj_fast():
    result = besselj(2.5, 4.0, mode="fast")
    assert result.backend == "scipy"
    assert not result.certified
    assert isclose(float(result.value), 0.440884974557338, rel_tol=1e-14)


def test_besselj_high_precision():
    result = besselj("2.5", "4.0", dps=60, mode="high_precision")
    assert result.backend == "mpmath"
    assert result.value.startswith("0.44088497455734116552")


def test_besselj_certified_returns_bounds_or_clean_failure():
    result = besselj("2.5", "4.0", dps=50, mode="certified")
    assert result.backend == "python-flint"
    if result.certified:
        assert result.abs_error_bound is not None
        assert result.value.startswith("0.44088497455734116552")
    else:
        assert "error" in result.diagnostics
