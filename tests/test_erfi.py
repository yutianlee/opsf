import pytest

from certsf import SFResult, erf, erfi

mp = pytest.importorskip("mpmath")
mp.mp.dps = 120


def test_erfi_zero():
    result = erfi("0", dps=80, mode="high_precision")

    assert result.function == "erfi"
    assert _mp_number(result.value) == 0


def test_erfi_one_regular_real_value():
    result = erfi("1", dps=80, mode="high_precision")

    _assert_close(_mp_number(result.value), mp.erfi(1), mp.mpf("1e-75"))


def test_erfi_is_odd():
    positive = erfi("1", dps=80, mode="high_precision")
    negative = erfi("-1", dps=80, mode="high_precision")

    _assert_close(_mp_number(negative.value), -_mp_number(positive.value), mp.mpf("1e-75"))


def test_erfi_complex_regular_sample():
    z = "0.5+0.25j"
    zz = mp.mpc("0.5", "0.25")
    result = erfi(z, dps=80, mode="high_precision")

    _assert_close(_mp_number(result.value), mp.erfi(zz), mp.mpf("1e-75"))


def test_erfi_high_precision_identity():
    z = "0.5+0.25j"
    iz = "-0.25+0.5j"
    result = erfi(z, dps=80, mode="high_precision")
    erf_result = erf(iz, dps=80, mode="high_precision")

    _assert_close(_mp_number(result.value), -mp.j * _mp_number(erf_result.value), mp.mpf("1e-75"))


def test_erfi_auto_dispatch_behavior():
    fast = erfi("1", dps=15, mode="auto")
    high_precision = erfi("1", dps=50, mode="auto")
    certified = erfi("1", dps=50, mode="auto", certify=True)

    assert fast.backend == "scipy"
    assert high_precision.backend == "mpmath"
    assert certified.backend == "python-flint"
    assert certified.diagnostics["mode"] == "certified"


def test_erfi_all_modes_return_sfresult():
    for mode in ("fast", "high_precision", "certified", "auto"):
        result = erfi("1", dps=40, mode=mode)
        assert isinstance(result, SFResult)
        assert result.function == "erfi"


def test_certified_erfi_identity_contains_zero():
    erfi_result = erfi("0.5+0.25j", dps=90, mode="certified")
    erf_result = erf("-0.25+0.5j", dps=90, mode="certified")
    _require_certified(erfi_result, erf_result)

    residual = _ball(erfi_result)[0] + mp.j * _ball(erf_result)[0]
    bound = _ball(erfi_result)[1] + _ball(erf_result)[1] + mp.mpf("1e-100")

    assert abs(residual) <= bound


def test_certified_erfi_scope_and_diagnostics_are_narrow():
    result = erfi("1", dps=60, mode="certified")
    _require_certified(result)

    assert result.diagnostics["certificate_scope"] in {"direct_arb_erfi", "arb_erfi_formula"}
    if result.diagnostics["certificate_scope"] == "direct_arb_erfi":
        assert result.diagnostics["certificate_level"] == "direct_arb_primitive"
        assert result.diagnostics["audit_status"] == "audited_direct"
        assert "erfi(z)" in result.diagnostics["certification_claim"]
    else:
        assert result.diagnostics["certificate_level"] == "formula_audited_alpha"
        assert result.diagnostics["audit_status"] == "formula_identity"
        assert result.diagnostics["formula"] == "-i*erf(i*z)"
        assert result.diagnostics["certification_claim"] == "certified Arb enclosure of -i*erf(i*z)"


def _require_certified(*results):
    for result in results:
        if not result.certified:
            pytest.skip(result.diagnostics.get("error", "certified backend unavailable"))


def _assert_close(left, right, tolerance):
    assert abs(left - right) <= tolerance


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
