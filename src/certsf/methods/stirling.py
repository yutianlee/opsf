"""Custom positive-real Stirling method for ``loggamma``."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation, ROUND_FLOOR, localcontext
import math
from typing import Any

from certsf.backends._common import ensure_dps, make_result
from certsf.methods.stirling_coefficients import STIRLING_COEFFICIENTS
from certsf.result import SFResult

_CERTIFICATE_SCOPE = "stirling_loggamma_positive_real"
_CERTIFICATE_LEVEL = "custom_asymptotic_bound"
_AUDIT_STATUS = "theorem_documented"
_CERTIFICATION_CLAIM = "certified positive-real Stirling loggamma enclosure with explicit asymptotic tail bound"
_DOMAIN = "positive_real_x_ge_20"
_FORMULA = "stirling_loggamma"
_METHOD = "stirling_loggamma"
_SHIFTED_FORMULA = "stirling_shifted_loggamma"
_SHIFTED_METHOD = "stirling_shifted_loggamma"
_BACKEND = "certsf+python-flint"
GUARD_DIGITS = 2
_MAX_TERMS = 256
_MAX_SHIFT = 10000


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


def stirling_loggamma_shifted(x: Any, *, dps: int = 50) -> SFResult:
    """Certified shifted positive-real Stirling enclosure for ``loggamma(x)``."""

    requested_dps = ensure_dps(dps)
    effective_dps = requested_dps + GUARD_DIGITS
    x_text, domain_error = _positive_real_text(x)
    if domain_error is not None:
        return _unavailable_shifted(requested_dps, effective_dps, domain_error)

    try:
        import flint
    except ImportError:  # pragma: no cover - optional dependency
        return _unavailable_shifted(requested_dps, effective_dps, "python-flint is not installed")

    x_decimal = Decimal(x_text)
    bits = _working_bits(effective_dps)
    old_prec = flint.ctx.prec
    flint.ctx.prec = bits
    try:
        argument = flint.arb(x_text)
        target_tolerance = flint.arb(10) ** (-effective_dps)
        shift, shift_policy, terms_used, tail_bound = _select_shifted_policy(
            flint,
            argument,
            x_decimal,
            effective_dps,
            target_tolerance,
        )
        if terms_used is None or tail_bound is None:
            final_shift = 0 if shift is None else shift
            final_argument = argument + flint.arb(final_shift)
            final_tail = _tail_bound_from_coefficient(flint, final_argument, _MAX_TERMS)
            return _unavailable_shifted(
                requested_dps,
                effective_dps,
                "Shifted Stirling loggamma tail bound did not reach the requested tolerance within the shift/term cap.",
                working_dps=_bits_to_dps(bits),
                diagnostics={
                    "working_precision_bits": bits,
                    "shift": final_shift,
                    "shifted_argument": _decimal_string(x_decimal + Decimal(final_shift)),
                    "shift_policy": shift_policy,
                    "terms_attempted": _MAX_TERMS,
                    "final_tail_bound": _safe_positive_string(final_tail, requested_dps, flint),
                    "requested_tolerance": _safe_positive_string(target_tolerance, requested_dps, flint),
                    "coefficient_source": _coefficient_source(_MAX_TERMS + 1),
                    "largest_bernoulli_used": 2 * _MAX_TERMS + 2,
                },
            )
        assert shift is not None
        assert terms_used is not None
        assert tail_bound is not None

        shifted_argument = argument + flint.arb(shift)
        value = _stirling_sum_with_coefficients(flint, shifted_argument, terms_used)
        for offset in range(shift):
            value -= (argument + flint.arb(offset)).log()
        if not bool(value.is_finite()):
            return _unavailable_shifted(
                requested_dps,
                effective_dps,
                "Shifted Stirling loggamma finite sum produced a non-finite enclosure.",
                working_dps=_bits_to_dps(bits),
                diagnostics={"working_precision_bits": bits, "shift": shift, "stirling_terms": terms_used},
            )

        finite_radius = value.rad()
        total_bound = finite_radius + tail_bound
        abs_error_bound = _safe_positive_string(total_bound, requested_dps, flint)
        tail_bound_text = _safe_positive_string(tail_bound, requested_dps, flint)
        diagnostics = _shifted_diagnostics(bits, effective_dps)
        diagnostics.update(
            {
                "shift": shift,
                "shifted_argument": _decimal_string(x_decimal + Decimal(shift)),
                "shift_policy": shift_policy,
                "terms_used": terms_used,
                "stirling_terms": terms_used,
                "largest_bernoulli_used": 2 * terms_used + 2,
                "coefficient_source": _coefficient_source(terms_used + 1),
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
            method=_SHIFTED_METHOD,
            backend=_BACKEND,
            requested_dps=requested_dps,
            working_dps=_bits_to_dps(bits),
            terms_used=terms_used,
            diagnostics=diagnostics,
        )
    except Exception as exc:  # pragma: no cover - depends on optional backend domains
        return _unavailable_shifted(
            requested_dps,
            effective_dps,
            f"Shifted Stirling loggamma method failed cleanly: {exc}",
            working_dps=_bits_to_dps(bits),
            diagnostics={"working_precision_bits": bits},
        )
    finally:
        flint.ctx.prec = old_prec


def _stirling_loggamma_ball(
    x: Any,
    *,
    dps: int = 50,
    shifted: bool | None = None,
) -> dict[str, Any]:
    """Return an internal Arb enclosure for positive-real ``loggamma(x)``.

    The returned ball includes the finite-sum Arb radius and the explicit
    positive-real Stirling tail bound. It is intentionally internal because the
    public ``loggamma`` result contract exposes strings, while downstream
    certified methods need the Arb ball before any nonlinear post-processing.
    """

    requested_dps = ensure_dps(dps)
    x_text, domain_error = _positive_real_text(x)
    if domain_error is not None:
        return _loggamma_ball_unavailable(requested_dps, domain_error)

    if shifted is None:
        unshifted_estimate = estimate_stirling_terms_for_tolerance(x_text, dps=requested_dps)
        shifted = not bool(unshifted_estimate.get("can_certify"))

    if shifted:
        return _stirling_loggamma_ball_shifted(x_text, requested_dps)
    return _stirling_loggamma_ball_unshifted(x_text, requested_dps)


def _stirling_loggamma_ball_unshifted(x_text: str, requested_dps: int) -> dict[str, Any]:
    try:
        import flint
    except ImportError:  # pragma: no cover - optional dependency
        return _loggamma_ball_unavailable(requested_dps, "python-flint is not installed")

    bits = _working_bits(requested_dps)
    old_prec = flint.ctx.prec
    flint.ctx.prec = bits
    try:
        argument = flint.arb(x_text)
        target_tolerance = flint.arb(10) ** (-(requested_dps + GUARD_DIGITS))
        terms_used, tail_bound = _select_terms(flint, argument, target_tolerance)
        if terms_used is None or tail_bound is None:
            final_tail = _tail_bound(flint, argument, _MAX_TERMS)
            return _loggamma_ball_unavailable(
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

        finite_ball = _stirling_sum(flint, argument, terms_used)
        if not bool(finite_ball.is_finite()):
            return _loggamma_ball_unavailable(
                requested_dps,
                "Stirling loggamma finite sum produced a non-finite enclosure.",
                working_dps=_bits_to_dps(bits),
                diagnostics={"working_precision_bits": bits, "terms_used": terms_used},
            )

        loggamma_ball = _widen_arb_ball(flint, finite_ball, tail_bound)
        tail_bound_text = _safe_positive_string(tail_bound, requested_dps, flint)
        diagnostics = _diagnostics(bits)
        diagnostics.update(
            {
                "terms_used": terms_used,
                "tail_bound": tail_bound_text,
                "requested_tolerance": _safe_positive_string(target_tolerance, requested_dps, flint),
            }
        )
        return {
            "certified": True,
            "ball": loggamma_ball,
            "finite_ball": finite_ball,
            "terms_used": terms_used,
            "tail_bound": tail_bound,
            "tail_bound_text": tail_bound_text,
            "abs_error_bound": _safe_positive_string(loggamma_ball.rad(), requested_dps, flint),
            "loggamma_method_used": "stirling",
            "working_dps": _bits_to_dps(bits),
            "working_precision_bits": bits,
            "diagnostics": diagnostics,
        }
    except Exception as exc:  # pragma: no cover - depends on optional backend domains
        return _loggamma_ball_unavailable(
            requested_dps,
            f"Stirling loggamma method failed cleanly: {exc}",
            working_dps=_bits_to_dps(bits),
            diagnostics={"working_precision_bits": bits},
        )
    finally:
        flint.ctx.prec = old_prec


def _stirling_loggamma_ball_shifted(x_text: str, requested_dps: int) -> dict[str, Any]:
    effective_dps = requested_dps + GUARD_DIGITS
    try:
        import flint
    except ImportError:  # pragma: no cover - optional dependency
        return _loggamma_ball_unavailable(
            requested_dps,
            "python-flint is not installed",
            diagnostics={"guard_digits": GUARD_DIGITS, "effective_dps": effective_dps},
        )

    x_decimal = Decimal(x_text)
    bits = _working_bits(effective_dps)
    old_prec = flint.ctx.prec
    flint.ctx.prec = bits
    try:
        argument = flint.arb(x_text)
        target_tolerance = flint.arb(10) ** (-effective_dps)
        shift, shift_policy, terms_used, tail_bound = _select_shifted_policy(
            flint,
            argument,
            x_decimal,
            effective_dps,
            target_tolerance,
        )
        if terms_used is None or tail_bound is None:
            final_shift = 0 if shift is None else shift
            final_argument = argument + flint.arb(final_shift)
            final_tail = _tail_bound_from_coefficient(flint, final_argument, _MAX_TERMS)
            return _loggamma_ball_unavailable(
                requested_dps,
                "Shifted Stirling loggamma tail bound did not reach the requested tolerance within the shift/term cap.",
                working_dps=_bits_to_dps(bits),
                diagnostics={
                    "working_precision_bits": bits,
                    "guard_digits": GUARD_DIGITS,
                    "effective_dps": effective_dps,
                    "shift": final_shift,
                    "shifted_argument": _decimal_string(x_decimal + Decimal(final_shift)),
                    "shift_policy": shift_policy,
                    "terms_attempted": _MAX_TERMS,
                    "final_tail_bound": _safe_positive_string(final_tail, requested_dps, flint),
                    "requested_tolerance": _safe_positive_string(target_tolerance, requested_dps, flint),
                    "coefficient_source": _coefficient_source(_MAX_TERMS + 1),
                    "largest_bernoulli_used": 2 * _MAX_TERMS + 2,
                },
            )
        assert shift is not None
        assert terms_used is not None
        assert tail_bound is not None

        shifted_argument = argument + flint.arb(shift)
        finite_ball = _stirling_sum_with_coefficients(flint, shifted_argument, terms_used)
        for offset in range(shift):
            finite_ball -= (argument + flint.arb(offset)).log()
        if not bool(finite_ball.is_finite()):
            return _loggamma_ball_unavailable(
                requested_dps,
                "Shifted Stirling loggamma finite sum produced a non-finite enclosure.",
                working_dps=_bits_to_dps(bits),
                diagnostics={
                    "working_precision_bits": bits,
                    "guard_digits": GUARD_DIGITS,
                    "effective_dps": effective_dps,
                    "shift": shift,
                    "stirling_terms": terms_used,
                },
            )

        loggamma_ball = _widen_arb_ball(flint, finite_ball, tail_bound)
        tail_bound_text = _safe_positive_string(tail_bound, requested_dps, flint)
        diagnostics = _shifted_diagnostics(bits, effective_dps)
        diagnostics.update(
            {
                "shift": shift,
                "shifted_argument": _decimal_string(x_decimal + Decimal(shift)),
                "shift_policy": shift_policy,
                "terms_used": terms_used,
                "stirling_terms": terms_used,
                "largest_bernoulli_used": 2 * terms_used + 2,
                "coefficient_source": _coefficient_source(terms_used + 1),
                "tail_bound": tail_bound_text,
                "requested_tolerance": _safe_positive_string(target_tolerance, requested_dps, flint),
            }
        )
        return {
            "certified": True,
            "ball": loggamma_ball,
            "finite_ball": finite_ball,
            "terms_used": terms_used,
            "tail_bound": tail_bound,
            "tail_bound_text": tail_bound_text,
            "abs_error_bound": _safe_positive_string(loggamma_ball.rad(), requested_dps, flint),
            "loggamma_method_used": "stirling_shifted",
            "working_dps": _bits_to_dps(bits),
            "working_precision_bits": bits,
            "diagnostics": diagnostics,
        }
    except Exception as exc:  # pragma: no cover - depends on optional backend domains
        return _loggamma_ball_unavailable(
            requested_dps,
            f"Shifted Stirling loggamma method failed cleanly: {exc}",
            working_dps=_bits_to_dps(bits),
            diagnostics={"working_precision_bits": bits, "guard_digits": GUARD_DIGITS, "effective_dps": effective_dps},
        )
    finally:
        flint.ctx.prec = old_prec


def _widen_arb_ball(flint, value, extra_radius):
    total_radius = value.rad() + extra_radius
    center = flint.arb(value.mid())
    # python-flint 0.8 exposes interval union rather than direct radius
    # mutation. The union of midpoint-total_radius and midpoint+total_radius
    # is an Arb ball containing the finite expression plus the explicit tail.
    return (center - total_radius).union(center + total_radius)


def _loggamma_ball_unavailable(
    requested_dps: int,
    message: str,
    *,
    working_dps: int | None = None,
    diagnostics: dict[str, Any] | None = None,
) -> dict[str, Any]:
    result_diagnostics = {"mode": "certified", "error": message, "fallback": []}
    if diagnostics is not None:
        result_diagnostics.update(diagnostics)
    return {
        "certified": False,
        "error": message,
        "working_dps": requested_dps if working_dps is None else working_dps,
        "diagnostics": result_diagnostics,
    }


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


def estimate_stirling_terms_for_tolerance(x: Any, *, dps: int = 50) -> dict[str, Any]:
    """Estimate unshifted Stirling certifiability without the finite sum."""

    requested_dps = ensure_dps(dps)
    x_text, domain_error = _positive_real_text(x)
    if domain_error is not None:
        return _preselection_unavailable("stirling", requested_dps, domain_error)

    try:
        import flint
    except ImportError:  # pragma: no cover - optional dependency
        return _preselection_unavailable("stirling", requested_dps, "python-flint is not installed")

    bits = _working_bits(requested_dps)
    old_prec = flint.ctx.prec
    flint.ctx.prec = bits
    try:
        argument = flint.arb(x_text)
        target_tolerance = flint.arb(10) ** (-(requested_dps + GUARD_DIGITS))
        terms_used, tail_bound = _select_terms(flint, argument, target_tolerance)
        base = _preselection_base("stirling", requested_dps)
        base.update(
            {
                "working_precision_bits": bits,
                "requested_tolerance": _safe_positive_string(target_tolerance, requested_dps, flint),
            }
        )
        if terms_used is None or tail_bound is None:
            final_tail = _tail_bound(flint, argument, _MAX_TERMS)
            base.update(
                {
                    "can_certify": False,
                    "estimated_terms_used": None,
                    "terms_attempted": _MAX_TERMS,
                    "final_tail_bound": _safe_positive_string(final_tail, requested_dps, flint),
                    "error": "Stirling loggamma tail bound did not reach the requested tolerance within the term cap.",
                    "reason": "unshifted Stirling tail bound does not reach the requested tolerance within the term cap",
                }
            )
            return base

        base.update(
            {
                "can_certify": True,
                "estimated_terms_used": terms_used,
                "tail_bound": _safe_positive_string(tail_bound, requested_dps, flint),
                "reason": "unshifted Stirling tail bound satisfies the requested tolerance",
            }
        )
        return base
    except Exception as exc:  # pragma: no cover - depends on optional backend domains
        return _preselection_unavailable(
            "stirling",
            requested_dps,
            f"unshifted Stirling preselection failed cleanly: {exc}",
        )
    finally:
        flint.ctx.prec = old_prec


def estimate_shifted_stirling_policy(x: Any, *, dps: int = 50) -> dict[str, Any]:
    """Estimate shifted Stirling certifiability without logs or the finite sum."""

    requested_dps = ensure_dps(dps)
    effective_dps = requested_dps + GUARD_DIGITS
    x_text, domain_error = _positive_real_text(x)
    if domain_error is not None:
        return _preselection_unavailable(
            "stirling_shifted",
            requested_dps,
            domain_error,
            effective_dps=effective_dps,
        )

    try:
        import flint
    except ImportError:  # pragma: no cover - optional dependency
        return _preselection_unavailable(
            "stirling_shifted",
            requested_dps,
            "python-flint is not installed",
            effective_dps=effective_dps,
        )

    x_decimal = Decimal(x_text)
    bits = _working_bits(effective_dps)
    old_prec = flint.ctx.prec
    flint.ctx.prec = bits
    try:
        argument = flint.arb(x_text)
        target_tolerance = flint.arb(10) ** (-effective_dps)
        shift, shift_policy, terms_used, tail_bound = _select_shifted_policy(
            flint,
            argument,
            x_decimal,
            effective_dps,
            target_tolerance,
        )
        final_shift = 0 if shift is None else shift
        shifted_argument_text = _decimal_string(x_decimal + Decimal(final_shift))
        base = _preselection_base("stirling_shifted", requested_dps, effective_dps=effective_dps)
        base.update(
            {
                "working_precision_bits": bits,
                "shift": final_shift,
                "shifted_argument": shifted_argument_text,
                "shift_policy": shift_policy,
                "guard_digits": GUARD_DIGITS,
                "effective_dps": effective_dps,
                "requested_tolerance": _safe_positive_string(target_tolerance, requested_dps, flint),
            }
        )
        if terms_used is None or tail_bound is None:
            final_argument = argument + flint.arb(final_shift)
            final_tail = _tail_bound_from_coefficient(flint, final_argument, _MAX_TERMS)
            base.update(
                {
                    "can_certify": False,
                    "estimated_terms_used": None,
                    "terms_attempted": _MAX_TERMS,
                    "final_tail_bound": _safe_positive_string(final_tail, requested_dps, flint),
                    "coefficient_source": _coefficient_source(_MAX_TERMS + 1),
                    "largest_bernoulli_used": 2 * _MAX_TERMS + 2,
                    "error": "Shifted Stirling loggamma tail bound did not reach the requested tolerance within the shift/term cap.",
                    "reason": "shifted Stirling tail bound does not reach the requested tolerance within the shift/term cap",
                }
            )
            return base

        base.update(
            {
                "can_certify": True,
                "estimated_terms_used": terms_used,
                "tail_bound": _safe_positive_string(tail_bound, requested_dps, flint),
                "coefficient_source": _coefficient_source(terms_used + 1),
                "largest_bernoulli_used": 2 * terms_used + 2,
                "reason": "shifted Stirling tail bound satisfies the requested tolerance",
            }
        )
        return base
    except Exception as exc:  # pragma: no cover - depends on optional backend domains
        return _preselection_unavailable(
            "stirling_shifted",
            requested_dps,
            f"shifted Stirling preselection failed cleanly: {exc}",
            effective_dps=effective_dps,
        )
    finally:
        flint.ctx.prec = old_prec


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


def _select_shifted_policy(flint, x, x_decimal: Decimal, effective_dps: int, target_tolerance):
    if effective_dps < 56:
        shift = 0
        shift_policy = "direct_no_shift"
    elif effective_dps <= 102:
        shift = _window_shift(x_decimal)
        shift_policy = "window_37_38"
    else:
        shift_policy = "minimal_shift"
        minimal_shift = _minimal_shift(flint, x, target_tolerance)
        if minimal_shift is None:
            return None, shift_policy, None, None
        shift = minimal_shift

    terms_used, tail_bound = _select_terms_from_coefficients(flint, x + flint.arb(shift), target_tolerance)
    return shift, shift_policy, terms_used, tail_bound


def _window_shift(x: Decimal) -> int:
    if x <= Decimal(37):
        return max(0, int((Decimal(38) - x).to_integral_value(rounding=ROUND_FLOOR)))
    return 0


def _minimal_shift(flint, x, target_tolerance) -> int | None:
    for shift in range(_MAX_SHIFT + 1):
        terms_used, _tail_bound_value = _select_terms_from_coefficients(flint, x + flint.arb(shift), target_tolerance)
        if terms_used is not None:
            return shift
    return None


def _select_terms_from_coefficients(flint, x, target_tolerance):
    for terms_used in range(1, _MAX_TERMS + 1):
        tail_bound = _tail_bound_from_coefficient(flint, x, terms_used)
        if tail_bound < target_tolerance:
            return terms_used, tail_bound
    return None, None


def _tail_bound_from_coefficient(flint, x, terms_used: int):
    omitted_k = terms_used + 1
    return abs(flint.arb(_coefficient(flint, omitted_k))) / (x ** (2 * omitted_k - 1))


def _stirling_sum_with_coefficients(flint, x, terms_used: int):
    half = flint.arb("0.5")
    two = flint.arb(2)
    total = (x - half) * x.log() - x + half * (two * flint.arb.pi()).log()
    for k in range(1, terms_used + 1):
        total += flint.arb(_coefficient(flint, k)) / (x ** (2 * k - 1))
    return total


def _coefficient(flint, k: int):
    if k <= len(STIRLING_COEFFICIENTS):
        return flint.fmpq(STIRLING_COEFFICIENTS[k - 1])
    n = 2 * k
    return flint.fmpq.bernoulli(n) / flint.fmpq(n * (n - 1))


def _coefficient_source(max_k: int) -> str:
    return "table" if max_k <= len(STIRLING_COEFFICIENTS) else "table+flint_fallback"


def _preselection_base(
    method_id: str,
    requested_dps: int,
    *,
    effective_dps: int | None = None,
) -> dict[str, Any]:
    result_method = _SHIFTED_METHOD if method_id == "stirling_shifted" else _METHOD
    base: dict[str, Any] = {
        "method": method_id,
        "preselected": True,
        "can_certify": False,
        "estimated_terms_used": None,
        "result_method": result_method,
        "backend": _BACKEND,
        "certificate_scope": _CERTIFICATE_SCOPE,
        "max_terms": _MAX_TERMS,
        "requested_dps": requested_dps,
    }
    if effective_dps is not None:
        base["effective_dps"] = effective_dps
    return base


def _preselection_unavailable(
    method_id: str,
    requested_dps: int,
    reason: str,
    *,
    effective_dps: int | None = None,
) -> dict[str, Any]:
    base = _preselection_base(method_id, requested_dps, effective_dps=effective_dps)
    base.update({"reason": reason, "error": reason})
    return base


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


def _unavailable_shifted(
    requested_dps: int,
    effective_dps: int,
    message: str,
    *,
    working_dps: int | None = None,
    diagnostics: dict[str, Any] | None = None,
) -> SFResult:
    result_diagnostics = _shifted_diagnostics(None, effective_dps)
    result_diagnostics["error"] = message
    if diagnostics is not None:
        result_diagnostics.update(diagnostics)
    return make_result(
        function="loggamma",
        value="",
        abs_error_bound=None,
        rel_error_bound=None,
        certified=False,
        method=_SHIFTED_METHOD,
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


def _shifted_diagnostics(bits: int | None, effective_dps: int) -> dict[str, Any]:
    diagnostics: dict[str, Any] = {
        "mode": "certified",
        "selected_method": "stirling_shifted",
        "certificate_scope": _CERTIFICATE_SCOPE,
        "certificate_level": _CERTIFICATE_LEVEL,
        "audit_status": _AUDIT_STATUS,
        "certification_claim": _CERTIFICATION_CLAIM,
        "formula": _SHIFTED_FORMULA,
        "domain": _DOMAIN,
        "fallback": [],
        "max_terms": _MAX_TERMS,
        "guard_digits": GUARD_DIGITS,
        "effective_dps": effective_dps,
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


def _decimal_string(value: Decimal) -> str:
    text = format(value, "f")
    if "." in text:
        return text.rstrip("0").rstrip(".")
    return text
