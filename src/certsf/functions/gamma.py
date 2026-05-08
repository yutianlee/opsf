"""Gamma-family public wrappers."""

from __future__ import annotations

from certsf.dispatcher import dispatch


def gamma(z, *, dps: int = 50, mode: str = "auto", certify: bool = False):
    return dispatch("gamma", z, dps=dps, mode=mode, certify=certify)


def loggamma(z, *, dps: int = 50, mode: str = "auto", certify: bool = False):
    return dispatch("loggamma", z, dps=dps, mode=mode, certify=certify)


def rgamma(z, *, dps: int = 50, mode: str = "auto", certify: bool = False):
    return dispatch("rgamma", z, dps=dps, mode=mode, certify=certify)


def gamma_ratio(a, b, *, dps: int = 50, mode: str = "auto", certify: bool = False):
    return dispatch("gamma_ratio", a, b, dps=dps, mode=mode, certify=certify)
