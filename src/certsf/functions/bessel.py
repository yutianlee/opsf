"""Bessel public wrappers."""

from __future__ import annotations

from certsf.dispatcher import dispatch


def besselj(v, z, *, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return dispatch("besselj", v, z, dps=dps, mode=mode, certify=certify, method=method)


def bessely(v, z, *, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return dispatch("bessely", v, z, dps=dps, mode=mode, certify=certify, method=method)


def besseli(v, z, *, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return dispatch("besseli", v, z, dps=dps, mode=mode, certify=certify, method=method)


def besselk(v, z, *, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return dispatch("besselk", v, z, dps=dps, mode=mode, certify=certify, method=method)
