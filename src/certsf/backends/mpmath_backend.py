"""mpmath high-precision wrappers."""

from __future__ import annotations

import mpmath as mp

from ._common import UNCERTIFIED_WARNING, ensure_dps, json_string, make_result


def mpmath_gamma(z, *, dps: int = 50):
    requested, working = _precisions(dps)
    with mp.workdps(working):
        value = mp.gamma(_mp_number(z))
        return _mp_result("gamma", _mp_string(value, requested), requested, working)


def mpmath_loggamma(z, *, dps: int = 50):
    requested, working = _precisions(dps)
    with mp.workdps(working):
        value = mp.loggamma(_mp_number(z))
        return _mp_result("loggamma", _mp_string(value, requested), requested, working)


def mpmath_rgamma(z, *, dps: int = 50):
    requested, working = _precisions(dps)
    with mp.workdps(working):
        value = mp.rgamma(_mp_number(z))
        return _mp_result("rgamma", _mp_string(value, requested), requested, working)


def mpmath_airy(z, *, dps: int = 50):
    requested, working = _precisions(dps)
    with mp.workdps(working):
        zz = _mp_number(z)
        value = json_string(
            {
                "ai": _mp_string(mp.airyai(zz), requested),
                "aip": _mp_string(mp.airyai(zz, derivative=1), requested),
                "bi": _mp_string(mp.airybi(zz), requested),
                "bip": _mp_string(mp.airybi(zz, derivative=1), requested),
            }
        )
        return _mp_result("airy", value, requested, working)


def mpmath_ai(z, derivative: int = 0, *, dps: int = 50):
    requested, working = _precisions(dps)
    derivative = _validate_airy_derivative(derivative)
    with mp.workdps(working):
        value = mp.airyai(_mp_number(z), derivative=derivative)
        return _mp_result(
            _airy_component_function("ai", derivative),
            _mp_string(value, requested),
            requested,
            working,
            diagnostics=_airy_component_diagnostics("ai", derivative),
        )


def mpmath_bi(z, derivative: int = 0, *, dps: int = 50):
    requested, working = _precisions(dps)
    derivative = _validate_airy_derivative(derivative)
    with mp.workdps(working):
        value = mp.airybi(_mp_number(z), derivative=derivative)
        return _mp_result(
            _airy_component_function("bi", derivative),
            _mp_string(value, requested),
            requested,
            working,
            diagnostics=_airy_component_diagnostics("bi", derivative),
        )


def mpmath_besselj(v, z, *, dps: int = 50):
    requested, working = _precisions(dps)
    with mp.workdps(working):
        value = mp.besselj(_mp_number(v), _mp_number(z))
        return _mp_result("besselj", _mp_string(value, requested), requested, working)


def mpmath_pbdv(v, x, *, dps: int = 50):
    requested, working = _precisions(dps)
    with mp.workdps(working):
        vv = _mp_number(v)
        xx = _mp_number(x)
        value = mp.pcfd(vv, xx)
        derivative = mp.diff(lambda t: mp.pcfd(vv, t), xx)
        payload = json_string(
            {
                "value": _mp_string(value, requested),
                "derivative": _mp_string(derivative, requested),
            }
        )
        return _mp_result("pbdv", payload, requested, working)


def _precisions(dps: int) -> tuple[int, int]:
    requested = ensure_dps(dps)
    return requested, max(requested + 10, 30)


def _mp_number(value):
    if isinstance(value, str):
        text = value.strip().replace("i", "j")
        if "j" in text.lower():
            parsed = complex(text)
            return mp.mpc(parsed.real, parsed.imag)
        return mp.mpf(text)
    if isinstance(value, complex):
        return mp.mpc(value.real, value.imag)
    return mp.mpf(value)


def _mp_string(value, requested_dps: int) -> str:
    return mp.nstr(value, n=max(requested_dps + 8, 20), strip_zeros=False)


def _mp_result(
    function: str,
    value: str,
    requested_dps: int,
    working_dps: int,
    diagnostics=None,
):
    default_diagnostics = {"mode": "high_precision", "warning": UNCERTIFIED_WARNING}
    return make_result(
        function=function,
        value=value,
        abs_error_bound=None,
        rel_error_bound=None,
        certified=False,
        method="mpmath",
        backend="mpmath",
        requested_dps=requested_dps,
        working_dps=working_dps,
        diagnostics=default_diagnostics if diagnostics is None else diagnostics,
    )


def _validate_airy_derivative(derivative: int) -> int:
    derivative = int(derivative)
    if derivative not in {0, 1}:
        raise ValueError("Airy component wrappers support derivative=0 or derivative=1")
    return derivative


def _airy_component_function(component: str, derivative: int) -> str:
    return component if derivative == 0 else f"{component}p"


def _airy_component_diagnostics(component: str, derivative: int):
    return {
        "mode": "high_precision",
        "component": component,
        "derivative": derivative,
        "warning": UNCERTIFIED_WARNING,
    }
