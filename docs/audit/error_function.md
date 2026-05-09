# Error-Function Certification Audit

Function:
`erf(z)`, `erfc(z)`.

Public API:
`erf` and `erfc` are exported from `certsf.__init__`, listed in
`certsf.__all__`, registered in the dispatcher with `fast`, `high_precision`,
and `certified` modes, and exposed through thin MCP tools named `special_erf`
and `special_erfc`. No `erfi`, `erfinv`, `erfcinv`, or `erfcx` wrapper is part
of this audit scope.

Target mathematical definition:
`erf(z) = 2/sqrt(pi) * integral_0^z exp(-t^2) dt`.
`erfc(z) = 1 - erf(z)`.

Backend primitive or formula:
Direct Arb error-function primitives through python-flint: `arb/acb.erf` and
`arb/acb.erfc`. If a supported python-flint build exposes `erf` but not
`erfc`, the certified `erfc` path may use the audited Arb arithmetic expression
`1 - erf(z)` and records `formula="1-erf"`.

Accepted domain:
Real or complex inputs accepted by Arb for the corresponding error-function
primitive, when the requested target value has a finite Arb enclosure.

Excluded domain:
Non-finite input or output enclosures and any domain where Arb does not return a
finite enclosure. No custom asymptotic or Taylor certification path is included.

Branch convention:
The error function is entire. The certified wrappers follow Arb's complex
elementary-function conventions for the direct primitives.

Singularities:
No finite singularities for `erf` or `erfc`; failures are limited to unsupported
or non-finite Arb enclosure cases.

Validation identities:
Tests cover `erf(0) = 0`, `erfc(0) = 1`, regular real and complex samples,
`erf(-z) = -erf(z)`, and certified ball containment for
`erf(z) + erfc(z) = 1`.

Reference equations:
DLMF 7.2 for definitions and DLMF 7.4 for symmetry. Arb/python-flint error
function primitive documentation for backend behavior.

Known numerical risks:
Large positive real values of `erfc` can suffer cancellation when implemented
as `1 - erf(z)`. The certified backend therefore prefers direct Arb `erfc`
when available and only records the `1-erf` formula fallback explicitly.

Certification status:
`certificate_level="direct_arb_primitive"`. Certified `erf` results use
`certificate_scope="direct_arb_erf"` and enclose direct Arb `erf` output.
Certified `erfc` results use `certificate_scope="direct_arb_erfc"` and enclose
direct Arb `erfc` output, or the explicit Arb `1 - erf(z)` fallback when
`formula="1-erf"` is present in diagnostics.

Release hygiene:
`pypi-smoke.yml` defaults to `0.2.0a5` after the published
`v0.2.0-alpha.5` release and covers `erf` and `erfc` in base and certified
Python API smoke calls, plus `special_erf` and `special_erfc` in MCP-certified
smoke calls. The PyPI publish workflows continue to use
`actions/upload-artifact@v6` and `actions/download-artifact@v6`.
