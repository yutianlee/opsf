"""Custom positive-real beta method via certified loggamma combination."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation, localcontext
from typing import Any

from certsf.backends._common import ensure_dps, make_result
from certsf.methods.stirling import _safe_positive_string, _stirling_loggamma_ball
from certsf.result import SFResult

_CERTIFICATE_SCOPE = "beta_positive_real_stirling_beta"
_CERTIFICATE_LEVEL = "custom_asymptotic_bound"
_AUDIT_STATUS = "theorem_documented"
_CERTIFICATION_CLAIM = "certified positive-real beta enclosure via exponentiated certified loggamma combination"
_DOMAIN = "positive_real_a_b_ge_20"
_FORMULA = "beta=exp(loggamma(a)+loggamma(b)-loggamma(a+b))"
_METHOD = "stirling_beta_beta"
_BACKEND = "certsf+python-flint"
_MIN_ARGUMENT = Decimal(20)


def beta_stirling_beta(a: Any, b: Any, *, dps: int = 50) -> SFResult:
    """Certified positive-real ``beta(a, b)`` via internal loggamma Arb balls."""

    requested_dps = ensure_dps(dps)
    a_text, a_error = _positive_real_ge_20_text(a, "a")
    if a_error is not None:
        return _unavailable(requested_dps, a_error)
    b_text, b_error = _positive_real_ge_20_text(b, "b")
    if b_error is not None:
        return _unavailable(requested_dps, b_error)
    assert a_text is not None
    assert b_text is not None
    sum_text = _decimal_string(Decimal(a_text) + Decimal(b_text))

    loggamma_a = _stirling_loggamma_ball(a_text, dps=requested_dps, shifted=None)
    if not loggamma_a.get("certified"):
        return _unavailable(
            requested_dps,
            str(loggamma_a.get("error", "certified loggamma(a) enclosure is unavailable")),
            working_dps=_working_dps(loggamma_a, requested_dps),
            diagnostics={"a_error": str(loggamma_a.get("error", "certified loggamma(a) enclosure is unavailable"))},
        )

    loggamma_b = _stirling_loggamma_ball(b_text, dps=requested_dps, shifted=None)
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

    loggamma_sum = _stirling_loggamma_ball(sum_text, dps=requested_dps, shifted=None)
    if not loggamma_sum.get("certified"):
        return _unavailable(
            requested_dps,
            str(loggamma_sum.get("error", "certified loggamma(a+b) enclosure is unavailable")),
            working_dps=max(
                _working_dps(loggamma_a, requested_dps),
                _working_dps(loggamma_b, requested_dps),
                _working_dps(loggamma_sum, requested_dps),
            ),
            diagnostics={
                "a_loggamma_method_used": str(loggamma_a.get("loggamma_method_used", "")),
                "b_loggamma_method_used": str(loggamma_b.get("loggamma_method_used", "")),
                "sum_error": str(loggamma_sum.get("error", "certified loggamma(a+b) enclosure is unavailable")),
            },
        )

    try:
        import flint
    except ImportError:  # pragma: no cover - optional dependency
        return _unavailable(requested_dps, "python-flint is not installed")

    bits = max(
        int(loggamma_a["working_precision_bits"]),
        int(loggamma_b["working_precision_bits"]),
        int(loggamma_sum["working_precision_bits"]),
    )
    old_prec = flint.ctx.prec
    flint.ctx.prec = bits
    try:
        log_beta_ball = loggamma_a["ball"] + loggamma_b["ball"] - loggamma_sum["ball"]
        if not bool(log_beta_ball.is_finite()):
            return _unavailable(
                requested_dps,
                "stirling_beta beta log combination produced a non-finite enclosure.",
                working_dps=_max_working_dps(requested_dps, loggamma_a, loggamma_b, loggamma_sum),
                diagnostics={"working_precision_bits": bits},
            )

        beta_ball = log_beta_ball.exp()
        if not bool(beta_ball.is_finite()):
            return _unavailable(
                requested_dps,
                "stirling_beta beta exponentiation produced a non-finite enclosure.",
                working_dps=_max_working_dps(requested_dps, loggamma_a, loggamma_b, loggamma_sum),
                diagnostics={"working_precision_bits": bits},
            )

        abs_error_bound = _safe_positive_string(beta_ball.rad(), requested_dps, flint)
        propagated_log_bound = beta_ball.abs_upper() * log_beta_ball.rad()
        diagnostics = _diagnostics(bits)
        diagnostics.update(_loggamma_diagnostics("a", loggamma_a))
        diagnostics.update(_loggamma_diagnostics("b", loggamma_b))
        diagnostics.update(_loggamma_diagnostics("sum", loggamma_sum))
        diagnostics.update(
            {
                "sum_argument": sum_text,
                "combined_log_abs_error_bound": _safe_positive_string(log_beta_ball.rad(), requested_dps, flint),
                "exp_radius": abs_error_bound,
                "propagated_error_bound": _safe_positive_string(propagated_log_bound, requested_dps, flint),
            }
        )
        return make_result(
            function="beta",
            value=_arb_value_string(beta_ball),
            abs_error_bound=abs_error_bound,
            rel_error_bound=_relative_error_bound(abs_error_bound, beta_ball),
            certified=True,
            method=_METHOD,
            backend=_BACKEND,
            requested_dps=requested_dps,
            working_dps=_max_working_dps(requested_dps, loggamma_a, loggamma_b, loggamma_sum),
            terms_used=max(
                int(loggamma_a["terms_used"]),
                int(loggamma_b["terms_used"]),
                int(loggamma_sum["terms_used"]),
            ),
            diagnostics=diagnostics,
        )
    except Exception as exc:  # pragma: no cover - depends on optional backend domains
        return _unavailable(
            requested_dps,
            f"stirling_beta beta method failed cleanly: {exc}",
            working_dps=_max_working_dps(requested_dps, loggamma_a, loggamma_b, loggamma_sum),
            diagnostics={"working_precision_bits": bits},
        )
    finally:
        flint.ctx.prec = old_prec


def _positive_real_ge_20_text(value: Any, label: str) -> tuple[str | None, str | None]:
    if isinstance(value, complex):
        return None, f"stirling_beta beta requires finite real {label} >= 20; complex inputs are unsupported."
    try:
        if isinstance(value, str):
            text = value.strip().replace("i", "j")
            if "j" in text.lower():
                return None, f"stirling_beta beta requires finite real {label} >= 20; complex inputs are unsupported."
        else:
            text = str(value)
        decimal = Decimal(text)
    except (InvalidOperation, ValueError):
        return None, f"stirling_beta beta requires finite real {label} >= 20."
    if not decimal.is_finite():
        return None, f"stirling_beta beta requires finite real {label} >= 20; non-finite inputs are unsupported."
    if decimal < _MIN_ARGUMENT:
        return None, f"stirling_beta beta requires finite real {label} >= 20."
    return _decimal_string(decimal), None


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
        "selected_method": "stirling_beta",
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
        function="beta",
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


def _max_working_dps(requested_dps: int, *loggammas: dict[str, Any]) -> int:
    return max(_working_dps(loggamma, requested_dps) for loggamma in loggammas)


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


def _decimal_string(decimal: Decimal) -> str:
    text = format(decimal, "f")
    return text.rstrip("0").rstrip(".") if "." in text else text


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
