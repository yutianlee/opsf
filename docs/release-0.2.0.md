# certsf 0.2.0

`v0.2.0` is the first non-prerelease release of the 0.2 line. It freezes the
same public API as `0.2.0-alpha.10` and promotes the release metadata from the
latest alpha to a normal release without changing runtime behavior.

The release-planning PR is metadata, documentation, workflow-default, and
release-hygiene-test only. It does not include `src/` changes, backend formula
changes, public-wrapper changes, behavior changes, or certification-scope
broadening.

## Scientific Scope

The package remains alpha-quality in scientific scope. Certified mode reports
rigorous Arb enclosures where a documented certified path exists, but the
release does not claim complete coverage of each special-function family.

Direct Arb primitive families are certified only on their documented
finite-enclosure domains. Formula-backed wrappers are certified only for the
explicitly documented formula enclosures, with formula and scope diagnostics
kept visible to callers.

`erfinv` and `erfcinv` are real principal branches only:

- `erfinv(x)` is supported for real `-1 < x < 1`.
- `erfcinv(x)` is supported for real `0 < x < 2`.

No complex inverse error-function branches are certified. No endpoint
asymptotic certification is claimed.

Parabolic-cylinder wrappers remain `experimental_formula`. The release does
not broaden their formula, branch, domain, or certification claims.

No custom Taylor/asymptotic certification methods are claimed.

## Public API Scope

The public API is unchanged from `0.2.0-alpha.10`. The 0.2 line includes:

- `gamma_ratio(a, b)`, `loggamma_ratio(a, b)`, `beta(a, b)`, and
  `pochhammer(a, n)`;
- `erf(z)`, `erfc(z)`, `erfcx(z)`, `erfi(z)`, and `dawson(z)`;
- real-only `erfinv(x)` on `-1 < x < 1`; and
- real-only `erfcinv(x)` on `0 < x < 2`.

No new public wrappers are added since `0.2.0-alpha.10`, and no mathematical
implementation changes are included since `0.2.0-alpha.10`.

## Release Policy

Under [`release_policy.md`](release_policy.md), this final release should be
staged to TestPyPI before the real PyPI release. The reason is that `v0.2.0` is
the first non-prerelease release of the 0.2 line and updates publish workflow
defaults from the latest alpha tag to the final tag.

Before the real PyPI release, manually run `publish-testpypi` with
`ref=v0.2.0` and `confirm=publish-testpypi`. Keep the TestPyPI confirmation
guard in place.

Do not update `pypi-smoke.yml` to `0.2.0` until after `certsf 0.2.0` is
actually published to PyPI. Until then, the smoke default remains `0.2.0a10`.

## Validation Before Tagging

Before tagging or publishing this release, run:

```powershell
python scripts/check_release_version.py v0.2.0
python -m ruff check .
python -m mypy
python -m pytest
python -m build
python -m twine check dist/*
```
