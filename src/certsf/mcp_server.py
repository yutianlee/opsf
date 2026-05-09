"""Thin optional MCP wrapper for the certsf public API."""

from __future__ import annotations

from .functions.airy import ai, airy, bi
from .functions.bessel import besseli, besselj, besselk, bessely
from .functions.gamma import beta, gamma, gamma_ratio, loggamma, loggamma_ratio, rgamma
from .functions.parabolic_cylinder import pbdv, pcfd, pcfu, pcfv, pcfw


def special_gamma(z: str, dps: int = 50, mode: str = "auto", certify: bool = False):
    return gamma(z, dps=dps, mode=mode, certify=certify).to_mcp_dict()


def special_loggamma(z: str, dps: int = 50, mode: str = "auto", certify: bool = False):
    return loggamma(z, dps=dps, mode=mode, certify=certify).to_mcp_dict()


def special_rgamma(z: str, dps: int = 50, mode: str = "auto", certify: bool = False):
    return rgamma(z, dps=dps, mode=mode, certify=certify).to_mcp_dict()


def special_gamma_ratio(a: str, b: str, dps: int = 50, mode: str = "auto", certify: bool = False):
    return gamma_ratio(a, b, dps=dps, mode=mode, certify=certify).to_mcp_dict()


def special_loggamma_ratio(a: str, b: str, dps: int = 50, mode: str = "auto", certify: bool = False):
    return loggamma_ratio(a, b, dps=dps, mode=mode, certify=certify).to_mcp_dict()


def special_beta(a: str, b: str, dps: int = 50, mode: str = "auto", certify: bool = False):
    return beta(a, b, dps=dps, mode=mode, certify=certify).to_mcp_dict()


def special_airy(z: str, dps: int = 50, mode: str = "auto", certify: bool = False):
    return airy(z, dps=dps, mode=mode, certify=certify).to_mcp_dict()


def special_ai(z: str, derivative: int = 0, dps: int = 50, mode: str = "auto", certify: bool = False):
    return ai(z, derivative=derivative, dps=dps, mode=mode, certify=certify).to_mcp_dict()


def special_bi(z: str, derivative: int = 0, dps: int = 50, mode: str = "auto", certify: bool = False):
    return bi(z, derivative=derivative, dps=dps, mode=mode, certify=certify).to_mcp_dict()


def special_besselj(v: str, z: str, dps: int = 50, mode: str = "auto", certify: bool = False):
    return besselj(v, z, dps=dps, mode=mode, certify=certify).to_mcp_dict()


def special_bessely(v: str, z: str, dps: int = 50, mode: str = "auto", certify: bool = False):
    return bessely(v, z, dps=dps, mode=mode, certify=certify).to_mcp_dict()


def special_besseli(v: str, z: str, dps: int = 50, mode: str = "auto", certify: bool = False):
    return besseli(v, z, dps=dps, mode=mode, certify=certify).to_mcp_dict()


def special_besselk(v: str, z: str, dps: int = 50, mode: str = "auto", certify: bool = False):
    return besselk(v, z, dps=dps, mode=mode, certify=certify).to_mcp_dict()


def special_pbdv(v: str, x: str, dps: int = 50, mode: str = "auto", certify: bool = False):
    return pbdv(v, x, dps=dps, mode=mode, certify=certify).to_mcp_dict()


def special_pcfd(v: str, z: str, dps: int = 50, mode: str = "auto", certify: bool = False):
    return pcfd(v, z, dps=dps, mode=mode, certify=certify).to_mcp_dict()


def special_pcfu(a: str, z: str, dps: int = 50, mode: str = "auto", certify: bool = False):
    return pcfu(a, z, dps=dps, mode=mode, certify=certify).to_mcp_dict()


def special_pcfv(a: str, z: str, dps: int = 50, mode: str = "auto", certify: bool = False):
    return pcfv(a, z, dps=dps, mode=mode, certify=certify).to_mcp_dict()


def special_pcfw(a: str, z: str, dps: int = 50, mode: str = "auto", certify: bool = False):
    return pcfw(a, z, dps=dps, mode=mode, certify=certify).to_mcp_dict()


_MCP_TOOLS = (
    special_gamma,
    special_loggamma,
    special_rgamma,
    special_gamma_ratio,
    special_loggamma_ratio,
    special_beta,
    special_airy,
    special_ai,
    special_bi,
    special_besselj,
    special_bessely,
    special_besseli,
    special_besselk,
    special_pbdv,
    special_pcfd,
    special_pcfu,
    special_pcfv,
    special_pcfw,
)


def build_server():
    """Build a FastMCP server when the optional MCP SDK is installed."""

    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise ImportError("Install certsf[mcp] to run the MCP server.") from exc

    server = FastMCP("certsf")
    for tool in _MCP_TOOLS:
        server.tool()(tool)
    return server


if __name__ == "__main__":  # pragma: no cover - manual server entrypoint
    build_server().run()
