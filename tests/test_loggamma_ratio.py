import pytest

from certsf import SFResult, loggamma_ratio

mp = pytest.importorskip("mpmath")
mp.mp.dps = 120


def test_loggamma_ratio_real_noninteger_case():
    result = loggamma_ratio("3.2", "1.2", dps=80, mode="high_precision")

    assert result.function == "loggamma_ratio"
    assert result.backend == "mpmath"
    _assert_close(_mp_number(result.value), mp.log(mp.mpf("2.64")), mp.mpf("1e-75"))


def test_loggamma_ratio_integer_case():
    result = loggamma_ratio("5", "3", dps=80, mode="high_precision")

    _assert_close(_mp_number(result.value), mp.log(mp.mpf("12")), mp.mpf("1e-75"))


def test_loggamma_ratio_half_integer_case():
    result = loggamma_ratio("0.5", "1", dps=80, mode="high_precision")

    _assert_close(_mp_number(result.value), mp.mpf("0.5") * mp.log(mp.pi), mp.mpf("1e-75"))


def test_loggamma_ratio_complex_regular_case():
    result = loggamma_ratio("2.5+0.25j", "1.5-0.5j", dps=80, mode="high_precision")
    expected = mp.loggamma(mp.mpc("2.5", "0.25")) - mp.loggamma(mp.mpc("1.5", "-0.5"))

    _assert_close(_mp_number(result.value), expected, mp.mpf("1e-75"))


def test_loggamma_ratio_uses_principal_loggamma_difference():
    result = loggamma_ratio("0.2+5j", "0.2-5j", dps=80, mode="high_precision")
    value = _mp_number(result.value)
    principal_log_of_ratio = mp.log(mp.gamma(mp.mpc("0.2", "5")) / mp.gamma(mp.mpc("0.2", "-5")))

    _assert_close(
        value,
        mp.loggamma(mp.mpc("0.2", "5")) - mp.loggamma(mp.mpc("0.2", "-5")),
        mp.mpf("1e-75"),
    )
    assert abs(value - principal_log_of_ratio) > 6


def test_certified_loggamma_ratio_numerator_pole_is_clean_failure():
    result = loggamma_ratio("0", "3.2", dps=80, mode="certified")

    assert result.certified is False
    assert result.value == ""
    assert result.diagnostics["mode"] == "certified"
    assert result.diagnostics["pole_case"] == "numerator_pole"
    assert result.diagnostics["numerator_pole"] is True
    assert result.diagnostics["denominator_pole"] is False
    assert result.diagnostics["certificate_scope"] == "direct_arb_loggamma_ratio"
    assert "Gamma(a) has a pole" in result.diagnostics["error"]


def test_certified_loggamma_ratio_denominator_pole_is_clean_failure():
    result = loggamma_ratio("3.2", "0", dps=80, mode="certified")

    assert result.certified is False
    assert result.value == ""
    assert result.diagnostics["mode"] == "certified"
    assert result.diagnostics["pole_case"] == "denominator_pole"
    assert result.diagnostics["numerator_pole"] is False
    assert result.diagnostics["denominator_pole"] is True
    assert result.diagnostics["certificate_scope"] == "direct_arb_loggamma_ratio"
    assert "Gamma(b) has a pole" in result.diagnostics["error"]


def test_certified_loggamma_ratio_two_poles_is_clean_failure():
    result = loggamma_ratio("0", "0", dps=80, mode="certified")

    assert result.certified is False
    assert result.value == ""
    assert result.diagnostics["mode"] == "certified"
    assert result.diagnostics["pole_case"] == "both_poles"
    assert result.diagnostics["numerator_pole"] is True
    assert result.diagnostics["denominator_pole"] is True
    assert result.diagnostics["certificate_scope"] == "direct_arb_loggamma_ratio"
    assert "both Gamma(a) and Gamma(b) have poles" in result.diagnostics["error"]


def test_loggamma_ratio_auto_dispatch_behavior():
    fast = loggamma_ratio("5", "3", dps=15, mode="auto")
    high_precision = loggamma_ratio("5", "3", dps=50, mode="auto")
    certified = loggamma_ratio("5", "3", dps=50, mode="auto", certify=True)

    assert fast.backend == "scipy"
    assert high_precision.backend == "mpmath"
    assert certified.backend == "python-flint"
    assert certified.diagnostics["mode"] == "certified"


def test_loggamma_ratio_all_modes_return_sfresult():
    for mode in ("fast", "high_precision", "certified", "auto"):
        result = loggamma_ratio("5", "3", dps=40, mode=mode)
        assert isinstance(result, SFResult)
        assert result.function == "loggamma_ratio"


def test_certified_loggamma_ratio_first_argument_recurrence_contains_zero():
    a = mp.mpf("2.25")
    b = mp.mpf("1.5")
    lower = loggamma_ratio(_mp_text(a), _mp_text(b), dps=90, mode="certified")
    upper = loggamma_ratio(_mp_text(a + 1), _mp_text(b), dps=90, mode="certified")
    _require_certified(lower, upper)

    _assert_contains_zero(_sub(_sub(_ball(upper), _ball(lower)), _point(mp.log(a))))


def test_certified_loggamma_ratio_second_argument_recurrence_contains_zero():
    a = mp.mpf("3.25")
    b = mp.mpf("1.5")
    lower = loggamma_ratio(_mp_text(a), _mp_text(b), dps=90, mode="certified")
    shifted = loggamma_ratio(_mp_text(a), _mp_text(b + 1), dps=90, mode="certified")
    _require_certified(lower, shifted)

    _assert_contains_zero(_add(_sub(_ball(shifted), _ball(lower)), _point(mp.log(b))))


def test_certified_loggamma_ratio_composition_identity_contains_zero():
    a = mp.mpf("3.25")
    b = mp.mpf("1.75")
    c = mp.mpf("0.5")
    ab = loggamma_ratio(_mp_text(a), _mp_text(b), dps=90, mode="certified")
    bc = loggamma_ratio(_mp_text(b), _mp_text(c), dps=90, mode="certified")
    ac = loggamma_ratio(_mp_text(a), _mp_text(c), dps=90, mode="certified")
    _require_certified(ab, bc, ac)

    _assert_contains_zero(_sub(_add(_ball(ab), _ball(bc)), _ball(ac)))


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


def _point(value):
    return value, mp.mpf("0")


def _add(left, right):
    return left[0] + right[0], left[1] + right[1]


def _sub(left, right):
    return left[0] - right[0], left[1] + right[1]


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
