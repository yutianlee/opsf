# certsf

`certsf` is a phase-built certified special-functions package. It exposes a stable
`SFResult` return object, thin wrappers over SciPy, mpmath, and python-flint
where available, plus an optional MCP-facing wrapper module.

```python
from certsf import gamma, loggamma, rgamma, airy, ai, bi, besselj, bessely, besseli, besselk
from certsf import pbdv, pcfd, pcfu, pcfv, pcfw

r = gamma(3.2, dps=50, mode="auto", certify=True)

print(r.value)
print(r.abs_error_bound)
print(r.certified)
print(r.backend)
print(r.method)
print(r.diagnostics)
```

The initial phase intentionally avoided custom Taylor, asymptotic, recurrence,
and ODE algorithms. That kept the wrapper architecture and diagnostics contract
small before the later certified-method phases expanded coverage.

## Modes

- `mode="fast"` uses `scipy.special` and returns `certified=False`.
- `mode="high_precision"` uses `mpmath` and returns `certified=False`.
- `mode="certified"` uses `python-flint` / Arb when implemented.
- `mode="auto"` chooses `certified` when `certify=True`, otherwise `fast`.

Certified mode returns clean non-certified failures for unsupported domains
instead of silently falling back to mpmath and calling the result certified.

## Phase 2 gamma family

The gamma-family API includes:

- `gamma(z)`
- `loggamma(z)` on the principal branch
- `rgamma(z) = 1 / gamma(z)`

`rgamma` is the preferred building block near non-positive integer poles. In
certified mode it returns a rigorous zero at gamma poles, while `gamma` and
`loggamma` return clean non-certified failures when the requested value is not
finite.

## Phase 3 Airy family

The Airy API includes:

- `airy(z)` returning Ai, Ai', Bi, and Bi' in one JSON payload
- `ai(z, derivative=0)` and `ai(z, derivative=1)`
- `bi(z, derivative=0)` and `bi(z, derivative=1)`

For real arguments in certified mode, these functions use Arb ball arithmetic
and report component-level absolute and relative error bounds.

## Phase 4 integer-order Bessel family

The Bessel API includes:

- `besselj(n, x)` for \(J_n(x)\)
- `bessely(n, x)` for \(Y_n(x)\)
- `besseli(n, x)` for \(I_n(x)\)
- `besselk(n, x)` for \(K_n(x)\)

Phase 4 established certified Arb support for integer order and real arguments,
reported with `certificate_scope="phase4_integer_real_bessel"` in diagnostics.

## Phase 5 real-order and complex Bessel support

Certified Bessel support now accepts real-valued order and real or complex
arguments. Expanded Phase 5 cases report
`certificate_scope="phase5_real_order_complex_bessel"` in diagnostics. Complex
order is still outside the certified scope and returns a clean non-certified
failure.

## Phase 6 parabolic-cylinder family

The parabolic-cylinder API includes:

- `pbdv(v, x)` returning \(D_v(x)\) and its derivative in one JSON payload
- `pcfd(v, z)` for \(D_v(z)\)
- `pcfu(a, z)` for \(U(a,z)\)
- `pcfv(a, z)` for \(V(a,z)\)
- `pcfw(a, z)` for \(W(a,z)\)

Fast real-valued mode delegates to SciPy where SciPy exposes the convention
directly or through a parameter translation. High-precision mode delegates to
mpmath and supports complex arguments.

## Phase 7 certified parabolic-cylinder core

Certified mode now covers the core parabolic-cylinder path for real parameters
and real or complex arguments:

- `pcfu(a, z)` uses Arb ball arithmetic with the global confluent
  hypergeometric `1F1` representation.
- `pcfd(v, z)` uses the identity \(D_v(z)=U(-v-\frac{1}{2}, z)\).
- `pbdv(v, x)` returns certified balls for \(D_v(x)\) and
  \(D_v'(x)=\frac{x}{2}D_v(x)-D_{v+1}(x)\).

These results report
`certificate_scope="phase7_hypergeometric_parabolic_cylinder"` in diagnostics.

## Phase 8 parabolic-cylinder connections

Certified mode now also covers the remaining parabolic-cylinder connection
functions for real parameters:

- `pcfv(a, z)` uses the DLMF connection formula through `pcfu`, supporting real
  or complex arguments.
- `pcfw(a, x)` uses the real-argument DLMF 12.14 connection formula through
  rotated `pcfu` values.

These results report
`certificate_scope="phase8_parabolic_cylinder_connections"` in diagnostics.
Certified `pcfw` returns a clean non-certified failure for complex arguments
until a complex-domain definition and validation target are selected.
