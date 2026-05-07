# Gamma Certification Audit

Function:
`gamma(z)`, `loggamma(z)`, `rgamma(z)`.

Target mathematical definition:
Euler gamma function, principal logarithm of gamma, and reciprocal gamma
function `1/gamma(z)`.

Backend primitive or formula:
Direct Arb primitives through python-flint: `arb/acb.gamma`,
`arb/acb.lgamma`, and `arb/acb.rgamma`.

Accepted domain:
Real or complex inputs accepted by Arb for the corresponding primitive, when
the requested target value is finite. `rgamma` accepts non-positive integer
gamma poles and returns the exact certified reciprocal-gamma zero reported by
Arb.

Excluded domain:
`gamma` and `loggamma` at poles; non-finite input values; any domain where Arb
does not return a finite enclosure.

Branch convention:
`loggamma` follows Arb's principal branch. Branch-side tests cover the negative
real axis away from poles.

Singularities:
`gamma` and `loggamma` have poles at non-positive integers. `rgamma` has zeros
at those points.

Validation identities:
`gamma(z + 1) = z gamma(z)`, `rgamma(z) gamma(z) = 1` away from poles, and
`rgamma(-n) = 0` for non-negative integers `n`.

Reference equations:
DLMF 5.2 for gamma definitions, DLMF 5.4 for recurrence, and Arb gamma
primitive documentation.

Known numerical risks:
Pole neighborhoods, branch-side evaluation for `loggamma`, and cancellation in
identity residual checks near singularities.

Certification status:
`certificate_level="direct_arb_primitive"`. Certified results enclose direct
Arb primitive output for the documented target function and domain.
