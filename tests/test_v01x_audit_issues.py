import json
import random

import pytest

from certsf import ai, besselj, bi, gamma, pbdv, pcfd, pcfu, pcfv, pcfw, rgamma

mp = pytest.importorskip("mpmath")
mp.mp.dps = 120


@pytest.mark.parametrize(
    ("parameter_text", "z_text"),
    [
        pytest.param("0.7", "-3.0+1e-18j", id="upper-negative-real-cut"),
        pytest.param("0.7", "-3.0-1e-18j", id="lower-negative-real-cut"),
        pytest.param("-1.25", "-0.125+2.5j", id="upper-imaginary-branch-grid"),
        pytest.param("1.5", "-8.0-1e-12j", id="large-lower-side"),
    ],
)
def test_v01x_pcfu_branch_side_residual_grid_issue_21(parameter_text, z_text):
    # Issue #21 / docs/formula_audit.md: audit pcfu branch-side behavior with
    # a certified recurrence residual, independent of mpmath reference values.
    parameter = mp.mpf(parameter_text)
    z = _mp_number(z_text)
    lower = pcfu(_mp_text(parameter - 1), z_text, dps=90, mode="certified")
    center = pcfu(parameter_text, z_text, dps=90, mode="certified")
    upper = pcfu(_mp_text(parameter + 1), z_text, dps=90, mode="certified")
    _require_certified(lower, center, upper)

    assert center.diagnostics["formula"] == "pcfu_1f1_global"
    assert center.diagnostics["certificate_level"] == "formula_audited_experimental"

    residual = _add(
        _sub(_scale(z, _ball(center)), _ball(lower)),
        _scale(parameter + mp.mpf("0.5"), _ball(upper)),
    )
    _assert_contains_zero(residual)


def test_v01x_pbdv_complex_domain_policy_keeps_pcfd_value_path_issue_22():
    # Issue #22: the v0.1.x policy is to keep certified pbdv complex arguments
    # public, with pbdv's value component exactly sharing the pcfd formula path.
    order = mp.mpf("0.7")
    z_text = "-1.1+1e-18j"
    z = _mp_number(z_text)
    pbdv_result = pbdv(_mp_text(order), z_text, dps=90, mode="certified")
    pcfd_value = pcfd(_mp_text(order), z_text, dps=90, mode="certified")
    pcfd_next = pcfd(_mp_text(order + 1), z_text, dps=90, mode="certified")
    _require_certified(pbdv_result, pcfd_value, pcfd_next)

    assert pbdv_result.diagnostics["domain"] == "complex"
    assert pbdv_result.diagnostics["formula"] == "pcfd_via_pcfu"
    assert pcfd_value.diagnostics["domain"] == "complex"

    _assert_contains_zero(_sub(_component_ball(pbdv_result, "value"), _ball(pcfd_value)))
    derivative_residual = _sub(
        _component_ball(pbdv_result, "derivative"),
        _sub(_scale(z / 2, _component_ball(pbdv_result, "value")), _ball(pcfd_next)),
    )
    _assert_contains_zero(derivative_residual)


@pytest.mark.parametrize(
    ("parameter_text", "z_text"),
    [
        pytest.param("0.7", "-2.75+1e-18j", id="upper-negative-real-cut"),
        pytest.param("0.7", "-2.75-1e-18j", id="lower-negative-real-cut"),
        pytest.param("-1.25", "0.25+2.0j", id="upper-imaginary-grid"),
    ],
)
def test_v01x_pcfv_connection_and_recurrence_grid_issue_23(parameter_text, z_text):
    # Issue #23 / docs/formula_audit.md: pair the V connection formula with an
    # independent recurrence residual on branch-side samples.
    parameter = mp.mpf(parameter_text)
    z = _mp_number(z_text)
    u_negative = pcfu(parameter_text, _mp_text(-z), dps=90, mode="certified")
    u_positive = pcfu(parameter_text, z_text, dps=90, mode="certified")
    v_center = pcfv(parameter_text, z_text, dps=90, mode="certified")
    v_lower = pcfv(_mp_text(parameter - 1), z_text, dps=90, mode="certified")
    v_upper = pcfv(_mp_text(parameter + 1), z_text, dps=90, mode="certified")
    _require_certified(u_negative, u_positive, v_center, v_lower, v_upper)

    assert v_center.diagnostics["formula"] == "pcfv_dlmf_connection"
    assert v_center.diagnostics["certificate_level"] == "formula_audited_experimental"

    sine = mp.sin(mp.pi * parameter)
    coefficient = mp.pi / mp.gamma(mp.mpf("0.5") + parameter)
    connection_residual = _add(
        _add(_ball(u_negative), _scale(sine, _ball(u_positive))),
        _scale(-coefficient, _ball(v_center)),
    )
    _assert_contains_zero(connection_residual)

    recurrence_residual = _add(
        _sub(_scale(z, _ball(v_center)), _ball(v_upper)),
        _scale(parameter - mp.mpf("0.5"), _ball(v_lower)),
    )
    _assert_contains_zero(recurrence_residual)


