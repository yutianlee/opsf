import pytest

from certsf import SFResult, erf, erfinv, mcp_server
from certsf.backends import arb_backend

mp = pytest.importorskip("mpmath")
mp.mp.dps = 120


def test_erfinv_zero():
    result = erfinv("0", dps=80, mode="high_precision")

    assert result.function == "erfinv"
    assert _mp_number(result.value) == 0


@pytest.mark.parametrize("x", ["0.5", "-0.5", "0.9", "-0.9"])
def test_erf_of_erfinv_matches_input(x):
    inverse = erfinv(x, dps=80, mode="high_precision")
    composed = erf(inverse.value, dps=80, mode="high_precision")

    _assert_close(_mp_number(composed.value), mp.mpf(x), mp.mpf("1e-75"))


def test_erfinv_is_odd():
    positive = erfinv("0.75", dps=80, mode="high_precision")
    negative = erfinv("-0.75", dps=80, mode="high_precision")

    _assert_close(_mp_number(negative.value), -_mp_number(positive.value), mp.mpf("1e-75"))


@pytest.mark.parametrize("x", ["1", "-1", "1.1", "-1.1"])
def test_certified_erfinv_rejects_closed_or_outside_domain(x):
    result = erfinv(x, dps=50, mode="certified")

    assert result.certified is False
    assert result.value == ""
    assert result.abs_error_bound is None
    assert result.rel_error_bound is None
    assert result.backend == "python-flint"
    assert result.method == "arb_ball"
    assert result.diagnostics["mode"] == "certified"
    assert result.diagnostics["certificate_scope"] == "arb_erfinv_real_root"
    assert result.diagnostics["domain"] == "real_x_in_open_interval_minus1_1"
    assert "error" in result.diagnostics


def test_certified_erfinv_rejects_complex_input():
    result = erfinv("0.5+0.25j", dps=50, mode="certified")

    assert result.certified is False
    assert result.value == ""
    assert result.diagnostics["mode"] == "certified"
    assert result.diagnostics["certificate_scope"] == "arb_erfinv_real_root"
    assert result.diagnostics["domain"] == "real_x_in_open_interval_minus1_1"
    assert "complex inverse branches are not certified" in result.diagnostics["error"]


def test_erfinv_auto_dispatch_behavior():
    fast = erfinv("0.5", dps=15, mode="auto")
    high_precision = erfinv("0.5", dps=50, mode="auto")
    certified = erfinv("0.5", dps=50, mode="auto", certify=True)

    assert fast.backend == "scipy"
    assert high_precision.backend == "mpmath"
    assert certified.backend == "python-flint"
    assert certified.diagnostics["mode"] == "certified"


def test_erfinv_all_modes_return_sfresult():
    for mode in ("fast", "high_precision", "certified", "auto"):
        result = erfinv("0.5", dps=40, mode=mode)
        assert isinstance(result, SFResult)
        assert result.function == "erfinv"


def test_special_erfinv_mcp_tool_matches_python_api():
    payload = mcp_server.special_erfinv("0.5", dps=50, mode="high_precision")

    assert payload == erfinv("0.5", dps=50, mode="high_precision").to_mcp_dict()
    assert payload["function"] == "erfinv"
    assert payload["backend"] == "mpmath"


@pytest.mark.parametrize("x", ["0.5", "-0.5", "0.9", "-0.9"])
def test_certified_erfinv_residual_contains_zero(x):
    flint = pytest.importorskip("flint")
    result = erfinv(x, dps=90, mode="certified")
    _require_certified(result)

    old_prec = flint.ctx.prec
    flint.ctx.prec = 400
    try:
        y_ball = flint.arb(result.value, result.abs_error_bound)
        residual = y_ball.erf() - flint.arb(x)
        assert residual.contains(0)
    finally:
        flint.ctx.prec = old_prec


def test_certified_erfinv_scope_and_diagnostics_are_narrow():
    result = erfinv("0.5", dps=60, mode="certified")
    _require_certified(result)

    assert result.diagnostics["certificate_scope"] in {"direct_arb_erfinv", "arb_erfinv_real_root"}
    assert result.diagnostics["domain"] == "real_x_in_open_interval_minus1_1"
    assert result.diagnostics["branch"] == "real_principal_inverse"
    if result.diagnostics["certificate_scope"] == "direct_arb_erfinv":
        assert result.diagnostics["certificate_level"] == "direct_arb_primitive"
        assert result.diagnostics["audit_status"] == "audited_direct"
        assert "real principal erfinv(x)" in result.diagnostics["certification_claim"]
    else:
        assert result.diagnostics["certificate_level"] == "certified_real_root"
        assert result.diagnostics["audit_status"] == "monotone_real_inverse"
        assert result.diagnostics["formula"] == "erf(y)-x=0"


def test_erfinv_real_root_fallback_records_certified_method(monkeypatch):
    pytest.importorskip("flint")
    monkeypatch.setattr(arb_backend, "_direct_arb_erfinv_method", lambda _argument: None)

    result = arb_backend.arb_erfinv("0.5", dps=50)

    _require_certified(result)
    assert result.diagnostics["certificate_scope"] == "arb_erfinv_real_root"
    assert result.diagnostics["certificate_level"] == "certified_real_root"
    assert result.diagnostics["audit_status"] == "monotone_real_inverse"
    assert result.diagnostics["domain"] == "real_x_in_open_interval_minus1_1"
    assert result.diagnostics["formula"] == "erf(y)-x=0"
    assert result.diagnostics["iterations"] > 0


def _require_certified(*results):
    for result in results:
        if not result.certified:
            pytest.skip(result.diagnostics.get("error", "certified backend unavailable"))


def _assert_close(left, right, tolerance):
    assert abs(left - right) <= tolerance


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
