# v0.2 Line Audit

Last reviewed: 2026-05-09.

This audit records the v0.2 alpha gamma-family surface and release hygiene
checks after `v0.2.0-alpha.6`.

## Public API

The current gamma-family wrappers are:

- `gamma(z)`
- `loggamma(z)`
- `rgamma(z)`
- `gamma_ratio(a, b)`
- `loggamma_ratio(a, b)`
- `beta(a, b)`
- `pochhammer(a, n)`

All seven wrappers are exported from `certsf.__init__`, appear in
`certsf.__all__`, are registered in the dispatcher with `fast`,
`high_precision`, and `certified` modes, and have thin MCP tools named
`special_<wrapper>`. The MCP tools call the Python wrapper and serialize the
same `SFResult` payload.

No new public wrappers were added by this audit.

## Certified Scope

- `gamma`, `loggamma`, and `rgamma` use direct Arb gamma primitives.
- `gamma_ratio` certifies only the Arb product `Gamma(a) * rgamma(b)`.
- `loggamma_ratio` certifies only the principal-branch Arb difference
  `loggamma(a) - loggamma(b)`.
- `beta` certifies only the Arb product
  `Gamma(a) * Gamma(b) * rgamma(a+b)`.
- `pochhammer` certifies only the finite Arb product
  `prod_{k=0}^{n-1}(a+k)` for exact integer `n >= 0`.

Analytic continuation in `n`, simultaneous-pole limiting values, and
unsupported pole interactions remain outside the certified scope.

## Pole And Domain Policy

The certified gamma-family policy remains intentionally narrow:

- `gamma` and `loggamma` return clean non-certified failures at gamma poles.
- `rgamma` certifies reciprocal-gamma zeros at gamma poles.
- `gamma_ratio` certifies denominator-pole zeros only when `Gamma(a)` is
  finite; numerator poles and simultaneous numerator/denominator poles fail
  cleanly.
- `loggamma_ratio` fails cleanly for poles in either argument.
- `beta` certifies `Gamma(a+b)` denominator-pole zeros only when both numerator
  gamma factors are finite; numerator poles and simultaneous singularities
  fail cleanly.
- `pochhammer` rejects non-integer `n`, negative `n`, product lengths above the
  documented ceiling, and simultaneous-pole quotient limits not covered by the
  finite-product zero-factor case.

Unsupported certified domains return `certified=False` with diagnostics; they
do not silently fall back to mpmath while claiming certification.

## Documentation

The README gamma-family section, dedicated docs for `gamma_ratio`,
`loggamma_ratio`, `beta`, and `pochhammer`, certification audit matrix,
current 0.2 scope document, and release-claim guardrails all describe the same
seven-wrapper surface and the same narrow certified expressions.

External-reference fixtures cover every gamma-family wrapper through
`gamma_reference.json`, `gamma_ratio_reference.json`,
`loggamma_ratio_reference.json`, `beta_reference.json`, and
`pochhammer_reference.json`. These fixtures supplement the recurrence,
identity, and pole-policy tests; they do not broaden any certified claim.

Parabolic-cylinder wrappers remain `experimental_formula`; this audit does not
broaden those claims.

## Release Hygiene

- `publish-pypi.yml` uses `actions/upload-artifact@v6`.
- `publish-testpypi.yml` uses `actions/upload-artifact@v6`.
- Both publish workflows keep `actions/download-artifact@v6`.
- `pypi-smoke.yml` defaults to `0.2.0a6`.
- `pypi-smoke.yml` now covers all seven gamma-family wrappers in Python API
  smoke calls and all seven corresponding MCP tools in MCP smoke calls.
- `pypi-smoke.yml` now covers `erf`, `erfc`, `special_erf`, and
  `special_erfc` after the `v0.2.0-alpha.5` publication.
- `pypi-smoke.yml` now covers `erfcx` and `special_erfcx` after the
  `v0.2.0-alpha.6` publication.

## Audit Findings

The audit found two non-source hygiene gaps:

- `pypi-smoke.yml` did not smoke `loggamma`, `rgamma`, `special_loggamma`, or
  `special_rgamma` even though those wrappers are part of the public
  gamma-family surface.
- `docs/release_claims.md` still introduced the guardrails as applying to the
  `0.1.0` alpha line even though the same guardrails now protect the broader
  `0.x` alpha line.

Both gaps were corrected without source changes, package version changes,
backend formula changes, public-wrapper changes, or certification-claim
broadening.
