# Explicit Stirling `loggamma` Method

This document records the first custom certified asymptotic method in `certsf`.
The method is selected only by:

```python
loggamma(x, mode="certified", method="stirling", dps=...)
```

Default certified `loggamma` remains the direct Arb primitive path. The
Stirling method is not automatic default selection.
Parabolic-cylinder wrappers remain an `experimental_formula` surface; this
method does not promote that family.

## Formula

For positive real `x`, the method uses the Stirling expansion

```text
log Gamma(x)
  = (x - 1/2) log(x) - x + (1/2) log(2*pi)
    + sum_{k=1}^{m} B_{2k} / (2k(2k - 1) x^(2k - 1))
    + R_m(x),
```

where `B_{2k}` are Bernoulli numbers and `m` is the number of Bernoulli
correction terms selected by the method.

On the documented positive-real domain, the runtime uses the tail certificate

```text
|R_m(x)| <= |B_{2m+2}| / ((2m + 2)(2m + 1) x^(2m + 1)).
```

The finite Stirling sum is evaluated with Arb ball arithmetic through
`python-flint`; the returned absolute error bound includes both the Arb radius
of that finite sum and the explicit asymptotic tail bound.

## Certificate Metadata

- domain: real `x >= 20`;
- `certificate_scope`: `stirling_loggamma_positive_real`;
- `certificate_level`: `custom_asymptotic_bound`;
- `audit_status`: `theorem_documented`;
- `certification_claim`: `certified positive-real Stirling loggamma enclosure with explicit asymptotic tail bound`.

## Required Diagnostics

Certified Stirling results record:

- `terms_used`: the number of Bernoulli correction terms included;
- `tail_bound`: the rigorous bound applied to the omitted tail;
- `domain`: `positive_real_x_ge_20`;
- `formula`: `stirling_loggamma`;
- `selected_method`: `stirling`;
- `working_precision_bits`: the Arb precision used internally;
- `fallback`: an empty fallback record.

These diagnostics distinguish the custom asymptotic certificate from direct
Arb primitive certificates and from non-certified SciPy or mpmath values.

## Explicit Exclusions

This method excludes:

- complex `z`;
- `x <= 0`;
- real `x < 20`;
- non-finite input;
- principal-branch complex `loggamma`;
- gamma-ratio asymptotics.

The exclusions are part of the certification scope. Unsupported inputs fail
cleanly as non-certified results or are rejected by dispatcher method
selection; explicit `method="stirling"` never silently falls back to Arb or
mpmath.
