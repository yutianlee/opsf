"""python-flint / Arb certified-mode wrappers."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation, localcontext
import json
import math
from typing import Any

from ._common import ensure_dps, json_string, make_result

_PHASE1_UNAVAILABLE = "Certified backend unavailable for this function/domain in Phase 1."
_NONFINITE_RESULT = "Certified backend returned a non-finite enclosure."
_PHASE7_PCF_SCOPE = "phase7_hypergeometric_parabolic_cylinder"
_PHASE7_PCF_REAL_PARAMETER_ONLY = "Phase 7 certified parabolic-cylinder supports real parameters only."
_PHASE8_PCF_SCOPE = "phase8_parabolic_cylinder_connections"
_PHASE8_PCFW_REAL_ARGUMENT_ONLY = "Phase 8 certified pcfw supports real arguments only."


def arb_gamma(z, *, dps: int = 50):
    return _with_flint("gamma", dps, lambda: _make_ball(z).gamma())


def arb_loggamma(z, *, dps: int = 50):
    return _with_flint(
        "loggamma",
        dps,
        lambda: _make_ball(z, force_complex=_is_real_nonpositive(z)).lgamma(),
    )


def arb_rgamma(z, *, dps: int = 50):
    return _with_flint("rgamma", dps, lambda: _make_ball(z).rgamma())


def arb_airy(z, *, dps: int = 50):
    requested = ensure_dps(dps)
    try:
        flint, old_prec, bits = _enter_flint_context(requested)
    except ImportError as exc:
        return _unavailable("airy", requested, str(exc))
    try:
        argument = _make_ball(z)
        domain = "real" if isinstance(argument, flint.arb) else "complex"
        ai, aip, bi, bip = argument.airy()
        values = {
            "ai": _ball_value_string(ai, flint),
            "aip": _ball_value_string(aip, flint),
            "bi": _ball_value_string(bi, flint),
            "bip": _ball_value_string(bip, flint),
        }
        abs_errors = {
            "ai": _ball_abs_error_string(ai),
            "aip": _ball_abs_error_string(aip),
            "bi": _ball_abs_error_string(bi),
            "bip": _ball_abs_error_string(bip),
        }
        rel_errors = {
            key: error
            for key, ball in {"ai": ai, "aip": aip, "bi": bi, "bip": bip}.items()
            if (error := _ball_rel_error_string(ball)) is not None
        }
        return make_result(
            function="airy",
            value=json_string(values),
            abs_error_bound=json_string(abs_errors),
            rel_error_bound=json.dumps(rel_errors, sort_keys=True) if rel_errors else None,
            certified=True,
            method="arb_ball",
            backend="python-flint",
            requested_dps=requested,
            working_dps=_bits_to_dps(bits),
            diagnostics={
                "mode": "certified",
                "working_precision_bits": bits,
                "domain": domain,
                "certificate_scope": "phase3_real_airy" if domain == "real" else "arb_complex_airy",
            },
        )
    except Exception as exc:  # pragma: no cover - depends on optional backend domains
        return _unavailable("airy", requested, f"{_PHASE1_UNAVAILABLE} {exc}")
    finally:
        flint.ctx.prec = old_prec


def arb_ai(z, derivative: int = 0, *, dps: int = 50):
    return _arb_airy_component("ai", z, derivative, dps=dps)


def arb_bi(z, derivative: int = 0, *, dps: int = 50):
    return _arb_airy_component("bi", z, derivative, dps=dps)


def arb_besselj(v, z, *, dps: int = 50):
    return _arb_bessel("besselj", "bessel_j", v, z, dps=dps)


def arb_bessely(v, z, *, dps: int = 50):
    return _arb_bessel("bessely", "bessel_y", v, z, dps=dps)


def arb_besseli(v, z, *, dps: int = 50):
    return _arb_bessel("besseli", "bessel_i", v, z, dps=dps)


def arb_besselk(v, z, *, dps: int = 50):
    return _arb_bessel("besselk", "bessel_k", v, z, dps=dps)


def arb_pbdv(v, x, *, dps: int = 50):
    requested = ensure_dps(dps)
    try:
        flint, old_prec, bits = _enter_flint_context(requested)
    except ImportError as exc:
        return _unavailable("pbdv", requested, str(exc))
    try:
        order_text = _real_order_text(v)
        if order_text is None:
            return _unavailable("pbdv", requested, _PHASE7_PCF_REAL_PARAMETER_ONLY)
        order = flint.arb(order_text)
        argument = _make_ball(x)
        value = _arb_pcfd_value(order, argument, flint)
        derivative = argument / 2 * value - _arb_pcfd_value(order + 1, argument, flint)
        if not _is_finite_ball(value, flint) or not _is_finite_ball(derivative, flint):
            return _unavailable("pbdv", requested, _NONFINITE_RESULT)

        values = {
            "value": _ball_value_string(value, flint),
            "derivative": _ball_value_string(derivative, flint),
        }
        abs_errors = {
            "value": _ball_abs_error_string(value),
            "derivative": _ball_abs_error_string(derivative),
        }
        rel_errors = {
            key: error
            for key, ball in {"value": value, "derivative": derivative}.items()
            if (error := _ball_rel_error_string(ball)) is not None
        }
        return make_result(
            function="pbdv",
            value=json_string(values),
            abs_error_bound=json_string(abs_errors),
            rel_error_bound=json.dumps(rel_errors, sort_keys=True) if rel_errors else None,
            certified=True,
            method="arb_hypergeometric",
            backend="python-flint",
            requested_dps=requested,
            working_dps=_bits_to_dps(bits),
            diagnostics=_parabolic_cylinder_diagnostics("pbdv", order_text, argument, bits, flint),
        )
    except Exception as exc:  # pragma: no cover - depends on optional backend domains
        return _unavailable("pbdv", requested, f"{_PHASE1_UNAVAILABLE} {exc}")
    finally:
        flint.ctx.prec = old_prec


def arb_pcfd(v, z, *, dps: int = 50):
    return _arb_parabolic_cylinder("pcfd", v, z, dps=dps)


def arb_pcfu(a, z, *, dps: int = 50):
    return _arb_parabolic_cylinder("pcfu", a, z, dps=dps)


def arb_pcfv(a, z, *, dps: int = 50):
    return _arb_parabolic_cylinder("pcfv", a, z, dps=dps)


def arb_pcfw(a, z, *, dps: int = 50):
    return _arb_parabolic_cylinder("pcfw", a, z, dps=dps)


def _with_flint(function: str, dps: int, evaluate):
    requested = ensure_dps(dps)
    try:
        flint, old_prec, bits = _enter_flint_context(requested)
    except ImportError as exc:
        return _unavailable(function, requested, str(exc))
    try:
        value = evaluate()
        return _certified_result(function, value, requested, bits, flint)
    except Exception as exc:  # pragma: no cover - depends on optional backend domains
        return _unavailable(function, requested, f"{_PHASE1_UNAVAILABLE} {exc}")
    finally:
        flint.ctx.prec = old_prec


def _arb_airy_component(component: str, z, derivative: int, *, dps: int):
    requested = ensure_dps(dps)
    derivative = _validate_airy_derivative(derivative)
    try:
        flint, old_prec, bits = _enter_flint_context(requested)
    except ImportError as exc:
        return _unavailable(_airy_component_function(component, derivative), requested, str(exc))
    try:
        argument = _make_ball(z)
        domain = "real" if isinstance(argument, flint.arb) else "complex"
        values = argument.airy()
        index = derivative if component == "ai" else 2 + derivative
        result = _certified_result(_airy_component_function(component, derivative), values[index], requested, bits, flint)
        if result.certified:
            diagnostics = dict(result.diagnostics)
            diagnostics.update(
                {
                    "component": component,
                    "derivative": derivative,
                    "domain": domain,
                    "certificate_scope": "phase3_real_airy" if domain == "real" else "arb_complex_airy",
                }
            )
            return make_result(
                function=result.function,
                value=result.value,
                abs_error_bound=result.abs_error_bound,
                rel_error_bound=result.rel_error_bound,
                certified=True,
                method=result.method,
                backend=result.backend,
                requested_dps=result.requested_dps,
                working_dps=result.working_dps,
                terms_used=result.terms_used,
                diagnostics=diagnostics,
            )
        return result
    except Exception as exc:  # pragma: no cover - depends on optional backend domains
        return _unavailable(_airy_component_function(component, derivative), requested, f"{_PHASE1_UNAVAILABLE} {exc}")
    finally:
        flint.ctx.prec = old_prec


def _arb_bessel(function: str, method_name: str, v, z, *, dps: int):
    requested = ensure_dps(dps)
    try:
        flint, old_prec, bits = _enter_flint_context(requested)
    except ImportError as exc:
        return _unavailable(function, requested, str(exc))
    try:
        order_text = _real_order_text(v)
        if order_text is None:
            return _unavailable(function, requested, "Phase 5 certified Bessel supports real order only.")
        argument = _make_ball(z)
        argument_domain = "real" if isinstance(argument, flint.arb) else "complex"
        order = flint.arb(order_text)
        order_argument = flint.acb(order) if isinstance(argument, flint.acb) else order
        value = getattr(argument, method_name)(order_argument)
        result = _certified_result(function, value, requested, bits, flint)
        if result.certified:
            order_domain = "integer" if _is_integral_decimal_text(order_text) else "real"
            certificate_scope = (
                "phase4_integer_real_bessel"
                if argument_domain == "real" and order_domain == "integer"
                else "phase5_real_order_complex_bessel"
            )
            diagnostics = dict(result.diagnostics)
            diagnostics.update(
                {
                    "order": _order_diagnostic_value(order_text),
                    "domain": argument_domain,
                    "order_domain": order_domain,
                    "certificate_scope": certificate_scope,
                }
            )
            return make_result(
                function=result.function,
                value=result.value,
                abs_error_bound=result.abs_error_bound,
                rel_error_bound=result.rel_error_bound,
                certified=True,
                method=result.method,
                backend=result.backend,
                requested_dps=result.requested_dps,
                working_dps=result.working_dps,
                terms_used=result.terms_used,
                diagnostics=diagnostics,
            )
        return result
    except Exception as exc:  # pragma: no cover - depends on optional backend domains
        return _unavailable(function, requested, f"{_PHASE1_UNAVAILABLE} {exc}")
    finally:
        flint.ctx.prec = old_prec


def _arb_parabolic_cylinder(function: str, parameter, z, *, dps: int):
    requested = ensure_dps(dps)
    try:
        flint, old_prec, bits = _enter_flint_context(requested)
    except ImportError as exc:
        return _unavailable(function, requested, str(exc))
    try:
        parameter_text = _real_order_text(parameter)
        if parameter_text is None:
            return _unavailable(function, requested, _PHASE7_PCF_REAL_PARAMETER_ONLY)
        parameter_ball = flint.arb(parameter_text)
        if function == "pcfw":
            argument_text = _real_order_text(z)
            if argument_text is None:
                return _unavailable(function, requested, _PHASE8_PCFW_REAL_ARGUMENT_ONLY)
            argument = flint.arb(argument_text)
        else:
            argument = _make_ball(z)
        if function == "pcfu":
            value = _arb_pcfu_value(parameter_ball, argument, flint)
        elif function == "pcfd":
            value = _arb_pcfd_value(parameter_ball, argument, flint)
        elif function == "pcfv":
            value = _arb_pcfv_value(parameter_ball, argument, flint)
        elif function == "pcfw":
            value = _arb_pcfw_value(parameter_ball, argument, flint)
        else:  # pragma: no cover - guarded by public wrappers
            raise ValueError(f"unsupported parabolic-cylinder function: {function}")
        if function in {"pcfv", "pcfw"} and isinstance(argument, flint.arb) and isinstance(value, flint.acb):
            value = value.real
        result = _certified_result(function, value, requested, bits, flint)
        if result.certified:
            diagnostics = _parabolic_cylinder_diagnostics(function, parameter_text, argument, bits, flint)
            return make_result(
                function=result.function,
                value=result.value,
                abs_error_bound=result.abs_error_bound,
                rel_error_bound=result.rel_error_bound,
                certified=True,
                method="arb_hypergeometric",
                backend=result.backend,
                requested_dps=result.requested_dps,
                working_dps=result.working_dps,
                terms_used=result.terms_used,
                diagnostics=diagnostics,
            )
        return result
    except Exception as exc:  # pragma: no cover - depends on optional backend domains
        return _unavailable(function, requested, f"{_PHASE1_UNAVAILABLE} {exc}")
    finally:
        flint.ctx.prec = old_prec


def _arb_pcfd_value(order, argument, flint):
    return _arb_pcfu_value(-order - flint.arb("0.5"), argument, flint)


def _arb_pcfv_value(parameter, argument, flint):
    half = flint.arb("0.5")
    one_quarter = flint.arb("0.25")
    two = flint.arb(2)
    pi = flint.arb.pi()
    imaginary_unit = flint.acb(0, 1)
    complex_argument = flint.acb(argument) if isinstance(argument, flint.arb) else argument
    term1 = -imaginary_unit * (half - parameter).rgamma() * _arb_pcfu_value(parameter, complex_argument, flint)
    phase = (-imaginary_unit * pi * (parameter / 2 - one_quarter)).exp()
    term2 = (two / pi).sqrt() * phase * _arb_pcfu_value(-parameter, imaginary_unit * complex_argument, flint)
    return term1 + term2


def _arb_pcfu_value(parameter, argument, flint):
    one_quarter = flint.arb("0.25")
    half = flint.arb("0.5")
    three_quarters = flint.arb("0.75")
    three_halves = flint.arb("1.5")
    two = flint.arb(2)
    sqrt_pi = flint.arb.pi().sqrt()
    z2 = argument * argument

    u0 = sqrt_pi * two ** (-parameter / 2 - one_quarter) * (parameter / 2 + three_quarters).rgamma()
    derivative0 = -sqrt_pi * two ** (-parameter / 2 + one_quarter) * (parameter / 2 + one_quarter).rgamma()
    even_part = (-z2 / 2).hypgeom_1f1(-parameter / 2 + one_quarter, half)
    odd_part = (-z2 / 2).hypgeom_1f1(-parameter / 2 + three_quarters, three_halves)
    return (z2 / 4).exp() * (u0 * even_part + derivative0 * argument * odd_part)


def _arb_pcfw_value(parameter, argument, flint):
    half = flint.arb("0.5")
    pi = flint.arb.pi()
    imaginary_unit = flint.acb(0, 1)
    complex_argument = flint.acb(argument)
    phi2 = ((half + imaginary_unit * parameter).lgamma() - (half - imaginary_unit * parameter).lgamma()) / (
        2 * imaginary_unit
    )
    rho = pi / 8 + phi2 / 2
    exp_pi_a = (pi * parameter).exp()
    k = 1 / ((1 + (2 * pi * parameter).exp()).sqrt() + exp_pi_a)
    coefficient = (k / 2).sqrt() * (pi * parameter / 4).exp()
    argument_minus = complex_argument * (-imaginary_unit * pi / 4).exp()
    argument_plus = complex_argument * (imaginary_unit * pi / 4).exp()
    return coefficient * (imaginary_unit * rho).exp() * _arb_pcfu_value(
        imaginary_unit * parameter, argument_minus, flint
    ) + coefficient * (-imaginary_unit * rho).exp() * _arb_pcfu_value(
        -imaginary_unit * parameter, argument_plus, flint
    )


def _parabolic_cylinder_diagnostics(function: str, parameter_text: str, argument, bits: int, flint):
    parameter_domain = "integer" if _is_integral_decimal_text(parameter_text) else "real"
    formula = {
        "pcfu": "pcfu_1f1_global",
        "pcfd": "pcfd_via_pcfu",
        "pbdv": "pcfd_via_pcfu",
        "pcfv": "pcfv_dlmf_connection",
        "pcfw": "pcfw_dlmf_12_14_real_connection",
    }[function]
    certificate_scope = _PHASE8_PCF_SCOPE if function in {"pcfv", "pcfw"} else _PHASE7_PCF_SCOPE
    return {
        "mode": "certified",
        "working_precision_bits": bits,
        "domain": "real" if isinstance(argument, flint.arb) else "complex",
        "parameter": _order_diagnostic_value(parameter_text),
        "parameter_domain": parameter_domain,
        "formula": formula,
        "certificate_scope": certificate_scope,
    }


def _enter_flint_context(requested_dps: int):
    try:
        import flint
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise ImportError("python-flint is not installed") from exc
    old_prec = flint.ctx.prec
    bits = _dps_to_bits(requested_dps)
    flint.ctx.prec = bits
    return flint, old_prec, bits


def _make_ball(value: Any, *, force_complex: bool = False):
    from flint import acb, arb

    if isinstance(value, (arb, acb)):
        if force_complex and isinstance(value, arb):
            return acb(value)
        return value
    if isinstance(value, complex):
        return acb(str(value.real), str(value.imag))
    if isinstance(value, str):
        text = value.strip().replace("i", "j")
        if "j" in text.lower():
            real, imag = _parse_complex_text(text)
            return acb(real, imag)
        if force_complex:
            return acb(text, "0")
        return arb(text)
    if force_complex:
        return acb(str(value), "0")
    return arb(str(value))


def _certified_result(function: str, value, requested_dps: int, bits: int, flint):
    if not _is_finite_ball(value, flint):
        return _unavailable(function, requested_dps, _NONFINITE_RESULT)
    return make_result(
        function=function,
        value=_ball_value_string(value, flint),
        abs_error_bound=_ball_abs_error_string(value),
        rel_error_bound=_ball_rel_error_string(value),
        certified=True,
        method="arb_ball",
        backend="python-flint",
        requested_dps=requested_dps,
        working_dps=_bits_to_dps(bits),
        diagnostics={
            "mode": "certified",
            "working_precision_bits": bits,
            "certificate_scope": "direct_arb_primitive",
        },
    )


def _unavailable(function: str, requested_dps: int, message: str):
    return make_result(
        function=function,
        value="",
        abs_error_bound=None,
        rel_error_bound=None,
        certified=False,
        method="arb_ball",
        backend="python-flint",
        requested_dps=requested_dps,
        working_dps=requested_dps,
        diagnostics={"error": message, "mode": "certified"},
    )


def _dps_to_bits(dps: int) -> int:
    return max(64, math.ceil(dps * math.log2(10)) + 32)


def _bits_to_dps(bits: int) -> int:
    return math.floor(bits / math.log2(10))


def _is_finite_ball(value, flint) -> bool:
    if isinstance(value, flint.acb):
        return bool(value.is_finite())
    return bool(value.is_finite())


def _is_real_nonpositive(value: Any) -> bool:
    try:
        if isinstance(value, complex):
            return value.imag == 0 and value.real <= 0
        if isinstance(value, str):
            text = value.strip().replace("i", "j")
            if "j" in text.lower():
                real, imag = _parse_complex_text(text)
                return Decimal(imag) == 0 and Decimal(real) <= 0
            return Decimal(text) <= 0
        return Decimal(str(value)) <= 0
    except (InvalidOperation, ValueError):
        return False


def _is_integer_order(value: Any) -> bool:
    order_text = _real_order_text(value)
    return order_text is not None and _is_integral_decimal_text(order_text)


def _real_order_text(value: Any) -> str | None:
    try:
        if isinstance(value, complex):
            if value.imag != 0:
                return None
            value = repr(value.real)
        if isinstance(value, str):
            text = value.strip().replace("i", "j")
            if "j" in text.lower():
                real, imag = _parse_complex_text(text)
                if Decimal(imag) != 0:
                    return None
                value = real
            else:
                value = text
        decimal = Decimal(str(value))
        if not decimal.is_finite():
            return None
        return format(decimal, "f")
    except (InvalidOperation, ValueError):
        return None


def _is_integral_decimal_text(value: str) -> bool:
    decimal = Decimal(value)
    return decimal == decimal.to_integral_value()


def _order_diagnostic_value(value: str):
    if _is_integral_decimal_text(value):
        return int(Decimal(value))
    return value


def _validate_airy_derivative(derivative: int) -> int:
    derivative = int(derivative)
    if derivative not in {0, 1}:
        raise ValueError("Airy component wrappers support derivative=0 or derivative=1")
    return derivative


def _airy_component_function(component: str, derivative: int) -> str:
    return component if derivative == 0 else f"{component}p"


def _parse_complex_text(text: str) -> tuple[str, str]:
    body = text.replace(" ", "").replace("i", "j")
    if not body.lower().endswith("j"):
        return body, "0"
    body = body[:-1]
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
    real = body[:split_at]
    imag = _normalize_imaginary_component(body[split_at:])
    return real, imag


def _normalize_imaginary_component(value: str) -> str:
    if value in {"", "+"}:
        return "1"
    if value == "-":
        return "-1"
    return value


def _ball_value_string(value, flint) -> str:
    if isinstance(value, flint.acb):
        real = _arb_mid_string(value.real)
        imag = _arb_mid_string(value.imag)
        sign = "" if imag.startswith("-") else "+"
        return f"{real}{sign}{imag}j"
    return _arb_mid_string(value)


def _ball_abs_error_string(value) -> str:
    return _arb_mid_string(value.rad())


def _ball_rel_error_string(value) -> str | None:
    try:
        radius = Decimal(_ball_abs_error_string(value))
        magnitude = Decimal(_arb_mid_string(value.abs_lower()))
    except (InvalidOperation, ValueError):
        return None
    if magnitude <= 0:
        return None
    with localcontext() as ctx:
        ctx.prec = 20
        return format(radius / magnitude, ".6E")


def _arb_mid_string(value) -> str:
    mantissa, _radius, exponent = value.mid_rad_10exp()
    return _decimal_from_mantissa_exponent(int(mantissa), int(exponent))


def _decimal_from_mantissa_exponent(mantissa: int, exponent: int) -> str:
    if mantissa == 0:
        return "0"
    sign = "-" if mantissa < 0 else ""
    digits = str(abs(mantissa))
    point = len(digits) + exponent
    if point <= 0:
        body = "0." + ("0" * (-point)) + digits
    elif point >= len(digits):
        body = digits + ("0" * (point - len(digits)))
    else:
        body = digits[:point] + "." + digits[point:]
    if "." in body:
        body = body.rstrip("0").rstrip(".")
    return sign + body
