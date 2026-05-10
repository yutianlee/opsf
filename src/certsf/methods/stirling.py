"""Custom positive-real Stirling method for ``loggamma``."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation, localcontext
import math
from typing import Any

from certsf.backends._common import ensure_dps, make_result
from certsf.result import SFResult

_CERTIFICATE_SCOPE = "stirling_loggamma_positive_real"
_CERTIFICATE_LEVEL = "custom_asymptotic_bound"
_AUDIT_STATUS = "theorem_documented"
_CERTIFICATION_CLAIM = "certified positive-real Stirling loggamma enclosure with explicit asymptotic tail bound"
_DOMAIN = "positive_real_x_ge_20"
_FORMULA = "stirling_loggamma"
_METHOD = "stirling_loggamma"
_BACKEND = "certsf+python-flint"
_MAX_TERMS = 256


def stirling_loggamma(x: Any, *, dps: int = 50) -> SFResult:
    """Certified positive-real Stirling enclosure for ``loggamma(x)``."""

    requested_dps = ensure_dps(dps)
    x_text, domain_error = _positive_real_text(x)
    if domain_error is not None:
        return _unavailable(requested_dps, domain_error)

    try:
        import flint
    except ImportError:  # pragma: no cover - optional dependency
        return _unavailable(requested_dps, "python-flint is not installed")

    bits = _working_bits(requested_dps)
    old_prec = flint.ctx.prec
    flint.ctx.prec = bits
    try:
        argument = flint.arb(x_text)
        target_tolerance = flint.arb(10) ** (-(requested_dps + 2))
        terms_used, tail_bound = _select_terms(flint, argument, target_tolerance)
        if terms_used is None or tail_bound is None:
            final_tail = _tail_bound(flint, argument, _MAX_TERMS)
            return _unavailable(
                requested_dps,
                "Stirling loggamma tail bound did not reach the requested tolerance within the term cap.",
                working_dps=_bits_to_dps(bits),
                diagnostics={
                    "working_precision_bits": bits,
                    "terms_attempted": _MAX_TERMS,
                    "final_tail_bound": _safe_positive_string(final_tail, requested_dps, flint),
                    "requested_tolerance": _safe_positive_string(target_tolerance, requested_dps, flint),
                },
            )

        value = _stirling_sum(flint, argument, terms_used)
        if not bool(value.is_finite()):
            return _unavailable(
                requested_dps,
                "Stirling loggamma finite sum produced a non-finite enclosure.",
                working_dps=_bits_to_dps(bits),
                diagnostics={"working_precision_bits": bits, "terms_used": terms_used},
            )

        finite_radius = value.rad()
        total_bound = finite_radius + tail_bound
        abs_error_bound = _safe_positive_string(total_bound, requested_dps, flint)
        tail_bound_text = _safe_positive_string(tail_bound, requested_dps, flint)
        diagnostics = _diagnostics(bits)
        diagnostics.update(
            {
                "terms_used": terms_used,
                "tail_bound": tail_bound_text,
                "requested_tolerance": _safe_positive_string(target_tolerance, requested_dps, flint),
            }
        )
        return make_result(
            function="loggamma",
            value=_arb_mid_string(value),
            abs_error_bound=abs_error_bound,
            rel_error_bound=_relative_error_bound(abs_error_bound, value),
            certified=True,
            method=_METHOD,
            backend=_BACKEND,
            requested_dps=requested_dps,
            working_dps=_bits_to_dps(bits),
            terms_used=terms_used,
            diagnostics=diagnostics,
        )
    except Exception as exc:  # pragma: no cover - depends on optional backend domains
        return _unavailable(
            requested_dps,
            f"Stirling loggamma method failed cleanly: {exc}",
            working_dps=_bits_to_dps(bits),
            diagnostics={"working_precision_bits": bits},
        )
    finally:
        flint.ctx.prec = old_prec


def _positive_real_text(value: Any) -> tuple[str, str | None]:
    if isinstance(value, complex):
        return "", "Stirling loggamma is certified only for real x >= 20; complex inputs are excluded."
    if isinstance(value, str):
        text = value.strip()
        if "j" in text.lower() or "i" in text.lower():
            return "", "Stirling loggamma is certified only for real x >= 20; complex inputs are excluded."
    else:
        text = str(value)
    try:
        decimal = Decimal(text)
    except (InvalidOperation, ValueError):
        return "", "Stirling loggamma requires a finite real input x >= 20."
    if not decimal.is_finite():
        return "", "Stirling loggamma requires a finite real input x >= 20."
    if decimal <= 0:
        return "", "Stirling loggamma excludes x <= 0."
    if decimal < Decimal(20):
        return "", "Stirling loggamma is currently certified only for real x >= 20."
    return format(decimal, "f"), None


def _select_terms(flint, x, target_tolerance) -> tuple[int | None, Any | None]:
    for terms_used in range(1, _MAX_TERMS + 1):
        tail_bound = _tail_bound(flint, x, terms_used)
        if tail_bound < target_tolerance:
            return terms_used, tail_bound
    return None, None


def _tail_bound(flint, x, terms_used: int):
    omitted_index = 2 * terms_used + 2
    bernoulli = abs(flint.arb(flint.fmpq.bernoulli(omitted_index)))
    denominator = flint.arb(omitted_index * (omitted_index - 1)) * (x ** (omitted_index - 1))
    return bernoulli / denominator


def _stirling_sum(flint, x, terms_used: int):
    half = flint.arb("0.5")
    two = flint.arb(2)
    total = (x - half) * x.log() - x + half * (two * flint.arb.pi()).log()
    for k in range(1, terms_used + 1):
        n = 2 * k
        bernoulli = flint.arb(flint.fmpq.bernoulli(n))
        total += bernoulli / (flint.arb(n * (n - 1)) * (x ** (n - 1)))
    return total


def _unavailable(
    requested_dps: int,
    message: str,
    *,
    working_dps: int | None = None,
    diagnostics: dict[str, Any] | None = None,
) -> SFResult:
    result_diagnostics = _diagnostics(None)
    result_diagnostics["error"] = message
    if diagnostics is not None:
        result_diagnostics.update(diagnostics)
    return make_result(
        function="loggamma",
        value="",
        abs_error_bound=None,
        rel_error_bound=None,
        certified=False,
        method=_METHOD,
        backend=_BACKEND,
        requested_dps=requested_dps,
        working_dps=requested_dps if working_dps is None else working_dps,
        diagnostics=result_diagnostics,
    )


def _diagnostics(bits: int | None) -> dict[str, Any]:
    diagnostics: dict[str, Any] = {
        "mode": "certified",
        "selected_method": "stirling",
        "certificate_scope": _CERTIFICATE_SCOPE,
        "certificate_level": _CERTIFICATE_LEVEL,
        "audit_status": _AUDIT_STATUS,
        "certification_claim": _CERTIFICATION_CLAIM,
        "formula": _FORMULA,
        "domain": _DOMAIN,
        "fallback": [],
        "max_terms": _MAX_TERMS,
    }
    if bits is not None:
        diagnostics["working_precision_bits"] = bits
    return diagnostics


def _working_bits(dps: int) -> int:
    return max(128, math.ceil((dps + 20) * math.log2(10)) + 96)


def _bits_to_dps(bits: int) -> int:
    return math.floor(bits / math.log2(10))


def _safe_positive_string(value, dps: int, flint) -> str:
    digits = max(30, dps + 20)
    safe = abs(value).abs_upper() * flint.arb(4)
    return safe.str(digits, radius=False)


def _relative_error_bound(abs_error_bound: str, value) -> str | None:
    try:
        error = Decimal(abs_error_bound)
        midpoint_magnitude = abs(Decimal(_arb_mid_string(value)))
    except (InvalidOperation, ValueError):
        return None
    if midpoint_magnitude <= error:
        return None
    with localcontext() as ctx:
        ctx.prec = 20
        return format(error / (midpoint_magnitude - error), ".6E")


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
    return sign + body.rstrip("0").rstrip(".")
