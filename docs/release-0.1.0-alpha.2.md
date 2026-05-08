# certsf 0.1.0 Alpha 2 Planning Notes

`v0.1.0-alpha.2` is a planning and hardening prerelease for the frozen 0.1.0
alpha line. It updates release notes and package metadata after the first public
PyPI artifact, without changing mathematical implementations, adding public
wrappers, or broadening certification claims.

## Scope Freeze

The 0.1.0 certified scope remains frozen. This prerelease keeps the same public
special-function surface and the same conservative release-status wording:

| Area | Release status |
| --- | --- |
| `gamma`, `loggamma`, `rgamma` | alpha-certified, direct Arb primitive |
| `airy`, `ai`, `bi` | alpha-certified, direct Arb primitive |
| `besselj`, `bessely`, `besseli`, `besselk` | alpha-certified where direct Arb primitive works; real-valued order only |
| `pcfd`, `pcfu`, `pcfv`, `pcfw`, `pbdv` | experimental certified formula layer |
| MCP server | experimental tool interface |
| Custom Taylor/asymptotic methods | not yet |

Unsupported certified domains continue to return clean non-certified results.
MCP remains a thin experimental interface over the same frozen Python API and
does not expand the mathematical support surface.

## Post-Alpha.1 Hardening

Since `v0.1.0-alpha.1`, the repository has focused on release discipline and
artifact verification:

- Added TestPyPI and PyPI trusted-publishing workflows.
- Added a PyPI smoke workflow for fresh prerelease install checks.
- Documented PyPI installation with `--pre` and optional extras.
- Recorded post-release verification evidence for the first PyPI artifact.
- Added release-claim guardrails and tests for conservative alpha wording.
- Added frozen-scope checks and v0.1.x audit issue coverage.
- Named required branch-protection checks and updated GitHub Actions for current
  runtime compatibility.

## Package Metadata

- Git tag: `v0.1.0-alpha.2`.
- Python package version: `0.1.0a2`.
- Citation metadata version: `0.1.0-alpha.2`.
- Package summary remains:
  `Alpha special-function wrappers with explicit certification diagnostics.`

## Validation Plan

Before tagging or publishing this prerelease, run:

```powershell
python -m ruff check .
python -m mypy
python -m pytest
python -m build
python -m twine check dist/*
```

The validation is expected to confirm that release metadata and documentation
changed while the frozen 0.1.0 certified scope remains unchanged.
