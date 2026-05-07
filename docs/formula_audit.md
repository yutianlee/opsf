# Formula Audit

Last reviewed: 2026-05-07.

This document records formula-level certification claims for wrappers that do
not call a single Arb special-function primitive. It is intentionally stricter
than a usage guide: each entry names the target function, the implemented
formula, source identities, domain assumptions, branch conventions, exclusions,
test coverage, and audit status.

The current nontrivial formula layer is the parabolic-cylinder family in
`src/certsf/backends/arb_backend.py`. Certified results for these wrappers mean:

- Arb encloses the implemented expression using ball arithmetic.
- The expression is the documented formula below on the documented domain.
- The result includes a `diagnostics["formula"]` string and a
  `diagnostics["certificate_scope"]` string.
- The result includes
  `diagnostics["certificate_level"] = "formula_audited_experimental"`.

Until a separate promotion review graduates the formula-backed family to a
broader non-experimental claim, runtime diagnostics describe these results as:

> certified Arb enclosure of the implemented documented formula; formula audit
> in progress

Do not describe the parabolic-cylinder family as broadly certified beyond the
domains and formulas listed here. The scope-level audit matrix lives in
[`certification_audit.md`](certification_audit.md).

## Status Vocabulary

- `audited_direct`: the wrapper delegates to a documented Arb special-function
  primitive and has representative domain, branch, singularity, and contract
  tests.
- `experimental_formula`: the implementation has Arb enclosures and regression
  tests for documented formulas, including first-pass source, domain, branch,
  and independent identity checks, but the formula-backed family has not been
  promoted to a broad non-experimental certification claim.

All parabolic-cylinder formulas are currently `experimental_formula`.

## Reference Map

Primary references:

- DLMF section 12.1 records the `D_nu(z)` notation and the convention that fractional
  powers use principal values: <https://dlmf.nist.gov/12.1>
- DLMF section 12.2 defines the standard `U(a,z)`, `V(a,z)`, and `D_nu(z)` solutions
  and gives connection formulas: <https://dlmf.nist.gov/12.2>
- DLMF section 12.7 gives the confluent-hypergeometric local solutions used for the
  `pcfu` formula: <https://dlmf.nist.gov/12.7>
- DLMF section 12.8 gives recurrence and derivative identities:
  <https://dlmf.nist.gov/12.8>
- DLMF section 12.14 gives the `W(a,x)` connection formula:
  <https://dlmf.nist.gov/12.14>

Implementation anchors:

- `_arb_pcfu_value`
- `_arb_pcfd_value`
- `arb_pbdv`
- `_arb_pcfv_value`
- `_arb_pcfw_value`
- `_parabolic_cylinder_diagnostics`

Contract tests:

- `tests/test_certification_contract.py` freezes formula and scope diagnostics.
- `tests/test_identity_residuals.py` checks selected identities and residuals
  without relying only on reference-value comparison.
- `tests/test_certified_identities.py` checks certified ball residuals for
  recurrences, connection formulas, and derivative identities with propagated
  radii.
- `tests/test_pbdv.py` compares current formula outputs against mpmath and
  checks domain rejections.

## Summary Table

| Wrapper | Target | Formula diagnostic | Certificate scope | Status |
| --- | --- | --- | --- | --- |
| `pcfu(a,z)` | `U(a,z)` | `pcfu_1f1_global` | `phase7_hypergeometric_parabolic_cylinder` | experimental_formula |
| `pcfd(v,z)` | `D_v(z)` | `pcfd_via_pcfu` | `phase7_hypergeometric_parabolic_cylinder` | experimental_formula |
| `pbdv(v,x)` | `D_v(x)`, `D_v'(x)` | `pcfd_via_pcfu` | `phase7_hypergeometric_parabolic_cylinder` | experimental_formula |
| `pcfv(a,z)` | `V(a,z)` | `pcfv_dlmf_connection` | `phase8_parabolic_cylinder_connections` | experimental_formula |
| `pcfw(a,x)` | `W(a,x)` | `pcfw_dlmf_12_14_real_connection` | `phase8_parabolic_cylinder_connections` | experimental_formula |

## `pcfu(a, z)`

Target function:
`U(a,z)`, the DLMF parabolic-cylinder function.

Implemented formula:

```text
U(a,z) =
  exp(z^2/4) *
  (
    U0(a) * M(-a/2 + 1/4, 1/2, -z^2/2)
    + U0p(a) * z * M(-a/2 + 3/4, 3/2, -z^2/2)
  )

U0(a)  = sqrt(pi) * 2^(-a/2 - 1/4) / Gamma(a/2 + 3/4)
U0p(a) = -sqrt(pi) * 2^(-a/2 + 1/4) / Gamma(a/2 + 1/4)
```

Here `M(alpha, beta, z)` is Kummer's confluent hypergeometric function
`1F1(alpha; beta; z)`. The implementation uses Arb `hypgeom_1f1` and reciprocal
gamma operations.

