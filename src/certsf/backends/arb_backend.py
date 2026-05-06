"""python-flint / Arb certified-mode wrappers."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation, localcontext
import json
import math
from typing import Any

from ._common import ensure_dps, json_string, make_result

_PHASE1_UNAVAILABLE = "Certified backend unavailable for this function/domain in Phase 1."


def arb_gamma(z, *, dps: int = 50):
    return _with_flint("gamma", dps, lambda: _make_ball(z).gamma())


def arb_loggamma(z, *, dps: int = 50):
    return _with_flint("loggamma", dps, lambda: _make_ball(z).lgamma())


def arb_airy(z, *, dps: int = 50):
    requested = ensure_dps(dps)
    try:
        flint, old_prec, bits = _enter_flint_context(requested)
    except ImportError as exc:
        return _unavailable("airy", requested, str(exc))
    try:
        ai, aip, bi, bip = _make_ball(z).airy()
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
            diagnostics={"mode": "certified", "working_precision_bits": bits},
        )
    except Exception as exc:  # pragma: no cover - depends on optional backend domains
        return _unavailable("airy", requested, f"{_PHASE1_UNAVAILABLE} {exc}")
    finally:
        flint.ctx.prec = old_prec


def arb_besselj(v, z, *, dps: int = 50):
    requested = ensure_dps(dps)
    try:
        flint, old_prec, bits = _enter_flint_context(requested)
    except ImportError as exc:
        return _unavailable("besselj", requested, str(exc))
    try:
        order = _make_ball(v)
        argument = _make_ball(z)
        if isinstance(order, flint.acb) or isinstance(argument, flint.acb):
            order = flint.acb(order)
            argument = flint.acb(argument)
        value = argument.bessel_j(order)
        return _certified_result("besselj", value, requested, bits, flint)
    except Exception as exc:  # pragma: no cover - depends on optional backend domains
        return _unavailable("besselj", requested, f"{_PHASE1_UNAVAILABLE} {exc}")
    finally:
        flint.ctx.prec = old_prec


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


def _enter_flint_context(requested_dps: int):
    try:
        import flint
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise ImportError("python-flint is not installed") from exc
    old_prec = flint.ctx.prec
    bits = _dps_to_bits(requested_dps)
    flint.ctx.prec = bits
    return flint, old_prec, bits


def _make_ball(value: Any):
    from flint import acb, arb

    if isinstance(value, (arb, acb)):
        return value
    if isinstance(value, complex):
        return acb(str(value.real), str(value.imag))
    if isinstance(value, str):
        text = value.strip().replace("i", "j")
        if "j" in text.lower():
            parsed = complex(text)
            return acb(str(parsed.real), str(parsed.imag))
        return arb(text)
    return arb(str(value))


def _certified_result(function: str, value, requested_dps: int, bits: int, flint):
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
