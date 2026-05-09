# certsf 0.2.0-alpha.10

`v0.2.0-alpha.10` is the tenth feature alpha for the 0.2.0 line. It keeps the
release wording conservative while adding one public special-function wrapper
since `0.2.0-alpha.9`: `erfcinv(x)`.

The release-planning PR is metadata and documentation only. It does not include
`src/` changes, backend formula changes, or public wrapper expansion beyond the
already-merged `erfcinv(x)`.

## Public API Scope

`erfcinv(x)` is the only new public API expansion since `0.2.0-alpha.9`. The
wrapper returns an `SFResult` value for the real principal inverse of `erfc`:

```text
erfc(erfcinv(x)) = x for real 0 < x < 2
erfcinv(x) = erfinv(1-x)
```

Fast mode uses `scipy.special.erfcinv(x)`.

High-precision mode uses a mpmath inverse when available. If mpmath does not
expose an inverse complementary error function, high-precision mode uses
`erfinv(1-x)`.

Certified `erfcinv` supports real `x` only with `0 < x < 2`. It prefers direct
Arb `erfcinv` when the installed `python-flint` exposes one. Otherwise it uses
the certified `erfinv(1-x)` fallback with
`certificate_scope="arb_erfcinv_via_erfinv"`,
`certificate_level="certified_real_root"`,
`audit_status="monotone_real_inverse"`,
`domain="real_x_in_open_interval_0_2"`, and `formula="erfinv(1-x)"` in
diagnostics.

Endpoints, out-of-domain real inputs, and complex inputs fail cleanly in
certified mode. This alpha does not add complex inverse branches, endpoint
asymptotic certification, Faddeeva/wofz, or plasma dispersion wrappers.

The MCP surface includes `special_erfcinv` for the same wrapper. MCP support
does not expand the mathematical support surface.

## Certification Claims

The current 0.2.0 alpha support matrix remains:

| Area | Release status |
| --- | --- |
| `gamma`, `loggamma`, `rgamma`, `gamma_ratio`, `loggamma_ratio`, `beta`, `pochhammer` | alpha-certified, direct Arb gamma primitives and finite products |
| `erf`, `erfc`, `erfcx`, `erfi`, `dawson`, `erfinv`, `erfcinv` | alpha-certified, direct Arb error-function primitives plus erfcx, erfi, and dawson identity formulas; real erfinv on (-1, 1); real erfcinv on (0, 2) |
| `airy`, `ai`, `bi` | alpha-certified, direct Arb primitive |
| `besselj`, `bessely`, `besseli`, `besselk` | alpha-certified where direct Arb primitive works; real-valued order only |
| `pcfd`, `pcfu`, `pcfv`, `pcfw`, `pbdv` | experimental certified formula layer |
| MCP server | experimental tool interface |
| Custom Taylor/asymptotic methods | not yet |

No `erfinv` behavior changes are included.

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

Before publication, the PyPI smoke workflow continues to target `0.2.0a9`.
Do not update `pypi-smoke.yml` to `0.2.0a10` until after the real PyPI release
is published and smoke verification succeeds.

## Validation Before Tagging

Before tagging or publishing this alpha, run:

```powershell
python scripts/check_release_version.py v0.2.0-alpha.10
python -m ruff check .
python -m mypy
python -m pytest
python -m build
python -m twine check dist/*
```
