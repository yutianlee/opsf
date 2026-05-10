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
[`certification_audit.md`](certification_audit.md). Family-level audit
checklists live under [`audit/`](audit/).
The active 0.3.0 development scope is recorded in
[`certified_scope_0_3_0.md`](certified_scope_0_3_0.md). The published 0.2.0
alpha certified surface remains recorded in
[`certified_scope_0_2_0.md`](certified_scope_0_2_0.md). The frozen 0.1.0
certified surface remains archived in
[`certified_scope_0_1_0.md`](certified_scope_0_1_0.md).

## 0.3.0 Development Certified Scope

The 0.3.0 development line keeps the 0.2 public wrapper surface and adds one
explicit custom asymptotic method for positive-real `loggamma`. Default
certified `loggamma` remains the direct Arb primitive path. The current status
matrix is:

| Area | Release status |
| --- | --- |
| `gamma`, `loggamma`, `rgamma`, `gamma_ratio`, `loggamma_ratio`, `beta`, `pochhammer` | alpha-certified, direct Arb gamma primitives and finite products |
| `erf`, `erfc`, `erfcx`, `erfi`, `dawson`, `erfinv`, `erfcinv` | alpha-certified, direct Arb error-function primitives plus erfcx, erfi, and dawson identity formulas; real erfinv on (-1, 1); real erfcinv on (0, 2) |
| `airy`, `ai`, `bi` | alpha-certified, direct Arb primitive |
| `besselj`, `bessely`, `besseli`, `besselk` | alpha-certified where direct Arb primitive works; real-valued order only |
| `pcfd`, `pcfu`, `pcfv`, `pcfw`, `pbdv` | experimental certified formula layer |
| MCP server | experimental tool interface |
| Custom Taylor/asymptotic methods | alpha-certified custom asymptotic bound for positive-real loggamma via explicit `method="stirling"`; real `x >= 20`; not automatic default selection |

## Result Contract

Certified results set:

- `certified=True`
- `backend="python-flint"`
- `method="arb_ball"`, `method="stirling_loggamma"`, or a documented Arb
  formula method
- `abs_error_bound` to a rigorous absolute radius
- `diagnostics["certificate_scope"]` to one of the scopes below
- `diagnostics["certificate_level"]` to `direct_arb_primitive` for direct Arb
  primitive paths, `direct_arb_finite_product` for audited finite-product
  paths, `certified_real_root` for a monotone real-root inverse certificate,
  `custom_asymptotic_bound` for documented custom asymptotic bounds,
  `formula_audited_alpha` for a narrowly audited identity formula, or
  `formula_audited_experimental` for formula-backed certificates with open
  formula audit work
- `diagnostics["audit_status"]` to `audited_direct` for direct Arb primitive
  paths, `monotone_real_inverse` for real inverse-root certificates,
  `theorem_documented` for documented custom asymptotic theorems,
  `formula_identity` for a narrowly audited identity formula, or
  `experimental_formula` for formula-backed paths with open audit work
- `diagnostics["certification_claim"]` to the precise claim wording for that
  audit status

Unsupported certified domains return `certified=False`, `value=""`, and a
diagnostic error. They must not fall back to a non-certified backend while
claiming certification.

## Gamma Family

Function:
`gamma(z)`, `loggamma(z)`, `rgamma(z)`, `gamma_ratio(a, b)`,
`loggamma_ratio(a, b)`, `beta(a, b)`, `pochhammer(a, n)`

