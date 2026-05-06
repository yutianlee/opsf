from math import isclose

import pytest

from certsf import gamma, loggamma, rgamma


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


def test_rgamma_fast_and_high_precision():
    fast = rgamma(3.2, mode="fast")
    high_precision = rgamma("3.2", dps=70, mode="high_precision")
    assert fast.function == "rgamma"
    assert fast.backend == "scipy"
    assert high_precision.backend == "mpmath"
    assert isclose(float(fast.value), 0.41254712918876374, rel_tol=1e-15)
    assert high_precision.value.startswith("0.41254712918876375296")


def test_certified_rgamma_at_gamma_poles_is_zero():
    for z in ["0", "-1", "-2"]:
        result = rgamma(z, dps=50, mode="certified")
        assert result.backend == "python-flint"
        if result.certified:
            assert result.value == "0"
            assert result.abs_error_bound == "0"
            assert result.rel_error_bound is None
        else:
            assert "error" in result.diagnostics


def test_certified_gamma_at_poles_is_clean_failure():
    result = gamma("0", dps=50, mode="certified")
    assert not result.certified
    assert result.value == ""
    assert "non-finite" in result.diagnostics["error"]


def test_certified_loggamma_negative_real_uses_principal_branch():
    result = loggamma("-2.5", dps=50, mode="certified")
    assert result.backend == "python-flint"
    if result.certified:
        value = complex(result.value)
        assert isclose(value.real, -0.05624371649767405, rel_tol=1e-15)
        assert isclose(value.imag, -9.42477796076938, rel_tol=1e-15)
        assert result.abs_error_bound is not None
    else:
        assert "error" in result.diagnostics


def test_certified_loggamma_pole_is_clean_failure():
    result = loggamma("-2", dps=50, mode="certified")
    assert not result.certified
    assert result.value == ""
    assert "non-finite" in result.diagnostics["error"]


def test_mcp_gamma_family_wrappers_return_dicts():
    from certsf.mcp_server import special_gamma, special_rgamma

    gamma_payload = special_gamma("3.2", dps=40, mode="fast")
    rgamma_payload = special_rgamma("0", dps=40, mode="certified")
    assert gamma_payload["function"] == "gamma"
    assert rgamma_payload["function"] == "rgamma"


def test_invalid_mode_raises():
    with pytest.raises(ValueError):
        gamma(3.2, mode="optimistic")
