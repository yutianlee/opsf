# certsf 0.3.0 Final Release

`v0.3.0` is the first non-prerelease release of the 0.3 line. It packages the
already verified `v0.3.0-alpha.1` through `v0.3.0-alpha.5` scope. It keeps the
0.2 public wrapper surface.

This release is for explicit custom certified positive-real methods on
existing wrappers. It does not make a broad package-wide certification claim,
does not change default method selection, and does not promote the
parabolic-cylinder formula layer beyond `experimental_formula`.
This release keeps the 0.2 public wrapper surface.

The final-readiness audit is recorded in
[`v0.3.0_final_readiness_audit.md`](v0.3.0_final_readiness_audit.md). That
audit concluded that `v0.3.0` final is release-ready subject to final release
checklist execution.

## Release Target

- Python package version: `0.3.0`.
- Git tag: `v0.3.0`.
- GitHub release type: normal release, not prerelease.
- PyPI version after release: `certsf 0.3.0`.

## Active Scope

The v0.3.0 line includes:

- method registry v2 metadata for method id, priority, certificate level, audit
  status, and applicability notes;
- `method=None` and `method="auto"` behavior equivalent to the previous
  automatic selection path;
- `method="arb"` selection for existing certified Arb backends when the
  resolved mode is `certified`;
- explicit `loggamma(x, mode="certified", method="stirling")` for real
  `x >= 20`;
- explicit `loggamma(x, mode="certified", method="stirling_shifted")` for
  real `x >= 20`, using Arb logs and the recurrence
  `loggamma(x) = stirling_loggamma_sum(x+r) - sum(log(x+j))`;
- explicit `loggamma(x, mode="certified", method="certified_auto")` as a
  selector that may choose direct Arb or a positive-real Stirling method
  without changing omitted-method or `method="auto"` dispatch, using
  preselection diagnostics to avoid unnecessary full custom candidate
  evaluations;
- explicit `gamma(x, mode="certified", method="stirling_exp")` for finite real
  `x >= 20`, using a certified positive-real `loggamma` Arb enclosure and Arb
  exponentiation;
- explicit `rgamma(x, mode="certified", method="stirling_recip")` for finite
  real `x >= 20`, using a certified positive-real `loggamma` Arb enclosure and
  Arb exponentiation of the negated enclosure;
- `certificate_scope="stirling_loggamma_positive_real"`;
- `certificate_scope="gamma_positive_real_stirling_exp"`;
- `certificate_scope="rgamma_positive_real_stirling_recip"`;
- `certificate_level="custom_asymptotic_bound"`; and
- `audit_status="theorem_documented"`.

The Stirling, shifted Stirling, certified-auto selector, Stirling-exp gamma
method, and Stirling-recip rgamma method are additional registered methods for
existing public wrappers. They are not new public special-function wrappers
and are not automatic default selection. Default certified `loggamma`, default
certified `gamma`, and default certified `rgamma` remain the existing direct
Arb paths.

Default certified `loggamma` remains direct Arb. Default certified `gamma`
remains direct Arb. Default certified `rgamma` remains direct Arb.

## Non-Goals

The v0.3.0 final release must not broaden certification claims beyond the
documented 0.3 scope.

The v0.3.0 line does not target parabolic-cylinder promotion. The
parabolic-cylinder family remains an `experimental_formula` surface unless a
separate proof, implementation, tests, and documentation change explicitly
broadens that scope.

The v0.3.0 line does not add Faddeeva, `wofz`, or plasma-dispersion wrappers.
It also does not add complex Stirling, complex `gamma` or `rgamma` Stirling
certification, reflection-formula certification, near-pole behavior support,
gamma-ratio asymptotics, or beta asymptotics.

The v0.3.0 line does not make a broad complete-package claim for all
`loggamma`, `gamma`, `rgamma`, or every special-function family. The only
custom asymptotic-bound scopes are the positive-real Stirling `loggamma`
methods documented in [`stirling_loggamma.md`](stirling_loggamma.md) and the
positive-real `gamma` and `rgamma` methods documented in
[`gamma_stirling_exp.md`](gamma_stirling_exp.md) and
[`rgamma_stirling_recip.md`](rgamma_stirling_recip.md).

## Positive-Real `rgamma` via Loggamma Exponentiation

The active explicit positive-real `rgamma(x)` method uses certified `loggamma`
exponentiation. The explicit method name is
`rgamma(x, mode="certified", method="stirling_recip", dps=...)` for finite
real `x >= 20`. The certificate scope is
`rgamma_positive_real_stirling_recip`, with certificate level
`custom_asymptotic_bound` and audit status `theorem_documented`.

