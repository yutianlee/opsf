# Post-release verification

## v0.3.0-alpha.1 / certsf 0.3.0a1

This section is intentionally incomplete because the required release evidence
was not available during post-release verification on 2026-05-10. Do not update
the scheduled/manual `pypi-smoke` default from `0.2.0` to `0.3.0a1` until the
real PyPI publication and a `pypi-smoke` run against `0.3.0a1` have both passed.

### Published artifact

- Git tag: TODO: `v0.3.0-alpha.1` was not found in GitHub tag refs.
- GitHub prerelease URL: TODO: no GitHub release was found at
  <https://github.com/yutianlee/certsf/releases/tag/v0.3.0-alpha.1>.
- GitHub release type: TODO: verify the GitHub release is marked prerelease.
- Source commit: `379cb0cd8d6da67b6b34c4f471e6bedc749411d0`
- TestPyPI URL: TODO: verify
  <https://test.pypi.org/project/certsf/0.3.0a1/> after staging; the JSON
  endpoint returned 404 during this verification.
- TestPyPI workflow run: TODO: no `publish-testpypi` run for
  `v0.3.0-alpha.1` was found.
- TestPyPI workflow URL: TODO.
- TestPyPI result: TODO.
- PyPI URL: TODO: verify <https://pypi.org/project/certsf/0.3.0a1/> after
  publication; the JSON endpoint returned 404 during this verification.
- Publish workflow run: TODO: no `publish-pypi` run for `v0.3.0-alpha.1` was
  found.
- Publish workflow URL: TODO.
- PyPI publish result: TODO.
- Wheel SHA256: TODO.
- sdist SHA256: TODO.
- `pypi-smoke` workflow run: TODO: no `pypi-smoke` run against `0.3.0a1` was
  found.
- `pypi-smoke` workflow URL: TODO.
- `pypi-smoke` result: TODO.
- PyPI edge-cache propagation failures: TODO: none were observed because the
  `0.3.0a1` package was not available to smoke.

### Verification status

The latest available release records at verification time were still for
`v0.2.0`: GitHub release `v0.2.0`, TestPyPI workflow run `25612987386`,
publish workflow run `25613028613`, and final `pypi-smoke` run `25613084716`.
No evidence was fabricated for `v0.3.0-alpha.1`.

Required follow-up before this section can be completed:

- Create and publish GitHub prerelease `v0.3.0-alpha.1`.
- Run `publish-testpypi` with `ref=v0.3.0-alpha.1` and
  `confirm=publish-testpypi`.
- Publish `certsf 0.3.0a1` to real PyPI through `publish-pypi`.
- Run `pypi-smoke` against `0.3.0a1`.
- After the smoke run passes, update `.github/workflows/pypi-smoke.yml` from
  `0.2.0` to `0.3.0a1` and add smoke coverage for explicit
  `method="stirling"` and `method="stirling_shifted"` calls.

## v0.2.0 / certsf 0.2.0

This records the verification evidence for the first non-prerelease 0.2 line
PyPI artifact.

### Published artifact

- Git tag: `v0.2.0`
- GitHub release: <https://github.com/yutianlee/certsf/releases/tag/v0.2.0>
- GitHub release type: normal release, not prerelease.
- PyPI URL: <https://pypi.org/project/certsf/0.2.0/>
- PyPI version: `certsf 0.2.0`
- TestPyPI URL: <https://test.pypi.org/project/certsf/0.2.0/>
- TestPyPI workflow run: `25612987386`
- TestPyPI workflow URL:
  <https://github.com/yutianlee/certsf/actions/runs/25612987386>
- TestPyPI result: passed after manual `publish-testpypi` dispatch with
  `ref=v0.2.0` and `confirm=publish-testpypi`.
- Publish workflow run: `25613028613`
- Publish workflow URL:
  <https://github.com/yutianlee/certsf/actions/runs/25613028613>
- Publish trigger: GitHub `release` event for `v0.2.0`
- Source commit: `8ce58cd750bf43e959073a606cb2014bf3c38141`
- Wheel SHA256:
  `17a1bd49fad77dcd693c0d29e512d6711dc8ef13a64e232f9084583a470082cd`
- sdist SHA256:
  `84434f98e43a001e90afe442c312bb3f7f85a6682706d511b66c14a03fb99b0e`

The TestPyPI workflow build job passed checkout, Python 3.12 setup,
tag/version parity check, build-tool installation, sdist/wheel build,
`twine check`, and distribution artifact upload. The TestPyPI publish job
completed through trusted publishing after the explicit confirmation guard.

The real PyPI publish workflow build job passed checkout, Python 3.12 setup,
tag/version parity check, build-tool installation, sdist/wheel build,
`twine check`, and distribution artifact upload. The PyPI publish job
completed through trusted publishing from the normal GitHub release event.

### TestPyPI smoke

A basic local TestPyPI install smoke passed using TestPyPI as the package index
and PyPI as the dependency fallback:

```bash
python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple certsf==0.2.0
```

The smoke imported `certsf` from the temporary virtual environment and exercised
`gamma`, `erf`, `erfc`, `erfinv`, and `erfcinv` in fast mode. TestPyPI remains
staging evidence only; real PyPI plus the `pypi-smoke` workflow are the main
install proof.

### PyPI confirmation

The PyPI JSON endpoint for `certsf 0.2.0` returned the published version and
the two uploaded files listed above. The TestPyPI JSON endpoint returned the
same version and matching wheel/sdist hashes for the staged artifacts.

### Fresh install smoke test

Final manual `pypi-smoke` run: `25613084716`

Workflow URL:
<https://github.com/yutianlee/certsf/actions/runs/25613084716>

Install targets:

```bash
python -m pip install --pre "certsf==0.2.0"
python -m pip install --pre "certsf[certified]==0.2.0"
python -m pip install --pre "certsf[mcp,certified]==0.2.0"
```

Verified from fresh GitHub Actions environments:

- Base installs passed on Python 3.10, 3.11, and 3.12.
- Certified installs passed on Python 3.10, 3.11, and 3.12.
- MCP certified installs passed on Python 3.10, 3.11, and 3.12.
- Imports came from environment `site-packages`, not the checkout.
- Smoke calls passed for `gamma`, `loggamma`, `rgamma`, `gamma_ratio`,
  `loggamma_ratio`, `beta`, `pochhammer`, `erf`, `erfc`, `erfcinv`, `erfcx`,
  `erfi`, `erfinv`, `dawson`, `ai`, `besselj`, and `pcfu`.
- Certified smoke calls passed for `gamma`, `loggamma`, `rgamma`,
  `gamma_ratio`, `loggamma_ratio`, `beta`, `pochhammer`, `erf`, `erfc`,
  `erfcinv`, `erfcx`, `erfi`, `erfinv`, `dawson`, `ai`, `besselj`, and
  `pcfu`.
- MCP server import and `special_gamma` / `special_loggamma` /
  `special_rgamma` / `special_gamma_ratio` / `special_loggamma_ratio` /
  `special_beta` / `special_pochhammer` / `special_erf` / `special_erfc` /
  `special_erfcinv` / `special_erfcx` / `special_erfi` / `special_erfinv` /
  `special_dawson` smoke calls passed.

One earlier manual smoke run captured PyPI edge-cache propagation lag:

- Run `25613047701` started immediately after publish. Several matrix jobs
  installed successfully, but the failed install logs on other runners saw only
  versions through `0.2.0a10` and did not yet list `0.2.0`.

The final run above passed every matrix job after the PyPI edge cache caught up.

After the successful smoke run, this follow-up PR updates the scheduled/manual
`pypi-smoke` workflow default and fallback version from `0.2.0a10` to
`0.2.0` while preserving the existing gamma-family, error-function,
inverse-error, Airy, Bessel, parabolic-cylinder, and MCP-certified smoke
coverage.

### Validation summary

- `v0.2.0` tag points at clean `main` commit
  `8ce58cd750bf43e959073a606cb2014bf3c38141`.
- GitHub release `v0.2.0` is not marked prerelease.
- TestPyPI staging run `25612987386` completed successfully.
- Basic TestPyPI install smoke passed with PyPI dependency fallback.
- `publish-pypi` run `25613028613` completed successfully.
- PyPI confirms `certsf 0.2.0` is available at the release URL above.
- PyPI file hashes match the wheel and sdist hashes recorded above.
- Initial `pypi-smoke` run `25613047701` had PyPI edge-cache propagation
  failures only; failed install logs did not yet list `0.2.0`.
- Final `pypi-smoke` run `25613084716` completed successfully across base,
  certified, and MCP-certified install paths on Python 3.10, 3.11, and 3.12.
