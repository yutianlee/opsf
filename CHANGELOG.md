# Changelog

## Unreleased

- Added the public `erfinv(x)` wrapper for the real principal inverse of `erf`
  on `-1 < x < 1`.
- Fast mode uses `scipy.special.erfinv(x)`.
- High-precision mode uses `mpmath.erfinv(x)` when available and otherwise
  solves `erf(y) = x` numerically.
- Certified mode supports real `x` only with `-1 < x < 1`, prefers direct Arb
  `erfinv` when available, and otherwise uses a certified monotone real-root
  enclosure for `erf(y)-x=0`.
- No `erfcinv`, complex inverse branches, Faddeeva functions, plasma
  dispersion wrapper, `wofz`, or endpoint asymptotic certification is added.
- No `erf`, `erfc`, `erfcx`, `erfi`, or `dawson` behavior changes are included.
- No gamma-family behavior changes are included.
- No parabolic-cylinder claim broadening is included; those wrappers remain
  `experimental_formula`.
- `pypi-smoke.yml` remains pinned to `0.2.0a8` for this feature PR.

## 0.2.0-alpha.8 - 2026-05-09

- Added the public `dawson(z)` wrapper.
- Defined `dawson(z)` as `sqrt(pi)/2 * exp(-z^2) * erfi(z)`.
- Fast mode uses `scipy.special.dawsn(z)` when available; otherwise it uses
  the `erfi` identity fallback.
- High-precision mode uses a mpmath Dawson function when available; otherwise
  it uses the `erfi` identity fallback.
- Certified mode prefers direct Arb Dawson when available; otherwise it uses
  the Arb formula `sqrt(pi)/2*exp(-z^2)*erfi(z)` with formula diagnostics.
- No inverse error functions, Faddeeva functions, plasma dispersion wrapper, or
  additional variants are added.
- No `erf`, `erfc`, `erfcx`, or `erfi` behavior changes are included.
- No gamma-family behavior changes are included.
- No parabolic-cylinder claim broadening is included; those wrappers remain
  `experimental_formula`.

## 0.2.0-alpha.7 - 2026-05-09

- Added the public `erfi(z)` wrapper.
- Defined `erfi(z)` as `-i erf(i z)`.
- Fast mode uses `scipy.special.erfi(z)` when available; otherwise it uses the
  formula fallback `-1j * scipy.special.erf(1j*z)`.
- High-precision mode uses `mpmath.erfi(z)` when available; otherwise it uses
  the formula fallback `-i*mpmath.erf(i*z)`.
- Certified mode prefers direct Arb `erfi` when available; otherwise it uses
  the Arb formula `-i*erf(i*z)` with formula diagnostics.
- No `erfinv`, `erfcinv`, Faddeeva, Dawson, or other error-function variants
  are added.
- No `erf`, `erfc`, or `erfcx` behavior changes are included.
- No gamma-family behavior changes are included.
- No parabolic-cylinder claim broadening is included; those wrappers remain
  `experimental_formula`.

## 0.2.0-alpha.6 - 2026-05-09

- Added the public `erfcx(z)` wrapper.
- Defined `erfcx(z)` as `exp(z^2) erfc(z)`.
- Fast mode uses `scipy.special.erfcx(z)`.
- High-precision mode uses `mpmath` evaluation of `exp(z*z) * erfc(z)`.
- Certified mode prefers direct Arb `erfcx` when available; otherwise it uses
  the Arb formula `exp(z^2)*erfc(z)` with formula diagnostics.
- No `erfi`, `erfinv`, `erfcinv`, or Faddeeva wrappers are added.
- No `erf` or `erfc` behavior changes are included.
- No gamma-family behavior changes are included.
- No parabolic-cylinder claim broadening is included; those wrappers remain
  `experimental_formula`.

## 0.2.0-alpha.5 - 2026-05-09

- Added the public `erf(z)` and `erfc(z)` wrappers as the only public API
  expansions since `0.2.0-alpha.4`.
- Added SciPy, mpmath, and Arb backends for `erf` and `erfc`.
- Certified `erf` uses the direct Arb `erf` primitive in the
  `direct_arb_erf` scope.
- Certified `erfc` uses the direct Arb `erfc` primitive when available in the
  `direct_arb_erfc` scope, with the documented Arb fallback `1 - erf(z)` only
  if direct `erfc` is unavailable.
- Added the MCP tools `special_erf` and `special_erfc`.
- Added external fixtures and certified identity tests for error-function
  behavior.
- No gamma-family behavior changes are included.
- No parabolic-cylinder claim broadening is included; those wrappers remain
  `experimental_formula`.

## 0.2.0-alpha.4 - 2026-05-09

- Added the public `pochhammer(a, n)` wrapper as the only public API expansion
  since `0.2.0-alpha.3`.
- Defined `pochhammer(a, n)` as the rising factorial `(a)_n`.
- Certified mode supports exact integer `n >= 0` only.
- Certified mode uses the Arb finite product `prod_{k=0}^{n-1}(a+k)` in the
  `direct_arb_pochhammer_product` scope.
- `n = 0` returns certified `1`.
- Exact zero factors return certified zero.
- Non-integer `n`, negative `n`, oversized product paths, and simultaneous
  gamma-pole limiting values fail cleanly.
