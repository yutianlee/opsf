# Release Checklist

Use this checklist before cutting any GitHub prerelease or release. For alpha
releases, keep the wording conservative: the package has certified Arb
enclosures for documented scopes, but the parabolic-cylinder formula layer
remains experimental until the formula audit is complete.

Release publishing policy is recorded in
[`release_policy.md`](release_policy.md).

## Required Checks

- [ ] CI green on Python 3.10, 3.11, and 3.12.
- [ ] Base install passes without `python-flint`.
- [ ] Certified install passes with `python-flint`.
- [ ] `examples/basic_usage.py` works.
- [ ] `examples/certified_vs_high_precision.py` works.
- [ ] Release examples print full payloads:
  `gamma_certified.py`, `airy_components.py`, `bessel_complex.py`,
  `pcf_experimental.py`, and `mcp_payload.py`.
- [ ] MCP server imports and registers tools.
- [ ] Certification docs and family certification audits reviewed.
- [ ] Release-claim guardrails reviewed; package metadata and release copy keep alpha/formula-audit wording.
- [ ] Current alpha certified scope reviewed; no new public special-function
  wrappers added beyond the planned release scope.
- [ ] Formula audit reviewed for any changed formula path.
- [ ] Unsupported certified domains fail cleanly.
- [ ] `CHANGELOG.md` updated.
- [ ] `CITATION.cff` version matches the release name.
- [ ] `pyproject.toml` version uses the matching PEP 440 form.
- [ ] Tag/version parity check passes before any publishing workflow builds distributions.
- [ ] `release-checks` workflow is green.
- [ ] Package builds with `python -m build`.
- [ ] Package metadata passes `python -m twine check dist/*`.
- [ ] Wheel installs in a clean virtual environment.
- [ ] GitHub release is marked prerelease for alpha tags.
- [ ] GitHub release is a normal release, not a prerelease, for final tags.
- [ ] Decide whether TestPyPI staging is needed under
  [`release_policy.md`](release_policy.md).

## Command Hints

```powershell
python -m pip install -e ".[dev]"
python -m ruff check src tests examples
python -m mypy
python -m pyright src
python -m pytest
python -m pytest tests/test_release_claims.py
python scripts/check_release_version.py v0.2.0
python -m build
python -m twine check dist/*
python examples/basic_usage.py
python examples/certified_vs_high_precision.py
python examples/gamma_certified.py
python examples/airy_components.py
python examples/bessel_complex.py
python examples/pcf_experimental.py
python examples/mcp_payload.py
python -c "from certsf.mcp_server import build_server; build_server()"
```

For an alpha tag, use a Git tag such as `v0.1.0-alpha.3` and a Python package
version such as `0.1.0a3`.

For the final 0.1.0 tag, use `v0.1.0` and Python package version `0.1.0`.

## Publishing Workflows

- TestPyPI publishing is manual-only through `publish-testpypi`; it keeps the
  current planned release tag as the default dispatch ref.
- Routine feature alpha releases may skip TestPyPI if build, `twine check`,
  tag/version parity, protected PyPI publish, and real PyPI smoke all pass.
- Real PyPI publishing runs from GitHub release/prerelease publication events
  through `publish-pypi`.
- Publishing workflows must pass the tag/version parity check before building:
  `v0.2.0` maps to `0.2.0`,
  `v0.2.0-alpha.10` maps to `0.2.0a10`,
  `v0.2.0-alpha.9` maps to `0.2.0a9`,
  `v0.2.0-alpha.8` maps to `0.2.0a8`,
  `v0.2.0-alpha.7` maps to `0.2.0a7`,
  `v0.2.0-alpha.6` maps to `0.2.0a6`,
  `v0.2.0-alpha.5` maps to `0.2.0a5`,
  `v0.2.0-alpha.4` maps to `0.2.0a4`,
  `v0.2.0-alpha.3` maps to `0.2.0a3`,
  `v0.2.0-alpha.2` maps to `0.2.0a2`,
  `v0.2.0-alpha.1` maps to `0.2.0a1`,
  `v0.1.0-alpha.3` maps to `0.1.0a3`, and `v0.1.0` maps to `0.1.0`.

