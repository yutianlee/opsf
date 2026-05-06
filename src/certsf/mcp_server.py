"""Thin optional MCP wrapper for the certsf public API."""

from __future__ import annotations

from .functions.airy import ai, airy, bi
from .functions.bessel import besseli, besselj, besselk, bessely
from .functions.gamma import gamma, loggamma, rgamma
from .functions.parabolic_cylinder import pbdv


def special_gamma(z: str, dps: int = 50, mode: str = "auto", certify: bool = False):
    return gamma(z, dps=dps, mode=mode, certify=certify).to_dict()


def special_loggamma(z: str, dps: int = 50, mode: str = "auto", certify: bool = False):
    return loggamma(z, dps=dps, mode=mode, certify=certify).to_dict()


def special_rgamma(z: str, dps: int = 50, mode: str = "auto", certify: bool = False):
    return rgamma(z, dps=dps, mode=mode, certify=certify).to_dict()


def special_airy(z: str, dps: int = 50, mode: str = "auto", certify: bool = False):
    return airy(z, dps=dps, mode=mode, certify=certify).to_dict()


def special_ai(z: str, derivative: int = 0, dps: int = 50, mode: str = "auto", certify: bool = False):
    return ai(z, derivative=derivative, dps=dps, mode=mode, certify=certify).to_dict()


def special_bi(z: str, derivative: int = 0, dps: int = 50, mode: str = "auto", certify: bool = False):
    return bi(z, derivative=derivative, dps=dps, mode=mode, certify=certify).to_dict()


def special_besselj(v: str, z: str, dps: int = 50, mode: str = "auto", certify: bool = False):
    return besselj(v, z, dps=dps, mode=mode, certify=certify).to_dict()


def special_bessely(v: str, z: str, dps: int = 50, mode: str = "auto", certify: bool = False):
    return bessely(v, z, dps=dps, mode=mode, certify=certify).to_dict()


def special_besseli(v: str, z: str, dps: int = 50, mode: str = "auto", certify: bool = False):
    return besseli(v, z, dps=dps, mode=mode, certify=certify).to_dict()


def special_besselk(v: str, z: str, dps: int = 50, mode: str = "auto", certify: bool = False):
    return besselk(v, z, dps=dps, mode=mode, certify=certify).to_dict()


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
    server.tool()(special_rgamma)
    server.tool()(special_airy)
    server.tool()(special_ai)
    server.tool()(special_bi)
    server.tool()(special_besselj)
    server.tool()(special_bessely)
    server.tool()(special_besseli)
    server.tool()(special_besselk)
    server.tool()(special_pbdv)
    return server


if __name__ == "__main__":  # pragma: no cover - manual server entrypoint
    build_server().run()
