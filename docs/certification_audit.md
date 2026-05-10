# Certification Audit

Last reviewed: 2026-05-10.

This audit is the public map from a certified result to the evidence behind the
claim. It covers every `certificate_scope` that the dispatcher can select in
`mode="certified"`.

Certified successes must include:

- `diagnostics["certificate_scope"]`: the scope listed below.
- `diagnostics["certificate_level"]`: `direct_arb_primitive`,
  `direct_arb_finite_product`, `certified_real_root`,
  `custom_asymptotic_bound`, `formula_audited_alpha`, or
  `formula_audited_experimental`.
- `diagnostics["audit_status"]`: either `audited_direct` or
  `monotone_real_inverse` or `theorem_documented` or `formula_identity` or
  `experimental_formula`.
- `diagnostics["certification_claim"]`: concise wording for the level of claim.

The certificate levels mean:

- `direct_arb_primitive`: the wrapper calls an Arb special-function primitive
  for the documented target function, and repo tests cover representative domain,
  branch, singularity, and result-contract behavior. The
  `direct_arb_gamma_ratio` and `direct_arb_beta` scopes are narrow audited
  compositions of Arb gamma primitives, and `direct_arb_loggamma_ratio` is a
  narrow principal-branch Arb `lgamma` difference, rather than a broader
  formula-layer claim.
- `direct_arb_finite_product`: the wrapper evaluates a finite product with Arb
  ball arithmetic for a documented integer-parameter domain, with explicit
  exclusions for unsupported continuation or pole-limit cases.
- `certified_real_root`: Arb encloses a unique real root on a documented
  monotone real interval. The runtime diagnostics must identify the domain and
  root equation, and unsupported real or complex inputs must fail cleanly.
- `custom_asymptotic_bound`: the wrapper evaluates a documented custom
  asymptotic formula on a narrow domain, computes the finite part with Arb ball
  arithmetic, and adds an explicit theorem-backed tail bound to the returned
  absolute error bound.
- `formula_audited_alpha`: Arb rigorously encloses a narrowly documented
  identity formula for an alpha wrapper. The runtime diagnostics must identify
  the formula and must not imply a broader algorithmic stability claim.
- `formula_audited_experimental`: Arb rigorously encloses the implemented
  formula, and repo tests cover the documented first-pass identities, branches,
  and domains, but the formula-backed family has not been promoted to a broad
  non-experimental certification claim.

Family-level checklists:

- [`audit/gamma.md`](audit/gamma.md)
- [`audit/error_function.md`](audit/error_function.md)
- [`audit/airy.md`](audit/airy.md)
- [`audit/bessel.md`](audit/bessel.md)
- [`audit/parabolic_cylinder.md`](audit/parabolic_cylinder.md)

Static external-reference fixtures in `tests/fixtures/external_reference/`
provide an additional containment check for selected gamma-family,
error-function, Airy, Bessel, and parabolic-cylinder values. This fixture
coverage supplements the scope evidence below; it does not broaden any
certificate level or promote
`experimental_formula` scopes.

## Scope Matrix

