import json

import pytest

from certsf import besselj, gamma, pbdv, pcfd, pcfu, pcfv, pcfw

mp = pytest.importorskip("mpmath")
mp.mp.dps = 140

EXPERIMENTAL_LEVEL = "formula_audited_experimental"
EXPERIMENTAL_STATUS = "experimental_formula"
EXPERIMENTAL_CLAIM = "certified Arb enclosure of the implemented documented formula; formula audit in progress"


@pytest.mark.parametrize(
    ("parameter_text", "z_text"),
    [
        pytest.param("0.125", "0.125", id="real-small"),
        pytest.param("2.5", "1.25", id="real-moderate"),
        pytest.param("0.7", "-1.1", id="negative-real-argument"),
        pytest.param("0.7", "-1.1+1e-20j", id="upper-negative-real-branch-side"),
        pytest.param("0.7", "-1.1-1e-20j", id="lower-negative-real-branch-side"),
        pytest.param("-0.49999999999999999999", "0.375", id="near-u-prime-zero-rgamma-cancel"),
        pytest.param("-1.49999999999999999999", "-0.875", id="near-u-zero-rgamma-cancel"),
        pytest.param("1.5", "8.0", id="large-real-argument"),
        pytest.param("1.5", "-8.0-1e-12j", id="large-lower-branch-side"),
    ],
)
def test_certified_pcfu_audit_grid_recurrence_residual_contains_zero(parameter_text, z_text):
    parameter = mp.mpf(parameter_text)
    z = _mp_number(z_text)
    lower = pcfu(_mp_text(parameter - 1), z_text, dps=90, mode="certified")
    center = pcfu(parameter_text, z_text, dps=90, mode="certified")
    upper = pcfu(_mp_text(parameter + 1), z_text, dps=90, mode="certified")
    _require_certified(lower, center, upper)

    _assert_experimental_formula_metadata(center, "pcfu_1f1_global")
    residual = _add(
        _sub(_scale(z, _ball(center)), _ball(lower)),
        _scale(parameter + mp.mpf("0.5"), _ball(upper)),
    )
    _assert_contains_zero(residual)


@pytest.mark.parametrize(
    ("order_text", "z_text"),
    [
        pytest.param("0.125", "0.125", id="real-small"),
        pytest.param("2.5", "1.25", id="real-moderate"),
        pytest.param("0.7", "-1.1", id="negative-real-argument"),
        pytest.param("0.7", "-1.1+1e-20j", id="upper-negative-real-branch-side"),
        pytest.param("-1.25", "-0.25-1.75j", id="lower-complex-branch-side"),
        pytest.param("-0.00000000000000000001", "0.375", id="near-underlying-u-prime-cancel"),
        pytest.param("1.00000000000000000001", "-0.875", id="near-underlying-u-zero-cancel"),
        pytest.param("1.5", "8.0", id="large-real-argument"),
    ],
)
def test_certified_pcfd_audit_grid_direct_recurrence_residual_contains_zero(order_text, z_text):
    order = mp.mpf(order_text)
    z = _mp_number(z_text)
    lower = pcfd(_mp_text(order - 1), z_text, dps=90, mode="certified")
    center = pcfd(order_text, z_text, dps=90, mode="certified")
    upper = pcfd(_mp_text(order + 1), z_text, dps=90, mode="certified")
    _require_certified(lower, center, upper)

    _assert_experimental_formula_metadata(center, "pcfd_via_pcfu")
    residual = _add(_sub(_ball(upper), _scale(z, _ball(center))), _scale(order, _ball(lower)))
    _assert_contains_zero(residual)


