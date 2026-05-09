"""mpmath high-precision wrappers."""

from __future__ import annotations

from typing import Any, cast

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


def mpmath_loggamma_ratio(a, b, *, dps: int = 50):
    requested, working = _precisions(dps)
    with mp.workdps(working):
        value = mp.loggamma(_mp_number(a)) - mp.loggamma(_mp_number(b))
        return _mp_result("loggamma_ratio", _mp_string(value, requested), requested, working)


def mpmath_beta(a, b, *, dps: int = 50):
    requested, working = _precisions(dps)
    with mp.workdps(working):
        aa = _mp_number(a)
        bb = _mp_number(b)
        if hasattr(mp, "beta"):
            value = mp.beta(aa, bb)
        else:
            value = mp.exp(mp.loggamma(aa) + mp.loggamma(bb) - mp.loggamma(aa + bb))
        return _mp_result("beta", _mp_string(value, requested), requested, working)


def mpmath_pochhammer(a, n, *, dps: int = 50):
    requested, working = _precisions(dps)
    with mp.workdps(working):
        value = mp.rf(_mp_number(a), _mp_number(n))
        return _mp_result("pochhammer", _mp_string(value, requested), requested, working)


def mpmath_rgamma(z, *, dps: int = 50):
    requested, working = _precisions(dps)
    with mp.workdps(working):
        value = mp.rgamma(_mp_number(z))
        return _mp_result("rgamma", _mp_string(value, requested), requested, working)


def mpmath_gamma_ratio(a, b, *, dps: int = 50):
    requested, working = _precisions(dps)
    with mp.workdps(working):
        value = mp.exp(mp.loggamma(_mp_number(a)) - mp.loggamma(_mp_number(b)))
        return _mp_result("gamma_ratio", _mp_string(value, requested), requested, working)


def mpmath_erf(z, *, dps: int = 50):
    requested, working = _precisions(dps)
    with mp.workdps(working):
        value = mp.erf(_mp_number(z))
        return _mp_result("erf", _mp_string(value, requested), requested, working)


def mpmath_erfc(z, *, dps: int = 50):
    requested, working = _precisions(dps)
    with mp.workdps(working):
        value = mp.erfc(_mp_number(z))
        return _mp_result("erfc", _mp_string(value, requested), requested, working)


def mpmath_erfcx(z, *, dps: int = 50):
    requested, working = _precisions(dps)
    with mp.workdps(working):
        zz = _mp_number(z)
        value = mp.exp(zz * zz) * mp.erfc(zz)
        return _mp_result("erfcx", _mp_string(value, requested), requested, working)


def mpmath_erfi(z, *, dps: int = 50):
    requested, working = _precisions(dps)
    with mp.workdps(working):
        zz = _mp_number(z)
        method = getattr(mp, "erfi", None)
        value = method(zz) if method is not None else -mp.j * mp.erf(mp.j * zz)
        return _mp_result("erfi", _mp_string(value, requested), requested, working)


def mpmath_dawson(z, *, dps: int = 50):
    requested, working = _precisions(dps)
    with mp.workdps(working):
        zz = _mp_number(z)
        method = getattr(mp, "dawson", None) or getattr(mp, "dawsn", None)
        if method is not None:
            value = method(zz)
        else:
            erfi_method = getattr(mp, "erfi", None)
            erfi_value = erfi_method(zz) if erfi_method is not None else -mp.j * mp.erf(mp.j * zz)
            value = mp.sqrt(mp.pi) / 2 * mp.exp(-zz * zz) * erfi_value
        return _mp_result("dawson", _mp_string(value, requested), requested, working)


def mpmath_erfinv(x, *, dps: int = 50):
    requested, working = _precisions(dps)
    with mp.workdps(working):
        xx = _mp_number(x)
        method = getattr(mp, "erfinv", None)
        value = method(xx) if method is not None else _mp_erfinv_solve(xx)
        return _mp_result("erfinv", _mp_string(value, requested), requested, working)


def mpmath_erfcinv(x, *, dps: int = 50):
    requested, working = _precisions(dps)
    with mp.workdps(working):
        xx = _mp_number(x)
        value = _mp_erfcinv_value(xx)
        return _mp_result("erfcinv", _mp_string(value, requested), requested, working)


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


def mpmath_bessely(v, z, *, dps: int = 50):
    requested, working = _precisions(dps)
    with mp.workdps(working):
        value = mp.bessely(_mp_number(v), _mp_number(z))
        return _mp_result("bessely", _mp_string(value, requested), requested, working)


def mpmath_besseli(v, z, *, dps: int = 50):
    requested, working = _precisions(dps)
    with mp.workdps(working):
        value = mp.besseli(_mp_number(v), _mp_number(z))
        return _mp_result("besseli", _mp_string(value, requested), requested, working)


