"""Thin optional MCP wrapper for the certsf public API."""

from __future__ import annotations

from .functions.airy import ai, airy, bi
from .functions.bessel import besseli, besselj, besselk, bessely
from .functions.error_function import dawson, erf, erfc, erfcinv, erfcx, erfi, erfinv
from .functions.gamma import beta, gamma, gamma_ratio, loggamma, loggamma_ratio, pochhammer, rgamma
from .functions.parabolic_cylinder import pbdv, pcfd, pcfu, pcfv, pcfw


def special_gamma(z: str, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return gamma(z, dps=dps, mode=mode, certify=certify, method=method).to_mcp_dict()


def special_loggamma(z: str, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return loggamma(z, dps=dps, mode=mode, certify=certify, method=method).to_mcp_dict()


def special_rgamma(z: str, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return rgamma(z, dps=dps, mode=mode, certify=certify, method=method).to_mcp_dict()


def special_gamma_ratio(
    a: str,
    b: str,
    dps: int = 50,
    mode: str = "auto",
    certify: bool = False,
    method: str | None = None,
):
    return gamma_ratio(a, b, dps=dps, mode=mode, certify=certify, method=method).to_mcp_dict()


def special_loggamma_ratio(
    a: str,
    b: str,
    dps: int = 50,
    mode: str = "auto",
    certify: bool = False,
    method: str | None = None,
):
    return loggamma_ratio(a, b, dps=dps, mode=mode, certify=certify, method=method).to_mcp_dict()


def special_beta(a: str, b: str, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return beta(a, b, dps=dps, mode=mode, certify=certify, method=method).to_mcp_dict()


def special_pochhammer(
    a: str,
    n: str,
    dps: int = 50,
    mode: str = "auto",
    certify: bool = False,
    method: str | None = None,
):
    return pochhammer(a, n, dps=dps, mode=mode, certify=certify, method=method).to_mcp_dict()


def special_erf(z: str, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return erf(z, dps=dps, mode=mode, certify=certify, method=method).to_mcp_dict()


def special_erfc(z: str, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return erfc(z, dps=dps, mode=mode, certify=certify, method=method).to_mcp_dict()


def special_erfcx(z: str, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return erfcx(z, dps=dps, mode=mode, certify=certify, method=method).to_mcp_dict()


def special_erfi(z: str, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return erfi(z, dps=dps, mode=mode, certify=certify, method=method).to_mcp_dict()


def special_dawson(z: str, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return dawson(z, dps=dps, mode=mode, certify=certify, method=method).to_mcp_dict()


def special_erfinv(x: str, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return erfinv(x, dps=dps, mode=mode, certify=certify, method=method).to_mcp_dict()


def special_erfcinv(x: str, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return erfcinv(x, dps=dps, mode=mode, certify=certify, method=method).to_mcp_dict()


def special_airy(z: str, dps: int = 50, mode: str = "auto", certify: bool = False, method: str | None = None):
    return airy(z, dps=dps, mode=mode, certify=certify, method=method).to_mcp_dict()


def special_ai(
    z: str,
    derivative: int = 0,
    dps: int = 50,
    mode: str = "auto",
    certify: bool = False,
    method: str | None = None,
):
    return ai(z, derivative=derivative, dps=dps, mode=mode, certify=certify, method=method).to_mcp_dict()


def special_bi(
    z: str,
    derivative: int = 0,
    dps: int = 50,
    mode: str = "auto",
    certify: bool = False,
    method: str | None = None,
):
    return bi(z, derivative=derivative, dps=dps, mode=mode, certify=certify, method=method).to_mcp_dict()


def special_besselj(
    v: str,
    z: str,
    dps: int = 50,
    mode: str = "auto",
    certify: bool = False,
    method: str | None = None,
):
    return besselj(v, z, dps=dps, mode=mode, certify=certify, method=method).to_mcp_dict()


def special_bessely(
    v: str,
    z: str,
    dps: int = 50,
    mode: str = "auto",
    certify: bool = False,
    method: str | None = None,
):
    return bessely(v, z, dps=dps, mode=mode, certify=certify, method=method).to_mcp_dict()


def special_besseli(
    v: str,
    z: str,
    dps: int = 50,
    mode: str = "auto",
    certify: bool = False,
    method: str | None = None,
):
    return besseli(v, z, dps=dps, mode=mode, certify=certify, method=method).to_mcp_dict()


def special_besselk(
    v: str,
    z: str,
    dps: int = 50,
    mode: str = "auto",
    certify: bool = False,
    method: str | None = None,
):
    return besselk(v, z, dps=dps, mode=mode, certify=certify, method=method).to_mcp_dict()


def special_pbdv(
    v: str,
    x: str,
    dps: int = 50,
    mode: str = "auto",
    certify: bool = False,
    method: str | None = None,
):
    return pbdv(v, x, dps=dps, mode=mode, certify=certify, method=method).to_mcp_dict()


def special_pcfd(
    v: str,
    z: str,
    dps: int = 50,
    mode: str = "auto",
    certify: bool = False,
    method: str | None = None,
):
    return pcfd(v, z, dps=dps, mode=mode, certify=certify, method=method).to_mcp_dict()


def special_pcfu(
    a: str,
    z: str,
    dps: int = 50,
    mode: str = "auto",
    certify: bool = False,
    method: str | None = None,
):
    return pcfu(a, z, dps=dps, mode=mode, certify=certify, method=method).to_mcp_dict()


def special_pcfv(
    a: str,
    z: str,
    dps: int = 50,
    mode: str = "auto",
    certify: bool = False,
    method: str | None = None,
):
    return pcfv(a, z, dps=dps, mode=mode, certify=certify, method=method).to_mcp_dict()


def special_pcfw(
    a: str,
    z: str,
    dps: int = 50,
    mode: str = "auto",
    certify: bool = False,
    method: str | None = None,
):
    return pcfw(a, z, dps=dps, mode=mode, certify=certify, method=method).to_mcp_dict()


_MCP_TOOLS = (
    special_gamma,
    special_loggamma,
    special_rgamma,
    special_gamma_ratio,
    special_loggamma_ratio,
    special_beta,
    special_pochhammer,
    special_erf,
    special_erfc,
    special_erfcx,
    special_erfi,
    special_dawson,
    special_erfinv,
    special_erfcinv,
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
