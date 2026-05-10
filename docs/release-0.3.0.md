# certsf 0.3.0 Planning

`v0.3.0` targets the first custom certified asymptotic-method line for
`certsf`. Method registry v2 infrastructure has landed so callers can request
an explicit implementation method where one is registered. This infrastructure
PR does not change package version metadata, backend formulas, default
selection behavior, or any existing certification result for calls that do not
pass `method=...`.

## Target Scope

The v0.3.0 line now includes:

- method registry v2 metadata for method id, priority, certificate level, audit
  status, and applicability notes;
- `method=None` and `method="auto"` behavior equivalent to the previous
  automatic selection path;
- `method="arb"` selection for existing certified Arb backends when the
  resolved mode is `certified`; and
- clear rejection of unsupported method/function/mode combinations.

The remaining planned v0.3.0 implementation work targets:

- the first custom certified `loggamma` Stirling/asymptotic method;
- a positive-real domain first, initially real `x >= 20`;
- `certificate_scope="stirling_loggamma_positive_real"`;
- `certificate_level="custom_asymptotic_bound"`; and
- `audit_status="theorem_documented"`.

The planned `loggamma` method is an additional certified method for the
existing public `loggamma` wrapper. It is not a new public special-function
wrapper.

`method="stirling"` is intentionally guarded as planned but not implemented.
It must fail before any backend result can be marked certified until the
separate implementation PR lands its proof references, runtime diagnostics, and
tests.

## Non-Goals

The v0.3.0 plan does not target parabolic-cylinder promotion. The
parabolic-cylinder family remains an `experimental_formula` surface unless a
separate proof, implementation, tests, and documentation change explicitly
broadens that scope.

The v0.3.0 plan does not add Faddeeva, `wofz`, or plasma-dispersion wrappers.

The v0.3.0 plan does not make a broad complete-certification claim for the
package, for all `loggamma` inputs, or for every special-function family. The
only planned custom-certified alpha scope is the positive-real Stirling
`loggamma` method documented in [`stirling_loggamma.md`](stirling_loggamma.md).

## Documentation Targets

The planning line adds:

- [`certified_scope_0_3_0.md`](certified_scope_0_3_0.md), which copies the
  current 0.2.0 support matrix and adds a planned custom-method row;
- [`stirling_loggamma.md`](stirling_loggamma.md), which records the target
  formula, intended domain, diagnostic contract, certificate metadata, and
  exclusions for the first custom asymptotic method.

## Validation Expectations

The implementation PR that lands the method must add proof references, runtime
diagnostics, method-registry tests, numerical enclosure tests, and release-scope
tests before claiming the new method as active.

For this planning PR, validation should confirm that no runtime behavior,
package version, or existing certification scope changed for default method
selection.
