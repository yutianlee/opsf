from decimal import Decimal, localcontext

import pytest

import certsf
from certsf import mcp_server

_BETA_STIRLING_BETA_DIAGNOSTICS = {
    "selected_method": "stirling_beta",
    "certificate_scope": "beta_positive_real_stirling_beta",
    "certificate_level": "custom_asymptotic_bound",
    "audit_status": "theorem_documented",
    "formula": "beta=exp(loggamma(a)+loggamma(b)-loggamma(a+b))",
    "domain": "positive_real_a_b_ge_20",
}


@pytest.mark.parametrize(
    ("a", "b", "dps"),
    [
        ("20", "30", 50),
        ("20", "30", 100),
        ("30", "20", 50),
    ],
)
def test_beta_stirling_beta_certifies_positive_real_cases(a, b, dps):
    pytest.importorskip("flint")

    result = certsf.beta(a, b, mode="certified", method="stirling_beta", dps=dps)

    _assert_successful_beta_stirling_beta_result(result, dps)

    reference = certsf.beta(a, b, mode="certified", method="arb", dps=dps + 30)
    if _backend_is_unavailable(reference):
        pytest.skip(reference.diagnostics["error"])
    _assert_reference_lies_in_beta_bound(result, reference)


def test_beta_stirling_beta_uses_shifted_loggamma_for_high_precision_boundary():
    pytest.importorskip("flint")

    result = certsf.beta("20", "30", mode="certified", method="stirling_beta", dps=100)

    _assert_successful_beta_stirling_beta_result(result, 100)
    assert result.diagnostics["a_loggamma_method_used"] == "stirling_shifted"
    assert result.diagnostics["b_loggamma_method_used"] == "stirling_shifted"
    assert result.diagnostics["a_shift"] == 18
    assert result.diagnostics["a_shifted_argument"] == "38"
    assert result.diagnostics["b_shift"] == 8
    assert result.diagnostics["b_shifted_argument"] == "38"
    assert result.diagnostics["sum_argument"] == "50"


def test_beta_stirling_beta_certifies_symmetric_overlap():
    pytest.importorskip("flint")

    ab = certsf.beta("20", "30", mode="certified", method="stirling_beta", dps=50)
    ba = certsf.beta("30", "20", mode="certified", method="stirling_beta", dps=50)

    _assert_successful_beta_stirling_beta_result(ab, 50)
    _assert_successful_beta_stirling_beta_result(ba, 50)
    distance = abs(Decimal(ab.value) - Decimal(ba.value))
    assert distance <= Decimal(ab.abs_error_bound) + Decimal(ba.abs_error_bound)


@pytest.mark.parametrize("bad", ["19.999", "0", "-5", "50+0j", "50+1j", "nan", "inf", "abc"])
def test_beta_stirling_beta_rejects_unsupported_a_inputs_cleanly(bad):
    result = certsf.beta(bad, "30", mode="certified", method="stirling_beta", dps=50)

    _assert_clean_unsupported_result(result)


@pytest.mark.parametrize("bad", ["19.999", "0", "-5", "50+0j", "50+1j", "nan", "inf", "abc"])
def test_beta_stirling_beta_rejects_unsupported_b_inputs_cleanly(bad):
    result = certsf.beta("30", bad, mode="certified", method="stirling_beta", dps=50)

    _assert_clean_unsupported_result(result)


@pytest.mark.parametrize("mode", ["high_precision", "fast"])
def test_beta_stirling_beta_is_certified_mode_only(mode):
    with pytest.raises(
        ValueError,
        match=f"method 'stirling_beta' is not available for 'beta' in mode '{mode}'",
    ):
        certsf.beta("50", "30", mode=mode, method="stirling_beta", dps=50)


@pytest.mark.parametrize(
    ("kwargs", "expected_method"),
    [
        ({"mode": "certified"}, "arb_ball"),
        ({"mode": "certified", "method": "arb"}, "arb_ball"),
        ({"mode": "auto", "certify": True}, "arb_ball"),
        ({"mode": "certified", "method": "auto"}, "arb_ball"),
    ],
)
def test_beta_stirling_beta_does_not_change_default_arb_selection(kwargs, expected_method):
    result = certsf.beta("50", "30", dps=50, **kwargs)
    if _backend_is_unavailable(result):
        pytest.skip(result.diagnostics["error"])

    assert result.certified is True
    assert result.method == expected_method
    assert result.backend == "python-flint"
    assert result.diagnostics["certificate_scope"] == "direct_arb_beta"


def test_beta_stirling_beta_never_falls_back_to_mpmath_or_arb_for_explicit_method():
    for args in (("19.999", "30"), ("50+1j", "30"), ("30", "19.999"), ("30", "50+1j")):
        result = certsf.beta(*args, dps=50, mode="certified", method="stirling_beta")

        assert result.certified is False
        assert result.backend == "certsf+python-flint"
        assert result.method == "stirling_beta_beta"


def test_special_beta_stirling_beta_method_returns_certified_mcp_payload():
    pytest.importorskip("flint")

    payload = mcp_server.special_beta("20", "30", dps=50, mode="certified", method="stirling_beta")

    assert payload["function"] == "beta"
    assert payload["certified"] is True
    assert payload["method"] == "stirling_beta_beta"
    assert payload["backend"] == "certsf+python-flint"
    assert payload["diagnostics"]["certificate_scope"] == "beta_positive_real_stirling_beta"
    assert payload["diagnostics"]["selected_method"] == "stirling_beta"


def _assert_successful_beta_stirling_beta_result(result, dps):
    assert result.certified is True
    assert result.function == "beta"
    assert result.method == "stirling_beta_beta"
    assert result.backend == "certsf+python-flint"
    assert result.terms_used is not None
    assert result.terms_used > 0
    assert result.abs_error_bound is not None
    assert result.requested_dps == dps
    assert result.working_dps >= dps
    for key, expected in _BETA_STIRLING_BETA_DIAGNOSTICS.items():
        assert result.diagnostics[key] == expected
    assert result.diagnostics["fallback"] == []
    assert result.diagnostics["a_loggamma_method_used"] in {"stirling", "stirling_shifted"}
    assert result.diagnostics["b_loggamma_method_used"] in {"stirling", "stirling_shifted"}
    assert result.diagnostics["sum_loggamma_method_used"] in {"stirling", "stirling_shifted"}
    assert "combined_log_abs_error_bound" in result.diagnostics
    assert "exp_radius" in result.diagnostics
    assert "propagated_error_bound" in result.diagnostics


def _assert_clean_unsupported_result(result):
    assert result.certified is False
    assert result.value == ""
    assert result.abs_error_bound is None
    assert result.rel_error_bound is None
    assert result.method == "stirling_beta_beta"
    assert result.backend == "certsf+python-flint"
    assert result.diagnostics["selected_method"] == "stirling_beta"
    assert result.diagnostics["certificate_scope"] == "beta_positive_real_stirling_beta"
    assert result.diagnostics["fallback"] == []
    assert "error" in result.diagnostics


def _assert_reference_lies_in_beta_bound(result, reference):
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
