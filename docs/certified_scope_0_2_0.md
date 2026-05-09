# Certified Scope for 0.2.0 Alpha

This document records the current public certified surface for the 0.2.0 alpha
line. The 0.1.0 surface remains frozen in
[`certified_scope_0_1_0.md`](certified_scope_0_1_0.md). The gamma-family
additions are `gamma_ratio(a, b)`, `loggamma_ratio(a, b)`, `beta(a, b)`, and
`pochhammer(a, n)`. The v0.2.0-alpha.5 feature branch adds `erf(z)` and
`erfc(z)`.

## Release Status Matrix

| Area | Public wrappers or surface | Release status |
| --- | --- | --- |
| Gamma family | `gamma`, `loggamma`, `rgamma`, `gamma_ratio`, `loggamma_ratio`, `beta`, `pochhammer` | alpha-certified, direct Arb gamma primitives and finite products |
| Error-function family | `erf`, `erfc` | alpha-certified, direct Arb error-function primitives |
| Airy family | `airy`, `ai`, `bi` | alpha-certified, direct Arb primitive |
| Bessel family | `besselj`, `bessely`, `besseli`, `besselk` | alpha-certified where direct Arb primitive works; real-valued order only |
| Parabolic-cylinder family | `pcfd`, `pcfu`, `pcfv`, `pcfw`, `pbdv` | experimental certified formula layer |
| MCP server | `certsf.mcp_server` tools for the current wrappers | experimental tool interface |
| Custom Taylor/asymptotic methods | none | not yet |

## Current Function List

The current public special-function wrappers are:

```text
gamma
loggamma
rgamma
gamma_ratio
loggamma_ratio
beta
pochhammer
erf
erfc
airy
ai
bi
besselj
bessely
besseli
besselk
pcfd
pcfu
pcfv
pcfw
pbdv
```

Compatibility aliases `airyai` and `airybi` remain exported, but they are aliases
for `ai` and `bi`, not additional certified functions.

## Boundary Notes

- `gamma_ratio(a, b)` is the only 0.2.0-alpha.1 API expansion.
- `loggamma_ratio(a, b)` is the v0.2.0-alpha.2 API expansion.
- `beta(a, b)` is the v0.2.0-alpha.3 API expansion.
- `pochhammer(a, n)` is the v0.2.0-alpha.4 API expansion.
- `erf(z)` and `erfc(z)` are the v0.2.0-alpha.5 feature-branch API expansion.
- Certified `gamma_ratio` uses Arb `Gamma(a) * rgamma(b)`, not direct division
  by `Gamma(b)`.
- Denominator gamma poles certify to zero when `Gamma(a)` is finite.
- Numerator poles and simultaneous numerator/denominator poles are clean
  non-certified failures with pole diagnostics.
- Certified `loggamma_ratio` uses Arb `lgamma(a) - lgamma(b)` with principal
  `loggamma` branches and `certificate_scope="direct_arb_loggamma_ratio"`.
- `loggamma_ratio` does not claim the principal logarithm of `gamma_ratio` for
  complex inputs and does not certify pole-limiting values.
- Certified `beta` uses Arb `Gamma(a) * Gamma(b) * rgamma(a+b)`, not direct
  division by `Gamma(a+b)`.
- Certified `beta` returns clean non-certified failures when `Gamma(a)` or
  `Gamma(b)` has a pole, and does not claim limiting values at simultaneous
  singularities.
- Certified `pochhammer` uses the finite product
  `product_{k=0}^{n-1} (a+k)` for integer `n >= 0`.
- Certified `pochhammer` returns `1` for `n = 0`, certifies exact zero factors
  to zero, rejects non-integer or negative `n`, and does not claim analytic
  continuation in `n` or simultaneous-pole limiting values.
- Certified `erf` and `erfc` use direct Arb error-function primitives where
  available, support real or complex inputs when Arb returns finite enclosures,
  and do not add custom asymptotic certification.
- If direct Arb `erfc` is unavailable but direct Arb `erf` is available,
  certified `erfc` may use `1 - erf(z)` and must record `formula="1-erf"`.
- Direct Arb primitive families are alpha-certified only on the domains where
  Arb returns finite enclosures and the wrapper records the documented
  certificate scope.
- Bessel certified claims remain restricted to real-valued order. Complex order
  must fail cleanly as a non-certified result.
- The parabolic-cylinder family remains an experimental certified formula layer:
  Arb encloses the implemented documented formula, but formula/domain audit work
  remains visible before broadening claims.
- Certified `pbdv(v, x)` keeps SciPy's real-variable argument name, but the
  certified formula layer accepts complex arguments for the value and derivative
  pair. Use `pcfd(v, z)` when only the complex `D_v(z)` value is needed.
- MCP is a thin experimental interface over the Python API. It does not expand
  the mathematical support surface.
- Custom Taylor, asymptotic, or non-Arb certification methods are outside the
  0.2.0 alpha scope.

## Change Gate

Any change to this scope before 0.2.0 final must update this document,
[`certification.md`](certification.md), the README support wording, MCP wrapper
coverage, and the public contract tests in the same PR.
