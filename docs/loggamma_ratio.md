# Loggamma Ratio

`loggamma_ratio(a, b)` returns an `SFResult` for:

```text
principal loggamma(a) - principal loggamma(b)
```

The public signature is:

```python
loggamma_ratio(a, b, *, dps=50, mode="auto", certify=False, method=None)
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
- `mode="certified", method="stirling_diff"` is an explicit positive-real
  method for finite real `a >= 20` and `b >= 20`. It does not replace the
  default direct Arb path.

## Explicit Positive-Real Stirling-Difference Method

The explicit method:

```python
loggamma_ratio(a, b, mode="certified", method="stirling_diff", dps=...)
```

certifies:

```text
loggamma_ratio(a, b) = loggamma(a) - loggamma(b)
```

on finite real `a >= 20` and finite real `b >= 20`. It calls the existing
internal certified positive-real `loggamma` machinery for each argument and
subtracts the resulting Arb balls. Those internal `loggamma` balls already
include the finite Arb radii and the explicit Stirling tail bounds, so the
`loggamma_ratio` method does not add the tail bounds a second time.

Successful results record:

- `method="stirling_diff_loggamma_ratio"`
- `backend="certsf+python-flint"`
- `certificate_scope="loggamma_ratio_positive_real_stirling_diff"`
- `certificate_level="custom_asymptotic_bound"`
- `audit_status="theorem_documented"`
- `selected_method="stirling_diff"`
- `formula="loggamma_ratio=loggamma(a)-loggamma(b)"`
- `domain="positive_real_a_b_ge_20"`

Diagnostics also record the selected internal `loggamma` method for each
argument, each `loggamma` absolute error bound, term counts, tail bounds,
shift metadata when a shifted `loggamma` enclosure is used, and the combined
absolute error bound from the final difference ball.

This method is explicit only. Calls with omitted `method`, `method="auto"`,
or `method="arb"` continue to use the direct Arb certified `loggamma_ratio`
path.

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

The explicit `stirling_diff` method is positive-real only. It rejects complex
inputs, including strings with zero imaginary part such as `"50+0j"`,
non-finite inputs, `a < 20`, and `b < 20` as clean non-certified results. It
does not certify complex gamma-ratio Stirling paths, reflection-formula paths,
near-pole behavior, simultaneous-pole limiting values, `gamma_ratio`
asymptotics, or beta asymptotics.
