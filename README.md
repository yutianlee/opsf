# certsf

`certsf` provides alpha special-function wrappers with explicit certification
diagnostics and, where available, rigorous Arb ball enclosures through
`python-flint`.

The public API is intentionally small: every function returns an `SFResult`
object with the computed value, backend metadata, certification status, optional
error bounds, and diagnostics explaining how the result was produced.

The certification scope lives in [`docs/certification.md`](docs/certification.md);
the scope-by-scope audit lives in
[`docs/certification_audit.md`](docs/certification_audit.md);
the current 0.2.0 alpha support matrix lives in
[`docs/certified_scope_0_2_0.md`](docs/certified_scope_0_2_0.md). The frozen
0.1.0 matrix remains archived in
[`docs/certified_scope_0_1_0.md`](docs/certified_scope_0_1_0.md), and the
formula audit trail lives in [`docs/formula_audit.md`](docs/formula_audit.md).
Release claim wording is guarded by
[`docs/release_claims.md`](docs/release_claims.md).

## Installation

From PyPI:

```bash
python -m pip install certsf
```

For certified Arb-backed mode:

```bash
python -m pip install "certsf[certified]"
```

For MCP tooling plus certified mode:

```bash
python -m pip install "certsf[mcp,certified]"
```

Prerelease versions such as `0.1.0a3` require `--pre` unless installing an exact
version, for example `certsf==0.1.0a3`.

For local development:

```powershell
python -m pip install -e ".[dev]"
```

For runtime use without optional MCP tooling:

```powershell
python -m pip install -e ".[certified]"
```

The base package depends on `scipy` and `mpmath`. Certified mode additionally
requires `python-flint`.

## Quick Start

```python
from certsf import gamma, besselj, pcfu

g = gamma("3.2", dps=50, mode="certified")
j = besselj("2.5", "4.0+1.25j", dps=60, mode="certified")
u = pcfu("2.5", "1.25", dps=60, mode="certified")

print(g.value)
print(g.abs_error_bound)
print(g.certified)
print(g.backend)
print(g.diagnostics)
```

For a plain numerical value, use `mode="fast"` or `mode="high_precision"`:

```python
from certsf import airy

result = airy("1.0", dps=80, mode="high_precision")
print(result.value)
```

## Result Object

Every wrapper returns an `SFResult` with these fields:

- `value`: string value, or a JSON string for multi-component results.
- `abs_error_bound`: rigorous absolute error bound when certified.
- `rel_error_bound`: rigorous relative error bound when available.
- `certified`: `True` only when a rigorous enclosure was produced.
- `function`: canonical function name.
- `method`: implementation method, such as `scipy.special`, `mpmath`, or
  `arb_ball`.
- `backend`: backend package name.
- `requested_dps`: requested decimal precision.
- `working_dps`: internal decimal precision estimate.
- `diagnostics`: structured details about mode, domain, formula, and scope.

Unsupported certified domains return a clean non-certified result with
`value=""`, `certified=False`, and an explanatory diagnostics error. They do not
silently fall back to mpmath and call the value certified.

Certified successes also expose `diagnostics["certificate_level"]`,
`diagnostics["audit_status"]`, and `diagnostics["certification_claim"]`, so
callers can distinguish direct Arb primitive wrappers from formula-backed
experimental claims.

## Choosing a Mode

- `mode="fast"` uses `scipy.special`; it is quick and non-certified.
- `mode="high_precision"` uses `mpmath`; it supports higher precision and
  complex arguments, but is still non-certified.
- `mode="certified"` uses `python-flint` / Arb when a validated enclosure path
  exists.
- `mode="auto"` chooses certified mode when `certify=True`, otherwise fast mode
  for `dps <= 15` and high-precision mode for larger `dps` requests.

Fast mode is double precision. If you request more than 15 digits while forcing
`mode="fast"`, the result reports `working_dps=16` and includes a diagnostic
warning that the requested digits are not guaranteed.

Use `mode="certified"` when the error bound matters. Use `high_precision` when
you need more digits but not a rigorous certificate.

The dispatcher uses an explicit `MethodSpec` registry for every concrete mode.
Each registered method records its backend, callable, certification intent,
domain note, and certificate scope. Adding a public wrapper requires registering
its SciPy, mpmath, and Arb methods together; tests verify the registry, public
API, and MCP tool list stay in sync.

