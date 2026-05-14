# Gamma Ratio

`gamma_ratio(a, b)` returns an `SFResult` for:

```text
Gamma(a) / Gamma(b)
```

The public signature is:

```python
gamma_ratio(a, b, *, dps=50, mode="auto", certify=False, method=None)
```

## Backend Policy

- `mode="fast"` uses SciPy's `loggamma` path as
  `exp(loggamma(a) - loggamma(b))`.
- `mode="high_precision"` uses the same expression with mpmath.
- `mode="certified"` uses Arb `Gamma(a) * rgamma(b)`.
- `mode="certified", method="stirling_ratio"` uses the explicit
  positive-real path described below.

The certified backend intentionally uses reciprocal gamma rather than
`Gamma(a) / Gamma(b)`. Arb can represent `rgamma(b)` as an exact zero at
non-positive integer gamma poles, so denominator poles can be certified without
introducing a non-finite division.

## Pole Policy

| Case | Certified behavior |
| --- | --- |
| `b` is a gamma pole and `Gamma(a)` is finite | certified zero when Arb returns the zero product |
| `a` is a gamma pole and `b` is finite | clean non-certified failure |
| both `a` and `b` are gamma poles | clean non-certified failure |

Pole-related results include diagnostics such as `pole_case`,
`numerator_pole`, and `denominator_pole`. Certified successes use
`certificate_scope="direct_arb_gamma_ratio"`.

The pole policy is deliberately narrow: the wrapper certifies the Arb product it
evaluates and does not claim a limiting value for simultaneous poles.

## Explicit Positive-Real Stirling-Ratio Method

```python
gamma_ratio(a, b, mode="certified", method="stirling_ratio", dps=...)
```

This explicit method is limited to finite real `a >= 20` and finite real
`b >= 20`. It evaluates

```text
gamma_ratio(a,b) = exp(loggamma_ratio(a,b))
```

by first using the explicit positive-real
`loggamma_ratio(method="stirling_diff")` enclosure and then applying Arb
`exp` to that certified log-ratio ball.

Certified successes record:

- `method="stirling_ratio_gamma_ratio"`
- `backend="certsf+python-flint"`
- `certificate_scope="gamma_ratio_positive_real_stirling_ratio"`
- `certificate_level="custom_asymptotic_bound"`
- `audit_status="theorem_documented"`
- `selected_method="stirling_ratio"`
- `formula="gamma_ratio=exp(loggamma_ratio(a,b))"`
- `domain="positive_real_a_b_ge_20"`

Diagnostics include the internal `loggamma_ratio` method and error bound, the
two underlying `loggamma` method choices and tail/error bounds, any recurrence
shifts used by the loggamma calls, the combined log-ratio bound, and the Arb
`exp` radius. Unsupported inputs return a clean non-certified result with
`value=""` and `fallback=[]`; this explicit method does not fall back to direct
Arb, mpmath, or SciPy.

The method is explicit-only. Omitted `method`, `method="auto"`, and
`method="arb"` continue to use the default direct Arb
`certificate_scope="direct_arb_gamma_ratio"` path in certified mode.

This method does not certify complex gamma-ratio Stirling paths,
reflection-formula paths, near-pole behavior, simultaneous-pole limiting
values, beta asymptotics, or default-dispatch promotion.