- Pre-publication validation passed:
  `python scripts/check_release_version.py v0.2.0`,
  `python -m ruff check .`, `python -m mypy`, `python -m pytest`,
  `python -m build`, and `python -m twine check dist/*`.
- No `src/`, mathematical implementation, backend formula, public-wrapper,
  runtime behavior, certification-scope, gamma-family behavior,
  inverse/error-function behavior, or parabolic-cylinder claim changes were
  made during publication or verification.

## v0.2.0-alpha.10 / certsf 0.2.0a10

This records the verification evidence for the tenth 0.2.0 alpha PyPI
prerelease artifact.

### Published artifact

- Git tag: `v0.2.0-alpha.10`
- GitHub prerelease: <https://github.com/yutianlee/certsf/releases/tag/v0.2.0-alpha.10>
- PyPI URL: <https://pypi.org/project/certsf/0.2.0a10/>
- PyPI version: `certsf 0.2.0a10`
- Publish workflow run: `25612217053`
- Publish workflow URL:
  <https://github.com/yutianlee/certsf/actions/runs/25612217053>
- Publish trigger: GitHub `release` event for `v0.2.0-alpha.10`
- Source commit: `b0e057c93f814ce574e64d1c89b7718a6cbc5045`
- Wheel SHA256:
  `fa807932784f409da69cd67633810f80f7c8887fa4ca97f3556ae38d0975bd4c`
- sdist SHA256:
  `cb4f1c8338b31cf8a2a235b28ad9cd65aad2754cd7e066aa6791e90029cd4170`

The publish workflow build job passed checkout, Python 3.12 setup, tag/version
parity check, build-tool installation, sdist/wheel build, `twine check`, and
distribution artifact upload. The PyPI publish job completed through trusted
publishing from the GitHub release event.

### PyPI confirmation

The PyPI JSON endpoint for `certsf 0.2.0a10` returned the published version and
the two uploaded files listed above. PyPI release metadata is tied to uploaded
file data, so these hashes are the durable evidence for this public prerelease
artifact.

### Fresh install smoke test

Final manual `pypi-smoke` run: `25612366805`

Workflow URL:
<https://github.com/yutianlee/certsf/actions/runs/25612366805>

Install targets:

```bash
python -m pip install --pre "certsf==0.2.0a10"
python -m pip install --pre "certsf[certified]==0.2.0a10"
python -m pip install --pre "certsf[mcp,certified]==0.2.0a10"
```

Verified from fresh GitHub Actions environments:

- Base installs passed on Python 3.10, 3.11, and 3.12.
- Certified installs passed on Python 3.10, 3.11, and 3.12.
- MCP certified installs passed on Python 3.10, 3.11, and 3.12.
- Imports came from environment `site-packages`, not the checkout.
- Smoke calls passed for `gamma`, `loggamma`, `rgamma`, `gamma_ratio`,
  `loggamma_ratio`, `beta`, `pochhammer`, `erf`, `erfc`, `erfcx`, `erfi`,
  `erfinv`, `dawson`, `ai`, `besselj`, and `pcfu`.
- Certified smoke calls passed for `gamma`, `loggamma`, `rgamma`,
  `gamma_ratio`, `loggamma_ratio`, `beta`, `pochhammer`, `erf`, `erfc`,
  `erfcx`, `erfi`, `erfinv`, `dawson`, `ai`, `besselj`, and `pcfu`.
- MCP server import and `special_gamma` / `special_loggamma` /
  `special_rgamma` / `special_gamma_ratio` / `special_loggamma_ratio` /
  `special_beta` / `special_pochhammer` / `special_erf` / `special_erfc` /
  `special_erfcx` / `special_erfi` / `special_erfinv` / `special_dawson`
  smoke calls passed.

One earlier manual smoke run captured PyPI edge-cache propagation lag:

- Run `25612238464` started immediately after publish. Several matrix jobs
  installed successfully, but other install jobs saw only versions through
  `0.2.0a9` and failed before `certsf 0.2.0a10` had propagated to every PyPI
  edge cache.

The final run above passed every matrix job after the PyPI edge cache caught up.

After the successful smoke run, this follow-up PR updates the scheduled/manual
`pypi-smoke` workflow default and fallback version from `0.2.0a9` to
`0.2.0a10`. It also adds `erfcinv` calls to the base and certified smoke paths
and adds `special_erfcinv` to the MCP-certified smoke path while preserving the
existing gamma-family, `erf`, `erfc`, `erfcx`, `erfi`, `erfinv`, `dawson`,
Airy, Bessel, and parabolic-cylinder smoke coverage.

### TestPyPI decision

TestPyPI staging was skipped under `docs/release_policy.md`. This was a routine
feature alpha, and the release introduced no packaging-risk or workflow-risk
changes; the real PyPI release plus `pypi-smoke` verification is sufficient for
this path.

### Validation summary

- `v0.2.0-alpha.10` tag points at clean `main` commit
  `b0e057c93f814ce574e64d1c89b7718a6cbc5045`.
- GitHub prerelease `v0.2.0-alpha.10` is marked prerelease.
- `publish-pypi` run `25612217053` completed successfully.
- PyPI confirms `certsf 0.2.0a10` is available at the release URL above.
- PyPI file hashes match the wheel and sdist hashes recorded above.
- Initial `pypi-smoke` run `25612238464` had PyPI edge-cache propagation
  failures only; failed install logs did not yet list `0.2.0a10`.
- Final `pypi-smoke` run `25612366805` completed successfully across base,
  certified, and MCP-certified install paths on Python 3.10, 3.11, and 3.12.
- Pre-publication validation passed:
  `python scripts/check_release_version.py v0.2.0-alpha.10`,
  `python -m ruff check .`, `python -m mypy`, `python -m pytest`,
  `python -m build`, and `python -m twine check dist/*`.
- No `src/`, mathematical implementation, backend formula, public-wrapper,
  certification-scope, gamma-family behavior, inverse/error-function behavior,
  or parabolic-cylinder claim changes were made during publication or
  verification.

## v0.2.0-alpha.9 / certsf 0.2.0a9

This records the verification evidence for the ninth 0.2.0 alpha PyPI
prerelease artifact.

### Published artifact

- Git tag: `v0.2.0-alpha.9`
- GitHub prerelease: <https://github.com/yutianlee/certsf/releases/tag/v0.2.0-alpha.9>
- PyPI URL: <https://pypi.org/project/certsf/0.2.0a9/>
- PyPI version: `certsf 0.2.0a9`
- Publish workflow run: `25610753603`
- Publish workflow URL:
  <https://github.com/yutianlee/certsf/actions/runs/25610753603>
- Publish trigger: GitHub `release` event for `v0.2.0-alpha.9`
- Source commit: `8a7d44af8aa8f4720d4c2b9b64c51572f9b73c8a`
- Wheel SHA256:
  `de5c6b351c27f5930d14c7f3cd091285bb2a625b22da10d18b6904e5b0ac0b20`
- sdist SHA256:
  `8a5bf2631d18b621738f10ef0aba8550282836a047a71715e1167528474d56d9`

The publish workflow build job passed checkout, Python 3.12 setup, tag/version
parity check, build-tool installation, sdist/wheel build, `twine check`, and
distribution artifact upload. The PyPI publish job completed through trusted
publishing from the GitHub release event.

### PyPI confirmation

The PyPI JSON endpoint for `certsf 0.2.0a9` returned the published version and
the two uploaded files listed above. PyPI release metadata is tied to uploaded
file data, so these hashes are the durable evidence for this public prerelease
artifact.

### Fresh install smoke test

Final manual `pypi-smoke` run: `25610843740`

Workflow URL:
<https://github.com/yutianlee/certsf/actions/runs/25610843740>

Install targets:

```bash
python -m pip install --pre "certsf==0.2.0a9"
python -m pip install --pre "certsf[certified]==0.2.0a9"
python -m pip install --pre "certsf[mcp,certified]==0.2.0a9"
```

Verified from fresh GitHub Actions environments:

- Base installs passed on Python 3.10, 3.11, and 3.12.
- Certified installs passed on Python 3.10, 3.11, and 3.12.
- MCP certified installs passed on Python 3.10, 3.11, and 3.12.
- Imports came from environment `site-packages`, not the checkout.
- Smoke calls passed for `gamma`, `loggamma`, `rgamma`, `gamma_ratio`,
  `loggamma_ratio`, `beta`, `pochhammer`, `erf`, `erfc`, `erfcx`, `erfi`,
  `dawson`, `ai`, `besselj`, and `pcfu`.
