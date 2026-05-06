"""python-flint / Arb certified-mode wrappers."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation, localcontext
import json
import math
from typing import Any

from ._common import ensure_dps, json_string, make_result

_PHASE1_UNAVAILABLE = "Certified backend unavailable for this function/domain in Phase 1."
_NONFINITE_RESULT = "Certified backend returned a non-finite enclosure."


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
    return _unavailable("pbdv", requested, _PHASE1_UNAVAILABLE)


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
        order_value = _integer_order_value(v)
        if order_value is None:
            return _unavailable(function, requested, "Phase 4 certified Bessel supports integer order only.")
        argument = _make_ball(z)
        if not isinstance(argument, flint.arb):
            return _unavailable(function, requested, "Phase 4 certified Bessel supports real arguments only.")
        order = _make_ball(v)
        value = getattr(argument, method_name)(order)
        result = _certified_result(function, value, requested, bits, flint)
        if result.certified:
            diagnostics = dict(result.diagnostics)
            diagnostics.update(
                {
                    "order": order_value,
                    "domain": "real",
                    "order_domain": "integer",
                    "certificate_scope": "phase4_integer_real_bessel",
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
        diagnostics={"mode": "certified", "working_precision_bits": bits},
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
    return _integer_order_value(value) is not None


def _integer_order_value(value: Any) -> int | None:
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
        integral = decimal.to_integral_value()
        if decimal != integral:
            return None
        return int(integral)
    except (InvalidOperation, ValueError):
        return None


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
