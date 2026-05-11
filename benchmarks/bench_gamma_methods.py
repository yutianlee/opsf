from __future__ import annotations

import json
from time import perf_counter
from typing import Any

from certsf import gamma


X_VALUES = ("20", "38", "100", "1000")
DPS_VALUES = (50, 100)
METHOD_CASES = (
    ("certified", "arb", {"mode": "certified", "method": "arb"}),
    ("certified", "stirling_exp", {"mode": "certified", "method": "stirling_exp"}),
    ("fast", None, {"mode": "fast"}),
    ("high_precision", None, {"mode": "high_precision"}),
)


def main() -> None:
    for x in X_VALUES:
        for dps in DPS_VALUES:
            for mode, method_requested, kwargs in METHOD_CASES:
                record = run_case(
                    x=x,
                    dps=dps,
                    mode=mode,
                    method_requested=method_requested,
                    kwargs=kwargs,
                )
                print(json.dumps(record, sort_keys=True))


def run_case(
    *,
    x: str,
    dps: int,
    mode: str,
    method_requested: str | None,
    kwargs: dict[str, Any],
) -> dict[str, Any]:
    call_kwargs = dict(kwargs)
    call_kwargs["dps"] = dps

    start = perf_counter()
    try:
        result = gamma(x, **call_kwargs)
        elapsed = perf_counter() - start
    except Exception as exc:
        elapsed = perf_counter() - start
        return _failure_record(
            x=x,
            dps=dps,
            mode=mode,
            method_requested=method_requested,
            elapsed=elapsed,
            error=str(exc),
        )

    diagnostics = result.diagnostics
    return {
        "function": result.function,
        "x": x,
        "dps": dps,
        "mode": mode,
        "method_requested": method_requested,
        "result_method": result.method,
        "backend": result.backend,
        "certified": result.certified,
        "elapsed_seconds": elapsed,
        "abs_error_bound": result.abs_error_bound,
        "rel_error_bound": result.rel_error_bound,
        "terms_used": result.terms_used,
        "certificate_scope": diagnostics.get("certificate_scope"),
        "selected_method": diagnostics.get("selected_method"),
        "loggamma_method_used": diagnostics.get("loggamma_method_used"),
        "loggamma_abs_error_bound": diagnostics.get("loggamma_abs_error_bound"),
        "exp_radius": diagnostics.get("exp_radius"),
        "propagated_error_bound": diagnostics.get("propagated_error_bound"),
        "error": None if result.certified else diagnostics.get("error", f"mode={mode!r} is not certified"),
    }


def _failure_record(
    *,
    x: str,
    dps: int,
    mode: str,
    method_requested: str | None,
    elapsed: float,
    error: str,
) -> dict[str, Any]:
    return {
        "function": "gamma",
        "x": x,
        "dps": dps,
        "mode": mode,
        "method_requested": method_requested,
        "result_method": None,
        "backend": None,
        "certified": False,
        "elapsed_seconds": elapsed,
        "abs_error_bound": None,
        "rel_error_bound": None,
        "terms_used": None,
        "certificate_scope": None,
        "selected_method": None,
        "loggamma_method_used": None,
        "loggamma_abs_error_bound": None,
        "exp_radius": None,
        "propagated_error_bound": None,
        "error": error,
    }


if __name__ == "__main__":
    main()
