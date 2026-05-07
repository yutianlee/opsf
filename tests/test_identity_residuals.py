import json

import pytest

from certsf import ai, besseli, besselj, besselk, bessely, gamma, pbdv, pcfd, pcfu, pcfv, pcfw, rgamma

mp = pytest.importorskip("mpmath")
mp.mp.dps = 100


def test_certified_gamma_recurrence_and_reciprocal_residuals_enclose_zero():
    z = mp.mpf("2.5")
    gamma_z = gamma(str(z), dps=80, mode="certified")
    gamma_next = gamma(str(z + 1), dps=80, mode="certified")
    rgamma_z = rgamma(str(z), dps=80, mode="certified")
    _require_certified(gamma_z, gamma_next, rgamma_z)

    recurrence_residual = _value(gamma_next) - z * _value(gamma_z)
    recurrence_bound = _radius(gamma_next) + abs(z) * _radius(gamma_z)
    _assert_encloses_zero(recurrence_residual, recurrence_bound)

    reciprocal_residual = _value(gamma_z) * _value(rgamma_z) - 1
    reciprocal_bound = (
        abs(_value(gamma_z)) * _radius(rgamma_z)
        + abs(_value(rgamma_z)) * _radius(gamma_z)
        + _radius(gamma_z) * _radius(rgamma_z)
    )
    _assert_encloses_zero(reciprocal_residual, reciprocal_bound)


def test_certified_rgamma_pole_identity_is_exact_zero():
    results = [rgamma(z, dps=80, mode="certified") for z in ("0", "-1", "-2")]
    _require_certified(*results)

    for result in results:
        assert result.value == "0"
        assert result.abs_error_bound == "0"


def test_high_precision_airy_ai_satisfies_differential_equation_residual():
    z = mp.mpf("1.25")
    h = mp.mpf("1e-4")

    values = {
        offset: _value(ai(str(z + offset * h), dps=120, mode="high_precision"))
        for offset in (-2, -1, 0, 1, 2)
    }
    second_derivative = (
        -values[2]
        + 16 * values[1]
        - 30 * values[0]
        + 16 * values[-1]
        - values[-2]
    ) / (12 * h * h)
    residual = second_derivative - z * values[0]

    assert abs(residual) < mp.mpf("1e-17")


@pytest.mark.parametrize(
    ("function", "left_coefficient", "right_coefficient"),
    [
        pytest.param(besselj, 1, 1, id="besselj"),
        pytest.param(bessely, 1, 1, id="bessely"),
        pytest.param(besseli, 1, -1, id="besseli"),
        pytest.param(besselk, -1, 1, id="besselk"),
    ],
)
def test_certified_bessel_three_term_recurrences_enclose_zero(
    function,
    left_coefficient,
    right_coefficient,
):
    order = mp.mpf("2")
    z = mp.mpf("3.75")
    lower = function(str(order - 1), str(z), dps=80, mode="certified")
    center = function(str(order), str(z), dps=80, mode="certified")
    upper = function(str(order + 1), str(z), dps=80, mode="certified")
    _require_certified(lower, center, upper)

    residual = (
        left_coefficient * _value(lower)
        + right_coefficient * _value(upper)
        - (2 * order / z) * _value(center)
    )
    bound = (
        abs(left_coefficient) * _radius(lower)
        + abs(right_coefficient) * _radius(upper)
        + abs(2 * order / z) * _radius(center)
    )
    _assert_encloses_zero(residual, bound)


def test_high_precision_pcfu_satisfies_differential_equation_residual():
    parameter = mp.mpf("0.7")
    z = mp.mpf("1.1")
    h = mp.mpf("1e-4")

    values = {
        offset: _value(pcfu(str(parameter), str(z + offset * h), dps=120, mode="high_precision"))
        for offset in (-2, -1, 0, 1, 2)
    }
    second_derivative = (
        -values[2]
        + 16 * values[1]
        - 30 * values[0]
        + 16 * values[-1]
        - values[-2]
    ) / (12 * h * h)
    residual = second_derivative - (z * z / 4 + parameter) * values[0]

    assert abs(residual) < mp.mpf("1e-17")


def test_certified_pbdv_derivative_identity_encloses_zero():
    order = mp.mpf("2.5")
    z = mp.mpf("1.25")
    result = pbdv(str(order), str(z), dps=80, mode="certified")
    next_value = pcfd(str(order + 1), str(z), dps=80, mode="certified")
    _require_certified(result, next_value)

    values = json.loads(result.value)
    bounds = json.loads(result.abs_error_bound)
    residual = _mp_number(values["derivative"]) - (
        z / 2 * _mp_number(values["value"]) - _value(next_value)
    )
    bound = (
        _mp_number(bounds["derivative"])
        + abs(z / 2) * _mp_number(bounds["value"])
        + _radius(next_value)
    )
    _assert_encloses_zero(residual, bound)