## v0.2.0 Checklist

- [ ] `pyproject.toml` version is `0.2.0`.
- [ ] `CITATION.cff` version is `0.2.0`.
- [ ] `CITATION.cff` date-released is `2026-05-09`.
- [ ] `CHANGELOG.md` records the first non-prerelease 0.2 line release.
- [ ] `docs/release-0.2.0.md` is reviewed.
- [ ] Publish workflow defaults point at `v0.2.0`.
- [ ] PyPI smoke workflow still targets `0.2.0a10` until `0.2.0` is
  published.
- [ ] GitHub release for `v0.2.0` is a normal release, not a prerelease.
- [ ] Stage to TestPyPI under `release_policy.md` because this is the first
  non-prerelease release of the 0.2 line and publish workflow defaults changed.
- [ ] Manually run `publish-testpypi` with `ref=v0.2.0` and
  `confirm=publish-testpypi` before the real PyPI release.
- [ ] Keep the TestPyPI confirm guard in `publish-testpypi.yml`.
- [ ] No `src/` changes are included in the release-planning PR.
- [ ] No backend formula changes are included.
- [ ] No public-wrapper changes are included.
- [ ] The same public API as `0.2.0-alpha.10` is retained.
- [ ] Release copy includes `gamma_ratio`, `loggamma_ratio`, `beta`, and
  `pochhammer`.
- [ ] Release copy includes `erf`, `erfc`, `erfcx`, `erfi`, and `dawson`.
- [ ] Release copy includes real-only `erfinv` on `-1 < x < 1`.
- [ ] Release copy includes real-only `erfcinv` on `0 < x < 2`.
- [ ] Release copy says no new public wrappers are added since
  `0.2.0-alpha.10`.
- [ ] Release copy says no mathematical implementation changes are included
  since `0.2.0-alpha.10`.
- [ ] Release copy does not broaden certification claims.
- [ ] Direct Arb primitive families remain certified only on documented
  finite-enclosure domains.
- [ ] Formula-backed wrappers remain certified only for explicitly documented
  formula enclosures.
- [ ] No complex inverse error-function branches are certified.
- [ ] Parabolic-cylinder wrappers remain `experimental_formula`.
- [ ] No custom Taylor/asymptotic certification methods are claimed.
- [ ] `python scripts/check_release_version.py v0.2.0` passes.
- [ ] `python -m ruff check .` passes.
- [ ] `python -m mypy` passes.
- [ ] `python -m pytest` passes.
- [ ] `python -m build` passes.
- [ ] `python -m twine check dist/*` passes.

## v0.2.0-alpha.10 Checklist

- [ ] `pyproject.toml` version is `0.2.0a10`.
- [ ] `CITATION.cff` version is `0.2.0-alpha.10`.
- [ ] `CITATION.cff` date-released is `2026-05-09`.
- [ ] `CHANGELOG.md` records `erfcinv(x)` as the only public API expansion
  since `0.2.0-alpha.9`.
- [ ] `docs/release-0.2.0-alpha.10.md` is reviewed.
- [ ] Publish workflow defaults point at `v0.2.0-alpha.10`.
- [ ] PyPI smoke workflow still targets `0.2.0a9` until `0.2.0a10` is
  published.
- [ ] TestPyPI staging is skipped for this routine feature alpha unless
  packaging or workflow risk is introduced under `release_policy.md`.
- [ ] No `src/` changes are included in the release-planning PR.
- [ ] No backend formula changes are included.
- [ ] No public-wrapper changes beyond the already-merged `erfcinv(x)` are
  included.
- [ ] Release copy defines `erfcinv(x)` as the real principal inverse of
  `erfc` on `x in (0, 2)`.
