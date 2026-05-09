"""python-flint / Arb certified-mode wrappers."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation, localcontext
import json
import math
from typing import Any

from ._common import ensure_dps, json_string, make_result

_PHASE1_UNAVAILABLE = "Certified backend unavailable for this function/domain in Phase 1."
_NONFINITE_RESULT = "Certified backend returned a non-finite enclosure."
_DIRECT_ARB_CERTIFICATE_LEVEL = "direct_arb_primitive"
_DIRECT_ARB_AUDIT_STATUS = "audited_direct"
_DIRECT_ARB_CERTIFICATION_CLAIM = "certified Arb enclosure of the documented direct Arb primitive"
_DIRECT_ARB_GAMMA_RATIO_SCOPE = "direct_arb_gamma_ratio"
_DIRECT_ARB_GAMMA_RATIO_CERTIFICATION_CLAIM = (
    "certified Arb enclosure of Gamma(a) * rgamma(b) using direct Arb gamma primitives"
)
_DIRECT_ARB_LOGGAMMA_RATIO_SCOPE = "direct_arb_loggamma_ratio"
_DIRECT_ARB_LOGGAMMA_RATIO_CERTIFICATION_CLAIM = (
    "certified Arb enclosure of principal loggamma(a) - principal loggamma(b) "
    "using direct Arb gamma primitives"
)
_DIRECT_ARB_BETA_SCOPE = "direct_arb_beta"
_DIRECT_ARB_BETA_CERTIFICATION_CLAIM = (
    "certified Arb enclosure of Gamma(a) * Gamma(b) * rgamma(a+b) using direct Arb gamma primitives"
)
_DIRECT_ARB_POCHHAMMER_SCOPE = "direct_arb_pochhammer_product"
_DIRECT_ARB_FINITE_PRODUCT_CERTIFICATE_LEVEL = "direct_arb_finite_product"
_DIRECT_ARB_POCHHAMMER_CERTIFICATION_CLAIM = (
    "certified Arb enclosure of finite product prod_{k=0}^{n-1}(a+k) for nonnegative integer n"
)
_ARB_POCHHAMMER_MAX_PRODUCT_TERMS = 10000
_DIRECT_ARB_ERF_SCOPE = "direct_arb_erf"
_DIRECT_ARB_ERFC_SCOPE = "direct_arb_erfc"
_DIRECT_ARB_ERFCX_SCOPE = "direct_arb_erfcx"
_ARB_ERFCX_FORMULA_SCOPE = "arb_erfcx_formula"
_DIRECT_ARB_ERFI_SCOPE = "direct_arb_erfi"
_ARB_ERFI_FORMULA_SCOPE = "arb_erfi_formula"
_DIRECT_ARB_DAWSON_SCOPE = "direct_arb_dawson"
_ARB_DAWSON_FORMULA_SCOPE = "arb_dawson_formula"
_DIRECT_ARB_ERFINV_SCOPE = "direct_arb_erfinv"
_ARB_ERFINV_REAL_ROOT_SCOPE = "arb_erfinv_real_root"
_ARB_ERFINV_REAL_DOMAIN = "real_x_in_open_interval_minus1_1"
_DIRECT_ARB_ERFCINV_SCOPE = "direct_arb_erfcinv"
_ARB_ERFCINV_VIA_ERFINV_SCOPE = "arb_erfcinv_via_erfinv"
_ARB_ERFCINV_REAL_DOMAIN = "real_x_in_open_interval_0_2"
_DIRECT_ARB_ERF_CERTIFICATION_CLAIM = "certified Arb enclosure of erf(z) using direct Arb error-function primitive"
_DIRECT_ARB_ERFC_CERTIFICATION_CLAIM = (
    "certified Arb enclosure of erfc(z) using direct Arb complementary error-function primitive"
)
_DIRECT_ARB_ERFC_FALLBACK_CERTIFICATION_CLAIM = (
    "certified Arb enclosure of 1 - erf(z) using direct Arb error-function primitive"
)
_DIRECT_ARB_ERFCX_CERTIFICATION_CLAIM = (
    "certified Arb enclosure of erfcx(z) using direct Arb scaled complementary error-function primitive"
)
_DIRECT_ARB_ERFI_CERTIFICATION_CLAIM = (
    "certified Arb enclosure of erfi(z) using direct Arb imaginary error-function primitive"
)
_DIRECT_ARB_DAWSON_CERTIFICATION_CLAIM = "certified Arb enclosure of dawson(z) using direct Arb Dawson primitive"
_DIRECT_ARB_ERFINV_CERTIFICATION_CLAIM = (
    "certified Arb enclosure of real principal erfinv(x) using direct Arb inverse error-function primitive"
)
_DIRECT_ARB_ERFCINV_CERTIFICATION_CLAIM = (
    "certified Arb enclosure of real principal erfcinv(x) using direct Arb inverse complementary error-function primitive"
)
_ARB_ERFINV_REAL_ROOT_CERTIFICATE_LEVEL = "certified_real_root"
_ARB_ERFINV_REAL_ROOT_AUDIT_STATUS = "monotone_real_inverse"
_ARB_ERFINV_REAL_ROOT_CERTIFICATION_CLAIM = (
    "certified real root enclosure for erf(y)-x=0 using monotonicity of real erf"
)
_ARB_ERFCINV_VIA_ERFINV_CERTIFICATION_CLAIM = (
    "certified real inverse enclosure for erfcinv(x)=erfinv(1-x) using monotonicity of real erfc"
)
_ARB_ERFCX_FORMULA = "exp(z^2)*erfc(z)"
_ARB_ERFCX_FORMULA_CERTIFICATE_LEVEL = "formula_audited_alpha"
_ARB_ERFCX_FORMULA_AUDIT_STATUS = "formula_identity"
_ARB_ERFCX_FORMULA_CERTIFICATION_CLAIM = "certified Arb enclosure of exp(z^2)*erfc(z)"
_ARB_ERFI_FORMULA = "-i*erf(i*z)"
_ARB_ERFI_FORMULA_CERTIFICATE_LEVEL = "formula_audited_alpha"
_ARB_ERFI_FORMULA_AUDIT_STATUS = "formula_identity"
_ARB_ERFI_FORMULA_CERTIFICATION_CLAIM = "certified Arb enclosure of -i*erf(i*z)"
_ARB_DAWSON_FORMULA = "sqrt(pi)/2*exp(-z^2)*erfi(z)"
_ARB_DAWSON_FORMULA_CERTIFICATE_LEVEL = "formula_audited_alpha"
_ARB_DAWSON_FORMULA_AUDIT_STATUS = "formula_identity"
_ARB_DAWSON_FORMULA_CERTIFICATION_CLAIM = "certified Arb enclosure of sqrt(pi)/2*exp(-z^2)*erfi(z)"
_PHASE7_PCF_SCOPE = "phase7_hypergeometric_parabolic_cylinder"
_PHASE7_PCF_REAL_PARAMETER_ONLY = "Phase 7 certified parabolic-cylinder supports real parameters only."
_PHASE8_PCF_SCOPE = "phase8_parabolic_cylinder_connections"
_PHASE8_PCFW_REAL_ARGUMENT_ONLY = "Phase 8 certified pcfw supports real arguments only."
_FORMULA_CERTIFICATE_LEVEL = "formula_audited_experimental"
_FORMULA_AUDIT_STATUS = "experimental_formula"
_FORMULA_CERTIFICATION_CLAIM = (
    "certified Arb enclosure of the implemented documented formula; formula audit in progress"
)


def arb_gamma(z, *, dps: int = 50):
    return _with_flint("gamma", dps, lambda: _make_ball(z).gamma())


def arb_loggamma(z, *, dps: int = 50):
    return _with_flint(
        "loggamma",
        dps,
        lambda: _make_ball(z, force_complex=_is_real_nonpositive(z)).lgamma(),
    )


def arb_loggamma_ratio(a, b, *, dps: int = 50):
    requested = ensure_dps(dps)
    numerator_pole = _is_gamma_pole(a)
    denominator_pole = _is_gamma_pole(b)
    if numerator_pole or denominator_pole:
        pole_case = (
            "both_poles"
            if numerator_pole and denominator_pole
            else "numerator_pole"
            if numerator_pole
            else "denominator_pole"
        )
        if numerator_pole and denominator_pole:
            message = "loggamma_ratio is undefined when both Gamma(a) and Gamma(b) have poles."
        elif numerator_pole:
            message = "loggamma_ratio has a non-finite loggamma(a) term because Gamma(a) has a pole."
        else:
            message = "loggamma_ratio has a non-finite loggamma(b) term because Gamma(b) has a pole."
        return _unavailable(
            "loggamma_ratio",
            requested,
            message,
            diagnostics={
                "pole_case": pole_case,
                "numerator_pole": numerator_pole,
                "denominator_pole": denominator_pole,
                "certificate_scope": _DIRECT_ARB_LOGGAMMA_RATIO_SCOPE,
            },
        )

    try:
        flint, old_prec, bits = _enter_flint_context(requested)
    except ImportError as exc:
        return _unavailable("loggamma_ratio", requested, str(exc))
    try:
        value = _make_ball(a, force_complex=_is_real_nonpositive(a)).lgamma() - _make_ball(
            b,
            force_complex=_is_real_nonpositive(b),
        ).lgamma()
        result = _certified_result("loggamma_ratio", value, requested, bits, flint)
        if result.certified:
            diagnostics = dict(result.diagnostics)
            diagnostics.update(
                {
                    "certificate_scope": _DIRECT_ARB_LOGGAMMA_RATIO_SCOPE,
                    "certification_claim": _DIRECT_ARB_LOGGAMMA_RATIO_CERTIFICATION_CLAIM,
                    "branch": "principal_loggamma_difference",
                    "pole_case": "regular",
                    "numerator_pole": False,
                    "denominator_pole": False,
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
        return _unavailable("loggamma_ratio", requested, f"{_PHASE1_UNAVAILABLE} {exc}")
    finally:
        flint.ctx.prec = old_prec


def arb_rgamma(z, *, dps: int = 50):
    return _with_flint("rgamma", dps, lambda: _make_ball(z).rgamma())


def arb_gamma_ratio(a, b, *, dps: int = 50):
    requested = ensure_dps(dps)
    numerator_pole = _is_gamma_pole(a)
    denominator_pole = _is_gamma_pole(b)
    if numerator_pole:
        if denominator_pole:
            return _unavailable(
                "gamma_ratio",
                requested,
                "gamma_ratio is undefined when both Gamma(a) and Gamma(b) have poles.",
                diagnostics={
                    "pole_case": "both_poles",
                    "numerator_pole": True,
                    "denominator_pole": True,
                    "certificate_scope": _DIRECT_ARB_GAMMA_RATIO_SCOPE,
                },
            )
        return _unavailable(
            "gamma_ratio",
            requested,
            "gamma_ratio has a non-finite numerator because Gamma(a) has a pole.",
            diagnostics={
                "pole_case": "numerator_pole",
                "numerator_pole": True,
                "denominator_pole": False,
                "certificate_scope": _DIRECT_ARB_GAMMA_RATIO_SCOPE,
            },
        )

    try:
        flint, old_prec, bits = _enter_flint_context(requested)
    except ImportError as exc:
        return _unavailable("gamma_ratio", requested, str(exc))
    try:
        value = _make_ball(a).gamma() * _make_ball(b).rgamma()
        result = _certified_result("gamma_ratio", value, requested, bits, flint)
        if result.certified:
            diagnostics = dict(result.diagnostics)
            diagnostics.update(
                {
                    "certificate_scope": _DIRECT_ARB_GAMMA_RATIO_SCOPE,
                    "certification_claim": _DIRECT_ARB_GAMMA_RATIO_CERTIFICATION_CLAIM,
                    "pole_case": "denominator_pole_zero" if denominator_pole else "regular",
                    "numerator_pole": False,
                    "denominator_pole": denominator_pole,
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
        return _unavailable("gamma_ratio", requested, f"{_PHASE1_UNAVAILABLE} {exc}")
    finally:
        flint.ctx.prec = old_prec


def arb_erf(z, *, dps: int = 50):
    return _arb_error_function("erf", z, dps=dps)


def arb_erfc(z, *, dps: int = 50):
    return _arb_error_function("erfc", z, dps=dps)


def arb_erfcx(z, *, dps: int = 50):
    requested = ensure_dps(dps)
    try:
        flint, old_prec, bits = _enter_flint_context(requested)
    except ImportError as exc:
        return _unavailable(
            "erfcx",
            requested,
            str(exc),
            diagnostics={"certificate_scope": _ARB_ERFCX_FORMULA_SCOPE},
        )
    try:
        argument = _make_ball(z)
        domain = "real" if isinstance(argument, flint.arb) else "complex"
        method = getattr(argument, "erfcx", None)
        if method is not None:
            result = _certified_result("erfcx", method(), requested, bits, flint)
            return _with_error_function_diagnostics(
                result,
                _DIRECT_ARB_ERFCX_SCOPE,
                domain,
                _DIRECT_ARB_ERFCX_CERTIFICATION_CLAIM,
            )

        erfc_method = getattr(argument, "erfc", None)
        if erfc_method is None:
            return _unavailable(
                "erfcx",
                requested,
                "python-flint does not expose an Arb erfcx or erfc primitive for this value.",
                diagnostics={
                    "certificate_scope": _ARB_ERFCX_FORMULA_SCOPE,
                    "domain": domain,
                    "formula": _ARB_ERFCX_FORMULA,
                },
            )
        value = (argument * argument).exp() * erfc_method()
        result = _certified_result("erfcx", value, requested, bits, flint)
        return _with_error_function_diagnostics(
            result,
            _ARB_ERFCX_FORMULA_SCOPE,
            domain,
            _ARB_ERFCX_FORMULA_CERTIFICATION_CLAIM,
            formula=_ARB_ERFCX_FORMULA,
            certificate_level=_ARB_ERFCX_FORMULA_CERTIFICATE_LEVEL,
            audit_status=_ARB_ERFCX_FORMULA_AUDIT_STATUS,
        )
    except Exception as exc:  # pragma: no cover - depends on optional backend domains
        return _unavailable(
            "erfcx",
            requested,
            f"{_PHASE1_UNAVAILABLE} {exc}",
            diagnostics={"certificate_scope": _ARB_ERFCX_FORMULA_SCOPE, "formula": _ARB_ERFCX_FORMULA},
        )
    finally:
        flint.ctx.prec = old_prec


def arb_erfi(z, *, dps: int = 50):
    requested = ensure_dps(dps)
    try:
        flint, old_prec, bits = _enter_flint_context(requested)
    except ImportError as exc:
        return _unavailable(
            "erfi",
            requested,
            str(exc),
            diagnostics={"certificate_scope": _ARB_ERFI_FORMULA_SCOPE},
        )
    try:
        argument = _make_ball(z)
        domain = "real" if isinstance(argument, flint.arb) else "complex"
        method = getattr(argument, "erfi", None)
        if method is not None:
            result = _certified_result("erfi", method(), requested, bits, flint)
            return _with_error_function_diagnostics(
                result,
                _DIRECT_ARB_ERFI_SCOPE,
                domain,
                _DIRECT_ARB_ERFI_CERTIFICATION_CLAIM,
            )

        erf_argument = flint.acb(argument) if isinstance(argument, flint.arb) else argument
        imaginary_unit = flint.acb(0, 1)
        erf_method = getattr(imaginary_unit * erf_argument, "erf", None)
        if erf_method is None:
            return _unavailable(
                "erfi",
                requested,
                "python-flint does not expose an Arb erfi or erf primitive for this value.",
                diagnostics={
                    "certificate_scope": _ARB_ERFI_FORMULA_SCOPE,
                    "domain": domain,
                    "formula": _ARB_ERFI_FORMULA,
                },
            )
        value = -imaginary_unit * erf_method()
        if isinstance(argument, flint.arb):
            value = value.real
        result = _certified_result("erfi", value, requested, bits, flint)
        return _with_error_function_diagnostics(
            result,
            _ARB_ERFI_FORMULA_SCOPE,
            domain,
            _ARB_ERFI_FORMULA_CERTIFICATION_CLAIM,
            formula=_ARB_ERFI_FORMULA,
            certificate_level=_ARB_ERFI_FORMULA_CERTIFICATE_LEVEL,
            audit_status=_ARB_ERFI_FORMULA_AUDIT_STATUS,
        )
    except Exception as exc:  # pragma: no cover - depends on optional backend domains
        return _unavailable(
            "erfi",
            requested,
            f"{_PHASE1_UNAVAILABLE} {exc}",
            diagnostics={"certificate_scope": _ARB_ERFI_FORMULA_SCOPE, "formula": _ARB_ERFI_FORMULA},
        )
    finally:
        flint.ctx.prec = old_prec


def arb_dawson(z, *, dps: int = 50):
    requested = ensure_dps(dps)
    try:
        flint, old_prec, bits = _enter_flint_context(requested)
    except ImportError as exc:
        return _unavailable(
            "dawson",
            requested,
            str(exc),
            diagnostics={"certificate_scope": _ARB_DAWSON_FORMULA_SCOPE},
        )
    try:
        argument = _make_ball(z)
        domain = "real" if isinstance(argument, flint.arb) else "complex"
        method = getattr(argument, "dawson", None) or getattr(argument, "dawsn", None)
        if method is not None:
            result = _certified_result("dawson", method(), requested, bits, flint)
            return _with_error_function_diagnostics(
                result,
                _DIRECT_ARB_DAWSON_SCOPE,
                domain,
                _DIRECT_ARB_DAWSON_CERTIFICATION_CLAIM,
            )

        erfi_value = _arb_erfi_value(argument, flint)
        coefficient = flint.arb.pi().sqrt() / 2
        value = coefficient * (-(argument * argument)).exp() * erfi_value
        result = _certified_result("dawson", value, requested, bits, flint)
        return _with_error_function_diagnostics(
            result,
            _ARB_DAWSON_FORMULA_SCOPE,
            domain,
            _ARB_DAWSON_FORMULA_CERTIFICATION_CLAIM,
            formula=_ARB_DAWSON_FORMULA,
            certificate_level=_ARB_DAWSON_FORMULA_CERTIFICATE_LEVEL,
            audit_status=_ARB_DAWSON_FORMULA_AUDIT_STATUS,
        )
    except Exception as exc:  # pragma: no cover - depends on optional backend domains
        return _unavailable(
            "dawson",
            requested,
            f"{_PHASE1_UNAVAILABLE} {exc}",
            diagnostics={"certificate_scope": _ARB_DAWSON_FORMULA_SCOPE, "formula": _ARB_DAWSON_FORMULA},
        )
    finally:
        flint.ctx.prec = old_prec


def arb_erfinv(x, *, dps: int = 50):
    requested = ensure_dps(dps)
    x_text, domain_error = _erfinv_real_input_text(x)
    if domain_error is not None:
        return _unavailable(
            "erfinv",
            requested,
            domain_error,
            diagnostics=_erfinv_domain_diagnostics(),
        )

    try:
        flint, old_prec, bits = _enter_flint_context(requested)
    except ImportError as exc:
        return _unavailable(
            "erfinv",
            requested,
            str(exc),
            diagnostics=_erfinv_domain_diagnostics(),
        )
    try:
        argument = flint.arb(x_text)
        method = _direct_arb_erfinv_method(argument)
        if method is not None:
            result = _certified_result("erfinv", method(), requested, bits, flint)
            return _with_erfinv_diagnostics(
                result,
                _DIRECT_ARB_ERFINV_SCOPE,
                _DIRECT_ARB_CERTIFICATE_LEVEL,
                _DIRECT_ARB_AUDIT_STATUS,
                _DIRECT_ARB_ERFINV_CERTIFICATION_CLAIM,
            )

        value, iterations = _arb_erfinv_real_root(argument, requested, bits, flint)
        result = _certified_result("erfinv", value, requested, bits, flint)
        return _with_erfinv_diagnostics(
            result,
            _ARB_ERFINV_REAL_ROOT_SCOPE,
            _ARB_ERFINV_REAL_ROOT_CERTIFICATE_LEVEL,
            _ARB_ERFINV_REAL_ROOT_AUDIT_STATUS,
            _ARB_ERFINV_REAL_ROOT_CERTIFICATION_CLAIM,
            iterations=iterations,
            formula="erf(y)-x=0",
        )
    except Exception as exc:  # pragma: no cover - depends on optional backend domains
        return _unavailable(
            "erfinv",
            requested,
            f"{_PHASE1_UNAVAILABLE} {exc}",
            diagnostics=_erfinv_domain_diagnostics(),
        )
    finally:
        flint.ctx.prec = old_prec


def arb_erfcinv(x, *, dps: int = 50):
    requested = ensure_dps(dps)
    x_text, domain_error = _erfcinv_real_input_text(x)
    if domain_error is not None:
        return _unavailable(
            "erfcinv",
            requested,
            domain_error,
            diagnostics=_erfcinv_domain_diagnostics(),
        )

    try:
        flint, old_prec, bits = _enter_flint_context(requested)
    except ImportError as exc:
        return _unavailable(
            "erfcinv",
            requested,
            str(exc),
            diagnostics=_erfcinv_domain_diagnostics(),
        )
    try:
        argument = flint.arb(x_text)
        method = _direct_arb_erfcinv_method(argument)
        if method is not None:
            result = _certified_result("erfcinv", method(), requested, bits, flint)
            return _with_erfcinv_diagnostics(
                result,
                _DIRECT_ARB_ERFCINV_SCOPE,
                _DIRECT_ARB_CERTIFICATE_LEVEL,
                _DIRECT_ARB_AUDIT_STATUS,
                _DIRECT_ARB_ERFCINV_CERTIFICATION_CLAIM,
            )

        target = flint.arb(1) - argument
        value, iterations = _arb_erfinv_real_root(target, requested, bits, flint)
        result = _certified_result("erfcinv", value, requested, bits, flint)
        return _with_erfcinv_diagnostics(
            result,
            _ARB_ERFCINV_VIA_ERFINV_SCOPE,
            _ARB_ERFINV_REAL_ROOT_CERTIFICATE_LEVEL,
            _ARB_ERFINV_REAL_ROOT_AUDIT_STATUS,
            _ARB_ERFCINV_VIA_ERFINV_CERTIFICATION_CLAIM,
            iterations=iterations,
            formula="erfinv(1-x)",
        )
    except Exception as exc:  # pragma: no cover - depends on optional backend domains
        return _unavailable(
            "erfcinv",
            requested,
            f"{_PHASE1_UNAVAILABLE} {exc}",
            diagnostics=_erfcinv_domain_diagnostics(),
        )
    finally:
        flint.ctx.prec = old_prec


def arb_beta(a, b, *, dps: int = 50):
    requested = ensure_dps(dps)
    a_pole = _is_gamma_pole(a)
    b_pole = _is_gamma_pole(b)
    sum_pole = _is_gamma_sum_pole(a, b)
    pole_diagnostics = {
        "a_pole": a_pole,
        "b_pole": b_pole,
        "sum_pole": sum_pole,
        "certificate_scope": _DIRECT_ARB_BETA_SCOPE,
    }
    if a_pole or b_pole:
        pole_case = _beta_failure_pole_case(a_pole, b_pole, sum_pole)
        return _unavailable(
            "beta",
            requested,
            "beta is undefined for certification when Gamma(a) or Gamma(b) has a pole; "
            "simultaneous singularities are not certified.",
            diagnostics={"pole_case": pole_case, **pole_diagnostics},
        )

    try:
        flint, old_prec, bits = _enter_flint_context(requested)
    except ImportError as exc:
        return _unavailable("beta", requested, str(exc), diagnostics={"pole_case": "unavailable", **pole_diagnostics})
    try:
        aa = _make_ball(a)
        bb = _make_ball(b)
        value = aa.gamma() * bb.gamma() * (aa + bb).rgamma()
        result = _certified_result("beta", value, requested, bits, flint)
        if result.certified:
            diagnostics = dict(result.diagnostics)
            diagnostics.update(
                {
                    "certificate_scope": _DIRECT_ARB_BETA_SCOPE,
                    "certification_claim": _DIRECT_ARB_BETA_CERTIFICATION_CLAIM,
                    "pole_case": "sum_pole_zero" if sum_pole else "regular",
                    **pole_diagnostics,
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
        diagnostics = dict(result.diagnostics)
        diagnostics.update(
            {
                "pole_case": "sum_pole_zero" if sum_pole else "regular",
                **pole_diagnostics,
            }
        )
        return make_result(
            function=result.function,
            value=result.value,
            abs_error_bound=result.abs_error_bound,
            rel_error_bound=result.rel_error_bound,
            certified=False,
            method=result.method,
            backend=result.backend,
            requested_dps=result.requested_dps,
            working_dps=result.working_dps,
            terms_used=result.terms_used,
            diagnostics=diagnostics,
        )
    except Exception as exc:  # pragma: no cover - depends on optional backend domains
        return _unavailable("beta", requested, f"{_PHASE1_UNAVAILABLE} {exc}", diagnostics=pole_diagnostics)
    finally:
        flint.ctx.prec = old_prec


def arb_pochhammer(a, n, *, dps: int = 50):
    requested = ensure_dps(dps)
    n_int, error = _nonnegative_integer_n(n)
    if error is not None:
        return _unavailable(
            "pochhammer",
            requested,
            error,
            diagnostics={"certificate_scope": _DIRECT_ARB_POCHHAMMER_SCOPE},
        )
    if n_int > _ARB_POCHHAMMER_MAX_PRODUCT_TERMS:
        return _unavailable(
            "pochhammer",
            requested,
            (
                "certified pochhammer currently uses the finite product path and "
                f"supports n <= {_ARB_POCHHAMMER_MAX_PRODUCT_TERMS}"
            ),
            diagnostics={
                "certificate_scope": _DIRECT_ARB_POCHHAMMER_SCOPE,
                "n": n_int,
                "max_product_terms": _ARB_POCHHAMMER_MAX_PRODUCT_TERMS,
            },
        )
    pole_case = _pochhammer_pole_case(a, n_int) if n_int > 0 else "regular"
    if pole_case == "simultaneous_poles_not_certified":
        return _unavailable(
            "pochhammer",
            requested,
            "pochhammer certified mode does not certify simultaneous-pole limiting values.",
            diagnostics={
                "certificate_scope": _DIRECT_ARB_POCHHAMMER_SCOPE,
                "n": n_int,
                "pole_case": pole_case,
                "a_pole": True,
                "shifted_pole": True,
            },
        )

    try:
        flint, old_prec, bits = _enter_flint_context(requested)
    except ImportError as exc:
        return _unavailable(
            "pochhammer",
            requested,
            str(exc),
            diagnostics={"certificate_scope": _DIRECT_ARB_POCHHAMMER_SCOPE},
        )
    try:
        if n_int == 0:
            return _certified_pochhammer_result(flint.arb(1), requested, bits, flint, n_int, terms_used=0)

        aa = _make_ball(a)
        value = flint.acb(1) if isinstance(aa, flint.acb) else flint.arb(1)
        for k in range(n_int):
            factor = aa + k
            if factor.is_zero():
                zero = flint.acb(0) if isinstance(factor, flint.acb) else flint.arb(0)
                return _certified_pochhammer_result(
                    zero,
                    requested,
                    bits,
                    flint,
                    n_int,
                    terms_used=k + 1,
                    diagnostics={"pole_case": "zero_factor", "zero_factor_index": k},
                )
            value *= factor

        return _certified_pochhammer_result(
            value,
            requested,
            bits,
            flint,
            n_int,
            terms_used=n_int,
            diagnostics={"pole_case": pole_case},
        )
    except Exception as exc:  # pragma: no cover - depends on optional backend domains
        return _unavailable(
            "pochhammer",
            requested,
            f"{_PHASE1_UNAVAILABLE} {exc}",
            diagnostics={"certificate_scope": _DIRECT_ARB_POCHHAMMER_SCOPE},
        )
    finally:
        flint.ctx.prec = old_prec


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
                "certificate_level": _DIRECT_ARB_CERTIFICATE_LEVEL,
                "audit_status": _DIRECT_ARB_AUDIT_STATUS,
                "certification_claim": _DIRECT_ARB_CERTIFICATION_CLAIM,
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


def _arb_error_function(function: str, z, *, dps: int):
    requested = ensure_dps(dps)
    scope = _DIRECT_ARB_ERF_SCOPE if function == "erf" else _DIRECT_ARB_ERFC_SCOPE
    try:
        flint, old_prec, bits = _enter_flint_context(requested)
    except ImportError as exc:
        return _unavailable(function, requested, str(exc), diagnostics={"certificate_scope": scope})
    try:
        argument = _make_ball(z)
        domain = "real" if isinstance(argument, flint.arb) else "complex"
        formula = None
        if function == "erf":
            method = getattr(argument, "erf", None)
            claim = _DIRECT_ARB_ERF_CERTIFICATION_CLAIM
        else:
            method = getattr(argument, "erfc", None)
            claim = _DIRECT_ARB_ERFC_CERTIFICATION_CLAIM
            if method is None:
                erf_method = getattr(argument, "erf", None)
                if erf_method is None:
                    return _unavailable(
                        function,
                        requested,
                        "python-flint does not expose an Arb erf or erfc primitive for this value.",
                        diagnostics={"certificate_scope": scope, "domain": domain},
                    )
                one = flint.acb(1) if isinstance(argument, flint.acb) else flint.arb(1)
                value = one - erf_method()
                formula = "1-erf"
                claim = _DIRECT_ARB_ERFC_FALLBACK_CERTIFICATION_CLAIM
                result = _certified_result(function, value, requested, bits, flint)
                return _with_error_function_diagnostics(result, scope, domain, claim, formula=formula)
        if method is None:
            return _unavailable(
                function,
                requested,
                f"python-flint does not expose an Arb {function} primitive for this value.",
                diagnostics={"certificate_scope": scope, "domain": domain},
            )
        result = _certified_result(function, method(), requested, bits, flint)
        return _with_error_function_diagnostics(result, scope, domain, claim, formula=formula)
    except Exception as exc:  # pragma: no cover - depends on optional backend domains
        return _unavailable(function, requested, f"{_PHASE1_UNAVAILABLE} {exc}", diagnostics={"certificate_scope": scope})
    finally:
        flint.ctx.prec = old_prec


def _arb_erfi_value(argument, flint):
    method = getattr(argument, "erfi", None)
    if method is not None:
        return method()

    erf_argument = flint.acb(argument) if isinstance(argument, flint.arb) else argument
    imaginary_unit = flint.acb(0, 1)
    erf_method = getattr(imaginary_unit * erf_argument, "erf", None)
    if erf_method is None:
        raise ValueError("python-flint does not expose an Arb erfi or erf primitive for this value.")
    value = -imaginary_unit * erf_method()
    if isinstance(argument, flint.arb):
        return value.real
    return value


def _direct_arb_erfinv_method(argument):
    return getattr(argument, "erfinv", None)


def _direct_arb_erfcinv_method(argument):
    return getattr(argument, "erfcinv", None)


def _erfinv_real_input_text(value: Any) -> tuple[str | None, str | None]:
    if isinstance(value, complex):
        return None, "certified erfinv supports real x only; complex inverse branches are not certified in this PR."
    try:
        if isinstance(value, str):
            text = value.strip()
            lowered = text.lower()
            if "j" in lowered or lowered.endswith("i"):
                return (
                    None,
                    "certified erfinv supports real x only; complex inverse branches are not certified in this PR.",
                )
            value = text
        decimal = Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None, "certified erfinv requires a finite real x with -1 < x < 1."

    if not decimal.is_finite():
        return None, "certified erfinv requires a finite real x with -1 < x < 1."
    if decimal <= Decimal(-1) or decimal >= Decimal(1):
        return None, "certified erfinv supports real x only with -1 < x < 1."
    return format(decimal, "f"), None


def _erfcinv_real_input_text(value: Any) -> tuple[str | None, str | None]:
    if isinstance(value, complex):
        return None, "certified erfcinv supports real x only; complex inverse branches are not certified in this PR."
    try:
        if isinstance(value, str):
            text = value.strip()
            lowered = text.lower()
            if "j" in lowered or lowered.endswith("i"):
                return (
                    None,
                    "certified erfcinv supports real x only; complex inverse branches are not certified in this PR.",
                )
            value = text
        decimal = Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None, "certified erfcinv requires a finite real x with 0 < x < 2."

    if not decimal.is_finite():
        return None, "certified erfcinv requires a finite real x with 0 < x < 2."
    if decimal <= Decimal(0) or decimal >= Decimal(2):
        return None, "certified erfcinv supports real x only with 0 < x < 2."
    return format(decimal, "f"), None


def _arb_erfinv_real_root(target, requested_dps: int, bits: int, flint):
    if target == flint.arb(0):
        return flint.arb(0), 0

    left, right = _arb_erfinv_bracket(target, flint)
    target_radius = flint.arb(f"1e-{requested_dps}")
    max_iterations = max(bits + 64, 128)
    for iterations in range(1, max_iterations + 1):
        center = (left + right) / 2
        radius = (right - left) / 2
        if radius < target_radius:
            return flint.arb(center, radius), iterations

        residual = _arb_erfinv_residual(center, target)
        if _arb_sign_negative(residual):
            left = center
        elif _arb_sign_positive(residual):
            right = center
        else:
            raise ValueError("unable to certify erfinv bisection sign at current Arb precision")

    raise ValueError("certified erfinv real-root refinement did not reach the requested precision")


def _arb_erfinv_bracket(target, flint):
    left = flint.arb(-1)
    right = flint.arb(1)

    expansions = 0
    while not _arb_sign_negative(_arb_erfinv_residual(left, target)):
        expansions += 1
        if expansions > 128:
            raise ValueError("unable to bracket the erfinv real root on the left")
        left *= 2

    expansions = 0
    while not _arb_sign_positive(_arb_erfinv_residual(right, target)):
        expansions += 1
        if expansions > 128:
            raise ValueError("unable to bracket the erfinv real root on the right")
        right *= 2

    return left, right


def _arb_erfinv_residual(y, target):
    return y.erf() - target


def _arb_sign_negative(value) -> bool:
    return bool(value < 0)


def _arb_sign_positive(value) -> bool:
    return bool(value > 0)


def _erfinv_domain_diagnostics():
    return {
        "certificate_scope": _ARB_ERFINV_REAL_ROOT_SCOPE,
        "domain": _ARB_ERFINV_REAL_DOMAIN,
        "branch": "real_principal_inverse",
    }


def _erfcinv_domain_diagnostics():
    return {
        "certificate_scope": _ARB_ERFCINV_VIA_ERFINV_SCOPE,
        "domain": _ARB_ERFCINV_REAL_DOMAIN,
        "branch": "real_principal_inverse",
    }


def _with_erfinv_diagnostics(
    result,
    scope: str,
    certificate_level: str,
    audit_status: str,
    claim: str,
    *,
    iterations: int | None = None,
    formula: str | None = None,
):
    diagnostics = dict(result.diagnostics)
    diagnostics.update(
        {
            "domain": _ARB_ERFINV_REAL_DOMAIN,
            "branch": "real_principal_inverse",
            "certificate_scope": scope,
        }
    )
    if result.certified:
        diagnostics.update(
            {
                "certificate_level": certificate_level,
                "audit_status": audit_status,
                "certification_claim": claim,
            }
        )
    if iterations is not None:
        diagnostics["iterations"] = iterations
    if formula is not None:
        diagnostics["formula"] = formula
    return make_result(
        function=result.function,
        value=result.value,
        abs_error_bound=result.abs_error_bound,
        rel_error_bound=result.rel_error_bound,
        certified=result.certified,
        method=result.method,
        backend=result.backend,
        requested_dps=result.requested_dps,
        working_dps=result.working_dps,
        terms_used=result.terms_used,
        diagnostics=diagnostics,
    )


def _with_erfcinv_diagnostics(
    result,
    scope: str,
    certificate_level: str,
    audit_status: str,
    claim: str,
    *,
    iterations: int | None = None,
    formula: str | None = None,
):
    diagnostics = dict(result.diagnostics)
    diagnostics.update(
        {
            "domain": _ARB_ERFCINV_REAL_DOMAIN,
            "branch": "real_principal_inverse",
            "certificate_scope": scope,
        }
    )
    if result.certified:
        diagnostics.update(
            {
                "certificate_level": certificate_level,
                "audit_status": audit_status,
                "certification_claim": claim,
            }
        )
    if iterations is not None:
        diagnostics["iterations"] = iterations
    if formula is not None:
        diagnostics["formula"] = formula
    return make_result(
        function=result.function,
        value=result.value,
        abs_error_bound=result.abs_error_bound,
        rel_error_bound=result.rel_error_bound,
        certified=result.certified,
        method=result.method,
        backend=result.backend,
        requested_dps=result.requested_dps,
        working_dps=result.working_dps,
        terms_used=result.terms_used,
        diagnostics=diagnostics,
    )


def _with_error_function_diagnostics(
    result,
    scope: str,
    domain: str,
    claim: str,
    *,
    formula: str | None = None,
    certificate_level: str = _DIRECT_ARB_CERTIFICATE_LEVEL,
    audit_status: str = _DIRECT_ARB_AUDIT_STATUS,
):
    diagnostics = dict(result.diagnostics)
    diagnostics.update({"domain": domain, "certificate_scope": scope})
    if result.certified:
        diagnostics.update(
            {
                "certificate_level": certificate_level,
                "audit_status": audit_status,
                "certification_claim": claim,
            }
        )
    if formula is not None:
        diagnostics["formula"] = formula
    return make_result(
        function=result.function,
        value=result.value,
        abs_error_bound=result.abs_error_bound,
        rel_error_bound=result.rel_error_bound,
        certified=result.certified,
        method=result.method,
        backend=result.backend,
        requested_dps=result.requested_dps,
        working_dps=result.working_dps,
        terms_used=result.terms_used,
        diagnostics=diagnostics,
    )


def _certified_pochhammer_result(
    value,
    requested_dps: int,
    bits: int,
    flint,
    n_int: int,
    *,
    terms_used: int,
    diagnostics=None,
):
    if not _is_finite_ball(value, flint):
        return _unavailable("pochhammer", requested_dps, _NONFINITE_RESULT)
    result_diagnostics = {
        "mode": "certified",
        "working_precision_bits": bits,
        "certificate_scope": _DIRECT_ARB_POCHHAMMER_SCOPE,
        "certificate_level": _DIRECT_ARB_FINITE_PRODUCT_CERTIFICATE_LEVEL,
        "audit_status": _DIRECT_ARB_AUDIT_STATUS,
        "certification_claim": _DIRECT_ARB_POCHHAMMER_CERTIFICATION_CLAIM,
        "formula": "finite_product",
        "n": n_int,
        "n_domain": "nonnegative_integer",
        "max_product_terms": _ARB_POCHHAMMER_MAX_PRODUCT_TERMS,
    }
    if diagnostics is not None:
        result_diagnostics.update(diagnostics)
    return make_result(
        function="pochhammer",
        value=_ball_value_string(value, flint),
        abs_error_bound=_ball_abs_error_string(value),
        rel_error_bound=_ball_rel_error_string(value),
        certified=True,
        method="arb_ball",
        backend="python-flint",
        requested_dps=requested_dps,
        working_dps=_bits_to_dps(bits),
        terms_used=terms_used,
        diagnostics=result_diagnostics,
    )


def _nonnegative_integer_n(value: Any) -> tuple[int, str | None]:
    text = _real_order_text(value)
    if text is None:
        return 0, "certified pochhammer requires integer n; analytic continuation in n is not certified."
    decimal = Decimal(text)
    if decimal != decimal.to_integral_value():
        return 0, "certified pochhammer requires integer n; analytic continuation in n is not certified."
    if decimal < 0:
        return 0, "certified pochhammer currently supports n >= 0 only."
    return int(decimal), None


def _pochhammer_pole_case(a: Any, n_int: int) -> str:
    a_text = _real_order_text(a)
    if a_text is None:
        return "regular"
    decimal = Decimal(a_text)
    a_pole = decimal <= 0 and decimal == decimal.to_integral_value()
    shifted = decimal + Decimal(n_int)
    shifted_pole = shifted <= 0 and shifted == shifted.to_integral_value()
    if a_pole and shifted_pole:
        return "simultaneous_poles_not_certified"
    return "regular"


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
        "certificate_level": _FORMULA_CERTIFICATE_LEVEL,
        "audit_status": _FORMULA_AUDIT_STATUS,
        "certification_claim": _FORMULA_CERTIFICATION_CLAIM,
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
            "certificate_level": _DIRECT_ARB_CERTIFICATE_LEVEL,
            "audit_status": _DIRECT_ARB_AUDIT_STATUS,
            "certification_claim": _DIRECT_ARB_CERTIFICATION_CLAIM,
        },
    )


def _unavailable(function: str, requested_dps: int, message: str, diagnostics=None):
    result_diagnostics = {"error": message, "mode": "certified"}
    if diagnostics is not None:
        result_diagnostics.update(diagnostics)
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
        diagnostics=result_diagnostics,
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


def _is_gamma_pole(value: Any) -> bool:
    real_text = _real_order_text(value)
    if real_text is None:
        return False
    decimal = Decimal(real_text)
    return decimal <= 0 and decimal == decimal.to_integral_value()


def _is_gamma_sum_pole(a: Any, b: Any) -> bool:
    a_text = _real_order_text(a)
    b_text = _real_order_text(b)
    if a_text is None or b_text is None:
        return False
    total = Decimal(a_text) + Decimal(b_text)
    return total <= 0 and total == total.to_integral_value()


def _beta_failure_pole_case(a_pole: bool, b_pole: bool, sum_pole: bool) -> str:
    pole_names = []
    if a_pole:
        pole_names.append("a")
    if b_pole:
        pole_names.append("b")
    if sum_pole:
        pole_names.append("sum")
    return "_".join(pole_names) + "_poles" if len(pole_names) > 1 else pole_names[0] + "_pole"


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
