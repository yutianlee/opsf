# certsf 0.2.0-alpha.8

`v0.2.0-alpha.8` is the eighth feature alpha for the 0.2.0 line. It keeps the
release wording conservative while adding one public special-function wrapper
since `0.2.0-alpha.7`: `dawson(z)`.

The release-planning PR is metadata and documentation only. It does not include
`src/` changes, backend formula changes, or public wrapper expansion beyond the
already-merged `dawson(z)`.

## Public API Scope

`dawson(z)` is the only new public API expansion since `0.2.0-alpha.7`. The
wrapper returns an `SFResult` value for:

```text
dawson(z) = sqrt(pi)/2 * exp(-z^2) * erfi(z)
```

Fast mode uses `scipy.special.dawsn(z)` when available. If SciPy does not
expose that primitive, fast mode evaluates the `erfi` identity.

High-precision mode uses a mpmath Dawson function when available. If mpmath
does not expose one, high-precision mode evaluates the `erfi` identity.

Certified `dawson` prefers a direct Arb Dawson primitive when the installed
`python-flint` exposes one. Otherwise it evaluates the Arb formula
`sqrt(pi)/2*exp(-z^2)*erfi(z)` with
`certificate_scope="arb_dawson_formula"`,
`certificate_level="formula_audited_alpha"`, `audit_status="formula_identity"`,
and `formula="sqrt(pi)/2*exp(-z^2)*erfi(z)"` in diagnostics.

No asymptotic or custom certification method is included. This alpha does not
add inverse error functions, Faddeeva functions, plasma dispersion, or any
additional error-function variants.

The MCP surface includes `special_dawson` for the same wrapper. MCP support
does not expand the mathematical support surface.

## Certification Claims

The current 0.2.0 alpha support matrix remains:

| Area | Release status |
| --- | --- |
| `gamma`, `loggamma`, `rgamma`, `gamma_ratio`, `loggamma_ratio`, `beta`, `pochhammer` | alpha-certified, direct Arb gamma primitives and finite products |
| `erf`, `erfc`, `erfcx`, `erfi`, `dawson` | alpha-certified, direct Arb error-function primitives plus erfcx, erfi, and dawson identity formulas |
| `airy`, `ai`, `bi` | alpha-certified, direct Arb primitive |
| `besselj`, `bessely`, `besseli`, `besselk` | alpha-certified where direct Arb primitive works; real-valued order only |
| `pcfd`, `pcfu`, `pcfv`, `pcfw`, `pbdv` | experimental certified formula layer |
| MCP server | experimental tool interface |
| Custom Taylor/asymptotic methods | not yet |

No `erf`, `erfc`, `erfcx`, or `erfi` behavior changes are included.

No gamma-family behavior changes are included.

Parabolic-cylinder wrappers remain `experimental_formula`. This alpha does not
broaden their formula, branch, domain, or release claims.

Custom Taylor/asymptotic methods are still not included.

## Release Policy

Under [`release_policy.md`](release_policy.md), routine feature alpha releases
may skip TestPyPI when build, `twine check`, tag/version parity, protected PyPI
publishing, and real PyPI smoke all pass. This release-planning PR does not
introduce packaging or workflow-risk changes that require TestPyPI staging.

The PyPI smoke workflow must continue to target `0.2.0a7` until `0.2.0a8` is
actually published. A post-release verification PR should update pypi-smoke
after the real PyPI release is available and smoke-tested.

## Validation Before Tagging

Before tagging or publishing this alpha, run:

```powershell
python scripts/check_release_version.py v0.2.0-alpha.8
python -m ruff check .
python -m mypy
python -m pytest
python -m build
python -m twine check dist/*
```