- [ ] Release copy says fast mode uses `scipy.special.erfcinv(x)`.
- [ ] Release copy says high-precision mode uses a mpmath inverse when
  available and otherwise uses `erfinv(1-x)`.
- [ ] Release copy says certified mode supports real `x` only with
  `0 < x < 2`.
- [ ] Release copy says certified mode prefers direct Arb `erfcinv` when
  available and otherwise uses the certified `erfinv(1-x)` fallback.
- [ ] Release copy says endpoints, out-of-domain real inputs, and complex
  inputs fail cleanly in certified mode.
- [ ] Release copy does not imply complex inverse branches, endpoint asymptotic
  certification, Faddeeva/wofz, or plasma dispersion wrappers.
- [ ] No `erfinv` behavior change is included.
- [ ] No existing error-function behavior change is included.
- [ ] No gamma-family behavior change is included.
- [ ] No parabolic-cylinder claim broadening is included.
- [ ] Parabolic-cylinder wrappers remain `experimental_formula`.
- [ ] `python scripts/check_release_version.py v0.2.0-alpha.10` passes.
- [ ] `python -m ruff check .` passes.
- [ ] `python -m mypy` passes.
- [ ] `python -m pytest` passes.
- [ ] `python -m build` passes.
- [ ] `python -m twine check dist/*` passes.

## v0.2.0-alpha.9 Checklist

- [ ] `pyproject.toml` version is `0.2.0a9`.
- [ ] `CITATION.cff` version is `0.2.0-alpha.9`.
- [ ] `CITATION.cff` date-released is `2026-05-09`.
- [ ] `CHANGELOG.md` records `erfinv(x)` as the only public API expansion
  since `0.2.0-alpha.8`.
- [ ] `docs/release-0.2.0-alpha.9.md` is reviewed.
- [ ] Publish workflow defaults point at `v0.2.0-alpha.9`.
- [ ] PyPI smoke workflow still targets `0.2.0a8` until `0.2.0a9` is
  published.
- [ ] TestPyPI staging is skipped for this routine feature alpha unless
  packaging or workflow risk is introduced under `release_policy.md`.
- [ ] No `src/` changes are included in the release-planning PR.
- [ ] No backend formula changes are included.
- [ ] No public-wrapper changes beyond the already-merged `erfinv(x)` are
  included.
- [ ] Release copy defines `erfinv(x)` as the real principal inverse of `erf`
  on `x in (-1, 1)`.
- [ ] Release copy says fast mode uses `scipy.special.erfinv(x)`.
- [ ] Release copy says high-precision mode uses `mpmath.erfinv(x)` when
  available and otherwise solves `erf(y) = x` numerically.
- [ ] Release copy says certified mode supports real `x` only with
  `-1 < x < 1`.
- [ ] Release copy says certified mode prefers direct Arb `erfinv` when
  available and otherwise uses a certified monotone real-root enclosure for
  `erf(y)-x=0`.
- [ ] Release copy says endpoints, out-of-domain real inputs, and complex
  inputs fail cleanly in certified mode.
- [ ] Release copy does not imply `erfcinv`, complex inverse branches,
  Faddeeva/wofz, plasma dispersion, or endpoint asymptotic certification.
- [ ] No error-function-family behavior change outside `erfinv` is included.
- [ ] No gamma-family behavior change is included.
- [ ] No parabolic-cylinder claim broadening is included.
- [ ] Parabolic-cylinder wrappers remain `experimental_formula`.
- [ ] `python scripts/check_release_version.py v0.2.0-alpha.9` passes.
- [ ] `python -m ruff check .` passes.
- [ ] `python -m mypy` passes.
- [ ] `python -m pytest` passes.
- [ ] `python -m build` passes.
- [ ] `python -m twine check dist/*` passes.

## v0.2.0-alpha.8 Checklist

- [ ] `pyproject.toml` version is `0.2.0a8`.
- [ ] `CITATION.cff` version is `0.2.0-alpha.8`.
- [ ] `CITATION.cff` date-released is `2026-05-09`.
- [ ] `CHANGELOG.md` records `dawson(z)` as the only public API expansion
  since `0.2.0-alpha.7`.