- Added the MCP tool `special_pochhammer`.
- Added external fixtures and certified recurrence tests for Pochhammer
  behavior.
- No `beta`, `gamma_ratio`, or `loggamma_ratio` behavior changes are included.
- No parabolic-cylinder claim broadening is included; those wrappers remain
  `experimental_formula`.

## 0.2.0-alpha.3 - 2026-05-09

- Added the public `beta(a, b)` wrapper as the only public API expansion since
  `0.2.0-alpha.2`.
- Defined `beta(a, b)` as `Gamma(a) Gamma(b) / Gamma(a+b)`.
- Added SciPy, mpmath, and Arb backends for `beta`.
- Certified `beta` uses Arb `Gamma(a) * Gamma(b) * rgamma(a+b)` in the
  `direct_arb_beta` scope.
- Sum-pole denominator zeros certify when `Gamma(a)` and `Gamma(b)` are finite.
- Numerator poles and simultaneous singularities fail cleanly.
- Added the MCP tool `special_beta`.
- Added external fixtures and certified identity tests for beta behavior.
- No `gamma_ratio` or `loggamma_ratio` behavior changes are included.
- No parabolic-cylinder claim broadening is included; those wrappers remain
  `experimental_formula`.

## 0.2.0-alpha.2 - 2026-05-09

- Added the public `loggamma_ratio(a, b)` wrapper as the only public API
  expansion since `0.2.0-alpha.1`.
- Defined `loggamma_ratio(a, b)` as principal `loggamma(a) - loggamma(b)`;
  for complex inputs, this is not necessarily principal
  `log(gamma_ratio(a, b))`.
- Added SciPy, mpmath, and Arb backends for `loggamma_ratio`.
- Certified `loggamma_ratio` uses Arb `lgamma(a) - lgamma(b)` in the
  `direct_arb_loggamma_ratio` scope.
- Numerator poles, denominator poles, and simultaneous poles fail cleanly.
- Added the MCP tool `special_loggamma_ratio`.
- Added external fixtures and certified identity tests for the loggamma-ratio
  behavior.
- No `gamma_ratio` behavior change is included.
- No parabolic-cylinder claim broadening is included; those wrappers remain
  `experimental_formula`.

## 0.2.0-alpha.1 - 2026-05-08

- Added the public `gamma_ratio(a, b)` wrapper as the only public API expansion
  for the 0.2.0 alpha line.
- Added SciPy, mpmath, and Arb backends for `gamma_ratio`.
- Certified `gamma_ratio` uses the Arb product `Gamma(a) * rgamma(b)` in the
  `direct_arb_gamma_ratio` scope.
- Denominator poles certify to zero when `Gamma(a)` is finite, while numerator
  poles and simultaneous numerator/denominator poles fail cleanly.
- Added the MCP tool `special_gamma_ratio`.
- Added external fixtures and certified identity tests for the gamma-ratio
  behavior.
- No parabolic-cylinder claim broadening is included; those wrappers remain
  `experimental_formula`.

## 0.1.0 - 2026-05-08

- Planned the first non-prerelease package release with the same frozen public
  API as `0.1.0-alpha.3`.
- No mathematical implementation changes from `0.1.0-alpha.3`, no
  public-wrapper expansion, and no certification-claim broadening are included.
- The parabolic-cylinder formula layer remains `experimental_formula`.
- The release includes PyPI publishing guardrails, fresh-install smoke tests,
  deterministic audit grids, and external-reference fixture containment tests.

## 0.1.0-alpha.3 - 2026-05-08

- Added deterministic parabolic-cylinder formula-audit grids for recurrence,
  connection-formula, derivative, branch-side, cancellation, and stress
  coverage.
- Added external-reference fixture containment tests for selected gamma, Airy,
  Bessel, and parabolic-cylinder certified results.
- Hardened release workflows by making TestPyPI manual-only and adding a
  tag/version parity guard before publishing builds.
- No mathematical implementation changes, public-wrapper expansion, or
  certification-claim broadening are included.

## 0.1.0-alpha.2 - 2026-05-08

- Added TestPyPI and PyPI trusted-publishing workflows, plus a PyPI smoke
  workflow for fresh prerelease install verification.
- Added release-claim guardrails, frozen-scope checks, branch-protection check
  naming, and v0.1.x audit coverage to keep the 0.1.0 certified scope frozen.
- Documented PyPI installation and the post-release verification evidence for
  `v0.1.0-alpha.1`.
- Hardened GitHub Actions compatibility and PyPI smoke workflow behavior without
  changing mathematical implementations, adding public wrappers, or broadening
  certification claims.

## 0.1.0-alpha.1 - 2026-05-07

- Added special-function wrappers for gamma, Airy, Bessel, and parabolic-cylinder families, with the
  parabolic-cylinder formula layer marked experimental.
- Added SciPy fast mode, mpmath high-precision mode, and optional python-flint certified mode.
- Added structured `SFResult` diagnostics, MCP wrappers, CI, and certification documentation.
- Hardened dispatcher v2 with an explicit backend method registry and API/MCP coverage checks.
