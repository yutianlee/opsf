# Loggamma Ratio

`loggamma_ratio(a, b)` returns an `SFResult` for:

```text
principal loggamma(a) - principal loggamma(b)
```

The public signature is:

```python
loggamma_ratio(a, b, *, dps=50, mode="auto", certify=False)
```

## Branch Policy

`loggamma_ratio(a, b)` is defined as the difference of two principal
`loggamma` values. For complex inputs, this is not necessarily the same value
as the principal logarithm of `gamma_ratio(a, b)` or of `Gamma(a) / Gamma(b)`.

## Backend Policy

- `mode="fast"` uses SciPy as
  `scipy.special.loggamma(a) - scipy.special.loggamma(b)`.
- `mode="high_precision"` uses the same principal-branch expression with
  mpmath.
- `mode="certified"` uses Arb `lgamma(a) - lgamma(b)`.

## Pole Policy

| Case | Certified behavior |
| --- | --- |
| `a` is a gamma pole and `b` is finite | clean non-certified failure |
| `b` is a gamma pole and `a` is finite | clean non-certified failure |
| both `a` and `b` are gamma poles | clean non-certified failure |

Pole-related failures include diagnostics such as `pole_case`,
`numerator_pole`, `denominator_pole`, and
`certificate_scope="direct_arb_loggamma_ratio"`.

The pole policy is deliberately narrow: the wrapper certifies the Arb
principal-loggamma difference it evaluates and does not claim simultaneous-pole
limiting values.
