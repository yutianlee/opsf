"""Parabolic-cylinder public wrappers."""

from __future__ import annotations

from certsf.dispatcher import dispatch


def pbdv(v, x, *, dps: int = 50, mode: str = "auto", certify: bool = False):
    return dispatch("pbdv", v, x, dps=dps, mode=mode, certify=certify)
