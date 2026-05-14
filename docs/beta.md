# Beta Function

`beta(a, b)` returns an `SFResult` for the Euler beta function:

```text
B(a,b) = Gamma(a) Gamma(b) / Gamma(a+b)
```

The public signature is:

```python
beta(a, b, *, dps=50, mode="auto", certify=False, method=None)
```

## Backend Policy

- `mode="fast"` uses `scipy.special.beta(a,b)` when available, otherwise
  `exp(loggamma(a) + loggamma(b) - loggamma(a+b))`.
- `mode="high_precision"` uses `mpmath.beta(a,b)` when available, otherwise
  the same loggamma expression with mpmath.
- `mode="certified"` uses Arb `Gamma(a) * Gamma(b) * rgamma(a+b)`.
- `mode="certified", method="stirling_beta"` uses the explicit positive-real
  path described below.

The certified backend intentionally uses reciprocal gamma for the denominator.
Arb can represent `rgamma(a+b)` as an exact zero at non-positive integer gamma
poles, so denominator poles can be certified without introducing a non-finite
division when the two numerator gamma factors are finite.

## Pole Policy

| Case | Certified behavior |
| --- | --- |
| `a+b` is a gamma pole while `Gamma(a)` and `Gamma(b)` are finite | certified zero when Arb returns the zero product |
| `a` is a gamma pole | clean non-certified failure |
| `b` is a gamma pole | clean non-certified failure |
| numerator pole with denominator pole, or other simultaneous pole interaction | clean non-certified failure |

Pole-related results include diagnostics such as `pole_case`, `a_pole`,
`b_pole`, `sum_pole`, and `certificate_scope="direct_arb_beta"`.

The pole policy is deliberately narrow: the wrapper certifies the Arb product it
evaluates and does not claim a limiting value at simultaneous singularities.

## Explicit Positive-Real Stirling-Beta Method

```python
beta(a, b, mode="certified", method="stirling_beta", dps=...)
```

This explicit method is limited to finite real `a >= 20` and finite real
`b >= 20`. It evaluates

```text
beta(a,b) = exp(loggamma(a)+loggamma(b)-loggamma(a+b))
```

using three certified positive-real `loggamma` Arb enclosures. Each internal
`loggamma` ball already includes its finite-expression Arb radius and explicit
Stirling tail bound, so the log-beta ball carries all three contributions
before Arb `exp` is applied.

Certified successes record:

- `method="stirling_beta_beta"`
- `backend="certsf+python-flint"`
- `certificate_scope="beta_positive_real_stirling_beta"`
- `certificate_level="custom_asymptotic_bound"`
- `audit_status="theorem_documented"`
- `selected_method="stirling_beta"`
- `formula="beta=exp(loggamma(a)+loggamma(b)-loggamma(a+b))"`
- `domain="positive_real_a_b_ge_20"`

Diagnostics include the three internal `loggamma` method choices and
tail/error bounds, any recurrence shifts used by those loggamma calls, the
combined log-beta bound, and the Arb `exp` radius. Unsupported inputs return a
clean non-certified result with `value=""` and `fallback=[]`; this explicit
method does not fall back to direct Arb, mpmath, or SciPy.

The method is explicit-only. Omitted `method`, `method="auto"`, and
`method="arb"` continue to use the default direct Arb
`certificate_scope="direct_arb_beta"` path in certified mode.

This method does not certify complex beta Stirling paths, reflection-formula
paths, near-pole behavior, simultaneous-pole limiting values, or
default-dispatch promotion.