@pytest.mark.parametrize(
    ("order_text", "z_text"),
    [
        pytest.param("0.125", "0.125", id="real-small"),
        pytest.param("2.5", "1.25", id="real-moderate"),
        pytest.param("0.7", "-1.1", id="negative-real-argument"),
        pytest.param("0.7", "-1.1+1e-20j", id="upper-negative-real-branch-side"),
        pytest.param("-1.25", "-0.25-1.75j", id="lower-complex-branch-side"),
        pytest.param("-0.00000000000000000001", "0.375", id="near-underlying-u-prime-cancel"),
        pytest.param("1.00000000000000000001", "-0.875", id="near-underlying-u-zero-cancel"),
        pytest.param("1.5", "8.0", id="large-real-argument"),
    ],
)
def test_certified_pbdv_audit_grid_value_and_derivative_residuals_contain_zero(order_text, z_text):
    order = mp.mpf(order_text)
    z = _mp_number(z_text)
    result = pbdv(order_text, z_text, dps=90, mode="certified")
    pcfd_value = pcfd(order_text, z_text, dps=90, mode="certified")
    pcfd_next = pcfd(_mp_text(order + 1), z_text, dps=90, mode="certified")
    _require_certified(result, pcfd_value, pcfd_next)

    _assert_experimental_formula_metadata(result, "pcfd_via_pcfu")
    _assert_contains_zero(_sub(_component_ball(result, "value"), _ball(pcfd_value)))

    derivative_residual = _sub(
        _component_ball(result, "derivative"),
        _sub(_scale(z / 2, _component_ball(result, "value")), _ball(pcfd_next)),
    )
    _assert_contains_zero(derivative_residual)


@pytest.mark.parametrize(
    ("parameter_text", "z_text"),
    [
        pytest.param("0.125", "0.125", id="real-small"),
        pytest.param("2.5", "1.25", id="real-moderate"),
        pytest.param("0.7", "-1.1", id="negative-real-argument"),
        pytest.param("0.7", "-1.1+1e-20j", id="upper-negative-real-branch-side"),
        pytest.param("0.7", "-1.1-1e-20j", id="lower-negative-real-branch-side"),
        pytest.param("0.49999999999999999999", "0.375", id="near-term1-rgamma-cancel"),
        pytest.param("1.50000000000000000001", "-0.875", id="near-higher-term1-rgamma-cancel"),
        pytest.param("1.5", "8.0", id="large-real-argument"),
    ],
)
def test_certified_pcfv_audit_grid_connection_and_recurrence_residuals_contain_zero(parameter_text, z_text):
    parameter = mp.mpf(parameter_text)
    z = _mp_number(z_text)
    u_same = pcfu(parameter_text, z_text, dps=90, mode="certified")
    u_rotated = pcfu(_mp_text(-parameter), _mp_text(mp.j * z), dps=90, mode="certified")
    v_lower = pcfv(_mp_text(parameter - 1), z_text, dps=90, mode="certified")
    v_center = pcfv(parameter_text, z_text, dps=90, mode="certified")
    v_upper = pcfv(_mp_text(parameter + 1), z_text, dps=90, mode="certified")
    _require_certified(u_same, u_rotated, v_lower, v_center, v_upper)

    _assert_experimental_formula_metadata(v_center, "pcfv_dlmf_connection")
    rgamma_factor = mp.rgamma(mp.mpf("0.5") - parameter)
    phase = mp.exp(-mp.j * mp.pi * (parameter / 2 - mp.mpf("0.25")))
    connection_residual = _sub(
        _ball(v_center),
        _add(
            _scale(-mp.j * rgamma_factor, _ball(u_same)),
            _scale(mp.sqrt(2 / mp.pi) * phase, _ball(u_rotated)),
        ),
    )
    _assert_contains_zero(connection_residual)

    recurrence_residual = _add(
        _sub(_scale(z, _ball(v_center)), _ball(v_upper)),
        _scale(parameter - mp.mpf("0.5"), _ball(v_lower)),
    )
    _assert_contains_zero(recurrence_residual)


