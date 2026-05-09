# Error Functions

`erf(z)` returns an `SFResult` for the error function:

```text
erf(z) = 2/sqrt(pi) * integral_0^z exp(-t^2) dt
```

`erfc(z)` returns an `SFResult` for the complementary error function:

```text
erfc(z) = 1 - erf(z)
```

`erfcx(z)` returns an `SFResult` for the scaled complementary error function:

```text
erfcx(z) = exp(z^2) erfc(z)
```

The public signatures are:

```python
erf(z, *, dps=50, mode="auto", certify=False)
erfc(z, *, dps=50, mode="auto", certify=False)
erfcx(z, *, dps=50, mode="auto", certify=False)
```

## Backend Policy

- `mode="fast"` uses `scipy.special.erf(z)`, `scipy.special.erfc(z)`, or
  `scipy.special.erfcx(z)`.
- `mode="high_precision"` uses `mpmath.erf(z)`, `mpmath.erfc(z)`, or
  `mpmath.exp(z*z) * mpmath.erfc(z)`.
- `mode="certified"` uses direct Arb `erf` and `erfc` primitives through
  `python-flint` where available. Certified `erfcx` prefers direct Arb `erfcx`
  when available; otherwise it evaluates the Arb ball formula
  `exp(z^2)*erfc(z)`.

Certified `erfc` uses the direct Arb `erfc` primitive when available. If a
supported `python-flint` build exposes direct `erf` but not direct `erfc`, the
certified backend may evaluate `1 - erf(z)` with Arb ball arithmetic and must
record `diagnostics["formula"] == "1-erf"`.

Certified `erfcx` uses `certificate_scope="direct_arb_erfcx"` if a direct Arb
primitive is exposed. The formula fallback uses
`certificate_scope="arb_erfcx_formula"`,
`certificate_level="formula_audited_alpha"`, `audit_status="formula_identity"`,
and records `diagnostics["formula"] == "exp(z^2)*erfc(z)"`.

## Certified Domain

Certified mode supports real and complex inputs when Arb returns a finite
enclosure for the target value. Unsupported inputs or non-finite returned
enclosures produce clean non-certified failures with `value=""`.

No Taylor, asymptotic, or custom certification method is added for these
wrappers. Certified successes use narrow scopes:

- `erf`: `certificate_scope="direct_arb_erf"`
- `erfc`: `certificate_scope="direct_arb_erfc"`
- `erfcx`: `certificate_scope="direct_arb_erfcx"` or
  `certificate_scope="arb_erfcx_formula"`

The wrapper does not add other public error-function variants such as `erfi`,
`erfinv`, `erfcinv`, or Faddeeva functions. It does not claim large-argument
scaled-erfc stability beyond the Arb or SciPy/mpmath backend behavior used for
the selected mode.
