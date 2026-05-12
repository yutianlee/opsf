# Positive-Real `rgamma` via Certified Loggamma Exponentiation

This document records the active explicit method for positive-real reciprocal
gamma. It does not change default dispatch, does not add a public wrapper, and
is not automatic default selection.

The active explicit method is:

```python
rgamma(x, mode="certified", method="stirling_recip", dps=...)
```

## Target

The target function is:

```text
rgamma(x) = 1/Gamma(x)
```

The preferred reduction is:

```text
rgamma(x) = exp(-loggamma(x))
```

Equivalently for diagnostics, the formula string is
`formula="rgamma=exp(-loggamma)"`.

The active domain is finite real `x >= 20`. This means finite real x >= 20
only.

## Dependency

The method depends on the existing certified positive-real `loggamma` Arb-ball
enclosure. The reciprocal-gamma value is obtained by exponentiating the negated
certified `loggamma` enclosure. This is preferable to computing `gamma(x)` and
then inverting it, because `gamma(x)` can be very large.

## Certificate Metadata

The certificate metadata is:

- `certificate_scope="rgamma_positive_real_stirling_recip"`
- `certificate_level="custom_asymptotic_bound"`
- `audit_status="theorem_documented"`
- `selected_method="stirling_recip"`

The runtime result method is `stirling_recip_rgamma`, and the backend is
`certsf+python-flint`.

This active method is explicit only. It is registered only for certified
`rgamma`; it is not selected by `method=None`, `method="auto"`, or default
certified dispatch.

## Error-Bound Contract

The `stirling_recip` method preserves both sources of uncertainty from the
dependent `loggamma` computation:

- the Arb radius from evaluating the finite positive-real `loggamma`
  expression and exponentiating the negated ball; and
- the explicit positive-real Stirling/loggamma tail bound propagated through
  the `exp(-L)` map.

The returned reciprocal-gamma enclosure includes the finite-expression Arb
radius and the propagated loggamma-tail contribution because the loggamma ball
is widened by the explicit tail bound before `exp(-L)` is evaluated.

## Diagnostics

A successful result includes diagnostics equivalent to:

- `selected_method="stirling_recip"`
- `certificate_scope="rgamma_positive_real_stirling_recip"`
- `certificate_level="custom_asymptotic_bound"`
- `audit_status="theorem_documented"`
- `formula="rgamma=exp(-loggamma)"`
- `domain="positive_real_x_ge_20"`
- `loggamma_method_used`
- `loggamma_abs_error_bound`
- `exp_radius`
- `propagated_error_bound`
- `fallback=[]`

Additional diagnostics may identify the underlying loggamma method, term count,
shift, shifted argument, coefficient source, and internal precision.

## Exclusions

The method excludes:

- real `x < 20`;
- real `x <= 0`;
- non-finite input;
- complex `rgamma`;
- reflection formula paths;
- near-pole behavior;
- gamma-ratio asymptotics;
- beta asymptotics;
- default dispatch;
- parabolic-cylinder promotion.

No complex rgamma path is in scope. No reflection formula path is in scope.
No near-pole behavior is in scope. No gamma-ratio asymptotics are in scope.
No beta asymptotics are in scope. No default dispatch change is made.
Parabolic-cylinder wrappers remain `experimental_formula`.

This method does not change `method=None`, `method="auto"`, or default
certified `rgamma` behavior. It does not broaden package-wide, gamma-family-wide,
reciprocal-gamma, gamma-ratio, beta, complex-domain, reflection-formula,
near-pole, or parabolic-cylinder certification claims.
