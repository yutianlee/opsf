"""Custom positive-real gamma-ratio method via certified loggamma-ratio."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation, localcontext
from typing import Any

from certsf.backends._common import ensure_dps, make_result
from certsf.methods.loggamma_ratio_stirling import loggamma_ratio_stirling_diff
from certsf.methods.stirling import _safe_positive_string
from certsf.result import SFResult

_CERTIFICATE_SCOPE = "gamma_ratio_positive_real_stirling_ratio"
_CERTIFICATE_LEVEL = "custom_asymptotic_bound"
_AUDIT_STATUS = "theorem_documented"
_CERTIFICATION_CLAIM = (
    "certified positive-real gamma-ratio enclosure via exponentiated certified loggamma-ratio"
)
_DOMAIN = "positive_real_a_b_ge_20"
_FORMULA = "gamma_ratio=exp(loggamma_ratio(a,b))"
_METHOD = "stirling_ratio_gamma_ratio"
_BACKEND = "certsf+python-flint"


def gamma_ratio_stirling_ratio(a: Any, b: Any, *, dps: int = 50) -> SFResult:
    """Certified positive-real ``gamma_ratio(a, b)`` via ``exp(loggamma_ratio)``."""

    requested_dps = ensure_dps(dps)
    log_ratio = loggamma_ratio_stirling_diff(a, b, dps=requested_dps)
    if not log_ratio.certified:
        return _unavailable(
            requested_dps,
            log_ratio.diagnostics.get("error", "certified loggamma_ratio enclosure is unavailable"),
            working_dps=log_ratio.working_dps,
            diagnostics=_project_loggamma_ratio_diagnostics(log_ratio),
        )

    try:
        import flint
    except ImportError:  # pragma: no cover - optional dependency
        return _unavailable(requested_dps, "python-flint is not installed")

    bits = int(log_ratio.diagnostics["working_precision_bits"])
    old_prec = flint.ctx.prec
    flint.ctx.prec = bits
    try:
        log_ratio_ball = _arb_ball_from_midpoint_and_radius(flint, log_ratio.value, log_ratio.abs_error_bound)
        gamma_ratio_ball = log_ratio_ball.exp()
        if not bool(gamma_ratio_ball.is_finite()):
            return _unavailable(
                requested_dps,
                "stirling_ratio gamma_ratio exponentiation produced a non-finite enclosure.",
                working_dps=log_ratio.working_dps,
                diagnostics={"working_precision_bits": bits},
            )

        abs_error_bound = _safe_positive_string(gamma_ratio_ball.rad(), requested_dps, flint)
        propagated_log_ratio_bound = gamma_ratio_ball.abs_upper() * flint.arb(log_ratio.abs_error_bound)
        diagnostics = _diagnostics(bits)
        diagnostics.update(_project_loggamma_ratio_diagnostics(log_ratio))
        diagnostics.update(
            {
                "loggamma_ratio_method_used": "stirling_diff",
                "loggamma_ratio_result_method": log_ratio.method,
                "loggamma_ratio_abs_error_bound": log_ratio.abs_error_bound,
                "exp_radius": abs_error_bound,
                "propagated_error_bound": _safe_positive_string(
                    propagated_log_ratio_bound,
                    requested_dps,
                    flint,
                ),
            }
        )
        return make_result(
            function="gamma_ratio",
            value=_arb_value_string(gamma_ratio_ball),
            abs_error_bound=abs_error_bound,
            rel_error_bound=_relative_error_bound(abs_error_bound, gamma_ratio_ball),
            certified=True,
            method=_METHOD,
            backend=_BACKEND,
            requested_dps=requested_dps,
            working_dps=log_ratio.working_dps,
            terms_used=log_ratio.terms_used,
            diagnostics=diagnostics,
        )
    except Exception as exc:  # pragma: no cover - depends on optional backend domains
        return _unavailable(
            requested_dps,
            f"stirling_ratio gamma_ratio method failed cleanly: {exc}",
            working_dps=log_ratio.working_dps,
            diagnostics={"working_precision_bits": bits},
        )
    finally:
        flint.ctx.prec = old_prec


def _arb_ball_from_midpoint_and_radius(flint, midpoint: str, radius: str | None):
    center = flint.arb(midpoint)
    if radius is None:
        return center
    bound = flint.arb(radius)
    return (center - bound).union(center + bound)


def _project_loggamma_ratio_diagnostics(log_ratio: SFResult) -> dict[str, Any]:
    source = dict(log_ratio.diagnostics)
    projected: dict[str, Any] = {}
    for key in (
        "a_loggamma_method_used",
        "b_loggamma_method_used",
        "a_loggamma_abs_error_bound",
        "b_loggamma_abs_error_bound",
        "a_terms_used",
        "b_terms_used",
        "a_tail_bound",
        "b_tail_bound",
        "a_shift",
        "a_shifted_argument",
        "a_shift_policy",
        "b_shift",
        "b_shifted_argument",
        "b_shift_policy",
        "combined_abs_error_bound",
    ):
        if key in source:
            projected[key] = source[key]
    if "error" in source:
        projected["loggamma_ratio_error"] = source["error"]
    return projected


def _diagnostics(bits: int | None) -> dict[str, Any]:
    diagnostics: dict[str, Any] = {
        "mode": "certified",
        "selected_method": "stirling_ratio",
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
    result_diagnostics["error"] = str(message)
    if diagnostics is not None:
        for key, value in diagnostics.items():
            if key not in {"mode", "fallback", "certificate_scope"}:
                result_diagnostics[key] = value
    return make_result(
        function="gamma_ratio",
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
