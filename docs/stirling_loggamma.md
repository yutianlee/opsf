# Planned Stirling `loggamma` Method

This document records the target for the first custom certified asymptotic
method planned for v0.3.0. Method registry v2 infrastructure is present, but
the Stirling method itself is not implemented or claimed by the current
runtime.

## Target Formula

For positive real `x`, the planned method targets the Stirling expansion

```text
log Gamma(x)
  = (x - 1/2) log(x) - x + (1/2) log(2*pi)
    + sum_{k=1}^{m} B_{2k} / (2k(2k - 1) x^(2k - 1))
    + R_m(x),
```

where `B_{2k}` are Bernoulli numbers and `m` is the number of Bernoulli
correction terms selected by the method.

The implementation PR must document the positive-real remainder theorem used
for certification. The intended tail certificate is an absolute bound for
`R_m(x)` no larger than the first omitted Bernoulli correction term under that
theorem:

```text
tail_bound <= |B_{2m+2}| / ((2m + 2)(2m + 1) x^(2m + 1)).
```

## Intended Certificate Metadata

- intended domain: real `x >= 20`;
- intended `certificate_scope`: `stirling_loggamma_positive_real`;
- intended `certificate_level`: `custom_asymptotic_bound`;
- intended `audit_status`: `theorem_documented`.

The method should be selected only when the input is real and inside the
documented positive-real domain. Other certified paths may continue to use Arb
direct primitives as documented by the method registry.

Until the implementation PR lands, `method="stirling"` is a planned method id
that must fail clearly before returning any certified result.

## Required Diagnostics

Any certified result from this planned method must record:

- `terms_used`: the number of Bernoulli correction terms included;
- `tail_bound`: the rigorous bound applied to the omitted tail;
- `domain`: the accepted domain string for the selected theorem;
- `formula`: the Stirling formula identifier or formula summary;
- `selected_method`: the registry method name chosen for this evaluation.

These diagnostics are required so callers can distinguish this custom
asymptotic certificate from direct Arb primitive certificates and from
non-certified SciPy or mpmath values.

## Explicit Exclusions

The v0.3.0 planned method excludes:

- complex `z`;
- `x <= 0`;
- real `x < 20`;
- principal-branch complex `loggamma`;
- gamma-ratio asymptotics.

The exclusions are part of the certification scope. They should fail cleanly as
non-certified results or dispatch to another documented certified path when one
exists.
