# Certified Scope for 0.1.0

This document freezes the public certified surface planned for the 0.1.0 alpha
line. Do not add more public special-function wrappers before 0.1.0; validation,
audit, packaging, and release discipline take priority over expanding the API.

## Release Status Matrix

| Area | Public wrappers or surface | Release status |
| --- | --- | --- |
| Gamma family | `gamma`, `loggamma`, `rgamma` | alpha-certified, direct Arb primitive |
| Airy family | `airy`, `ai`, `bi` | alpha-certified, direct Arb primitive |
| Bessel family | `besselj`, `bessely`, `besseli`, `besselk` | alpha-certified where direct Arb primitive works; real-valued order only |
| Parabolic-cylinder family | `pcfd`, `pcfu`, `pcfv`, `pcfw`, `pbdv` | experimental certified formula layer |
| MCP server | `certsf.mcp_server` tools for the frozen wrappers | experimental tool interface |
| Custom Taylor/asymptotic methods | none | not yet |

## Frozen Function List

The frozen public special-function wrappers are:

```text
gamma
loggamma
rgamma
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

- Direct Arb primitive families are alpha-certified only on the domains where
  Arb returns finite enclosures and the wrapper records the documented
  certificate scope.
- Bessel certified claims remain restricted to real-valued order. Complex order
  must fail cleanly as a non-certified result.
- The parabolic-cylinder family remains an experimental certified formula layer:
  Arb encloses the implemented documented formula, but formula/domain audit work
  remains visible before broadening claims.
- MCP is a thin experimental interface over the Python API. It does not expand
  the mathematical support surface.
- Custom Taylor, asymptotic, or non-Arb certification methods are outside the
  0.1.0 scope.

## Change Gate

Any change to this frozen scope before 0.1.0 must update this document,
[`certification.md`](certification.md), the README support wording, MCP wrapper
coverage, and the public contract tests in the same PR.
