# certsf 0.1.0 Alpha Release Notes

`certsf` 0.1.0 is an alpha release for a small certified-dispatch API around
special functions. The package returns `SFResult` payloads with values,
backend metadata, certification status, error bounds, and diagnostics. The
diagnostics are part of the product: they explain whether a result is a plain
numerical value, a direct Arb enclosure, or an experimental formula-backed
enclosure.

Release claim wording is intentionally guarded by
[`release_claims.md`](release_claims.md): alpha release copy must not imply a
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

Unsupported certified domains return clean non-certified failures with
`certified=False`, an empty value, and a diagnostic error. They must not silently
fall back to a non-certified backend while claiming certification.

## Certification Notes

Direct Arb primitive families call Arb special-function primitives through
`python-flint` and report Arb ball radii as absolute error bounds.

The parabolic-cylinder family is different. Arb rigorously encloses the
implemented documented formula, but formula and branch auditing remains in
progress. Treat those certificates as experimental formula-layer certificates,
not as a broad global certification claim for every continuation of the target
functions.

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

## Pre-Release Checks

Before tagging 0.1.0, run:

```powershell
python -m ruff check src tests examples
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
