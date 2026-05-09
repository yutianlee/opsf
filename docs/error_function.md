# Error Functions

`erf(z)` returns an `SFResult` for the error function:

```text
erf(z) = 2/sqrt(pi) * integral_0^z exp(-t^2) dt
```

`erfc(z)` returns an `SFResult` for the complementary error function:

```text
erfc(z) = 1 - erf(z)
```

The public signatures are:

```python
erf(z, *, dps=50, mode="auto", certify=False)
erfc(z, *, dps=50, mode="auto", certify=False)
```

## Backend Policy

- `mode="fast"` uses `scipy.special.erf(z)` or `scipy.special.erfc(z)`.
- `mode="high_precision"` uses `mpmath.erf(z)` or `mpmath.erfc(z)`.
- `mode="certified"` uses direct Arb `erf` and `erfc` primitives through
  `python-flint` where available.

Certified `erfc` uses the direct Arb `erfc` primitive when available. If a
supported `python-flint` build exposes direct `erf` but not direct `erfc`, the
certified backend may evaluate `1 - erf(z)` with Arb ball arithmetic and must
record `diagnostics["formula"] == "1-erf"`.

## Certified Domain

Certified mode supports real and complex inputs when Arb returns a finite
enclosure for the target value. Unsupported inputs or non-finite returned
enclosures produce clean non-certified failures with `value=""`.

No Taylor, asymptotic, or custom certification method is added for these
wrappers. Certified successes use narrow scopes:

- `erf`: `certificate_scope="direct_arb_erf"`
- `erfc`: `certificate_scope="direct_arb_erfc"`

The wrapper does not add other public error-function variants such as `erfi`, `erfinv`, `erfcinv`, or `erfcx`.
