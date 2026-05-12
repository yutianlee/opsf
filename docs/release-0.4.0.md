# certsf 0.4.0 Development Plan

`v0.4.0` is a new development line after the completed `v0.3.0` final
release. This document is planning only: it does not authorize a release, bump
the package version, change runtime behavior, or broaden certification claims.

The target direction is explicit certified positive-real gamma-ratio methods
built from the existing certified positive-real `loggamma` machinery.

## Proposed Scope

The first proposed method is an explicit certified positive-real
`loggamma_ratio` method:

```python
loggamma_ratio(a, b, mode="certified", method="stirling_diff", dps=...)
```

The intended domain is finite real `a >= 20` and finite real `b >= 20`. The
method should compute a certified enclosure for `loggamma(a) - loggamma(b)`
using the positive-real certified `loggamma` Stirling machinery and a
documented difference error budget.

Later work may add an explicit certified positive-real `gamma_ratio` method:

```python
gamma_ratio(a, b, mode="certified", method="stirling_ratio", dps=...)
```

That method should use `exp(loggamma_ratio(a, b))` after the
`loggamma_ratio` certificate is in place.

Later work may also consider an explicit certified positive-real `beta`
method:

```python
beta(a, b, mode="certified", method="stirling_beta", dps=...)
```

That method should use
`exp(loggamma(a) + loggamma(b) - loggamma(a + b))` after the required
positive-real loggamma certificates and cancellation/error accounting are
documented.

## Intended Certificate Scopes

These scope names are planning targets only:

- `loggamma_ratio_positive_real_stirling_diff`
- `gamma_ratio_positive_real_stirling_ratio`
- `beta_positive_real_stirling_beta`

They must not be treated as active runtime scopes until a later implementation
PR supplies proof notes, tests, diagnostics, and documentation.

## Dispatch Guardrails

All proposed methods are explicit-only. The v0.4.0 development line must not
change:

- `method=None` behavior;
- `method="auto"` behavior;
- default certified dispatch; or
- existing direct Arb paths.

The existing direct Arb certified paths for `loggamma_ratio`, `gamma_ratio`,
and `beta` remain the default certified behavior unless a separate future PR
explicitly proves, tests, documents, and reviews a default-dispatch change.

## Exclusions

The v0.4.0 positive-real gamma-ratio plan excludes:

- no complex gamma-ratio Stirling certification;
- no reflection-formula certification;
- no near-pole behavior;
- no simultaneous-pole limiting values;
- no default-dispatch promotion;
- no parabolic-cylinder promotion; and
- no broad package-wide certification claim.

This plan also does not implement any new method, add public wrappers, change
workflow files, or alter release policy.
