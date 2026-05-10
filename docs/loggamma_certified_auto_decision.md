# Certified-auto loggamma decision support

This file is `docs/loggamma_certified_auto_decision.md`.

This note records evidence-gathering infrastructure for deciding whether a
future release should consider changing certified `loggamma` default selection.
It does not change runtime behavior. In `v0.3.0-alpha.2`,
`method="certified_auto"` remains explicit only, default certified `loggamma`
remains the direct Arb path, and `method="auto"` remains unchanged.
The key status remains: default certified `loggamma` remains the direct Arb path.

## Current Selector

Explicit:

```python
loggamma(x, mode="certified", method="certified_auto", dps=...)
```

The selector may choose direct Arb, explicit unshifted Stirling, or explicit
shifted Stirling. Outside the positive-real custom Stirling scope, it selects
direct Arb rather than attempting a custom asymptotic method. For real
`x >= 20`, it chooses a Stirling path only when the documented positive-real
tail-bound certificate succeeds. If custom selection is uncertain or cannot
certify the requested precision, direct Arb remains the conservative path.

## Evidence Tooling

[`benchmarks/analyze_loggamma_auto.py`](../benchmarks/analyze_loggamma_auto.py)
compares certified `loggamma` with:

- `method="arb"`;
- `method="stirling"`;
- `method="stirling_shifted"`; and
- `method="certified_auto"`.

The script emits JSON-lines records over a moderate grid:

- `x in ["3.2", "20", "21", "30", "37", "38", "50", "100", "1000", "10000"]`;
- `dps in [30, 50, 80, 100, 150, 200]`.

Unsupported explicit Stirling cases are recorded as non-certified records with
an `error` field rather than terminating the run. Records include the requested
method, selected method diagnostics, certificate scope, timing, bounds, term
counts, shift policy, coefficient source, and auto-selector diagnostics.

A compact representative sample is stored at
[`benchmark_samples/loggamma_certified_auto_sample.jsonl`](benchmark_samples/loggamma_certified_auto_sample.jsonl).
It covers `x in ["3.2", "20", "38", "1000"]` and `dps in [50, 100]`.

The sample can be summarized with
[`benchmarks/summarize_loggamma_auto.py`](../benchmarks/summarize_loggamma_auto.py).
The committed summary is
[`benchmark_samples/loggamma_certified_auto_sample_summary.json`](benchmark_samples/loggamma_certified_auto_sample_summary.json).

## Current Evidence Summary

The committed sample is intentionally small. It shows that
`method="certified_auto"` remains explicit only, direct Arb remains the default
certified `loggamma` path, and unsupported explicit Stirling requests are
reported as structured non-certified cases rather than broadening the custom
method scope.

Within the sample, `certified_auto` selects direct Arb outside the positive-real
Stirling scope, selects unshifted Stirling for several positive-real cases where
the tail-bound certificate succeeds, and selects shifted Stirling for the
`x = 20`, `dps = 100` case where unshifted Stirling does not certify but shifted
Stirling does. The sample also records timing comparisons against direct Arb,
including cases where the selector is slower than direct Arb.

This evidence is not sufficient to change the default. Changing the default
certified `loggamma` selector would be a visible behavior change requiring a
dedicated runtime PR, release note, stability review, and fresh validation.
Today, `certified_auto` is valuable as an opt-in selector and as a diagnostic
benchmark path.

## Recommendation

For now, keep direct Arb as the default certified `loggamma` method. Keep
`method="certified_auto"` explicit. Consider a future guarded default only after
broader benchmark evidence and user-facing stability review.

## Decision Criteria

This PR provides tooling needed to decide later. It does not claim that
`certified_auto` is faster than direct Arb, and it does not recommend changing the default in this PR. A future default-dispatch proposal should use the
benchmark output together with certification evidence, failure-mode review,
and release-copy guardrails.

Any future default change should still preserve these exclusions unless a
separate proof, implementation, tests, and documentation update explicitly
changes them:

- no certification for complex Stirling expansions;
- no gamma-ratio asymptotics;
- no beta asymptotics;
- no new public wrappers; and
- parabolic-cylinder wrappers remain `experimental_formula`.
