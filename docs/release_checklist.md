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
- [ ] Frozen 0.1.0 certified scope reviewed; no new public special-function wrappers added.
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
python scripts/check_release_version.py v0.1.0
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
  `v0.1.0-alpha.3` maps to `0.1.0a3`, and `v0.1.0` maps to `0.1.0`.

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
