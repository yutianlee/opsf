# certsf 0.3.0-alpha.3

`v0.3.0-alpha.3` is the third alpha in the 0.3 line. It packages the
preselection optimization for the explicit certified `loggamma` selector added
after `v0.3.0-alpha.2`.

## Release Target

- Python package version: `0.3.0a3`.
- Git tag: `v0.3.0-alpha.3`.
- GitHub release type: prerelease.
- PyPI version after release: `certsf 0.3.0a3`.

## Scope

The public wrapper surface remains unchanged. The release-facing change is an
optimization inside the existing explicit selector:

```python
loggamma(x, mode="certified", method="certified_auto", dps=...)
```

The selector may choose:

- direct Arb, returned as `method="arb_ball"`;
- explicit positive-real `method="stirling"`, returned as
  `method="stirling_loggamma"`; or
- explicit positive-real `method="stirling_shifted"`, returned as
  `method="stirling_shifted_loggamma"`.

The alpha packages preselection helpers that estimate unshifted and shifted
Stirling certifiability before evaluating full custom candidates. This avoids
unnecessary full custom candidate evaluations when the tail-bound check already
shows that a candidate cannot certify, while preserving the selected backend's
method, certificate scope, and diagnostics.

## Default Dispatch

Default certified `loggamma` remains direct Arb. Calls that omit `method=...`
or pass `method="auto"` remain unchanged. `method="certified_auto"` remains
explicit only and is not a default selector.

## Exclusions

This alpha does not add complex `loggamma` branch certification, complex
Stirling, gamma-ratio asymptotics, beta asymptotics, or new public wrappers.
Custom Stirling certification remains limited to real `x >= 20`; `x < 20`
custom Stirling and `x <= 0` custom Stirling are excluded.
Parabolic-cylinder wrappers remain `experimental_formula`.

## TestPyPI Decision

Under [`release_policy.md`](release_policy.md), this is a routine feature alpha
with no packaging, dependency, or workflow-risk change beyond release defaults.
TestPyPI staging is skipped unless release validation identifies packaging or
workflow risk. Real PyPI publication plus `pypi-smoke` is sufficient.

The PyPI smoke workflow remains pinned to the latest published and verified
package, `0.3.0a2`, until `certsf 0.3.0a3` is published and smoke verification
passes.

## Validation

Before tagging or publishing this prerelease, run:

```powershell
python scripts/check_release_version.py v0.3.0-alpha.3
python -m ruff check .
python -m mypy
python -m pyright src
python -m pytest
python -m build
python -m twine check dist/*
python benchmarks/bench_loggamma_methods.py
python benchmarks/analyze_loggamma_auto.py
python benchmarks/summarize_loggamma_auto.py docs/benchmark_samples/loggamma_certified_auto_sample.jsonl
```
