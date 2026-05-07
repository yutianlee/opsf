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
- [ ] MCP server imports and registers tools.
- [ ] Certification docs reviewed.
- [ ] Formula audit reviewed for any changed formula path.
- [ ] Unsupported certified domains fail cleanly.
- [ ] `CHANGELOG.md` updated.
- [ ] `CITATION.cff` version matches the release name.
- [ ] `pyproject.toml` version uses the matching PEP 440 form.
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
python -m build
python -m twine check dist/*
python examples/basic_usage.py
python examples/certified_vs_high_precision.py
python -c "from certsf.mcp_server import build_server; build_server()"
```

For an alpha tag, use a Git tag such as `v0.1.0-alpha.1` and a Python package
version such as `0.1.0a1`.

## v0.1.0-alpha.1 Snapshot

- [x] CI green on Python 3.10, 3.11, and 3.12.
- [x] Base and certified test jobs pass.
- [x] Package-build job passes.
- [x] Ruff and mypy job passes.
- [x] GitHub release is marked prerelease.
- [x] Alpha sdist and wheel are attached to the release.
