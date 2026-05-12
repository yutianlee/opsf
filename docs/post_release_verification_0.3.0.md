# v0.3.0 Post-release Verification

This file records real release evidence for `v0.3.0` / `certsf 0.3.0`.
It does not change runtime code, public wrappers, default dispatch, or
certification claims.

## Published Artifact

- Git tag: `v0.3.0`
- Tag commit: `a84fab858d4d40051311d2b8810d8cedb06e1b87`
- GitHub release:
  <https://github.com/yutianlee/certsf/releases/tag/v0.3.0>
- GitHub release type: normal release, not prerelease.
- GitHub release title: `certsf v0.3.0`
- GitHub release published: `2026-05-12T05:30:51Z`
- Package version: `certsf 0.3.0`

The GitHub release notes keep conservative certification wording. They state
that v0.3.0 keeps the 0.2 public wrapper surface, adds only explicit custom
certified methods for existing wrappers, leaves default certified
`loggamma`/`gamma`/`rgamma` on direct Arb, leaves `method=None` and
`method="auto"` unchanged, and keeps parabolic-cylinder wrappers at
`experimental_formula`.

## TestPyPI Staging

- Workflow: `publish-testpypi`
- Workflow run: `25715127842`
- Workflow URL:
  <https://github.com/yutianlee/certsf/actions/runs/25715127842>
- Trigger: `workflow_dispatch`
- Dispatch ref: `v0.3.0`
- Required confirmation input: `publish-testpypi`
- Head commit: `a84fab858d4d40051311d2b8810d8cedb06e1b87`
- Conclusion: success.
- TestPyPI package URL:
  <https://test.pypi.org/project/certsf/0.3.0/>

Clean TestPyPI install verification passed in separate environments:

- Base install:
  `certsf==0.3.0`
- Certified install:
  `certsf[certified]==0.3.0`
- MCP/certified install:
  `certsf[mcp,certified]==0.3.0`

Representative certified API checks passed from the TestPyPI package:

- `loggamma("20", mode="certified", method="stirling", dps=50)`
- `loggamma("20", mode="certified", method="stirling_shifted", dps=100)`
- `loggamma("20", mode="certified", method="certified_auto", dps=100)`
- `gamma("20", mode="certified", method="stirling_exp", dps=50)`
- `rgamma("20", mode="certified", method="stirling_recip", dps=50)`

The MCP check also passed:

- `special_rgamma("20", mode="certified", method="stirling_recip", dps=50)`
- Returned `certified=True`
- Returned `method="stirling_recip_rgamma"`
- Returned
  `diagnostics["certificate_scope"] == "rgamma_positive_real_stirling_recip"`

## PyPI Publication

- Workflow: `publish-pypi`
- Workflow run: `25715439858`
- Workflow URL:
  <https://github.com/yutianlee/certsf/actions/runs/25715439858>
- Trigger: GitHub `release` event for `v0.3.0`
- Head commit: `a84fab858d4d40051311d2b8810d8cedb06e1b87`
- Conclusion: success.
- PyPI URL:
  <https://pypi.org/project/certsf/0.3.0/>

## PyPI Artifacts

- Wheel: `certsf-0.3.0-py3-none-any.whl`
  - SHA256:
    `cd69acae18782828e4ee02da841a7c6753f33cb7894d30886e46743d69798b51`
- sdist: `certsf-0.3.0.tar.gz`
  - SHA256:
    `e1c81147870c1e86a59ee4159cfd4d0f21eeeb48e63b6d2f63d71fd98d7c9441`

No PyPI edge-cache propagation delay was observed. Real PyPI base, certified,
and MCP/certified clean installs all succeeded on the first attempt.

## PyPI Install Verification

Clean real PyPI install verification passed in separate environments:

- Base install:
  `python -m pip install --no-cache-dir "certsf==0.3.0"`
- Certified install:
  `python -m pip install --no-cache-dir "certsf[certified]==0.3.0"`
- MCP/certified install:
  `python -m pip install --no-cache-dir "certsf[mcp,certified]==0.3.0"`

Representative API checks passed from the real PyPI package:

- `gamma("3.2", mode="fast")`
- `loggamma("3.2", mode="fast")`
- `rgamma("3.2", mode="fast")`
- `loggamma("20", mode="certified", method="stirling", dps=50)`
- `loggamma("20", mode="certified", method="stirling_shifted", dps=100)`
- `loggamma("20", mode="certified", method="certified_auto", dps=100)`
- `gamma("20", mode="certified", method="stirling_exp", dps=50)`
- `rgamma("20", mode="certified", method="stirling_recip", dps=50)`

The real PyPI MCP check also passed:

- `special_rgamma("20", mode="certified", method="stirling_recip", dps=50)`
- Returned `certified=True`
- Returned `function="rgamma"`
- Returned `method="stirling_recip_rgamma"`
- Returned
  `diagnostics["certificate_scope"] == "rgamma_positive_real_stirling_recip"`

## PyPI Smoke

- Manual `pypi-smoke` workflow run: `25715711137`
- Workflow URL:
  <https://github.com/yutianlee/certsf/actions/runs/25715711137>
- Trigger: `workflow_dispatch`
- Branch/ref: `main`
- Version input: `0.3.0`
- Head commit: `a84fab858d4d40051311d2b8810d8cedb06e1b87`
- Conclusion: success.

All nine smoke jobs passed:

- `pypi-smoke / 3.10 base`
- `pypi-smoke / 3.11 base`
- `pypi-smoke / 3.12 base`
- `pypi-smoke / 3.10 [certified]`
- `pypi-smoke / 3.11 [certified]`
- `pypi-smoke / 3.12 [certified]`
- `pypi-smoke / 3.10 mcp-certified`
- `pypi-smoke / 3.11 mcp-certified`
- `pypi-smoke / 3.12 mcp-certified`

At the time this verification was recorded, the `pypi-smoke.yml` workflow
remained pinned to `0.3.0a5`. Advancing that default to `0.3.0` was reserved
for a separate post-release smoke-pin PR.

## Post-release Smoke-pin Follow-up

After successful real PyPI publication and the passing manual `pypi-smoke` run
`25715711137` with `version=0.3.0`, the smoke-pin follow-up advances
`pypi-smoke.yml` from `0.3.0a5` to `0.3.0`.

The follow-up changes only the workflow dispatch default and fallback install
literals. It preserves the base, certified, and MCP-certified matrices and the
explicit Python API and MCP smoke coverage for
`rgamma(method="stirling_recip")`.

## Scope Confirmation

No files under `src/` changed for this verification. No runtime implementation,
public wrapper, or default dispatch behavior changed.

The v0.3.0 final release keeps the documented 0.3 scope:

- Default certified `loggamma`, `gamma`, and `rgamma` remain direct Arb.
- Custom certified methods remain explicit-only.
- `method=None` and `method="auto"` remain unchanged.
- The explicit reciprocal-gamma custom method remains
  `rgamma(x, mode="certified", method="stirling_recip", dps=...)` for finite
  real `x >= 20`.
- Parabolic-cylinder wrappers remain `experimental_formula`.
- Release claims were not broadened.

This release does not add certification of complex-valued Stirling formulas,
certification for complex reciprocal gamma, certification via reflection
formulas, near-pole behavior, gamma-ratio asymptotics, beta asymptotics,
parabolic-cylinder promotion, or new public wrappers.
