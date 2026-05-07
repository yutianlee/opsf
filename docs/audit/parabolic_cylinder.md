# Parabolic-Cylinder Certification Audit

Function:
`pcfu(a, z)`, `pcfd(v, z)`, `pbdv(v, x)`, `pcfv(a, z)`, `pcfw(a, x)`.

Target mathematical definition:
DLMF parabolic-cylinder functions `U(a,z)`, `D_v(z)`, `D_v'(z)`, `V(a,z)`,
and real-variable `W(a,x)`.

Backend primitive or formula:
Formula-derived Arb paths using `hypgeom_1f1`, reciprocal gamma, elementary
operations, and connection formulas. See [`../formula_audit.md`](../formula_audit.md)
for formula-by-formula details.

Accepted domain:
Real parameters. `pcfu`, `pcfd`, `pbdv`, and `pcfv` accept real or complex
arguments through the current documented formula paths; for `pbdv`, the public
argument name `x` is retained for compatibility but the certified formula path
documents complex arguments. `pcfw` accepts real arguments only.

Excluded domain:
Complex parameters; complex `pcfw` arguments; non-finite inputs; any formula
evaluation where Arb does not return a finite enclosure.

Branch convention:
The implemented formulas use Arb principal elementary, gamma, loggamma, and
hypergeometric conventions. The audit intentionally keeps this narrower than a
broad claim over every continuation of the DLMF functions.

Singularities:
Gamma-factor poles and connection-formula phase behavior are handled only within
the documented real-parameter formula domains. Unsupported or non-finite cases
must fail cleanly as non-certified results.

Validation identities:
Differential-equation residual checks for `U` and `W`, branch-side recurrences
for `U`, direct recurrence and shifted differential-equation residual checks for
`D_v`, derivative relation for `D_v`, `D_v(z) = U(-v - 1/2,z)`, branch-side
`U`/`V` connection-formula residuals, independent `V` recurrence checks, `W`
connection round-trips, and `phi2` phase-continuity checks.

Reference equations:
DLMF 12.2 for definitions and connections, DLMF 12.7 for hypergeometric local
solutions, DLMF 12.8 for recurrence and derivative identities, and DLMF 12.14
for the `W(a,x)` connection formula.

Known numerical risks:
Branch continuation away from audited grids, gamma factor cancellation, and
relying on formula equivalence rather than a single Arb target-function
primitive.

Certification status:
`certificate_level="formula_audited_experimental"`. Arb rigorously encloses the
implemented documented formula, but this is not the same as a completed global
formula and branch audit for every advertised continuation. Keep the wording:
"certified Arb enclosure of the implemented documented formula; formula audit in
progress".
