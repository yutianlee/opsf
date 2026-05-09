# certsf 0.2.0-alpha.4

`v0.2.0-alpha.4` is the fourth feature alpha for the 0.2.0 line. It keeps the
release wording conservative while adding one public special-function wrapper
since `0.2.0-alpha.3`: `pochhammer(a, n)`.

This planning release is metadata and documentation only. It does not include
`src/` changes, backend formula changes, or public wrapper expansion beyond the
already-merged `pochhammer(a, n)`.

## Public API Scope

`pochhammer(a, n)` is the only new public API expansion since
`0.2.0-alpha.3`. The wrapper returns an `SFResult` for the rising factorial:

```text
(a)_n = Gamma(a+n) / Gamma(a)
```

Certified `pochhammer` uses the narrow `direct_arb_pochhammer_product` scope.
The Arb backend evaluates only the finite product

```text
prod_{k=0}^{n-1}(a+k)
```

for exact integer `n >= 0`. The `n = 0` case returns certified `1`, and exact
zero factors return certified zero.

Analytic continuation in `n` is not certified. Non-integer `n`, negative `n`,
oversized product paths, and simultaneous gamma-pole limiting values fail
cleanly as non-certified results. No simultaneous-pole limiting values are
certified.

The MCP surface includes `special_pochhammer` for the same wrapper. MCP support
does not expand the mathematical support surface.

## Certification Claims

The current 0.2.0 alpha support matrix remains:

| Area | Release status |
| --- | --- |
| `gamma`, `loggamma`, `rgamma`, `gamma_ratio`, `loggamma_ratio`, `beta`, `pochhammer` | alpha-certified, direct Arb gamma primitives and finite products |
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
python scripts/check_release_version.py v0.2.0-alpha.4
python -m ruff check .
python -m mypy
python -m pytest
python -m build
python -m twine check dist/*
```

The PyPI smoke workflow should continue to target the latest actually published
version until `0.2.0a4` is published.
