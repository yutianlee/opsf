# Release Claim Guardrails

The 0.x alpha line should make conservative certification claims. Release
copy, package metadata, README text, examples, and GitHub release notes must
help users distinguish four different things:

- plain numerical values from SciPy or mpmath;
- direct Arb primitive enclosures with alpha certification evidence; and
- the narrow custom positive-real `loggamma` Stirling method with a documented
  asymptotic tail bound; and
- experimental formula-backed Arb enclosures with open formula audit work.

## Required Short Summary

Use this exact short summary for package metadata and citation metadata:

```text
Alpha special-function wrappers with explicit certification diagnostics.
```

This wording keeps the PyPI/TestPyPI summary from implying that every public
wrapper has a completed global mathematical audit.

## Required Release Status Wording

Release-facing support matrices must keep these status phrases:

| Surface | Required wording |
| --- | --- |
| Gamma family | alpha-certified, direct Arb gamma primitives and finite products |
| Error-function family | alpha-certified, direct Arb error-function primitives plus erfcx, erfi, and dawson identity formulas; real erfinv on (-1, 1); real erfcinv on (0, 2) |
| Airy family | alpha-certified, direct Arb primitive |
| Bessel family | alpha-certified where direct Arb primitive works; real-valued order only |
| Parabolic-cylinder family | experimental certified formula layer |
| MCP server | experimental tool interface |
| Custom Taylor/asymptotic methods | alpha-certified custom asymptotic bound for positive-real loggamma via explicit `method="stirling"`; real `x >= 20`; not automatic default selection |

## Wording Rules

- Say that direct Arb primitive families are alpha-certified only on documented
  finite-enclosure domains.
- Say that `gamma_ratio` is certified through the narrow
  `Gamma(a) * rgamma(b)` Arb product, with denominator-pole zeros and
  numerator-pole clean failures.
- Say that `loggamma_ratio` is certified through the narrow principal
  `loggamma(a) - loggamma(b)` Arb difference, with clean failures for poles in
  either argument.
- Say that `beta` is certified through the narrow
  `Gamma(a) * Gamma(b) * rgamma(a+b)` Arb product, with `Gamma(a+b)` pole zeros
  only when both numerator gamma factors are finite and clean failures for
  numerator poles or simultaneous singularities.
- Say that `pochhammer` is certified only through the finite product for
  integer `n >= 0`, with no analytic continuation in `n` and no simultaneous
  pole-limit claim.
- Say that explicit `loggamma(x, mode="certified", method="stirling")` is an
  alpha-certified custom asymptotic bound only for real `x >= 20`, and that it
  is not automatic default selection.
- Do not claim complex `loggamma` branch certification, real `x < 20`,
  `x <= 0`, or gamma-ratio asymptotics for the Stirling method.
- Say that `erf` and `erfc` are certified only where Arb returns finite
  enclosures; direct Arb `erfc` is preferred, and any allowed `1 - erf`
  fallback must be visible in diagnostics.
- Say that `erfcx` is defined as `exp(z^2) erfc(z)`; direct Arb `erfcx` is
  preferred when available, and any allowed `exp(z^2)*erfc(z)` fallback must be
  visible in diagnostics.
- Say that `erfi` is defined as `-i erf(i z)`; direct Arb `erfi` is preferred
  when available, and any allowed `-i*erf(i*z)` fallback must be visible in
  diagnostics.
- Say that `dawson` is defined as `sqrt(pi)/2 * exp(-z^2) * erfi(z)`; direct Arb `dawson` is preferred when
  available, and any allowed `sqrt(pi)/2*exp(-z^2)*erfi(z)` fallback must be
  visible in diagnostics.
- Say that `erfinv` is only the real principal inverse on `-1 < x < 1`;
  direct Arb `erfinv` is preferred when available, and any allowed
  `erf(y)-x=0` real-root fallback must be visible in diagnostics.
- Say that `erfcinv` is only the real principal inverse on `0 < x < 2`;
  direct Arb `erfcinv` is preferred when available, and any allowed
  `erfinv(1-x)` fallback must be visible in diagnostics.
- Do not claim scaled-erfc stability for large arguments beyond what the
  selected backend certifies.
- Do not claim Faddeeva, plasma dispersion, `wofz`, or other error-function
  variant support until those wrappers, backends, tests, and audit docs exist.
- Do not claim complex inverse branches or endpoint asymptotic certification for `erfinv`.
- Do not claim complex inverse branches or endpoint asymptotic certification for `erfcinv`.
- Do not claim Taylor or asymptotic certification methods for the
  error-function family.
- Do not imply that complex `loggamma_ratio` is the principal logarithm of
  `gamma_ratio` or that it certifies pole-limiting values.
- Say that Bessel certified mode is restricted to real-valued order.
- Say that parabolic-cylinder certificates are experimental formula-layer
  certificates until the formula, branch, and domain audit issues are closed.
- Say that unsupported certified domains fail cleanly as non-certified results.
- Do not say "fully certified", "globally certified", "production-certified",
  or "certified for every continuation".
- Do not say "fully certified loggamma", "global loggamma certification", or
  "complete certified special functions".
- Do not say "complex Stirling certification", "complete certified asymptotic
  support", "automatic Stirling default", or "certified gamma-ratio
  asymptotics".
- Do not describe the parabolic-cylinder family as certified without the
  experimental formula-layer qualifier.
- Do not imply that MCP expands the mathematical support surface.

## Change Gate

Any release-facing claim change must update the relevant audit docs and keep
`tests/test_release_claims.py` passing. If a future audit broadens a claim, the
same change should update runtime diagnostics, support matrices, README wording,
and release notes together.
