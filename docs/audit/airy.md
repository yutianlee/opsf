# Airy Certification Audit

Function:
`airy(z)`, `ai(z, derivative=0|1)`, `bi(z, derivative=0|1)`.

Target mathematical definition:
Airy Ai and Bi solutions of `y'' - z y = 0`, with first derivatives where
requested.

Backend primitive or formula:
Direct Arb Airy primitive through python-flint `arb/acb.airy`.

Accepted domain:
Real and complex arguments supported by Arb Airy primitives. Real arguments use
certificate scope `phase3_real_airy`; complex arguments use
`arb_complex_airy`.

Excluded domain:
Derivative orders other than 0 and 1; non-finite inputs; any domain where Arb
does not return finite component enclosures.

Branch convention:
Arb Airy convention for real and complex arguments.

Singularities:
Ai and Bi are entire functions; no finite singularities are expected.

Validation identities:
Component comparisons against high-precision references, real-domain Wronskian
`Ai(z) Bi'(z) - Ai'(z) Bi(z) = 1/pi`, and large positive argument decay checks
for Ai.

Reference equations:
DLMF 9.2 for Airy definitions and DLMF 9.2.12 for the Wronskian identity.

Known numerical risks:
Large positive or negative arguments, component serialization for multi-value
results, and propagation of component radii in Wronskian checks.

Certification status:
`certificate_level="direct_arb_primitive"`. Certified results enclose direct
Arb Airy primitive output for the documented target function and domain.
