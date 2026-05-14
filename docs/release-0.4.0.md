# certsf 0.4.0 Development Plan

`v0.4.0` is a new development line after the completed `v0.3.0` final
release. This document tracks v0.4.0 development planning: it does not
authorize a release, bump the package version, change default runtime
behavior, or broaden certification claims beyond implemented and documented
explicit methods.

The positive-real method implementation closeout is recorded in
[`v0.4.0_method_closeout.md`](v0.4.0_method_closeout.md).
The release-readiness preflight is recorded in
[`v0.4.0_release_readiness_preflight.md`](v0.4.0_release_readiness_preflight.md).

The target direction is explicit certified positive-real gamma-ratio and beta
methods built from the existing certified positive-real `loggamma` machinery.

## Active Scopes

The first active implementation target was the explicit certified
positive-real `loggamma_ratio` method:

```python
loggamma_ratio(a, b, mode="certified", method="stirling_diff", dps=...)
```

The domain is finite real `a >= 20` and finite real `b >= 20`. The method
computes a certified enclosure for `loggamma(a) - loggamma(b)` by subtracting
the already widened positive-real certified `loggamma` Arb balls for `a` and
`b`.

It uses certificate scope:

- `loggamma_ratio_positive_real_stirling_diff`

The next active implementation target is the explicit certified positive-real
`gamma_ratio` method:

```python
gamma_ratio(a, b, mode="certified", method="stirling_ratio", dps=...)
```

The domain is finite real `a >= 20` and finite real `b >= 20`. The method
uses `exp(loggamma_ratio(a, b))` after the explicit `loggamma_ratio`
certificate is in place.

It uses certificate scope:

- `gamma_ratio_positive_real_stirling_ratio`

The final active implementation target in this plan is the explicit certified
positive-real `beta` method:

```python
beta(a, b, mode="certified", method="stirling_beta", dps=...)
```

The domain is finite real `a >= 20` and finite real `b >= 20`. The method uses
`exp(loggamma(a) + loggamma(b) - loggamma(a + b))` with the existing
positive-real `loggamma` certificates and explicit cancellation/error
accounting.

It uses certificate scope:

- `beta_positive_real_stirling_beta`

## Later Certificate Scope

No additional certificate scope is active in this planning document.

## Dispatch Guardrails

All proposed methods are explicit-only. The v0.4.0 development line must not
change:

- `method=None` behavior;
- `method="auto"` behavior;
- default certified dispatch; or
- existing direct Arb paths.

The existing direct Arb certified paths for `loggamma_ratio`, `gamma_ratio`,
and `beta` remain the default certified behavior. This line has no
default-dispatch promotion.

## Exclusions

The v0.4.0 positive-real gamma-ratio and beta plan excludes:

- no complex gamma-ratio Stirling certification;
- no complex beta Stirling certification;
- no reflection-formula certification;
- no near-pole behavior;
- no simultaneous-pole limiting values;
- no default-dispatch promotion;
- no parabolic-cylinder promotion; and
- no broad package-wide certification claim.

This plan does not add public wrappers, change workflow files, alter release
policy, or promote any explicit method into default dispatch.
