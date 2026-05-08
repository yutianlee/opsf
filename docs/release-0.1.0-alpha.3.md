# certsf 0.1.0 Alpha 3 Planning Notes

`v0.1.0-alpha.3` is an audit and release-infrastructure hardening prerelease
for the frozen 0.1.0 alpha line. It records additional formula-audit evidence,
external-reference fixture coverage, and publishing guardrails.

## Scope Freeze

This prerelease does not change mathematical implementations, expand the public
API, add public wrappers, or broaden certification scope. The 0.1.0 certified
scope remains frozen:

| Area | Release status |
| --- | --- |
| `gamma`, `loggamma`, `rgamma` | alpha-certified, direct Arb primitive |
| `airy`, `ai`, `bi` | alpha-certified, direct Arb primitive |
| `besselj`, `bessely`, `besseli`, `besselk` | alpha-certified where direct Arb primitive works; real-valued order only |
| `pcfd`, `pcfu`, `pcfv`, `pcfw`, `pbdv` | experimental certified formula layer |
| MCP server | experimental tool interface |
| Custom Taylor/asymptotic methods | not yet |

The parabolic-cylinder wrappers remain `experimental_formula`. Runtime
diagnostics for that family continue to use the existing
`formula_audited_experimental` level and the in-progress formula-audit claim.

## Audit And Infrastructure Changes

- Deterministic parabolic-cylinder formula-audit grids now cover real small
  values, moderate real values, negative arguments where allowed, complex
  branch-side samples where allowed, gamma-factor cancellation neighborhoods,
  and larger-argument stress samples.
- External reference fixtures now check certified ball containment for selected
  gamma, Airy, Bessel, and parabolic-cylinder values.
- TestPyPI publishing is manual-only.
- PyPI and TestPyPI publishing workflows check tag/package version parity before
  building distributions.

External fixtures supplement but do not replace formula and domain audit. They
are additional containment evidence beside recurrence, derivative,
connection-formula, branch, and domain-policy tests.

## Package Metadata

- Git tag: `v0.1.0-alpha.3`.
- Python package version: `0.1.0a3`.
- Citation metadata version: `0.1.0-alpha.3`.
- Package summary remains:
  `Alpha special-function wrappers with explicit certification diagnostics.`

## Validation Plan

Before tagging or publishing this prerelease, run:

```powershell
python scripts/check_release_version.py v0.1.0-alpha.3
python -m ruff check .
python -m mypy
python -m pytest
python -m build
python -m twine check dist/*
```

The validation is expected to confirm that only release metadata and
documentation changed while the frozen 0.1.0 certified scope remains unchanged.
