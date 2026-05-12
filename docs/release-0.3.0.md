# certsf 0.3.0 Planning

`v0.3.0` is the first `certsf` line with custom certified asymptotic methods.
It keeps the 0.2 public special-function wrapper surface and adds explicit
positive-real `loggamma` and `gamma` methods behind method registry v2.

The implementation PRs did not change package version metadata, did not change
default method selection, and did not alter existing certified results for
calls that omit `method=...` or pass `method="auto"`. The first release
metadata bump for this line was planned in
[`release-0.3.0-alpha.1.md`](release-0.3.0-alpha.1.md). The second alpha,
[`release-0.3.0-alpha.2.md`](release-0.3.0-alpha.2.md), packages the explicit
`method="certified_auto"` selector. The third alpha,
[`release-0.3.0-alpha.3.md`](release-0.3.0-alpha.3.md), packages the
preselection optimization for that explicit selector. The fourth alpha,
[`release-0.3.0-alpha.4.md`](release-0.3.0-alpha.4.md), packages the explicit
positive-real `gamma` method `method="stirling_exp"` with no default-dispatch
change.

## Active Scope

The v0.3.0 line includes:

- method registry v2 metadata for method id, priority, certificate level, audit
  status, and applicability notes;
- `method=None` and `method="auto"` behavior equivalent to the previous
  automatic selection path;
- `method="arb"` selection for existing certified Arb backends when the
  resolved mode is `certified`;
- explicit `loggamma(x, mode="certified", method="stirling")` for real
  `x >= 20`;
- explicit `loggamma(x, mode="certified", method="stirling_shifted")` for
  real `x >= 20`, using Arb logs and the recurrence
  `loggamma(x) = stirling_loggamma_sum(x+r) - sum(log(x+j))`;
- explicit `loggamma(x, mode="certified", method="certified_auto")` as a
  selector that may choose direct Arb or a positive-real Stirling method
  without changing omitted-method or `method="auto"` dispatch, using
  preselection diagnostics to avoid unnecessary full custom candidate
  evaluations;
- explicit `gamma(x, mode="certified", method="stirling_exp")` for finite real
  `x >= 20`, using a certified positive-real `loggamma` Arb enclosure and Arb
  exponentiation;
- `certificate_scope="stirling_loggamma_positive_real"`;
- `certificate_scope="gamma_positive_real_stirling_exp"`;
- `certificate_level="custom_asymptotic_bound"`; and
- `audit_status="theorem_documented"`.

The Stirling, shifted Stirling, certified-auto selector, and Stirling-exp
gamma method are additional registered methods for existing public wrappers.
They are not new public special-function wrappers and are not automatic
default selection. Default certified `loggamma` and default certified `gamma`
remain the existing direct Arb paths.

## Non-Goals

The v0.3.0 line does not target parabolic-cylinder promotion. The
parabolic-cylinder family remains an `experimental_formula` surface unless a
separate proof, implementation, tests, and documentation change explicitly
broadens that scope.

The v0.3.0 line does not add Faddeeva, `wofz`, or plasma-dispersion wrappers.
It also does not add complex Stirling, gamma-ratio asymptotics, or beta
asymptotics.

The v0.3.0 line does not make a broad complete-certification claim for the
package, for all `loggamma` inputs, or for every special-function family. The
only custom-certified alpha scopes are the positive-real Stirling `loggamma`
methods documented in [`stirling_loggamma.md`](stirling_loggamma.md) and the
positive-real `gamma` method documented in
[`gamma_stirling_exp.md`](gamma_stirling_exp.md).

## Future Work

The next candidate custom method is positive-real `rgamma` via
`exp(-loggamma)`, using the existing certified positive-real `loggamma`
Arb-ball enclosure. The planned explicit method name is
`method="stirling_recip"` for finite real `x >= 20`.

This reciprocal-gamma method is not implemented yet.
No release claim is active yet.
No default dispatch change is made or planned by the documentation-only
planning PR. See
[`rgamma_stirling_recip.md`](rgamma_stirling_recip.md).

## Positive-Real `gamma` via Loggamma Exponentiation

The active explicit positive-real `gamma(x)` method uses certified `loggamma`
exponentiation. The explicit method name is
`gamma(x, mode="certified", method="stirling_exp", dps=...)` for finite real
`x >= 20`. The certificate scope is
`gamma_positive_real_stirling_exp`, with certificate level
`custom_asymptotic_bound` and audit status `theorem_documented`.

This is an active explicit method only; no default dispatch behavior changes.
The method uses a rigorous positive-real `loggamma` enclosure and Arb
exponentiation, and the returned `gamma` enclosure accounts for both
finite-expression Arb radius and the propagated explicit loggamma tail bound.

