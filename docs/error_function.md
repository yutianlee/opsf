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

`erfi(z)` returns an `SFResult` for the imaginary error function:

```text
erfi(z) = -i erf(i z)
```

`dawson(z)` returns an `SFResult` for Dawson's integral:

```text
dawson(z) = sqrt(pi)/2 * exp(-z^2) * erfi(z)
```

`erfinv(x)` returns an `SFResult` for the real principal inverse error
function:

```text
erf(erfinv(x)) = x for real -1 < x < 1
```

The public signatures are:

```python
erf(z, *, dps=50, mode="auto", certify=False)
erfc(z, *, dps=50, mode="auto", certify=False)
erfcx(z, *, dps=50, mode="auto", certify=False)
erfi(z, *, dps=50, mode="auto", certify=False)
dawson(z, *, dps=50, mode="auto", certify=False)
erfinv(x, *, dps=50, mode="auto", certify=False)
```

## Backend Policy

- `mode="fast"` uses `scipy.special.erf(z)`, `scipy.special.erfc(z)`, or
  `scipy.special.erfcx(z)`. For `erfi`, it uses `scipy.special.erfi(z)` when
  available and otherwise evaluates `-1j * scipy.special.erf(1j*z)`.
  For `dawson`, it uses `scipy.special.dawsn(z)` when available and otherwise
  evaluates `sqrt(pi)/2 * exp(-z*z) * scipy.special.erfi(z)`.
  For `erfinv`, it uses `scipy.special.erfinv(x)`.
- `mode="high_precision"` uses `mpmath.erf(z)`, `mpmath.erfc(z)`, or
  `mpmath.exp(z*z) * mpmath.erfc(z)`. For `erfi`, it uses `mpmath.erfi(z)`
  when available and otherwise evaluates `-i*mpmath.erf(i*z)`. For `dawson`,
  it uses a mpmath Dawson function when available and otherwise evaluates
  `sqrt(pi)/2 * exp(-z*z) * erfi(z)`. For `erfinv`, it uses
  `mpmath.erfinv(x)` when available and otherwise solves `erf(y) = x`
  numerically.
- `mode="certified"` uses direct Arb `erf` and `erfc` primitives through
  `python-flint` where available. Certified `erfcx` prefers direct Arb `erfcx`
  when available; otherwise it evaluates the Arb ball formula
  `exp(z^2)*erfc(z)`. Certified `erfi` prefers direct Arb `erfi` when
  available; otherwise it evaluates the Arb ball formula `-i*erf(i*z)`.
  Certified `dawson` prefers direct Arb `dawson` when available; otherwise it
  evaluates the Arb ball formula `sqrt(pi)/2*exp(-z^2)*erfi(z)`. Certified
  `erfinv` supports only real `x` with `-1 < x < 1`; it prefers direct Arb
  `erfinv` when available and otherwise uses a certified monotone real-root
  enclosure for `erf(y)-x=0`.

Certified `erfc` uses the direct Arb `erfc` primitive when available. If a
supported `python-flint` build exposes direct `erf` but not direct `erfc`, the
certified backend may evaluate `1 - erf(z)` with Arb ball arithmetic and must
record `diagnostics["formula"] == "1-erf"`.

Certified `erfcx` uses `certificate_scope="direct_arb_erfcx"` if a direct Arb
primitive is exposed. The formula fallback uses
`certificate_scope="arb_erfcx_formula"`,
`certificate_level="formula_audited_alpha"`, `audit_status="formula_identity"`,
and records `diagnostics["formula"] == "exp(z^2)*erfc(z)"`.

Certified `erfi` uses `certificate_scope="direct_arb_erfi"` if a direct Arb
primitive is exposed. The formula fallback uses
`certificate_scope="arb_erfi_formula"`,
`certificate_level="formula_audited_alpha"`, `audit_status="formula_identity"`,
and records `diagnostics["formula"] == "-i*erf(i*z)"`.

Certified `dawson` uses `certificate_scope="direct_arb_dawson"` if a direct Arb
primitive is exposed. The formula fallback uses
`certificate_scope="arb_dawson_formula"`,
`certificate_level="formula_audited_alpha"`, `audit_status="formula_identity"`,
`certification_claim="certified Arb enclosure of sqrt(pi)/2*exp(-z^2)*erfi(z)"`,
and records `diagnostics["formula"] == "sqrt(pi)/2*exp(-z^2)*erfi(z)"`.

Certified `erfinv` uses `certificate_scope="direct_arb_erfinv"` if a direct Arb
primitive is exposed. If no direct primitive is exposed, the real-root fallback
uses `certificate_scope="arb_erfinv_real_root"`,
`certificate_level="certified_real_root"`,
`audit_status="monotone_real_inverse"`,
`certification_claim="certified real root enclosure for erf(y)-x=0 using monotonicity of real erf"`,
`diagnostics["formula"] == "erf(y)-x=0"`, and
`diagnostics["domain"] == "real_x_in_open_interval_minus1_1"`.

## Certified Domain

Certified `erf`, `erfc`, `erfcx`, `erfi`, and `dawson` support real and complex
inputs when Arb returns a finite enclosure for the target value. Certified
`erfinv` is intentionally narrower: it supports only the real principal inverse
on `x in (-1, 1)`. It rejects `x <= -1`, `x >= 1`, and complex inputs as clean
non-certified failures with `value=""`. This PR does not claim complex inverse
branches or endpoint asymptotic certification.

No Taylor or asymptotic certification method is added for these wrappers.
Certified successes use narrow scopes:

- `erf`: `certificate_scope="direct_arb_erf"`
- `erfc`: `certificate_scope="direct_arb_erfc"`
- `erfcx`: `certificate_scope="direct_arb_erfcx"` or
  `certificate_scope="arb_erfcx_formula"`
- `erfi`: `certificate_scope="direct_arb_erfi"` or
  `certificate_scope="arb_erfi_formula"`
- `dawson`: `certificate_scope="direct_arb_dawson"` or
  `certificate_scope="arb_dawson_formula"`
- `erfinv`: `certificate_scope="direct_arb_erfinv"` or
  `certificate_scope="arb_erfinv_real_root"`

The wrapper does not add other public error-function variants such as
`erfcinv` or Faddeeva functions. It does not claim large-argument scaled-erfc
stability beyond the Arb or SciPy/mpmath backend behavior used for the selected
mode.
