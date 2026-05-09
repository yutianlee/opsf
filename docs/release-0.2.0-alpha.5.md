# certsf 0.2.0-alpha.5

`v0.2.0-alpha.5` is the fifth feature alpha for the 0.2.0 line. It keeps the
release wording conservative while adding two public special-function wrappers
since `0.2.0-alpha.4`: `erf(z)` and `erfc(z)`.

This planning release is metadata and documentation only. It does not include
`src/` changes, backend formula changes, or public wrapper expansion beyond the
already-merged `erf(z)` and `erfc(z)`.

## Public API Scope

`erf(z)` and `erfc(z)` are the only new public API expansions since
`0.2.0-alpha.4`. The wrappers return `SFResult` values for:

```text
erf(z) = 2/sqrt(pi) * integral_0^z exp(-t^2) dt
erfc(z) = 1 - erf(z)
```

Certified `erf` uses the narrow `direct_arb_erf` scope. Certified `erfc` uses
the narrow `direct_arb_erfc` scope. The Arb backend prefers the direct Arb
`erfc` primitive when available; if direct `erfc` is unavailable but direct
`erf` is available, the only documented certified fallback is Arb arithmetic
for `1 - erf(z)` with `formula="1-erf"` in diagnostics.

No asymptotic or custom certification method is included. This alpha does not
add `erfi`, `erfinv`, `erfcinv`, scaled `erfc`, or any other error-function
wrapper.

The MCP surface includes `special_erf` and `special_erfc` for the same
wrappers. MCP support does not expand the mathematical support surface.

## Certification Claims

The current 0.2.0 alpha support matrix remains:

| Area | Release status |
| --- | --- |
| `gamma`, `loggamma`, `rgamma`, `gamma_ratio`, `loggamma_ratio`, `beta`, `pochhammer` | alpha-certified, direct Arb gamma primitives and finite products |
| `erf`, `erfc` | alpha-certified, direct Arb error-function primitives |
| `airy`, `ai`, `bi` | alpha-certified, direct Arb primitive |
| `besselj`, `bessely`, `besseli`, `besselk` | alpha-certified where direct Arb primitive works; real-valued order only |
| `pcfd`, `pcfu`, `pcfv`, `pcfw`, `pbdv` | experimental certified formula layer |
| MCP server | experimental tool interface |
| Custom Taylor/asymptotic methods | not yet |

No gamma-family behavior changes are included.

Parabolic-cylinder wrappers remain `experimental_formula`. This alpha does not
broaden their formula, branch, domain, or release claims.

Custom Taylor/asymptotic methods are still not included.

## Validation Before Tagging

Before tagging or publishing this alpha, run:

```powershell
python scripts/check_release_version.py v0.2.0-alpha.5
python -m ruff check .
python -m mypy
python -m pytest
python -m build
python -m twine check dist/*
```

The PyPI smoke workflow should continue to target `0.2.0a4` until
`0.2.0a5` is published.
