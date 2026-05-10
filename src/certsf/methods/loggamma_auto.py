"""Explicit certified-method selector for ``loggamma``."""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from certsf.backends import arb_backend
from certsf.backends._common import ensure_dps
from certsf.methods.stirling import _positive_real_text, stirling_loggamma, stirling_loggamma_shifted
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
                    "reason": domain_error,
                    "certified": result.certified,
                    "result_method": result.method,
                    "backend": result.backend,
                }
            ],
        )

    candidates: list[dict[str, Any]] = []
    stirling = stirling_loggamma(x_text, dps=requested_dps)
    candidates.append(_candidate_summary("stirling", stirling))
    if stirling.certified:
        candidates[-1]["selected"] = True
        return _with_auto_diagnostics(
            stirling,
            selected_method="stirling",
            reason="unshifted Stirling tail bound satisfied the requested tolerance",
            candidates=candidates,
        )

    shifted = stirling_loggamma_shifted(x_text, dps=requested_dps)
    candidates.append(_candidate_summary("stirling_shifted", shifted))
    if shifted.certified:
        candidates[-1]["selected"] = True
        return _with_auto_diagnostics(
            shifted,
            selected_method="stirling_shifted",
            reason="shifted Stirling selected because unshifted Stirling did not certify",
            candidates=candidates,
        )

    arb = arb_backend.arb_loggamma(x, dps=requested_dps)
    candidates.append(_candidate_summary("arb", arb))
    candidates[-1]["selected"] = True
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
