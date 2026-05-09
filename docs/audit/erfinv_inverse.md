# Inverse Error-Function Audit

Last reviewed: 2026-05-10.

This audit covers the public inverse-error wrappers `erfinv(x)` and
`erfcinv(x)`. It does not add public wrappers, complex inverse branches,
Faddeeva/`wofz`, plasma dispersion, or endpoint asymptotic certification.

## Public Surface

`erfinv` and `erfcinv` are exported from `certsf.__init__`, appear in
`certsf.__all__`, are registered in the dispatcher with `fast`,
`high_precision`, and `certified` modes, and are exposed through the thin MCP
tools `special_erfinv` and `special_erfcinv`.

The mathematical branch for `erfinv` is the real principal inverse of `erf`:

```text
erf(erfinv(x)) = x, for real -1 < x < 1
```

The mathematical branch for `erfcinv` is the real principal inverse of `erfc`:

```text
erfc(erfcinv(x)) = x, for real 0 < x < 2
erfcinv(x) = erfinv(1-x)
```

## Backend Modes

- `mode="fast"` uses `scipy.special.erfinv(x)`.
- `mode="high_precision"` uses `mpmath.erfinv(x)` when available and otherwise
  solves `erf(y) = x` numerically.
- `mode="fast"` for `erfcinv` uses `scipy.special.erfcinv(x)`.
- `mode="high_precision"` for `erfcinv` uses a mpmath inverse when available
  and otherwise evaluates the real principal value through `erfinv(1-x)`.
- `mode="certified"` never calls mpmath. Certified `erfinv` supports only real
  `x` with `-1 < x < 1`. Certified `erfcinv` supports only real `x` with
  `0 < x < 2`.

## Certified Diagnostics

When direct Arb `erfinv` is exposed by python-flint, certified `erfinv`
successes record:

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

When direct Arb `erfcinv` is exposed by python-flint, certified `erfcinv`
successes record:

```text
certificate_scope="direct_arb_erfcinv"
certificate_level="direct_arb_primitive"
audit_status="audited_direct"
domain="real_x_in_open_interval_0_2"
```

When the direct `erfcinv` primitive is unavailable, certified successes use the
existing certified real-inverse path for `erfinv(1-x)` and record:

```text
certificate_scope="arb_erfcinv_via_erfinv"
certificate_level="certified_real_root"
audit_status="monotone_real_inverse"
domain="real_x_in_open_interval_0_2"
formula="erfinv(1-x)"
```

## Domain Rejections

Certified mode rejects `x = -1`, `x = 1`, real `x < -1`, real `x > 1`, and
complex inputs for `erfinv` as clean non-certified failures. It rejects
`x = 0`, `x = 2`, real `x < 0`, real `x > 2`, and complex inputs for
`erfcinv` as clean non-certified failures. Unsupported certified domains return
`certified=False` with diagnostics and never fall back to mpmath while claiming
certification.

## Audit Evidence

Tests cover `erfinv(0) = 0`, composition through `erf(erfinv(x))`, oddness,
near-endpoint in-domain values, endpoint and out-of-domain rejection, complex
input rejection, direct-or-real-root certificate scopes, real-root fallback
diagnostics, residual containment, external-reference fixture containment, and
Python API/MCP parity. Tests also cover `erfcinv(1) = 0`, composition through
`erfc(erfcinv(x))`, the relation `erfcinv(x) = erfinv(1-x)`, monotonic
orientation, near-endpoint in-domain values, endpoint and out-of-domain
rejection, complex input rejection, direct-or-`erfinv(1-x)` certificate scopes,
fallback diagnostics, residual containment, external-reference fixture
containment, and Python API/MCP parity.

The release-hygiene audit checks that `pypi-smoke.yml` defaults to `0.2.0a10`
and covers `erfinv`, `erfcinv`, `special_erfinv`, and `special_erfcinv` in the
base, certified, and MCP-certified smoke paths.

This audit corrected stale documentation that still described `erfcinv(x)` as
future alpha.10 work after `0.2.0a10` was published. The public API,
dispatcher, backend, MCP wrappers, certification diagnostics, and release
workflow are consistent with the published `0.2.0a10` surface.

No public-wrapper, backend-formula, package-version, gamma-family, existing
error-function behavior, or parabolic-cylinder claim change is part of this
audit.
