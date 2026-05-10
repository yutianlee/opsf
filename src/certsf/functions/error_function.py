"""Error-function public wrappers."""

from __future__ import annotations

from certsf.dispatcher import dispatch


def erf(z, *, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return dispatch("erf", z, dps=dps, mode=mode, certify=certify, method=method)


def erfc(z, *, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return dispatch("erfc", z, dps=dps, mode=mode, certify=certify, method=method)


def erfcx(z, *, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return dispatch("erfcx", z, dps=dps, mode=mode, certify=certify, method=method)


def erfi(z, *, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return dispatch("erfi", z, dps=dps, mode=mode, certify=certify, method=method)


def dawson(z, *, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return dispatch("dawson", z, dps=dps, mode=mode, certify=certify, method=method)


def erfinv(x, *, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return dispatch("erfinv", x, dps=dps, mode=mode, certify=certify, method=method)


def erfcinv(x, *, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return dispatch("erfcinv", x, dps=dps, mode=mode, certify=certify, method=method)
