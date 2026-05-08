# Post-release verification

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
