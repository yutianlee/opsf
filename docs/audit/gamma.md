# Gamma Certification Audit

Function:
`gamma(z)`, `loggamma(z)`, `rgamma(z)`, `gamma_ratio(a, b)`.

Target mathematical definition:
Euler gamma function, principal logarithm of gamma, and reciprocal gamma
function `1/gamma(z)`. `gamma_ratio(a, b)` is `Gamma(a) / Gamma(b)`.

Backend primitive or formula:
Direct Arb primitives through python-flint: `arb/acb.gamma`,
`arb/acb.lgamma`, and `arb/acb.rgamma`. The certified `gamma_ratio` path uses
the audited product `Gamma(a) * rgamma(b)`.

Accepted domain:
Real or complex inputs accepted by Arb for the corresponding primitive, when
the requested target value is finite. `rgamma` accepts non-positive integer
gamma poles and returns the exact certified reciprocal-gamma zero reported by
Arb. `gamma_ratio` accepts denominator poles as certified zeros when
`Gamma(a)` is finite.

Excluded domain:
`gamma` and `loggamma` at poles; `gamma_ratio` when `a` is a gamma pole,
including simultaneous numerator/denominator poles; non-finite input values;
any domain where Arb does not return a finite enclosure.

Branch convention:
`loggamma` follows Arb's principal branch. Branch-side tests cover the negative
real axis away from poles.

Singularities:
`gamma` and `loggamma` have poles at non-positive integers. `rgamma` has zeros
at those points. `gamma_ratio(a, b)` has a certified zero when `b` is a pole and
`Gamma(a)` is finite; numerator poles are reported as non-certified failures.

Validation identities:
`gamma(z + 1) = z gamma(z)`, `rgamma(z) gamma(z) = 1` away from poles, and
`rgamma(-n) = 0` for non-negative integers `n`. Gamma-ratio tests cover
`gamma_ratio(a+1,b) = a gamma_ratio(a,b)`,
`gamma_ratio(a,b+1) = gamma_ratio(a,b) / b`, and
`gamma_ratio(a,b) gamma_ratio(b,c) = gamma_ratio(a,c)`.

Reference equations:
DLMF 5.2 for gamma definitions, DLMF 5.4 for recurrence, and Arb gamma
primitive documentation.

Known numerical risks:
Pole neighborhoods, branch-side evaluation for `loggamma`, and cancellation in
identity residual checks near singularities. `gamma_ratio` uses `rgamma(b)` to
avoid introducing non-finite denominator-pole divisions.

Certification status:
`certificate_level="direct_arb_primitive"`. Certified `gamma`, `loggamma`, and
`rgamma` results enclose direct Arb primitive output for the documented target
function and domain. Certified `gamma_ratio` results use
`certificate_scope="direct_arb_gamma_ratio"` and enclose the audited Arb
`Gamma(a) * rgamma(b)` product.
