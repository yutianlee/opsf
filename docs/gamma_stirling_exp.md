# Planned Positive-Real `gamma` via Stirling Loggamma Exponentiation

This document is a planning note only. It does not activate a runtime method,
does not register a new method, and does not change default dispatch.

The proposed future method is:

```python
gamma(x, mode="certified", method="stirling_exp", dps=...)
```

## Target

The target function is `gamma(x)` on finite real inputs with `x >= 20`.
Planned domain: real `x >= 20`.

The planned reduction is:

```text
Gamma(x) = exp(log Gamma(x))
```

The future implementation would first use the existing certified
positive-real `loggamma` machinery to obtain a rigorous enclosure
`L in log Gamma(x)`. It would then use Arb ball arithmetic to return
`exp(L)` as an enclosure for `Gamma(x)`.

## Planned Certificate Metadata

The planned certificate metadata is:

- `certificate_scope="gamma_positive_real_stirling_exp"`
- `certificate_level="custom_asymptotic_bound"`
- `audit_status="theorem_documented"`
- `selected_method="stirling_exp"`

This scope is planned only and is not active until an implementation, tests,
and audit updates land in a later runtime PR.

## Planned Error-Bound Contract

The future `stirling_exp` method must depend on the existing positive-real
`loggamma` certificate. A successful result must not discard either source of
uncertainty:

- the Arb radius from evaluating the finite expression and exponentiation; and
- the explicit positive-real Stirling/loggamma tail bound propagated through
  exponentiation.

The returned gamma enclosure must include the finite-expression Arb radius and
the propagated loggamma-tail contribution. The implementation PR must document
the exact propagation formula and test containment against a higher-precision
direct Arb reference.

## Planned Diagnostics

A successful future result should include diagnostics equivalent to:

- `selected_method="stirling_exp"`
- `certificate_scope="gamma_positive_real_stirling_exp"`
- `certificate_level="custom_asymptotic_bound"`
- `audit_status="theorem_documented"`
- `loggamma_method_used`
- `loggamma_abs_error_bound`
- `exp_radius`
- `propagated_error_bound`
- `fallback=[]`

Additional implementation diagnostics may be added if they clarify the
underlying loggamma method, internal precision, or enclosure construction.

## Exclusions

The planned method excludes:

- real `x < 20`;
- real `x <= 0`;
- non-finite input;
- complex `gamma`;
- reflection-formula paths;
- near-pole behavior;
- gamma-ratio asymptotics;
- beta asymptotics; and
- default dispatch.

No complex gamma path is in scope. No reflection formula path is in scope.
No gamma-ratio asymptotics are in scope. Parabolic-cylinder wrappers remain
`experimental_formula`.

The method must remain explicit. It must not change `method=None`,
`method="auto"`, or default certified `gamma` behavior. It must not broaden
package-wide, gamma-family-wide, gamma-ratio, beta, complex-gamma, or
parabolic-cylinder certification claims.
