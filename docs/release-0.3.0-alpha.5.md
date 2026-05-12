# certsf 0.3.0-alpha.5

`v0.3.0-alpha.5` is the fifth alpha in the 0.3 line. It packages the
explicit positive-real `rgamma` method added after `v0.3.0-alpha.4`.

## Release Target

- Python package version: `0.3.0a5`.
- Git tag: `v0.3.0-alpha.5`.
- GitHub release type: prerelease.
- PyPI version after release: `certsf 0.3.0a5`.

## Scope

The public wrapper surface remains unchanged. This release packages the
existing `rgamma` wrapper's explicit certified method:

```python
rgamma(x, mode="certified", method="stirling_recip", dps=...)
```

The method is limited to finite real `x >= 20`. It computes `rgamma(x)` by
exponentiating the negated certified positive-real `loggamma` Arb enclosure:
`rgamma(x) = exp(-loggamma(x))`. The method uses
`certificate_scope="rgamma_positive_real_stirling_recip"` and returns runtime
result method `method="stirling_recip_rgamma"`.

## Default Dispatch

Default certified `rgamma` remains the direct Arb path. Calls with
`method=None` and calls with `method="auto"` remain unchanged. The
`method="stirling_recip"` path is explicit only and is not automatic default
selection.

## Exclusions

This alpha does not add:

- complex `rgamma` certification;
- reflection formula certification;
- near-pole behavior support;
- custom Stirling-recip `rgamma` for real `x < 20`;
- custom Stirling-recip `rgamma` for real `x <= 0`;
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
`0.3.0a4`, until `certsf 0.3.0a5` is published and smoke verification passes.
If a smoke-pin update lands before PyPI publication succeeds, revert the pin to
the latest published version and retry the update after real PyPI plus
`pypi-smoke` verification passes.

## Validation

Release validation should run:

```powershell
python scripts/check_release_version.py v0.3.0-alpha.5
python -m ruff check .
python -m mypy
python -m pyright src
python -m pytest
python -m build
python -m twine check dist/*
python benchmarks/bench_gamma_methods.py
python benchmarks/bench_rgamma_methods.py
python benchmarks/bench_loggamma_methods.py
python benchmarks/analyze_loggamma_auto.py
python benchmarks/summarize_loggamma_auto.py docs/benchmark_samples/loggamma_certified_auto_sample.jsonl
```