- [ ] `docs/release-0.2.0-alpha.8.md` is reviewed.
- [ ] Publish workflow defaults point at `v0.2.0-alpha.8`.
- [ ] PyPI smoke workflow still targets `0.2.0a7` until `0.2.0a8` is
  published.
- [ ] TestPyPI staging is skipped for this routine feature alpha unless
  packaging or workflow risk is introduced under `release_policy.md`.
- [ ] No `src/` changes are included in the release-planning PR.
- [ ] No backend formula changes are included.
- [ ] No public-wrapper changes beyond the already-merged `dawson(z)` are
  included.
- [ ] Release copy defines `dawson(z)` as
  `sqrt(pi)/2 * exp(-z^2) * erfi(z)`.
- [ ] Release copy says fast mode uses `scipy.special.dawsn(z)` when available
  and otherwise uses the `erfi` identity fallback.
- [ ] Release copy says high-precision mode uses a mpmath Dawson function when
  available and otherwise uses the `erfi` identity fallback.
- [ ] Release copy says certified mode prefers direct Arb Dawson when available
  and otherwise uses the Arb formula `sqrt(pi)/2*exp(-z^2)*erfi(z)`.
- [ ] Release copy does not imply custom Taylor/asymptotic certification.
- [ ] Release copy does not imply inverse error functions, Faddeeva functions,
  plasma dispersion, or additional variants are included.
- [ ] No `erf`, `erfc`, `erfcx`, or `erfi` behavior change is included.
- [ ] No gamma-family behavior change is included.
- [ ] No parabolic-cylinder claim broadening is included.
- [ ] Parabolic-cylinder wrappers remain `experimental_formula`.
- [ ] `python scripts/check_release_version.py v0.2.0-alpha.8` passes.
- [ ] `python -m ruff check .` passes.
- [ ] `python -m mypy` passes.
- [ ] `python -m pytest` passes.
- [ ] `python -m build` passes.
- [ ] `python -m twine check dist/*` passes.

## v0.2.0-alpha.7 Checklist

- [ ] `pyproject.toml` version is `0.2.0a7`.
- [ ] `CITATION.cff` version is `0.2.0-alpha.7`.
- [ ] `CITATION.cff` date-released is `2026-05-09`.
- [ ] `CHANGELOG.md` records `erfi(z)` as the only public API expansion since
  `0.2.0-alpha.6`.
- [ ] `docs/release-0.2.0-alpha.7.md` is reviewed.
- [ ] Publish workflow defaults point at `v0.2.0-alpha.7`.
- [ ] PyPI smoke workflow still targets `0.2.0a6` until `0.2.0a7` is
  published.
- [ ] No `src/` changes are included in the release-planning PR.
- [ ] No backend formula changes are included.
- [ ] No public-wrapper changes beyond the already-merged `erfi(z)` are
  included.
- [ ] Release copy defines `erfi(z)` as `-i erf(i z)`.
- [ ] Release copy says fast mode uses `scipy.special.erfi(z)` when available
  and otherwise uses the formula fallback.
- [ ] Release copy says high-precision mode uses `mpmath.erfi(z)` when
  available and otherwise uses the formula fallback.
- [ ] Release copy says certified mode prefers direct Arb `erfi` when available
  and otherwise uses the Arb formula `-i*erf(i*z)`.
- [ ] Release copy does not imply custom Taylor/asymptotic certification.
- [ ] Release copy does not imply `erfinv`, `erfcinv`, Faddeeva, Dawson, or
  other error-function variants are included.
- [ ] No `erf`, `erfc`, or `erfcx` behavior change is included.
- [ ] No gamma-family behavior change is included.
- [ ] No parabolic-cylinder claim broadening is included.
- [ ] Parabolic-cylinder wrappers remain `experimental_formula`.
- [ ] `python scripts/check_release_version.py v0.2.0-alpha.7` passes.
- [ ] `python -m ruff check .` passes.
- [ ] `python -m mypy` passes.
- [ ] `python -m pytest` passes.
- [ ] `python -m build` passes.
- [ ] `python -m twine check dist/*` passes.

