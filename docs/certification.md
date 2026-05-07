# Certification Notes

This document records what `certsf` means by a certified result. A result is
certified only when:

1. the numerical backend returns an Arb ball enclosure for the expression that
   was evaluated, and
2. the expression evaluated by `certsf` is the documented target function on
   the stated domain.

The first layer is provided by `python-flint` / Arb. The second layer is a
project-level responsibility: formulas, branch conventions, and exclusions
must be documented and tested before a wrapper claims `certified=True`.
The scope-by-scope audit is maintained in
[`certification_audit.md`](certification_audit.md).

## Result Contract

Certified results set:

- `certified=True`
- `backend="python-flint"`
- `method="arb_ball"` or a documented Arb formula method
- `abs_error_bound` to a rigorous absolute radius
- `diagnostics["certificate_scope"]` to one of the scopes below
- `diagnostics["certificate_level"]` to `direct_arb_primitive` for direct Arb
  primitive paths or `formula_audited_experimental` for formula-backed
  certificates with open formula audit work
- `diagnostics["audit_status"]` to `audited_direct` for direct Arb primitive
  paths or `experimental_formula` for formula-backed paths with open audit work
- `diagnostics["certification_claim"]` to the precise claim wording for that
  audit status

Unsupported certified domains return `certified=False`, `value=""`, and a
diagnostic error. They must not fall back to a non-certified backend while
claiming certification.

## Gamma Family

Function:
`gamma(z)`, `loggamma(z)`, `rgamma(z)`

Certified domain:
real or complex inputs accepted by Arb for the corresponding primitive, with
non-finite target values reported as clean failures.

Backend primitive:
`arb/acb.gamma`, `arb/acb.lgamma`, and `arb/acb.rgamma`.

Returned enclosure:
Arb midpoint string plus absolute radius. `rgamma` returns an exact certified
zero at non-positive integer gamma poles when Arb reports that enclosure.

Branch convention:
`loggamma` follows the principal branch used by Arb.

Formula transformations:
none.

Known exclusions:
`gamma` and `loggamma` at poles return non-certified failures because the
requested value is not finite.

Validation tests:
pole behavior, principal-branch checks on the negative real axis, and
comparison against mpmath away from singularities.

Certificate scope:
`direct_arb_primitive`, recorded through `method="arb_ball"`.

## Airy Family

Function:
`airy(z)`, `ai(z)`, `bi(z)` and first derivatives.

Certified domain:
real and complex arguments supported by Arb Airy primitives. Real arguments are
tagged as `phase3_real_airy`; complex arguments are tagged as
`arb_complex_airy`.

Backend primitive:
`arb/acb.airy`.

Returned enclosure:
component midpoint strings plus component absolute radii. Multi-component
results store JSON strings in the Python API and nested objects in MCP payloads.

Branch convention:
Arb Airy convention.

Formula transformations:
none.

Known exclusions:
higher derivatives beyond `derivative=1`.

Validation tests:
component comparisons against mpmath, real-domain Wronskian identity with
propagated radii, and large positive/negative real arguments.

Certificate scope:
`phase3_real_airy` or `arb_complex_airy`.

## Bessel Family

Function:
`besselj(v, z)`, `bessely(v, z)`, `besseli(v, z)`, `besselk(v, z)`

Certified domain:
real-valued order and real or complex argument. Integer real-order cases are
tagged separately from general real-order complex-argument cases.

Backend primitive:
Arb/acb Bessel primitives through `python-flint`.

Returned enclosure:
Arb midpoint string plus absolute radius.

Branch convention:
Arb branch conventions for `Y_v` and `K_v`.

Formula transformations:
none in the certified backend; domain routing selects the appropriate Arb
primitive path.

Known exclusions:
complex order is outside the certified scope and returns a clean failure.

Validation tests:
comparison against mpmath grids, integer-order recurrence identities with
propagated radii, near-zero tests, and branch-cut side checks for `K_v`.

Certificate scopes:
`phase4_integer_real_bessel`, `phase5_real_order_complex_bessel`.

## Parabolic-Cylinder Family

Function:
`pcfd(v, z)`, `pcfu(a, z)`, `pcfv(a, z)`, `pcfw(a, x)`, `pbdv(v, x)`

Certified domain:
real parameters. `pcfd`, `pcfu`, `pcfv`, and `pbdv` support real or complex
arguments through the current formula paths. `pcfw` currently supports real
arguments only.

Backend primitive:
Arb hypergeometric primitives and Arb elementary operations.

Returned enclosure:
Arb enclosure of the documented formula expression. `pbdv` returns component
enclosures for value and derivative.

Branch convention:
The implemented formulas follow the branch conventions of the underlying Arb
hypergeometric and elementary operations. These conventions should be reviewed
against the target DLMF definitions before expanding the public certified
domain.

Formula transformations:
`pcfu` uses a hypergeometric representation. `pcfd` and `pbdv` are reduced
through `pcfu` relations. `pcfv` and `pcfw` use connection formulas.
The detailed audit trail is maintained in [`formula_audit.md`](formula_audit.md).

Known exclusions:
complex parameters and complex `pcfw` arguments are clean failures.

Validation tests:
comparison against mpmath over real and complex grids, derivative identity for
`pbdv`, and domain-rejection tests for unsupported inputs.

Certificate scopes:
`phase7_hypergeometric_parabolic_cylinder`,
`phase8_parabolic_cylinder_connections`.

Status:
experimental certified formula layer. The Arb enclosure is rigorous for the
computed expression; the formula/domain audit should remain visible and
versioned before broadening claims.
