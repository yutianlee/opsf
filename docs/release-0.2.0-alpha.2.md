# certsf 0.2.0-alpha.2

`v0.2.0-alpha.2` is the second feature alpha for the 0.2.0 line. It keeps the
release wording conservative while adding one public special-function wrapper
since `0.2.0-alpha.1`: `loggamma_ratio(a, b)`.

This planning release is metadata and documentation only. It does not include
`src/` changes, backend formula changes, or public wrapper expansion beyond the
already-merged `loggamma_ratio`.

## Public API Scope

`loggamma_ratio(a, b)` is the only new public API expansion since
`0.2.0-alpha.1`. The wrapper returns an `SFResult` for the principal-loggamma
difference:

```text
principal loggamma(a) - principal loggamma(b)
```

Certified `loggamma_ratio` uses the narrow `direct_arb_loggamma_ratio` scope:
the Arb backend evaluates `lgamma(a) - lgamma(b)` using principal `loggamma`
branches. For complex inputs, this certifies the principal-loggamma difference,
not the principal logarithm of `gamma_ratio(a, b)` or of `Gamma(a) / Gamma(b)`.

Numerator poles, denominator poles, and simultaneous poles fail cleanly. This
alpha does not certify simultaneous-pole limiting values.

The MCP surface includes `special_loggamma_ratio` for the same wrapper. MCP
support does not expand the mathematical support surface.

## Certification Claims

The current 0.2.0 alpha support matrix remains:

| Area | Release status |
| --- | --- |
| `gamma`, `loggamma`, `rgamma`, `gamma_ratio`, `loggamma_ratio` | alpha-certified, direct Arb gamma primitives |
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
python scripts/check_release_version.py v0.2.0-alpha.2
python -m ruff check .
python -m mypy
python -m pytest
python -m build
python -m twine check dist/*
```

The PyPI smoke workflow should continue to target the latest actually published
version until `0.2.0a2` is published.
