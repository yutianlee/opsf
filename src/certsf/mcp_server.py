"""Thin optional MCP wrapper for the certsf public API."""

from __future__ import annotations

from .functions.airy import airy
from .functions.bessel import besselj
from .functions.gamma import gamma, loggamma
from .functions.parabolic_cylinder import pbdv


def special_gamma(z: str, dps: int = 50, mode: str = "auto", certify: bool = False):
    return gamma(z, dps=dps, mode=mode, certify=certify).to_dict()


def special_loggamma(z: str, dps: int = 50, mode: str = "auto", certify: bool = False):
    return loggamma(z, dps=dps, mode=mode, certify=certify).to_dict()


def special_airy(z: str, dps: int = 50, mode: str = "auto", certify: bool = False):
    return airy(z, dps=dps, mode=mode, certify=certify).to_dict()


def special_besselj(v: str, z: str, dps: int = 50, mode: str = "auto", certify: bool = False):
    return besselj(v, z, dps=dps, mode=mode, certify=certify).to_dict()


def special_pbdv(v: str, x: str, dps: int = 50, mode: str = "auto", certify: bool = False):
    return pbdv(v, x, dps=dps, mode=mode, certify=certify).to_dict()


def build_server():
    """Build a FastMCP server when the optional MCP SDK is installed."""

    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise ImportError("Install certsf[mcp] to run the MCP server.") from exc

    server = FastMCP("certsf")
    server.tool()(special_gamma)
    server.tool()(special_loggamma)
    server.tool()(special_airy)
    server.tool()(special_besselj)
    server.tool()(special_pbdv)
    return server


if __name__ == "__main__":  # pragma: no cover - manual server entrypoint
    build_server().run()
