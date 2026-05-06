"""Airy public wrapper."""

from __future__ import annotations

from certsf.dispatcher import dispatch


def airy(z, *, dps: int = 50, mode: str = "auto", certify: bool = False):
    return dispatch("airy", z, dps=dps, mode=mode, certify=certify)
