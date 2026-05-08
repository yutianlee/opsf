"""Mode dispatcher for special-function wrappers."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from certsf.result import SFResult

from .backends import arb_backend, mpmath_backend, scipy_backend

Mode = str


@dataclass(frozen=True)
class MethodSpec:
    """Auditable method selection record for one function/mode pair."""

    function: str
    mode: Mode
    backend: str
    callable: Callable[..., SFResult]
    certified: bool
    domain: str
    certificate_scope: str | None = None


_MODE_ORDER: tuple[Mode, ...] = ("auto", "fast", "high_precision", "certified")
_CONCRETE_MODES: tuple[Mode, ...] = ("fast", "high_precision", "certified")
_FUNCTION_ORDER = (
    "gamma",
    "loggamma",
    "rgamma",
    "gamma_ratio",
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


def _spec(
    function: str,
    mode: Mode,
    backend: str,
    method: Callable[..., SFResult],
    *,
    certified: bool,
    domain: str,
    certificate_scope: str | None = None,
) -> MethodSpec:
    return MethodSpec(
        function=function,
        mode=mode,
        backend=backend,
        callable=method,
        certified=certified,
        domain=domain,
        certificate_scope=certificate_scope,
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

_VALID_MODES = frozenset(_MODE_ORDER)
_VALID_FUNCTIONS = frozenset(_FUNCTION_ORDER)


def dispatch(
    function: str,
    *args: Any,
    dps: int = 50,
    mode: Mode = "auto",
    certify: bool = False,
) -> SFResult:
    """Dispatch a public wrapper call through the explicit method registry."""

    if function not in _VALID_FUNCTIONS:
        raise ValueError(f"unknown special function: {function!r}")
    selected_mode = _select_mode(mode, certify, dps)
    method = _method_spec(function, selected_mode)
    return method.callable(*args, dps=dps)


def available_functions() -> tuple[str, ...]:
    """Return the canonical public function names known to the dispatcher."""

    return _FUNCTION_ORDER


def available_modes() -> tuple[Mode, ...]:
    """Return the accepted dispatcher modes."""

    return _MODE_ORDER


def available_methods() -> tuple[MethodSpec, ...]:
    """Return all registered concrete methods in dispatch order."""

    return tuple(REGISTRY[function][mode] for function in _FUNCTION_ORDER for mode in _CONCRETE_MODES)


def _select_mode(mode: Mode, certify: bool, dps: int) -> Mode:
    if mode not in _VALID_MODES:
        valid = ", ".join(_MODE_ORDER)
        raise ValueError(f"mode must be one of: {valid}")
    if mode == "auto":
        if certify:
            return "certified"
        return "fast" if int(dps) <= 15 else "high_precision"
    return mode


def _method_spec(function: str, mode: Mode) -> MethodSpec:
    try:
        return REGISTRY[function][mode]
    except KeyError as exc:  # pragma: no cover - guarded by public validation
        raise RuntimeError(f"no backend registered for {function!r} in mode {mode!r}") from exc


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


_validate_method_registry()
