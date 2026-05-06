# certsf

`certsf` is a Phase 1 special-functions package skeleton. It exposes a stable
`SFResult` return object, thin wrappers over SciPy, mpmath, and python-flint
where available, plus an optional MCP-facing wrapper module.

```python
from certsf import gamma, loggamma, rgamma, airy, ai, bi, besselj, bessely, besseli, besselk, pbdv

r = gamma(3.2, dps=50, mode="auto", certify=True)

print(r.value)
print(r.abs_error_bound)
print(r.certified)
print(r.backend)
print(r.method)
print(r.diagnostics)
```

Phase 1 intentionally avoids custom Taylor, asymptotic, recurrence, and ODE
algorithms. The goal is to prove the wrapper architecture and diagnostics
contract before adding deeper certified methods.

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
