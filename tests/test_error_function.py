import pytest

from certsf import SFResult, erf, erfc

mp = pytest.importorskip("mpmath")
mp.mp.dps = 120


def test_erf_zero():
    result = erf("0", dps=80, mode="high_precision")

    assert result.function == "erf"
    assert _mp_number(result.value) == 0


def test_erfc_zero():
    result = erfc("0", dps=80, mode="high_precision")

    assert result.function == "erfc"
    assert _mp_number(result.value) == 1


def test_erf_one_regular_real_value():
    result = erf("1", dps=80, mode="high_precision")

    _assert_close(_mp_number(result.value), mp.erf(1), mp.mpf("1e-75"))


def test_erfc_one_regular_real_value():
    result = erfc("1", dps=80, mode="high_precision")

    _assert_close(_mp_number(result.value), mp.erfc(1), mp.mpf("1e-75"))


def test_erf_is_odd():
    x = mp.mpf("1.25")
    positive = erf(_mp_text(x), dps=80, mode="high_precision")
    negative = erf(_mp_text(-x), dps=80, mode="high_precision")

    _assert_close(_mp_number(negative.value), -_mp_number(positive.value), mp.mpf("1e-75"))


def test_erfc_is_one_minus_erf():
    x = mp.mpf("0.75")
    erf_result = erf(_mp_text(x), dps=80, mode="high_precision")
    erfc_result = erfc(_mp_text(x), dps=80, mode="high_precision")

    _assert_close(_mp_number(erfc_result.value), 1 - _mp_number(erf_result.value), mp.mpf("1e-75"))


def test_complex_regular_sample():
    z = "0.5+0.25j"
    erf_result = erf(z, dps=80, mode="high_precision")
    erfc_result = erfc(z, dps=80, mode="high_precision")
    zz = mp.mpc("0.5", "0.25")

    _assert_close(_mp_number(erf_result.value), mp.erf(zz), mp.mpf("1e-75"))
    _assert_close(_mp_number(erfc_result.value), mp.erfc(zz), mp.mpf("1e-75"))


def test_error_function_auto_dispatch_behavior():
    fast = erf("1", dps=15, mode="auto")
    high_precision = erf("1", dps=50, mode="auto")
    certified = erf("1", dps=50, mode="auto", certify=True)

    assert fast.backend == "scipy"
    assert high_precision.backend == "mpmath"
    assert certified.backend == "python-flint"
    assert certified.diagnostics["mode"] == "certified"


@pytest.mark.parametrize("function", [erf, erfc])
def test_error_function_all_modes_return_sfresult(function):
    for mode in ("fast", "high_precision", "certified", "auto"):
        result = function("1", dps=40, mode=mode)
        assert isinstance(result, SFResult)
        assert result.function == function.__name__


def test_certified_erf_erfc_identity_contains_one():
    z = "0.5+0.25j"
    erf_result = erf(z, dps=90, mode="certified")
    erfc_result = erfc(z, dps=90, mode="certified")
    _require_certified(erf_result, erfc_result)

    _assert_contains_constant(_add(_ball(erf_result), _ball(erfc_result)), mp.mpf(1))


def test_certified_erf_oddness_contains_zero():
    z = "0.5+0.25j"
    positive = erf(z, dps=90, mode="certified")
    negative = erf("-0.5-0.25j", dps=90, mode="certified")
    _require_certified(positive, negative)

    _assert_contains_zero(_add(_ball(positive), _ball(negative)))


def test_certified_error_function_scopes_are_narrow():
    erf_result = erf("1", dps=60, mode="certified")
    erfc_result = erfc("1", dps=60, mode="certified")
    _require_certified(erf_result, erfc_result)

    assert erf_result.diagnostics["certificate_scope"] == "direct_arb_erf"
    assert erfc_result.diagnostics["certificate_scope"] == "direct_arb_erfc"
    assert erf_result.diagnostics["audit_status"] == "audited_direct"
    assert erfc_result.diagnostics["audit_status"] == "audited_direct"


def _require_certified(*results):
    for result in results:
        if not result.certified:
            pytest.skip(result.diagnostics.get("error", "certified backend unavailable"))


def _assert_close(left, right, tolerance):
    assert abs(left - right) <= tolerance


def _assert_contains_zero(ball):
    assert abs(ball[0]) <= ball[1]


def _assert_contains_constant(ball, constant):
    assert abs(ball[0] - constant) <= ball[1]


def _ball(result):
    return _mp_number(result.value), _mp_number(result.abs_error_bound)


def _add(left, right):
    return left[0] + right[0], left[1] + right[1]


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