Certified domain:
real or complex inputs accepted by Arb for the corresponding primitive, with
non-finite target values reported as clean failures. For `gamma_ratio(a, b)`,
`Gamma(a)` must be finite; non-positive integer poles in `b` certify to zero
through reciprocal gamma.
For `loggamma_ratio(a, b)`, both `loggamma(a)` and `loggamma(b)` must be
finite.
For `beta(a, b)`, `Gamma(a)` and `Gamma(b)` must be finite; non-positive
integer poles in `a+b` certify to zero through reciprocal gamma.
For `pochhammer(a, n)`, certified mode supports integer `n >= 0` through the
finite product `product_{k=0}^{n-1} (a+k)`. The `n = 0` case certifies to `1`,
and exact zero factors certify to zero.
For explicit `loggamma(x, method="stirling")`, certified mode additionally
supports real `x >= 20` through the positive-real Stirling expansion. This is
an explicit method only and does not replace the default direct Arb path.

Backend primitive:
`arb/acb.gamma`, `arb/acb.lgamma`, and `arb/acb.rgamma`. The explicit
`loggamma(method="stirling")` path evaluates a finite positive-real Stirling
sum with Arb ball arithmetic and adds a documented first-omitted-term tail
bound. The certified
`gamma_ratio` backend evaluates `Gamma(a) * rgamma(b)` using Arb gamma
primitives rather than dividing by `Gamma(b)`. The certified
`loggamma_ratio` backend evaluates Arb `lgamma(a) - lgamma(b)`. The certified
`beta` backend evaluates `Gamma(a) * Gamma(b) * rgamma(a+b)`. The certified
`pochhammer` backend evaluates the finite product with Arb ball arithmetic.

Returned enclosure:
Arb midpoint string plus absolute radius. `rgamma` returns an exact certified
zero at non-positive integer gamma poles when Arb reports that enclosure.
`gamma_ratio` returns an exact certified zero for denominator poles when
`Gamma(a)` is finite and Arb reports the zero product.
`beta` returns an exact certified zero for `Gamma(a+b)` denominator poles when
`Gamma(a)` and `Gamma(b)` are finite and Arb reports the zero product.
`pochhammer` returns Arb midpoint and radius for the finite product, including
an exact certified zero when a product factor is exactly zero.
`loggamma(method="stirling")` returns a midpoint string plus a conservative
absolute bound including the Arb finite-sum radius and the explicit
asymptotic tail bound.

Branch convention:
`loggamma` follows the principal branch used by Arb. `loggamma_ratio` is the
difference of principal `loggamma` values; for complex values this is not
necessarily the same as the principal logarithm of `gamma_ratio`.

Formula transformations:
`gamma_ratio(a, b)` is evaluated as `Gamma(a) * rgamma(b)` for denominator-pole
handling. The one-argument gamma-family wrappers use no formula transformation.
`loggamma_ratio(a, b)` is evaluated as a direct difference of Arb principal
`lgamma` values. `beta(a, b)` is evaluated as
`Gamma(a) * Gamma(b) * rgamma(a+b)` for denominator-pole handling.
`pochhammer(a, n)` is evaluated as a finite product only for certified
integer `n >= 0`.
`loggamma(x, method="stirling")` is evaluated as the documented positive-real
Stirling expansion only for real `x >= 20`; method omission and
`method="auto"` continue to use the direct Arb primitive in certified mode.

Known exclusions:
`gamma` and `loggamma` at poles return non-certified failures because the
requested value is not finite. `gamma_ratio` returns a clean non-certified
failure when `a` is a gamma pole, including the simultaneous pole case.
`loggamma_ratio` returns clean non-certified failures when either argument is a
gamma pole, including simultaneous pole cases.
`beta` returns clean non-certified failures when `a` or `b` is a gamma pole,
including simultaneous numerator and denominator pole interactions.
`pochhammer` returns clean non-certified failures for non-integer `n`, negative
`n`, product lengths above the documented ceiling, and simultaneous-pole
limiting values not covered by the finite-product zero-factor proof.
`loggamma(method="stirling")` returns clean non-certified failures for complex
inputs, non-finite input, `x < 20`, `x <= 0`, principal-branch complex
`loggamma` requests, and gamma-ratio asymptotics.

