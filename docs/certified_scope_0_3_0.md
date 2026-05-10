# Certified Scope for 0.3.0

This document records the v0.3.0 certified-scope direction. It keeps the
current 0.2.0 public wrapper list and adds active custom-certified-method rows
for explicit positive-real `loggamma` and explicit positive-real `gamma`.

The published 0.2.0 surface remains recorded in
[`certified_scope_0_2_0.md`](certified_scope_0_2_0.md). This document does not
broaden package-wide, gamma-family-wide, loggamma-wide, or
parabolic-cylinder certification claims.

## Release Status Matrix

| Area | Public wrappers or surface | Release status |
| --- | --- | --- |
| Gamma family | `gamma`, `loggamma`, `rgamma`, `gamma_ratio`, `loggamma_ratio`, `beta`, `pochhammer` | alpha-certified, direct Arb gamma primitives and finite products |
| Error-function family | `erf`, `erfc`, `erfcx`, `erfi`, `dawson`, `erfinv`, `erfcinv` | alpha-certified, direct Arb error-function primitives plus erfcx, erfi, and dawson identity formulas; real erfinv on (-1, 1); real erfcinv on (0, 2) |
| Airy family | `airy`, `ai`, `bi` | alpha-certified, direct Arb primitive |
| Bessel family | `besselj`, `bessely`, `besseli`, `besselk` | alpha-certified where direct Arb primitive works; real-valued order only |
| Parabolic-cylinder family | `pcfd`, `pcfu`, `pcfv`, `pcfw`, `pbdv` | experimental certified formula layer |
| MCP server | `certsf.mcp_server` tools for the current wrappers | experimental tool interface |
| Method registry v2 | existing Python wrappers with optional `method=...` selection | infrastructure active; default selection unchanged |
| Custom Taylor/asymptotic methods | `loggamma` positive-real Stirling asymptotic | alpha-certified custom asymptotic bound for positive-real loggamma via explicit `method="stirling"` or `method="stirling_shifted"`; explicit `method="certified_auto"` may select those methods or direct Arb; real `x >= 20` for custom methods; not automatic default selection |
| Custom gamma method | positive-real `gamma` via certified `loggamma` exponentiation | active explicit method `method="stirling_exp"` only; alpha-certified custom asymptotic bound for finite real `x >= 20`; no default dispatch change |

## Current Function List

The current public special-function wrappers remain the 0.2.0 list:

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
erfcx
erfi
dawson
erfinv
erfcinv
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

Compatibility aliases `airyai` and `airybi` remain aliases for `ai` and `bi`.
They are not additional certified functions.

## Custom Method Row

The active custom-certified row is limited to the existing `loggamma` wrapper:

- method family: Stirling/asymptotic expansion for positive real `x`;
- selector: explicit `mode="certified", method="stirling"` or
  `mode="certified", method="stirling_shifted"`;
- explicit selector: `mode="certified", method="certified_auto"` may select
  direct Arb or one of the positive-real Stirling methods, and is not used for
  `method=None` or `method="auto"`;
- domain: real `x >= 20`;
- certificate scope: `stirling_loggamma_positive_real`;
- certificate level: `custom_asymptotic_bound`;
- audit status: `theorem_documented`;
- runtime method field: `stirling_loggamma` or `stirling_shifted_loggamma`
  when a custom method is selected; `arb_ball` when the explicit selector
  chooses direct Arb;
- default status: not automatic default selection.

This row does not add a public wrapper, does not replace direct Arb primitive
certification, and does not claim support for complex `loggamma`, branch-cut
behavior, `x < 20`, `x <= 0`, or gamma-ratio asymptotics.

## Custom Gamma Method Row

The custom gamma row is active only for the existing `gamma` wrapper and the
explicit method:

- selector: explicit `mode="certified", method="stirling_exp"`;
- target: positive-real `gamma(x)`;
- domain: finite real `x >= 20`;
- reduction: obtain a certified positive-real `loggamma` enclosure, widen it
  by the explicit Stirling/loggamma tail bound, and exponentiate it using Arb
  ball arithmetic;
- certificate scope: `gamma_positive_real_stirling_exp`;
- certificate level: `custom_asymptotic_bound`;
- audit status: `theorem_documented`;
- runtime method field: `stirling_exp_gamma`;
- default status: not automatic default selection.

This active explicit method does not change direct Arb as the default
certified `gamma` path. It excludes complex `gamma`, real `x < 20`, real
`x <= 0`, reflection-formula paths, near-pole behavior, gamma-ratio
asymptotics, beta asymptotics, and parabolic-cylinder promotion.

## Scope Boundaries

- Default certified `loggamma` remains direct Arb.
- Default certified `gamma` remains direct Arb.
- `method="auto"` remains equivalent to the previous automatic selection path.
- Explicit `method="certified_auto"` is a selector only and does not change
  default dispatch.
- Parabolic-cylinder wrappers remain `experimental_formula`.
- No Faddeeva, `wofz`, or plasma-dispersion wrappers are included.
- No broad package-wide, family-wide, or all-input `loggamma` certification
  claim is made.
- MCP remains a thin experimental interface and does not expand the
  mathematical support surface.
- Unsupported certified domains must continue to fail cleanly as non-certified
  results.
