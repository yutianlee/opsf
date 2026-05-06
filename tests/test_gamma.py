from math import isclose

import pytest

from certsf import gamma, loggamma


def test_gamma_fast_uses_scipy():
    result = gamma(3.2, mode="fast")
    assert result.backend == "scipy"
    assert result.method == "scipy.special"
    assert not result.certified
    assert isclose(float(result.value), 2.4239654799353687, rel_tol=1e-15)


def test_gamma_high_precision_uses_mpmath():
    result = gamma("3.2", dps=70, mode="high_precision")
    assert result.backend == "mpmath"
    assert result.working_dps >= 70
    assert not result.certified
    assert result.abs_error_bound is None
    assert result.value.startswith("2.42396547993536801209")


def test_gamma_auto_certify_uses_certified_backend_when_available():
    result = gamma("3.2", dps=50, mode="auto", certify=True)
    assert result.backend == "python-flint"
    assert result.method == "arb_ball"
    if result.certified:
        assert result.abs_error_bound is not None
        assert result.value.startswith("2.42396547993536801209")
    else:
        assert "error" in result.diagnostics


def test_loggamma_wrapper():
    result = loggamma(3.2, mode="fast")
    assert result.function == "loggamma"
    assert result.backend == "scipy"
    assert isclose(float(result.value), 0.885404827154909, rel_tol=1e-15)


def test_invalid_mode_raises():
    with pytest.raises(ValueError):
        gamma(3.2, mode="optimistic")
