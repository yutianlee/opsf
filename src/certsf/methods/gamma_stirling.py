"""Custom positive-real gamma method via certified loggamma exponentiation."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation, localcontext
from typing import Any

from certsf.backends._common import ensure_dps, make_result
from certsf.methods.stirling import (
    _safe_positive_string,
    _stirling_loggamma_ball,
)
from certsf.result import SFResult

_CERTIFICATE_SCOPE = "gamma_positive_real_stirling_exp"
_CERTIFICATE_LEVEL = "custom_asymptotic_bound"
_AUDIT_STATUS = "theorem_documented"
_CERTIFICATION_CLAIM = "certified positive-real gamma enclosure via certified loggamma exponentiation"
_DOMAIN = "positive_real_x_ge_20"
_FORMULA = "gamma=exp(loggamma)"
_METHOD = "stirling_exp_gamma"
_BACKEND = "certsf+python-flint"


def gamma_stirling_exp(x: Any, *, dps: int = 50) -> SFResult:
    """Certified positive-real ``gamma(x)`` via an internal loggamma Arb ball."""

    requested_dps = ensure_dps(dps)
    loggamma = _stirling_loggamma_ball(x, dps=requested_dps, shifted=None)
    if not loggamma.get("certified"):
        return _unavailable(
            requested_dps,
            str(loggamma.get("error", "certified loggamma enclosure is unavailable")),
            working_dps=_working_dps(loggamma, requested_dps),
            diagnostics=dict(loggamma.get("diagnostics", {})),
        )

    try:
        import flint
    except ImportError:  # pragma: no cover - optional dependency
        return _unavailable(requested_dps, "python-flint is not installed")

    bits = int(loggamma["working_precision_bits"])
    old_prec = flint.ctx.prec
    flint.ctx.prec = bits
    try:
        loggamma_ball = loggamma["ball"]
        gamma_ball = loggamma_ball.exp()
        if not bool(gamma_ball.is_finite()):
            return _unavailable(
                requested_dps,
                "stirling_exp gamma exponentiation produced a non-finite enclosure.",
                working_dps=_working_dps(loggamma, requested_dps),
                diagnostics={"working_precision_bits": bits},
            )

        abs_error_bound = _safe_positive_string(gamma_ball.rad(), requested_dps, flint)
        propagated_tail = gamma_ball.abs_upper() * loggamma["tail_bound"]
        diagnostics = _diagnostics(bits)
        diagnostics.update(_loggamma_diagnostics(loggamma))
        diagnostics.update(
            {
                "terms_used": loggamma["terms_used"],
                "loggamma_method_used": loggamma["loggamma_method_used"],
                "loggamma_abs_error_bound": loggamma["abs_error_bound"],
                "exp_radius": _safe_positive_string(gamma_ball.rad(), requested_dps, flint),
                "propagated_error_bound": _safe_positive_string(propagated_tail, requested_dps, flint),
            }
        )
        return make_result(
            function="gamma",
            value=_arb_value_string(gamma_ball),
            abs_error_bound=abs_error_bound,
            rel_error_bound=_relative_error_bound(abs_error_bound, gamma_ball),
            certified=True,
            method=_METHOD,
            backend=_BACKEND,
            requested_dps=requested_dps,
            working_dps=_working_dps(loggamma, requested_dps),
            terms_used=int(loggamma["terms_used"]),
            diagnostics=diagnostics,
        )
    except Exception as exc:  # pragma: no cover - depends on optional backend domains
        return _unavailable(
            requested_dps,
            f"stirling_exp gamma method failed cleanly: {exc}",
            working_dps=_working_dps(loggamma, requested_dps),
            diagnostics={"working_precision_bits": bits},
        )
    finally:
        flint.ctx.prec = old_prec


def _loggamma_diagnostics(loggamma: dict[str, Any]) -> dict[str, Any]:
    source = dict(loggamma.get("diagnostics", {}))
    projected: dict[str, Any] = {}
    for key in (
        "tail_bound",
        "requested_tolerance",
        "shift",
        "shifted_argument",
        "shift_policy",
        "guard_digits",
        "effective_dps",
        "stirling_terms",
        "largest_bernoulli_used",
        "coefficient_source",
    ):
        if key in source:
            projected[key] = source[key]
    if "stirling_terms" not in projected and "terms_used" in source:
        projected["stirling_terms"] = source["terms_used"]
    return projected


def _diagnostics(bits: int | None) -> dict[str, Any]:
    diagnostics: dict[str, Any] = {
        "mode": "certified",
        "selected_method": "stirling_exp",
        "certificate_scope": _CERTIFICATE_SCOPE,
        "certificate_level": _CERTIFICATE_LEVEL,
        "audit_status": _AUDIT_STATUS,
        "certification_claim": _CERTIFICATION_CLAIM,
        "domain": _DOMAIN,
        "formula": _FORMULA,
        "fallback": [],
    }
    if bits is not None:
        diagnostics["working_precision_bits"] = bits
    return diagnostics


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
        for key, value in diagnostics.items():
            if key not in {"mode", "fallback"}:
                result_diagnostics[key] = value
    return make_result(
        function="gamma",
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


def _working_dps(loggamma: dict[str, Any], requested_dps: int) -> int:
    return int(loggamma.get("working_dps", requested_dps))


def _relative_error_bound(abs_error_bound: str, value) -> str | None:
    try:
        error = Decimal(abs_error_bound)
        midpoint_magnitude = abs(Decimal(_arb_value_string(value)))
    except (InvalidOperation, ValueError):
        return None
    if midpoint_magnitude <= error:
        return None
    with localcontext() as ctx:
        ctx.prec = 20
        return format(error / (midpoint_magnitude - error), ".6E")


def _arb_value_string(value) -> str:
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
