# Bessel Certification Audit

Function:
`besselj(v, z)`, `bessely(v, z)`, `besseli(v, z)`, `besselk(v, z)`.

Target mathematical definition:
Bessel functions `J_v(z)`, `Y_v(z)`, modified Bessel functions `I_v(z)` and
`K_v(z)`.

Backend primitive or formula:
Direct Arb/acb Bessel primitives through python-flint.

Accepted domain:
Real-valued order with real or complex argument. Integer real-order and real
argument cases use certificate scope `phase4_integer_real_bessel`; other
real-order supported cases use `phase5_real_order_complex_bessel`.

Excluded domain:
Complex order; non-finite inputs; singular or branch domains where Arb does not
return a finite enclosure.

Branch convention:
Arb branch conventions for `Y_v` and `K_v`, including cuts inherited from the
underlying Arb/acb implementation.

Singularities:
Function-dependent behavior near zero and along branch cuts, especially for
`Y_v` and `K_v`.

Validation identities:
Three-term recurrence checks for `J`, `Y`, `I`, and `K`; comparison grids
against high-precision references; near-zero checks for `J_v`; branch-side
checks for `K_v`.

Reference equations:
DLMF 10.2 for Bessel definitions, DLMF 10.6 for recurrence relations, and Arb
Bessel primitive documentation.

Known numerical risks:
Near-zero evaluation, branch cuts for `Y_v` and `K_v`, cancellation in
recurrences, and real-order versus complex-order domain boundaries.

Certification status:
`certificate_level="direct_arb_primitive"`. Certified results enclose direct
Arb Bessel primitive output for the documented real-order target domain.
