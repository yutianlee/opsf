# Release Checklist

Use this checklist before cutting any GitHub prerelease or release. For alpha
releases, keep the wording conservative: the package has certified Arb
enclosures for documented scopes, but the parabolic-cylinder formula layer
remains experimental until the formula audit is complete.

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

## Command Hints

```powershell
python -m pip install -e ".[dev]"
python -m ruff check src tests examples
python -m mypy
python -m pyright src
python -m pytest
python -m pytest tests/test_release_claims.py
python scripts/check_release_version.py v0.2.0-alpha.3
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
- Real PyPI publishing runs from GitHub release/prerelease publication events
  through `publish-pypi`.
- Publishing workflows must pass the tag/version parity check before building:
  `v0.2.0-alpha.3` maps to `0.2.0a3`, `v0.2.0-alpha.2` maps to
  `0.2.0a2`, `v0.2.0-alpha.1` maps to `0.2.0a1`,
  `v0.1.0-alpha.3` maps to `0.1.0a3`, and `v0.1.0` maps to `0.1.0`.

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
