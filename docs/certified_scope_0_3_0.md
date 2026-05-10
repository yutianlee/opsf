# Certified Scope for 0.3.0

This document records the v0.3.0 certified-scope direction. It keeps the
current 0.2.0 public wrapper list and adds one active custom-certified-method
row for explicit positive-real `loggamma`.

The published 0.2.0 surface remains recorded in
[`certified_scope_0_2_0.md`](certified_scope_0_2_0.md). This document does not
broaden package-wide, loggamma-wide, or parabolic-cylinder certification claims.

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
| Custom Taylor/asymptotic methods | `loggamma` positive-real Stirling asymptotic | alpha-certified custom asymptotic bound for positive-real loggamma via explicit `method="stirling"`; real `x >= 20`; not automatic default selection |

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
- selector: explicit `mode="certified", method="stirling"`;
- domain: real `x >= 20`;
- certificate scope: `stirling_loggamma_positive_real`;
- certificate level: `custom_asymptotic_bound`;
- audit status: `theorem_documented`;
- runtime method field: `stirling_loggamma`;
- default status: not automatic default selection.

This row does not add a public wrapper, does not replace direct Arb primitive
certification, and does not claim support for complex `loggamma`, branch-cut
behavior, `x < 20`, `x <= 0`, or gamma-ratio asymptotics.

## Scope Boundaries

- Default certified `loggamma` remains direct Arb.
- `method="auto"` remains equivalent to the previous automatic selection path.
- Parabolic-cylinder wrappers remain `experimental_formula`.
- No Faddeeva, `wofz`, or plasma-dispersion wrappers are included.
- No broad package-wide, family-wide, or all-input `loggamma` certification
  claim is made.
- MCP remains a thin experimental interface and does not expand the
  mathematical support surface.
- Unsupported certified domains must continue to fail cleanly as non-certified
  results.