- Certified smoke calls passed for `gamma`, `loggamma`, `rgamma`,
  `gamma_ratio`, `loggamma_ratio`, `beta`, `pochhammer`, `erf`, `erfc`,
  `erfcx`, `erfi`, `dawson`, `ai`, `besselj`, and `pcfu`.
- MCP server import and `special_gamma` / `special_loggamma` /
  `special_rgamma` / `special_gamma_ratio` / `special_loggamma_ratio` /
  `special_beta` / `special_pochhammer` / `special_erf` / `special_erfc` /
  `special_erfcx` / `special_erfi` / `special_dawson` smoke calls passed.

Two earlier manual smoke runs captured PyPI edge-cache propagation lag:

- Run `25610774389` started immediately after publish. Several matrix jobs
  installed successfully, but other install jobs saw only versions through
  `0.2.0a8` and failed before `certsf 0.2.0a9` had propagated to every PyPI
  edge cache.
- Run `25610795680` followed shortly after. Most matrix jobs passed, but two
  Python 3.12 install jobs still saw only versions through `0.2.0a8`.

The final run above passed every matrix job after the PyPI edge cache caught up.

After the successful smoke run, this follow-up PR updates the scheduled/manual
`pypi-smoke` workflow default and fallback version from `0.2.0a8` to
`0.2.0a9`. It also adds `erfinv` calls to the base and certified smoke paths
and adds `special_erfinv` to the MCP-certified smoke path while preserving the
existing gamma-family, `erf`, `erfc`, `erfcx`, `erfi`, `dawson`, Airy, Bessel,
and parabolic-cylinder smoke coverage.

### TestPyPI decision

TestPyPI staging was skipped under `docs/release_policy.md`. This was a routine
feature alpha, and the release introduced no packaging-risk or workflow-risk
changes; the real PyPI release plus `pypi-smoke` verification is sufficient for
this path.

### Validation summary

- `v0.2.0-alpha.9` tag points at clean `main` commit
  `8a7d44af8aa8f4720d4c2b9b64c51572f9b73c8a`.
- GitHub prerelease `v0.2.0-alpha.9` is marked prerelease.
- `publish-pypi` run `25610753603` completed successfully.
- PyPI confirms `certsf 0.2.0a9` is available at the release URL above.
- PyPI file hashes match the wheel and sdist hashes recorded above.
- Initial `pypi-smoke` runs `25610774389` and `25610795680` had PyPI
  edge-cache propagation failures only; failed install logs did not yet list
  `0.2.0a9`.
- Final `pypi-smoke` run `25610843740` completed successfully across base,
  certified, and MCP-certified install paths on Python 3.10, 3.11, and 3.12.
- Pre-publication validation passed:
  `python scripts/check_release_version.py v0.2.0-alpha.9`,
  `python -m ruff check .`, `python -m mypy`, `python -m pytest`,
  `python -m build`, and `python -m twine check dist/*`.
- No `src/`, mathematical implementation, backend formula, public-wrapper,
  certification-scope, gamma-family behavior, error-function behavior, or
  parabolic-cylinder claim changes were made during publication or verification.

## v0.2.0-alpha.8 / certsf 0.2.0a8

This records the verification evidence for the eighth 0.2.0 alpha PyPI
prerelease artifact.

### Published artifact

- Git tag: `v0.2.0-alpha.8`
- GitHub prerelease: <https://github.com/yutianlee/certsf/releases/tag/v0.2.0-alpha.8>
- PyPI URL: <https://pypi.org/project/certsf/0.2.0a8/>
- PyPI version: `certsf 0.2.0a8`
- Publish workflow run: `25609883635`
- Publish workflow URL:
  <https://github.com/yutianlee/certsf/actions/runs/25609883635>
- Publish trigger: GitHub `release` event for `v0.2.0-alpha.8`
- Source commit: `20f4d05e881aead86b740f46198a93f86601080c`
- Wheel SHA256:
  `91c960e9b1e418a5f56402f266783b9c3f64b37b546d155bcaea8e1631d9ea6d`
- sdist SHA256:
  `6e092396de14fd5260db49ca50d1fc61b6863b13b19ff58a06def8b9e2856249`

The publish workflow build job passed checkout, Python 3.12 setup, tag/version
parity check, build-tool installation, sdist/wheel build, `twine check`, and
distribution artifact upload. The PyPI publish job completed through trusted
publishing from the GitHub release event.

### PyPI confirmation

The PyPI JSON endpoint for `certsf 0.2.0a8` returned the published version and
the two uploaded files listed above. PyPI release metadata is tied to uploaded
file data, so these hashes are the durable evidence for this public prerelease
artifact.

### Fresh install smoke test

Final manual `pypi-smoke` run: `25609942967`

Workflow URL:
<https://github.com/yutianlee/certsf/actions/runs/25609942967>

Install targets:

```bash
python -m pip install --pre "certsf==0.2.0a8"
python -m pip install --pre "certsf[certified]==0.2.0a8"
python -m pip install --pre "certsf[mcp,certified]==0.2.0a8"
```

Verified from fresh GitHub Actions environments:

- Base installs passed on Python 3.10, 3.11, and 3.12.
- Certified installs passed on Python 3.10, 3.11, and 3.12.
- MCP certified installs passed on Python 3.10, 3.11, and 3.12.
- Imports came from environment `site-packages`, not the checkout.
- Smoke calls passed for `gamma`, `loggamma`, `rgamma`, `gamma_ratio`,
  `loggamma_ratio`, `beta`, `pochhammer`, `erf`, `erfc`, `erfcx`, `erfi`,
  `dawson`, `ai`, `besselj`, and `pcfu`.
- Certified smoke calls passed for `gamma`, `loggamma`, `rgamma`,
  `gamma_ratio`, `loggamma_ratio`, `beta`, `pochhammer`, `erf`, `erfc`,
  `erfcx`, `erfi`, `dawson`, `ai`, `besselj`, and `pcfu`.
- MCP server import and `special_gamma` / `special_loggamma` /
  `special_rgamma` / `special_gamma_ratio` / `special_loggamma_ratio` /
  `special_beta` / `special_pochhammer` / `special_erf` / `special_erfc` /
  `special_erfcx` / `special_erfi` / `special_dawson` smoke calls passed.

One earlier manual smoke run captured PyPI edge-cache propagation lag:

- Run `25609906534` started immediately after publish. Several matrix jobs
  installed successfully, but other install jobs saw only versions through
  `0.2.0a7` and failed before `certsf 0.2.0a8` had propagated to every PyPI
  edge cache.

The final run above passed every matrix job after the PyPI edge cache caught up.

After the successful smoke run, this follow-up PR updates the scheduled/manual
`pypi-smoke` workflow default and fallback version from `0.2.0a7` to
`0.2.0a8`. It also adds `dawson` calls to the base and certified smoke paths
and adds `special_dawson` to the MCP-certified smoke path while preserving the
existing gamma-family, `erf`, `erfc`, `erfcx`, `erfi`, Airy, Bessel, and
parabolic-cylinder smoke coverage.

### TestPyPI decision

TestPyPI staging was skipped under `docs/release_policy.md`. This was a routine
feature alpha, and the release introduced no packaging-risk or workflow-risk
changes; the real PyPI release plus `pypi-smoke` verification is sufficient for
this path.

### Validation summary

- `v0.2.0-alpha.8` tag points at clean `main` commit
  `20f4d05e881aead86b740f46198a93f86601080c`.
- GitHub prerelease `v0.2.0-alpha.8` is marked prerelease.
- `publish-pypi` run `25609883635` completed successfully.
- PyPI confirms `certsf 0.2.0a8` is available at the release URL above.
- PyPI file hashes match the wheel and sdist hashes recorded above.
- Initial `pypi-smoke` run `25609906534` had PyPI edge-cache propagation
  failures only; failed install logs did not yet list `0.2.0a8`.
- Final `pypi-smoke` run `25609942967` completed successfully across base,
  certified, and MCP-certified install paths on Python 3.10, 3.11, and 3.12.
- Pre-publication validation passed:
  `python scripts/check_release_version.py v0.2.0-alpha.8`,
  `python -m ruff check .`, `python -m mypy`, `python -m pytest`,
  `python -m build`, and `python -m twine check dist/*`.
- No `src/`, mathematical implementation, backend formula, public-wrapper,
  gamma-family behavior, parabolic-cylinder claim, or certification-scope
  changes were made during publication or verification.

## v0.2.0-alpha.7 / certsf 0.2.0a7

This records the verification evidence for the seventh 0.2.0 alpha PyPI
prerelease artifact.

### Published artifact

