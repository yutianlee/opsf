# Post-release verification: v0.1.0-alpha.1 / certsf 0.1.0a1

This records the verification evidence for the first public PyPI artifact.

## Published artifact

- PyPI version: `certsf 0.1.0a1`
- Publish workflow run: `25508798430`
- Wheel SHA256:
  `509a9fe90fb52281ab98725c3fdb465bc50a0913a50adb3deb029b342c168ed2`
- sdist SHA256:
  `0ffd1c29339cb01c3195016dcd660102dc1dc76150ecad37ba63fd5a7282f7e8`

## Fresh install smoke test

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