## Supported Functions

The 0.2.0 alpha line adds gamma-family wrappers while keeping the release
wording conservative and the parabolic-cylinder claims unchanged.

| Area | Release status |
| --- | --- |
| `gamma`, `loggamma`, `rgamma`, `gamma_ratio`, `loggamma_ratio`, `beta` | alpha-certified, direct Arb gamma primitives |
| `airy`, `ai`, `bi` | alpha-certified, direct Arb primitive |
| `besselj`, `bessely`, `besseli`, `besselk` | alpha-certified where direct Arb primitive works; real-valued order only |
| `pcfd`, `pcfu`, `pcfv`, `pcfw`, `pbdv` | experimental certified formula layer |
| MCP server | experimental tool interface |
| Custom Taylor/asymptotic methods | not yet |

```python
from certsf import (
    beta,
    gamma,
    loggamma,
    loggamma_ratio,
    rgamma,
    gamma_ratio,
    airy,
    ai,
    bi,
    besselj,
    bessely,
    besseli,
    besselk,
    pbdv,
    pcfd,
    pcfu,
    pcfv,
    pcfw,
)
```

### Gamma Family

- `gamma(z)`
- `loggamma(z)`, using the principal branch
- `rgamma(z) = 1 / gamma(z)`
- `gamma_ratio(a, b) = Gamma(a) / Gamma(b)`
- `loggamma_ratio(a, b) = loggamma(a) - loggamma(b)`, using the principal
  `loggamma` branch
- `beta(a, b) = Gamma(a) Gamma(b) / Gamma(a+b)`

`rgamma` is the safest wrapper near non-positive integer gamma poles. In
certified mode, `rgamma` returns a rigorous zero at poles, while `gamma` and
`loggamma` return clean non-certified failures when the requested value is not
finite.

```python
from certsf import gamma_ratio

r = gamma_ratio("3.2", "1.2", mode="certified", dps=50)
print(r.value)
print(r.certified)
print(r.diagnostics)
```

Certified `gamma_ratio(a, b)` evaluates `Gamma(a) * rgamma(b)`. This lets
denominator poles certify to exact zero when `Gamma(a)` is finite, while
numerator poles and simultaneous numerator/denominator poles return clean
non-certified failures with pole diagnostics. See
[`docs/gamma_ratio.md`](docs/gamma_ratio.md).

```python
from certsf import loggamma_ratio

r = loggamma_ratio("3.2", "1.2", mode="certified", dps=50)
print(r.value)
print(r.certified)
print(r.diagnostics)
```

Certified `loggamma_ratio(a, b)` evaluates Arb `lgamma(a) - lgamma(b)` with
`certificate_scope="direct_arb_loggamma_ratio"`. Any gamma pole in either
argument returns a clean non-certified failure. For complex values, the result
is the difference of principal `loggamma` values, not necessarily the principal
logarithm of `gamma_ratio(a, b)`. See
[`docs/loggamma_ratio.md`](docs/loggamma_ratio.md).

```python
from certsf import beta

r = beta("2", "3", mode="certified", dps=50)
print(r.value)
print(r.certified)
print(r.diagnostics)
```

Certified `beta(a, b)` evaluates `Gamma(a) * Gamma(b) * rgamma(a+b)` with
`certificate_scope="direct_arb_beta"`. Poles in `Gamma(a)` or `Gamma(b)` return
clean non-certified failures. A pole in `Gamma(a+b)` certifies to zero only when
both numerator gamma factors are finite and Arb returns the zero product. The
wrapper does not claim limiting values at simultaneous singularities. See
[`docs/beta.md`](docs/beta.md).

### Airy Family

- `airy(z)` returns Ai, Ai', Bi, and Bi' in one JSON payload.
- `ai(z, derivative=0)` and `ai(z, derivative=1)`.
- `bi(z, derivative=0)` and `bi(z, derivative=1)`.

Certified Airy wrappers use Arb ball arithmetic and report component-level
absolute and relative error bounds.

### Bessel Family

- `besselj(v, z)` for \(J_v(z)\)
- `bessely(v, z)` for \(Y_v(z)\)
- `besseli(v, z)` for \(I_v(z)\)
- `besselk(v, z)` for \(K_v(z)\)

