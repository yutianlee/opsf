# certsf 0.2.0-alpha.1

`v0.2.0-alpha.1` is a feature alpha for the 0.2.0 line. It keeps the release
wording conservative while adding one public special-function wrapper:
`gamma_ratio(a, b)`.

This planning release is metadata and documentation only. It does not include
`src/` changes, backend formula changes, or public wrapper expansion beyond the
already-merged `gamma_ratio`.

## Public API Scope

`gamma_ratio(a, b)` is the only public API expansion in this alpha. The wrapper
computes `Gamma(a) / Gamma(b)` and follows the same `SFResult` contract as the
existing gamma-family wrappers.

Certified `gamma_ratio` uses the narrow `direct_arb_gamma_ratio` scope: the Arb
backend evaluates `Gamma(a) * rgamma(b)`. This certifies denominator-pole zeros
when `Gamma(a)` is finite. Numerator poles and simultaneous
numerator/denominator poles fail cleanly rather than claiming a certified
limiting value.

The MCP surface includes `special_gamma_ratio` for the same wrapper. MCP support
does not expand the mathematical support surface.

## Certification Claims

The current 0.2.0 alpha support matrix remains:

| Area | Release status |
| --- | --- |
| `gamma`, `loggamma`, `rgamma`, `gamma_ratio` | alpha-certified, direct Arb gamma primitives |
| `airy`, `ai`, `bi` | alpha-certified, direct Arb primitive |
| `besselj`, `bessely`, `besseli`, `besselk` | alpha-certified where direct Arb primitive works; real-valued order only |
| `pcfd`, `pcfu`, `pcfv`, `pcfw`, `pbdv` | experimental certified formula layer |
| MCP server | experimental tool interface |
| Custom Taylor/asymptotic methods | not yet |

Parabolic-cylinder wrappers remain `experimental_formula`. This alpha does not
broaden their formula, branch, domain, or release claims.

Custom Taylor/asymptotic methods are still not included.

## Validation Before Tagging

Before tagging or publishing this alpha, run:

```powershell
python scripts/check_release_version.py v0.2.0-alpha.1
python -m ruff check .
python -m mypy
python -m pytest
python -m build
python -m twine check dist/*
```

The PyPI smoke workflow should continue to target the latest actually published
version until `0.2.0a1` is published.
