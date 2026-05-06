"""Mode dispatcher for special-function wrappers."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .backends import arb_backend, mpmath_backend, scipy_backend

Mode = str

_VALID_MODES = {"auto", "fast", "high_precision", "certified"}
_VALID_FUNCTIONS = {"gamma", "loggamma", "rgamma", "airy", "besselj", "pbdv"}


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
    selected_mode = _select_mode(mode, certify)
    backend_function = _backend_function(function, selected_mode)
    return backend_function(*args, dps=dps)


def _select_mode(mode: Mode, certify: bool) -> Mode:
    if mode not in _VALID_MODES:
        valid = ", ".join(sorted(_VALID_MODES))
        raise ValueError(f"mode must be one of: {valid}")
    if mode == "auto":
        return "certified" if certify else "fast"
    return mode


def _backend_function(function: str, mode: Mode) -> Callable[..., Any]:
    prefix = {
        "fast": "scipy",
        "high_precision": "mpmath",
        "certified": "arb",
    }[mode]
    module = {
        "fast": scipy_backend,
        "high_precision": mpmath_backend,
        "certified": arb_backend,
    }[mode]
    name = f"{prefix}_{function}"
    return getattr(module, name)