## v0.2.0-alpha.6 Checklist

- [ ] `pyproject.toml` version is `0.2.0a6`.
- [ ] `CITATION.cff` version is `0.2.0-alpha.6`.
- [ ] `CITATION.cff` date-released is `2026-05-09`.
- [ ] `CHANGELOG.md` records `erfcx(z)` as the only public API expansion since
  `0.2.0-alpha.5`.
- [ ] `docs/release-0.2.0-alpha.6.md` is reviewed.
- [ ] Publish workflow defaults point at `v0.2.0-alpha.6`.
- [ ] PyPI smoke workflow still targets `0.2.0a5` until `0.2.0a6` is
  published.
- [ ] No `src/` changes are included in the release-planning PR.
- [ ] No backend formula changes are included.
- [ ] No public-wrapper changes beyond the already-merged `erfcx(z)` are
  included.
- [ ] Release copy defines `erfcx(z)` as `exp(z^2) erfc(z)`.
- [ ] Release copy says fast mode uses `scipy.special.erfcx(z)`.
- [ ] Release copy says high-precision mode uses mpmath evaluation of
  `exp(z*z) * erfc(z)`.
- [ ] Release copy says certified mode prefers direct Arb `erfcx` when
  available and otherwise uses the Arb formula `exp(z^2)*erfc(z)`.
- [ ] Release copy does not imply custom Taylor/asymptotic certification.
- [ ] Release copy does not imply `erfi`, `erfinv`, `erfcinv`, Faddeeva, or
  other error-function wrappers are included.
- [ ] No `erf` or `erfc` behavior change is included.
- [ ] No gamma-family behavior change is included.
- [ ] No parabolic-cylinder claim broadening is included.
- [ ] Parabolic-cylinder wrappers remain `experimental_formula`.
- [ ] `python scripts/check_release_version.py v0.2.0-alpha.6` passes.
- [ ] `python -m ruff check .` passes.
- [ ] `python -m mypy` passes.
- [ ] `python -m pytest` passes.
- [ ] `python -m build` passes.
- [ ] `python -m twine check dist/*` passes.

## v0.2.0-alpha.5 Checklist

- [ ] `pyproject.toml` version is `0.2.0a5`.
- [ ] `CITATION.cff` version is `0.2.0-alpha.5`.
- [ ] `CITATION.cff` date-released is `2026-05-09`.
- [ ] `CHANGELOG.md` records `erf(z)` and `erfc(z)` as the only public API
  expansions since `0.2.0-alpha.4`.
- [ ] `docs/release-0.2.0-alpha.5.md` is reviewed.
- [ ] Publish workflow defaults point at `v0.2.0-alpha.5`.
- [ ] PyPI smoke workflow still targets `0.2.0a4` until `0.2.0a5` is
  published.
- [ ] No `src/` changes are included in the release-planning PR.
- [ ] No backend formula changes are included.
- [ ] No public-wrapper changes beyond the already-merged `erf(z)` and
  `erfc(z)` are included.
- [ ] `erf` certified scope remains `direct_arb_erf`.
- [ ] `erfc` certified scope remains `direct_arb_erfc`.
- [ ] Release copy says certified `erf` uses the direct Arb `erf` primitive.
- [ ] Release copy says certified `erfc` uses the direct Arb `erfc` primitive
  when available, with the documented Arb fallback `1 - erf(z)` only if
  necessary.
- [ ] Release copy does not imply custom Taylor/asymptotic certification.
- [ ] Release copy does not imply inverse, imaginary, scaled, or other
  error-function wrappers are included.
