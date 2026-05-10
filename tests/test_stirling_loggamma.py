from decimal import Decimal, localcontext
from pathlib import Path

import pytest

import certsf


ROOT = Path(__file__).resolve().parents[1]

_STIRLING_DIAGNOSTICS = {
    "selected_method": "stirling",
    "certificate_scope": "stirling_loggamma_positive_real",
    "certificate_level": "custom_asymptotic_bound",
    "audit_status": "theorem_documented",
    "formula": "stirling_loggamma",
    "domain": "positive_real_x_ge_20",
}

_AUDIT_GRID_CASES = [
    ("20", 30),
    ("21", 30),
    ("25", 50),
    ("30", 80),
    ("50", 100),
    ("75", 30),
    ("100", 50),
    ("250", 80),
    ("1000", 100),
    ("10000", 100),
]


@pytest.mark.parametrize(
    ("x", "dps"),
    _AUDIT_GRID_CASES,
)
def test_stirling_loggamma_certifies_positive_real_audit_grid(x, dps):
    pytest.importorskip("flint")

    result = certsf.loggamma(x, mode="certified", method="stirling", dps=dps)

    _assert_successful_stirling_result(result, dps)

    reference = certsf.loggamma(x, mode="certified", method="arb", dps=dps + 20)
    if _backend_is_unavailable(reference):
        pytest.skip(reference.diagnostics["error"])
    _assert_reference_lies_in_stirling_bound(result, reference)


@pytest.mark.parametrize("x", ["20", "20.000000000001"])
def test_stirling_loggamma_accepts_boundary_and_above(x):
    result = certsf.loggamma(x, mode="certified", method="stirling", dps=30)
    if _backend_is_unavailable(result):
        pytest.skip(result.diagnostics["error"])

    _assert_successful_stirling_result(result, 30)


@pytest.mark.parametrize("x", ["19.999", "19.999999999999", "0", "-5", "nan", "inf", "-inf", "50+0j", "50+1j", "abc"])
def test_stirling_loggamma_rejects_unsupported_inputs_cleanly(x):
    result = certsf.loggamma(x, mode="certified", method="stirling", dps=50)

    assert result.certified is False
    assert result.value == ""
    assert result.method == "stirling_loggamma"
    assert result.backend == "certsf+python-flint"
    for key, expected in _STIRLING_DIAGNOSTICS.items():
        assert result.diagnostics[key] == expected
    assert result.diagnostics["fallback"] == []
    assert "error" in result.diagnostics


def test_stirling_loggamma_terms_increase_with_precision_for_fixed_x():
    pytest.importorskip("flint")

    results = [certsf.loggamma("100", mode="certified", method="stirling", dps=dps) for dps in (30, 50, 80, 100)]
    terms = []
    for result, dps in zip(results, (30, 50, 80, 100), strict=True):
        _assert_successful_stirling_result(result, dps)
        terms.append(result.terms_used)

    assert terms == sorted(terms)
    assert len(set(terms)) > 1


def test_stirling_loggamma_high_dps_cap_failure_reports_term_selection_diagnostics():
    pytest.importorskip("flint")

    result = certsf.loggamma("20", mode="certified", method="stirling", dps=80)

    assert result.certified is False
    assert result.value == ""
    assert result.method == "stirling_loggamma"
    assert result.backend == "certsf+python-flint"
    assert result.diagnostics["selected_method"] == "stirling"
    assert result.diagnostics["terms_attempted"] == result.diagnostics["max_terms"]
    assert result.diagnostics["terms_attempted"] == 256
    assert "final_tail_bound" in result.diagnostics
    assert "requested_tolerance" in result.diagnostics
    assert result.diagnostics["fallback"] == []
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
    for x in ("19.999", "50+0j"):
        result = certsf.loggamma(x, dps=50, mode="certified", method="stirling")

        assert result.certified is False
        assert result.backend == "certsf+python-flint"
        assert result.method == "stirling_loggamma"


def test_stirling_implementation_does_not_import_scipy_or_mpmath():
    source = (ROOT / "src" / "certsf" / "methods" / "stirling.py").read_text(encoding="utf-8")

    assert "import scipy" not in source
    assert "from scipy" not in source
    assert "import mpmath" not in source
    assert "from mpmath" not in source


def _assert_successful_stirling_result(result, dps):
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