| Certificate scope | Wrappers | Certificate level | Evidence | Exclusions |
| --- | --- | --- | --- | --- |
| `direct_arb_primitive` | `gamma`, `loggamma`, `rgamma` | `direct_arb_primitive` | Direct Arb gamma primitives; pole and reciprocal tests; principal `loggamma` branch-side tests | Non-finite `gamma` and `loggamma` targets at poles |
| `direct_arb_gamma_ratio` | `gamma_ratio` | `direct_arb_primitive` | Arb `gamma(a) * rgamma(b)` product; denominator-pole zero tests; numerator-pole clean-failure tests; recurrence and composition identity checks | Non-finite `Gamma(a)` targets, including numerator poles and simultaneous numerator/denominator poles |
| `direct_arb_loggamma_ratio` | `loggamma_ratio` | `direct_arb_primitive` | Arb `lgamma(a) - lgamma(b)` principal-branch difference; pole clean-failure tests; branch convention test; recurrence and composition identity checks | Gamma poles in either argument; simultaneous-pole limiting values; principal-log-of-ratio claims |
| `direct_arb_beta` | `beta` | `direct_arb_primitive` | Arb `Gamma(a) * Gamma(b) * rgamma(a+b)` product; denominator-pole zero tests; numerator-pole clean-failure tests; symmetry and recurrence identity checks | Non-finite `Gamma(a)` or `Gamma(b)` targets; simultaneous pole interactions and limiting-value claims |
| `direct_arb_pochhammer_product` | `pochhammer` | `direct_arb_finite_product` | Arb finite product `prod_{k=0}^{n-1}(a+k)`; special-value tests; zero-factor test; recurrence identity check; integer-domain rejection tests | Non-integer `n`; negative `n`; analytic continuation in `n`; simultaneous-pole limiting values; product paths above the documented term ceiling |
| `stirling_loggamma_positive_real` | `loggamma` via explicit `method="stirling"` or `method="stirling_shifted"`; explicit `method="certified_auto"` may select this scope | `custom_asymptotic_bound` | Positive-real Stirling expansion with Bernoulli terms; Arb finite sum; shifted Arb recurrence for `stirling_shifted`; exact coefficient table through `B_300`; explicit first-omitted-term tail bound; direct Arb containment; MCP parity; default-Arb preservation; explicit selector diagnostics | Complex `z`; `x < 20`; `x <= 0`; non-finite input; principal-branch complex `loggamma`; gamma-ratio asymptotics; default selection |
| `gamma_positive_real_stirling_exp` | `gamma` via explicit `method="stirling_exp"` | `custom_asymptotic_bound` | Certified positive-real `loggamma` Arb enclosure widened by the explicit Stirling tail bound, followed by Arb exponentiation; direct Arb containment; MCP parity; default-Arb preservation | Complex `gamma`; `x < 20`; `x <= 0`; non-finite input; reflection formulas; near-pole behavior; gamma-ratio asymptotics; beta asymptotics; default selection |
| `direct_arb_erf` | `erf` | `direct_arb_primitive` | Direct Arb `erf` primitive; zero, oddness, complex sample, and external-reference containment tests | Non-finite Arb enclosures; custom asymptotic certification paths |
| `direct_arb_erfc` | `erfc` | `direct_arb_primitive` | Direct Arb `erfc` primitive, or explicit Arb `1-erf` fallback with `formula="1-erf"`; zero, complement identity, complex sample, and external-reference containment tests | Non-finite Arb enclosures; unrecorded cancellation-prone fallback formulas; custom asymptotic certification paths |
| `direct_arb_erfcx` | `erfcx` | `direct_arb_primitive` | Direct Arb `erfcx` primitive when exposed by python-flint; runtime scope and diagnostics tests preserve the direct path | Non-finite Arb enclosures; custom asymptotic certification paths |
| `arb_erfcx_formula` | `erfcx` | `formula_audited_alpha` | Arb identity formula `exp(z^2)*erfc(z)` with `formula="exp(z^2)*erfc(z)"`; zero, positive/negative real samples, complex sample, identity containment, MCP parity, and external-reference containment tests | Non-finite Arb enclosures; large-argument scaled-erfc stability claims beyond the backend-certified formula |
| `direct_arb_erfi` | `erfi` | `direct_arb_primitive` | Direct Arb `erfi` primitive when exposed by python-flint; zero, oddness, complex sample, identity containment, MCP parity, and external-reference containment tests | Non-finite Arb enclosures; custom asymptotic certification paths |
| `arb_erfi_formula` | `erfi` | `formula_audited_alpha` | Arb identity formula `-i*erf(i*z)` with `formula="-i*erf(i*z)"`; zero, positive/negative real samples, complex sample, identity containment, MCP parity, and external-reference containment tests | Non-finite Arb enclosures; custom asymptotic certification paths |
| `direct_arb_dawson` | `dawson` | `direct_arb_primitive` | Direct Arb `dawson` primitive when exposed by python-flint; zero, oddness, complex sample, identity containment, MCP parity, and external-reference containment tests | Non-finite Arb enclosures; custom asymptotic certification paths |
| `arb_dawson_formula` | `dawson` | `formula_audited_alpha` | Arb identity formula `sqrt(pi)/2*exp(-z^2)*erfi(z)` with `formula="sqrt(pi)/2*exp(-z^2)*erfi(z)"`; zero, positive/negative real samples, complex sample, identity containment, MCP parity, and external-reference containment tests | Non-finite Arb enclosures; custom asymptotic certification paths |
| `direct_arb_erfinv` | `erfinv` | `direct_arb_primitive` | Direct Arb `erfinv` primitive when exposed by python-flint; zero, oddness, real composition checks, residual containment, MCP parity, and external-reference containment tests | Complex inverse branches; `x <= -1` or `x >= 1`; endpoint asymptotic certification |
| `arb_erfinv_real_root` | `erfinv` | `certified_real_root` | Arb real interval root enclosure for `erf(y)-x=0`, using monotonicity of real `erf`; zero, oddness, real composition checks, forced-fallback diagnostics, residual containment, MCP parity, and external-reference containment tests | Complex inverse branches; `x <= -1` or `x >= 1`; endpoint asymptotic certification |
| `direct_arb_erfcinv` | `erfcinv` | `direct_arb_primitive` | Direct Arb `erfcinv` primitive when exposed by python-flint; unit, composition checks, relation to `erfinv(1-x)`, orientation checks, residual containment, MCP parity, and external-reference containment tests | Complex inverse branches; `x <= 0` or `x >= 2`; endpoint asymptotic certification; Faddeeva or plasma-dispersion wrappers |
| `arb_erfcinv_via_erfinv` | `erfcinv` | `certified_real_root` | Arb real inverse enclosure for `erfcinv(x)=erfinv(1-x)` through the certified `erfinv` real-root path; unit, composition checks, forced-fallback diagnostics, residual containment, MCP parity, and external-reference containment tests | Complex inverse branches; `x <= 0` or `x >= 2`; endpoint asymptotic certification; Faddeeva or plasma-dispersion wrappers |
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

