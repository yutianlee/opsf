# Gamma Certification Audit

Function:
`gamma(z)`, `loggamma(z)`, `rgamma(z)`, `gamma_ratio(a, b)`,
`loggamma_ratio(a, b)`, `beta(a, b)`, `pochhammer(a, n)`.

Target mathematical definition:
Euler gamma function, principal logarithm of gamma, and reciprocal gamma
function `1/gamma(z)`. `gamma_ratio(a, b)` is `Gamma(a) / Gamma(b)`.
`loggamma_ratio(a, b)` is principal `loggamma(a) - loggamma(b)`.
`beta(a, b)` is the Euler beta function `Gamma(a) Gamma(b) / Gamma(a+b)`.
`pochhammer(a, n)` is the rising factorial `(a)_n = Gamma(a+n) / Gamma(a)`.

Backend primitive or formula:
Direct Arb primitives through python-flint: `arb/acb.gamma`,
`arb/acb.lgamma`, and `arb/acb.rgamma`. The certified `gamma_ratio` path uses
the audited product `Gamma(a) * rgamma(b)`. The certified `loggamma_ratio` path
uses the audited Arb `lgamma(a) - lgamma(b)` difference. The certified `beta`
path uses the audited product `Gamma(a) * Gamma(b) * rgamma(a+b)`.
The certified `pochhammer` path uses the audited finite product
`prod_{k=0}^{n-1}(a+k)` for integer `n >= 0`. Explicit
`loggamma(x, method="stirling")` uses the positive-real Stirling expansion,
with Arb ball arithmetic for the finite Bernoulli sum and an explicit
first-omitted-term asymptotic tail bound. Explicit
`loggamma(x, method="stirling_shifted")` applies the same positive-real
Stirling theorem at `y = x + r` and subtracts the Arb finite recurrence
`sum(log(x+j))`. Explicit `loggamma(x, method="certified_auto")` is a selector
that may choose direct Arb or one of those positive-real Stirling methods; it
does not evaluate a new formula.
Explicit `gamma(x, method="stirling_exp")` widens the certified positive-real
`loggamma` Arb enclosure by its explicit tail bound and evaluates `exp` using
Arb ball arithmetic.

Accepted domain:
Real or complex inputs accepted by Arb for the corresponding primitive, when
the requested target value is finite. `rgamma` accepts non-positive integer
gamma poles and returns the exact certified reciprocal-gamma zero reported by
Arb. `gamma_ratio` accepts denominator poles as certified zeros when
`Gamma(a)` is finite.
`loggamma_ratio` accepts only arguments where both principal `loggamma` terms
are finite.
`beta` accepts denominator `Gamma(a+b)` poles as certified zeros when
`Gamma(a)` and `Gamma(b)` are finite.
`pochhammer` accepts real or complex `a` with integer `n >= 0`, subject to the
finite-product ceiling, and certifies exact zero factors to zero.
Explicit `loggamma(method="stirling")` and
`loggamma(method="stirling_shifted")` accept finite real `x >= 20` only.
Explicit `loggamma(method="certified_auto")` uses direct Arb outside that
positive-real Stirling scope.
Explicit `gamma(method="stirling_exp")` accepts finite real `x >= 20` only.

Excluded domain:
`gamma` and `loggamma` at poles; `gamma_ratio` when `a` is a gamma pole,
including simultaneous numerator/denominator poles; non-finite input values;
`loggamma_ratio` when either argument is a gamma pole, including simultaneous
pole cases; `beta` when `a` or `b` is a gamma pole, including simultaneous pole
interactions; any domain where Arb does not return a finite enclosure.
`pochhammer` excludes non-integer `n`, negative `n`, product lengths above the
documented ceiling, analytic continuation in `n`, and simultaneous-pole
limiting values not covered by the zero-factor finite-product case.
Explicit `loggamma(method="stirling")` and
`loggamma(method="stirling_shifted")` exclude complex inputs, non-finite
inputs, `x < 20`, `x <= 0`, principal-branch complex `loggamma`, and
gamma-ratio asymptotics. The explicit `certified_auto` selector may choose
direct Arb for unsupported Stirling domains, but it does not add complex
Stirling or gamma-ratio asymptotics.
Explicit `gamma(method="stirling_exp")` excludes complex gamma, non-finite
inputs, `x < 20`, `x <= 0`, reflection-formula paths, near-pole behavior,
gamma-ratio asymptotics, and beta asymptotics.

Branch convention:
`loggamma` follows Arb's principal branch. `loggamma_ratio` is the difference
of principal `loggamma` values and is not necessarily the principal logarithm
of `gamma_ratio` for complex inputs. Branch-side tests cover the negative real
axis away from poles.

