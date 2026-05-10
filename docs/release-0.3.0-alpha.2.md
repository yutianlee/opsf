# certsf 0.3.0-alpha.2

`v0.3.0-alpha.2` is the second alpha in the 0.3 line. It packages the
explicit certified `loggamma` selector added and hardened after
`v0.3.0-alpha.1`.

## Release Target

- Python package version: `0.3.0a2`.
- Git tag: `v0.3.0-alpha.2`.
- GitHub release type: prerelease.
- PyPI version after release: `certsf 0.3.0a2`.

## Scope

The public wrapper surface remains unchanged from `0.3.0-alpha.1` and from the
0.2 wrapper list. The new release-facing functionality is explicit certified
method selection for the existing `loggamma` wrapper:

```python
loggamma(x, mode="certified", method="certified_auto", dps=...)
```

The selector may choose:

- direct Arb, returned as `method="arb_ball"`;
- explicit positive-real `method="stirling"`, returned as
  `method="stirling_loggamma"`; or
- explicit positive-real `method="stirling_shifted"`, returned as
  `method="stirling_shifted_loggamma"`.

The selected result preserves the selected backend's method and certificate
scope. Selector diagnostics record `auto_selector`, `auto_selected_method`,
`auto_reason`, and `auto_candidates`.

## Default Dispatch

Default certified `loggamma` remains direct Arb. Calls that omit `method=...`
or pass `method="auto"` remain unchanged. `method="certified_auto"` is explicit
only and is not a default selector.

## Exclusions

This alpha does not add complex Stirling, gamma-ratio asymptotics, beta
asymptotics, or new public wrappers. Custom Stirling certification remains
limited to real `x >= 20`; complex `loggamma` branches, `x < 20` custom
Stirling, and `x <= 0` custom Stirling are excluded. Parabolic-cylinder
wrappers remain `experimental_formula`.

## TestPyPI Decision

Under [`release_policy.md`](release_policy.md), this is a routine feature alpha
with no packaging, dependency, or workflow-risk change beyond release defaults.
TestPyPI staging is skipped unless release validation identifies packaging or
workflow risk. Real PyPI publication plus `pypi-smoke` is sufficient.

The PyPI smoke workflow remains pinned to the latest published and verified
package, `0.3.0a1`, until `certsf 0.3.0a2` is published and smoke verification
passes.

## Validation

Before tagging or publishing this prerelease, run:

```powershell
python scripts/check_release_version.py v0.3.0-alpha.2
python -m ruff check .
python -m mypy
python -m pyright src
python -m pytest
python -m build
python -m twine check dist/*
python benchmarks/bench_loggamma_methods.py
```