- [ ] No gamma-family behavior change is included.
- [ ] No parabolic-cylinder claim broadening is included.
- [ ] Parabolic-cylinder wrappers remain `experimental_formula`.
- [ ] `python scripts/check_release_version.py v0.2.0-alpha.5` passes.
- [ ] `python -m ruff check .` passes.
- [ ] `python -m mypy` passes.
- [ ] `python -m pytest` passes.
- [ ] `python -m build` passes.
- [ ] `python -m twine check dist/*` passes.

## v0.2.0-alpha.4 Checklist

- [ ] `pyproject.toml` version is `0.2.0a4`.
- [ ] `CITATION.cff` version is `0.2.0-alpha.4`.
- [ ] `CHANGELOG.md` records `pochhammer(a, n)` as the only public API
  expansion since `0.2.0-alpha.3`.
- [ ] `docs/release-0.2.0-alpha.4.md` is reviewed.
- [ ] Publish workflow defaults point at `v0.2.0-alpha.4`.
- [ ] PyPI smoke workflow still targets `0.2.0a3` until `0.2.0a4` is
  published.
- [ ] No `src/` changes are included in the release-planning PR.
- [ ] No backend formula changes are included.
- [ ] No public-wrapper changes beyond the already-merged `pochhammer(a, n)`
  are included.
- [ ] `pochhammer` certified scope remains `direct_arb_pochhammer_product`.
- [ ] `pochhammer` release copy describes only the finite Arb product
  `prod_{k=0}^{n-1}(a+k)` for exact integer `n >= 0`.
- [ ] Release copy says `n = 0` certifies to `1` and exact zero factors certify
  to zero.
- [ ] Release copy says non-integer `n`, negative `n`, oversized product paths,
  and simultaneous gamma-pole limiting values fail cleanly.
- [ ] Release copy does not imply that analytic continuation in `n` is
  certified.
- [ ] Release copy does not imply that simultaneous gamma-pole limiting values
  are certified.
- [ ] No `beta`, `gamma_ratio`, or `loggamma_ratio` behavior change is
  included.
- [ ] No parabolic-cylinder claim broadening is included.
- [ ] Parabolic-cylinder wrappers remain `experimental_formula`.
- [ ] Custom Taylor/asymptotic methods are still not included.
- [ ] `python scripts/check_release_version.py v0.2.0-alpha.4` passes.
- [ ] `python -m ruff check .` passes.
- [ ] `python -m mypy` passes.
- [ ] `python -m pytest` passes.
- [ ] `python -m build` passes.
- [ ] `python -m twine check dist/*` passes.

## v0.2.0-alpha.3 Checklist

- [ ] `pyproject.toml` version is `0.2.0a3`.
- [ ] `CITATION.cff` version is `0.2.0-alpha.3`.
- [ ] `CHANGELOG.md` records `beta(a, b)` as the only public API expansion
  since `0.2.0-alpha.2`.
- [ ] `docs/release-0.2.0-alpha.3.md` is reviewed.
- [ ] Publish workflow defaults point at `v0.2.0-alpha.3`.
- [ ] PyPI smoke workflow still targets `0.2.0a2` until `0.2.0a3` is
  published.
- [ ] No `src/` changes are included in the release-planning PR.
- [ ] No backend formula changes are included.
- [ ] No public-wrapper changes beyond the already-merged `beta(a, b)` are
  included.
- [ ] `beta` certified scope remains `direct_arb_beta`.
- [ ] `beta` release copy describes only the narrow Arb
  `Gamma(a) * Gamma(b) * rgamma(a+b)` product.
- [ ] Release copy says denominator or sum-pole zeros certify only when
  `Gamma(a)` and `Gamma(b)` are finite.
- [ ] Release copy does not imply that all beta-function analytic continuations
  or singular limits are certified.
- [ ] Release copy does not imply that simultaneous-pole limiting values are
  certified.