- Git tag: `v0.2.0-alpha.7`
- GitHub prerelease: <https://github.com/yutianlee/certsf/releases/tag/v0.2.0-alpha.7>
- PyPI URL: <https://pypi.org/project/certsf/0.2.0a7/>
- PyPI version: `certsf 0.2.0a7`
- Publish workflow run: `25608607009`
- Publish workflow URL:
  <https://github.com/yutianlee/certsf/actions/runs/25608607009>
- Publish trigger: GitHub `release` event for `v0.2.0-alpha.7`
- Source commit: `7e0bc59dbe9d81f2680de4f4ea8ee042f97987ff`
- Wheel SHA256:
  `818477ceaf1ebabe80aa9be60f8daa3e41c326858cc4035a5681e4bd21b454b3`
- sdist SHA256:
  `63f2796ecae870ac3bdd2f4e735039b6a0eea93a0ba190b32763b137a8f7093e`

The publish workflow build job passed checkout, Python 3.12 setup, tag/version
parity check, build-tool installation, sdist/wheel build, `twine check`, and
distribution artifact upload. The first publish job attempt was rejected by the
`pypi` environment deployment policy because tag deployments were not yet
covered by the environment's custom deployment policy. After adding the missing
`v*` tag deployment policy, rerunning the failed job in the same workflow run
published the distributions through trusted publishing.

### PyPI confirmation

The PyPI JSON endpoint for `certsf 0.2.0a7` returned the published version and
the two uploaded files listed above. PyPI release metadata is tied to uploaded
file data, so these hashes are the durable evidence for this public prerelease
artifact.

### Fresh install smoke test

Final manual `pypi-smoke` run: `25608711789`

Workflow URL:
<https://github.com/yutianlee/certsf/actions/runs/25608711789>

Install targets:

```bash
python -m pip install --pre "certsf==0.2.0a7"
python -m pip install --pre "certsf[certified]==0.2.0a7"
python -m pip install --pre "certsf[mcp,certified]==0.2.0a7"
```

Verified from fresh GitHub Actions environments:

- Base installs passed on Python 3.10, 3.11, and 3.12.
- Certified installs passed on Python 3.10, 3.11, and 3.12.
- MCP certified installs passed on Python 3.10, 3.11, and 3.12.
- Imports came from environment `site-packages`, not the checkout.
- Smoke calls passed for `gamma`, `loggamma`, `rgamma`, `gamma_ratio`,
  `loggamma_ratio`, `beta`, `pochhammer`, `erf`, `erfc`, `erfcx`, `erfi`,
  `ai`, `besselj`, and `pcfu`.
- Certified smoke calls passed for `gamma`, `loggamma`, `rgamma`,
  `gamma_ratio`, `loggamma_ratio`, `beta`, `pochhammer`, `erf`, `erfc`,
  `erfcx`, `erfi`, `ai`, `besselj`, and `pcfu`.
- MCP server import and `special_gamma` / `special_loggamma` /
  `special_rgamma` / `special_gamma_ratio` / `special_loggamma_ratio` /
  `special_beta` / `special_pochhammer` / `special_erf` / `special_erfc` /
  `special_erfcx` / `special_erfi` smoke calls passed.

Two earlier manual smoke runs captured PyPI edge-cache propagation lag:

- Run `25608650711` started immediately after publish. Most matrix jobs
  installed successfully, but the Python 3.11 base install job saw only
  versions through `0.2.0a6`.
- Run `25608670104` followed shortly after. Most matrix jobs passed, but the
  Python 3.12 MCP-certified, Python 3.11 base, and Python 3.10 certified
  install jobs still saw only versions through `0.2.0a6`.

The final run above passed every matrix job after the PyPI edge cache caught up.

After the successful smoke run, this follow-up PR updates the scheduled/manual
`pypi-smoke` workflow default and fallback version from `0.2.0a6` to
`0.2.0a7`. It also adds `erfi` calls to the base and certified smoke paths and
adds `special_erfi` to the MCP-certified smoke path while preserving the
existing gamma-family, `erf`, `erfc`, `erfcx`, Airy, Bessel, and
parabolic-cylinder smoke coverage.

### Validation summary

- `v0.2.0-alpha.7` tag points at clean `main` commit
  `7e0bc59dbe9d81f2680de4f4ea8ee042f97987ff`.
- GitHub prerelease `v0.2.0-alpha.7` is marked prerelease.
- `publish-pypi` run `25608607009` completed successfully after rerunning the
  publish job with the corrected `pypi` environment tag deployment policy.
- PyPI confirms `certsf 0.2.0a7` is available at the release URL above.
- PyPI file hashes match the wheel and sdist hashes recorded above.
- Initial `pypi-smoke` runs `25608650711` and `25608670104` had PyPI
  edge-cache propagation failures only; the failed install logs did not yet
  list `0.2.0a7`.
- Final `pypi-smoke` run `25608711789` completed successfully across base,
  certified, and MCP-certified install paths on Python 3.10, 3.11, and 3.12.
- No `src/`, mathematical implementation, backend formula, public-wrapper,
  gamma-family behavior, parabolic-cylinder claim, or certification-scope
  changes were made during publication or verification.

## v0.2.0-alpha.6 / certsf 0.2.0a6

This records the verification evidence for the sixth 0.2.0 alpha PyPI
prerelease artifact.

### Published artifact

- Git tag: `v0.2.0-alpha.6`
- GitHub prerelease: <https://github.com/yutianlee/certsf/releases/tag/v0.2.0-alpha.6>
- PyPI URL: <https://pypi.org/project/certsf/0.2.0a6/>
- PyPI version: `certsf 0.2.0a6`
- Publish workflow run: `25605169744`
- Publish workflow URL:
  <https://github.com/yutianlee/certsf/actions/runs/25605169744>
- Publish trigger: GitHub `release` event for `v0.2.0-alpha.6`
- Source commit: `7bea7c84039a94518f7533b392cd0b64d14a5487`
- Wheel SHA256:
  `a197c08d4ec897425db7c4b79d809b42663ad31e96fb2f4fe732c313bc15eac4`
- sdist SHA256:
  `84673bb2d8567ee760eabddd7ea55b611164b11395d9d3515c565f8ee6ff98a9`

The publish workflow build job passed checkout, Python 3.12 setup, tag/version
parity check, build-tool installation, sdist/wheel build, `twine check`, and
distribution artifact upload. The PyPI publish job passed after the `pypi`
environment approval and published the distributions through trusted publishing.

### PyPI confirmation

The PyPI JSON endpoint for `certsf 0.2.0a6` returned the published version and
the two uploaded files listed above. PyPI release metadata is tied to uploaded
file data, so these hashes are the durable evidence for this public prerelease
artifact.

### Fresh install smoke test

Final manual `pypi-smoke` run: `25605590191`

Workflow URL:
<https://github.com/yutianlee/certsf/actions/runs/25605590191>

Install targets:

```bash
python -m pip install --pre "certsf==0.2.0a6"
python -m pip install --pre "certsf[certified]==0.2.0a6"
python -m pip install --pre "certsf[mcp,certified]==0.2.0a6"
```

Verified from fresh GitHub Actions environments:

- Base installs passed on Python 3.10, 3.11, and 3.12.
- Certified installs passed on Python 3.10, 3.11, and 3.12.
- MCP certified installs passed on Python 3.10, 3.11, and 3.12.
- Imports came from environment `site-packages`, not the checkout.
- Smoke calls passed for `gamma`, `loggamma`, `rgamma`, `gamma_ratio`,
  `loggamma_ratio`, `beta`, `pochhammer`, `erf`, `erfc`, `ai`, `besselj`, and
  `pcfu`.
- Certified smoke calls passed for `gamma`, `loggamma`, `rgamma`,
  `gamma_ratio`, `loggamma_ratio`, `beta`, `pochhammer`, `erf`, `erfc`, `ai`,
  `besselj`, and `pcfu`.
- MCP server import and `special_gamma` / `special_loggamma` /
  `special_rgamma` / `special_gamma_ratio` / `special_loggamma_ratio` /
  `special_beta` / `special_pochhammer` / `special_erf` / `special_erfc` smoke
  calls passed.

Two earlier manual smoke runs captured PyPI edge-cache propagation lag:

- Run `25605526388` started immediately after publish. Some matrix jobs
  installed successfully, but failed install logs on other runners saw only
  versions through `0.2.0a5`.
- Run `25605543365` followed shortly after. Most matrix jobs passed, but Python
  3.10 certified and MCP-certified install jobs still saw only versions through
  `0.2.0a5`.

The final run above passed every matrix job after the PyPI edge cache caught up.

