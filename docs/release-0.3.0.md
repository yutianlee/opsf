# certsf 0.3.0 Planning

`v0.3.0` is the first `certsf` line with a custom certified asymptotic method.
It keeps the 0.2 public special-function wrapper surface and adds an explicit
positive-real `loggamma` Stirling methods behind method registry v2.

The implementation PRs did not change package version metadata, did not change
default method selection, and did not alter existing certified results for
calls that omit `method=...` or pass `method="auto"`. The first release
metadata bump for this line is planned in
[`release-0.3.0-alpha.1.md`](release-0.3.0-alpha.1.md).

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
  without changing omitted-method or `method="auto"` dispatch;
- `certificate_scope="stirling_loggamma_positive_real"`;
- `certificate_level="custom_asymptotic_bound"`; and
- `audit_status="theorem_documented"`.

The Stirling, shifted Stirling, and certified-auto selector are additional
registered methods for the existing public `loggamma` wrapper. They are not
new public special-function wrappers and are not automatic default selection.
Default certified `loggamma` remains the existing direct Arb path.

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
only custom-certified alpha scope is the positive-real Stirling `loggamma`
methods documented in [`stirling_loggamma.md`](stirling_loggamma.md).

## Documentation

The line includes:

- [`certified_scope_0_3_0.md`](certified_scope_0_3_0.md), which records the
  0.3.0 development support matrix and the narrow active custom-method row;
- [`stirling_loggamma.md`](stirling_loggamma.md), which records the formula,
  domain, diagnostics, certificate metadata, tail-bound contract, and
  exclusions for the first custom asymptotic method.

## Benchmarks

The manual benchmark
[`benchmarks/bench_loggamma_methods.py`](../benchmarks/bench_loggamma_methods.py)
emits JSON-lines timing records for direct Arb certified `loggamma`, explicit
Stirling, explicit shifted Stirling, explicit certified-auto selection,
high-precision mpmath, and fast SciPy over representative positive real inputs.
It is evidence-gathering infrastructure only; custom methods and the selector
remain explicit and are not claimed as the faster or default method.

## Validation Expectations

Validation should confirm that:

- explicit `method="stirling"` and `method="stirling_shifted"` certify
  positive-real `loggamma` only for real `x >= 20`;
- explicit `method="certified_auto"` may select direct Arb or a positive-real
  Stirling method, while preserving the selected backend's certificate scope;
- default certified `loggamma` and explicit `method="arb"` continue to use the
  existing direct Arb path;
- unsupported domains and unsupported modes fail cleanly rather than falling
  back to mpmath in certified mode;
- release metadata changes are limited to the dedicated alpha release-planning
  PR;
- no parabolic-cylinder, Faddeeva, `wofz`, or plasma-dispersion support claim is
  added.
