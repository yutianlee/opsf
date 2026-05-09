import pytest

from certsf import SFResult, dawson, erfi, mcp_server
from certsf.backends import arb_backend

mp = pytest.importorskip("mpmath")
mp.mp.dps = 140

DAWSON_FORMULA = "sqrt(pi)/2*exp(-z^2)*erfi(z)"
DAWSON_FORMULA_CLAIM = "certified Arb enclosure of sqrt(pi)/2*exp(-z^2)*erfi(z)"


def test_dawson_zero():
    result = dawson("0", dps=80, mode="high_precision")

    assert result.function == "dawson"
    assert _mp_number(result.value) == 0


def test_dawson_is_odd():
    positive = dawson("1.25", dps=80, mode="high_precision")
    negative = dawson("-1.25", dps=80, mode="high_precision")

    _assert_close(_mp_number(negative.value), -_mp_number(positive.value), mp.mpf("1e-75"))


def test_dawson_one_regular_real_value():
    result = dawson("1", dps=80, mode="high_precision")

    _assert_close(_mp_number(result.value), _dawson_formula(mp.mpf(1)), mp.mpf("1e-75"))


def test_dawson_negative_one_matches_oddness():
    positive = dawson("1", dps=80, mode="high_precision")
    negative = dawson("-1", dps=80, mode="high_precision")

    _assert_close(_mp_number(negative.value), -_mp_number(positive.value), mp.mpf("1e-75"))


def test_dawson_complex_regular_sample():
    z = "0.5+0.25j"
    zz = mp.mpc("0.5", "0.25")
    result = dawson(z, dps=80, mode="high_precision")

    _assert_close(_mp_number(result.value), _dawson_formula(zz), mp.mpf("1e-75"))


def test_dawson_high_precision_identity():
    z = "0.5+0.25j"
    zz = mp.mpc("0.5", "0.25")
    dawson_result = dawson(z, dps=80, mode="high_precision")
    erfi_result = erfi(z, dps=80, mode="high_precision")
    expected = mp.sqrt(mp.pi) / 2 * mp.exp(-zz * zz) * _mp_number(erfi_result.value)

    _assert_close(_mp_number(dawson_result.value), expected, mp.mpf("1e-75"))


def test_dawson_auto_dispatch_behavior():
    fast = dawson("1", dps=15, mode="auto")
    high_precision = dawson("1", dps=50, mode="auto")
    certified = dawson("1", dps=50, mode="auto", certify=True)

    assert fast.backend == "scipy"
    assert high_precision.backend == "mpmath"
    assert certified.backend == "python-flint"
    assert certified.diagnostics["mode"] == "certified"


def test_dawson_all_modes_return_sfresult():
    for mode in ("fast", "high_precision", "certified", "auto"):
        result = dawson("1", dps=40, mode=mode)
        assert isinstance(result, SFResult)
        assert result.function == "dawson"


def test_special_dawson_mcp_tool_matches_python_api():
    payload = mcp_server.special_dawson("0.5+0.25j", dps=50, mode="high_precision")

    assert payload == dawson("0.5+0.25j", dps=50, mode="high_precision").to_mcp_dict()
    assert payload["function"] == "dawson"
    assert payload["backend"] == "mpmath"
    assert isinstance(payload["diagnostics"], dict)


def test_certified_dawson_identity_contains_formula_value():
    z = mp.mpc("0.5", "0.25")
    result = dawson(_mp_text(z), dps=90, mode="certified")
    _require_certified(result)

    value, radius = _ball(result)
    reference = _dawson_formula(z)

    assert abs(value - reference) <= radius + mp.mpf("1e-85")


def test_certified_dawson_scope_and_diagnostics_are_narrow():
    result = dawson("1", dps=60, mode="certified")
    _require_certified(result)

    assert result.diagnostics["certificate_scope"] in {"direct_arb_dawson", "arb_dawson_formula"}
    if result.diagnostics["certificate_scope"] == "direct_arb_dawson":
        assert result.diagnostics["certificate_level"] == "direct_arb_primitive"
        assert result.diagnostics["audit_status"] == "audited_direct"
        assert "dawson(z)" in result.diagnostics["certification_claim"]
    else:
        assert result.diagnostics["certificate_level"] == "formula_audited_alpha"
        assert result.diagnostics["audit_status"] == "formula_identity"
        assert result.diagnostics["formula"] == DAWSON_FORMULA
        assert result.diagnostics["certification_claim"] == DAWSON_FORMULA_CLAIM


def test_certified_dawson_nonfinite_output_returns_clean_failure():
    result = dawson("nan", dps=50, mode="certified")
    if _backend_is_unavailable(result):
        pytest.skip(result.diagnostics["error"])

    assert result.certified is False
    assert result.value == ""
    assert result.abs_error_bound is None
    assert result.rel_error_bound is None
    assert result.method == "arb_ball"
    assert result.backend == "python-flint"
    assert result.diagnostics["mode"] == "certified"
    assert result.diagnostics["certificate_scope"] in {"direct_arb_dawson", "arb_dawson_formula"}
    assert "error" in result.diagnostics


def test_dawson_formula_fallback_records_formula_when_direct_dawson_is_unavailable(monkeypatch):
    flint = pytest.importorskip("flint")

    class ErfiOnlyBall:
        def __init__(self, value):
            self.value = flint.acb(value)

        def __mul__(self, other):
            other_value = other.value if isinstance(other, ErfiOnlyBall) else other
            return self.value * other_value

        def erfi(self):
            return self.value.erfi()

    monkeypatch.setattr(arb_backend, "_make_ball", lambda z: ErfiOnlyBall(z))

    result = arb_backend.arb_dawson("0.5", dps=50)

    assert result.certified is True
    assert result.diagnostics["certificate_scope"] == "arb_dawson_formula"
    assert result.diagnostics["certificate_level"] == "formula_audited_alpha"
    assert result.diagnostics["audit_status"] == "formula_identity"
    assert result.diagnostics["formula"] == DAWSON_FORMULA
    assert result.diagnostics["certification_claim"] == DAWSON_FORMULA_CLAIM


def _require_certified(*results):
    for result in results:
        if not result.certified:
            pytest.skip(result.diagnostics.get("error", "certified backend unavailable"))


def _backend_is_unavailable(result):
    return not result.certified and "python-flint is not installed" in result.diagnostics.get("error", "")


def _assert_close(left, right, tolerance):
    assert abs(left - right) <= tolerance


def _dawson_formula(value):
    return mp.sqrt(mp.pi) / 2 * mp.exp(-value * value) * mp.erfi(value)


def _ball(result):
    return _mp_number(result.value), _mp_number(result.abs_error_bound)


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