After the successful smoke run, this follow-up PR updates the scheduled/manual
`pypi-smoke` workflow default and fallback version from `0.2.0a5` to
`0.2.0a6`. It also adds `erfcx` calls to the base and certified smoke paths and
adds `special_erfcx` to the MCP-certified smoke path while preserving the
existing gamma-family, `erf`, `erfc`, Airy, Bessel, and parabolic-cylinder
smoke coverage.

### Validation summary

- `v0.2.0-alpha.6` tag points at clean `main` commit
  `7bea7c84039a94518f7533b392cd0b64d14a5487`.
- GitHub prerelease `v0.2.0-alpha.6` is marked prerelease.
- `publish-pypi` run `25605169744` completed successfully.
- PyPI confirms `certsf 0.2.0a6` is available at the release URL above.
- PyPI file hashes match the wheel and sdist hashes recorded above.
- Initial `pypi-smoke` runs `25605526388` and `25605543365` had PyPI
  edge-cache propagation failures only; the failed install logs did not yet
  list `0.2.0a6`.
- Final `pypi-smoke` run `25605590191` completed successfully across base,
  certified, and MCP-certified install paths on Python 3.10, 3.11, and 3.12.
- No `src/`, mathematical implementation, backend formula, public-wrapper,
  gamma-family behavior, parabolic-cylinder claim, or certification-scope
  changes were made during publication or verification.

## v0.2.0-alpha.5 / certsf 0.2.0a5

This records the verification evidence for the fifth 0.2.0 alpha PyPI
prerelease artifact.

### Published artifact

- Git tag: `v0.2.0-alpha.5`
- GitHub prerelease: <https://github.com/yutianlee/certsf/releases/tag/v0.2.0-alpha.5>
- PyPI URL: <https://pypi.org/project/certsf/0.2.0a5/>
- PyPI version: `certsf 0.2.0a5`
- Publish workflow run: `25603708604`
- Publish workflow URL:
  <https://github.com/yutianlee/certsf/actions/runs/25603708604>
- Publish trigger: GitHub `release` event for `v0.2.0-alpha.5`
- Source commit: `59cf790a6eb21ebfc795bb64283db7123f5fdd5f`
- Wheel SHA256:
  `afbcd41c293fd53230e578324445b9e9d459198e0754c1b9594acf3232b1d63a`
- sdist SHA256:
  `e3ce2524bdc45c5f9cbf4ae800b50f8e797556476d0fa785c432b6a3ba686cad`

The publish workflow build job passed checkout, Python 3.12 setup, tag/version
parity check, build-tool installation, sdist/wheel build, `twine check`, and
distribution artifact upload. The PyPI publish job passed after the `pypi`
environment approval and published the distributions through trusted publishing.

### PyPI confirmation

The PyPI JSON endpoint for `certsf 0.2.0a5` returned the published version and
the two uploaded files listed above. PyPI release metadata is tied to uploaded
file data, so these hashes are the durable evidence for this public prerelease
artifact.

### Fresh install smoke test

Final manual `pypi-smoke` run: `25604211944`

Workflow URL:
<https://github.com/yutianlee/certsf/actions/runs/25604211944>

Install targets:

```bash
python -m pip install --pre "certsf==0.2.0a5"
python -m pip install --pre "certsf[certified]==0.2.0a5"
python -m pip install --pre "certsf[mcp,certified]==0.2.0a5"
```

Verified from fresh GitHub Actions environments:

- Base installs passed on Python 3.10, 3.11, and 3.12.
- Certified installs passed on Python 3.10, 3.11, and 3.12.
- MCP certified installs passed on Python 3.10, 3.11, and 3.12.
- Imports came from environment `site-packages`, not the checkout.
- Smoke calls passed for `gamma`, `loggamma`, `rgamma`, `gamma_ratio`,
  `loggamma_ratio`, `beta`, `pochhammer`, `ai`, `besselj`, and `pcfu`.
- Certified smoke calls passed for `gamma`, `loggamma`, `rgamma`,
  `gamma_ratio`, `loggamma_ratio`, `beta`, `pochhammer`, `ai`, `besselj`, and
  `pcfu`.
- MCP server import and `special_gamma` / `special_loggamma` /
  `special_rgamma` / `special_gamma_ratio` / `special_loggamma_ratio` /
  `special_beta` / `special_pochhammer` smoke calls passed.

Two earlier manual smoke runs captured PyPI edge-cache propagation lag:

- Run `25604145930` started immediately after publish. Some matrix jobs
  installed successfully, but failed install logs on other runners saw only
  versions through `0.2.0a4`.
- Run `25604185744` followed shortly after. Most matrix jobs passed, but one
  Python 3.12 MCP-certified install still saw only versions through
  `0.2.0a4`.

The final run above passed every matrix job after the PyPI edge cache caught up.

After the successful smoke run, this follow-up PR updates the scheduled/manual
`pypi-smoke` workflow default and fallback version from `0.2.0a4` to
`0.2.0a5`. It also adds `erf` and `erfc` calls to the base and certified smoke
paths and adds `special_erf` and `special_erfc` to the MCP-certified smoke path
while preserving the existing gamma-family, Airy, Bessel, and
parabolic-cylinder smoke coverage.

### Validation summary

- `v0.2.0-alpha.5` tag points at clean `main` commit
  `59cf790a6eb21ebfc795bb64283db7123f5fdd5f`.
- GitHub prerelease `v0.2.0-alpha.5` is marked prerelease.
- `publish-pypi` run `25603708604` completed successfully.
- PyPI confirms `certsf 0.2.0a5` is available at the release URL above.
- PyPI file hashes match the wheel and sdist hashes recorded above.
- Initial `pypi-smoke` runs `25604145930` and `25604185744` had PyPI
  edge-cache propagation failures only; the failed install logs did not yet
  list `0.2.0a5`.
- Final `pypi-smoke` run `25604211944` completed successfully across base,
  certified, and MCP-certified install paths on Python 3.10, 3.11, and 3.12.
- No `src/`, mathematical implementation, backend formula, public-wrapper,
  gamma-family behavior, or parabolic-cylinder claim changes were made during
  publication or verification.

## v0.2.0-alpha.4 / certsf 0.2.0a4

This records the verification evidence for the fourth 0.2.0 alpha PyPI
prerelease artifact.

### Published artifact

- Git tag: `v0.2.0-alpha.4`
- GitHub prerelease: <https://github.com/yutianlee/certsf/releases/tag/v0.2.0-alpha.4>
- PyPI URL: <https://pypi.org/project/certsf/0.2.0a4/>
- PyPI version: `certsf 0.2.0a4`
- Publish workflow run: `25599731814`
- Publish workflow URL:
  <https://github.com/yutianlee/certsf/actions/runs/25599731814>
- Publish trigger: GitHub `release` event for `v0.2.0-alpha.4`
- Source commit: `a6514c20e2615005890265018c6edb957fc7954a`
- Wheel SHA256:
  `9d441d6e65d33ed5913cd8594a62d808286c2f31e35274342a7720dcdc16e4ef`
- sdist SHA256:
  `7d9a922d2cfb72ac7fbb67d3fee752e54599e032437f45da5ec35023103711f8`

The publish workflow build job passed checkout, Python 3.12 setup, tag/version
parity check, build-tool installation, sdist/wheel build, `twine check`, and
distribution artifact upload. The PyPI publish job passed after the `pypi`
environment approval and published the distributions through trusted publishing.

### PyPI confirmation

The PyPI JSON endpoint for `certsf 0.2.0a4` returned the published version and
the two uploaded files listed above. PyPI release metadata is tied to uploaded
file data, so these hashes are the durable evidence for this public prerelease
artifact.

### Fresh install smoke test

Final manual `pypi-smoke` run: `25601711537`

Workflow URL:
<https://github.com/yutianlee/certsf/actions/runs/25601711537>

Install targets:

```bash
python -m pip install --pre "certsf==0.2.0a4"
python -m pip install --pre "certsf[certified]==0.2.0a4"
python -m pip install --pre "certsf[mcp,certified]==0.2.0a4"
```

Verified from fresh GitHub Actions environments:

- Base installs passed on Python 3.10, 3.11, and 3.12.
- Certified installs passed on Python 3.10, 3.11, and 3.12.
- MCP certified installs passed on Python 3.10, 3.11, and 3.12.
- Imports came from environment `site-packages`, not the checkout.
- Smoke calls passed for `gamma`, `gamma_ratio`, `loggamma_ratio`, `beta`,
  `ai`, `besselj`, and `pcfu`.