@pytest.mark.parametrize(
    ("parameter_text", "x_text"),
    [
        pytest.param("0.7", "-2.2", id="positive-parameter-negative-x"),
        pytest.param("0.7", "2.2", id="positive-parameter-positive-x"),
        pytest.param("-1.25", "-0.85", id="negative-parameter-negative-x"),
        pytest.param("-1.25", "0.85", id="negative-parameter-positive-x"),
    ],
)
def test_v01x_pcfw_real_phase_and_residual_grid_issue_24(parameter_text, x_text):
    # Issue #24: keep pcfw on the real-variable path and check the differential
    # equation residual away from mpmath reference-value comparison.
    parameter = mp.mpf(parameter_text)
    x = mp.mpf(x_text)
    h = mp.mpf("1e-3")
    results = {
        offset: pcfw(parameter_text, _mp_text(x + offset * h), dps=90, mode="certified")
        for offset in (-2, -1, 0, 1, 2)
    }
    _require_certified(*results.values())

    assert results[0].diagnostics["formula"] == "pcfw_dlmf_12_14_real_connection"
    assert results[0].diagnostics["domain"] == "real"

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


def test_v01x_pcfw_phi2_grid_is_locally_continuous_issue_24():
    # Issue #24: phi2 is calculated from a principal-loggamma difference, so the
    # audit grid checks local continuity and odd symmetry over both signs.
    delta = mp.mpf("1e-6")
    centers = [mp.mpf(text) for text in ("-4", "-2.5", "-0.25", "0", "0.7", "2.5", "4")]
    for center in centers:
        center_phase = _pcfw_phi2(center)
        assert abs(_pcfw_phi2(center + delta) - center_phase) < mp.mpf("1e-5")
        assert abs(_pcfw_phi2(center - delta) - center_phase) < mp.mpf("1e-5")
        assert abs(center_phase + _pcfw_phi2(-center)) < mp.mpf("1e-80")


def test_v01x_deterministic_high_precision_property_grid_issue_25():
    # Issue #25: deterministic random grids plus explicit edge cases, using
    # identities and residuals instead of plain reference-value comparison.
    rng = random.Random(20260507)

    gamma_points = [
        mp.mpf("0.001"),
        mp.mpc("-0.999", "1e-6"),
        mp.mpc("-2.001", "-1e-6"),
    ]
    gamma_points.extend(mp.mpf(str(round(rng.uniform(-1.75, 3.75), 3))) for _ in range(2))
    for z in gamma_points:
        if abs(z) < mp.mpf("1e-12"):
            continue
        residual = _value(gamma(_mp_text(z + 1), dps=80, mode="high_precision")) - z * _value(
            gamma(_mp_text(z), dps=80, mode="high_precision")
        )
        assert abs(residual) < mp.mpf("1e-55")

    for z in [mp.mpf("-8"), mp.mpf("-0.001"), mp.mpf("0.001"), mp.mpf("8")]:
        ai_value = _value(ai(_mp_text(z), dps=80, mode="high_precision"))
        aip = _value(ai(_mp_text(z), derivative=1, dps=80, mode="high_precision"))
        bi_value = _value(bi(_mp_text(z), dps=80, mode="high_precision"))
        bip = _value(bi(_mp_text(z), derivative=1, dps=80, mode="high_precision"))
        assert abs(ai_value * bip - aip * bi_value - 1 / mp.pi) < mp.mpf("1e-55")

    bessel_samples = [
        (mp.mpf("2.5"), mp.mpf("0.125")),
        (mp.mpf("2.5"), mp.mpc("-4.0", "1e-6")),
        (mp.mpf("3"), mp.mpc("8.0", "-0.5")),
    ]
    bessel_samples.extend((mp.mpf("1.5"), mp.mpf(str(round(rng.uniform(1.0, 6.0), 3)))) for _ in range(2))
    for order, z in bessel_samples:
        lower = _value(besselj(_mp_text(order - 1), _mp_text(z), dps=80, mode="high_precision"))
        center = _value(besselj(_mp_text(order), _mp_text(z), dps=80, mode="high_precision"))
        upper = _value(besselj(_mp_text(order + 1), _mp_text(z), dps=80, mode="high_precision"))
        assert abs(lower + upper - (2 * order / z) * center) < mp.mpf("1e-55")

    parabolic_samples = [
        (mp.mpf("0.7"), mp.mpc("-1.1", "1e-6")),
        (mp.mpf("-1.25"), mp.mpc("-0.25", "-1.75")),
        (mp.mpf("1.5"), mp.mpf("8.0")),
    ]
    for parameter, z in parabolic_samples:
        lower = _value(pcfu(_mp_text(parameter - 1), _mp_text(z), dps=80, mode="high_precision"))
        center = _value(pcfu(_mp_text(parameter), _mp_text(z), dps=80, mode="high_precision"))
        upper = _value(pcfu(_mp_text(parameter + 1), _mp_text(z), dps=80, mode="high_precision"))
        assert abs(z * center - lower + (parameter + mp.mpf("0.5")) * upper) < mp.mpf("1e-55")


