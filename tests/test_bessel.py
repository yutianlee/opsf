from math import isclose

import pytest

from certsf import besseli, besselj, besselk, bessely

mp = pytest.importorskip("mpmath")

def test_besselj_fast():
    result = besselj(2.5, 4.0, mode="fast")
    assert result.backend == "scipy"
    assert not result.certified
    assert isclose(float(result.value), 0.440884974557338, rel_tol=1e-14)


def test_besselj_high_precision():
    result = besselj("2.5", "4.0", dps=60, mode="high_precision")
    assert result.backend == "mpmath"
    assert result.value.startswith("0.44088497455734116552")


def test_mpmath_complex_string_parser_preserves_decimal_precision():
    from certsf.backends.mpmath_backend import _mp_number

    text = "1.2345678901234567890123456789+0.1000000000000000000000000001j"
    with mp.workdps(90):
        parsed = _mp_number(text)
        assert parsed.real == mp.mpf("1.2345678901234567890123456789")
        assert parsed.imag == mp.mpf("0.1000000000000000000000000001")


def test_besselj_certified_returns_bounds_or_clean_failure():
    result = besselj("2.5", "4.0", dps=50, mode="certified")
    assert result.backend == "python-flint"
    if result.certified:
        assert result.abs_error_bound is not None
        assert result.value.startswith("0.44088497455734116552")
    else:
        assert "error" in result.diagnostics


def test_bessel_family_fast_and_high_precision():
    cases = [
        (besselj, 2, 4.0, 0.3641281458520728),
        (bessely, 2, 4.0, 0.21590359460361497),
        (besseli, 2, 4.0, 6.422189375284105),
        (besselk, 2, 4.0, 0.017401425529487237),
    ]
    for function, order, x, expected in cases:
        fast = function(order, x, mode="fast")
        high_precision = function(str(order), str(x), dps=60, mode="high_precision")
        assert fast.backend == "scipy"
        assert high_precision.backend == "mpmath"
        assert isclose(float(fast.value), expected, rel_tol=1e-14)
        assert isclose(float(high_precision.value), expected, rel_tol=1e-14)


def test_bessel_family_fast_and_high_precision_complex_arguments():
    z = "4.0+1.25j"
    for function in [besselj, bessely, besseli, besselk]:
        fast = function("2.5", z, mode="fast")
        high_precision = function("2.5", z, dps=60, mode="high_precision")
        assert fast.backend == "scipy"
        assert high_precision.backend == "mpmath"
        assert abs(_complex_value(fast.value) - _complex_value(high_precision.value)) < 1e-12


@pytest.mark.parametrize(
    ("function", "reference"),
    [
        (besselj, lambda n, x: mp.besselj(n, x)),
        (bessely, lambda n, x: mp.bessely(n, x)),
        (besseli, lambda n, x: mp.besseli(n, x)),
        (besselk, lambda n, x: mp.besselk(n, x)),
    ],
)
@pytest.mark.parametrize(("order", "x"), [(0, "1.25"), (2, "4.0"), (3, "5.5")])
def test_certified_integer_real_bessel_covers_mpmath(function, reference, order, x):
    result = function(str(order), x, dps=70, mode="certified")
    assert result.backend == "python-flint"
    if not result.certified:
        pytest.skip(result.diagnostics.get("error", "certified backend unavailable"))

    value = float(result.value)
    bound = float(result.abs_error_bound)
    expected = float(reference(order, mp.mpf(x)))
    assert result.diagnostics["order"] == order
    assert result.diagnostics["domain"] == "real"
    assert result.diagnostics["order_domain"] == "integer"
    assert result.diagnostics["certificate_scope"] == "phase4_integer_real_bessel"
    assert abs(value - expected) <= max(bound, 1e-65)


@pytest.mark.parametrize(
    ("function", "reference"),
    [
        (besselj, lambda n, x: mp.besselj(n, x)),
        (bessely, lambda n, x: mp.bessely(n, x)),
        (besseli, lambda n, x: mp.besseli(n, x)),
        (besselk, lambda n, x: mp.besselk(n, x)),
    ],
)
@pytest.mark.parametrize(("order", "z"), [("2.5", "4.0"), ("2.5", "4.0+1.25j"), ("2", "4.0+1.25j")])
def test_certified_real_order_complex_bessel_covers_mpmath(function, reference, order, z):
    result = function(order, z, dps=70, mode="certified")
    assert result.backend == "python-flint"
    if not result.certified:
        pytest.skip(result.diagnostics.get("error", "certified backend unavailable"))

    value = _complex_value(result.value)
    bound = float(result.abs_error_bound)
    expected = complex(reference(mp.mpf(order), _mp_number(z)))
    assert result.diagnostics["order"] == (int(order) if "." not in order else order)
    assert result.diagnostics["order_domain"] in {"integer", "real"}
    assert result.diagnostics["certificate_scope"] in {
        "phase4_integer_real_bessel",
        "phase5_real_order_complex_bessel",
    }
    if "j" in z:
        assert result.diagnostics["domain"] == "complex"
        assert result.diagnostics["certificate_scope"] == "phase5_real_order_complex_bessel"
    assert abs(value - expected) <= max(bound, 1e-65)


def test_certified_besselj_three_term_recurrence():
    x = "3.75"
    n = 2
    jm = besselj(n - 1, x, dps=80, mode="certified")
    jn = besselj(n, x, dps=80, mode="certified")
    jp = besselj(n + 1, x, dps=80, mode="certified")
    if not all(result.certified for result in [jm, jn, jp]):
        pytest.skip("certified backend unavailable")

    x_float = float(x)
    residual = float(jm.value) + float(jp.value) - (2 * n / x_float) * float(jn.value)
    propagated = (
        float(jm.abs_error_bound)
        + abs(2 * n / x_float) * float(jn.abs_error_bound)
        + float(jp.abs_error_bound)
    )
    assert abs(residual) <= max(propagated, 1e-14)


def test_certified_bessel_phase5_scope_rejects_complex_order():
    result = bessely("2.5+1j", "4.0", dps=50, mode="certified")
    assert result.backend == "python-flint"
    assert not result.certified
    assert result.value == ""
    if "python-flint is not installed" in result.diagnostics["error"]:
        pytest.skip(result.diagnostics["error"])
    assert "real order" in result.diagnostics["error"]


def test_mcp_bessel_family_wrappers_return_dicts():
    from certsf.mcp_server import special_besseli, special_besselj, special_besselk, special_bessely

    assert special_besselj("2", "4.0", dps=40, mode="certified")["function"] == "besselj"
    assert special_bessely("2", "4.0", dps=40, mode="certified")["function"] == "bessely"
    assert special_besseli("2", "4.0", dps=40, mode="certified")["function"] == "besseli"
    assert special_besselk("2", "4.0", dps=40, mode="certified")["function"] == "besselk"


def _mp_number(value):
    text = str(value).replace("i", "j")
    if "j" in text.lower():
        parsed = complex(text)
        return mp.mpc(parsed.real, parsed.imag)
    return mp.mpf(text)


def _complex_value(value):
    return complex(str(value).strip().strip("()").replace(" ", ""))
