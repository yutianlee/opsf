import json

import pytest

from certsf import ai, besselj, besseli, besselk, bessely, bi, gamma, pbdv, pcfd, pcfu, rgamma

mp = pytest.importorskip("mpmath")
mp.mp.dps = 120


def test_certified_gamma_balls_imply_recurrence_and_reciprocal_identity():
    z = mp.mpf("2.5")
    gamma_z_result = gamma(str(z), dps=90, mode="certified")
    gamma_next_result = gamma(str(z + 1), dps=90, mode="certified")
    rgamma_z_result = rgamma(str(z), dps=90, mode="certified")
    _require_certified(gamma_z_result, gamma_next_result, rgamma_z_result)

    gamma_z = _ball(gamma_z_result)
    gamma_next = _ball(gamma_next_result)
    rgamma_z = _ball(rgamma_z_result)

    _assert_contains_zero(_sub(gamma_next, _scale(z, gamma_z)))
    _assert_contains_constant(_mul(gamma_z, rgamma_z), mp.mpf(1))


def test_certified_rgamma_poles_are_exact_zero_balls():
    results = [rgamma(z, dps=90, mode="certified") for z in ("0", "-1", "-2")]
    _require_certified(*results)

    for result in results:
        pole_zero = _ball(result)
        assert pole_zero == (mp.mpf(0), mp.mpf(0))


def test_certified_airy_balls_imply_wronskian_constant():
    z = "2.5"
    ai_result = ai(z, dps=90, mode="certified")
    aip_result = ai(z, derivative=1, dps=90, mode="certified")
    bi_result = bi(z, dps=90, mode="certified")
    bip_result = bi(z, derivative=1, dps=90, mode="certified")
    _require_certified(ai_result, aip_result, bi_result, bip_result)

    wronskian = _sub(_mul(_ball(ai_result), _ball(bip_result)), _mul(_ball(aip_result), _ball(bi_result)))
    _assert_contains_constant(wronskian, 1 / mp.pi)


@pytest.mark.parametrize(
    ("function", "upper_coefficient"),
    [
        pytest.param(besselj, 1, id="besselj"),
        pytest.param(besseli, -1, id="besseli"),
    ],
)
def test_certified_bessel_balls_imply_three_term_recurrences(function, upper_coefficient):
    order = mp.mpf("2.5")
    z = mp.mpf("3.75")
    lower_result = function(str(order - 1), str(z), dps=90, mode="certified")
    center_result = function(str(order), str(z), dps=90, mode="certified")
    upper_result = function(str(order + 1), str(z), dps=90, mode="certified")
    _require_certified(lower_result, center_result, upper_result)

    residual = _add(
        _sub(_ball(lower_result), _scale(2 * order / z, _ball(center_result))),
        _scale(upper_coefficient, _ball(upper_result)),
    )
    _assert_contains_zero(residual)


def test_certified_bessel_jy_balls_imply_wronskian_constant():
    order = mp.mpf("2")
    z = mp.mpf("3.75")
    j_result = besselj(str(order), str(z), dps=90, mode="certified")
    y_result = bessely(str(order), str(z), dps=90, mode="certified")
    _require_certified(j_result, y_result)

    j_prime = _ordinary_bessel_derivative_ball(besselj, order, z)
    y_prime = _ordinary_bessel_derivative_ball(bessely, order, z)
    wronskian = _sub(_mul(_ball(j_result), y_prime), _mul(j_prime, _ball(y_result)))
    _assert_contains_constant(wronskian, 2 / (mp.pi * z))


def test_certified_bessel_ik_balls_imply_wronskian_constant():
    order = mp.mpf("2")
    z = mp.mpf("3.75")
    i_result = besseli(str(order), str(z), dps=90, mode="certified")
    k_result = besselk(str(order), str(z), dps=90, mode="certified")
    _require_certified(i_result, k_result)

    i_prime = _modified_bessel_i_derivative_ball(order, z)
    k_prime = _modified_bessel_k_derivative_ball(order, z)
    wronskian = _sub(_mul(_ball(i_result), k_prime), _mul(i_prime, _ball(k_result)))
    _assert_contains_constant(wronskian, -1 / z)


