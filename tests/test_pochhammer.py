import pytest

from certsf import SFResult, pochhammer

mp = pytest.importorskip("mpmath")
mp.mp.dps = 120


@pytest.mark.parametrize(
    ("a", "n", "expected"),
    [
        ("3", "0", mp.mpf("1")),
        ("3", "1", mp.mpf("3")),
        ("3", "4", mp.mpf("360")),
        ("0.5", "3", mp.mpf("15") / 8),
        ("-2", "3", mp.mpf("0")),
    ],
)
def test_pochhammer_certified_special_values(a, n, expected):
    result = pochhammer(a, n, dps=80, mode="certified")
    _require_certified(result)

    assert result.function == "pochhammer"
    assert result.diagnostics["certificate_scope"] == "direct_arb_pochhammer_product"
    _assert_close(_mp_number(result.value), expected, mp.mpf("1e-75"))


def test_pochhammer_complex_a_with_integer_n():
    result = pochhammer("1+2j", "3", dps=80, mode="certified")
    _require_certified(result)

    _assert_close(_mp_number(result.value), mp.mpc("-18", "14"), mp.mpf("1e-75"))


def test_pochhammer_high_precision_uses_mpmath_rf():
    result = pochhammer("3.2", "1.2", dps=80, mode="high_precision")
    expected = mp.rf(mp.mpf("3.2"), mp.mpf("1.2"))

    assert result.backend == "mpmath"
    _assert_close(_mp_number(result.value), expected, mp.mpf("1e-75"))


def test_certified_pochhammer_non_integer_n_is_clean_failure():
    result = pochhammer("3", "2.5", dps=80, mode="certified")

    assert result.certified is False
    assert result.value == ""
    assert result.diagnostics["mode"] == "certified"
    assert result.diagnostics["certificate_scope"] == "direct_arb_pochhammer_product"
    assert "requires integer n" in result.diagnostics["error"]


def test_certified_pochhammer_negative_n_is_clean_failure():
    result = pochhammer("3", "-1", dps=80, mode="certified")

    assert result.certified is False
    assert result.value == ""
    assert result.diagnostics["mode"] == "certified"
    assert result.diagnostics["certificate_scope"] == "direct_arb_pochhammer_product"
    assert "n >= 0" in result.diagnostics["error"]


def test_certified_pochhammer_simultaneous_poles_are_not_certified():
    result = pochhammer("-2", "2", dps=80, mode="certified")

    assert result.certified is False
    assert result.value == ""
    assert result.diagnostics["mode"] == "certified"
    assert result.diagnostics["pole_case"] == "simultaneous_poles_not_certified"
    assert "simultaneous-pole" in result.diagnostics["error"]


def test_pochhammer_auto_dispatch_behavior():
    fast = pochhammer("3", "4", dps=15, mode="auto")
    high_precision = pochhammer("3", "4", dps=50, mode="auto")
    certified = pochhammer("3", "4", dps=50, mode="auto", certify=True)

    assert fast.backend == "scipy"
    assert high_precision.backend == "mpmath"
    assert certified.backend == "python-flint"
    assert certified.diagnostics["mode"] == "certified"


def test_pochhammer_all_modes_return_sfresult():
    for mode in ("fast", "high_precision", "certified", "auto"):
        result = pochhammer("3", "4", dps=40, mode=mode)
        assert isinstance(result, SFResult)
        assert result.function == "pochhammer"


def test_certified_pochhammer_recurrence_contains_zero():
    a = mp.mpf("2.25")
    n = 4
    lower = pochhammer(_mp_text(a), str(n), dps=90, mode="certified")
    upper = pochhammer(_mp_text(a), str(n + 1), dps=90, mode="certified")
    _require_certified(lower, upper)

    _assert_contains_zero(_sub(_ball(upper), _scale(a + n, _ball(lower))))


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
