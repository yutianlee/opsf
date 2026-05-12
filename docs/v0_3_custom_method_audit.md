# v0.3 Custom-Method Audit

This audit records the active custom methods in the 0.3 line after
`v0.3.0-alpha.4`. These methods are explicit certified-mode choices for
existing public wrappers. They do not add public wrappers, do not change
default dispatch, and do not broaden package-wide certification claims.

Default certified `loggamma` and default certified `gamma` remain direct Arb
primitive paths. Calls that omit `method=...` or pass `method="auto"` continue
to use the existing default dispatch.

## Summary Matrix

| Function | Explicit method | Domain | Certificate scope | Default dispatch |
| --- | --- | --- | --- | --- |
| `loggamma` | `method="stirling"` | finite real `x >= 20` | `stirling_loggamma_positive_real` | no |
| `loggamma` | `method="stirling_shifted"` | finite real `x >= 20` | `stirling_loggamma_positive_real` | no |
| `loggamma` | `method="certified_auto"` | selector over direct Arb and positive-real Stirling methods | selected method's scope | no |
| `gamma` | `method="stirling_exp"` | finite real `x >= 20` | `gamma_positive_real_stirling_exp` | no |

## Future Work: Planned `rgamma(method="stirling_recip")`

The planned positive-real `rgamma` method is future work only. It is not active,
is not registered, and must not be included in the active summary matrix until
an implementation PR lands with proof, tests, diagnostics, and release wording.

The active 0.3 custom methods remain the four currently active paths:
`loggamma(method="stirling")`, `loggamma(method="stirling_shifted")`,
`loggamma(method="certified_auto")`, and `gamma(method="stirling_exp")`.

The planned future call shape is
`rgamma(x, mode="certified", method="stirling_recip", dps=...)` for finite
real `x >= 20`, with the planned reduction `rgamma(x) = exp(-loggamma(x))`,
planned certificate scope `rgamma_positive_real_stirling_recip`, planned
certificate level `custom_asymptotic_bound`, planned audit status
`theorem_documented`, and planned runtime method `stirling_recip_rgamma`.

This future work excludes complex `rgamma`, real `x < 20`, real `x <= 0`,
non-finite input, reflection-formula paths, near-pole behavior, gamma-ratio
asymptotics, beta asymptotics, parabolic-cylinder promotion, and default
dispatch changes.

## `loggamma(method="stirling")`

- Function: `loggamma`.
- Call shape: `loggamma(x, mode="certified", method="stirling", dps=...)`.
- Domain: finite real `x >= 20`.
- Runtime method: `stirling_loggamma`.
- Certificate scope: `certificate_scope="stirling_loggamma_positive_real"`.
- Certificate level: `certificate_level="custom_asymptotic_bound"`.
- Audit status: `audit_status="theorem_documented"`.
- Default dispatch: no.

This method evaluates the documented positive-real Stirling expansion with Arb
ball arithmetic for the finite expression and adds the explicit theorem-backed
first-omitted-term tail bound.

Exclusions: complex `loggamma`, principal-branch complex Stirling, real
`x < 20`, real `x <= 0`, non-finite input, gamma-ratio asymptotics, beta
asymptotics, and default method selection.

## `loggamma(method="stirling_shifted")`

- Function: `loggamma`.
- Call shape:
  `loggamma(x, mode="certified", method="stirling_shifted", dps=...)`.
- Domain: finite real `x >= 20`.
- Runtime method: `stirling_shifted_loggamma`.
- Certificate scope: `certificate_scope="stirling_loggamma_positive_real"`.
- Certificate level: `certificate_level="custom_asymptotic_bound"`.
- Audit status: `audit_status="theorem_documented"`.
- Default dispatch: no.

This method applies a positive-real recurrence shift, evaluates the same
Stirling expansion at the shifted argument, and subtracts Arb logs of the
recurrence factors. The shifted recurrence does not change the mathematical
scope: it is still only a finite positive-real `loggamma` method for
`x >= 20`.

Expected diagnostics include:

- `shift`
- `shifted_argument`
- `shift_policy`
- `guard_digits`
- `effective_dps`
- `coefficient_source`
- `largest_bernoulli_used`
- `tail_bound`

Exclusions: complex `loggamma`, principal-branch complex Stirling, real
`x < 20`, real `x <= 0`, non-finite input, gamma-ratio asymptotics, beta
asymptotics, and default method selection.

## `loggamma(method="certified_auto")`

- Function: `loggamma`.
- Call shape:
  `loggamma(x, mode="certified", method="certified_auto", dps=...)`.
- Domain: explicit selector only; it may select direct Arb, `stirling`, or
  `stirling_shifted` when those methods are applicable and certify.
- Certificate scope: the selected method's certificate scope is preserved.
- Certificate level: the selected method's certificate level is preserved.
- Audit status: the selected method's audit status is preserved.
- Default dispatch: no.

This selector does not introduce a new mathematical certificate. It chooses
between already documented certified paths, including direct Arb for
unsupported positive-real Stirling domains. It is not used for omitted-method
calls or for `method="auto"`.

Expected selector diagnostics include:

- `auto_selector`
- `auto_selected_method`
- `auto_reason`
- `auto_candidates`
- `preselected`
- `can_certify`
- `estimated_terms_used`

Exclusions: complex-domain Stirling coverage, package-wide `loggamma` custom
coverage, real `x < 20` custom Stirling coverage, real `x <= 0` custom
Stirling coverage, gamma-ratio asymptotics, beta asymptotics, and default
method selection.

## `gamma(method="stirling_exp")`

- Function: `gamma`.
- Call shape: `gamma(x, mode="certified", method="stirling_exp", dps=...)`.
- Domain: finite real `x >= 20`.
- Runtime method: `stirling_exp_gamma`.
- Certificate scope: `certificate_scope="gamma_positive_real_stirling_exp"`.
- Certificate level: `certificate_level="custom_asymptotic_bound"`.
- Audit status: `audit_status="theorem_documented"`.
- Default dispatch: no.

This method obtains a certified positive-real `loggamma` Arb enclosure, widens
that enclosure by the explicit loggamma tail bound, and evaluates Arb `exp` on
the widened ball. Successful diagnostics identify `formula="gamma=exp(loggamma)"`
and expose the underlying `loggamma_method_used`.

Expected diagnostics include:

- `selected_method="stirling_exp"`
- `loggamma_method_used`
- `loggamma_abs_error_bound`
- `exp_radius`
- `propagated_error_bound`

Exclusions: complex `gamma`, complex `gamma` via Stirling, reflection formula
certification, near-pole certification, real `x < 20`, real `x <= 0`,
non-finite input, gamma-ratio asymptotics, beta asymptotics, and default
`gamma` method selection.

## Release-Claim Boundaries

The 0.3 custom methods are narrow alpha-certified custom asymptotic-bound
paths. They do not imply package-wide certification for `loggamma` or `gamma`,
complex-domain Stirling certificates, a complex `gamma` Stirling certificate,
reflection formula certification, gamma-ratio asymptotic certification, beta
asymptotic certification, complete asymptotic coverage, or broader
parabolic-cylinder status.

Parabolic-cylinder wrappers remain `experimental_formula`.
