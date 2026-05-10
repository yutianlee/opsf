# certsf 0.3.0 Planning

`v0.3.0` targets the first custom certified asymptotic-method line for
`certsf`. This planning PR is documentation-only: it does not change
`src/certsf`, public API behavior, package version metadata, backend formulas,
or any existing certification result.

## Target Scope

The planned v0.3.0 implementation work targets:

- method registry v2, with explicit method selection diagnostics for custom
  certified methods;
- the first custom certified `loggamma` Stirling/asymptotic method;
- a positive-real domain first, initially real `x >= 20`;
- `certificate_scope="stirling_loggamma_positive_real"`;
- `certificate_level="custom_asymptotic_bound"`; and
- `audit_status="theorem_documented"`.

The planned `loggamma` method is an additional certified method for the
existing public `loggamma` wrapper. It is not a new public special-function
wrapper.

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
public API, package version, or existing certification scope changed.
