"""Bessel public wrappers."""

from __future__ import annotations

from certsf.dispatcher import dispatch


def besselj(v, z, *, dps: int = 50, mode: str = "auto", certify: bool = False):
    return dispatch("besselj", v, z, dps=dps, mode=mode, certify=certify)


def bessely(v, z, *, dps: int = 50, mode: str = "auto", certify: bool = False):
    return dispatch("bessely", v, z, dps=dps, mode=mode, certify=certify)


def besseli(v, z, *, dps: int = 50, mode: str = "auto", certify: bool = False):
    return dispatch("besseli", v, z, dps=dps, mode=mode, certify=certify)


def besselk(v, z, *, dps: int = 50, mode: str = "auto", certify: bool = False):
    return dispatch("besselk", v, z, dps=dps, mode=mode, certify=certify)
