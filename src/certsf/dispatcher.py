"""Mode dispatcher for special-function wrappers."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .backends import arb_backend, mpmath_backend, scipy_backend

Mode = str

_MODE_ORDER: tuple[Mode, ...] = ("auto", "fast", "high_precision", "certified")
_CONCRETE_MODES: tuple[Mode, ...] = ("fast", "high_precision", "certified")
_FUNCTION_ORDER = (
    "gamma",
    "loggamma",
    "rgamma",
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
_VALID_MODES = frozenset(_MODE_ORDER)
_VALID_FUNCTIONS = frozenset(_FUNCTION_ORDER)
_METHOD_REGISTRY: dict[Mode, dict[str, Callable[..., Any]]] = {
    "fast": {
        "gamma": scipy_backend.scipy_gamma,
        "loggamma": scipy_backend.scipy_loggamma,
        "rgamma": scipy_backend.scipy_rgamma,
        "airy": scipy_backend.scipy_airy,
        "ai": scipy_backend.scipy_ai,
        "bi": scipy_backend.scipy_bi,
        "besselj": scipy_backend.scipy_besselj,
        "bessely": scipy_backend.scipy_bessely,
        "besseli": scipy_backend.scipy_besseli,
        "besselk": scipy_backend.scipy_besselk,
        "pcfd": scipy_backend.scipy_pcfd,
        "pcfu": scipy_backend.scipy_pcfu,
        "pcfv": scipy_backend.scipy_pcfv,
        "pcfw": scipy_backend.scipy_pcfw,
        "pbdv": scipy_backend.scipy_pbdv,
    },
    "high_precision": {
        "gamma": mpmath_backend.mpmath_gamma,
        "loggamma": mpmath_backend.mpmath_loggamma,
        "rgamma": mpmath_backend.mpmath_rgamma,
        "airy": mpmath_backend.mpmath_airy,
        "ai": mpmath_backend.mpmath_ai,
        "bi": mpmath_backend.mpmath_bi,
        "besselj": mpmath_backend.mpmath_besselj,
        "bessely": mpmath_backend.mpmath_bessely,
        "besseli": mpmath_backend.mpmath_besseli,
        "besselk": mpmath_backend.mpmath_besselk,
        "pcfd": mpmath_backend.mpmath_pcfd,
        "pcfu": mpmath_backend.mpmath_pcfu,
        "pcfv": mpmath_backend.mpmath_pcfv,
        "pcfw": mpmath_backend.mpmath_pcfw,
        "pbdv": mpmath_backend.mpmath_pbdv,
    },
    "certified": {
        "gamma": arb_backend.arb_gamma,
        "loggamma": arb_backend.arb_loggamma,
        "rgamma": arb_backend.arb_rgamma,
        "airy": arb_backend.arb_airy,
        "ai": arb_backend.arb_ai,
        "bi": arb_backend.arb_bi,
        "besselj": arb_backend.arb_besselj,
        "bessely": arb_backend.arb_bessely,
        "besseli": arb_backend.arb_besseli,
        "besselk": arb_backend.arb_besselk,
        "pcfd": arb_backend.arb_pcfd,
        "pcfu": arb_backend.arb_pcfu,
        "pcfv": arb_backend.arb_pcfv,
        "pcfw": arb_backend.arb_pcfw,
        "pbdv": arb_backend.arb_pbdv,
    },
}


def dispatch(
    function: str,
    *args: Any,
    dps: int = 50,
    mode: Mode = "auto",
    certify: bool = False,
) -> Any:
    """Dispatch a public wrapper call to the requested backend."""

    if function not in _VALID_FUNCTIONS:
        raise ValueError(f"unknown special function: {function!r}")
    selected_mode = _select_mode(mode, certify, dps)
    backend_function = _backend_function(function, selected_mode)
    return backend_function(*args, dps=dps)


def available_functions() -> tuple[str, ...]:
    """Return the canonical public function names known to the dispatcher."""

    return _FUNCTION_ORDER


def available_modes() -> tuple[Mode, ...]:
    """Return the accepted dispatcher modes."""

    return _MODE_ORDER


def _select_mode(mode: Mode, certify: bool, dps: int) -> Mode:
    if mode not in _VALID_MODES:
        valid = ", ".join(_MODE_ORDER)
        raise ValueError(f"mode must be one of: {valid}")
    if mode == "auto":
        if certify:
            return "certified"
        return "fast" if int(dps) <= 15 else "high_precision"
    return mode


def _backend_function(function: str, mode: Mode) -> Callable[..., Any]:
    try:
        return _METHOD_REGISTRY[mode][function]
    except KeyError as exc:  # pragma: no cover - guarded by public validation
        raise RuntimeError(f"no backend registered for {function!r} in mode {mode!r}") from exc


def _validate_method_registry() -> None:
    expected_modes = set(_CONCRETE_MODES)
    registered_modes = set(_METHOD_REGISTRY)
    if registered_modes != expected_modes:
        raise RuntimeError(
            "dispatcher registry mode mismatch: "
            f"missing={sorted(expected_modes - registered_modes)!r}, "
            f"extra={sorted(registered_modes - expected_modes)!r}"
        )

    expected_functions = set(_FUNCTION_ORDER)
    for mode, methods in _METHOD_REGISTRY.items():
        registered_functions = set(methods)
        if registered_functions != expected_functions:
            raise RuntimeError(
                f"dispatcher registry function mismatch for {mode!r}: "
                f"missing={sorted(expected_functions - registered_functions)!r}, "
                f"extra={sorted(registered_functions - expected_functions)!r}"
            )


_validate_method_registry()
