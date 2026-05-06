"""SciPy fast-mode wrappers."""

from __future__ import annotations

from scipy import special

from ._common import (
    ensure_dps,
    float_digits,
    json_string,
    make_result,
    number_to_string,
    scipy_number,
    scipy_real,
)


def scipy_gamma(z, *, dps: int = 50):
    requested = ensure_dps(dps)
    value = special.gamma(scipy_number(z))
    return _fast_result("gamma", number_to_string(value, digits=float_digits(requested)), requested)


def scipy_loggamma(z, *, dps: int = 50):
    requested = ensure_dps(dps)
    value = special.loggamma(scipy_number(z))
    return _fast_result("loggamma", number_to_string(value, digits=float_digits(requested)), requested)


def scipy_rgamma(z, *, dps: int = 50):
    requested = ensure_dps(dps)
    value = special.rgamma(scipy_number(z))
    return _fast_result("rgamma", number_to_string(value, digits=float_digits(requested)), requested)


def scipy_airy(z, *, dps: int = 50):
    requested = ensure_dps(dps)
    ai, aip, bi, bip = special.airy(scipy_number(z))
    value = json_string(
        {
            "ai": number_to_string(ai, digits=float_digits(requested)),
            "aip": number_to_string(aip, digits=float_digits(requested)),
            "bi": number_to_string(bi, digits=float_digits(requested)),
            "bip": number_to_string(bip, digits=float_digits(requested)),
        }
    )
    return _fast_result("airy", value, requested)


def scipy_ai(z, derivative: int = 0, *, dps: int = 50):
    requested = ensure_dps(dps)
    derivative = _validate_airy_derivative(derivative)
    values = special.airy(scipy_number(z))
    return _fast_result(
        _airy_component_function("ai", derivative),
        number_to_string(values[derivative], digits=float_digits(requested)),
        requested,
        diagnostics={"mode": "fast", "component": "ai", "derivative": derivative},
    )


def scipy_bi(z, derivative: int = 0, *, dps: int = 50):
    requested = ensure_dps(dps)
    derivative = _validate_airy_derivative(derivative)
    values = special.airy(scipy_number(z))
    return _fast_result(
        _airy_component_function("bi", derivative),
        number_to_string(values[2 + derivative], digits=float_digits(requested)),
        requested,
        diagnostics={"mode": "fast", "component": "bi", "derivative": derivative},
    )


def scipy_besselj(v, z, *, dps: int = 50):
    requested = ensure_dps(dps)
    value = special.jv(scipy_number(v), scipy_number(z))
    return _fast_result("besselj", number_to_string(value, digits=float_digits(requested)), requested)


def scipy_bessely(v, z, *, dps: int = 50):
    requested = ensure_dps(dps)
    value = special.yv(scipy_number(v), scipy_number(z))
    return _fast_result("bessely", number_to_string(value, digits=float_digits(requested)), requested)


def scipy_besseli(v, z, *, dps: int = 50):
    requested = ensure_dps(dps)
    value = special.iv(scipy_number(v), scipy_number(z))
    return _fast_result("besseli", number_to_string(value, digits=float_digits(requested)), requested)


def scipy_besselk(v, z, *, dps: int = 50):
    requested = ensure_dps(dps)
    value = special.kv(scipy_number(v), scipy_number(z))
    return _fast_result("besselk", number_to_string(value, digits=float_digits(requested)), requested)


def scipy_pbdv(v, x, *, dps: int = 50):
    requested = ensure_dps(dps)
    value, derivative = special.pbdv(scipy_real(v), scipy_real(x))
    payload = json_string(
        {
            "value": number_to_string(value, digits=float_digits(requested)),
            "derivative": number_to_string(derivative, digits=float_digits(requested)),
        }
    )
    return _fast_result("pbdv", payload, requested)


def _fast_result(function: str, value: str, requested_dps: int, diagnostics=None):
    return make_result(
        function=function,
        value=value,
        abs_error_bound=None,
        rel_error_bound=None,
        certified=False,
        method="scipy.special",
        backend="scipy",
        requested_dps=requested_dps,
        working_dps=16,
        diagnostics={"mode": "fast"} if diagnostics is None else diagnostics,
    )


def _validate_airy_derivative(derivative: int) -> int:
    derivative = int(derivative)
    if derivative not in {0, 1}:
        raise ValueError("Airy component wrappers support derivative=0 or derivative=1")
    return derivative


def _airy_component_function(component: str, derivative: int) -> str:
    return component if derivative == 0 else f"{component}p"
