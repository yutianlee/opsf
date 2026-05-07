# certsf

`certsf` provides special-function wrappers with explicit diagnostics and, where
available, rigorous Arb ball enclosures through `python-flint`.

The public API is intentionally small: every function returns an `SFResult`
object with the computed value, backend metadata, certification status, optional
error bounds, and diagnostics explaining how the result was produced.

The certification scope lives in [`docs/certification.md`](docs/certification.md);
the formula audit trail lives in [`docs/formula_audit.md`](docs/formula_audit.md).

## Installation

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

```python
from certsf import (
    gamma,
    loggamma,
    rgamma,
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

`rgamma` is the safest wrapper near non-positive integer gamma poles. In
certified mode, `rgamma` returns a rigorous zero at poles, while `gamma` and
`loggamma` return clean non-certified failures when the requested value is not
finite.

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
- `examples/basic_usage.py` for a short end-to-end usage example.
- `examples/certified_vs_high_precision.py` for a compact comparison of
  high-precision and certified result diagnostics.
- `benchmarks/bench_gamma.py`, `benchmarks/bench_airy.py`,
  `benchmarks/bench_bessel.py`, and `benchmarks/bench_pcf.py` for lightweight
  JSON-lines timing smoke benchmarks.
