# certsf 0.3.0 Planning

`v0.3.0` is the first `certsf` line with a custom certified asymptotic method.
It keeps the 0.2 public special-function wrapper surface and adds an explicit
positive-real `loggamma` Stirling method behind method registry v2.

This implementation does not change package version metadata, does not change
default method selection, and does not alter existing certified results for
calls that omit `method=...` or pass `method="auto"`.

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
- `certificate_scope="stirling_loggamma_positive_real"`;
- `certificate_level="custom_asymptotic_bound"`; and
- `audit_status="theorem_documented"`.

The Stirling method is an additional certified method for the existing public
`loggamma` wrapper. It is not a new public special-function wrapper and is not
automatic default selection. Default certified `loggamma` remains the existing
direct Arb path.

## Non-Goals

The v0.3.0 line does not target parabolic-cylinder promotion. The
parabolic-cylinder family remains an `experimental_formula` surface unless a
separate proof, implementation, tests, and documentation change explicitly
broadens that scope.

The v0.3.0 line does not add Faddeeva, `wofz`, or plasma-dispersion wrappers.

The v0.3.0 line does not make a broad complete-certification claim for the
package, for all `loggamma` inputs, or for every special-function family. The
only custom-certified alpha scope is the positive-real Stirling `loggamma`
method documented in [`stirling_loggamma.md`](stirling_loggamma.md).

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
Stirling, high-precision mpmath, and fast SciPy over representative positive
real inputs. It is evidence-gathering infrastructure only; Stirling remains
explicit and is not claimed as the faster or automatic default method.

## Validation Expectations

Validation should confirm that:

- explicit `method="stirling"` certifies positive-real `loggamma` only for
  real `x >= 20`;
- default certified `loggamma` and explicit `method="arb"` continue to use the
  existing direct Arb path;
- unsupported domains and unsupported modes fail cleanly rather than falling
  back to mpmath in certified mode;
- package version metadata is unchanged;
- no parabolic-cylinder, Faddeeva, `wofz`, or plasma-dispersion support claim is
  added.