The method excludes complex `gamma`, real `x < 20`, real `x <= 0`,
reflection-formula paths, near-pole behavior, gamma-ratio asymptotics, and beta
asymptotics. See [`gamma_stirling_exp.md`](gamma_stirling_exp.md).

## Documentation

The line includes:

- [`certified_scope_0_3_0.md`](certified_scope_0_3_0.md), which records the
  0.3.0 development support matrix and the narrow active custom-method row;
- [`stirling_loggamma.md`](stirling_loggamma.md), which records the formula,
  domain, diagnostics, certificate metadata, tail-bound contract, and
  exclusions for the first custom asymptotic method;
- [`loggamma_certified_auto_decision.md`](loggamma_certified_auto_decision.md),
  which records decision support and evidence-gathering notes for any later
  consideration of default certified `loggamma` method selection;
- [`gamma_stirling_exp.md`](gamma_stirling_exp.md), which records the active
  explicit positive-real `gamma` method and its exclusions;
- [`rgamma_stirling_recip.md`](rgamma_stirling_recip.md), which records the
  planned inactive positive-real `rgamma` method and its exclusions;
- [`v0_3_custom_method_audit.md`](v0_3_custom_method_audit.md), which
  summarizes all active 0.3 custom methods, their diagnostics, preserved
  default-dispatch behavior, and exclusions;
- [`release-0.3.0-alpha.4.md`](release-0.3.0-alpha.4.md), which records the
  prerelease plan for packaging the explicit positive-real `gamma`
  `method="stirling_exp"` with no default-dispatch change; and
- [`release-0.3.0-alpha.3.md`](release-0.3.0-alpha.3.md), which records the
  prerelease plan for packaging the explicit `certified_auto` preselection
  optimization with no default-dispatch change.

## Benchmarks

The manual benchmark
[`benchmarks/bench_loggamma_methods.py`](../benchmarks/bench_loggamma_methods.py)
emits JSON-lines timing records for direct Arb certified `loggamma`, explicit
Stirling, explicit shifted Stirling, explicit certified-auto selection,
high-precision mpmath, and fast SciPy over representative positive real inputs.
It is evidence-gathering infrastructure only; custom methods and the selector
remain explicit and are not claimed as the faster or default method.

The manual benchmark
[`benchmarks/bench_gamma_methods.py`](../benchmarks/bench_gamma_methods.py)
emits JSON-lines timing and diagnostic records for direct Arb certified
`gamma`, explicit `method="stirling_exp"`, high-precision mpmath, and fast
SciPy over representative positive real inputs. It is evidence gathering only:
`method="stirling_exp"` remains explicit, direct Arb remains the default
certified `gamma` path, and this document does not claim performance
superiority.

The decision-support analyzer
[`benchmarks/analyze_loggamma_auto.py`](../benchmarks/analyze_loggamma_auto.py)
compares direct Arb, explicit unshifted Stirling, explicit shifted Stirling,
and explicit `method="certified_auto"` over a broader certified-mode grid. It
records unsupported explicit Stirling cases as structured failures. This is
evidence gathering only: `certified_auto` remains explicit, and this document
does not make any default-dispatch change.

The summary helper
[`benchmarks/summarize_loggamma_auto.py`](../benchmarks/summarize_loggamma_auto.py)
reduces analyzer JSON-lines output into certified counts, selector choices,
timing comparisons, and failure-pattern summaries. A compact generated sample
is stored at
[`docs/benchmark_samples/loggamma_certified_auto_sample_summary.json`](benchmark_samples/loggamma_certified_auto_sample_summary.json).
The current recommendation remains conservative: direct Arb stays the default
certified `loggamma` method, `method="certified_auto"` stays explicit, and no
default-dispatch change is made in this evidence PR.

## Validation Expectations

Validation should confirm that:

- explicit `method="stirling"` and `method="stirling_shifted"` certify
  positive-real `loggamma` only for real `x >= 20`;
- explicit `method="certified_auto"` may select direct Arb or a positive-real
  Stirling method, while preserving the selected backend's certificate scope;
- explicit `method="stirling_exp"` certifies `gamma` only for finite real
  `x >= 20`;
- default certified `loggamma` and explicit `method="arb"` continue to use the
  existing direct Arb path;
- default certified `gamma` and explicit `method="arb"` continue to use the
  existing direct Arb path;
- unsupported domains and unsupported modes fail cleanly rather than falling
  back to mpmath in certified mode;
- release metadata changes are limited to the dedicated alpha release-planning
  PR;
- no parabolic-cylinder, Faddeeva, `wofz`, or plasma-dispersion support claim is
  added.
