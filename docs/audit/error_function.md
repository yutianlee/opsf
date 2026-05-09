# Error-Function Certification Audit

Last reviewed: 2026-05-10.

Function:
`erf(z)`, `erfc(z)`, `erfcx(z)`, `erfi(z)`, `dawson(z)`, `erfinv(x)`,
`erfcinv(x)`.

Public API:
`erf`, `erfc`, `erfcx`, `erfi`, `dawson`, `erfinv`, and `erfcinv` are exported
from `certsf.__init__`, listed in `certsf.__all__`, registered in the
dispatcher with `fast`, `high_precision`, and `certified` modes, and exposed
through thin MCP tools named `special_erf`, `special_erfc`, `special_erfcx`,
`special_erfi`, `special_dawson`, `special_erfinv`, and `special_erfcinv`. No
additional inverse-error wrapper, Faddeeva wrapper, plasma dispersion wrapper,
or `wofz` wrapper is part of this audit scope.

Target mathematical definition:
`erf(z) = 2/sqrt(pi) * integral_0^z exp(-t^2) dt`.
`erfc(z) = 1 - erf(z)`.
`erfcx(z) = exp(z^2) erfc(z)`.
`erfi(z) = -i erf(i z)`.
`dawson(z) = sqrt(pi)/2 * exp(-z^2) * erfi(z)`.
`erfinv(x)` is the real principal inverse satisfying `erf(erfinv(x)) = x` for
real `-1 < x < 1`.
`erfcinv(x)` is the real principal inverse satisfying `erfc(erfcinv(x)) = x`
for real `0 < x < 2`, with `erfcinv(x) = erfinv(1-x)`.

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
For `erfinv`, the certified path supports only real `x` with `-1 < x < 1`.
It prefers direct Arb `erfinv` when available. Otherwise it brackets the unique
real root of `erf(y)-x=0`, uses monotonicity of real `erf`, and records
`formula="erf(y)-x=0"`.
For `erfcinv`, the certified path supports only real `x` with `0 < x < 2`.
It prefers direct Arb `erfcinv` when available. Otherwise it uses the certified
real-inverse path for `erfinv(1-x)` and records `formula="erfinv(1-x)"`.

Accepted domain:
For `erf`, `erfc`, `erfcx`, `erfi`, and `dawson`, real or complex inputs
accepted by Arb for the corresponding error-function primitive or identity
formula, when the requested target value has a finite Arb enclosure. For
`erfinv`, real `x` only with `-1 < x < 1`. For `erfcinv`, real `x` only with
`0 < x < 2`.

Excluded domain:
Non-finite input or output enclosures and any domain where Arb does not return a
finite enclosure. Certified `erfinv` also excludes `x <= -1`, `x >= 1`,
complex inverse branches, and endpoint asymptotic certification. Certified
`erfcinv` excludes `x <= 0`, `x >= 2`, complex inverse branches, endpoint
asymptotic certification, Faddeeva, plasma dispersion, and `wofz`. No custom
asymptotic or Taylor certification path is included, and no large-argument
scaled-erfc stability claim is made beyond backend certification of the
selected expression.
No custom asymptotic or Taylor certification path is added for the
error-function family.

Branch convention:
The direct and formula error-function entries here are entire. The certified
wrappers follow Arb's complex elementary-function conventions for the direct
primitives and the `exp(z^2)*erfc(z)`, `-i*erf(i*z)`, and
`sqrt(pi)/2*exp(-z^2)*erfi(z)` formulas. Certified `erfinv` uses only the real
principal inverse branch on `(-1, 1)`. Certified `erfcinv` uses only the real
principal inverse branch on `(0, 2)`.