This is an active explicit method only; no default dispatch behavior changes.
The method uses a rigorous positive-real `loggamma` enclosure and Arb
exponentiation of the negated enclosure. It avoids computing `gamma(x)` and
then inverting it.

The method excludes complex `rgamma`, real `x < 20`, real `x <= 0`,
non-finite input, reflection-formula paths, near-pole behavior, gamma-ratio
asymptotics, and beta asymptotics. See
[`rgamma_stirling_recip.md`](rgamma_stirling_recip.md).

## Positive-Real `gamma` via Loggamma Exponentiation

The active explicit positive-real `gamma(x)` method uses certified `loggamma`
exponentiation. The explicit method name is
`gamma(x, mode="certified", method="stirling_exp", dps=...)` for finite real
`x >= 20`. The certificate scope is
`gamma_positive_real_stirling_exp`, with certificate level
`custom_asymptotic_bound` and audit status `theorem_documented`.

This is an active explicit method only; no default dispatch behavior changes.
The method uses a rigorous positive-real `loggamma` enclosure and Arb
exponentiation, and the returned `gamma` enclosure accounts for both
finite-expression Arb radius and the propagated explicit loggamma tail bound.

The method excludes complex `gamma`, real `x < 20`, real `x <= 0`,
reflection-formula paths, near-pole behavior, gamma-ratio asymptotics, and beta
asymptotics. See [`gamma_stirling_exp.md`](gamma_stirling_exp.md).

## TestPyPI and PyPI Smoke Plan

Under [`release_policy.md`](release_policy.md), TestPyPI staging is required
or strongly recommended for the first non-prerelease release of the 0.3 line.
Before the real PyPI release, manually run `publish-testpypi` with
`ref=v0.3.0` and `confirm=publish-testpypi`, then verify the staged package
enough to catch packaging and metadata issues.
TestPyPI staging is required or strongly recommended for this final release.
Use `ref=v0.3.0` and `confirm=publish-testpypi` for that staging run.

The final release-planning PR did not update `pypi-smoke.yml` to `0.3.0`.
It remained pinned to the latest verified published prerelease, `0.3.0a5`,
until `certsf 0.3.0` was published to real PyPI and the manual `pypi-smoke`
run against `0.3.0` passed. The post-release smoke-pin follow-up then advances
that default to `0.3.0`.

## Documentation

The line includes:

- [`certified_scope_0_3_0.md`](certified_scope_0_3_0.md), which records the
  0.3.0 support matrix and the narrow active custom-method rows;
- [`stirling_loggamma.md`](stirling_loggamma.md), which records the formula,
  domain, diagnostics, certificate metadata, tail-bound contract, and
  exclusions for the first custom asymptotic method;
- [`loggamma_certified_auto_decision.md`](loggamma_certified_auto_decision.md),
  which records decision support and evidence-gathering notes for any later
  consideration of default certified `loggamma` method selection;
- [`gamma_stirling_exp.md`](gamma_stirling_exp.md), which records the active
  explicit positive-real `gamma` method and its exclusions;
- [`rgamma_stirling_recip.md`](rgamma_stirling_recip.md), which records the
  active explicit positive-real `rgamma` method and its exclusions;
- [`v0_3_custom_method_audit.md`](v0_3_custom_method_audit.md), which
  summarizes all active 0.3 custom methods, their diagnostics, preserved
  default-dispatch behavior, and exclusions;
- [`v0.3.0_final_readiness_audit.md`](v0.3.0_final_readiness_audit.md), which
  records the final readiness decision and release-sequence implications;
- [`release-0.3.0-alpha.5.md`](release-0.3.0-alpha.5.md), which records the
  prerelease plan for packaging the explicit positive-real `rgamma`
  `method="stirling_recip"` with no default-dispatch change;
- [`release-0.3.0-alpha.4.md`](release-0.3.0-alpha.4.md), which records the
  prerelease plan for packaging the explicit positive-real `gamma`
  `method="stirling_exp"` with no default-dispatch change; and
- [`release-0.3.0-alpha.3.md`](release-0.3.0-alpha.3.md), which records the
  prerelease plan for packaging the explicit `certified_auto` preselection
  optimization with no default-dispatch change.

## Benchmarks