Certified Bessel wrappers support real-valued order and real or complex
arguments. Complex order is outside the certified scope and returns a clean
non-certified failure.

### Parabolic-Cylinder Family

- `pbdv(v, x)` returns \(D_v(x)\) and \(D_v'(x)\) in one JSON payload.
- `pcfd(v, z)` returns \(D_v(z)\).
- `pcfu(a, z)` returns \(U(a,z)\).
- `pcfv(a, z)` returns \(V(a,z)\).
- `pcfw(a, x)` returns \(W(a,x)\).

Certified `pcfu`, `pcfd`, `pbdv`, and `pcfv` support real parameters and real
or complex arguments. Certified `pcfw` currently supports real parameters and
real arguments; complex arguments return a clean non-certified failure until a
validated complex-domain target is selected.

For `pbdv`, the argument name `x` follows SciPy's real-variable naming, but the
certified formula layer intentionally accepts complex arguments for the
`D_v(x)` value and derivative pair. Use `pcfd(v, z)` when only the complex
`D_v(z)` value is needed.

The parabolic-cylinder family is an experimental certified formula layer: Arb
encloses the implemented documented formula, while formula/domain audit remains
visible before broadening the claim.

## Multi-Component Values

Functions such as `airy` and `pbdv` keep backward-compatible JSON strings in
`SFResult.value`, and provide helpers for Python callers:

```python
from certsf import pbdv

result = pbdv("2.5", "1.25", dps=60, mode="certified")
values = result.value_as_dict()
bounds = result.abs_error_bound_as_dict()

print(values["value"])
print(values["derivative"])
print(bounds["value"])
print(bounds["derivative"])
print(result.component("value"))
```

## MCP Wrapper

`certsf.mcp_server` exposes thin MCP-facing wrappers around the same public API.
MCP payloads decode multi-component values and bounds as nested JSON objects
instead of JSON-encoded strings.
Install the optional MCP dependency before running the server:

```powershell
python -m pip install -e ".[mcp,certified]"
python -m certsf.mcp_server
```

## Development

Run the test suite with:

```powershell
python -m pytest
```

The tests exercise the SciPy, mpmath, and Arb-backed paths when the optional
dependencies are installed.

The repository also includes:

- `docs/release_checklist.md` for prerelease/release verification.
- `docs/release_claims.md` for conservative alpha release claim wording.
- `docs/certification_audit.md` for scope-level certification evidence and
  remaining audit gates.
- `docs/audit/` for family-level certification checklists.
- `docs/gamma_ratio.md` for gamma-ratio pole policy and certified-backend
  rationale.
- `docs/loggamma_ratio.md` for loggamma-ratio branch convention and pole
  policy.
- `docs/beta.md` for beta-function pole policy and certified-backend
  rationale.
- `docs/certified_scope_0_2_0.md` for the current 0.2.0 alpha certified
  support matrix.
- `docs/certified_scope_0_1_0.md` for the frozen 0.1.0 certified support
  matrix.
- `docs/release-0.2.0-alpha.3.md` for v0.2.0-alpha.3 feature-alpha planning
  notes.
- `docs/release-0.2.0-alpha.2.md` for v0.2.0-alpha.2 feature-alpha planning
  notes.
- `docs/release-0.2.0-alpha.1.md` for v0.2.0-alpha.1 feature-alpha planning
  notes.
- `docs/release-0.1.0.md` for conservative 0.1.0 release notes and example
  commands.
- `docs/release-0.1.0-alpha.2.md` for the v0.1.0-alpha.2 planning notes.
- `examples/basic_usage.py` for a short end-to-end usage example.
- `examples/certified_vs_high_precision.py` for a compact comparison of
  high-precision and certified result diagnostics.
- `examples/gamma_certified.py`, `examples/airy_components.py`,
  `examples/bessel_complex.py`, `examples/pcf_experimental.py`, and
  `examples/mcp_payload.py` for payload-first release examples.
- `benchmarks/bench_gamma.py`, `benchmarks/bench_airy.py`,
  `benchmarks/bench_bessel.py`, and `benchmarks/bench_pcf.py` for lightweight
  JSON-lines timing smoke benchmarks.
