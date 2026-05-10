from decimal import Decimal, localcontext

import pytest

import certsf


_STIRLING_DIAGNOSTICS = {
    "selected_method": "stirling",
    "certificate_scope": "stirling_loggamma_positive_real",
    "certificate_level": "custom_asymptotic_bound",
    "audit_status": "theorem_documented",
    "formula": "stirling_loggamma",
    "domain": "positive_real_x_ge_20",
}


@pytest.mark.parametrize(
    ("x", "dps"),
    [
        ("20", 30),
        ("50", 50),
        ("100", 80),
        ("1000", 100),
    ],
)
def test_stirling_loggamma_certifies_positive_real_samples(x, dps):
    pytest.importorskip("flint")

    result = certsf.loggamma(x, mode="certified", method="stirling", dps=dps)

    assert result.certified is True
    assert result.function == "loggamma"
    assert result.method == "stirling_loggamma"
    assert result.backend == "certsf+python-flint"
    assert result.terms_used is not None
    assert result.terms_used > 0
    assert result.abs_error_bound is not None
    assert result.rel_error_bound is not None
    assert result.requested_dps == dps
    assert result.working_dps >= dps
    for key, expected in _STIRLING_DIAGNOSTICS.items():
        assert result.diagnostics[key] == expected
    assert result.diagnostics["terms_used"] == result.terms_used
    assert "tail_bound" in result.diagnostics
    assert result.diagnostics["working_precision_bits"] > 0
    assert result.diagnostics["fallback"] == []

    reference = certsf.loggamma(x, mode="certified", method="arb", dps=dps + 20)
    if _backend_is_unavailable(reference):
        pytest.skip(reference.diagnostics["error"])
    _assert_reference_lies_in_stirling_bound(result, reference)


@pytest.mark.parametrize("x", ["19.999", "0", "-5", "50+1j"])
def test_stirling_loggamma_rejects_unsupported_inputs_cleanly(x):
    result = certsf.loggamma(x, mode="certified", method="stirling", dps=50)

    assert result.certified is False
    assert result.value == ""
    assert result.method == "stirling_loggamma"
    assert result.backend == "certsf+python-flint"
    for key, expected in _STIRLING_DIAGNOSTICS.items():
        assert result.diagnostics[key] == expected
    assert "error" in result.diagnostics


@pytest.mark.parametrize("mode", ["high_precision", "fast"])
def test_stirling_loggamma_is_certified_mode_only(mode):
    with pytest.raises(ValueError, match=f"method 'stirling' is not available for 'loggamma' in mode '{mode}'"):
        certsf.loggamma("50", mode=mode, method="stirling", dps=50)


@pytest.mark.parametrize(
    ("kwargs", "expected_method"),
    [
        ({"mode": "certified"}, "arb_ball"),
        ({"mode": "certified", "method": "arb"}, "arb_ball"),
        ({"mode": "auto", "certify": True}, "arb_ball"),
        ({"mode": "certified", "method": "auto"}, "arb_ball"),
    ],
)
def test_stirling_loggamma_does_not_change_default_arb_selection(kwargs, expected_method):
    result = certsf.loggamma("50", dps=50, **kwargs)
    if _backend_is_unavailable(result):
        pytest.skip(result.diagnostics["error"])

    assert result.certified is True
    assert result.method == expected_method
    assert result.backend == "python-flint"
    assert result.diagnostics["certificate_scope"] == "direct_arb_primitive"


def test_explicit_stirling_never_falls_back_to_mpmath_in_certified_mode():
    result = certsf.loggamma("19.999", dps=50, mode="certified", method="stirling")

    assert result.certified is False
    assert result.backend == "certsf+python-flint"
    assert result.method == "stirling_loggamma"


def _assert_reference_lies_in_stirling_bound(result, reference):
    assert result.abs_error_bound is not None

    with localcontext() as ctx:
        ctx.prec = max(result.requested_dps, reference.requested_dps) + 80
        distance = abs(Decimal(result.value) - Decimal(reference.value))
        allowed = Decimal(result.abs_error_bound)
        if reference.abs_error_bound is not None:
            allowed += Decimal(reference.abs_error_bound)

    assert distance <= allowed


def _backend_is_unavailable(result):
    return not result.certified and "python-flint is not installed" in result.diagnostics.get("error", "")
