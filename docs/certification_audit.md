# Certification Audit

Last reviewed: 2026-05-08.

This audit is the public map from a certified result to the evidence behind the
claim. It covers every `certificate_scope` that the dispatcher can select in
`mode="certified"`.

Certified successes must include:

- `diagnostics["certificate_scope"]`: the scope listed below.
- `diagnostics["certificate_level"]`: either `direct_arb_primitive` or
  `formula_audited_experimental`.
- `diagnostics["audit_status"]`: either `audited_direct` or
  `experimental_formula`.
- `diagnostics["certification_claim"]`: concise wording for the level of claim.

The two certificate levels mean:

- `direct_arb_primitive`: the wrapper calls an Arb special-function primitive
  for the documented target function, and repo tests cover representative domain,
  branch, singularity, and result-contract behavior. The
  `direct_arb_gamma_ratio` scope is a narrow audited composition of Arb gamma
  primitives rather than a broader formula-layer claim.
- `formula_audited_experimental`: Arb rigorously encloses the implemented
  formula, and repo tests cover the documented first-pass identities, branches,
  and domains, but the formula-backed family has not been promoted to a broad
  non-experimental certification claim.

Family-level checklists:

- [`audit/gamma.md`](audit/gamma.md)
- [`audit/airy.md`](audit/airy.md)
- [`audit/bessel.md`](audit/bessel.md)
- [`audit/parabolic_cylinder.md`](audit/parabolic_cylinder.md)

Static external-reference fixtures in `tests/fixtures/external_reference/`
provide an additional containment check for selected gamma-family, Airy, Bessel, and
parabolic-cylinder values. This fixture coverage supplements the scope evidence
below; it does not broaden any certificate level or promote
`experimental_formula` scopes.

## Scope Matrix

| Certificate scope | Wrappers | Certificate level | Evidence | Exclusions |
| --- | --- | --- | --- | --- |
| `direct_arb_primitive` | `gamma`, `loggamma`, `rgamma` | `direct_arb_primitive` | Direct Arb gamma primitives; pole and reciprocal tests; principal `loggamma` branch-side tests | Non-finite `gamma` and `loggamma` targets at poles |
| `direct_arb_gamma_ratio` | `gamma_ratio` | `direct_arb_primitive` | Arb `gamma(a) * rgamma(b)` product; denominator-pole zero tests; numerator-pole clean-failure tests; recurrence and composition identity checks | Non-finite `Gamma(a)` targets, including numerator poles and simultaneous numerator/denominator poles |
| `phase3_real_airy` | `airy`, `ai`, `bi` on real arguments | `direct_arb_primitive` | Direct Arb Airy primitive; component contract tests; real Wronskian and large-argument checks | Derivatives beyond 1 |
| `arb_complex_airy` | `airy`, `ai`, `bi` on complex arguments | `direct_arb_primitive` | Direct Arb Airy primitive; complex component comparisons and result-contract checks | Derivatives beyond 1 |
| `phase4_integer_real_bessel` | `besselj`, `bessely`, `besseli`, `besselk` with integer order and real argument | `direct_arb_primitive` | Direct Arb Bessel primitives; integer recurrence tests and near-zero checks | Complex order |
| `phase5_real_order_complex_bessel` | `besselj`, `bessely`, `besseli`, `besselk` with real order and real or complex argument | `direct_arb_primitive` | Direct Arb Bessel primitives; real-order comparisons and branch-side checks for `K_v` | Complex order |
| `phase7_hypergeometric_parabolic_cylinder` | `pcfu`, `pcfd`, `pbdv` | `formula_audited_experimental` | Arb `1F1`, reciprocal-gamma, and elementary formula paths; branch-side recurrence checks, direct `D_v` recurrence checks, derivative-identity residual grids, explicit `pbdv` complex-argument policy tests, and deterministic v0.1.x property grids | Complex parameters; broader non-experimental formula graduation |
| `phase8_parabolic_cylinder_connections` | `pcfv`, `pcfw` | `formula_audited_experimental` | Arb connection formulas layered on `pcfu`; branch-side `U`/`V` connection checks, `V` recurrence checks, `W` connection round-trip checks, `phi2` phase-continuity checks, real-domain residual tests, and deterministic v0.1.x property grids | Complex parameters; complex `pcfw` arguments; broader non-experimental formula graduation |

## Claim Wording

For `audited_direct` scopes, runtime diagnostics use:

```text
certified Arb enclosure of the documented direct Arb primitive
```

The `direct_arb_gamma_ratio` scope uses the narrower audited-direct wording:

```text
certified Arb enclosure of Gamma(a) * rgamma(b) using direct Arb gamma primitives
```

For `experimental_formula` scopes, runtime diagnostics use:

```text
certified Arb enclosure of the implemented documented formula; formula audit in progress
```

The second wording is deliberately narrower. It allows callers to rely on Arb's
enclosure of the computed expression while preserving the fact that
formula-backed scopes require an explicit promotion review before any broader
non-experimental claim.

## Audit Gates

Before broadening any certified claim:

- Update the scope matrix and the family notes in [`certification.md`](certification.md).
- Update formula-level source identities, branch notes, and open items in
  [`formula_audit.md`](formula_audit.md) for formula-backed wrappers.
- Keep unsupported certified domains as clean non-certified failures.
- Add or update tests that freeze the runtime `certificate_scope`,
  `certificate_level`, `audit_status`, `certification_claim`, and formula
  diagnostics.
- Run the base and certified test suites.
