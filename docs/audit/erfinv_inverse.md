# erfinv Inverse-Function Audit

Last reviewed: 2026-05-10.

This audit covers only the public inverse-error wrapper `erfinv(x)`. It does
not add `erfcinv`, complex inverse branches, Faddeeva/`wofz`, plasma
dispersion, or endpoint asymptotic certification.

## Public Surface

`erfinv` is exported from `certsf.__init__`, appears in `certsf.__all__`, is
registered in the dispatcher with `fast`, `high_precision`, and `certified`
modes, and is exposed through the thin MCP tool `special_erfinv`.

The mathematical branch is the real principal inverse of `erf`:

```text
erf(erfinv(x)) = x, for real -1 < x < 1
```

## Backend Modes

- `mode="fast"` uses `scipy.special.erfinv(x)`.
- `mode="high_precision"` uses `mpmath.erfinv(x)` when available and otherwise
  solves `erf(y) = x` numerically.
- `mode="certified"` never calls mpmath. It supports only real `x` with
  `-1 < x < 1`.

## Certified Diagnostics

When direct Arb `erfinv` is exposed by python-flint, certified successes record:

```text
certificate_scope="direct_arb_erfinv"
certificate_level="direct_arb_primitive"
audit_status="audited_direct"
domain="real_x_in_open_interval_minus1_1"
```

When the direct primitive is unavailable, certified successes use the monotone
real-root fallback for `erf(y)-x=0` and record:

```text
certificate_scope="arb_erfinv_real_root"
certificate_level="certified_real_root"
audit_status="monotone_real_inverse"
domain="real_x_in_open_interval_minus1_1"
formula="erf(y)-x=0"
```

## Domain Rejections

Certified mode rejects `x = -1`, `x = 1`, real `x < -1`, real `x > 1`, and
complex inputs as clean non-certified failures. Unsupported certified domains
return `certified=False` with diagnostics and never fall back to mpmath while
claiming certification.

## Audit Evidence

Tests cover `erfinv(0) = 0`, composition through `erf(erfinv(x))`, oddness,
near-endpoint in-domain values, endpoint and out-of-domain rejection, complex
input rejection, direct-or-real-root certificate scopes, real-root fallback
diagnostics, residual containment, external-reference fixture containment,
Python API/MCP parity, and pypi-smoke base/certified/MCP coverage.

This audit corrected stale pre-publication documentation that still described
`erfinv(x)` as future alpha.9 work and still described pypi-smoke as excluding
`erfinv`. The public API, dispatcher, backend, MCP wrapper, certification
diagnostics, and release workflow were already consistent with the published
`0.2.0a9` surface.

No public-wrapper, backend-formula, package-version, gamma-family, existing
error-function behavior, or parabolic-cylinder claim change is part of this
audit.