- [ ] No `gamma_ratio` or `loggamma_ratio` behavior change is included.
- [ ] No parabolic-cylinder claim broadening is included.
- [ ] Parabolic-cylinder wrappers remain `experimental_formula`.
- [ ] Custom Taylor/asymptotic methods are still not included.
- [ ] `python scripts/check_release_version.py v0.2.0-alpha.3` passes.
- [ ] `python -m ruff check .` passes.
- [ ] `python -m mypy` passes.
- [ ] `python -m pytest` passes.
- [ ] `python -m build` passes.
- [ ] `python -m twine check dist/*` passes.

## v0.2.0-alpha.2 Checklist

- [ ] `pyproject.toml` version is `0.2.0a2`.
- [ ] `CITATION.cff` version is `0.2.0-alpha.2`.
- [ ] `CHANGELOG.md` records `loggamma_ratio(a, b)` as the only public API
  expansion since `0.2.0-alpha.1`.
- [ ] `docs/release-0.2.0-alpha.2.md` is reviewed.
- [ ] Publish workflow defaults point at `v0.2.0-alpha.2`.
- [ ] PyPI smoke workflow still targets `0.2.0a1` until `0.2.0a2` is
  published.
- [ ] No `src/` changes are included in the release-planning PR.
- [ ] No backend formula changes are included.
- [ ] No public-wrapper changes beyond the already-merged `loggamma_ratio` are
  included.
- [ ] `loggamma_ratio` certified scope remains `direct_arb_loggamma_ratio`.
- [ ] `loggamma_ratio` release copy describes only the narrow Arb
  `lgamma(a) - lgamma(b)` principal-loggamma difference.
- [ ] Release copy does not imply that complex `loggamma_ratio` is the
  principal logarithm of `gamma_ratio(a, b)`.
- [ ] Release copy does not imply that pole limiting values are certified.
- [ ] No `gamma_ratio` behavior change is included.
- [ ] No parabolic-cylinder claim broadening is included.
- [ ] Parabolic-cylinder wrappers remain `experimental_formula`.
- [ ] Custom Taylor/asymptotic methods are still not included.
- [ ] `python scripts/check_release_version.py v0.2.0-alpha.2` passes.
- [ ] `python -m ruff check .` passes.
- [ ] `python -m mypy` passes.
- [ ] `python -m pytest` passes.
- [ ] `python -m build` passes.
- [ ] `python -m twine check dist/*` passes.

## v0.2.0-alpha.1 Checklist

- [ ] `pyproject.toml` version is `0.2.0a1`.
- [ ] `CITATION.cff` version is `0.2.0-alpha.1`.
- [ ] `CHANGELOG.md` records `gamma_ratio(a, b)` as the only public API
  expansion for the 0.2.0 alpha line.
- [ ] `docs/release-0.2.0-alpha.1.md` is reviewed.
- [ ] Publish workflow defaults point at `v0.2.0-alpha.1`.
- [ ] PyPI smoke workflow still targets the latest actually published version
  until `0.2.0a1` is published.
- [ ] No `src/` changes are included in the release-planning PR.
- [ ] No backend formula changes are included.
- [ ] No new public wrappers beyond the already-merged `gamma_ratio` are
  included.
- [ ] `gamma_ratio` certified scope remains `direct_arb_gamma_ratio`.
- [ ] `gamma_ratio` release copy describes only the narrow Arb
  `Gamma(a) * rgamma(b)` product, denominator-pole zeros when `Gamma(a)` is
  finite, and clean failures for numerator poles and simultaneous poles.
- [ ] Release copy does not imply that all gamma-family ratios or
  simultaneous-pole limits are certified.
- [ ] No parabolic-cylinder claim broadening is included.
- [ ] Parabolic-cylinder wrappers remain `experimental_formula`.
- [ ] Custom Taylor/asymptotic methods are still not included.
- [ ] `python scripts/check_release_version.py v0.2.0-alpha.1` passes.
- [ ] `python -m ruff check .` passes.
- [ ] `python -m mypy` passes.
- [ ] `python -m pytest` passes.
- [ ] `python -m build` passes.
- [ ] `python -m twine check dist/*` passes.

## v0.1.0 Checklist

