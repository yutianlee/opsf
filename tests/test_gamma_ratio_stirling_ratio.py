from decimal import Decimal, localcontext

import pytest

import certsf
from certsf import mcp_server

_GAMMA_RATIO_STIRLING_RATIO_DIAGNOSTICS = {
    "selected_method": "stirling_ratio",
    "certificate_scope": "gamma_ratio_positive_real_stirling_ratio",
    "certificate_level": "custom_asymptotic_bound",
    "audit_status": "theorem_documented",
    "formula": "gamma_ratio=exp(loggamma_ratio(a,b))",
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
def test_gamma_ratio_stirling_ratio_certifies_positive_real_cases(a, b, dps):
    pytest.importorskip("flint")

    result = certsf.gamma_ratio(a, b, mode="certified", method="stirling_ratio", dps=dps)

    _assert_successful_gamma_ratio_stirling_ratio_result(result, dps)

    reference = certsf.gamma_ratio(a, b, mode="certified", method="arb", dps=dps + 30)
    if _backend_is_unavailable(reference):
        pytest.skip(reference.diagnostics["error"])
    _assert_reference_lies_in_gamma_ratio_bound(result, reference)


def test_gamma_ratio_stirling_ratio_uses_shifted_loggamma_ratio_for_high_precision_boundary():
    pytest.importorskip("flint")

    result = certsf.gamma_ratio("20", "30", mode="certified", method="stirling_ratio", dps=100)

    _assert_successful_gamma_ratio_stirling_ratio_result(result, 100)
    assert result.diagnostics["loggamma_ratio_method_used"] == "stirling_diff"
    assert result.diagnostics["a_loggamma_method_used"] == "stirling_shifted"
    assert result.diagnostics["b_loggamma_method_used"] == "stirling_shifted"
    assert result.diagnostics["a_shift"] == 18
    assert result.diagnostics["a_shifted_argument"] == "38"
    assert result.diagnostics["b_shift"] == 8
    assert result.diagnostics["b_shifted_argument"] == "38"


def test_gamma_ratio_stirling_ratio_certifies_unit_ratio():
    pytest.importorskip("flint")

    result = certsf.gamma_ratio("20", "20", mode="certified", method="stirling_ratio", dps=50)

    _assert_successful_gamma_ratio_stirling_ratio_result(result, 50)
    assert result.abs_error_bound is not None
    assert abs(Decimal(result.value) - Decimal(1)) <= Decimal(result.abs_error_bound)


@pytest.mark.parametrize("bad", ["19.999", "0", "-5", "50+0j", "50+1j", "nan", "inf", "abc"])
def test_gamma_ratio_stirling_ratio_rejects_unsupported_a_inputs_cleanly(bad):
    result = certsf.gamma_ratio(bad, "30", mode="certified", method="stirling_ratio", dps=50)

    _assert_clean_unsupported_result(result)


@pytest.mark.parametrize("bad", ["19.999", "0", "-5", "50+0j", "50+1j", "nan", "inf", "abc"])
def test_gamma_ratio_stirling_ratio_rejects_unsupported_b_inputs_cleanly(bad):
    result = certsf.gamma_ratio("30", bad, mode="certified", method="stirling_ratio", dps=50)

    _assert_clean_unsupported_result(result)


@pytest.mark.parametrize("mode", ["high_precision", "fast"])
def test_gamma_ratio_stirling_ratio_is_certified_mode_only(mode):
    with pytest.raises(
        ValueError,
        match=f"method 'stirling_ratio' is not available for 'gamma_ratio' in mode '{mode}'",
    ):
        certsf.gamma_ratio("50", "30", mode=mode, method="stirling_ratio", dps=50)


@pytest.mark.parametrize(
    ("kwargs", "expected_method"),
    [
        ({"mode": "certified"}, "arb_ball"),
        ({"mode": "certified", "method": "arb"}, "arb_ball"),
        ({"mode": "auto", "certify": True}, "arb_ball"),
        ({"mode": "certified", "method": "auto"}, "arb_ball"),
    ],
)
def test_gamma_ratio_stirling_ratio_does_not_change_default_arb_selection(kwargs, expected_method):
    result = certsf.gamma_ratio("50", "30", dps=50, **kwargs)
    if _backend_is_unavailable(result):
        pytest.skip(result.diagnostics["error"])

    assert result.certified is True
    assert result.method == expected_method
    assert result.backend == "python-flint"
    assert result.diagnostics["certificate_scope"] == "direct_arb_gamma_ratio"


def test_gamma_ratio_stirling_ratio_never_falls_back_to_mpmath_or_arb_for_explicit_method():
    for args in (("19.999", "30"), ("50+1j", "30"), ("30", "19.999"), ("30", "50+1j")):
        result = certsf.gamma_ratio(*args, dps=50, mode="certified", method="stirling_ratio")

        assert result.certified is False
        assert result.backend == "certsf+python-flint"
        assert result.method == "stirling_ratio_gamma_ratio"


def test_special_gamma_ratio_stirling_ratio_method_returns_certified_mcp_payload():
    pytest.importorskip("flint")

    payload = mcp_server.special_gamma_ratio("20", "30", dps=50, mode="certified", method="stirling_ratio")

    assert payload["function"] == "gamma_ratio"
    assert payload["certified"] is True
    assert payload["method"] == "stirling_ratio_gamma_ratio"
    assert payload["backend"] == "certsf+python-flint"
    assert payload["diagnostics"]["certificate_scope"] == "gamma_ratio_positive_real_stirling_ratio"
    assert payload["diagnostics"]["selected_method"] == "stirling_ratio"


def _assert_successful_gamma_ratio_stirling_ratio_result(result, dps):
    assert result.certified is True
    assert result.function == "gamma_ratio"
    assert result.method == "stirling_ratio_gamma_ratio"
    assert result.backend == "certsf+python-flint"
    assert result.terms_used is not None
    assert result.terms_used > 0
    assert result.abs_error_bound is not None
    assert result.rel_error_bound is not None
    assert result.requested_dps == dps
    assert result.working_dps >= dps
    for key, expected in _GAMMA_RATIO_STIRLING_RATIO_DIAGNOSTICS.items():
        assert result.diagnostics[key] == expected
    assert result.diagnostics["loggamma_ratio_method_used"] == "stirling_diff"
    assert result.diagnostics["loggamma_ratio_result_method"] == "stirling_diff_loggamma_ratio"
    assert "loggamma_ratio_abs_error_bound" in result.diagnostics
    assert "combined_abs_error_bound" in result.diagnostics
    assert "exp_radius" in result.diagnostics
    assert "propagated_error_bound" in result.diagnostics
    assert result.diagnostics["a_loggamma_method_used"] in {"stirling", "stirling_shifted"}
    assert result.diagnostics["b_loggamma_method_used"] in {"stirling", "stirling_shifted"}
    assert result.diagnostics["fallback"] == []


def _assert_clean_unsupported_result(result):
    assert result.certified is False
    assert result.value == ""
    assert result.abs_error_bound is None
    assert result.rel_error_bound is None
    assert result.method == "stirling_ratio_gamma_ratio"
    assert result.backend == "certsf+python-flint"
    assert result.diagnostics["selected_method"] == "stirling_ratio"
    assert result.diagnostics["certificate_scope"] == "gamma_ratio_positive_real_stirling_ratio"
    assert result.diagnostics["fallback"] == []
    assert "error" in result.diagnostics


def _assert_reference_lies_in_gamma_ratio_bound(result, reference):
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
