# Dawson Integral

`dawson(z)` returns an `SFResult` for Dawson's integral:

```text
dawson(z) = sqrt(pi)/2 * exp(-z^2) * erfi(z)
```

The public signature is:

```python
dawson(z, *, dps=50, mode="auto", certify=False)
```

## Backend Policy

- `mode="fast"` uses `scipy.special.dawsn(z)` when available. If SciPy does
  not expose `dawsn`, it evaluates
  `sqrt(pi)/2 * exp(-z*z) * scipy.special.erfi(z)`.
- `mode="high_precision"` uses a mpmath Dawson function when available. If
  mpmath does not expose one, it evaluates
  `sqrt(pi)/2 * exp(-z*z) * erfi(z)`.
- `mode="certified"` uses a direct Arb `dawson` primitive when available.
  Otherwise it evaluates the Arb ball formula
  `sqrt(pi)/2*exp(-z^2)*erfi(z)`.

## Certified Domain

Certified mode supports real and complex inputs only when Arb returns a finite
enclosure. Unsupported inputs and non-finite output enclosures return clean
non-certified failures with `value=""`; certified mode does not call mpmath.

Direct Arb primitive results use:

```text
certificate_scope="direct_arb_dawson"
certificate_level="direct_arb_primitive"
audit_status="audited_direct"
```

The formula fallback uses:

```text
certificate_scope="arb_dawson_formula"
certificate_level="formula_audited_alpha"
audit_status="formula_identity"
certification_claim="certified Arb enclosure of sqrt(pi)/2*exp(-z^2)*erfi(z)"
```

In prose form, the formula fallback is identified by
`certificate_scope="arb_dawson_formula"` and
`certification_claim="certified Arb enclosure of sqrt(pi)/2*exp(-z^2)*erfi(z)"`.

and records:

```text
diagnostics["formula"] == "sqrt(pi)/2*exp(-z^2)*erfi(z)"
```

The same runtime diagnostic is checked as
`diagnostics["formula"] == "sqrt(pi)/2*exp(-z^2)*erfi(z)"`.

No asymptotic custom certification, Faddeeva wrapper, plasma dispersion
wrapper, or inverse error-function variant is added by `dawson(z)`.
