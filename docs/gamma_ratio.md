# Gamma Ratio

`gamma_ratio(a, b)` returns an `SFResult` for:

```text
Gamma(a) / Gamma(b)
```

The public signature is:

```python
gamma_ratio(a, b, *, dps=50, mode="auto", certify=False)
```

## Backend Policy

- `mode="fast"` uses SciPy's `loggamma` path as
  `exp(loggamma(a) - loggamma(b))`.
- `mode="high_precision"` uses the same expression with mpmath.
- `mode="certified"` uses Arb `Gamma(a) * rgamma(b)`.

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