def test_certified_parabolic_cylinder_balls_imply_derivative_relation():
    order = mp.mpf("2.5")
    z = mp.mpf("1.25")
    result = pbdv(str(order), str(z), dps=90, mode="certified")
    next_result = pcfd(str(order + 1), str(z), dps=90, mode="certified")
    _require_certified(result, next_result)

    value = _component_ball(result, "value")
    derivative = _component_ball(result, "derivative")
    residual = _sub(derivative, _sub(_scale(z / 2, value), _ball(next_result)))
    _assert_contains_zero(residual)


def test_certified_parabolic_cylinder_balls_imply_u_d_connection():
    order = mp.mpf("1.25")
    z = mp.mpf("0.75")
    d_result = pcfd(str(order), str(z), dps=90, mode="certified")
    u_result = pcfu(str(-order - mp.mpf("0.5")), str(z), dps=90, mode="certified")
    _require_certified(d_result, u_result)

    _assert_contains_zero(_sub(_ball(d_result), _ball(u_result)))


def test_certified_parabolic_cylinder_balls_imply_differential_equation_residual():
    order = mp.mpf("0.7")
    z = mp.mpf("1.1")
    d0_result = pcfd(str(order), str(z), dps=90, mode="certified")
    d1_result = pcfd(str(order + 1), str(z), dps=90, mode="certified")
    d2_result = pcfd(str(order + 2), str(z), dps=90, mode="certified")
    _require_certified(d0_result, d1_result, d2_result)

    # This is the D_v differential-equation residual after substituting the
    # certified derivative identity D_v' = z/2 D_v - D_(v+1).
    residual = _add(_sub(_scale(order + 1, _ball(d0_result)), _scale(z, _ball(d1_result))), _ball(d2_result))
    _assert_contains_zero(residual)


def _ordinary_bessel_derivative_ball(function, order, z):
    lower_result = function(str(order - 1), str(z), dps=90, mode="certified")
    upper_result = function(str(order + 1), str(z), dps=90, mode="certified")
    _require_certified(lower_result, upper_result)
    return _scale(mp.mpf("0.5"), _sub(_ball(lower_result), _ball(upper_result)))


def _modified_bessel_i_derivative_ball(order, z):
    lower_result = besseli(str(order - 1), str(z), dps=90, mode="certified")
    upper_result = besseli(str(order + 1), str(z), dps=90, mode="certified")
    _require_certified(lower_result, upper_result)
    return _scale(mp.mpf("0.5"), _add(_ball(lower_result), _ball(upper_result)))


def _modified_bessel_k_derivative_ball(order, z):
    lower_result = besselk(str(order - 1), str(z), dps=90, mode="certified")
    upper_result = besselk(str(order + 1), str(z), dps=90, mode="certified")
    _require_certified(lower_result, upper_result)
    return _scale(mp.mpf("-0.5"), _add(_ball(lower_result), _ball(upper_result)))


def _require_certified(*results):
    for result in results:
        if not result.certified:
            pytest.skip(result.diagnostics.get("error", "certified backend unavailable"))


def _assert_contains_zero(ball):
    assert abs(ball[0]) <= ball[1]


def _assert_contains_constant(ball, constant):
    assert abs(ball[0] - constant) <= ball[1]


def _ball(result):
    return _mp_number(result.value), _mp_number(result.abs_error_bound)


def _component_ball(result, component):
    values = json.loads(result.value)
    radii = json.loads(result.abs_error_bound)
    return _mp_number(values[component]), _mp_number(radii[component])


def _add(left, right):
    return left[0] + right[0], left[1] + right[1]


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
