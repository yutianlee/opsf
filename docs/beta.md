# Beta Function

`beta(a, b)` returns an `SFResult` for the Euler beta function:

```text
B(a,b) = Gamma(a) Gamma(b) / Gamma(a+b)
```

The public signature is:

```python
beta(a, b, *, dps=50, mode="auto", certify=False)
```

## Backend Policy

- `mode="fast"` uses `scipy.special.beta(a,b)` when available, otherwise
  `exp(loggamma(a) + loggamma(b) - loggamma(a+b))`.
- `mode="high_precision"` uses `mpmath.beta(a,b)` when available, otherwise
  the same loggamma expression with mpmath.
- `mode="certified"` uses Arb `Gamma(a) * Gamma(b) * rgamma(a+b)`.

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