Validation tests:
pole behavior, principal-branch checks on the negative real axis, gamma-ratio
recurrence and composition identities, loggamma-ratio branch and identity
checks, beta symmetry and recurrence identities, and comparison against mpmath
away from singularities. Pochhammer tests cover finite-product special values,
complex `a` with integer `n`, zero factors, certified recurrence, dispatch
behavior, and rejected certified domains. Stirling-loggamma tests cover
positive-real samples, Arb-reference containment, rejected inputs, MCP parity,
and preservation of direct Arb default selection.

Certificate scope:
`direct_arb_primitive` for `gamma`, `loggamma`, and `rgamma`; the narrow
`direct_arb_gamma_ratio` scope for `gamma_ratio`; and the narrow
`direct_arb_loggamma_ratio` scope for `loggamma_ratio`; and the narrow
`direct_arb_beta` scope for `beta`; and `direct_arb_pochhammer_product` for
`pochhammer`, recorded through `method="arb_ball"`. The explicit custom
positive-real Stirling method for `loggamma` uses
`stirling_loggamma_positive_real`, recorded through
`method="stirling_loggamma"`.

## Error-Function Family

Function:
`erf(z)`, `erfc(z)`, `erfcx(z)`, `erfi(z)`, `dawson(z)`, `erfinv(x)`,
`erfcinv(x)`

Certified domain:
`erf`, `erfc`, `erfcx`, `erfi`, and `dawson` accept real or complex inputs
accepted by Arb for the corresponding error-function primitive or identity
formula, with non-finite target values reported as clean failures. Certified
`erfinv` is restricted to real `x` with `-1 < x < 1` on the real principal
inverse branch; endpoints, out-of-interval values, and complex inputs are clean
non-certified failures. Certified `erfcinv` is restricted to real `x` with
`0 < x < 2` on the real principal inverse branch; endpoints, out-of-interval
values, and complex inputs are clean non-certified failures.

Backend primitive:
`arb/acb.erf` and `arb/acb.erfc`. If a supported python-flint build exposes
direct `erf` but not direct `erfc`, the certified `erfc` backend may evaluate
the Arb expression `1 - erf(z)` and records `formula="1-erf"`.
Certified `erfcx` prefers direct Arb `erfcx` if exposed by python-flint;
otherwise it evaluates `exp(z^2) * erfc(z)` with Arb ball arithmetic and
records `formula="exp(z^2)*erfc(z)"`.
Certified `erfi` prefers direct Arb `erfi` if exposed by python-flint;
otherwise it evaluates `-i*erf(i*z)` with Arb ball arithmetic and records
`formula="-i*erf(i*z)"`.
Certified `dawson` prefers direct Arb `dawson` if exposed by python-flint;
otherwise it evaluates `sqrt(pi)/2*exp(-z^2)*erfi(z)` with Arb ball arithmetic
and records `formula="sqrt(pi)/2*exp(-z^2)*erfi(z)"`.
Certified `erfinv` prefers direct Arb `erfinv` if exposed by python-flint;
otherwise it brackets the unique real root of `erf(y)-x=0` using monotonicity
of real `erf` and records `formula="erf(y)-x=0"`.
Certified `erfcinv` prefers direct Arb `erfcinv` if exposed by python-flint;
otherwise it uses the certified real-inverse path for `erfinv(1-x)` and
records `formula="erfinv(1-x)"`.

Returned enclosure:
Arb midpoint string plus absolute radius.

Branch convention:
`erf`, `erfc`, `erfcx`, `erfi`, and `dawson` are entire functions. These
wrappers follow Arb's complex primitive and elementary-function conventions.
`erfinv` uses only the real principal inverse branch on `(-1, 1)`.
`erfcinv` uses only the real principal inverse branch on `(0, 2)`.

