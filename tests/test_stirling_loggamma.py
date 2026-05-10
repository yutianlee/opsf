from decimal import Decimal, localcontext
from pathlib import Path

import pytest

import certsf
from certsf.methods.stirling_coefficients import STIRLING_COEFFICIENTS


ROOT = Path(__file__).resolve().parents[1]

_STIRLING_DIAGNOSTICS = {
    "selected_method": "stirling",
    "certificate_scope": "stirling_loggamma_positive_real",
    "certificate_level": "custom_asymptotic_bound",
    "audit_status": "theorem_documented",
    "formula": "stirling_loggamma",
    "domain": "positive_real_x_ge_20",
}

_SHIFTED_DIAGNOSTICS = {
    "selected_method": "stirling_shifted",
    "certificate_scope": "stirling_loggamma_positive_real",
    "certificate_level": "custom_asymptotic_bound",
    "audit_status": "theorem_documented",
    "formula": "stirling_shifted_loggamma",
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


def test_certified_auto_loggamma_selects_unshifted_stirling_when_tail_certifies():
    pytest.importorskip("flint")

    result = certsf.loggamma("20", mode="certified", method="certified_auto", dps=50)

    _assert_successful_stirling_result(result, 50)
    _assert_auto_selector_diagnostics(result, "stirling")
    assert result.diagnostics["auto_candidates"][0]["method"] == "stirling"
    assert result.diagnostics["auto_candidates"][0]["selected"] is True

    reference = certsf.loggamma("20", mode="certified", method="arb", dps=80)
    if _backend_is_unavailable(reference):
        pytest.skip(reference.diagnostics["error"])
    _assert_reference_lies_in_stirling_bound(result, reference)


def test_certified_auto_loggamma_selects_shifted_stirling_when_unshifted_fails():
    pytest.importorskip("flint")

    result = certsf.loggamma("20", mode="certified", method="certified_auto", dps=100)

    _assert_successful_shifted_stirling_result(result, 100)
    _assert_auto_selector_diagnostics(result, "stirling_shifted")
    assert result.diagnostics["shift"] == 18
    assert result.diagnostics["shifted_argument"] == "38"
    assert result.diagnostics["auto_candidates"][0]["method"] == "stirling"
    assert result.diagnostics["auto_candidates"][0]["certified"] is False
    assert result.diagnostics["auto_candidates"][1]["method"] == "stirling_shifted"
    assert result.diagnostics["auto_candidates"][1]["selected"] is True

    reference = certsf.loggamma("20", mode="certified", method="arb", dps=130)
    if _backend_is_unavailable(reference):
        pytest.skip(reference.diagnostics["error"])
    _assert_reference_lies_in_stirling_bound(result, reference)


def test_certified_auto_loggamma_selects_custom_method_for_positive_real_boundary_window():
    pytest.importorskip("flint")

    result = certsf.loggamma("38", mode="certified", method="certified_auto", dps=100)

    assert result.certified is True
    assert result.backend == "certsf+python-flint"
    assert result.method in {"stirling_loggamma", "stirling_shifted_loggamma"}
    assert result.diagnostics["auto_selected_method"] in {"stirling", "stirling_shifted"}
    assert result.diagnostics["auto_selector"] == "certified_auto"
    assert result.diagnostics["certificate_scope"] == "stirling_loggamma_positive_real"

    reference = certsf.loggamma("38", mode="certified", method="arb", dps=130)
    if _backend_is_unavailable(reference):
        pytest.skip(reference.diagnostics["error"])
    _assert_reference_lies_in_stirling_bound(result, reference)


@pytest.mark.parametrize("x", ["3.2", "50+1j"])
def test_certified_auto_loggamma_uses_direct_arb_outside_positive_real_stirling_scope(x):
    result = certsf.loggamma(x, mode="certified", method="certified_auto", dps=50)
    if _backend_is_unavailable(result):
        pytest.skip(result.diagnostics["error"])

    assert result.certified is True
    assert result.method == "arb_ball"
    assert result.backend == "python-flint"
    assert result.diagnostics["certificate_scope"] == "direct_arb_primitive"
    _assert_auto_selector_diagnostics(result, "arb")
    assert result.diagnostics["auto_candidates"][0]["method"] == "arb"


@pytest.mark.parametrize("x", ["20", "3.2", "50+1j"])
def test_certified_auto_loggamma_never_falls_back_to_mpmath(x):
    result = certsf.loggamma(x, mode="certified", method="certified_auto", dps=50)

    assert result.backend != "mpmath"


@pytest.mark.parametrize("mode", ["high_precision", "fast"])
def test_certified_auto_loggamma_is_certified_mode_only(mode):
    with pytest.raises(ValueError, match=f"method 'certified_auto' is not available for 'loggamma' in mode '{mode}'"):
        certsf.loggamma("50", mode=mode, method="certified_auto", dps=50)


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


@pytest.mark.parametrize("k", [1, 2, 3, 10, 50, 100, 150])
def test_stirling_coefficient_table_matches_exact_flint_bernoulli_values(k):
    flint = pytest.importorskip("flint")

    n = 2 * k
    expected = flint.fmpq.bernoulli(n) / flint.fmpq(n * (n - 1))

    assert len(STIRLING_COEFFICIENTS) == 150
    assert flint.fmpq(STIRLING_COEFFICIENTS[k - 1]) == expected


@pytest.mark.parametrize(
    ("x", "dps", "shift", "shifted_argument", "shift_policy"),
    [
        ("20", 50, 0, "20", "direct_no_shift"),
        ("20", 100, 18, "38", "window_37_38"),
        ("37", 100, 1, "38", "window_37_38"),
        ("38", 100, 0, "38", "window_37_38"),
    ],
)
def test_shifted_stirling_loggamma_uses_requested_shift_policy(x, dps, shift, shifted_argument, shift_policy):
    result = certsf.loggamma(x, mode="certified", method="stirling_shifted", dps=dps)
    if _backend_is_unavailable(result):
        pytest.skip(result.diagnostics["error"])

    _assert_successful_shifted_stirling_result(result, dps)
    assert result.diagnostics["shift"] == shift
    assert result.diagnostics["shifted_argument"] == shifted_argument
    assert result.diagnostics["shift_policy"] == shift_policy
    _assert_shifted_error_bound_policy(result, dps)


def test_shifted_stirling_loggamma_above_100_dps_uses_minimal_shift():
    result = certsf.loggamma("20", mode="certified", method="stirling_shifted", dps=120)
    if _backend_is_unavailable(result):
        pytest.skip(result.diagnostics["error"])

    _assert_successful_shifted_stirling_result(result, 120)
    assert result.diagnostics["shift_policy"] == "minimal_shift"
    assert result.diagnostics["shift"] > 0
    assert result.diagnostics["shifted_argument"] == "45"
    _assert_shifted_error_bound_policy(result, 120)


def test_shifted_stirling_loggamma_records_flint_coefficient_fallback_when_needed():
    result = certsf.loggamma("20", mode="certified", method="stirling_shifted", dps=200)
    if _backend_is_unavailable(result):
        pytest.skip(result.diagnostics["error"])

    _assert_successful_shifted_stirling_result(result, 200)
    assert result.diagnostics["coefficient_source"] == "table+flint_fallback"
    assert result.diagnostics["largest_bernoulli_used"] == 2 * result.diagnostics["stirling_terms"] + 2
    assert result.diagnostics["largest_bernoulli_used"] > 300
    _assert_shifted_error_bound_policy(result, 200)


@pytest.mark.parametrize(
    ("x", "dps"),
    [
        ("20", 50),
        ("20", 100),
        ("37", 100),
        ("38", 100),
        ("100", 150),
    ],
)
def test_shifted_stirling_loggamma_contains_direct_arb_reference(x, dps):
    result = certsf.loggamma(x, mode="certified", method="stirling_shifted", dps=dps)
    reference = certsf.loggamma(x, mode="certified", method="arb", dps=dps + 30)
    if _backend_is_unavailable(result):
        pytest.skip(result.diagnostics["error"])
    if _backend_is_unavailable(reference):
        pytest.skip(reference.diagnostics["error"])

    _assert_successful_shifted_stirling_result(result, dps)
    _assert_reference_lies_in_stirling_bound(result, reference)
    _assert_shifted_error_bound_policy(result, dps)


@pytest.mark.parametrize("x", ["19.999", "0", "-5", "nan", "inf", "-inf", "50+0j", "50+1j", "abc"])
def test_shifted_stirling_loggamma_rejects_unsupported_inputs_cleanly(x):
    result = certsf.loggamma(x, mode="certified", method="stirling_shifted", dps=50)

    assert result.certified is False
    assert result.value == ""
    assert result.method == "stirling_shifted_loggamma"
    assert result.backend == "certsf+python-flint"
    for key, expected in _SHIFTED_DIAGNOSTICS.items():
        assert result.diagnostics[key] == expected
    assert result.diagnostics["guard_digits"] == 2
    assert result.diagnostics["effective_dps"] == 52
    assert result.diagnostics["fallback"] == []
    assert "error" in result.diagnostics


@pytest.mark.parametrize("mode", ["high_precision", "fast"])
def test_shifted_stirling_loggamma_is_certified_mode_only(mode):
    with pytest.raises(ValueError, match=f"method 'stirling_shifted' is not available for 'loggamma' in mode '{mode}'"):
        certsf.loggamma("50", mode=mode, method="stirling_shifted", dps=50)


def test_explicit_shifted_stirling_never_falls_back_to_arb_or_mpmath_in_certified_mode():
    result = certsf.loggamma("19.999", dps=50, mode="certified", method="stirling_shifted")

    assert result.certified is False
    assert result.backend == "certsf+python-flint"
    assert result.method == "stirling_shifted_loggamma"


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


def _assert_successful_shifted_stirling_result(result, dps):
    assert result.certified is True
    assert result.function == "loggamma"
    assert result.method == "stirling_shifted_loggamma"
    assert result.backend == "certsf+python-flint"
    assert result.terms_used is not None
    assert result.terms_used > 0
    assert result.abs_error_bound is not None
    assert result.rel_error_bound is not None
    assert result.requested_dps == dps
    assert result.working_dps >= dps
    for key, expected in _SHIFTED_DIAGNOSTICS.items():
        assert result.diagnostics[key] == expected
    assert result.diagnostics["guard_digits"] == 2
    assert result.diagnostics["effective_dps"] == dps + 2
    assert result.diagnostics["terms_used"] == result.terms_used
    assert result.diagnostics["stirling_terms"] == result.terms_used
    assert result.diagnostics["largest_bernoulli_used"] == 2 * result.terms_used + 2
    assert result.diagnostics["coefficient_source"] in {"table", "table+flint_fallback"}
    assert "shift" in result.diagnostics
    assert "shifted_argument" in result.diagnostics
    assert "shift_policy" in result.diagnostics
    assert "tail_bound" in result.diagnostics
    assert result.diagnostics["working_precision_bits"] > 0
    assert result.diagnostics["fallback"] == []


def _assert_shifted_error_bound_policy(result, dps):
    assert result.abs_error_bound is not None
    with localcontext() as ctx:
        ctx.prec = dps + 40
        assert Decimal(result.abs_error_bound) <= Decimal(4) * (Decimal(10) ** Decimal(-(dps + 2)))


def _assert_reference_lies_in_stirling_bound(result, reference):
    assert result.abs_error_bound is not None

    with localcontext() as ctx:
        ctx.prec = max(result.requested_dps, reference.requested_dps) + 80
        distance = abs(Decimal(result.value) - Decimal(reference.value))
        allowed = Decimal(result.abs_error_bound)
        if reference.abs_error_bound is not None:
            allowed += Decimal(reference.abs_error_bound)

    assert distance <= allowed


def _assert_auto_selector_diagnostics(result, selected_method):
    assert result.diagnostics["auto_selector"] == "certified_auto"
    assert result.diagnostics["auto_selected_method"] == selected_method
    assert result.diagnostics["auto_reason"]
    assert isinstance(result.diagnostics["auto_candidates"], list)
    assert result.diagnostics["auto_candidates"]


def _backend_is_unavailable(result):
    return not result.certified and "python-flint is not installed" in result.diagnostics.get("error", "")
