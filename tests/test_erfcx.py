import pytest

from certsf import SFResult, erfc, erfcx

mp = pytest.importorskip("mpmath")
mp.mp.dps = 120


def test_erfcx_zero():
    result = erfcx("0", dps=80, mode="high_precision")

    assert result.function == "erfcx"
    assert _mp_number(result.value) == 1


@pytest.mark.parametrize(
    ("z", "expected"),
    [
        pytest.param("1", mp.e * mp.erfc(1), id="positive-real"),
        pytest.param("-1", mp.e * mp.erfc(-1), id="negative-real"),
    ],
)
def test_erfcx_regular_real_values(z, expected):
    result = erfcx(z, dps=80, mode="high_precision")

    _assert_close(_mp_number(result.value), expected, mp.mpf("1e-75"))


def test_erfcx_complex_regular_sample():
    z = "0.5+0.25j"
    zz = mp.mpc("0.5", "0.25")
    result = erfcx(z, dps=80, mode="high_precision")

    _assert_close(_mp_number(result.value), mp.exp(zz * zz) * mp.erfc(zz), mp.mpf("1e-75"))


def test_erfcx_high_precision_identity():
    z = "0.75"
    zz = mp.mpf(z)
    erfcx_result = erfcx(z, dps=80, mode="high_precision")
    erfc_result = erfc(z, dps=80, mode="high_precision")

    _assert_close(_mp_number(erfcx_result.value), mp.exp(zz * zz) * _mp_number(erfc_result.value), mp.mpf("1e-75"))


def test_erfcx_auto_dispatch_behavior():
    fast = erfcx("1", dps=15, mode="auto")
    high_precision = erfcx("1", dps=50, mode="auto")
    certified = erfcx("1", dps=50, mode="auto", certify=True)

    assert fast.backend == "scipy"
    assert high_precision.backend == "mpmath"
    assert certified.backend == "python-flint"
    assert certified.diagnostics["mode"] == "certified"


def test_erfcx_all_modes_return_sfresult():
    for mode in ("fast", "high_precision", "certified", "auto"):
        result = erfcx("1", dps=40, mode=mode)
        assert isinstance(result, SFResult)
        assert result.function == "erfcx"


def test_certified_erfcx_identity_contains_zero():
    z_text = "0.5+0.25j"
    z = mp.mpc("0.5", "0.25")
    erfc_result = erfc(z_text, dps=90, mode="certified")
    erfcx_result = erfcx(z_text, dps=90, mode="certified")
    _require_certified(erfc_result, erfcx_result)

    factor = mp.exp(z * z)
    residual = factor * _ball(erfc_result)[0] - _ball(erfcx_result)[0]
    bound = abs(factor) * _ball(erfc_result)[1] + _ball(erfcx_result)[1] + mp.mpf("1e-100")

    assert abs(residual) <= bound


def test_certified_erfcx_scope_and_diagnostics_are_narrow():
    result = erfcx("1", dps=60, mode="certified")
    _require_certified(result)

    assert result.diagnostics["certificate_scope"] in {"direct_arb_erfcx", "arb_erfcx_formula"}
    if result.diagnostics["certificate_scope"] == "direct_arb_erfcx":
        assert result.diagnostics["certificate_level"] == "direct_arb_primitive"
        assert result.diagnostics["audit_status"] == "audited_direct"
    else:
        assert result.diagnostics["certificate_level"] == "formula_audited_alpha"
        assert result.diagnostics["audit_status"] == "formula_identity"
        assert result.diagnostics["formula"] == "exp(z^2)*erfc(z)"
        assert result.diagnostics["certification_claim"] == "certified Arb enclosure of exp(z^2)*erfc(z)"


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