The `direct_arb_loggamma_ratio` scope also uses narrower audited-direct
wording:

```text
certified Arb enclosure of principal loggamma(a) - principal loggamma(b) using direct Arb gamma primitives
```

The `direct_arb_beta` scope uses narrower audited-direct wording:

```text
certified Arb enclosure of Gamma(a) * Gamma(b) * rgamma(a+b) using direct Arb gamma primitives
```

The `direct_arb_pochhammer_product` scope uses finite-product wording:

```text
certified Arb enclosure of finite product prod_{k=0}^{n-1}(a+k) for nonnegative integer n
```

The explicit positive-real Stirling `loggamma` methods use custom-asymptotic
wording:

```text
certified positive-real Stirling loggamma enclosure with explicit asymptotic tail bound
```

The explicit positive-real `gamma` method uses custom-asymptotic wording:

```text
certified positive-real gamma enclosure via certified loggamma exponentiation
```

The error-function scopes use narrow audited-direct wording:

```text
certified Arb enclosure of erf(z) using direct Arb error-function primitive
certified Arb enclosure of erfc(z) using direct Arb complementary error-function primitive
certified Arb enclosure of erfcx(z) using direct Arb scaled complementary error-function primitive
certified Arb enclosure of erfi(z) using direct Arb imaginary error-function primitive
certified Arb enclosure of dawson(z) using direct Arb Dawson primitive
certified Arb enclosure of real principal erfinv(x) using direct Arb inverse error-function primitive
certified Arb enclosure of real principal erfcinv(x) using direct Arb inverse complementary error-function primitive
```

If certified `erfc` uses the allowed Arb fallback, diagnostics record
`formula="1-erf"` and use the claim:

```text
certified Arb enclosure of 1 - erf(z) using direct Arb error-function primitive
```

If certified `erfcx` uses the Arb identity fallback, diagnostics record
`formula="exp(z^2)*erfc(z)"`, use `audit_status="formula_identity"`, and use
the claim:

```text
certified Arb enclosure of exp(z^2)*erfc(z)
```

If certified `erfi` uses the Arb identity fallback, diagnostics record
`formula="-i*erf(i*z)"`, use `audit_status="formula_identity"`, and use the
claim:

```text
certified Arb enclosure of -i*erf(i*z)
```

If certified `dawson` uses the Arb identity fallback, diagnostics record
`formula="sqrt(pi)/2*exp(-z^2)*erfi(z)"`, use
`audit_status="formula_identity"`, and use the claim:

```text
certified Arb enclosure of sqrt(pi)/2*exp(-z^2)*erfi(z)
```

If certified `erfinv` uses the Arb real-root fallback, diagnostics record
`formula="erf(y)-x=0"`, use `audit_status="monotone_real_inverse"`, and use
the claim:

```text
certified real root enclosure for erf(y)-x=0 using monotonicity of real erf
```

If certified `erfcinv` uses the allowed fallback through the certified
`erfinv` path, diagnostics record `formula="erfinv(1-x)"`, use
`audit_status="monotone_real_inverse"`, and use the claim:

```text
certified real inverse enclosure for erfcinv(x)=erfinv(1-x) using monotonicity of real erfc
```

For `experimental_formula` scopes, runtime diagnostics use:

```text
certified Arb enclosure of the implemented documented formula; formula audit in progress
```

The narrow audited-direct wordings are deliberately specific about the Arb
expression being enclosed. Formula-backed scopes still require an explicit
promotion review before any broader non-experimental claim.

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