- Certified smoke calls passed for `gamma`, `gamma_ratio`, `loggamma_ratio`,
  `beta`, `ai`, `besselj`, and `pcfu`.
- MCP server import and `special_gamma` / `special_gamma_ratio` /
  `special_loggamma_ratio` / `special_beta` smoke calls passed.

One earlier manual smoke run captured PyPI edge-cache propagation lag:

- Run `25601669244` started immediately after publish. Some matrix jobs
  installed successfully, but failed install logs on other runners saw only
  versions through `0.2.0a3`.

The final run above passed every matrix job after the PyPI edge cache caught up.

After the successful smoke run, this follow-up PR updates the scheduled/manual
`pypi-smoke` workflow default and fallback version from `0.2.0a3` to
`0.2.0a4`. It also adds `pochhammer` calls to the base and certified smoke
paths and adds `special_pochhammer` to the MCP-certified smoke path while
preserving the existing `gamma_ratio`, `loggamma_ratio`, and `beta` coverage.

### Validation summary

- `v0.2.0-alpha.4` tag points at clean `main` commit
  `a6514c20e2615005890265018c6edb957fc7954a`.
- GitHub prerelease `v0.2.0-alpha.4` is marked prerelease.
- `publish-pypi` run `25599731814` completed successfully.
- PyPI confirms `certsf 0.2.0a4` is available at the release URL above.
- PyPI file hashes match the wheel and sdist hashes recorded above.
- Initial `pypi-smoke` run `25601669244` had PyPI edge-cache propagation
  failures only; the failed install logs did not yet list `0.2.0a4`.
- Final `pypi-smoke` run `25601711537` completed successfully across base,
  certified, and MCP-certified install paths on Python 3.10, 3.11, and 3.12.
- No `src/`, mathematical implementation, backend formula, public-wrapper, or
  certification-scope changes were made during publication or verification.

## v0.2.0-alpha.3 / certsf 0.2.0a3

This records the verification evidence for the third 0.2.0 alpha PyPI
prerelease artifact.

### Published artifact

- Git tag: `v0.2.0-alpha.3`
- GitHub prerelease: <https://github.com/yutianlee/certsf/releases/tag/v0.2.0-alpha.3>
- PyPI URL: <https://pypi.org/project/certsf/0.2.0a3/>
- PyPI version: `certsf 0.2.0a3`
- Publish workflow run: `25597680136`
- Publish workflow URL:
  <https://github.com/yutianlee/certsf/actions/runs/25597680136>
- Publish trigger: GitHub `release` event for `v0.2.0-alpha.3`
- Source commit: `9329b99eb735a63b52a5d12e22e6ab0a40b22fba`
- Wheel SHA256:
  `7845e683be012b0f6df22e6232a5ada374cc13c1e0f52eb9289b54987bb6639c`
- sdist SHA256:
  `b216ab7f68fb0edb1f8dbeb9bd8692d4568fbec0ef1f1397b6ac529f3e512b08`

The publish workflow build job passed checkout, Python 3.12 setup, tag/version
parity check, build-tool installation, sdist/wheel build, `twine check`, and
distribution artifact upload. The PyPI publish job passed after the `pypi`
environment approval and published the distributions through trusted publishing.

### PyPI confirmation

The PyPI JSON endpoint for `certsf 0.2.0a3` returned the published version and
the two uploaded files listed above. PyPI release metadata is tied to uploaded
file data, so these hashes are the durable evidence for this public prerelease
artifact.

### Fresh install smoke test

Final manual `pypi-smoke` run: `25598157583`

Workflow URL:
<https://github.com/yutianlee/certsf/actions/runs/25598157583>

Install targets:

```bash
python -m pip install --pre "certsf==0.2.0a3"
python -m pip install --pre "certsf[certified]==0.2.0a3"
python -m pip install --pre "certsf[mcp,certified]==0.2.0a3"
```

Verified from fresh GitHub Actions environments:

- Base installs passed on Python 3.10, 3.11, and 3.12.
- Certified installs passed on Python 3.10, 3.11, and 3.12.
- MCP certified installs passed on Python 3.10, 3.11, and 3.12.
- Imports came from environment `site-packages`, not the checkout.
- Smoke calls passed for `gamma`, `gamma_ratio`, `loggamma_ratio`, `ai`,
  `besselj`, and `pcfu`.
- Certified smoke calls passed for `gamma`, `gamma_ratio`, `loggamma_ratio`,
  `ai`, `besselj`, and `pcfu`.
- MCP server import and `special_gamma` / `special_gamma_ratio` /
  `special_loggamma_ratio` smoke calls passed.

Three earlier manual smoke runs captured PyPI edge-cache propagation lag:

- Run `25598008536` started immediately after publish. Some matrix jobs
  installed successfully, but failed install logs on other runners saw only
  versions through `0.2.0a2`.
- Run `25598049815` followed after the PyPI JSON endpoint reported
  `0.2.0a3`; most jobs passed, but one Python 3.12 certified install still saw
  only versions through `0.2.0a2`.
- Run `25598085325` followed after an additional delay; most jobs passed, but
  one Python 3.12 base install still saw only versions through `0.2.0a2`.

The final run above passed every matrix job after the PyPI edge cache caught up.

After the successful smoke run, this follow-up PR updates the scheduled/manual
`pypi-smoke` workflow default and fallback version from `0.2.0a2` to
`0.2.0a3`. It also adds `beta` calls to the base, certified, and MCP-certified
smoke paths while preserving the existing `gamma_ratio` and `loggamma_ratio`
coverage.

### Validation summary

- `v0.2.0-alpha.3` tag points at clean `main` commit
  `9329b99eb735a63b52a5d12e22e6ab0a40b22fba`.
- GitHub prerelease `v0.2.0-alpha.3` is marked prerelease.
- `publish-pypi` run `25597680136` completed successfully.
- PyPI confirms `certsf 0.2.0a3` is available at the release URL above.
- PyPI file hashes match the wheel and sdist hashes recorded above.
- Final `pypi-smoke` run `25598157583` completed successfully across base,
  certified, and MCP-certified install paths on Python 3.10, 3.11, and 3.12.
- No mathematical implementation, backend formula, public wrapper, or
  certification-scope changes were made during publication or verification.

## v0.2.0-alpha.2 / certsf 0.2.0a2

This records the verification evidence for the second 0.2.0 alpha PyPI
prerelease artifact.

### Published artifact

- Git tag: `v0.2.0-alpha.2`
- GitHub prerelease: <https://github.com/yutianlee/certsf/releases/tag/v0.2.0-alpha.2>
- PyPI URL: <https://pypi.org/project/certsf/0.2.0a2/>
- PyPI version: `certsf 0.2.0a2`
- Publish workflow run: `25596527307`
- Publish workflow URL:
  <https://github.com/yutianlee/certsf/actions/runs/25596527307>
- Publish trigger: GitHub `release` event for `v0.2.0-alpha.2`
- Source commit: `741c3875761800260565c1cf5321c71f68143eee`
- Wheel SHA256:
  `2899abb436f743d3d17e4dee47a3a4fcdef46aa280098aba2e9718edf6bc06f3`
- sdist SHA256:
  `d22aaeff4a265d425287ab8d31039c9dce8214886e6dc6dc2b1fceb6498f835f`

The publish workflow build job passed checkout, Python 3.12 setup, tag/version
parity check, build-tool installation, sdist/wheel build, `twine check`, and
distribution artifact upload. The PyPI publish job passed after the `pypi`
environment approval and published the distributions through trusted publishing.

### PyPI confirmation

The PyPI JSON endpoint for `certsf 0.2.0a2` returned the published version and
the two uploaded files listed above. PyPI release metadata is tied to uploaded
file data, so these hashes are the durable evidence for this public prerelease
artifact.

### Fresh install smoke test

Final manual `pypi-smoke` run: `25596982098`

Workflow URL:
<https://github.com/yutianlee/certsf/actions/runs/25596982098>

Install targets:

```bash
python -m pip install --pre "certsf==0.2.0a2"
python -m pip install --pre "certsf[certified]==0.2.0a2"
python -m pip install --pre "certsf[mcp,certified]==0.2.0a2"
```

Verified from fresh GitHub Actions environments:

- Base installs passed on Python 3.10, 3.11, and 3.12.
- Certified installs passed on Python 3.10, 3.11, and 3.12.
- MCP certified installs passed on Python 3.10, 3.11, and 3.12.
- Imports came from environment `site-packages`, not the checkout.
- Smoke calls passed for `gamma`, `gamma_ratio`, `ai`, `besselj`, and `pcfu`.
- Certified smoke calls passed for `gamma`, `gamma_ratio`, `ai`, `besselj`,
  and `pcfu`.
