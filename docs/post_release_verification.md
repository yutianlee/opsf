# Post-release verification

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