def test_v01x_deterministic_certified_property_grid_issue_25():
    # The certified portion of issue #25 keeps the grid tiny for CI but covers
    # direct Arb and formula-backed certificate paths.
    gamma_z = gamma("2.5", dps=90, mode="certified")
    gamma_next = gamma("3.5", dps=90, mode="certified")
    rgamma_z = rgamma("2.5", dps=90, mode="certified")
    _require_certified(gamma_z, gamma_next, rgamma_z)
    _assert_contains_zero(_sub(_ball(gamma_next), _scale(mp.mpf("2.5"), _ball(gamma_z))))
    _assert_contains_constant(_mul(_ball(gamma_z), _ball(rgamma_z)), mp.mpf(1))

    ai_result = ai("2.5", dps=90, mode="certified")
    aip_result = ai("2.5", derivative=1, dps=90, mode="certified")
    bi_result = bi("2.5", dps=90, mode="certified")
    bip_result = bi("2.5", derivative=1, dps=90, mode="certified")
    _require_certified(ai_result, aip_result, bi_result, bip_result)
    wronskian = _sub(_mul(_ball(ai_result), _ball(bip_result)), _mul(_ball(aip_result), _ball(bi_result)))
    _assert_contains_constant(wronskian, 1 / mp.pi)

    order = mp.mpf("2.5")
    z = mp.mpc("-4.0", "1e-6")
    lower = besselj(_mp_text(order - 1), _mp_text(z), dps=90, mode="certified")
    center = besselj(_mp_text(order), _mp_text(z), dps=90, mode="certified")
    upper = besselj(_mp_text(order + 1), _mp_text(z), dps=90, mode="certified")
    _require_certified(lower, center, upper)
    _assert_contains_zero(_add(_sub(_ball(lower), _scale(2 * order / z, _ball(center))), _ball(upper)))

    parameter = mp.mpf("0.7")
    z_text = "-1.1+1e-18j"
    lower = pcfu(_mp_text(parameter - 1), z_text, dps=90, mode="certified")
    center = pcfu(_mp_text(parameter), z_text, dps=90, mode="certified")
    upper = pcfu(_mp_text(parameter + 1), z_text, dps=90, mode="certified")
    _require_certified(lower, center, upper)
    residual = _add(
        _sub(_scale(_mp_number(z_text), _ball(center)), _ball(lower)),
        _scale(parameter + mp.mpf("0.5"), _ball(upper)),
    )
    _assert_contains_zero(residual)


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


def _value(result):
    return _mp_number(result.value)


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


def _mp_text(value, digits: int = 50) -> str:
    if isinstance(value, mp.mpc):
        sign = "+" if mp.im(value) >= 0 else "-"
        return f"{mp.nstr(mp.re(value), digits)}{sign}{mp.nstr(abs(mp.im(value)), digits)}j"
    return mp.nstr(value, digits)


def _pcfw_phi2(parameter):
    imaginary_unit = mp.j
    return (
        mp.loggamma(mp.mpf("0.5") + imaginary_unit * parameter)
        - mp.loggamma(mp.mpf("0.5") - imaginary_unit * parameter)
    ) / (2 * imaginary_unit)