- MCP server import and `special_gamma` / `special_gamma_ratio` smoke calls
  passed.

Two earlier manual smoke runs captured PyPI edge-cache propagation lag:

- Run `25596849623` started immediately after publish. Some matrix jobs
  installed successfully, but failed install logs on other runners saw only
  versions through `0.2.0a1`.
- Run `25596905510` followed after the PyPI JSON endpoint reported
  `0.2.0a2`; all base and certified jobs passed, but one Python 3.10
  MCP-certified install still saw only versions through `0.2.0a1`.

The final run above passed every matrix job after the PyPI edge cache caught up.

After the successful smoke run, this follow-up PR updates the scheduled/manual
`pypi-smoke` workflow default and fallback version from `0.2.0a1` to
`0.2.0a2`. It also adds `loggamma_ratio` calls to the base, certified, and
MCP-certified smoke paths while preserving the existing `gamma_ratio` coverage.

### Validation summary

- `v0.2.0-alpha.2` tag points at clean `main` commit
  `741c3875761800260565c1cf5321c71f68143eee`.
- GitHub release `v0.2.0-alpha.2` is marked prerelease.
- `publish-pypi` run `25596527307` completed successfully.
- PyPI confirms `certsf 0.2.0a2` is available at the release URL above.
- PyPI file hashes match the wheel and sdist hashes recorded above.
- Final `pypi-smoke` run `25596982098` completed successfully across base,
  certified, and MCP-certified install paths on Python 3.10, 3.11, and 3.12.
- No mathematical implementation, backend formula, public wrapper, or
  certification-scope changes were made during publication or verification.

## v0.2.0-alpha.1 / certsf 0.2.0a1

This records the verification evidence for the first 0.2.0 alpha PyPI
prerelease artifact.

### Published artifact

- Git tag: `v0.2.0-alpha.1`
- GitHub prerelease: <https://github.com/yutianlee/certsf/releases/tag/v0.2.0-alpha.1>
- PyPI URL: <https://pypi.org/project/certsf/0.2.0a1/>
- PyPI version: `certsf 0.2.0a1`
- Publish workflow run: `25551068192`
- Publish workflow URL:
  <https://github.com/yutianlee/certsf/actions/runs/25551068192>
- Publish trigger: GitHub `release` event for `v0.2.0-alpha.1`
- Source commit: `20795af2e9200a6eacb97ddbf8dbf3f3c708da1f`
- Wheel SHA256:
  `e92ad9e28aed0839c2209ae3596d4c902232925610a1c1b4f56af0ca21329529`
- sdist SHA256:
  `24a6a30634c7069a9130b1d37b0da0b4ddd513ca9fa2df840ec8dd589b36cc4c`

The publish workflow build job passed checkout, Python 3.12 setup, tag/version
parity check, build-tool installation, sdist/wheel build, `twine check`, and
distribution artifact upload. The PyPI publish job passed after the `pypi`
environment approval and published the distributions through trusted publishing.

### PyPI confirmation

The PyPI JSON endpoint for `certsf 0.2.0a1` returned the published version and
the two uploaded files listed above. PyPI release metadata is tied to uploaded
file data, so these hashes are the durable evidence for this public prerelease
artifact.

### Fresh install smoke test

Manual `pypi-smoke` run: `25551842586`

Workflow URL:
<https://github.com/yutianlee/certsf/actions/runs/25551842586>

Install targets:

```bash
python -m pip install --pre "certsf==0.2.0a1"
python -m pip install --pre "certsf[certified]==0.2.0a1"
python -m pip install --pre "certsf[mcp,certified]==0.2.0a1"
```

Verified from fresh GitHub Actions environments:

- Base installs passed on Python 3.10, 3.11, and 3.12.
- Certified installs passed on Python 3.10, 3.11, and 3.12.
- MCP certified installs passed on Python 3.10, 3.11, and 3.12.
- Imports came from environment `site-packages`, not the checkout.
- Smoke calls passed for `gamma`, `ai`, `besselj`, and `pcfu`.
- Certified smoke calls passed for `gamma`, `ai`, `besselj`, and `pcfu`.
- MCP server import and `special_gamma` smoke call passed.

An earlier manual smoke run, `25551781178`, started immediately after publish
and failed a subset of install jobs while other matrix jobs succeeded. The
failed pip logs saw only `0.1.0a1`, `0.1.0a2`, `0.1.0a3`, and `0.1.0`
available from PyPI, so that run is treated as PyPI edge-cache propagation
evidence rather than artifact failure. The follow-up run above passed every
matrix job.

After the successful smoke run, the scheduled/manual `pypi-smoke` workflow
default was updated from `0.1.0` to `0.2.0a1`.

A follow-up smoke-workflow update added `gamma_ratio` calls to the base,
certified, and MCP-certified smoke paths so scheduled/manual PyPI verification
covers the new public wrapper directly.

### Validation summary

- `v0.2.0-alpha.1` tag points at clean `main` commit
  `20795af2e9200a6eacb97ddbf8dbf3f3c708da1f`.
- GitHub release `v0.2.0-alpha.1` is marked prerelease.
- `publish-pypi` run `25551068192` completed successfully.
- PyPI confirms `certsf 0.2.0a1` is available at the release URL above.
- PyPI file hashes match the wheel and sdist hashes recorded above.
- Final `pypi-smoke` run `25551842586` completed successfully across base,
  certified, and MCP-certified install paths on Python 3.10, 3.11, and 3.12.
- No mathematical implementation, formula, public wrapper, or certification
  scope changes were made during publication or verification.

## v0.1.0 / certsf 0.1.0

This records the verification evidence for the first non-prerelease PyPI
artifact.

### Published artifact

- Git tag: `v0.1.0`
- GitHub release: <https://github.com/yutianlee/certsf/releases/tag/v0.1.0>
- GitHub release type: normal release, not prerelease
- PyPI URL: <https://pypi.org/project/certsf/0.1.0/>
- PyPI version: `certsf 0.1.0`
- Publish workflow run: `25547072957`
- Publish workflow URL:
  <https://github.com/yutianlee/certsf/actions/runs/25547072957>
- Publish trigger: GitHub `release` event for `v0.1.0`
- Source commit: `f444c3d97e36317236e11720a148468f8ff4e667`
- Wheel SHA256:
  `153990947a1aeac44060ac612718dc43ad436821a89a1812846965465287231d`
- sdist SHA256:
  `8ffafe64ce3dff6651eb5c417db617fc929f1902b5f4eebbe9c96cfa429b52f0`

The publish workflow build job passed checkout, Python 3.12 setup, tag/version
parity check, build-tool installation, sdist/wheel build, `twine check`, and
distribution artifact upload. The PyPI publish job passed after the `pypi`
environment approval and published the distributions through trusted publishing.

### PyPI confirmation

The PyPI JSON endpoint for `certsf 0.1.0` returned the published version and the
two uploaded files listed above. PyPI release metadata is tied to uploaded file
data, so these hashes are the durable evidence for this public release artifact.

### Fresh install smoke test

Manual `pypi-smoke` run: `25547662691`

Workflow URL:
<https://github.com/yutianlee/certsf/actions/runs/25547662691>

Install targets:

```bash
python -m pip install --pre "certsf==0.1.0"
python -m pip install --pre "certsf[certified]==0.1.0"
python -m pip install --pre "certsf[mcp,certified]==0.1.0"
```

Verified from fresh GitHub Actions environments:

- Base installs passed on Python 3.10, 3.11, and 3.12.
- Certified installs passed on Python 3.10, 3.11, and 3.12.
- MCP certified installs passed on Python 3.10, 3.11, and 3.12.
- Imports came from environment `site-packages`, not the checkout.
- Smoke calls passed for `gamma`, `ai`, `besselj`, and `pcfu`.
- Certified smoke calls passed for `gamma`, `ai`, `besselj`, and `pcfu`.
- MCP server import and `special_gamma` smoke call passed.

An earlier manual smoke run, `25547551682`, started shortly after publish and
failed a small number of install jobs while other matrix jobs succeeded. The
failed pip logs saw only `0.1.0a1`, `0.1.0a2`, and `0.1.0a3` available from
PyPI, so that run is treated as PyPI edge-cache propagation evidence rather
than artifact failure. The follow-up run above passed every matrix job.

After the successful smoke run, the scheduled/manual `pypi-smoke` workflow
default was updated from `0.1.0a3` to `0.1.0`.

### Validation summary

- `v0.1.0` tag points at clean `main` commit
  `f444c3d97e36317236e11720a148468f8ff4e667`.