@pytest.mark.parametrize(
    ("x_text", "sign"),
    [
        pytest.param("0.125", 1, id="real-small-positive"),
        pytest.param("0.125", -1, id="real-small-negative"),
        pytest.param("1.25", 1, id="real-moderate-positive"),
        pytest.param("1.25", -1, id="real-moderate-negative"),
        pytest.param("8.0", 1, id="large-positive"),
        pytest.param("8.0", -1, id="large-negative"),
    ],
)
def test_certified_pcfw_zero_parameter_bessel_identity_residual_contains_zero(x_text, sign):
    x = mp.mpf(x_text)
    signed_x = sign * x
    w_result = pcfw("0", _mp_text(signed_x), dps=90, mode="certified")
    j_minus = besselj("-0.25", _mp_text(x * x / 4), dps=90, mode="certified")
    j_plus = besselj("0.25", _mp_text(x * x / 4), dps=90, mode="certified")
    _require_certified(w_result, j_minus, j_plus)

    _assert_experimental_formula_metadata(w_result, "pcfw_dlmf_12_14_real_connection")
    coefficient = 2 ** (-mp.mpf(5) / 4) * mp.sqrt(mp.pi * x)
    if sign > 0:
        bessel_combination = _sub(_ball(j_minus), _ball(j_plus))
    else:
        bessel_combination = _add(_ball(j_minus), _ball(j_plus))
    residual = _sub(_ball(w_result), _scale(coefficient, bessel_combination))
    _assert_contains_zero(residual)


@pytest.mark.parametrize(
    "parameter_text",
    [
        pytest.param("-4.0", id="large-negative-parameter"),
        pytest.param("-0.00000000000000000001", id="near-zero-phase-negative"),
        pytest.param("0", id="zero-phase"),
        pytest.param("0.00000000000000000001", id="near-zero-phase-positive"),
        pytest.param("4.0", id="large-positive-parameter"),
    ],
)
def test_certified_pcfw_origin_gamma_modulus_identity_intervals_overlap(parameter_text):
    parameter = mp.mpf(parameter_text)
    numerator = gamma(_mp_text(mp.mpf("0.25") + mp.j * parameter / 2), dps=90, mode="certified")
    denominator = gamma(_mp_text(mp.mpf("0.75") + mp.j * parameter / 2), dps=90, mode="certified")
    w_result = pcfw(parameter_text, "0", dps=90, mode="certified")
    _require_certified(numerator, denominator, w_result)

    _assert_experimental_formula_metadata(w_result, "pcfw_dlmf_12_14_real_connection")
    formula_interval = _pcfw_origin_formula_interval(_ball(numerator), _ball(denominator))
    w_interval = _real_interval(_ball(w_result))
    assert formula_interval[0] <= w_interval[1]
    assert w_interval[0] <= formula_interval[1]


def _pcfw_origin_formula_interval(numerator, denominator):
    numerator_center, numerator_radius = numerator
    denominator_center, denominator_radius = denominator
    denominator_abs = abs(denominator_center)
    assert denominator_abs > denominator_radius

    ratio_center = numerator_center / denominator_center
    ratio_radius = (
        abs(numerator_center) * denominator_radius + denominator_abs * numerator_radius
    ) / (denominator_abs * (denominator_abs - denominator_radius))
    ratio_abs_low = max(mp.mpf("0"), abs(ratio_center) - ratio_radius)
    ratio_abs_high = abs(ratio_center) + ratio_radius
    coefficient = 2 ** (-mp.mpf(3) / 4)
    return coefficient * mp.sqrt(ratio_abs_low), coefficient * mp.sqrt(ratio_abs_high)


def _assert_experimental_formula_metadata(result, formula):
    assert result.diagnostics["formula"] == formula
    assert result.diagnostics["certificate_level"] == EXPERIMENTAL_LEVEL
    assert result.diagnostics["audit_status"] == EXPERIMENTAL_STATUS
    assert result.diagnostics["certification_claim"] == EXPERIMENTAL_CLAIM


def _require_certified(*results):
    for result in results:
        if not result.certified:
            pytest.skip(result.diagnostics.get("error", "certified backend unavailable"))


def _assert_contains_zero(ball):
    assert abs(ball[0]) <= ball[1]


def _ball(result):
    return _mp_number(result.value), _mp_number(result.abs_error_bound)


def _component_ball(result, component):
    values = json.loads(result.value)
    radii = json.loads(result.abs_error_bound)
    return _mp_number(values[component]), _mp_number(radii[component])


def _real_interval(ball):
    center, radius = ball
    assert abs(mp.im(center)) <= radius
    real_center = mp.re(center)
    return real_center - radius, real_center + radius


def _add(left, right):
    return left[0] + right[0], left[1] + right[1]


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
