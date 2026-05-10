"""Parabolic-cylinder public wrappers."""

from __future__ import annotations

from certsf.dispatcher import dispatch


def pbdv(v, x, *, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return dispatch("pbdv", v, x, dps=dps, mode=mode, certify=certify, method=method)


def pcfd(v, z, *, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return dispatch("pcfd", v, z, dps=dps, mode=mode, certify=certify, method=method)


def pcfu(a, z, *, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return dispatch("pcfu", a, z, dps=dps, mode=mode, certify=certify, method=method)


def pcfv(a, z, *, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return dispatch("pcfv", a, z, dps=dps, mode=mode, certify=certify, method=method)


def pcfw(a, z, *, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return dispatch("pcfw", a, z, dps=dps, mode=mode, certify=certify, method=method)
