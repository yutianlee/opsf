# Error-Function Certification Audit

Last reviewed: 2026-05-10.

Function:
`erf(z)`, `erfc(z)`, `erfcx(z)`, `erfi(z)`, `dawson(z)`.

Public API:
`erf`, `erfc`, `erfcx`, `erfi`, and `dawson` are exported from
`certsf.__init__`, listed in `certsf.__all__`, registered in the dispatcher
with `fast`, `high_precision`, and `certified` modes, and exposed through thin
MCP tools named `special_erf`, `special_erfc`, `special_erfcx`, `special_erfi`,
and `special_dawson`. No `erfinv`, `erfcinv`, Faddeeva wrapper, or plasma
dispersion wrapper is part of this audit scope.

Target mathematical definition:
`erf(z) = 2/sqrt(pi) * integral_0^z exp(-t^2) dt`.
`erfc(z) = 1 - erf(z)`.
`erfcx(z) = exp(z^2) erfc(z)`.
`erfi(z) = -i erf(i z)`.
`dawson(z) = sqrt(pi)/2 * exp(-z^2) * erfi(z)`.

Backend primitive or formula:
Direct Arb error-function primitives through python-flint: `arb/acb.erf` and
`arb/acb.erfc`. If a supported python-flint build exposes `erf` but not
`erfc`, the certified `erfc` path may use the audited Arb arithmetic expression
`1 - erf(z)` and records `formula="1-erf"`.
For `erfcx`, the certified path prefers a direct Arb `erfcx` primitive when
available. Otherwise it evaluates the audited Arb identity
`exp(z^2) * erfc(z)` and records `formula="exp(z^2)*erfc(z)"`.
For `erfi`, the certified path prefers a direct Arb `erfi` primitive when
available. Otherwise it evaluates the audited Arb identity `-i*erf(i*z)` and
records `formula="-i*erf(i*z)"`.
For `dawson`, the certified path prefers a direct Arb `dawson` primitive when
available. Otherwise it evaluates the audited Arb identity
`sqrt(pi)/2 * exp(-z^2) * erfi(z)` and records
`formula="sqrt(pi)/2*exp(-z^2)*erfi(z)"`.

Accepted domain:
Real or complex inputs accepted by Arb for the corresponding error-function
primitive or identity formula, when the requested target value has a finite Arb
enclosure.

Excluded domain:
Non-finite input or output enclosures and any domain where Arb does not return a
finite enclosure. No custom asymptotic or Taylor certification path is included,
and no large-argument scaled-erfc stability claim is made beyond backend
certification of the selected expression.

Branch convention:
The error-function family entries here are entire. The certified wrappers
follow Arb's complex elementary-function conventions for the direct primitives
and the `exp(z^2)*erfc(z)`, `-i*erf(i*z)`, and
`sqrt(pi)/2*exp(-z^2)*erfi(z)` formulas.

Singularities:
No finite singularities for `erf`, `erfc`, `erfcx`, `erfi`, or `dawson`;
failures are limited to unsupported or non-finite Arb enclosure cases.

Validation identities:
Tests cover `erf(0) = 0`, `erfc(0) = 1`, regular real and complex samples,
`erf(-z) = -erf(z)`, and certified ball containment for
`erf(z) + erfc(z) = 1`. `erfcx` tests cover `erfcx(0) = 1`, positive and
negative real samples, a complex sample, external-reference containment, and
certified identity containment for `exp(z^2)*erfc(z) - erfcx(z) = 0`.
`erfi` tests cover `erfi(0) = 0`, positive and negative real samples, a complex
sample, external-reference containment, and certified identity containment for
`erfi(z) + i*erf(i*z) = 0`.
`dawson` tests cover `dawson(0) = 0`, oddness, positive and negative real
samples, a complex sample, external-reference containment, and certified
identity containment for `dawson(z) = sqrt(pi)/2 * exp(-z^2) * erfi(z)`.

Reference equations:
DLMF 7.2 for definitions and DLMF 7.4 for symmetry. Arb/python-flint error
function primitive documentation for backend behavior.

Known numerical risks:
Large positive real values of `erfc` can suffer cancellation when implemented
as `1 - erf(z)`. The certified backend therefore prefers direct Arb `erfc`
when available and only records the `1-erf` formula fallback explicitly.
`erfcx` is exposed as a scaled wrapper but this PR does not add custom
asymptotic certification or claim stability outside the selected backend
enclosure.

Certification status:
`certificate_level="direct_arb_primitive"`. Certified `erf` results use
`certificate_scope="direct_arb_erf"` and enclose direct Arb `erf` output.
Certified `erfc` results use `certificate_scope="direct_arb_erfc"` and enclose
direct Arb `erfc` output, or the explicit Arb `1 - erf(z)` fallback when
`formula="1-erf"` is present in diagnostics.
Certified `erfcx` results use `certificate_scope="direct_arb_erfcx"` with
`certificate_level="direct_arb_primitive"` if a direct Arb primitive is
available. The formula fallback uses `certificate_scope="arb_erfcx_formula"`,
`certificate_level="formula_audited_alpha"`, `audit_status="formula_identity"`,
`certification_claim="certified Arb enclosure of exp(z^2)*erfc(z)"`, and
`formula="exp(z^2)*erfc(z)"`.
Certified `erfi` results use `certificate_scope="direct_arb_erfi"` with
`certificate_level="direct_arb_primitive"` if a direct Arb primitive is
available. The formula fallback uses `certificate_scope="arb_erfi_formula"`,
`certificate_level="formula_audited_alpha"`, `audit_status="formula_identity"`,
`certification_claim="certified Arb enclosure of -i*erf(i*z)"`, and
`formula="-i*erf(i*z)"`.
Certified `dawson` results use `certificate_scope="direct_arb_dawson"` with
`certificate_level="direct_arb_primitive"` if a direct Arb primitive is
available. The formula fallback uses `certificate_scope="arb_dawson_formula"`,
`certificate_level="formula_audited_alpha"`, `audit_status="formula_identity"`,
`certification_claim="certified Arb enclosure of sqrt(pi)/2*exp(-z^2)*erfi(z)"`,
and `formula="sqrt(pi)/2*exp(-z^2)*erfi(z)"`.

Release hygiene:
`pypi-smoke.yml` defaults to `0.2.0a7` after the published
`v0.2.0-alpha.7` release. This Dawson feature branch intentionally does not
update the PyPI smoke workflow before a future release is published. The
existing smoke workflow covers `erf`, `erfc`, `erfcx`, and `erfi` in base and
certified Python API smoke calls, plus certified `special_erf`, `special_erfc`,
`special_erfcx`, and `special_erfi` calls in the MCP-certified smoke job. The
PyPI publish workflows continue to use
`actions/upload-artifact@v6` and `actions/download-artifact@v6`.

Current v0.2 audit result:
The Dawson feature branch adds `dawson(z)` as the only new public
error-function-family wrapper and keeps pypi-smoke pinned to `0.2.0a7` until a
future release is published. Tests keep the five wrappers, MCP parity, fixture
containment, and formula diagnostics in lockstep. No `erf`, `erfc`, `erfcx`,
`erfi`, gamma-family, or parabolic-cylinder behavior or claim changes are part
of this feature branch.
No public API, dispatcher, backend formula, MCP, or certified-scope
inconsistency was found after the Dawson surface and audit docs were updated.
