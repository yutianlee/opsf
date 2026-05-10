"""Airy public wrapper."""

from __future__ import annotations

from certsf.dispatcher import dispatch


def airy(z, *, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return dispatch("airy", z, dps=dps, mode=mode, certify=certify, method=method)


def ai(
    z,
    *,
    derivative: int = 0,
    dps: int = 50,
    mode: str = "auto",
    certify: bool = False,
    method: str | None = None,
):
    """Return Airy Ai or Ai' as an :class:`certsf.SFResult`."""

    return dispatch("ai", z, int(derivative), dps=dps, mode=mode, certify=certify, method=method)


def bi(
    z,
    *,
    derivative: int = 0,
    dps: int = 50,
    mode: str = "auto",
    certify: bool = False,
    method: str | None = None,
):
    """Return Airy Bi or Bi' as an :class:`certsf.SFResult`."""

    return dispatch("bi", z, int(derivative), dps=dps, mode=mode, certify=certify, method=method)


airyai = ai
airybi = bi
