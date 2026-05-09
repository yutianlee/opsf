# certsf 0.2.0-alpha.9

`v0.2.0-alpha.9` is the ninth feature alpha for the 0.2.0 line. It keeps the
release wording conservative while adding one public special-function wrapper
since `0.2.0-alpha.8`: `erfinv(x)`.

The release-planning PR is metadata and documentation only. It does not include
`src/` changes, backend formula changes, or public wrapper expansion beyond the
already-merged `erfinv(x)`.

## Public API Scope

`erfinv(x)` is the only new public API expansion since `0.2.0-alpha.8`. The
wrapper returns an `SFResult` value for the real principal inverse of `erf`:

```text
erf(erfinv(x)) = x for real -1 < x < 1
```

Fast mode uses `scipy.special.erfinv(x)`.

High-precision mode uses `mpmath.erfinv(x)` when available. If mpmath does not
expose `erfinv`, high-precision mode solves `erf(y) = x` numerically.

Certified `erfinv` supports real `x` only with `-1 < x < 1`. It prefers direct
Arb `erfinv` when the installed `python-flint` exposes one. Otherwise it uses a
certified monotone real-root enclosure for `erf(y)-x=0` with
`certificate_scope="arb_erfinv_real_root"`,
`certificate_level="certified_real_root"`,
`audit_status="monotone_real_inverse"`, and
`domain="real_x_in_open_interval_minus1_1"` in diagnostics.

Endpoints, out-of-domain real inputs, and complex inputs fail cleanly in
certified mode. This alpha does not add `erfcinv`, complex inverse branches,
Faddeeva/wofz, plasma dispersion, or endpoint asymptotic certification.

The MCP surface includes `special_erfinv` for the same wrapper. MCP support
does not expand the mathematical support surface.

## Certification Claims

The current 0.2.0 alpha support matrix remains:

| Area | Release status |
| --- | --- |
| `gamma`, `loggamma`, `rgamma`, `gamma_ratio`, `loggamma_ratio`, `beta`, `pochhammer` | alpha-certified, direct Arb gamma primitives and finite products |
| `erf`, `erfc`, `erfcx`, `erfi`, `dawson`, `erfinv` | alpha-certified, direct Arb error-function primitives plus erfcx, erfi, and dawson identity formulas; real erfinv on (-1, 1) |
| `airy`, `ai`, `bi` | alpha-certified, direct Arb primitive |
| `besselj`, `bessely`, `besseli`, `besselk` | alpha-certified where direct Arb primitive works; real-valued order only |
| `pcfd`, `pcfu`, `pcfv`, `pcfw`, `pbdv` | experimental certified formula layer |
| MCP server | experimental tool interface |
| Custom Taylor/asymptotic methods | not yet |

No `erf`, `erfc`, `erfcx`, `erfi`, or `dawson` behavior changes are included.

No gamma-family behavior changes are included.

Parabolic-cylinder wrappers remain `experimental_formula`. This alpha does not
broaden their formula, branch, domain, or release claims.

Custom Taylor/asymptotic methods are still not included.

## Release Policy

Under [`release_policy.md`](release_policy.md), routine feature alpha releases
may skip TestPyPI when build, `twine check`, tag/version parity, protected PyPI
publishing, and real PyPI smoke all pass. This release-planning PR does not
introduce packaging or workflow-risk changes that require TestPyPI staging.

Before publication, the PyPI smoke workflow continues to target `0.2.0a8`.
Do not update `pypi-smoke.yml` to `0.2.0a9` until after the real PyPI release
is published and smoke verification succeeds.

## Validation Before Tagging

Before tagging or publishing this alpha, run:

```powershell
python scripts/check_release_version.py v0.2.0-alpha.9
python -m ruff check .
python -m mypy
python -m pytest
python -m build
python -m twine check dist/*
```
