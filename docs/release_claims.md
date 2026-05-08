# Release Claim Guardrails

The 0.1.0 alpha line should make conservative certification claims. Release
copy, package metadata, README text, examples, and GitHub release notes must
help users distinguish three different things:

- plain numerical values from SciPy or mpmath;
- direct Arb primitive enclosures with alpha certification evidence; and
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
| Gamma family | alpha-certified, direct Arb gamma primitives |
| Airy family | alpha-certified, direct Arb primitive |
| Bessel family | alpha-certified where direct Arb primitive works; real-valued order only |
| Parabolic-cylinder family | experimental certified formula layer |
| MCP server | experimental tool interface |
| Custom Taylor/asymptotic methods | not yet |

## Wording Rules

- Say that direct Arb primitive families are alpha-certified only on documented
  finite-enclosure domains.
- Say that `gamma_ratio` is certified through the narrow
  `Gamma(a) * rgamma(b)` Arb product, with denominator-pole zeros and
  numerator-pole clean failures.
- Say that Bessel certified mode is restricted to real-valued order.
- Say that parabolic-cylinder certificates are experimental formula-layer
  certificates until the formula, branch, and domain audit issues are closed.
- Say that unsupported certified domains fail cleanly as non-certified results.
- Do not say "fully certified", "globally certified", "production-certified",
  or "certified for every continuation".
- Do not describe the parabolic-cylinder family as certified without the
  experimental formula-layer qualifier.
- Do not imply that MCP expands the mathematical support surface.

## Change Gate

Any release-facing claim change must update the relevant audit docs and keep
`tests/test_release_claims.py` passing. If a future audit broadens a claim, the
same change should update runtime diagnostics, support matrices, README wording,
and release notes together.
