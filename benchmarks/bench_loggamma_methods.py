from __future__ import annotations

import json
from time import perf_counter
from typing import Any

from certsf import loggamma


X_VALUES = ("20", "50", "100", "1000", "10000")
DPS_VALUES = (30, 50, 80, 100)
METHOD_CASES = (
    ("certified", "arb", {"mode": "certified", "method": "arb"}),
    ("certified", "stirling", {"mode": "certified", "method": "stirling"}),
    ("certified", "stirling_shifted", {"mode": "certified", "method": "stirling_shifted"}),
    ("high_precision", None, {"mode": "high_precision"}),
    ("fast", None, {"mode": "fast"}),
)


def main() -> None:
    for x in X_VALUES:
        for dps in DPS_VALUES:
            for mode, method_requested, kwargs in METHOD_CASES:
                payload = _run_case(x, dps, mode, method_requested, kwargs)
                print(json.dumps(payload, sort_keys=True))


def _run_case(x: str, dps: int, mode: str, method_requested: str | None, kwargs: dict[str, Any]) -> dict[str, Any]:
    call_kwargs = dict(kwargs)
    call_kwargs["dps"] = dps
    start = perf_counter()
    result = loggamma(x, **call_kwargs)
    elapsed = perf_counter() - start
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
        "terms_used": result.terms_used,
        "abs_error_bound": result.abs_error_bound,
        "certificate_scope": result.diagnostics.get("certificate_scope"),
    }


if __name__ == "__main__":
    main()
