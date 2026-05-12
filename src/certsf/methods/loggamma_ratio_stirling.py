"""Custom positive-real loggamma-ratio method via certified loggamma differences."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation, localcontext
from typing import Any

from certsf.backends._common import ensure_dps, make_result
from certsf.methods.stirling import _safe_positive_string, _stirling_loggamma_ball
from certsf.result import SFResult

_CERTIFICATE_SCOPE = "loggamma_ratio_positive_real_stirling_diff"
_CERTIFICATE_LEVEL = "custom_asymptotic_bound"
_AUDIT_STATUS = "theorem_documented"
_CERTIFICATION_CLAIM = (
    "certified positive-real loggamma-ratio enclosure via difference of certified loggamma enclosures"
)
_DOMAIN = "positive_real_a_b_ge_20"
_FORMULA = "loggamma_ratio=loggamma(a)-loggamma(b)"
_METHOD = "stirling_diff_loggamma_ratio"
_BACKEND = "certsf+python-flint"


def loggamma_ratio_stirling_diff(a: Any, b: Any, *, dps: int = 50) -> SFResult:
    """Certified positive-real ``loggamma_ratio(a, b)`` via loggamma balls."""

    requested_dps = ensure_dps(dps)
    loggamma_a = _stirling_loggamma_ball(a, dps=requested_dps, shifted=None)
    if not loggamma_a.get("certified"):
        return _unavailable(
            requested_dps,
            str(loggamma_a.get("error", "certified loggamma(a) enclosure is unavailable")),
            working_dps=_working_dps(loggamma_a, requested_dps),
            diagnostics={
                "a_error": str(loggamma_a.get("error", "certified loggamma(a) enclosure is unavailable")),
            },
        )

    loggamma_b = _stirling_loggamma_ball(b, dps=requested_dps, shifted=None)
    if not loggamma_b.get("certified"):
        return _unavailable(
            requested_dps,
            str(loggamma_b.get("error", "certified loggamma(b) enclosure is unavailable")),
            working_dps=max(_working_dps(loggamma_a, requested_dps), _working_dps(loggamma_b, requested_dps)),
            diagnostics={
                "a_loggamma_method_used": str(loggamma_a.get("loggamma_method_used", "")),
                "b_error": str(loggamma_b.get("error", "certified loggamma(b) enclosure is unavailable")),
            },
        )

    try:
        import flint
    except ImportError:  # pragma: no cover - optional dependency
        return _unavailable(requested_dps, "python-flint is not installed")

    bits = max(int(loggamma_a["working_precision_bits"]), int(loggamma_b["working_precision_bits"]))
    old_prec = flint.ctx.prec
    flint.ctx.prec = bits
    try:
        ratio_ball = loggamma_a["ball"] - loggamma_b["ball"]
        if not bool(ratio_ball.is_finite()):
            return _unavailable(
                requested_dps,
                "stirling_diff loggamma_ratio subtraction produced a non-finite enclosure.",
                working_dps=max(_working_dps(loggamma_a, requested_dps), _working_dps(loggamma_b, requested_dps)),
                diagnostics={"working_precision_bits": bits},
            )

        abs_error_bound = _safe_positive_string(ratio_ball.rad(), requested_dps, flint)
        terms_used = max(int(loggamma_a["terms_used"]), int(loggamma_b["terms_used"]))
        diagnostics = _diagnostics(bits)
        diagnostics.update(_loggamma_diagnostics("a", loggamma_a))
        diagnostics.update(_loggamma_diagnostics("b", loggamma_b))
        diagnostics["combined_abs_error_bound"] = abs_error_bound
        return make_result(
            function="loggamma_ratio",
            value=_arb_value_string(ratio_ball),
            abs_error_bound=abs_error_bound,
            rel_error_bound=_relative_error_bound(abs_error_bound, ratio_ball),
            certified=True,
            method=_METHOD,
            backend=_BACKEND,
            requested_dps=requested_dps,
            working_dps=max(_working_dps(loggamma_a, requested_dps), _working_dps(loggamma_b, requested_dps)),
            terms_used=terms_used,
            diagnostics=diagnostics,
        )
    except Exception as exc:  # pragma: no cover - depends on optional backend domains
        return _unavailable(
            requested_dps,
            f"stirling_diff loggamma_ratio method failed cleanly: {exc}",
            working_dps=max(_working_dps(loggamma_a, requested_dps), _working_dps(loggamma_b, requested_dps)),
            diagnostics={"working_precision_bits": bits},
        )
    finally:
        flint.ctx.prec = old_prec


def _loggamma_diagnostics(prefix: str, loggamma: dict[str, Any]) -> dict[str, Any]:
    source = dict(loggamma.get("diagnostics", {}))
    projected: dict[str, Any] = {
        f"{prefix}_loggamma_method_used": loggamma["loggamma_method_used"],
        f"{prefix}_loggamma_abs_error_bound": loggamma["abs_error_bound"],
        f"{prefix}_terms_used": loggamma["terms_used"],
        f"{prefix}_tail_bound": loggamma["tail_bound_text"],
    }
    for key in ("shift", "shifted_argument", "shift_policy"):
        if key in source:
            projected[f"{prefix}_{key}"] = source[key]
    return projected


def _diagnostics(bits: int | None) -> dict[str, Any]:
    diagnostics: dict[str, Any] = {
        "mode": "certified",
        "selected_method": "stirling_diff",
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
            if key not in {"mode", "fallback", "certificate_scope"}:
                result_diagnostics[key] = value
    return make_result(
        function="loggamma_ratio",
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
        radius = Decimal(abs_error_bound)
        magnitude = Decimal(_arb_value_string(value.abs_lower()))
    except (InvalidOperation, ValueError):
        return None
    if magnitude <= 0:
        return None
    with localcontext() as ctx:
        ctx.prec = 20
        return format(radius / magnitude, ".6E")


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
