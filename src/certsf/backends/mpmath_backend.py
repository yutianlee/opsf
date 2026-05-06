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


def _mp_result(function: str, value: str, requested_dps: int, working_dps: int):
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
        diagnostics={"mode": "high_precision", "warning": UNCERTIFIED_WARNING},
    )