def mpmath_besselk(v, z, *, dps: int = 50):
    requested, working = _precisions(dps)
    with mp.workdps(working):
        value = mp.besselk(_mp_number(v), _mp_number(z))
        return _mp_result("besselk", _mp_string(value, requested), requested, working)


def mpmath_pbdv(v, x, *, dps: int = 50):
    requested, working = _precisions(dps)
    with mp.workdps(working):
        vv = _mp_number(v)
        xx = _mp_number(x)
        value = mp.pcfd(vv, xx)
        derivative = (xx / 2) * value - mp.pcfd(vv + 1, xx)
        payload = json_string(
            {
                "value": _mp_string(value, requested),
                "derivative": _mp_string(derivative, requested),
            }
        )
        return _mp_result("pbdv", payload, requested, working)


def mpmath_pcfd(v, z, *, dps: int = 50):
    requested, working = _precisions(dps)
    with mp.workdps(working):
        value = mp.pcfd(_mp_number(v), _mp_number(z))
        return _mp_result("pcfd", _mp_string(value, requested), requested, working)


def mpmath_pcfu(a, z, *, dps: int = 50):
    requested, working = _precisions(dps)
    with mp.workdps(working):
        value = mp.pcfu(_mp_number(a), _mp_number(z))
        return _mp_result("pcfu", _mp_string(value, requested), requested, working)


def mpmath_pcfv(a, z, *, dps: int = 50):
    requested, working = _precisions(dps)
    with mp.workdps(working):
        value = mp.pcfv(_mp_number(a), _mp_number(z))
        return _mp_result("pcfv", _mp_string(value, requested), requested, working)


def mpmath_pcfw(a, z, *, dps: int = 50):
    requested, working = _precisions(dps)
    with mp.workdps(working):
        value = mp.pcfw(_mp_number(a), _mp_number(z))
        return _mp_result("pcfw", _mp_string(value, requested), requested, working)


def _precisions(dps: int) -> tuple[int, int]:
    requested = ensure_dps(dps)
    return requested, max(requested + 10, 30)


def _mp_number(value):
    if isinstance(value, str):
        text = value.strip().replace("i", "j")
        if "j" in text.lower():
            real, imag = _parse_complex_text(text)
            return mp.mpc(cast(Any, mp.mpf(real)), cast(Any, mp.mpf(imag)))
        return mp.mpf(text)
    if isinstance(value, complex):
        return mp.mpc(cast(Any, value.real), cast(Any, value.imag))
    return mp.mpf(value)


def _parse_complex_text(text: str) -> tuple[str, str]:
    text = text.strip()
    if text.startswith("(") and text.endswith(")"):
        text = text[1:-1].strip()
    if not text.lower().endswith("j"):
        raise ValueError(f"complex string must end with 'j': {text!r}")

    body = text[:-1].strip()
    split_at = None
    for index in range(1, len(body)):
        if body[index] in "+-" and body[index - 1].lower() != "e":
            split_at = index
    if split_at is None:
        real = "0"
        imag = body
    else:
        real = body[:split_at]
        imag = body[split_at:]
    if imag in {"", "+"}:
        imag = "1"
    elif imag == "-":
        imag = "-1"
    return real, imag


def _mp_string(value, requested_dps: int) -> str:
    return str(mp.nstr(value, n=max(requested_dps + 8, 20), strip_zeros=False))


def _mp_erfinv_solve(value):
    if value == 0:
        return mp.mpf("0")
    if not (mp.im(value) == 0 and -1 < mp.re(value) < 1):
        raise ValueError("high-precision erfinv fallback supports real x in (-1, 1)")

    xx = mp.re(value)
    sign = -1 if xx < 0 else 1
    abs_x = abs(xx)
    a = mp.mpf("0.147")
    log_term = mp.log(1 - abs_x * abs_x)
    first = 2 / (mp.pi * a) + log_term / 2
    guess = sign * mp.sqrt(mp.sqrt(first * first - log_term / a) - first)
    return mp.findroot(lambda y: mp.erf(y) - xx, guess)


def _mp_erfcinv_value(value):
    if not (mp.im(value) == 0 and 0 < mp.re(value) < 2):
        raise ValueError("high-precision erfcinv supports real x in (0, 2)")

    xx = mp.re(value)
    method = getattr(mp, "erfcinv", None)
    if method is not None:
        return method(xx)

    erfinv_method = getattr(mp, "erfinv", None)
    return erfinv_method(1 - xx) if erfinv_method is not None else _mp_erfinv_solve(1 - xx)


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
