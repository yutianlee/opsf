# erfcinv

`erfcinv(x)` returns an `SFResult` for the real principal inverse of `erfc` on `x in (0, 2)`:

```text
erfc(erfcinv(x)) = x
erfcinv(x) = erfinv(1-x)
```

The public signature is:

```python
erfcinv(x, *, dps=50, mode="auto", certify=False)
```

## Modes

- `mode="fast"` uses `scipy.special.erfcinv(x)`.
- `mode="high_precision"` uses a mpmath inverse when available. Otherwise it
  evaluates the real principal value through `erfinv(1-x)`.
- `mode="certified"` supports real `x` only with `0 < x < 2`.

Certified mode never calls mpmath. It prefers direct Arb `erfcinv` when
python-flint exposes it. If no direct Arb primitive exists, it uses the
existing certified real-inverse path for `erfinv(1-x)`.

Direct Arb successes record:

```text
certificate_scope="direct_arb_erfcinv"
certificate_level="direct_arb_primitive"
audit_status="audited_direct"
domain="real_x_in_open_interval_0_2"
```

The certified fallback records:

```text
certificate_scope="arb_erfcinv_via_erfinv"
certificate_level="certified_real_root"
audit_status="monotone_real_inverse"
domain="real_x_in_open_interval_0_2"
formula="erfinv(1-x)"
```

Inline diagnostics include `certificate_scope="arb_erfcinv_via_erfinv"`,
`certificate_level="certified_real_root"`, and
`audit_status="monotone_real_inverse"` on the certified fallback.

## Certified Domain

Certified mode accepts only finite real `x` with `0 < x < 2`. It rejects
`x <= 0`, `x >= 2`, and complex inputs as clean non-certified failures with
`value=""`.

No complex inverse branches, Faddeeva, plasma dispersion, or endpoint asymptotic certification is part of the
certified `erfcinv` surface.
