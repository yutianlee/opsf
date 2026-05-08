# Changelog

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