- GitHub release `v0.1.0` is not marked prerelease.
- `publish-pypi` run `25547072957` completed successfully.
- PyPI confirms `certsf 0.1.0` is available at the release URL above.
- PyPI file hashes match the wheel and sdist hashes recorded above.
- Final `pypi-smoke` run `25547662691` completed successfully across base,
  certified, and MCP-certified install paths on Python 3.10, 3.11, and 3.12.
- No mathematical implementation, formula, public wrapper, or certification
  scope changes were made during publication or verification.

## v0.1.0-alpha.3 / certsf 0.1.0a3

This records the verification evidence for the third public PyPI prerelease
artifact.

### Published artifact

- Git tag: `v0.1.0-alpha.3`
- GitHub prerelease: <https://github.com/yutianlee/certsf/releases/tag/v0.1.0-alpha.3>
- PyPI URL: <https://pypi.org/project/certsf/0.1.0a3/>
- PyPI version: `certsf 0.1.0a3`
- Publish workflow run: `25544396246`
- Publish workflow URL:
  <https://github.com/yutianlee/certsf/actions/runs/25544396246>
- Publish trigger: GitHub `release` event for `v0.1.0-alpha.3`
- Source commit: `fdd8ab3e85455a2b0bbf3bd7ec182757f1354f30`
- Wheel SHA256:
  `e29ee0d2eb9c4935de411e2b80d20045ad9112ef8381ec289db8772f45cb52c5`
- sdist SHA256:
  `d73b0aa31549fabe1214dd96c77d89e47bd6520debe6f5ff510523da84c224ed`

The publish workflow build job passed checkout, Python 3.12 setup, tag/version
parity check, build-tool installation, sdist/wheel build, `twine check`, and
distribution artifact upload. The PyPI publish job passed after the `pypi`
environment approval and published the distributions through trusted publishing.

### PyPI confirmation

The PyPI JSON endpoint for `certsf 0.1.0a3` returned the published version and
the two uploaded files listed above. PyPI release metadata is tied to uploaded
file data, so these hashes are the durable evidence for this public prerelease
artifact.

### Fresh install smoke test

Manual `pypi-smoke` run: `25545367590`

Workflow URL:
<https://github.com/yutianlee/certsf/actions/runs/25545367590>

Install targets:

```bash
python -m pip install --pre "certsf==0.1.0a3"
python -m pip install --pre "certsf[certified]==0.1.0a3"
python -m pip install --pre "certsf[mcp,certified]==0.1.0a3"
```

Verified from fresh GitHub Actions environments:

- Base installs passed on Python 3.10, 3.11, and 3.12.
- Certified installs passed on Python 3.10, 3.11, and 3.12.
- MCP certified installs passed on Python 3.10, 3.11, and 3.12.
- Imports came from environment `site-packages`, not the checkout.
- Smoke calls passed for `gamma`, `ai`, `besselj`, and `pcfu`.
- Certified smoke calls passed for `gamma`, `ai`, `besselj`, and `pcfu`.
- MCP server import and `special_gamma` smoke call passed.

Earlier manual smoke runs, `25545094581` and `25545190346`, started shortly
after publish and failed a small number of install jobs while other matrix jobs
succeeded. The failed pip logs saw only `0.1.0a1` and `0.1.0a2` available from
PyPI, so those runs are treated as PyPI edge-cache propagation evidence rather
than artifact failure. The follow-up run above passed every matrix job.

After the successful smoke run, the scheduled/manual `pypi-smoke` workflow
default was updated from `0.1.0a2` to `0.1.0a3`.

### Validation summary

- `v0.1.0-alpha.3` tag points at clean `main` commit
  `fdd8ab3e85455a2b0bbf3bd7ec182757f1354f30`.
- GitHub prerelease `v0.1.0-alpha.3` is marked prerelease.
- `publish-pypi` run `25544396246` completed successfully.
- PyPI confirms `certsf 0.1.0a3` is available at the release URL above.
- PyPI file hashes match the wheel and sdist hashes recorded above.
- Final `pypi-smoke` run `25545367590` completed successfully across base,
  certified, and MCP-certified install paths on Python 3.10, 3.11, and 3.12.
- No mathematical implementation, formula, public wrapper, or certification
  scope changes were made during publication or verification.

## v0.1.0-alpha.2 / certsf 0.1.0a2

This records the verification evidence for the second public PyPI prerelease
artifact.

### Published artifact

- Git tag: `v0.1.0-alpha.2`
- GitHub prerelease: <https://github.com/yutianlee/certsf/releases/tag/v0.1.0-alpha.2>
- PyPI URL: <https://pypi.org/project/certsf/0.1.0a2/>
- PyPI version: `certsf 0.1.0a2`
- Publish workflow run: `25540759737`
- Publish trigger: GitHub `release` event for `v0.1.0-alpha.2`
- Source commit: `b736bf7c75ecbc0d53daf0ecd42c4f9601fa10da`
- Wheel SHA256:
  `df4052d56074a66b932b193122d9fcf6340176f7db593f45fcac3b33a3bdaa88`
- sdist SHA256:
  `5830d0061eba984290be35626c8ca6afac8a9e41098e134d2e4c888b0d05fbba`

The publish workflow build job passed checkout, Python 3.12 setup, build-tool
installation, sdist/wheel build, `twine check`, and distribution artifact
upload. The PyPI publish job passed after the `pypi` environment approval and
published the distributions through trusted publishing.

### PyPI confirmation

The PyPI JSON endpoint for `certsf 0.1.0a2` returned the published version and
the two uploaded files listed above. PyPI release metadata is tied to uploaded
file data, so these hashes are the durable evidence for this public prerelease
artifact.

### Fresh install smoke test

Manual `pypi-smoke` run: `25541278586`

Install targets:

```bash
python -m pip install --pre "certsf==0.1.0a2"
python -m pip install --pre "certsf[certified]==0.1.0a2"
python -m pip install --pre "certsf[mcp,certified]==0.1.0a2"
```

Verified from fresh GitHub Actions environments:

- Base installs passed on Python 3.10, 3.11, and 3.12.
- Certified installs passed on Python 3.10, 3.11, and 3.12.
- MCP certified installs passed on Python 3.10, 3.11, and 3.12.
- Imports came from environment `site-packages`, not the checkout.
- Smoke calls passed for `gamma`, `ai`, `besselj`, and `pcfu`.
- Certified smoke calls passed for `gamma`, `ai`, `besselj`, and `pcfu`.
- MCP server import and `special_gamma` smoke call passed.

An earlier manual smoke run, `25541202216`, started immediately after publish
and failed three install jobs while some other matrix jobs succeeded. The failed
pip logs saw only `0.1.0a1` available from PyPI, so that run is treated as PyPI
edge-cache propagation evidence rather than artifact failure. The follow-up run
above passed every matrix job.

### Validation summary

- `v0.1.0-alpha.2` tag points at clean `main` commit
  `b736bf7c75ecbc0d53daf0ecd42c4f9601fa10da`.
- GitHub prerelease `v0.1.0-alpha.2` is marked prerelease.
- `publish-pypi` run `25540759737` completed successfully.
- PyPI confirms `certsf 0.1.0a2` is available at the release URL above.
- PyPI file hashes match the wheel and sdist hashes recorded above.
- Final `pypi-smoke` run `25541278586` completed successfully across base,
  certified, and MCP-certified install paths on Python 3.10, 3.11, and 3.12.
- No mathematical implementation, formula, public wrapper, or certification
  scope changes were made during publication or verification.

## v0.1.0-alpha.1 / certsf 0.1.0a1

This records the verification evidence for the first public PyPI artifact.

### Published artifact

- PyPI version: `certsf 0.1.0a1`
- Publish workflow run: `25508798430`
- Wheel SHA256:
  `509a9fe90fb52281ab98725c3fdb465bc50a0913a50adb3deb029b342c168ed2`
- sdist SHA256:
  `0ffd1c29339cb01c3195016dcd660102dc1dc76150ecad37ba63fd5a7282f7e8`

### Fresh install smoke test

Install command:

```bash
python -m pip install --pre "certsf[certified]==0.1.0a1"
```

Verified from a fresh virtual environment:

- Import came from the virtual environment `site-packages`, not the local checkout.
- `python-flint 0.8.0` was installed.
- Certified `gamma` smoke call passed.
- Certified `ai` smoke call passed.
- Certified `besselj` smoke call passed.
- Certified `pcfu` smoke call passed.

PyPI release metadata is tied to the uploaded files. Subsequent uploads do not
rewrite the existing release metadata, so these hashes are the durable evidence
for this public prerelease artifact.