Singularities:
`gamma` and `loggamma` have poles at non-positive integers. `rgamma` has zeros
at those points. `gamma_ratio(a, b)` has a certified zero when `b` is a pole and
`Gamma(a)` is finite; numerator poles are reported as non-certified failures.
`loggamma_ratio(a, b)` reports any pole in either argument as a non-certified
failure.
`beta(a, b)` has a certified zero when `a+b` is a pole and both numerator gamma
factors are finite; numerator poles are reported as non-certified failures.
`pochhammer(a, n)` has a certified zero when an exact factor `a+k` is zero.
When both `Gamma(a)` and `Gamma(a+n)` have poles and no zero-factor case
applies, the certified wrapper returns a clean non-certified failure.

Validation identities:
`gamma(z + 1) = z gamma(z)`, `rgamma(z) gamma(z) = 1` away from poles, and
`rgamma(-n) = 0` for non-negative integers `n`. Gamma-ratio tests cover
`gamma_ratio(a+1,b) = a gamma_ratio(a,b)`,
`gamma_ratio(a,b+1) = gamma_ratio(a,b) / b`, and
`gamma_ratio(a,b) gamma_ratio(b,c) = gamma_ratio(a,c)`.
Loggamma-ratio tests cover the additive recurrence identities
`loggamma_ratio(a+1,b) - loggamma_ratio(a,b) = log(a)`,
`loggamma_ratio(a,b+1) - loggamma_ratio(a,b) = -log(b)`, and
`loggamma_ratio(a,b) + loggamma_ratio(b,c) = loggamma_ratio(a,c)`.
Beta tests cover symmetry and the recurrence identities
`beta(a+1,b) = a/(a+b) beta(a,b)` and
`beta(a,b+1) = b/(a+b) beta(a,b)`.
Pochhammer tests cover special finite products, complex `a`, zero factors, and
`pochhammer(a,n+1) = (a+n) pochhammer(a,n)`.

Reference equations:
DLMF 5.2 for gamma definitions, DLMF 5.4 for recurrence, and Arb gamma
primitive documentation.

Known numerical risks:
Pole neighborhoods, branch-side evaluation for `loggamma`, and cancellation in
identity residual checks near singularities. `gamma_ratio` uses `rgamma(b)` to
avoid introducing non-finite denominator-pole divisions.
`loggamma_ratio` follows principal branches, so complex values can differ from
the principal logarithm of `gamma_ratio` by integer multiples of `2*pi*i`.
`beta` uses `rgamma(a+b)` to avoid introducing non-finite denominator-pole
divisions, but it does not claim limiting values at simultaneous singularities.
`pochhammer` uses finite products to avoid gamma quotient pole ambiguity in the
supported integer-`n` path. Large product lengths can accumulate wide balls, so
the certified path has a documented term ceiling rather than a gamma fallback.
The explicit Stirling methods are restricted to positive real inputs with
`x >= 20`; they are not selected automatically and do not certify branch-cut or
complex-principal-loggamma behavior. Explicit `method="certified_auto"` keeps
that scope narrow and leaves omitted-method and `method="auto"` dispatch on the
direct Arb path.
Explicit `gamma(method="stirling_exp")` is restricted to finite positive real
inputs with `x >= 20`; it is not selected automatically and does not certify
reflection formulas or complex gamma behavior.

Certification status:
`certificate_level="direct_arb_primitive"`. Certified `gamma`, `loggamma`, and
`rgamma` results enclose direct Arb primitive output for the documented target
function and domain. Certified `gamma_ratio` results use
`certificate_scope="direct_arb_gamma_ratio"` and enclose the audited Arb
`Gamma(a) * rgamma(b)` product. Certified `loggamma_ratio` results use
`certificate_scope="direct_arb_loggamma_ratio"` and enclose the audited Arb
principal `lgamma(a) - lgamma(b)` difference. Certified `beta` results use
`certificate_scope="direct_arb_beta"` and enclose the audited Arb
`Gamma(a) * Gamma(b) * rgamma(a+b)` product.
Certified `pochhammer` results use
`certificate_scope="direct_arb_pochhammer_product"` and enclose the audited Arb
finite product for nonnegative integer `n`.
Explicit `loggamma(method="stirling")` and
`loggamma(method="stirling_shifted")` results use
`certificate_scope="stirling_loggamma_positive_real"`,
`certificate_level="custom_asymptotic_bound"`, and
`audit_status="theorem_documented"`. Explicit `method="certified_auto"`
preserves the selected backend's method and certificate scope and adds selector
diagnostics.
Explicit `gamma(method="stirling_exp")` results use
`certificate_scope="gamma_positive_real_stirling_exp"`,
`certificate_level="custom_asymptotic_bound"`, and
`audit_status="theorem_documented"`.