def test_certified_parabolic_cylinder_connection_formula_encloses_zero():
    parameter = mp.mpf("0.7")
    z = mp.mpf("1.1")
    u_negative = pcfu(str(parameter), str(-z), dps=80, mode="certified")
    u_positive = pcfu(str(parameter), str(z), dps=80, mode="certified")
    v_positive = pcfv(str(parameter), str(z), dps=80, mode="certified")
    _require_certified(u_negative, u_positive, v_positive)

    sine = mp.sin(mp.pi * parameter)
    coefficient = mp.pi / mp.gamma(mp.mpf("0.5") + parameter)
    residual = _value(u_negative) - (
        -sine * _value(u_positive) + coefficient * _value(v_positive)
    )
    bound = (
        _radius(u_negative)
        + abs(sine) * _radius(u_positive)
        + abs(coefficient) * _radius(v_positive)
    )
    _assert_encloses_zero(residual, bound)


@pytest.mark.parametrize(
    ("parameter_text", "x_text"),
    [
        pytest.param("0.7", "1.1", id="positive-parameter"),
        pytest.param("-1.25", "0.85", id="negative-parameter"),
    ],
)
def test_certified_pcfw_matches_connection_formula_round_trip(parameter_text, x_text):
    parameter = mp.mpf(parameter_text)
    x = mp.mpf(x_text)
    positive = pcfw(parameter_text, x_text, dps=90, mode="certified")
    negative = pcfw(parameter_text, _mp_text(-x), dps=90, mode="certified")
    _require_certified(positive, negative)

    expected_positive = _pcfw_connection_formula(parameter, x, negative=False)
    expected_negative = _pcfw_connection_formula(parameter, x, negative=True)
    assert abs(_value(positive) - expected_positive) <= max(_radius(positive), mp.mpf("1e-85"))
    assert abs(_value(negative) - expected_negative) <= max(_radius(negative), mp.mpf("1e-85"))


def test_pcfw_phi2_principal_loggamma_phase_is_locally_continuous():
    delta = mp.mpf("1e-6")
    for center in (mp.mpf("-2.5"), mp.mpf("-0.25"), mp.mpf("0"), mp.mpf("0.7"), mp.mpf("2.5")):
        center_phase = _pcfw_phi2(center)
        assert abs(_pcfw_phi2(center + delta) - center_phase) < mp.mpf("1e-5")
        assert abs(_pcfw_phi2(center - delta) - center_phase) < mp.mpf("1e-5")
        assert abs(center_phase + _pcfw_phi2(-center)) < mp.mpf("1e-80")


@pytest.mark.parametrize(
    ("parameter_text", "x_text"),
    [
        pytest.param("0.7", "0.85", id="inner-positive-parameter"),
        pytest.param("0.7", "2.2", id="outer-positive-parameter"),
        pytest.param("-1.25", "0.85", id="inner-negative-parameter"),
        pytest.param("-1.25", "2.2", id="outer-negative-parameter"),
    ],
)
def test_certified_pcfw_satisfies_real_variable_differential_equation_residual(parameter_text, x_text):
    parameter = mp.mpf(parameter_text)
    x = mp.mpf(x_text)
    h = mp.mpf("1e-3")
    results = {
        offset: pcfw(parameter_text, _mp_text(x + offset * h), dps=90, mode="certified")
        for offset in (-2, -1, 0, 1, 2)
    }
    _require_certified(*results.values())

    values = {offset: _value(result) for offset, result in results.items()}
    second_derivative = (
        -values[2]
        + 16 * values[1]
        - 30 * values[0]
        + 16 * values[-1]
        - values[-2]
    ) / (12 * h * h)
    residual = second_derivative + (x * x / 4 - parameter) * values[0]

    assert abs(residual) < mp.mpf("1e-12")


def _require_certified(*results):
    for result in results:
        if not result.certified:
            pytest.skip(result.diagnostics.get("error", "certified backend unavailable"))


def _assert_encloses_zero(residual, bound):
    assert abs(residual) <= bound


def _value(result):
    return _mp_number(result.value)


def _radius(result):
    return _mp_number(result.abs_error_bound)


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


def _pcfw_connection_formula(parameter, x, *, negative: bool):
    imaginary_unit = mp.j
    phi2 = _pcfw_phi2(parameter)
    rho = mp.pi / 8 + phi2 / 2
    k = 1 / (mp.sqrt(1 + mp.exp(2 * mp.pi * parameter)) + mp.exp(mp.pi * parameter))
    term_positive = mp.exp(imaginary_unit * rho) * mp.pcfu(
        imaginary_unit * parameter,
        x * mp.exp(-imaginary_unit * mp.pi / 4),
    )
    term_negative = mp.exp(-imaginary_unit * rho) * mp.pcfu(
        -imaginary_unit * parameter,
        x * mp.exp(imaginary_unit * mp.pi / 4),
    )
    if negative:
        return (
            -imaginary_unit
            / mp.sqrt(2 * k)
            * mp.exp(mp.pi * parameter / 4)
            * (term_positive - term_negative)
        )
    return mp.sqrt(k / 2) * mp.exp(mp.pi * parameter / 4) * (term_positive + term_negative)


def _pcfw_phi2(parameter):
    imaginary_unit = mp.j
    return (
        mp.loggamma(mp.mpf("0.5") + imaginary_unit * parameter)
        - mp.loggamma(mp.mpf("0.5") - imaginary_unit * parameter)
    ) / (2 * imaginary_unit)


def _mp_text(value, digits: int = 50) -> str:
    return mp.nstr(value, digits)
