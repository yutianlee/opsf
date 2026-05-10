# Explicit Stirling `loggamma` Method

This document records the first custom certified asymptotic method in `certsf`.
The method is selected only by:

```python
loggamma(x, mode="certified", method="stirling", dps=...)
loggamma(x, mode="certified", method="stirling_shifted", dps=...)
loggamma(x, mode="certified", method="certified_auto", dps=...)
```

Default certified `loggamma` remains the direct Arb primitive path. The
Stirling methods are not automatic default selection. The explicit
`method="certified_auto"` selector may choose direct Arb or a positive-real
Stirling method, but it is not used for `method=None` or `method="auto"`.
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

## Shifted Method

`method="stirling_shifted"` uses the recurrence

```text
loggamma(x) = loggamma(x + r) - sum_{j=0}^{r-1} log(x + j)
```

with `y = x + r`. The shifted method evaluates all logarithms and the finite
Stirling sum with Arb ball arithmetic. The explicit tail bound is computed at
the shifted positive-real argument `y`, and the returned absolute error bound
includes the Arb radius of the complete finite expression plus that explicit
tail bound.

The shifted method uses `GUARD_DIGITS = 2`, so
`effective_dps = requested_dps + 2` and
`target_tolerance = 10**(-effective_dps)`. For real `x >= 20`, the shift policy
is:

- `effective_dps < 56`: `r = 0`, `shift_policy="direct_no_shift"`;
- `effective_dps <= 102`: if `x <= 37`, `r = floor(38 - x)`, otherwise
  `r = 0`, with `shift_policy="window_37_38"`;
- otherwise: choose the minimal integer `r >= 0` such that the Stirling tail at
  `y = x + r` can reach the target tolerance within the method term cap, with
  `shift_policy="minimal_shift"`.

The shifted method does not change `method="stirling"` and is not used for
`method=None` or `method="auto"`.

## Explicit Certified Selector

`method="certified_auto"` is an explicit certified-mode selector. For inputs
outside the positive-real Stirling scope, including complex values,
non-finite values, and real `x < 20`, it selects the direct Arb `loggamma`
primitive rather than a custom Stirling method. For finite real `x >= 20`, it
may select `method="stirling"` or `method="stirling_shifted"` only when the
selected method certifies its documented tail bound; otherwise it selects
direct Arb. The selector never falls back to mpmath in certified mode and does
not add complex Stirling, gamma-ratio asymptotics, or beta asymptotics.

Successful selected results preserve the selected backend's result method:
`arb_ball`, `stirling_loggamma`, or `stirling_shifted_loggamma`.

## Remainder Theorem Used

The theorem used here is only the positive-real Stirling remainder theorem for
`log Gamma(x)`. When `x` is real and positive, and the Stirling series is
truncated after `m` Bernoulli correction terms, the remainder is bounded in
absolute value by the first omitted Bernoulli correction term and has the
corresponding sign. The implemented absolute tail bound is:

```text
|R_m(x)| <= |B_{2m+2}| / ((2m + 2)(2m + 1) x^(2m + 1)).
```

This is the bound recorded in result diagnostics as `tail_bound`. The final
returned `abs_error_bound` also includes the Arb rounding radius from the
finite Stirling sum.

The reference used for this scope is DLMF 5.11(i), which states the
first-neglected-term remainder property for the gamma-function asymptotic
expansions when the variable is real and positive:
<https://dlmf.nist.gov/5.11.i>.

This theorem does not apply to complex `z`, branch-cut or principal-branch
complex `loggamma`, gamma-ratio asymptotics, or beta asymptotics. Those cases
remain outside the `stirling_loggamma_positive_real` certificate scope.

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

Certified shifted Stirling results additionally record:

- `selected_method`: `stirling_shifted`;
- `shift`: the integer recurrence shift `r`;
- `shifted_argument`: the positive-real argument `y = x + r`;
- `shift_policy`: one of `direct_no_shift`, `window_37_38`, or
  `minimal_shift`;
- `guard_digits`: `2`;
- `effective_dps`: `requested_dps + 2`;
- `stirling_terms`: the number of Bernoulli correction terms included;
- `largest_bernoulli_used`: including the omitted Bernoulli number used for
  the tail bound;
- `coefficient_source`: `table` or `table+flint_fallback`;
- `tail_bound`: the rigorous bound applied at the shifted argument.

These diagnostics distinguish the custom asymptotic certificate from direct
Arb primitive certificates and from non-certified SciPy or mpmath values.
When `method="certified_auto"` is used, the selected result also records
`auto_selector="certified_auto"`, `auto_selected_method`, `auto_reason`, and
`auto_candidates`; the selected backend's certificate scope and method field
remain unchanged.

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
selection; explicit `method="stirling"` and `method="stirling_shifted"` never
silently fall back to Arb or mpmath. Explicit `method="certified_auto"` may
select direct Arb for excluded Stirling domains, including poles or complex
principal-branch requests, but that preserves the direct Arb certificate scope
or clean Arb failure and never becomes a custom Stirling certificate.