Source identity:
DLMF 12.7.12 and 12.7.13 give the even and odd local solutions in terms of
`M`. DLMF 12.2.6 and 12.2.7 give `U(a,0)` and `U'(a,0)`. The implemented
formula forms the linear combination with those initial values.

Domain assumptions:

- Certified mode accepts real `a`.
- Certified mode accepts real or complex `z`.
- Complex `a` is rejected before formula evaluation.

Branch convention:
For real `a`, the powers of `2` and gamma factors are real-valued. The `z`
dependence enters through `z`, `z^2`, exponentials, and `1F1`; branch behavior is
therefore inherited from Arb elementary and hypergeometric operations. Complex
parameter branches are intentionally outside scope.

Known exclusions:
complex parameter; unreviewed branch behavior outside the current real-parameter
domain; any domain where Arb returns a non-finite enclosure.

Tests covering the identity:

- `test_certified_parabolic_cylinder_core_covers_mpmath` compares real and
  complex-argument samples against mpmath.
- `test_certified_parabolic_cylinder_rejects_complex_parameter` checks clean
  failure for complex parameters.
- `test_parabolic_cylinder_certified_results_keep_formula_audit_visible` checks
  that the formula and certificate scope remain visible.
- `test_high_precision_pcfu_satisfies_differential_equation_residual` checks
  the defining differential-equation residual with a high-precision five-point
  stencil.
- `test_certified_pcfu_balls_imply_complex_branch_side_recurrence` checks the
  `z U(a,z) - U(a-1,z) + (a+1/2) U(a+1,z) = 0` recurrence on complex
  branch-side samples using certified balls rather than reference values.

Audit note:
complex branch-side recurrence coverage is now part of the first-pass audit.
The wrapper remains `experimental_formula` until the formula-backed family is
explicitly promoted in a later release.

Status:
experimental_formula.

## `pcfd(v, z)`

Target function:
`D_v(z)`, Whittaker's parabolic-cylinder `D` function.

Implemented formula:

```text
D_v(z) = U(-v - 1/2, z)
```

Source identity:
DLMF 12.2.5 gives the relation between `D_nu(z)` and `U(a,z)`.

Domain assumptions:

- Certified mode accepts real `v`.
- Certified mode accepts real or complex `z`.
- Complex `v` is rejected before formula evaluation.

Branch convention:
All branch behavior is inherited from the `pcfu` formula after the real
parameter substitution `a = -v - 1/2`.

Known exclusions:
complex order; any excluded `pcfu` domain.

Tests covering the identity:

- `test_pcfd_matches_pbdv_value_high_precision` checks the high-precision
  `pcfd`/`pbdv` value relation.
- `test_certified_parabolic_cylinder_core_covers_mpmath` compares certified
  samples against mpmath.
- `test_parabolic_cylinder_certified_results_keep_formula_audit_visible` checks
  formula and scope diagnostics.
- `test_certified_pcfd_balls_imply_direct_recurrence` checks the direct
  `D_(v+1)(z) - z D_v(z) + v D_(v-1)(z) = 0` recurrence on real and complex
  samples.
- `test_certified_parabolic_cylinder_balls_imply_differential_equation_residual`
  checks a shifted recurrence form of the `D_v` differential-equation residual
  on real and complex samples.

Audit note:
direct `D_v` recurrence and shifted differential-equation residual coverage are
now part of the first-pass audit.

Status:
experimental_formula.

## `pbdv(v, x)`

Target function:
the pair `D_v(x)` and `D_v'(x)`.

Implemented formula:

```text
value      = D_v(x)
derivative = x/2 * D_v(x) - D_(v+1)(x)
```

The value component is the `pcfd` formula. The derivative component follows
from the `U` derivative identity after substituting `D_v(z) = U(-v - 1/2,z)`.

Source identity:
DLMF 12.2.5 gives `D_v(z) = U(-v - 1/2,z)`. DLMF 12.8.10 gives the derivative
identity that yields `D_v'(z) = z/2 * D_v(z) - D_(v+1)(z)`.

Domain assumptions:

- Certified mode accepts real `v`.
- Certified mode accepts real or complex arguments through the shared `pcfd`
  formula path. The parameter name `x` is kept for SciPy compatibility; in the
  certified formula layer it is a documented argument and may be complex.
- Complex `v` is rejected before formula evaluation.

Branch convention:
same as `pcfd` for the value and shifted-order `pcfd` calls.

Known exclusions:
complex order; any excluded `pcfd` domain.

Tests covering the identity:

- `test_certified_pbdv_returns_value_and_derivative_bounds` checks value and
  derivative component bounds against mpmath and the derivative identity.
- `test_certified_pbdv_derivative_identity_encloses_zero` checks that the
  derivative identity residual is enclosed by propagated certified radii.
- `test_certified_pbdv_derivative_relation_covers_wider_grid` checks the same
  derivative identity over positive real, negative real, larger real, and
  complex samples.
- `test_mcp_pbdv_returns_nested_component_payloads` checks the component payload
  shape exposed to MCP.
