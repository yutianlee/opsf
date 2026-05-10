# Positive-Real `gamma` via Stirling Loggamma Exponentiation

This document records the active explicit method for positive-real `gamma`.
It does not change default dispatch, does not add a public wrapper, and is not
automatic default selection. In other words: not automatic default selection.

The active explicit method is:

```python
gamma(x, mode="certified", method="stirling_exp", dps=...)
```

## Target

The target function is `gamma(x)` on finite real inputs with `x >= 20`.
Active domain: finite real `x >= 20`.

The reduction is:

```text
Gamma(x) = exp(log Gamma(x))
```

The implementation first uses the existing certified positive-real `loggamma`
machinery to obtain an Arb ball enclosure `L in log Gamma(x)`. The explicit
Stirling/loggamma tail bound is added to that Arb ball before exponentiation.
The method then computes `exp(L)` using Arb ball arithmetic and returns that
ball as the enclosure for `Gamma(x)`.

## Certificate Metadata

The certificate metadata is:

- `certificate_scope="gamma_positive_real_stirling_exp"`
- `certificate_level="custom_asymptotic_bound"`
- `audit_status="theorem_documented"`
- `selected_method="stirling_exp"`

The runtime result method is `stirling_exp_gamma`, and the backend is
`certsf+python-flint`.

## Error-Bound Contract

The `stirling_exp` method depends on the positive-real `loggamma` certificate.
A successful result must not discard either source of uncertainty:

- the Arb radius from evaluating the finite loggamma expression and
  exponentiation; and
- the explicit positive-real Stirling/loggamma tail bound propagated through
  exponentiation.

The returned gamma enclosure includes the finite-expression Arb radius and the
propagated loggamma-tail contribution because the loggamma ball is widened by
the explicit tail bound before `exp` is evaluated.

## Diagnostics

A successful result includes diagnostics equivalent to:

- `selected_method="stirling_exp"`
- `certificate_scope="gamma_positive_real_stirling_exp"`
- `certificate_level="custom_asymptotic_bound"`
- `audit_status="theorem_documented"`
- `formula="gamma=exp(loggamma)"`
- `domain="positive_real_x_ge_20"`
- `loggamma_method_used`
- `loggamma_abs_error_bound`
- `exp_radius`
- `propagated_error_bound`
- `fallback=[]`

Additional diagnostics may identify the underlying loggamma method, term count,
shift, shifted argument, coefficient source, and internal precision.

## Exclusions

The method excludes:

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

The method remains explicit. It does not change `method=None`,
`method="auto"`, or default certified `gamma` behavior. It does not broaden
package-wide, gamma-family-wide, gamma-ratio, beta, complex-gamma, or
parabolic-cylinder certification claims.
