# Inverse Error Function

`erfinv(x)` returns an `SFResult` for the real principal inverse of `erf` on `x in (-1, 1)`:

```text
erf(erfinv(x)) = x
```

The public signature is:

```python
erfinv(x, *, dps=50, mode="auto", certify=False)
```

## Backend Policy

- `mode="fast"` uses `scipy.special.erfinv(x)`.
- `mode="high_precision"` uses `mpmath.erfinv(x)` when available and otherwise
  solves `erf(y) = x` numerically.
- `mode="certified"` supports real `x` only, with `-1 < x < 1`. It rejects
  endpoints, out-of-interval values, and complex inputs as clean non-certified
  failures.

Certified mode never calls mpmath. It prefers direct Arb `erfinv` when
`python-flint` exposes it. If no direct primitive is exposed, it uses Arb ball
arithmetic to bracket the unique real root of `erf(y)-x=0`, exploiting
monotonicity of real `erf`, and refines the bracket until the output ball
certifies the requested precision.

Direct Arb successes use:

```text
certificate_scope="direct_arb_erfinv"
certificate_level="direct_arb_primitive"
audit_status="audited_direct"
domain="real_x_in_open_interval_minus1_1"
```

Real-root fallback successes use:

```text
certificate_scope="arb_erfinv_real_root"
certificate_level="certified_real_root"
audit_status="monotone_real_inverse"
domain="real_x_in_open_interval_minus1_1"
```

and record `diagnostics["formula"] == "erf(y)-x=0"`.

Inline diagnostics include `certificate_scope="arb_erfinv_real_root"`,
`certificate_level="certified_real_root"`, and
`audit_status="monotone_real_inverse"` on the certified real-root fallback.

## Guardrails

This wrapper adds only the real principal inverse branch for `erfinv`. No complex
inverse branches, Faddeeva, plasma dispersion, or endpoint asymptotic
certification is part of the certified `erfinv` surface.