- [ ] `pyproject.toml` version is `0.1.0`.
- [ ] `CITATION.cff` version is `0.1.0`.
- [ ] `CHANGELOG.md` records the first non-prerelease package release.
- [ ] `docs/release-0.1.0.md` is reviewed.
- [ ] README PyPI install instructions use stable install commands, with a
  short note that prereleases require `--pre`.
- [ ] Publish workflow defaults point at `v0.1.0`.
- [ ] PyPI smoke workflow still targets the latest actually published version
  until `v0.1.0` is published.
- [ ] GitHub release for `v0.1.0` is not marked prerelease.
- [ ] No mathematical implementation changes from `0.1.0-alpha.3` are included.
- [ ] No new public wrappers are included.
- [ ] The same frozen public API as `0.1.0-alpha.3` is retained.
- [ ] Release copy does not broaden certification claims.
- [ ] Frozen 0.1.0 certified scope is unchanged.
- [ ] Parabolic-cylinder wrappers remain `experimental_formula`.
- [ ] Direct Arb primitive families remain described as alpha-certified on
  documented finite-enclosure domains.
- [ ] Unsupported certified domains fail cleanly as non-certified results.
- [ ] No custom Taylor/asymptotic methods are included.
- [ ] `python scripts/check_release_version.py v0.1.0` passes.
- [ ] `python -m ruff check .` passes.
- [ ] `python -m mypy` passes.
- [ ] `python -m pytest` passes.
- [ ] `python -m build` passes.
- [ ] `python -m twine check dist/*` passes.

## v0.1.0-alpha.3 Checklist

- [ ] `pyproject.toml` version is `0.1.0a3`.
- [ ] `CITATION.cff` version is `0.1.0-alpha.3`.
- [ ] `CHANGELOG.md` records formula-audit grids, external fixtures, and
  release-workflow hardening.
- [ ] `docs/release-0.1.0-alpha.3.md` is reviewed.
- [ ] PyPI smoke workflow still targets the latest actually published version
  until alpha.3 is published.
- [ ] No mathematical implementation changes are included.
- [ ] No new public wrappers are included.
- [ ] Release copy does not broaden certification claims.
- [ ] Frozen 0.1.0 certified scope is unchanged.
- [ ] Parabolic-cylinder wrappers remain `experimental_formula`.
- [ ] External fixtures are described as supplemental to formula/domain audit.
- [ ] `python scripts/check_release_version.py v0.1.0-alpha.3` passes.
- [ ] `python -m ruff check .` passes.
- [ ] `python -m mypy` passes.
- [ ] `python -m pytest` passes.
- [ ] `python -m build` passes.
- [ ] `python -m twine check dist/*` passes.

## v0.1.0-alpha.2 Checklist

- [ ] `pyproject.toml` version is `0.1.0a2`.
- [ ] `CITATION.cff` version is `0.1.0-alpha.2`.
- [ ] `CHANGELOG.md` records post-release hardening since `v0.1.0-alpha.1`.
- [ ] `docs/release-0.1.0-alpha.2.md` is reviewed.
- [ ] README PyPI install instructions still use prerelease-aware commands.
- [ ] No mathematical implementation changes are included.
- [ ] No new public wrappers are included.
- [ ] Release copy does not broaden certification claims.
- [ ] Frozen 0.1.0 certified scope is unchanged.
- [ ] `python scripts/check_release_version.py v0.1.0-alpha.2` passes.
- [ ] `python -m ruff check .` passes.
- [ ] `python -m mypy` passes.
- [ ] `python -m pytest` passes.
- [ ] `python -m build` passes.
- [ ] `python -m twine check dist/*` passes.

## v0.1.0-alpha.1 Snapshot

- [x] CI green on Python 3.10, 3.11, and 3.12.
- [x] Base and certified test jobs pass.
- [x] Package-build job passes.
- [x] Ruff and mypy job passes.
- [x] GitHub release is marked prerelease.
- [x] Alpha sdist and wheel are attached to the release.
