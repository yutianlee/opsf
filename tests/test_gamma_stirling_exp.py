from decimal import Decimal, localcontext

import pytest

import certsf
from certsf import mcp_server

_GAMMA_STIRLING_EXP_DIAGNOSTICS = {
    "selected_method": "stirling_exp",
    "certificate_scope": "gamma_positive_real_stirling_exp",
    "certificate_level": "custom_asymptotic_bound",
    "audit_status": "theorem_documented",
    "formula": "gamma=exp(loggamma)",
    "domain": "positive_real_x_ge_20",
}


@pytest.mark.parametrize(
    ("x", "dps"),
    [
        ("20", 50),
        ("20", 100),
        ("38", 100),
        ("100", 100),
    ],
)
def test_gamma_stirling_exp_certifies_positive_real_cases(x, dps):
    pytest.importorskip("flint")

    result = certsf.gamma(x, mode="certified", method="stirling_exp", dps=dps)

    _assert_successful_gamma_stirling_exp_result(result, dps)

    reference = certsf.gamma(x, mode="certified", method="arb", dps=dps + 30)
    if _backend_is_unavailable(reference):
        pytest.skip(reference.diagnostics["error"])
    _assert_reference_lies_in_gamma_bound(result, reference)


def test_gamma_stirling_exp_uses_shifted_loggamma_for_high_precision_boundary():
    pytest.importorskip("flint")

    result = certsf.gamma("20", mode="certified", method="stirling_exp", dps=100)

    _assert_successful_gamma_stirling_exp_result(result, 100)
    assert result.diagnostics["loggamma_method_used"] == "stirling_shifted"
    assert result.diagnostics["shift"] == 18
    assert result.diagnostics["shifted_argument"] == "38"


@pytest.mark.parametrize("x", ["19.999", "0", "-5", "50+0j", "50+1j", "nan", "inf", "abc"])
def test_gamma_stirling_exp_rejects_unsupported_inputs_cleanly(x):
    result = certsf.gamma(x, mode="certified", method="stirling_exp", dps=50)

    assert result.certified is False
    assert result.value == ""
    assert result.method == "stirling_exp_gamma"
    assert result.backend == "certsf+python-flint"
    assert result.diagnostics["selected_method"] == "stirling_exp"
    assert result.diagnostics["certificate_scope"] == "gamma_positive_real_stirling_exp"
    assert result.diagnostics["fallback"] == []
    assert "error" in result.diagnostics


@pytest.mark.parametrize("mode", ["high_precision", "fast"])
def test_gamma_stirling_exp_is_certified_mode_only(mode):
    with pytest.raises(ValueError, match=f"method 'stirling_exp' is not available for 'gamma' in mode '{mode}'"):
        certsf.gamma("50", mode=mode, method="stirling_exp", dps=50)


@pytest.mark.parametrize(
    ("kwargs", "expected_method"),
    [
        ({"mode": "certified"}, "arb_ball"),
        ({"mode": "certified", "method": "arb"}, "arb_ball"),
        ({"mode": "auto", "certify": True}, "arb_ball"),
        ({"mode": "certified", "method": "auto"}, "arb_ball"),
    ],
)
def test_gamma_stirling_exp_does_not_change_default_arb_selection(kwargs, expected_method):
    result = certsf.gamma("50", dps=50, **kwargs)
    if _backend_is_unavailable(result):
        pytest.skip(result.diagnostics["error"])

    assert result.certified is True
    assert result.method == expected_method
    assert result.backend == "python-flint"
    assert result.diagnostics["certificate_scope"] == "direct_arb_primitive"


def test_gamma_stirling_exp_never_falls_back_to_mpmath_or_arb_for_explicit_method():
    for x in ("19.999", "50+1j"):
        result = certsf.gamma(x, dps=50, mode="certified", method="stirling_exp")

        assert result.certified is False
        assert result.backend == "certsf+python-flint"
        assert result.method == "stirling_exp_gamma"


def test_special_gamma_stirling_exp_method_returns_certified_mcp_payload():
    pytest.importorskip("flint")

    payload = mcp_server.special_gamma("20", dps=50, mode="certified", method="stirling_exp")

    assert payload["function"] == "gamma"
    assert payload["certified"] is True
    assert payload["method"] == "stirling_exp_gamma"
    assert payload["backend"] == "certsf+python-flint"
    assert payload["diagnostics"]["certificate_scope"] == "gamma_positive_real_stirling_exp"
    assert payload["diagnostics"]["selected_method"] == "stirling_exp"


def _assert_successful_gamma_stirling_exp_result(result, dps):
    assert result.certified is True
    assert result.function == "gamma"
    assert result.method == "stirling_exp_gamma"
    assert result.backend == "certsf+python-flint"
    assert result.terms_used is not None
    assert result.terms_used > 0
    assert result.abs_error_bound is not None
    assert result.rel_error_bound is not None
    assert result.requested_dps == dps
    assert result.working_dps >= dps
    for key, expected in _GAMMA_STIRLING_EXP_DIAGNOSTICS.items():
        assert result.diagnostics[key] == expected
    assert result.diagnostics["terms_used"] == result.terms_used
    assert result.diagnostics["stirling_terms"] == result.terms_used
    assert result.diagnostics["loggamma_method_used"] in {"stirling", "stirling_shifted"}
    assert "loggamma_abs_error_bound" in result.diagnostics
    assert "exp_radius" in result.diagnostics
    assert "propagated_error_bound" in result.diagnostics
    assert result.diagnostics["fallback"] == []


def _assert_reference_lies_in_gamma_bound(result, reference):
    assert result.abs_error_bound is not None

    with localcontext() as ctx:
        ctx.prec = max(result.requested_dps, reference.requested_dps) + 120
        distance = abs(Decimal(result.value) - Decimal(reference.value))
        allowed = Decimal(result.abs_error_bound)
        if reference.abs_error_bound is not None:
            allowed += Decimal(reference.abs_error_bound)

    assert distance <= allowed


def _backend_is_unavailable(result):
    return not result.certified and "python-flint is not installed" in result.diagnostics.get("error", "")
