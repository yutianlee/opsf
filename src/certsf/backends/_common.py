"""Shared helpers for backend wrappers."""

from __future__ import annotations

import json
from typing import Any

from certsf.result import SFResult

UNCERTIFIED_WARNING = "High precision numerical value, but no rigorous error enclosure."


def ensure_dps(dps: int) -> int:
    requested = int(dps)
    if requested <= 0:
        raise ValueError("dps must be a positive integer")
    return requested


def scipy_number(value: Any) -> Any:
    if isinstance(value, str):
        text = value.strip().replace("i", "j")
        return complex(text) if "j" in text.lower() else float(text)
    return value


def scipy_real(value: Any) -> float:
    if isinstance(value, str):
        return float(value.strip())
    return float(value)


def float_digits(dps: int) -> int:
    return 17


def number_to_string(value: Any, *, digits: int = 17) -> str:
    if hasattr(value, "item"):
        try:
            value = value.item()
        except ValueError:
            pass
    if isinstance(value, complex):
        real = format(float(value.real), f".{digits}g")
        imag_abs = format(abs(float(value.imag)), f".{digits}g")
        sign = "+" if value.imag >= 0 else "-"
        return f"{real}{sign}{imag_abs}j"
    if isinstance(value, float):
        return format(value, f".{digits}g")
    return str(value)


def json_string(mapping: dict[str, str]) -> str:
    return json.dumps(mapping, sort_keys=True)


def make_result(
    *,
    function: str,
    value: str,
    requested_dps: int,
    working_dps: int,
    method: str,
    backend: str,
    certified: bool,
    abs_error_bound: str | None = None,
    rel_error_bound: str | None = None,
    terms_used: int | None = None,
    diagnostics: dict[str, Any] | None = None,
) -> SFResult:
    return SFResult(
        value=value,
        abs_error_bound=abs_error_bound,
        rel_error_bound=rel_error_bound,
        certified=certified,
        function=function,
        method=method,
        backend=backend,
        requested_dps=requested_dps,
        working_dps=working_dps,
        terms_used=terms_used,
        diagnostics={} if diagnostics is None else diagnostics,
    )
