# certsf 0.3.0-alpha.4

`v0.3.0-alpha.4` is the fourth alpha in the 0.3 line. It packages the
explicit positive-real `gamma` method added after `v0.3.0-alpha.3`.

## Release Target

- Python package version: `0.3.0a4`.
- Git tag: `v0.3.0-alpha.4`.
- GitHub release type: prerelease.
- PyPI version after release: `certsf 0.3.0a4`.

## Scope

The public wrapper surface remains unchanged. This release packages the
existing `gamma` wrapper's explicit certified method:

```python
gamma(x, mode="certified", method="stirling_exp", dps=...)
```

The method is limited to finite real `x >= 20`. It computes `gamma(x)` by
exponentiating a certified positive-real `loggamma` Arb enclosure, keeping the
loggamma enclosure and exponentiation inside Arb ball arithmetic. The method
uses `certificate_scope="gamma_positive_real_stirling_exp"` and returns
runtime result method `method="stirling_exp_gamma"`.

## Default Dispatch

Default certified `gamma` remains the direct Arb path. Calls with
`method=None` and calls with `method="auto"` remain unchanged. The
`method="stirling_exp"` path is explicit only and is not automatic default
selection.

## Exclusions

This alpha does not add:

- complex `gamma` certification;
- reflection formula certification;
- near-pole behavior certification;
- custom Stirling-exp `gamma` for real `x < 20`;
- custom Stirling-exp `gamma` for real `x <= 0`;
- gamma-ratio asymptotics;
- beta asymptotics;
- parabolic-cylinder promotion; or
- new public wrappers.

Parabolic-cylinder wrappers remain `experimental_formula`.

## TestPyPI Decision

Under [`release_policy.md`](release_policy.md), this is a routine feature
alpha unless release validation identifies packaging or workflow risk. TestPyPI
staging is skipped unless that risk appears during validation. Real PyPI
publication plus `pypi-smoke` is sufficient.

The `pypi-smoke` workflow remains pinned to the last verified prerelease,
`0.3.0a3`, until `certsf 0.3.0a4` is published and smoke verification passes.

## Validation

Release validation should run:

```powershell
python scripts/check_release_version.py v0.3.0-alpha.4
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

