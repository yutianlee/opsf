# certsf 0.3.0-alpha.1

`v0.3.0-alpha.1` is the first alpha in the 0.3 line. It takes the runtime
work from the v0.3.0 planning branch, method registry v2, the explicit
positive-real Stirling `loggamma` method, and the explicit shifted Stirling
`loggamma` method into release metadata.

The release-planning PR is metadata, documentation, checklist, and workflow
default work only. It does not add mathematical implementation changes beyond
the already-merged 0.3 runtime work, does not add public wrappers, does not add
complex Stirling, and does not change default dispatch behavior.

## Release Target

- Python package version: `0.3.0a1`.
- Git tag: `v0.3.0-alpha.1`.
- GitHub release type: prerelease.
- PyPI version after release: `certsf 0.3.0a1`.

## Public Surface

The public special-function wrapper surface remains the same as `0.2.0`.
The new 0.3 alpha functionality is explicit certified custom methods for the
existing `loggamma` wrapper:

- `loggamma(x, mode="certified", method="stirling", dps=...)`;
- `loggamma(x, mode="certified", method="stirling_shifted", dps=...)`.

Default certified `loggamma` remains the direct Arb primitive path. Passing
`method=None` or `method="auto"` keeps the existing automatic selection path.
The explicit Stirling methods are not automatic default selection.

## Certified Custom Scope

The custom asymptotic domain is finite real `x >= 20`.

The explicit methods use
`certificate_scope="stirling_loggamma_positive_real"` and
`certificate_level="custom_asymptotic_bound"`. The shifted method uses the
documented Arb recurrence shift and `GUARD_DIGITS=2`; both explicit methods
return conservative absolute bounds that include Arb finite-expression radius
plus the explicit positive-real Stirling tail bound.

Excluded from this release:

- complex `loggamma` branch certification;
- real `x < 20`;
- `x <= 0`;
- gamma-ratio asymptotics;
- beta asymptotics;
- automatic selection of either Stirling method.

Parabolic-cylinder wrappers remain an `experimental_formula` surface. This
release does not promote or broaden their certification claims.

## TestPyPI Decision

This is the first release of a new minor line, so TestPyPI staging should be
used before the real PyPI prerelease. Manually run `publish-testpypi` with
`ref=v0.3.0-alpha.1` and `confirm=publish-testpypi` before publishing the real
GitHub prerelease that triggers PyPI publication.

The PyPI smoke workflow remains pinned to the latest actually published PyPI
version, `0.2.0`, until `certsf 0.3.0a1` is published and smoke verification
passes. Update the smoke default in a post-release verification PR, not in this
release-planning PR.

## Validation

Before tagging or publishing this prerelease, run:

```powershell
python scripts/check_release_version.py v0.3.0-alpha.1
python -m ruff check .
python -m mypy
python -m pyright src
python -m pytest
python -m build
python -m twine check dist/*
python benchmarks/bench_loggamma_methods.py
```

Release-claim guardrails must continue to forbid broad `loggamma`, complex
Stirling, automatic selection of Stirling methods, gamma-ratio asymptotic, and
expanded parabolic-cylinder certification claims.
