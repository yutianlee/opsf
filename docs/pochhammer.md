# Pochhammer Symbol

`pochhammer(a, n)` returns an `SFResult` for the rising factorial:

```text
(a)_n = Gamma(a+n) / Gamma(a)
```

For nonnegative integer `n`, this is evaluated in certified mode as the finite
product:

```text
(a)_n = product_{k=0}^{n-1} (a+k)
```

The public signature is:

```python
pochhammer(a, n, *, dps=50, mode="auto", certify=False)
```

## Backend Policy

- `mode="fast"` uses `scipy.special.poch(a,n)` where SciPy supports the input,
  with a double-precision finite-product fallback for complex `a` and
  nonnegative integer `n`.
- `mode="high_precision"` uses `mpmath.rf(a,n)`.
- `mode="certified"` uses Arb ball arithmetic for the finite product only when
  `n` is an exact integer with `n >= 0`.

The certified path intentionally avoids evaluating the defining gamma quotient.
This keeps gamma-pole ambiguity out of the supported path for this PR.

## Certified Domain

| Case | Certified behavior |
| --- | --- |
| `n = 0` | certified `1` |
| integer `n > 0`, no excluded pole case | certified finite-product enclosure |
| an exact zero factor `a+k = 0` | certified zero |
| non-integer `n` | clean non-certified failure |
| negative integer `n` | clean non-certified failure |
| simultaneous gamma-pole quotient limit | clean non-certified failure |
| `n > 10000` | clean non-certified failure |

The finite-product ceiling is deliberately conservative. There is no gamma
quotient fallback in certified mode yet.

Certified results use `certificate_scope="direct_arb_pochhammer_product"` and
`certificate_level="direct_arb_finite_product"`. They certify only the
documented finite product for nonnegative integer `n`; they do not claim
analytic continuation in `n` or unproven simultaneous-pole limiting values.
