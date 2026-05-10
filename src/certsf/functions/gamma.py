"""Gamma-family public wrappers."""

from __future__ import annotations

from certsf.dispatcher import dispatch


def beta(a, b, *, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return dispatch("beta", a, b, dps=dps, mode=mode, certify=certify, method=method)


def gamma(z, *, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return dispatch("gamma", z, dps=dps, mode=mode, certify=certify, method=method)


def loggamma(z, *, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return dispatch("loggamma", z, dps=dps, mode=mode, certify=certify, method=method)


def loggamma_ratio(a, b, *, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return dispatch("loggamma_ratio", a, b, dps=dps, mode=mode, certify=certify, method=method)


def pochhammer(a, n, *, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return dispatch("pochhammer", a, n, dps=dps, mode=mode, certify=certify, method=method)


def rgamma(z, *, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return dispatch("rgamma", z, dps=dps, mode=mode, certify=certify, method=method)


def gamma_ratio(a, b, *, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return dispatch("gamma_ratio", a, b, dps=dps, mode=mode, certify=certify, method=method)
