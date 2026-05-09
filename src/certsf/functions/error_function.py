"""Error-function public wrappers."""

from __future__ import annotations

from certsf.dispatcher import dispatch


def erf(z, *, dps: int = 50, mode: str = "auto", certify: bool = False):
    return dispatch("erf", z, dps=dps, mode=mode, certify=certify)


def erfc(z, *, dps: int = 50, mode: str = "auto", certify: bool = False):
    return dispatch("erfc", z, dps=dps, mode=mode, certify=certify)


def erfcx(z, *, dps: int = 50, mode: str = "auto", certify: bool = False):
    return dispatch("erfcx", z, dps=dps, mode=mode, certify=certify)


def erfi(z, *, dps: int = 50, mode: str = "auto", certify: bool = False):
    return dispatch("erfi", z, dps=dps, mode=mode, certify=certify)


def dawson(z, *, dps: int = 50, mode: str = "auto", certify: bool = False):
    return dispatch("dawson", z, dps=dps, mode=mode, certify=certify)
