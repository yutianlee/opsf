"""Mode dispatcher for special-function wrappers."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from certsf.result import SFResult

from .backends import arb_backend, mpmath_backend, scipy_backend
from .methods import certified_auto_loggamma, gamma_stirling_exp, stirling_loggamma, stirling_loggamma_shifted

Mode = str


@dataclass(frozen=True)
class MethodSpec:
    """Auditable method selection record for one function/mode pair."""

    function: str
    mode: Mode
    method_id: str
    priority: int
    backend: str
    callable: Callable[..., SFResult]
    certified: bool
    domain: str
    certificate_scope: str | None = None
    certificate_level: str | None = None
    audit_status: str | None = None
    applicability_note: str | None = None


_MODE_ORDER: tuple[Mode, ...] = ("auto", "fast", "high_precision", "certified")
_CONCRETE_MODES: tuple[Mode, ...] = ("fast", "high_precision", "certified")
_FUNCTION_ORDER = (
    "gamma",
    "loggamma",
    "rgamma",
    "gamma_ratio",
    "loggamma_ratio",
    "beta",
    "pochhammer",
    "erf",
    "erfc",
    "erfcx",
    "erfi",
    "dawson",
    "erfinv",
    "erfcinv",
    "airy",
    "ai",
    "bi",
    "besselj",
    "bessely",
    "besseli",
    "besselk",
    "pcfd",
    "pcfu",
    "pcfv",
    "pcfw",
    "pbdv",
)

_FAST_DOMAIN = "SciPy-supported double-precision inputs"
_HIGH_PRECISION_DOMAIN = "mpmath-supported high-precision inputs"


def _default_method_id(mode: Mode) -> str:
    if mode == "fast":
        return "scipy"
    if mode == "high_precision":
        return "mpmath"
    if mode == "certified":
        return "arb"
    raise ValueError(f"no default method id for mode {mode!r}")


def _certificate_metadata(certificate_scope: str) -> tuple[str, str]:
    levels: list[str] = []
    audit_statuses: list[str] = []
    for scope in certificate_scope.split("|"):
        level, audit_status = _certificate_metadata_for_scope(scope)
        if level not in levels:
            levels.append(level)
        if audit_status not in audit_statuses:
            audit_statuses.append(audit_status)
    return "|".join(levels), "|".join(audit_statuses)


def _certificate_metadata_for_scope(certificate_scope: str) -> tuple[str, str]:
    if certificate_scope == "direct_arb_pochhammer_product":
        return "direct_arb_finite_product", "audited_direct"
    if certificate_scope in {"arb_erfcx_formula", "arb_erfi_formula", "arb_dawson_formula"}:
        return "formula_audited_alpha", "formula_identity"
    if certificate_scope in {"arb_erfinv_real_root", "arb_erfcinv_via_erfinv"}:
        return "certified_real_root", "monotone_real_inverse"
    if certificate_scope in {"phase7_hypergeometric_parabolic_cylinder", "phase8_parabolic_cylinder_connections"}:
        return "formula_audited_experimental", "experimental_formula"
    if certificate_scope in {"stirling_loggamma_positive_real", "gamma_positive_real_stirling_exp"}:
        return "custom_asymptotic_bound", "theorem_documented"
    return "direct_arb_primitive", "audited_direct"


def _spec(
    function: str,
    mode: Mode,
    backend: str,
    method: Callable[..., SFResult],
    *,
    certified: bool,
    domain: str,
    certificate_scope: str | None = None,
    method_id: str | None = None,
    priority: int = 100,
    certificate_level: str | None = None,
    audit_status: str | None = None,
    applicability_note: str | None = None,
) -> MethodSpec:
    if certificate_scope is not None:
        inferred_certificate_level, inferred_audit_status = _certificate_metadata(certificate_scope)
        certificate_level = inferred_certificate_level if certificate_level is None else certificate_level
        audit_status = inferred_audit_status if audit_status is None else audit_status
    return MethodSpec(
        function=function,
        mode=mode,
        method_id=_default_method_id(mode) if method_id is None else method_id,
        priority=priority,
        backend=backend,
        callable=method,
        certified=certified,
        domain=domain,
        certificate_scope=certificate_scope,
        certificate_level=certificate_level,
        audit_status=audit_status,
        applicability_note=domain if applicability_note is None else applicability_note,
    )


REGISTRY: dict[str, dict[Mode, MethodSpec]] = {
    "gamma": {
        "fast": _spec("gamma", "fast", "scipy", scipy_backend.scipy_gamma, certified=False, domain=_FAST_DOMAIN),
        "high_precision": _spec(
            "gamma",
            "high_precision",
            "mpmath",
            mpmath_backend.mpmath_gamma,
            certified=False,
            domain=_HIGH_PRECISION_DOMAIN,
        ),
        "certified": _spec(
            "gamma",
            "certified",
            "python-flint",
            arb_backend.arb_gamma,
            certified=True,
            domain="Arb real or complex inputs with finite gamma target",
            certificate_scope="direct_arb_primitive",
        ),
    },
    "loggamma": {
        "fast": _spec("loggamma", "fast", "scipy", scipy_backend.scipy_loggamma, certified=False, domain=_FAST_DOMAIN),
        "high_precision": _spec(
            "loggamma",
            "high_precision",
            "mpmath",
            mpmath_backend.mpmath_loggamma,
            certified=False,
            domain=_HIGH_PRECISION_DOMAIN,
        ),
        "certified": _spec(
            "loggamma",
            "certified",
            "python-flint",
            arb_backend.arb_loggamma,
            certified=True,
            domain="Arb real or complex inputs with finite principal loggamma target",
            certificate_scope="direct_arb_primitive",
        ),
    },
    "rgamma": {
        "fast": _spec("rgamma", "fast", "scipy", scipy_backend.scipy_rgamma, certified=False, domain=_FAST_DOMAIN),
        "high_precision": _spec(
            "rgamma",
            "high_precision",
            "mpmath",
            mpmath_backend.mpmath_rgamma,
            certified=False,
            domain=_HIGH_PRECISION_DOMAIN,
        ),
        "certified": _spec(
            "rgamma",
            "certified",
            "python-flint",
            arb_backend.arb_rgamma,
            certified=True,
            domain="Arb real or complex inputs, including exact reciprocal-gamma zeros at poles",
            certificate_scope="direct_arb_primitive",
        ),
    },
    "gamma_ratio": {
        "fast": _spec(
            "gamma_ratio",
            "fast",
            "scipy",
            scipy_backend.scipy_gamma_ratio,
            certified=False,
            domain=_FAST_DOMAIN,
        ),
        "high_precision": _spec(
            "gamma_ratio",
            "high_precision",
            "mpmath",
            mpmath_backend.mpmath_gamma_ratio,
            certified=False,
            domain=_HIGH_PRECISION_DOMAIN,
        ),
        "certified": _spec(
            "gamma_ratio",
            "certified",
            "python-flint",
            arb_backend.arb_gamma_ratio,
            certified=True,
            domain="Arb real or complex inputs with finite Gamma(a) target; denominator poles certify to zero",
            certificate_scope="direct_arb_gamma_ratio",
        ),
    },
    "loggamma_ratio": {
        "fast": _spec(
            "loggamma_ratio",
            "fast",
            "scipy",
            scipy_backend.scipy_loggamma_ratio,
            certified=False,
            domain=_FAST_DOMAIN,
        ),
        "high_precision": _spec(
            "loggamma_ratio",
            "high_precision",
            "mpmath",
            mpmath_backend.mpmath_loggamma_ratio,
            certified=False,
            domain=_HIGH_PRECISION_DOMAIN,
        ),
        "certified": _spec(
            "loggamma_ratio",
            "certified",
            "python-flint",
            arb_backend.arb_loggamma_ratio,
            certified=True,
            domain="Arb real or complex inputs with finite principal loggamma(a) and loggamma(b) targets",
            certificate_scope="direct_arb_loggamma_ratio",
        ),
    },
    "beta": {
        "fast": _spec("beta", "fast", "scipy", scipy_backend.scipy_beta, certified=False, domain=_FAST_DOMAIN),
        "high_precision": _spec(
            "beta",
            "high_precision",
            "mpmath",
            mpmath_backend.mpmath_beta,
            certified=False,
            domain=_HIGH_PRECISION_DOMAIN,
        ),
        "certified": _spec(
            "beta",
            "certified",
            "python-flint",
            arb_backend.arb_beta,
            certified=True,
            domain=(
                "Arb real or complex inputs with finite Gamma(a) and Gamma(b); "
                "Gamma(a+b) poles certify to zero"
            ),
            certificate_scope="direct_arb_beta",
        ),
    },
    "pochhammer": {
        "fast": _spec(
            "pochhammer",
            "fast",
            "scipy",
            scipy_backend.scipy_pochhammer,
            certified=False,
            domain="SciPy-supported double-precision inputs; finite-product fallback for complex integer-n cases",
        ),
        "high_precision": _spec(
            "pochhammer",
            "high_precision",
            "mpmath",
            mpmath_backend.mpmath_pochhammer,
            certified=False,
            domain=_HIGH_PRECISION_DOMAIN,
        ),
        "certified": _spec(
            "pochhammer",
            "certified",
            "python-flint",
            arb_backend.arb_pochhammer,
            certified=True,
            domain="Arb real or complex a with integer n >= 0; finite-product path only",
            certificate_scope="direct_arb_pochhammer_product",
        ),
    },
    "erf": {
        "fast": _spec("erf", "fast", "scipy", scipy_backend.scipy_erf, certified=False, domain=_FAST_DOMAIN),
        "high_precision": _spec(
            "erf",
            "high_precision",
            "mpmath",
            mpmath_backend.mpmath_erf,
            certified=False,
            domain=_HIGH_PRECISION_DOMAIN,
        ),
        "certified": _spec(
            "erf",
            "certified",
            "python-flint",
            arb_backend.arb_erf,
            certified=True,
            domain="Arb real or complex inputs with finite erf target",
            certificate_scope="direct_arb_erf",
        ),
    },
    "erfc": {
        "fast": _spec("erfc", "fast", "scipy", scipy_backend.scipy_erfc, certified=False, domain=_FAST_DOMAIN),
        "high_precision": _spec(
            "erfc",
            "high_precision",
            "mpmath",
            mpmath_backend.mpmath_erfc,
            certified=False,
            domain=_HIGH_PRECISION_DOMAIN,
        ),
        "certified": _spec(
            "erfc",
            "certified",
            "python-flint",
            arb_backend.arb_erfc,
            certified=True,
            domain="Arb real or complex inputs with finite erfc target",
            certificate_scope="direct_arb_erfc",
        ),
    },
    "erfcx": {
        "fast": _spec("erfcx", "fast", "scipy", scipy_backend.scipy_erfcx, certified=False, domain=_FAST_DOMAIN),
        "high_precision": _spec(
            "erfcx",
            "high_precision",
            "mpmath",
            mpmath_backend.mpmath_erfcx,
            certified=False,
            domain=_HIGH_PRECISION_DOMAIN,
        ),
        "certified": _spec(
            "erfcx",
            "certified",
            "python-flint",
            arb_backend.arb_erfcx,
            certified=True,
            domain="Arb real or complex inputs with finite scaled complementary error-function target",
            certificate_scope="direct_arb_erfcx|arb_erfcx_formula",
        ),
    },
    "erfi": {
        "fast": _spec("erfi", "fast", "scipy", scipy_backend.scipy_erfi, certified=False, domain=_FAST_DOMAIN),
        "high_precision": _spec(
            "erfi",
            "high_precision",
            "mpmath",
            mpmath_backend.mpmath_erfi,
            certified=False,
            domain=_HIGH_PRECISION_DOMAIN,
        ),
        "certified": _spec(
            "erfi",
            "certified",
            "python-flint",
            arb_backend.arb_erfi,
            certified=True,
            domain="Arb real or complex inputs with finite imaginary error-function target",
            certificate_scope="direct_arb_erfi|arb_erfi_formula",
        ),
    },
    "dawson": {
        "fast": _spec("dawson", "fast", "scipy", scipy_backend.scipy_dawson, certified=False, domain=_FAST_DOMAIN),
        "high_precision": _spec(
            "dawson",
            "high_precision",
            "mpmath",
            mpmath_backend.mpmath_dawson,
            certified=False,
            domain=_HIGH_PRECISION_DOMAIN,
        ),
        "certified": _spec(
            "dawson",
            "certified",
            "python-flint",
            arb_backend.arb_dawson,
            certified=True,
            domain="Arb real or complex inputs with finite Dawson target",
            certificate_scope="direct_arb_dawson|arb_dawson_formula",
        ),
    },
    "erfinv": {
        "fast": _spec(
            "erfinv",
            "fast",
            "scipy",
            scipy_backend.scipy_erfinv,
            certified=False,
            domain="SciPy-supported real double-precision inputs for erfinv",
        ),
        "high_precision": _spec(
            "erfinv",
            "high_precision",
            "mpmath",
            mpmath_backend.mpmath_erfinv,
            certified=False,
            domain="mpmath-supported real principal inverse error-function inputs",
        ),
        "certified": _spec(
            "erfinv",
            "certified",
            "python-flint",
            arb_backend.arb_erfinv,
            certified=True,
            domain="Real x with -1 < x < 1; principal real inverse branch only",
            certificate_scope="direct_arb_erfinv|arb_erfinv_real_root",
        ),
    },
    "erfcinv": {
        "fast": _spec(
            "erfcinv",
            "fast",
            "scipy",
            scipy_backend.scipy_erfcinv,
            certified=False,
            domain="SciPy-supported real double-precision inputs for erfcinv",
        ),
        "high_precision": _spec(
            "erfcinv",
            "high_precision",
            "mpmath",
            mpmath_backend.mpmath_erfcinv,
            certified=False,
            domain="mpmath-supported real principal inverse complementary error-function inputs",
        ),
        "certified": _spec(
            "erfcinv",
            "certified",
            "python-flint",
            arb_backend.arb_erfcinv,
            certified=True,
            domain="Real x with 0 < x < 2; principal real inverse branch only",
            certificate_scope="direct_arb_erfcinv|arb_erfcinv_via_erfinv",
        ),
    },
    "airy": {
        "fast": _spec("airy", "fast", "scipy", scipy_backend.scipy_airy, certified=False, domain=_FAST_DOMAIN),
        "high_precision": _spec(
            "airy",
            "high_precision",
            "mpmath",
            mpmath_backend.mpmath_airy,
            certified=False,
            domain=_HIGH_PRECISION_DOMAIN,
        ),
        "certified": _spec(
            "airy",
            "certified",
            "python-flint",
            arb_backend.arb_airy,
            certified=True,
            domain="Arb real or complex Airy inputs",
            certificate_scope="phase3_real_airy|arb_complex_airy",
        ),
    },
    "ai": {
        "fast": _spec("ai", "fast", "scipy", scipy_backend.scipy_ai, certified=False, domain=_FAST_DOMAIN),
        "high_precision": _spec(
            "ai",
            "high_precision",
            "mpmath",
            mpmath_backend.mpmath_ai,
            certified=False,
            domain=_HIGH_PRECISION_DOMAIN,
        ),
        "certified": _spec(
            "ai",
            "certified",
            "python-flint",
            arb_backend.arb_ai,
            certified=True,
            domain="Arb real or complex Airy Ai inputs, derivative 0 or 1",
            certificate_scope="phase3_real_airy|arb_complex_airy",
        ),
    },
    "bi": {
        "fast": _spec("bi", "fast", "scipy", scipy_backend.scipy_bi, certified=False, domain=_FAST_DOMAIN),
        "high_precision": _spec(
            "bi",
            "high_precision",
            "mpmath",
            mpmath_backend.mpmath_bi,
            certified=False,
            domain=_HIGH_PRECISION_DOMAIN,
        ),
        "certified": _spec(
            "bi",
            "certified",
            "python-flint",
            arb_backend.arb_bi,
            certified=True,
            domain="Arb real or complex Airy Bi inputs, derivative 0 or 1",
            certificate_scope="phase3_real_airy|arb_complex_airy",
        ),
    },
    "besselj": {
        "fast": _spec("besselj", "fast", "scipy", scipy_backend.scipy_besselj, certified=False, domain=_FAST_DOMAIN),
        "high_precision": _spec(
            "besselj",
            "high_precision",
            "mpmath",
            mpmath_backend.mpmath_besselj,
            certified=False,
            domain=_HIGH_PRECISION_DOMAIN,
        ),
        "certified": _spec(
            "besselj",
            "certified",
            "python-flint",
            arb_backend.arb_besselj,
            certified=True,
            domain="Arb real-valued order with real or complex argument",
            certificate_scope="phase4_integer_real_bessel|phase5_real_order_complex_bessel",
        ),
    },
    "bessely": {
        "fast": _spec("bessely", "fast", "scipy", scipy_backend.scipy_bessely, certified=False, domain=_FAST_DOMAIN),
        "high_precision": _spec(
            "bessely",
            "high_precision",
            "mpmath",
            mpmath_backend.mpmath_bessely,
            certified=False,
            domain=_HIGH_PRECISION_DOMAIN,
        ),
        "certified": _spec(
            "bessely",
            "certified",
            "python-flint",
            arb_backend.arb_bessely,
            certified=True,
            domain="Arb real-valued order with real or complex argument",
            certificate_scope="phase4_integer_real_bessel|phase5_real_order_complex_bessel",
        ),
    },
    "besseli": {
        "fast": _spec("besseli", "fast", "scipy", scipy_backend.scipy_besseli, certified=False, domain=_FAST_DOMAIN),
        "high_precision": _spec(
            "besseli",
            "high_precision",
            "mpmath",
            mpmath_backend.mpmath_besseli,
            certified=False,
            domain=_HIGH_PRECISION_DOMAIN,
        ),
        "certified": _spec(
            "besseli",
            "certified",
            "python-flint",
            arb_backend.arb_besseli,
            certified=True,
            domain="Arb real-valued order with real or complex argument",
            certificate_scope="phase4_integer_real_bessel|phase5_real_order_complex_bessel",
        ),
    },
    "besselk": {
        "fast": _spec("besselk", "fast", "scipy", scipy_backend.scipy_besselk, certified=False, domain=_FAST_DOMAIN),
        "high_precision": _spec(
            "besselk",
            "high_precision",
            "mpmath",
            mpmath_backend.mpmath_besselk,
            certified=False,
            domain=_HIGH_PRECISION_DOMAIN,
        ),
        "certified": _spec(
            "besselk",
            "certified",
            "python-flint",
            arb_backend.arb_besselk,
            certified=True,
            domain="Arb real-valued order with real or complex argument",
            certificate_scope="phase4_integer_real_bessel|phase5_real_order_complex_bessel",
        ),
    },
    "pcfd": {
        "fast": _spec("pcfd", "fast", "scipy", scipy_backend.scipy_pcfd, certified=False, domain=_FAST_DOMAIN),
        "high_precision": _spec(
            "pcfd",
            "high_precision",
            "mpmath",
            mpmath_backend.mpmath_pcfd,
            certified=False,
            domain=_HIGH_PRECISION_DOMAIN,
        ),
        "certified": _spec(
            "pcfd",
            "certified",
            "python-flint",
            arb_backend.arb_pcfd,
            certified=True,
            domain="Documented formula with real parameter and real or complex argument",
            certificate_scope="phase7_hypergeometric_parabolic_cylinder",
        ),
    },
    "pcfu": {
        "fast": _spec("pcfu", "fast", "scipy", scipy_backend.scipy_pcfu, certified=False, domain=_FAST_DOMAIN),
        "high_precision": _spec(
            "pcfu",
            "high_precision",
            "mpmath",
            mpmath_backend.mpmath_pcfu,
            certified=False,
            domain=_HIGH_PRECISION_DOMAIN,
        ),
        "certified": _spec(
            "pcfu",
            "certified",
            "python-flint",
            arb_backend.arb_pcfu,
            certified=True,
            domain="Documented formula with real parameter and real or complex argument",
            certificate_scope="phase7_hypergeometric_parabolic_cylinder",
        ),
    },
    "pcfv": {
        "fast": _spec("pcfv", "fast", "scipy", scipy_backend.scipy_pcfv, certified=False, domain=_FAST_DOMAIN),
        "high_precision": _spec(
            "pcfv",
            "high_precision",
            "mpmath",
            mpmath_backend.mpmath_pcfv,
            certified=False,
            domain=_HIGH_PRECISION_DOMAIN,
        ),
        "certified": _spec(
            "pcfv",
            "certified",
            "python-flint",
            arb_backend.arb_pcfv,
            certified=True,
            domain="Documented connection formula with real parameter and real or complex argument",
            certificate_scope="phase8_parabolic_cylinder_connections",
        ),
    },
    "pcfw": {
        "fast": _spec("pcfw", "fast", "scipy", scipy_backend.scipy_pcfw, certified=False, domain=_FAST_DOMAIN),
        "high_precision": _spec(
            "pcfw",
            "high_precision",
            "mpmath",
            mpmath_backend.mpmath_pcfw,
            certified=False,
            domain=_HIGH_PRECISION_DOMAIN,
        ),
        "certified": _spec(
            "pcfw",
            "certified",
            "python-flint",
            arb_backend.arb_pcfw,
            certified=True,
            domain="Documented real-variable W(a,x) connection formula",
            certificate_scope="phase8_parabolic_cylinder_connections",
        ),
    },
    "pbdv": {
        "fast": _spec("pbdv", "fast", "scipy", scipy_backend.scipy_pbdv, certified=False, domain=_FAST_DOMAIN),
        "high_precision": _spec(
            "pbdv",
            "high_precision",
            "mpmath",
            mpmath_backend.mpmath_pbdv,
            certified=False,
            domain=_HIGH_PRECISION_DOMAIN,
        ),
        "certified": _spec(
            "pbdv",
            "certified",
            "python-flint",
            arb_backend.arb_pbdv,
            certified=True,
            domain="Documented D_v value and derivative formula with real parameter",
            certificate_scope="phase7_hypergeometric_parabolic_cylinder",
        ),
    },
}

METHOD_REGISTRY: dict[str, dict[Mode, tuple[MethodSpec, ...]]] = {
    function: {mode: (method,) for mode, method in methods.items()} for function, methods in REGISTRY.items()
}
METHOD_REGISTRY["gamma"]["certified"] = (
    REGISTRY["gamma"]["certified"],
    _spec(
        "gamma",
        "certified",
        "certsf+python-flint",
        gamma_stirling_exp,
        certified=True,
        domain="Real x >= 20; explicit positive-real gamma via certified loggamma exponentiation",
        certificate_scope="gamma_positive_real_stirling_exp",
        method_id="stirling_exp",
        priority=200,
        applicability_note=(
            "Explicit method='stirling_exp' only; real x >= 20; not automatic default selection; "
            "complex gamma, reflection formulas, gamma-ratio asymptotics, and beta asymptotics excluded"
        ),
    ),
)
METHOD_REGISTRY["loggamma"]["certified"] = (
    REGISTRY["loggamma"]["certified"],
    _spec(
        "loggamma",
        "certified",
        "certsf+python-flint",
        stirling_loggamma,
        certified=True,
        domain="Real x >= 20; explicit positive-real Stirling/asymptotic loggamma method",
        certificate_scope="stirling_loggamma_positive_real",
        method_id="stirling",
        priority=200,
        applicability_note=(
            "Explicit method='stirling' only; real x >= 20; not automatic default selection; "
            "complex loggamma branches and gamma-ratio asymptotics excluded"
        ),
    ),
    _spec(
        "loggamma",
        "certified",
        "certsf+python-flint",
        stirling_loggamma_shifted,
        certified=True,
        domain="Real x >= 20; explicit shifted positive-real Stirling/asymptotic loggamma method",
        certificate_scope="stirling_loggamma_positive_real",
        method_id="stirling_shifted",
        priority=210,
        applicability_note=(
            "Explicit method='stirling_shifted' only; real x >= 20; not automatic default selection; "
            "complex loggamma branches and gamma-ratio asymptotics excluded"
        ),
    ),
    _spec(
        "loggamma",
        "certified",
        "certsf+python-flint",
        certified_auto_loggamma,
        certified=True,
        domain=(
            "Explicit certified loggamma selector; direct Arb outside the positive-real Stirling scope; "
            "real x >= 20 may select Stirling or shifted Stirling"
        ),
        certificate_scope="direct_arb_primitive|stirling_loggamma_positive_real",
        method_id="certified_auto",
        priority=220,
        applicability_note=(
            "Explicit method='certified_auto' only; does not change method=None, method='auto', "
            "or default certified dispatch; no complex Stirling or gamma-ratio asymptotics"
        ),
    ),
)

_VALID_MODES = frozenset(_MODE_ORDER)
_VALID_FUNCTIONS = frozenset(_FUNCTION_ORDER)
_PLANNED_METHODS: dict[tuple[str, Mode, str], str] = {}


def dispatch(
    function: str,
    *args: Any,
    dps: int = 50,
    mode: Mode = "auto",
    certify: bool = False,
    method: str | None = None,
) -> SFResult:
    """Dispatch a public wrapper call through the explicit method registry."""

    if function not in _VALID_FUNCTIONS:
        raise ValueError(f"unknown special function: {function!r}")
    selected_mode = _select_mode(mode, certify, dps)
    method_spec = _method_spec(function, selected_mode, method)
    return method_spec.callable(*args, dps=dps)


def available_functions() -> tuple[str, ...]:
    """Return the canonical public function names known to the dispatcher."""

    return _FUNCTION_ORDER


def available_modes() -> tuple[Mode, ...]:
    """Return the accepted dispatcher modes."""

    return _MODE_ORDER


def available_methods() -> tuple[MethodSpec, ...]:
    """Return all registered concrete methods in dispatch order."""

    return tuple(
        method
        for function in _FUNCTION_ORDER
        for mode in _CONCRETE_MODES
        for method in sorted(METHOD_REGISTRY[function][mode], key=lambda item: item.priority)
    )


def _select_mode(mode: Mode, certify: bool, dps: int) -> Mode:
    if mode not in _VALID_MODES:
        valid = ", ".join(_MODE_ORDER)
        raise ValueError(f"mode must be one of: {valid}")
    if mode == "auto":
        if certify:
            return "certified"
        return "fast" if int(dps) <= 15 else "high_precision"
    return mode


def _method_spec(function: str, mode: Mode, requested_method: str | None = None) -> MethodSpec:
    try:
        methods = METHOD_REGISTRY[function][mode]
    except KeyError as exc:  # pragma: no cover - guarded by public validation
        raise RuntimeError(f"no backend registered for {function!r} in mode {mode!r}") from exc
    if requested_method is None or requested_method == "auto":
        return sorted(methods, key=lambda item: item.priority)[0]
    if not isinstance(requested_method, str):
        raise ValueError("method must be a string or None")

    for method in methods:
        if method.method_id == requested_method:
            return method

    planned_message = _PLANNED_METHODS.get((function, mode, requested_method))
    if planned_message is not None:
        raise ValueError(planned_message)

    available = ", ".join(("auto", *(method.method_id for method in sorted(methods, key=lambda item: item.priority))))
    raise ValueError(
        f"method {requested_method!r} is not available for {function!r} in mode {mode!r}; "
        f"available methods: {available}"
    )


def _validate_method_registry() -> None:
    expected_functions = set(_FUNCTION_ORDER)
    registered_functions = set(REGISTRY)
    if registered_functions != expected_functions:
        raise RuntimeError(
            "dispatcher registry function mismatch: "
            f"missing={sorted(expected_functions - registered_functions)!r}, "
            f"extra={sorted(registered_functions - expected_functions)!r}"
        )

    expected_modes = set(_CONCRETE_MODES)
    for function, methods in REGISTRY.items():
        registered_modes = set(methods)
        if registered_modes != expected_modes:
            raise RuntimeError(
                f"dispatcher registry mode mismatch for {function!r}: "
                f"missing={sorted(expected_modes - registered_modes)!r}, "
                f"extra={sorted(registered_modes - expected_modes)!r}"
            )
        for mode, method in methods.items():
            if method.function != function or method.mode != mode:
                raise RuntimeError(
                    "dispatcher registry MethodSpec mismatch: "
                    f"key=({function!r}, {mode!r}), "
                    f"spec=({method.function!r}, {method.mode!r})"
                )
            if not callable(method.callable):
                raise RuntimeError(f"dispatcher registry method is not callable: {function!r}/{mode!r}")
            if method.certified and method.certificate_scope is None:
                raise RuntimeError(f"certified method missing certificate scope: {function!r}/{mode!r}")

    registered_v2_functions = set(METHOD_REGISTRY)
    if registered_v2_functions != expected_functions:
        raise RuntimeError(
            "dispatcher method registry v2 function mismatch: "
            f"missing={sorted(expected_functions - registered_v2_functions)!r}, "
            f"extra={sorted(registered_v2_functions - expected_functions)!r}"
        )
    for function, modes in METHOD_REGISTRY.items():
        registered_modes = set(modes)
        if registered_modes != expected_modes:
            raise RuntimeError(
                f"dispatcher method registry v2 mode mismatch for {function!r}: "
                f"missing={sorted(expected_modes - registered_modes)!r}, "
                f"extra={sorted(registered_modes - expected_modes)!r}"
            )
        for mode, v2_methods in modes.items():
            if not v2_methods:
                raise RuntimeError(f"dispatcher method registry v2 has no methods for {function!r}/{mode!r}")
            default_method = min(v2_methods, key=lambda item: item.priority)
            if default_method != REGISTRY[function][mode]:
                raise RuntimeError(f"dispatcher default method mismatch for {function!r}/{mode!r}")
            method_ids: set[str] = set()
            for v2_method in v2_methods:
                if v2_method.function != function or v2_method.mode != mode:
                    raise RuntimeError(
                        "dispatcher method registry v2 MethodSpec mismatch: "
                        f"key=({function!r}, {mode!r}), "
                        f"spec=({v2_method.function!r}, {v2_method.mode!r})"
                    )
                if v2_method.method_id in method_ids:
                    raise RuntimeError(f"duplicate method id for {function!r}/{mode!r}: {v2_method.method_id!r}")
                method_ids.add(v2_method.method_id)
                if v2_method.priority < 0:
                    raise RuntimeError(f"method priority must be nonnegative: {function!r}/{mode!r}")
                if not v2_method.applicability_note:
                    raise RuntimeError(f"method missing applicability note: {function!r}/{mode!r}")
                if v2_method.certified:
                    if v2_method.certificate_scope is None:
                        raise RuntimeError(f"certified method missing certificate scope: {function!r}/{mode!r}")
                    if v2_method.certificate_level is None or v2_method.audit_status is None:
                        raise RuntimeError(f"certified method missing audit metadata: {function!r}/{mode!r}")


_validate_method_registry()
