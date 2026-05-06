# certsf

`certsf` is a Phase 1 special-functions package skeleton. It exposes a stable
`SFResult` return object, thin wrappers over SciPy, mpmath, and python-flint
where available, plus an optional MCP-facing wrapper module.

```python
from certsf import gamma, airy, besselj, pbdv

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

Certified mode returns clean non-certified failures for Phase 1 gaps instead
of silently falling back to mpmath and calling the result certified.