Singularities:
No finite singularities for `erf`, `erfc`, `erfcx`, `erfi`, or `dawson`;
failures are limited to unsupported or non-finite Arb enclosure cases.
Certified `erfinv` has excluded endpoints at `x = -1` and `x = 1`; this audit
does not certify endpoint asymptotics.
Certified `erfcinv` has excluded endpoints at `x = 0` and `x = 2`; this audit
does not certify endpoint asymptotics.

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
`erfinv` tests cover `erfinv(0) = 0`, real composition with `erf`, oddness,
positive and negative near-endpoint samples, external-reference containment,
endpoint and out-of-interval rejection, complex rejection, auto dispatch, MCP
parity, forced real-root fallback diagnostics, and certified residual
containment for `erf(erfinv(x))-x = 0`.
`erfcinv` tests cover `erfcinv(1) = 0`, real composition with `erfc`, the
relation `erfcinv(x) = erfinv(1-x)`, monotonic orientation, near-endpoint
samples, external-reference containment, endpoint and out-of-interval
rejection, complex rejection, auto dispatch, MCP parity, forced fallback
diagnostics, and certified residual containment for `erfc(erfcinv(x))-x = 0`.

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
`erfinv` is restricted to real `x in (-1, 1)`. Values near endpoints can have
large derivative amplification; this PR does not add endpoint asymptotic
certification.
`erfcinv` is restricted to real `x in (0, 2)`. Values near endpoints can have
large derivative amplification; this PR does not add endpoint asymptotic
certification.

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
Certified `erfinv` results use `certificate_scope="direct_arb_erfinv"` with
`certificate_level="direct_arb_primitive"` if a direct Arb primitive is
available. The real-root fallback uses
`certificate_scope="arb_erfinv_real_root"`,
`certificate_level="certified_real_root"`,
`audit_status="monotone_real_inverse"`,
`certification_claim="certified real root enclosure for erf(y)-x=0 using monotonicity of real erf"`,
`domain="real_x_in_open_interval_minus1_1"`, and `formula="erf(y)-x=0"`.
Certified `erfcinv` results use `certificate_scope="direct_arb_erfcinv"` with
`certificate_level="direct_arb_primitive"` if a direct Arb primitive is
available. The fallback uses `certificate_scope="arb_erfcinv_via_erfinv"`,
`certificate_level="certified_real_root"`,
`audit_status="monotone_real_inverse"`,
`certification_claim="certified real inverse enclosure for erfcinv(x)=erfinv(1-x) using monotonicity of real erfc"`,
`domain="real_x_in_open_interval_0_2"`, and `formula="erfinv(1-x)"`.

Release hygiene:
`pypi-smoke.yml` defaults to `0.2.0a10` after the published
`v0.2.0-alpha.10` release. The smoke workflow covers `erf`, `erfc`,
`erfcinv`, `erfcx`, `erfi`, `erfinv`, and `dawson` in base and certified
Python API smoke calls, plus certified `special_erf`, `special_erfc`,
`special_erfcinv`, `special_erfcx`, `special_erfi`, `special_erfinv`, and
`special_dawson` calls in the MCP-certified smoke job. The PyPI publish
workflows continue to use
`actions/upload-artifact@v6` and `actions/download-artifact@v6`.

Audit evidence:
This audit found no implementation inconsistency in the seven-wrapper
error-function surface. The Python API, dispatcher registry, certified method
scopes, MCP thin wrappers, external-reference fixtures, identity tests, and
formula-diagnostics tests are in lockstep. The audit also checked that
Faddeeva, plasma dispersion, and `wofz` wrappers are not exported, registered,
or exposed as MCP tools.

Release infrastructure remains version-stable: this audit keeps the package
version fixed, keeps `pypi-smoke.yml` on the published `0.2.0a10` default,
keeps upload/download artifact actions on v6, and leaves the TestPyPI policy
wording unchanged. Routine feature alphas may still skip TestPyPI under
`docs/release_policy.md` when the documented release-policy conditions are met.

Current v0.2 audit result:
The published `v0.2.0-alpha.10` feature surface includes `erfcinv(x)` as one
new public error-function-family wrapper after `v0.2.0-alpha.9`. It keeps
inverse scope to real principal branches: `erfinv` on `-1 < x < 1` and
`erfcinv` on `0 < x < 2`. It does not add complex inverse branches, endpoint
asymptotic certification, Faddeeva, plasma dispersion, or `wofz`. Tests keep
the seven wrappers, MCP parity, fixture containment, formula diagnostics, and
real inverse-root diagnostics in lockstep. No `erfinv`, `erfcinv`, `erf`,
`erfc`, `erfcx`, `erfi`, `dawson`, gamma-family, or parabolic-cylinder behavior
or claim changes are part of this audit update.
No public API, dispatcher, backend formula, MCP, or certified-scope
inconsistency was found after the erfcinv surface and audit docs were updated.
