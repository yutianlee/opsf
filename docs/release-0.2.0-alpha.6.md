# certsf 0.2.0-alpha.6

`v0.2.0-alpha.6` is the sixth feature alpha for the 0.2.0 line. It keeps the
release wording conservative while adding one public special-function wrapper
since `0.2.0-alpha.5`: `erfcx(z)`.

This planning release is metadata and documentation only. It does not include
`src/` changes, backend formula changes, or public wrapper expansion beyond the
already-merged `erfcx(z)`.

## Public API Scope

`erfcx(z)` is the only new public API expansion since `0.2.0-alpha.5`. The
wrapper returns an `SFResult` value for:

```text
erfcx(z) = exp(z^2) erfc(z)
```

Fast mode uses `scipy.special.erfcx(z)`. High-precision mode uses mpmath
evaluation of `exp(z*z) * erfc(z)`.

Certified `erfcx` prefers a direct Arb `erfcx` primitive when the installed
`python-flint` exposes one. Otherwise it evaluates the Arb formula
`exp(z^2)*erfc(z)` with `certificate_scope="arb_erfcx_formula"`,
`certificate_level="formula_audited_alpha"`, `audit_status="formula_identity"`,
and `formula="exp(z^2)*erfc(z)"` in diagnostics.

No asymptotic or custom certification method is included. This alpha does not
add `erfi`, `erfinv`, `erfcinv`, Faddeeva functions, or any other
error-function wrapper.

The MCP surface includes `special_erfcx` for the same wrapper. MCP support does
not expand the mathematical support surface.

## Certification Claims

The current 0.2.0 alpha support matrix remains:

| Area | Release status |
| --- | --- |
| `gamma`, `loggamma`, `rgamma`, `gamma_ratio`, `loggamma_ratio`, `beta`, `pochhammer` | alpha-certified, direct Arb gamma primitives and finite products |
| `erf`, `erfc`, `erfcx` | alpha-certified, direct Arb error-function primitives plus erfcx identity formula |
| `airy`, `ai`, `bi` | alpha-certified, direct Arb primitive |
| `besselj`, `bessely`, `besseli`, `besselk` | alpha-certified where direct Arb primitive works; real-valued order only |
| `pcfd`, `pcfu`, `pcfv`, `pcfw`, `pbdv` | experimental certified formula layer |
| MCP server | experimental tool interface |
| Custom Taylor/asymptotic methods | not yet |

No `erf` or `erfc` behavior changes are included.

No gamma-family behavior changes are included.

Parabolic-cylinder wrappers remain `experimental_formula`. This alpha does not
broaden their formula, branch, domain, or release claims.

Custom Taylor/asymptotic methods are still not included.

## Validation Before Tagging

Before tagging or publishing this alpha, run:

```powershell
python scripts/check_release_version.py v0.2.0-alpha.6
python -m ruff check .
python -m mypy
python -m pytest
python -m build
python -m twine check dist/*
```

The PyPI smoke workflow should continue to target `0.2.0a5` until
`0.2.0a6` is published.
