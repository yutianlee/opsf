# Certified Scope for 0.3.0 Planning

This document records the v0.3.0 certified-scope direction. It copies the
current 0.2.0 support matrix and adds one planned custom-certified-method row.
Method registry v2 infrastructure is active, but the planned Stirling row is
not active until implementation, proof references, runtime diagnostics, and
tests land in a later PR.

The current 0.2.0 surface remains recorded in
[`certified_scope_0_2_0.md`](certified_scope_0_2_0.md). This document does not
broaden current certification claims.

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
| Custom Taylor/asymptotic methods | none | not yet |
| Custom certified methods | `loggamma` positive-real Stirling asymptotic | planned alpha scope only; not active until implementation lands |

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

## Planned Custom Method Row

The planned custom-certified row is limited to the existing `loggamma` wrapper:

- method family: Stirling/asymptotic expansion for positive real `x`;
- intended domain: real `x >= 20`;
- intended certificate scope:
  `stirling_loggamma_positive_real`;
- intended certificate level:
  `custom_asymptotic_bound`;
- intended audit status:
  `theorem_documented`;
- implementation status: planned only until the method implementation lands.

This row does not add a public wrapper, does not replace direct Arb primitive
certification, and does not claim support for complex `loggamma`, branch-cut
behavior, `x < 20`, `x <= 0`, or gamma-ratio asymptotics.

`method="stirling"` is a guarded planned method id only. It must not return a
certified result until the implementation lands.

## Scope Boundaries

- Parabolic-cylinder wrappers remain `experimental_formula`.
- No Faddeeva, `wofz`, or plasma-dispersion wrappers are planned for v0.3.0.
- No broad package-wide, family-wide, or global certification claim is made.
- Method registry v2 does not change default dispatch behavior for callers that
  omit `method` or pass `method="auto"`.
- MCP remains a thin experimental interface and does not expand the
  mathematical support surface.
- Unsupported certified domains must continue to fail cleanly as non-certified
  results.

## Change Gate

The implementation PR that activates the planned custom row must update runtime
diagnostics, method-registry coverage, support matrices, audit documentation,
and tests in the same change.
