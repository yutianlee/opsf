# Release Policy

This document clarifies how public prereleases are published and when TestPyPI
staging is useful. It is release-process policy only; it does not change package
behavior, certified scope, or public APIs.

## Real PyPI

Public alpha prereleases are published to real PyPI.

Non-prerelease final releases are also published to real PyPI. A final release
uses the protected `publish-pypi` workflow from a normal GitHub release rather
than a GitHub prerelease.

GitHub prerelease publication triggers the protected `publish-pypi` workflow.
That workflow builds from the tag, checks tag/package-version parity, runs
`twine check`, and publishes through the configured PyPI trusted-publishing
environment.

Real PyPI is the source of truth for install smoke tests. Each real PyPI
prerelease must be followed by:

- a manual `pypi-smoke` run against the newly published version;
- a rerun if the first smoke attempt only fails because PyPI edge caches have
  not yet propagated the new version; and
- a post-release verification PR that records the tag, release URL, PyPI URL,
  workflow run, source commit, artifact hashes, smoke result, and any
  propagation failures.

## TestPyPI

TestPyPI is manual-only staging. Do not publish every alpha prerelease to
TestPyPI.

Use TestPyPI only when packaging or workflow risk justifies staging before the
real PyPI release, including:

- first release of a new minor line;
- first non-prerelease release of a minor line;
- final release candidates;
- `pyproject.toml` or build-backend changes;
- extras or dependency changes;
- Trusted Publishing or environment changes;
- release workflow changes; or
- prior PyPI packaging failure.

Routine feature alpha releases may skip TestPyPI if build, `twine check`,
tag/version parity, protected PyPI publish, and real PyPI smoke all pass.

For a first non-prerelease release in a minor line, stage to TestPyPI unless
the release-planning PR explicitly documents why staging is skipped. This
guards the transition from prerelease-only installs to the stable install path.

The `publish-testpypi` workflow must remain `workflow_dispatch` only. It must
not gain a release trigger, and operators must intentionally confirm the manual
staging run before it can publish to TestPyPI.
