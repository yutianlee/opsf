# certsf 0.2.0-alpha.3

`v0.2.0-alpha.3` is the third feature alpha for the 0.2.0 line. It keeps the
release wording conservative while adding one public special-function wrapper
since `0.2.0-alpha.2`: `beta(a, b)`.

This planning release is metadata and documentation only. It does not include
`src/` changes, backend formula changes, or public wrapper expansion beyond the
already-merged `beta(a, b)`.

## Public API Scope

`beta(a, b)` is the only new public API expansion since `0.2.0-alpha.2`. The
wrapper returns an `SFResult` for the Euler beta function:

```text
B(a,b) = Gamma(a) Gamma(b) / Gamma(a+b)
```

Certified `beta` uses the narrow `direct_arb_beta` scope: the Arb backend
evaluates the product

```text
Gamma(a) * Gamma(b) * rgamma(a+b)
```

This certifies the Arb product, not all analytic continuations or singular
limits of the beta function. Denominator or sum-pole zeros are certified only
when the numerator gamma factors `Gamma(a)` and `Gamma(b)` are finite and Arb
returns the zero product. Numerator poles and simultaneous pole interactions
fail cleanly as non-certified results; no simultaneous-pole limiting values are
certified.

The MCP surface includes `special_beta` for the same wrapper. MCP support does
not expand the mathematical support surface.

## Certification Claims

The current 0.2.0 alpha support matrix remains:

| Area | Release status |
| --- | --- |
| `gamma`, `loggamma`, `rgamma`, `gamma_ratio`, `loggamma_ratio`, `beta` | alpha-certified, direct Arb gamma primitives |
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
python scripts/check_release_version.py v0.2.0-alpha.3
python -m ruff check .
python -m mypy
python -m pytest
python -m build
python -m twine check dist/*
```

The PyPI smoke workflow should continue to target the latest actually published
version until `0.2.0a3` is published.
