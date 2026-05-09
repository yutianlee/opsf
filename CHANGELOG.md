# Changelog

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