Formula transformations:
none for `erf`; direct `erfc` is preferred. The only allowed certified `erfc`
fallback is the explicit Arb expression `1 - erf(z)`.
For `erfcx`, direct Arb `erfcx` is preferred when available. The allowed
formula fallback is the explicit Arb expression `exp(z^2) * erfc(z)`.
For `erfi`, direct Arb `erfi` is preferred when available. The allowed formula
fallback is the explicit Arb expression `-i*erf(i*z)`.
For `dawson`, direct Arb `dawson` is preferred when available. The allowed
formula fallback is the explicit Arb expression
`sqrt(pi)/2*exp(-z^2)*erfi(z)`.
For `erfinv`, direct Arb `erfinv` is preferred when available. The allowed
fallback is a certified monotone real-root enclosure for `erf(y)-x=0`.
For `erfcinv`, direct Arb `erfcinv` is preferred when available. The allowed
fallback is the certified real-inverse path for `erfinv(1-x)`.

Known exclusions:
non-finite Arb input or output enclosures and any domain where Arb does not
return a finite enclosure. Certified `erfinv` also excludes complex inverse
branches, `x <= -1`, `x >= 1`, and endpoint asymptotic certification.
Certified `erfcinv` excludes complex inverse branches, `x <= 0`, `x >= 2`,
endpoint asymptotic certification, Faddeeva, plasma dispersion, and `wofz`.
No Taylor or asymptotic certification path is included. The scaled wrapper does
not claim large-argument stability beyond what the selected backend certifies.

Validation tests:
zero values, regular real and complex samples, `erf(-z) = -erf(z)`,
`erfc(z) = 1 - erf(z)`, auto dispatch, MCP parity, external fixtures, and
certified ball containment for `erf(z) + erfc(z) = 1` and
`erf(-z) + erf(z) = 0`. `erfcx` tests cover zero, positive and negative real
values, a complex sample, `erfcx(z) = exp(z^2) erfc(z)`, auto dispatch, MCP
parity, external fixtures, and certified containment of
`exp(z^2)*erfc(z) - erfcx(z) = 0`.
`erfi` tests cover zero, positive and negative real values, a complex sample,
`erfi(z) = -i erf(i z)`, auto dispatch, MCP parity, external fixtures, and
certified containment of `erfi(z) + i*erf(i*z) = 0`.
`dawson` tests cover zero, oddness, positive and negative real values, a
complex sample, `dawson(z) = sqrt(pi)/2 * exp(-z^2) * erfi(z)`, auto dispatch,
MCP parity, external fixtures, and certified containment of the identity
formula.
`erfinv` tests cover zero, real composition with `erf`, oddness, values near
but not too close to endpoints, endpoint and out-of-interval rejection, complex
rejection in certified mode, auto dispatch, MCP parity, external fixtures,
forced real-root fallback diagnostics, and certified residual containment for
`erf(erfinv(x))-x = 0`.
`erfcinv` tests cover `erfcinv(1) = 0`, real composition with `erfc`, the
relation `erfcinv(x) = erfinv(1-x)`, monotonic orientation, values near but not
too close to endpoints, endpoint and out-of-interval rejection, complex
rejection in certified mode, auto dispatch, MCP parity, external fixtures,
forced fallback diagnostics, and certified residual containment for
`erfc(erfcinv(x))-x = 0`.

Certificate scopes:
`direct_arb_erf`, `direct_arb_erfc`, and either `direct_arb_erfcx` or
`arb_erfcx_formula` for `erfcx`, depending on the Arb primitive exposed by the
installed backend. `erfi` uses either `direct_arb_erfi` or
`arb_erfi_formula`, depending on the Arb primitive exposed by the installed
backend. `dawson` uses either `direct_arb_dawson` or
`arb_dawson_formula`, depending on the Arb primitive exposed by the installed
backend. `erfinv` uses either `direct_arb_erfinv` or
`arb_erfinv_real_root`, depending on the Arb primitive exposed by the installed
backend. `erfcinv` uses either `direct_arb_erfcinv` or
`arb_erfcinv_via_erfinv`, depending on the Arb primitive exposed by the
installed backend.

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