The manual benchmark
[`benchmarks/bench_loggamma_methods.py`](../benchmarks/bench_loggamma_methods.py)
emits JSON-lines timing records for direct Arb certified `loggamma`, explicit
Stirling, explicit shifted Stirling, explicit certified-auto selection,
high-precision mpmath, and fast SciPy over representative positive real inputs.
It is evidence-gathering infrastructure only; custom methods and the selector
remain explicit and are not claimed as the faster or default method.

The manual benchmark
[`benchmarks/bench_gamma_methods.py`](../benchmarks/bench_gamma_methods.py)
emits JSON-lines timing and diagnostic records for direct Arb certified
`gamma`, explicit `method="stirling_exp"`, high-precision mpmath, and fast
SciPy over representative positive real inputs. It is evidence gathering only:
`method="stirling_exp"` remains explicit, direct Arb remains the default
certified `gamma` path, and this document does not claim performance
superiority.

The manual benchmark
[`benchmarks/bench_rgamma_methods.py`](../benchmarks/bench_rgamma_methods.py)
emits JSON-lines timing and diagnostic records for direct Arb certified
`rgamma`, explicit `method="stirling_recip"`, high-precision mpmath, and fast
SciPy over representative positive real inputs. It is evidence gathering only:
`method="stirling_recip"` remains explicit, direct Arb remains the default
certified `rgamma` path, and this document does not claim performance
superiority.

The decision-support analyzer
[`benchmarks/analyze_loggamma_auto.py`](../benchmarks/analyze_loggamma_auto.py)
compares direct Arb, explicit unshifted Stirling, explicit shifted Stirling,
and explicit `method="certified_auto"` over a broader certified-mode grid. It
records unsupported explicit Stirling cases as structured failures. This is
evidence gathering only: `certified_auto` remains explicit, and this document
does not make any default-dispatch change.

The summary helper
[`benchmarks/summarize_loggamma_auto.py`](../benchmarks/summarize_loggamma_auto.py)
reduces analyzer JSON-lines output into certified counts, selector choices,
timing comparisons, and failure-pattern summaries. A compact generated sample
is stored at
[`docs/benchmark_samples/loggamma_certified_auto_sample_summary.json`](benchmark_samples/loggamma_certified_auto_sample_summary.json).
The current recommendation remains conservative: direct Arb stays the default
certified `loggamma` method, `method="certified_auto"` stays explicit, and no
default-dispatch change is made in this release.

## Validation Expectations

Validation should confirm that:

- explicit `method="stirling"` and `method="stirling_shifted"` certify
  positive-real `loggamma` only for real `x >= 20`;
- explicit `method="certified_auto"` may select direct Arb or a positive-real
  Stirling method, while preserving the selected backend's certificate scope;
- explicit `method="stirling_exp"` certifies `gamma` only for finite real
  `x >= 20`;
- explicit `method="stirling_recip"` certifies `rgamma` only for finite real
  `x >= 20`;
- default certified `loggamma` and explicit `method="arb"` continue to use the
  existing direct Arb path;
- default certified `gamma` and explicit `method="arb"` continue to use the
  existing direct Arb path;
- default certified `rgamma` and explicit `method="arb"` continue to use the
  existing direct Arb path;
- unsupported domains and unsupported modes fail cleanly rather than falling
  back to mpmath in certified mode;
- release metadata changes are limited to the dedicated final release-planning
  PR;
- the post-release smoke-pin follow-up advances `pypi-smoke.yml` to `0.3.0`
  only after final real PyPI smoke passes; and
- no parabolic-cylinder, Faddeeva, `wofz`, or plasma-dispersion support claim is
  added.

## Final Release Checklist

Before publishing:

```powershell
python scripts/check_release_version.py v0.3.0
python -m ruff check .
python -m mypy
python -m pyright src
python -m pytest
python -m build
python -m twine check dist/*
```

After this final release-planning PR merges, the release operator should:

1. Tag the final `main` commit as `v0.3.0`.
2. Stage to TestPyPI with `publish-testpypi.yml` using `ref=v0.3.0` and
   `confirm=publish-testpypi`.
3. Verify the TestPyPI package.
4. Create a normal GitHub release for `v0.3.0`.
5. Confirm the protected `publish-pypi` workflow publishes `certsf 0.3.0`.
6. Verify real PyPI clean installs for base, certified, and MCP/certified
   extras.
7. Run manual `pypi-smoke` with `version=0.3.0`.
8. Record post-release evidence in a follow-up PR.
9. Only after the real PyPI smoke passes, open a separate smoke-pin PR to
   advance `pypi-smoke.yml` to `0.3.0`.
