# certsf 0.1.0 Release Notes

`certsf` 0.1.0 is a conservative first non-prerelease package release for a
small certified-dispatch API around special functions. It keeps the same frozen
public API as `0.1.0-alpha.3`; there are no mathematical implementation changes,
no public-wrapper expansion, and no certification-scope broadening from that
prerelease.

The package is still alpha-quality in scientific scope. It returns `SFResult`
payloads with values, backend metadata, certification status, error bounds, and
diagnostics. The diagnostics are part of the product: they explain whether a
result is a plain numerical value, a direct Arb enclosure, or an experimental
formula-backed enclosure.

Release claim wording is intentionally guarded by
[`release_claims.md`](release_claims.md): release copy must not imply a
completed global certification audit for formula-backed wrappers.

## Package Metadata

- Build backend: hatchling.
- Python support: Python 3.10 and newer.
- License: MIT.
- Base dependencies: SciPy and mpmath.
- Optional extras:
  - `certified`: installs `python-flint` for Arb-backed certified mode.
  - `mcp`: installs MCP server dependencies.
  - `test`: installs pytest.
  - `dev`: installs development, test, MCP, and certified dependencies.

## Certified Support Matrix

| Area | Release status |
| --- | --- |
| `gamma`, `loggamma`, `rgamma` | alpha-certified, direct Arb primitive |
| `airy`, `ai`, `bi` | alpha-certified, direct Arb primitive |
| `besselj`, `bessely`, `besseli`, `besselk` | alpha-certified where direct Arb primitive works; real-valued order only |
| `pcfd`, `pcfu`, `pcfv`, `pcfw`, `pbdv` | experimental certified formula layer |
| MCP server | experimental tool interface |
| Custom Taylor/asymptotic methods | not yet |

Direct Arb primitive families are alpha-certified on documented
finite-enclosure domains. Unsupported certified domains return clean
non-certified failures with `certified=False`, an empty value, and a diagnostic
error. They must not silently fall back to a non-certified backend while
claiming certification.

## Certification Notes

Direct Arb primitive families call Arb special-function primitives through
`python-flint` and report Arb ball radii as absolute error bounds.

The parabolic-cylinder family is different. Arb rigorously encloses the
implemented documented formula, but formula and branch auditing remains in
progress. Treat those certificates as experimental formula-layer certificates,
not as a broad global certification claim for every continuation of the target
functions. The parabolic-cylinder wrappers remain `experimental_formula`.

No custom Taylor or asymptotic methods are included yet.

## Release Hardening

This release includes the packaging and audit hardening added during the alpha
cycle:

- PyPI publishing guardrails, including tag/version parity checks.
- Fresh-install PyPI smoke tests for base, certified, and MCP certified
  installs.
- Deterministic parabolic-cylinder formula-audit grids.
- External-reference fixture containment tests that supplement, but do not
  replace, formula and domain audit.

## Examples

The example scripts print full payloads instead of just numerical values:

- `examples/gamma_certified.py`
- `examples/airy_components.py`
- `examples/bessel_complex.py`
- `examples/pcf_experimental.py`
- `examples/mcp_payload.py`

Run examples from an editable checkout with:

```powershell
python -m pip install -e ".[dev]"
python examples/gamma_certified.py
python examples/airy_components.py
python examples/bessel_complex.py
python examples/pcf_experimental.py
python examples/mcp_payload.py
```

When `python-flint` is unavailable, certified examples still return structured
non-certified failure payloads. That behavior is intentional and part of the
public contract.

## Release Checks

Before tagging 0.1.0, run:

```powershell
python scripts/check_release_version.py v0.1.0
python -m ruff check .
python -m mypy
python -m pytest
python -m build
python -m twine check dist/*
python examples/gamma_certified.py
python examples/airy_components.py
python examples/bessel_complex.py
python examples/pcf_experimental.py
python examples/mcp_payload.py
```
