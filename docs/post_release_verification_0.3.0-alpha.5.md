# v0.3.0-alpha.5 Post-release Verification

This file records real release evidence for `v0.3.0-alpha.5` / `certsf
0.3.0a5` and the follow-up smoke-pin update. It does not change runtime code,
public wrappers, or default dispatch.

## Published Artifact

- Git tag: `v0.3.0-alpha.5`
- Tag commit: `49ce2443374bd7e03f85ba63e9204b7ee86b01cc`
- GitHub prerelease:
  <https://github.com/yutianlee/certsf/releases/tag/v0.3.0-alpha.5>
- GitHub release type: prerelease, not draft.
- PyPI URL: <https://pypi.org/project/certsf/0.3.0a5/>
- PyPI version: `certsf 0.3.0a5`
- TestPyPI decision: skipped; TestPyPI was not used for this routine feature
  alpha.
- Publish workflow run: `25709658634`
- Publish workflow URL:
  <https://github.com/yutianlee/certsf/actions/runs/25709658634>
- Publish trigger: GitHub `release` event for `v0.3.0-alpha.5`
- Publish workflow conclusion: success.

## PyPI Artifacts

- Wheel: `certsf-0.3.0a5-py3-none-any.whl`
  - Uploaded: `2026-05-12T02:31:37.838074Z`
  - SHA256:
    `82579600688abba23525d5079d4bdec6f60dbfec85c01b09d4f189befe722b04`
- sdist: `certsf-0.3.0a5.tar.gz`
  - Uploaded: `2026-05-12T02:31:39.410211Z`
  - SHA256:
    `b2c064aa0a232180b139d3765aad1ed6254a149e84a2545e466157a03726fd68`

No PyPI edge-cache propagation delay was observed after the publish workflow
completed. The package was visible to clean `pip install --no-cache-dir --pre`
verification commands.

## PyPI Install Verification

Clean base install of `certsf==0.3.0a5` succeeded from real PyPI. A certified
`rgamma(method="stirling_recip")` call from that base-only environment returned
a clean non-certified result because `python-flint` is not installed by the base
package.

Clean certified install of `certsf[certified]==0.3.0a5` succeeded from real
PyPI. The explicit positive-real reciprocal-gamma method passed:

- call:
  `rgamma("20", mode="certified", method="stirling_recip", dps=50)`
- `certified=True`
- `function="rgamma"`
- `method="stirling_recip_rgamma"`
- `backend="certsf+python-flint"`
- `diagnostics["selected_method"] == "stirling_recip"`
- `diagnostics["certificate_scope"] == "rgamma_positive_real_stirling_recip"`
- `diagnostics["certificate_level"] == "custom_asymptotic_bound"`
- `diagnostics["audit_status"] == "theorem_documented"`
- `abs_error_bound` is present.

Clean MCP/certified install of `certsf[mcp,certified]==0.3.0a5` succeeded from
real PyPI. The MCP wrapper passed:

- call:
  `special_rgamma("20", mode="certified", method="stirling_recip", dps=50)`
- `certified=True`
- `function="rgamma"`
- `method="stirling_recip_rgamma"`
- `diagnostics["certificate_scope"] == "rgamma_positive_real_stirling_recip"`

## PyPI Smoke

- Manual `pypi-smoke` workflow run: `25710093100`
- Workflow URL:
  <https://github.com/yutianlee/certsf/actions/runs/25710093100>
- Trigger: `workflow_dispatch` on `main` with `version=0.3.0a5`
- Conclusion: success.
- Passing jobs:
  - `pypi-smoke / 3.10 base`
  - `pypi-smoke / 3.11 base`
  - `pypi-smoke / 3.12 base`
  - `pypi-smoke / 3.10 [certified]`
  - `pypi-smoke / 3.11 [certified]`
  - `pypi-smoke / 3.12 [certified]`
  - `pypi-smoke / 3.10 mcp-certified`
  - `pypi-smoke / 3.11 mcp-certified`
  - `pypi-smoke / 3.12 mcp-certified`

The post-release verification PR left the workflow default pinned to `0.3.0a4`.
After that PR merged, the smoke-pin follow-up updated the scheduled/manual
default to `0.3.0a5` and added alpha.5 `rgamma(method="stirling_recip")`
Python API and MCP smoke coverage.

## Post-smoke-pin Verification

After the smoke-pin follow-up merged, the updated `pypi-smoke` workflow was
manually run again from `main`.

- Manual `pypi-smoke` workflow run: `25711747679`
- Workflow URL:
  <https://github.com/yutianlee/certsf/actions/runs/25711747679>
- Branch/ref: `main`
- Head commit: `2587b07c6341a4116c2ddc96e6c6afb20aeabcc6`
- Version input: `0.3.0a5`
- Conclusion: success.
- Passing jobs:
  - `pypi-smoke / 3.10 base`
  - `pypi-smoke / 3.11 base`
  - `pypi-smoke / 3.12 base`
  - `pypi-smoke / 3.10 [certified]`
  - `pypi-smoke / 3.11 [certified]`
  - `pypi-smoke / 3.12 [certified]`
  - `pypi-smoke / 3.10 mcp-certified`
  - `pypi-smoke / 3.11 mcp-certified`
  - `pypi-smoke / 3.12 mcp-certified`

Log inspection confirmed that the certified Python API smoke block ran both
`rgamma("20", mode="certified", method="stirling_recip", dps=50)` and
`rgamma("20", mode="certified", method="stirling_recip", dps=100)`, producing
certified `stirling_recip_rgamma` payloads with
`certificate_scope="rgamma_positive_real_stirling_recip"`.

Log inspection also confirmed that the MCP smoke block ran both
`special_rgamma("20", mode="certified", method="stirling_recip", dps=50)` and
`special_rgamma("20", mode="certified", method="stirling_recip", dps=100)`,
producing certified `stirling_recip_rgamma` payloads with
`certificate_scope="rgamma_positive_real_stirling_recip"`.

## Scope Confirmation

This release packages the explicit certified positive-real reciprocal-gamma
method
`rgamma(x, mode="certified", method="stirling_recip", dps=...)` for finite real
`x >= 20`.

Default certified `rgamma` remains the direct Arb path. `method=None` and
`method="auto"` remain unchanged. This release does not add complex `rgamma`,
reflection formula certification, near-pole behavior, gamma-ratio asymptotics,
beta asymptotics, parabolic-cylinder promotion, public wrappers, or default
dispatch changes.
