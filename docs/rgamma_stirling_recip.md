# Planned Positive-Real `rgamma` via Certified Loggamma Exponentiation

This document records a planning-only future method for positive-real
reciprocal gamma. It is not active, is not registered, does not change default
dispatch, and does not add a public wrapper.

The future explicit method name is:

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

Equivalently for diagnostics, the planned formula string is
`formula="rgamma=exp(-loggamma)"`.

The planned domain is finite real `x >= 20`. This means finite real x >= 20
only.

## Dependency

The planned method depends on the existing certified positive-real `loggamma`
Arb-ball enclosure. The reciprocal-gamma value should be obtained by
exponentiating the negated certified `loggamma` enclosure. This is preferable
to computing `gamma(x)` and then inverting it, because `gamma(x)` can be very
large.

## Planned Certificate Metadata

The planned certificate metadata is:

- `certificate_scope="rgamma_positive_real_stirling_recip"`
- `certificate_level="custom_asymptotic_bound"`
- `audit_status="theorem_documented"`
- `selected_method="stirling_recip"`

The planned runtime result method is `stirling_recip_rgamma`, and the planned
backend is `certsf+python-flint`.

These are planning notes only. No runtime implementation or registry entry is
active in this PR.

## Planned Error-Bound Contract

The future `stirling_recip` method should preserve both sources of
uncertainty from the dependent `loggamma` computation:

- the Arb radius from evaluating the finite positive-real `loggamma`
  expression and exponentiating the negated ball; and
- the explicit positive-real Stirling/loggamma tail bound propagated through
  the `exp(-L)` map.

The returned reciprocal-gamma enclosure should include the finite-expression
Arb radius and the propagated loggamma-tail contribution.

## Planned Diagnostics

A successful future result is expected to include diagnostics equivalent to:

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

The plan excludes:

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
No beta asymptotics are in scope. No default dispatch change is planned.
Parabolic-cylinder wrappers remain `experimental_formula`.

This plan does not change `method=None`, `method="auto"`, or default certified
`rgamma` behavior. It does not broaden package-wide, gamma-family-wide,
reciprocal-gamma, gamma-ratio, beta, complex-domain, reflection-formula,
near-pole, or parabolic-cylinder certification claims.