- `test_parabolic_cylinder_certified_results_keep_formula_audit_visible` checks
  formula and scope diagnostics.

Audit note:
the public certified domain advertises real parameters and real or complex
arguments for `pbdv`; the wider derivative residual grid is now part of the
first-pass audit.

Status:
experimental_formula.

## `pcfv(a, z)`

Target function:
`V(a,z)`, the DLMF parabolic-cylinder `V` function.

Implemented formula:
the upper-sign case of the DLMF connection formula

```text
V(a,z) =
  -i / Gamma(1/2 - a) * U(a,z)
  + sqrt(2/pi) * exp(-i*pi*(a/2 - 1/4)) * U(-a, i*z)
```

Source identity:
DLMF 12.2.20 gives `V(a,z)` in terms of two `U` functions.

Domain assumptions:

- Certified mode accepts real `a`.
- Certified mode accepts real or complex `z`.
- Complex `a` is rejected before formula evaluation.

Branch convention:
The implementation uses the upper-sign connection formula, Arb principal
exponential and gamma conventions, and the `pcfu` branch behavior for both `U`
terms.

Known exclusions:
complex parameter; unreviewed sign/branch behavior outside the current
real-parameter domain.

Tests covering the identity:

- `test_certified_parabolic_cylinder_core_covers_mpmath` compares real and
  complex-argument samples against mpmath.
- `test_certified_parabolic_cylinder_rejects_complex_parameter` covers shared
  complex-parameter rejection.
- `test_parabolic_cylinder_certified_results_keep_formula_audit_visible` checks
  formula and scope diagnostics.
- `test_certified_parabolic_cylinder_connection_formula_encloses_zero` checks a
  `U(a,-z)`/`U(a,z)`/`V(a,z)` connection-formula residual with propagated
  certified radii.
- `test_certified_pcfv_balls_imply_branch_side_connection_formula` extends that
  connection-formula residual to complex branch-side samples.
- `test_certified_pcfv_balls_imply_independent_recurrence` checks the
  `z V(a,z) - V(a+1,z) + (a-1/2) V(a-1,z) = 0` recurrence independently of
  reference-value comparison.

Audit note:
branch-side connection-formula and independent recurrence coverage are now part
of the first-pass audit.

Status:
experimental_formula.

## `pcfw(a, x)`

Target function:
`W(a,x)`, the real-variable DLMF parabolic-cylinder `W` function.

Implemented formula:

```text
W(a,x) =
  sqrt(k/2) * exp(pi*a/4) *
  (
    exp(i*rho)  * U(i*a,  x*exp(-pi*i/4))
    + exp(-i*rho) * U(-i*a, x*exp(pi*i/4))
  )

1/k  = sqrt(1 + exp(2*pi*a)) + exp(pi*a)
rho  = pi/8 + phi2/2
phi2 = ph Gamma(1/2 + i*a)
```

The implementation computes `phi2` from the principal-log difference
`(loggamma(1/2+ia) - loggamma(1/2-ia)) / (2i)`.

Source identity:
DLMF 12.14.4 gives the connection formula for `W(a,x)`. DLMF 12.14.5 gives
the stable reciprocal form for `k`, DLMF 12.14.6 gives `rho`, and DLMF 12.14.7
defines `phi2`.

Domain assumptions:

- Certified mode accepts real `a`.
- Certified mode accepts real `x`.
- Complex `a` and complex `x` are rejected before formula evaluation.

Branch convention:
The DLMF formula is for real `x`. The rotated arguments enter the shared `pcfu`
formula as complex values. The phase calculation uses Arb principal loggamma;
agreement with the continuous DLMF phase convention is part of the remaining
audit.

Known exclusions:
complex parameter; complex argument; unreviewed continuation away from real
`x`.

Tests covering the identity:

- `test_certified_parabolic_cylinder_core_covers_mpmath` compares real samples
  against mpmath.
- `test_certified_pcfw_rejects_complex_argument` checks clean failure for
  complex arguments.
- `test_parabolic_cylinder_certified_results_keep_formula_audit_visible` checks
  formula and scope diagnostics.
- `test_certified_pcfw_matches_connection_formula_round_trip` checks both
  `W(a,x)` and `W(a,-x)` against the DLMF 12.14.4 connection formulas built from
  `U(ia, x exp(-pi i/4))` and `U(-ia, x exp(pi i/4))`.
- `test_pcfw_phi2_principal_loggamma_phase_is_locally_continuous` checks local
  continuity and odd symmetry of the principal-loggamma `phi2` calculation used
  by the connection formula.
- `test_certified_pcfw_satisfies_real_variable_differential_equation_residual`
  checks the real-variable residual `W''(a,x) + (x^2/4 - a) W(a,x) = 0` on
  representative real grids.

Audit note:
connection round-trip, phase-continuity, and real-variable residual coverage are
now part of the first-pass audit. Complex `x` remains outside the certified
`pcfw` domain.

Status:
experimental_formula.
