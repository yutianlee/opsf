import pytest

from certsf import SFResult, beta

mp = pytest.importorskip("mpmath")
mp.mp.dps = 120


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        ("1", "1", mp.mpf("1")),
        ("0.5", "0.5", mp.pi),
        ("2", "3", mp.mpf(1) / 12),
    ],
)
def test_beta_special_values(a, b, expected):
    result = beta(a, b, dps=80, mode="high_precision")

    assert result.function == "beta"
    assert result.backend == "mpmath"
    _assert_close(_mp_number(result.value), expected, mp.mpf("1e-75"))


def test_beta_real_noninteger_case():
    result = beta("3.2", "1.2", dps=80, mode="high_precision")
    expected = mp.beta(mp.mpf("3.2"), mp.mpf("1.2"))

    _assert_close(_mp_number(result.value), expected, mp.mpf("1e-75"))


def test_beta_complex_regular_case():
    result = beta("2.5+0.25j", "1.5-0.5j", dps=80, mode="high_precision")
    expected = mp.beta(mp.mpc("2.5", "0.25"), mp.mpc("1.5", "-0.5"))

    _assert_close(_mp_number(result.value), expected, mp.mpf("1e-75"))


def test_certified_beta_sum_pole_is_zero():
    result = beta("0.5", "-0.5", dps=80, mode="certified")
    if not result.certified and "python-flint is not installed" in result.diagnostics.get("error", ""):
        pytest.skip(result.diagnostics["error"])

    assert result.certified is True
    assert result.value == "0"
    assert result.abs_error_bound == "0"
    assert result.rel_error_bound is None
    assert result.diagnostics["certificate_scope"] == "direct_arb_beta"
    assert result.diagnostics["pole_case"] == "sum_pole_zero"
    assert result.diagnostics["a_pole"] is False
    assert result.diagnostics["b_pole"] is False
    assert result.diagnostics["sum_pole"] is True


def test_certified_beta_a_pole_is_clean_failure():
    result = beta("0", "1.2", dps=80, mode="certified")

    assert result.certified is False
    assert result.value == ""
    assert result.diagnostics["mode"] == "certified"
    assert result.diagnostics["pole_case"] == "a_pole"
    assert result.diagnostics["a_pole"] is True
    assert result.diagnostics["b_pole"] is False
    assert result.diagnostics["sum_pole"] is False
    assert result.diagnostics["certificate_scope"] == "direct_arb_beta"
    assert "Gamma(a) or Gamma(b) has a pole" in result.diagnostics["error"]


def test_certified_beta_b_pole_is_clean_failure():
    result = beta("1.2", "0", dps=80, mode="certified")

    assert result.certified is False
    assert result.value == ""
    assert result.diagnostics["mode"] == "certified"
    assert result.diagnostics["pole_case"] == "b_pole"
    assert result.diagnostics["a_pole"] is False
    assert result.diagnostics["b_pole"] is True
    assert result.diagnostics["sum_pole"] is False
    assert result.diagnostics["certificate_scope"] == "direct_arb_beta"
    assert "Gamma(a) or Gamma(b) has a pole" in result.diagnostics["error"]


def test_certified_beta_simultaneous_pole_interaction_is_clean_failure():
    result = beta("0", "0", dps=80, mode="certified")

    assert result.certified is False
    assert result.value == ""
    assert result.diagnostics["mode"] == "certified"
    assert result.diagnostics["pole_case"] == "a_b_sum_poles"
    assert result.diagnostics["a_pole"] is True
    assert result.diagnostics["b_pole"] is True
    assert result.diagnostics["sum_pole"] is True
    assert result.diagnostics["certificate_scope"] == "direct_arb_beta"
    assert "simultaneous singularities are not certified" in result.diagnostics["error"]


def test_beta_auto_dispatch_behavior():
    fast = beta("2", "3", dps=15, mode="auto")
    high_precision = beta("2", "3", dps=50, mode="auto")
    certified = beta("2", "3", dps=50, mode="auto", certify=True)

    assert fast.backend == "scipy"
    assert high_precision.backend == "mpmath"
    assert certified.backend == "python-flint"
    assert certified.diagnostics["mode"] == "certified"


def test_beta_all_modes_return_sfresult():
    for mode in ("fast", "high_precision", "certified", "auto"):
        result = beta("2", "3", dps=40, mode=mode)
        assert isinstance(result, SFResult)
        assert result.function == "beta"


def test_certified_beta_symmetry_contains_zero():
    ab = beta("3.2", "1.2", dps=90, mode="certified")
    ba = beta("1.2", "3.2", dps=90, mode="certified")
    _require_certified(ab, ba)

    _assert_contains_zero(_sub(_ball(ab), _ball(ba)))


def test_certified_beta_first_argument_recurrence_contains_zero():
    a = mp.mpf("2.25")
    b = mp.mpf("1.5")
    lower = beta(_mp_text(a), _mp_text(b), dps=90, mode="certified")
    upper = beta(_mp_text(a + 1), _mp_text(b), dps=90, mode="certified")
    _require_certified(lower, upper)

    _assert_contains_zero(_sub(_ball(upper), _scale(a / (a + b), _ball(lower))))


def test_certified_beta_second_argument_recurrence_contains_zero():
    a = mp.mpf("2.25")
    b = mp.mpf("1.5")
    lower = beta(_mp_text(a), _mp_text(b), dps=90, mode="certified")
    shifted = beta(_mp_text(a), _mp_text(b + 1), dps=90, mode="certified")
    _require_certified(lower, shifted)

    _assert_contains_zero(_sub(_ball(shifted), _scale(b / (a + b), _ball(lower))))


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
