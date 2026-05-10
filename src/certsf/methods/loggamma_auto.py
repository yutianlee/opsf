"""Explicit certified-method selector for ``loggamma``."""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from certsf.backends import arb_backend
from certsf.backends._common import ensure_dps
from certsf.methods.stirling import (
    _positive_real_text,
    estimate_shifted_stirling_policy,
    estimate_stirling_terms_for_tolerance,
    stirling_loggamma,
    stirling_loggamma_shifted,
)
from certsf.result import SFResult


def certified_auto_loggamma(x: Any, *, dps: int = 50) -> SFResult:
    """Select a certified ``loggamma`` method without changing default dispatch."""

    requested_dps = ensure_dps(dps)
    x_text, domain_error = _positive_real_text(x)
    if domain_error is not None:
        result = arb_backend.arb_loggamma(x, dps=requested_dps)
        return _with_auto_diagnostics(
            result,
            selected_method="arb",
            reason="input is outside the positive-real Stirling scope; selected direct Arb",
            candidates=[
                {
                    "method": "arb",
                    "selected": True,
                    "preselected": False,
                    "can_certify": result.certified,
                    "estimated_terms_used": None,
                    "reason": domain_error,
                    "certified": result.certified,
                    "result_method": result.method,
                    "backend": result.backend,
                }
            ],
        )

    candidates: list[dict[str, Any]] = []
    stirling_estimate = estimate_stirling_terms_for_tolerance(x_text, dps=requested_dps)
    candidates.append(_preselection_candidate("stirling", stirling_estimate))
    if stirling_estimate["can_certify"]:
        stirling = stirling_loggamma(x_text, dps=requested_dps)
        candidates[-1] = _merge_candidate(candidates[-1], _candidate_summary("stirling", stirling))
        if not stirling.certified:
            candidates[-1]["reason"] = "unshifted Stirling preselection certified but full method did not certify"
            arb = arb_backend.arb_loggamma(x, dps=requested_dps)
            candidates.append(_selected_arb_candidate(arb, "selected direct Arb after unshifted Stirling did not certify"))
            return _with_auto_diagnostics(
                arb,
                selected_method="arb",
                reason="unshifted Stirling did not certify after preselection; selected direct Arb",
                candidates=candidates,
            )

        candidates[-1]["selected"] = True
        return _with_auto_diagnostics(
            stirling,
            selected_method="stirling",
            reason="unshifted Stirling tail bound satisfied the requested tolerance",
            candidates=candidates,
        )

    shifted_estimate = estimate_shifted_stirling_policy(x_text, dps=requested_dps)
    candidates.append(_preselection_candidate("stirling_shifted", shifted_estimate))
    if shifted_estimate["can_certify"]:
        shifted = stirling_loggamma_shifted(x_text, dps=requested_dps)
        candidates[-1] = _merge_candidate(candidates[-1], _candidate_summary("stirling_shifted", shifted))
        if not shifted.certified:
            candidates[-1]["reason"] = "shifted Stirling preselection certified but full method did not certify"
            arb = arb_backend.arb_loggamma(x, dps=requested_dps)
            candidates.append(_selected_arb_candidate(arb, "selected direct Arb after shifted Stirling did not certify"))
            return _with_auto_diagnostics(
                arb,
                selected_method="arb",
                reason="shifted Stirling did not certify after preselection; selected direct Arb",
                candidates=candidates,
            )

        candidates[-1]["selected"] = True
        return _with_auto_diagnostics(
            shifted,
            selected_method="stirling_shifted",
            reason="shifted Stirling selected because unshifted Stirling did not certify",
            candidates=candidates,
        )

    arb = arb_backend.arb_loggamma(x, dps=requested_dps)
    candidates.append(_selected_arb_candidate(arb, "custom Stirling preselection did not certify"))
    return _with_auto_diagnostics(
        arb,
        selected_method="arb",
        reason="custom Stirling candidates did not certify; selected direct Arb",
        candidates=candidates,
    )


def _candidate_summary(method_id: str, result: SFResult) -> dict[str, Any]:
    diagnostics = result.diagnostics
    summary: dict[str, Any] = {
        "method": method_id,
        "selected": False,
        "certified": result.certified,
        "result_method": result.method,
        "backend": result.backend,
        "abs_error_bound": result.abs_error_bound,
        "terms_used": result.terms_used,
    }
    for key in (
        "selected_method",
        "tail_bound",
        "final_tail_bound",
        "requested_tolerance",
        "terms_attempted",
        "shift",
        "shifted_argument",
        "shift_policy",
        "error",
    ):
        if key in diagnostics:
            summary[key] = diagnostics[key]
    return summary


def _preselection_candidate(method_id: str, estimate: dict[str, Any]) -> dict[str, Any]:
    summary = {
        "method": method_id,
        "selected": False,
        "certified": False,
        "abs_error_bound": None,
        "terms_used": None,
    }
    summary.update(estimate)
    summary["method"] = method_id
    summary["selected"] = False
    return summary


def _merge_candidate(base: dict[str, Any], evaluated: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    merged.update(evaluated)
    for key in ("preselected", "can_certify", "estimated_terms_used"):
        if key in base:
            merged[key] = base[key]
    for key in (
        "tail_bound",
        "final_tail_bound",
        "requested_tolerance",
        "shift",
        "shifted_argument",
        "shift_policy",
        "coefficient_source",
        "largest_bernoulli_used",
    ):
        if key in base and key not in merged:
            merged[key] = base[key]
    return merged


def _selected_arb_candidate(result: SFResult, reason: str) -> dict[str, Any]:
    candidate = _candidate_summary("arb", result)
    candidate.update(
        {
            "selected": True,
            "preselected": False,
            "can_certify": result.certified,
            "estimated_terms_used": None,
            "reason": reason,
        }
    )
    return candidate


def _with_auto_diagnostics(
    result: SFResult,
    *,
    selected_method: str,
    reason: str,
    candidates: list[dict[str, Any]],
) -> SFResult:
    diagnostics = dict(result.diagnostics)
    diagnostics.update(
        {
            "auto_selector": "certified_auto",
            "auto_selected_method": selected_method,
            "auto_reason": reason,
            "auto_candidates": candidates,
        }
    )
    return replace(result, diagnostics=diagnostics)
