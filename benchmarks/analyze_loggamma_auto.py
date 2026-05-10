from __future__ import annotations

import json
from time import perf_counter
from typing import Any

from certsf import loggamma


X_VALUES = ("3.2", "20", "21", "30", "37", "38", "50", "100", "1000", "10000")
DPS_VALUES = (30, 50, 80, 100, 150, 200)
METHODS = ("arb", "stirling", "stirling_shifted", "certified_auto")


def main() -> None:
    for record in run_grid(X_VALUES, DPS_VALUES):
        print(json.dumps(record, sort_keys=True))


def run_grid(x_values: tuple[str, ...], dps_values: tuple[int, ...]) -> list[dict[str, Any]]:
    return [
        run_case(x=x, dps=dps, method_requested=method)
        for x in x_values
        for dps in dps_values
        for method in METHODS
    ]


def run_case(*, x: str, dps: int, method_requested: str) -> dict[str, Any]:
    start = perf_counter()
    try:
        result = loggamma(x, mode="certified", method=method_requested, dps=dps)
        elapsed = perf_counter() - start
    except Exception as exc:
        elapsed = perf_counter() - start
        return {
            "function": "loggamma",
            "x": x,
            "dps": dps,
            "method_requested": method_requested,
            "result_method": None,
            "backend": None,
            "certified": False,
            "elapsed_seconds": elapsed,
            "abs_error_bound": None,
            "terms_used": None,
            "certificate_scope": None,
            "selected_method": None,
            "auto_selected_method": None,
            "auto_reason": None,
            "shift": None,
            "shifted_argument": None,
            "shift_policy": None,
            "coefficient_source": None,
            "largest_bernoulli_used": None,
            "preselected": None,
            "can_certify": None,
            "estimated_terms_used": None,
            "auto_candidates": None,
            "error": str(exc),
        }

    diagnostics = result.diagnostics
    auto_candidates = diagnostics.get("auto_candidates")
    selected_candidate = _selected_candidate(auto_candidates)
    return {
        "function": result.function,
        "x": x,
        "dps": dps,
        "method_requested": method_requested,
        "result_method": result.method,
        "backend": result.backend,
        "certified": result.certified,
        "elapsed_seconds": elapsed,
        "abs_error_bound": result.abs_error_bound,
        "terms_used": result.terms_used,
        "certificate_scope": diagnostics.get("certificate_scope"),
        "selected_method": diagnostics.get("selected_method"),
        "auto_selected_method": diagnostics.get("auto_selected_method"),
        "auto_reason": diagnostics.get("auto_reason"),
        "shift": diagnostics.get("shift"),
        "shifted_argument": diagnostics.get("shifted_argument"),
        "shift_policy": diagnostics.get("shift_policy"),
        "coefficient_source": diagnostics.get("coefficient_source"),
        "largest_bernoulli_used": diagnostics.get("largest_bernoulli_used"),
        "preselected": _candidate_field(selected_candidate, "preselected"),
        "can_certify": _candidate_field(selected_candidate, "can_certify"),
        "estimated_terms_used": _candidate_field(selected_candidate, "estimated_terms_used"),
        "auto_candidates": auto_candidates,
        "error": None if result.certified else diagnostics.get("error"),
    }


def _selected_candidate(candidates: Any) -> dict[str, Any] | None:
    if not isinstance(candidates, list):
        return None
    for candidate in candidates:
        if isinstance(candidate, dict) and candidate.get("selected") is True:
            return candidate
    return None


def _candidate_field(candidate: dict[str, Any] | None, key: str) -> Any:
    if candidate is None:
        return None
    return candidate.get(key)


if __name__ == "__main__":
    main()
