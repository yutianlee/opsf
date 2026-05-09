# certsf 0.2.0-alpha.7

`v0.2.0-alpha.7` is the seventh feature alpha for the 0.2.0 line. It keeps the
release wording conservative while adding one public special-function wrapper
since `0.2.0-alpha.6`: `erfi(z)`.

This planning release is metadata and documentation only. It does not include
`src/` changes, backend formula changes, or public wrapper expansion beyond the
already-merged `erfi(z)`.

## Public API Scope

`erfi(z)` is the only new public API expansion since `0.2.0-alpha.6`. The
wrapper returns an `SFResult` value for:

```text
erfi(z) = -i erf(i z)
```

Fast mode uses `scipy.special.erfi(z)` when available. If SciPy does not expose
that primitive, fast mode evaluates `-1j * scipy.special.erf(1j*z)`.

High-precision mode uses `mpmath.erfi(z)` when available. If mpmath does not
expose that primitive, high-precision mode evaluates `-i*mpmath.erf(i*z)`.

Certified `erfi` prefers a direct Arb `erfi` primitive when the installed
`python-flint` exposes one. Otherwise it evaluates the Arb formula
`-i*erf(i*z)` with `certificate_scope="arb_erfi_formula"`,
`certificate_level="formula_audited_alpha"`, `audit_status="formula_identity"`,
and `formula="-i*erf(i*z)"` in diagnostics.

No asymptotic or custom certification method is included. This alpha does not
add `erfinv`, `erfcinv`, Faddeeva, Dawson, or any other error-function variant.

The MCP surface includes `special_erfi` for the same wrapper. MCP support does
not expand the mathematical support surface.

## Certification Claims

The current 0.2.0 alpha support matrix remains:

| Area | Release status |
| --- | --- |
| `gamma`, `loggamma`, `rgamma`, `gamma_ratio`, `loggamma_ratio`, `beta`, `pochhammer` | alpha-certified, direct Arb gamma primitives and finite products |
| `erf`, `erfc`, `erfcx`, `erfi` | alpha-certified, direct Arb error-function primitives plus erfcx/erfi identity formulas |
| `airy`, `ai`, `bi` | alpha-certified, direct Arb primitive |
| `besselj`, `bessely`, `besseli`, `besselk` | alpha-certified where direct Arb primitive works; real-valued order only |
| `pcfd`, `pcfu`, `pcfv`, `pcfw`, `pbdv` | experimental certified formula layer |
| MCP server | experimental tool interface |
| Custom Taylor/asymptotic methods | not yet |

No `erf`, `erfc`, or `erfcx` behavior changes are included.

No gamma-family behavior changes are included.

Parabolic-cylinder wrappers remain `experimental_formula`. This alpha does not
broaden their formula, branch, domain, or release claims.

Custom Taylor/asymptotic methods are still not included.

## Validation Before Tagging

Before tagging or publishing this alpha, run:

```powershell
python scripts/check_release_version.py v0.2.0-alpha.7
python -m ruff check .
python -m mypy
python -m pytest
python -m build
python -m twine check dist/*
```

The PyPI smoke workflow should continue to target `0.2.0a6` until
`0.2.0a7` is published.
