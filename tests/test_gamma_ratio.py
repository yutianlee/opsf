import pytest

from certsf import SFResult, gamma_ratio

mp = pytest.importorskip("mpmath")
mp.mp.dps = 120


def test_gamma_ratio_real_noninteger_case():
    result = gamma_ratio("3.2", "1.2", dps=80, mode="high_precision")

    assert result.function == "gamma_ratio"
    assert result.backend == "mpmath"
    _assert_close(_mp_number(result.value), mp.mpf("2.64"), mp.mpf("1e-75"))


def test_gamma_ratio_integer_case():
    result = gamma_ratio("5", "3", dps=80, mode="high_precision")

    _assert_close(_mp_number(result.value), mp.mpf("12"), mp.mpf("1e-75"))


def test_gamma_ratio_half_integer_case():
    result = gamma_ratio("0.5", "1", dps=80, mode="high_precision")

    _assert_close(_mp_number(result.value), mp.sqrt(mp.pi), mp.mpf("1e-75"))


def test_certified_gamma_ratio_denominator_pole_is_zero():
    result = gamma_ratio("3.2", "0", dps=80, mode="certified")
    if not result.certified and "python-flint is not installed" in result.diagnostics.get("error", ""):
        pytest.skip(result.diagnostics["error"])

    assert result.certified is True
    assert result.value == "0"
    assert result.abs_error_bound == "0"
    assert result.rel_error_bound is None
    assert result.diagnostics["certificate_scope"] == "direct_arb_gamma_ratio"
    assert result.diagnostics["pole_case"] == "denominator_pole_zero"
    assert result.diagnostics["denominator_pole"] is True


def test_certified_gamma_ratio_numerator_pole_is_clean_failure():
    result = gamma_ratio("0", "3.2", dps=80, mode="certified")

    assert result.certified is False
    assert result.value == ""
    assert result.diagnostics["mode"] == "certified"
    assert result.diagnostics["pole_case"] == "numerator_pole"
    assert "Gamma(a) has a pole" in result.diagnostics["error"]


def test_certified_gamma_ratio_two_poles_is_clean_failure():
    result = gamma_ratio("0", "0", dps=80, mode="certified")

    assert result.certified is False
    assert result.value == ""
    assert result.diagnostics["mode"] == "certified"
    assert result.diagnostics["pole_case"] == "both_poles"
    assert "both Gamma(a) and Gamma(b) have poles" in result.diagnostics["error"]


def test_gamma_ratio_complex_regular_case():
    result = gamma_ratio("2.5+0.25j", "1.5-0.5j", dps=80, mode="high_precision")
    expected = mp.exp(mp.loggamma(mp.mpc("2.5", "0.25")) - mp.loggamma(mp.mpc("1.5", "-0.5")))

    _assert_close(_mp_number(result.value), expected, mp.mpf("1e-75"))


def test_gamma_ratio_auto_dispatch_behavior():
    fast = gamma_ratio("5", "3", dps=15, mode="auto")
    high_precision = gamma_ratio("5", "3", dps=50, mode="auto")
    certified = gamma_ratio("5", "3", dps=50, mode="auto", certify=True)

    assert fast.backend == "scipy"
    assert high_precision.backend == "mpmath"
    assert certified.backend == "python-flint"
    assert certified.diagnostics["mode"] == "certified"


def test_gamma_ratio_all_modes_return_sfresult():
    for mode in ("fast", "high_precision", "certified", "auto"):
        result = gamma_ratio("5", "3", dps=40, mode=mode)
        assert isinstance(result, SFResult)
        assert result.function == "gamma_ratio"


def test_certified_gamma_ratio_first_argument_recurrence_contains_zero():
    a = mp.mpf("2.25")
    b = mp.mpf("1.5")
    lower = gamma_ratio(_mp_text(a), _mp_text(b), dps=90, mode="certified")
    upper = gamma_ratio(_mp_text(a + 1), _mp_text(b), dps=90, mode="certified")
    _require_certified(lower, upper)

    _assert_contains_zero(_sub(_ball(upper), _scale(a, _ball(lower))))


def test_certified_gamma_ratio_second_argument_recurrence_contains_zero():
    a = mp.mpf("3.25")
    b = mp.mpf("1.5")
    lower = gamma_ratio(_mp_text(a), _mp_text(b), dps=90, mode="certified")
    shifted = gamma_ratio(_mp_text(a), _mp_text(b + 1), dps=90, mode="certified")
    _require_certified(lower, shifted)

    _assert_contains_zero(_sub(_scale(b, _ball(shifted)), _ball(lower)))


def test_certified_gamma_ratio_composition_identity_contains_zero():
    a = mp.mpf("3.25")
    b = mp.mpf("1.75")
    c = mp.mpf("0.5")
    ab = gamma_ratio(_mp_text(a), _mp_text(b), dps=90, mode="certified")
    bc = gamma_ratio(_mp_text(b), _mp_text(c), dps=90, mode="certified")
    ac = gamma_ratio(_mp_text(a), _mp_text(c), dps=90, mode="certified")
    _require_certified(ab, bc, ac)

    _assert_contains_zero(_sub(_mul(_ball(ab), _ball(bc)), _ball(ac)))


def _require_certified(*results):
    for result in results:
        if not result.certified:
            pytest.skip(result.diagnostics.get("error", "certified backend unavailable"))


def _assert_close(left, right, tolerance):
    assert abs(left - right) <= tolerance


def _assert_contains_zero(ball):
    assert abs(ball[0]) <= ball[1]


def _ball(result):
    return _mp_number(result.value), _mp_number(result.abs_error_bound)


def _sub(left, right):
    return left[0] - right[0], left[1] + right[1]


def _scale(factor, ball):
    return factor * ball[0], abs(factor) * ball[1]


def _mul(left, right):
    value = left[0] * right[0]
    radius = abs(left[0]) * right[1] + abs(right[0]) * left[1] + left[1] * right[1]
    return value, radius


def _mp_number(value):
    text = str(value).strip().strip("()").replace(" ", "").replace("i", "j")
    if "j" not in text.lower():
        return mp.mpf(text)
    real, imag = _split_complex_text(text)
    return mp.mpc(mp.mpf(real), mp.mpf(imag))


def _split_complex_text(text: str) -> tuple[str, str]:
    body = text[:-1]
    if body in {"", "+"}:
        return "0", "1"
    if body == "-":
        return "0", "-1"

    split_at = None
    for index in range(len(body) - 1, 0, -1):
        if body[index] in "+-" and body[index - 1] not in "eE":
            split_at = index
            break
    if split_at is None:
        return "0", _normalize_imaginary_component(body)
    return body[:split_at], _normalize_imaginary_component(body[split_at:])


def _normalize_imaginary_component(value: str) -> str:
    if value in {"", "+"}:
        return "1"
    if value == "-":
        return "-1"
    return value


def _mp_text(value, digits: int = 50) -> str:
    if isinstance(value, mp.mpc):
        sign = "+" if mp.im(value) >= 0 else "-"
        return f"{mp.nstr(mp.re(value), digits)}{sign}{mp.nstr(abs(mp.im(value)), digits)}j"
    return mp.nstr(value, digits)
