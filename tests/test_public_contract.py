import dataclasses
import json

import certsf
from certsf import SFResult
from certsf import mcp_server


EXPECTED_PUBLIC_NAMES = (
    "SFResult",
    "ai",
    "airyai",
    "airy",
    "airybi",
    "bi",
    "besseli",
    "besselj",
    "besselk",
    "bessely",
    "beta",
    "erf",
    "erfc",
    "erfcx",
    "erfi",
    "dawson",
    "erfinv",
    "erfcinv",
    "gamma",
    "gamma_ratio",
    "loggamma",
    "loggamma_ratio",
    "pochhammer",
    "rgamma",
    "pbdv",
    "pcfd",
    "pcfu",
    "pcfv",
    "pcfw",
)

EXPECTED_RESULT_FIELDS = (
    "value",
    "abs_error_bound",
    "rel_error_bound",
    "certified",
    "function",
    "method",
    "backend",
    "requested_dps",
    "working_dps",
    "terms_used",
    "diagnostics",
)

EXPECTED_MCP_TOOL_NAMES = (
    "special_gamma",
    "special_loggamma",
    "special_rgamma",
    "special_gamma_ratio",
    "special_loggamma_ratio",
    "special_beta",
    "special_pochhammer",
    "special_erf",
    "special_erfc",
    "special_erfcx",
    "special_erfi",
    "special_dawson",
    "special_erfinv",
    "special_erfcinv",
    "special_airy",
    "special_ai",
    "special_bi",
    "special_besselj",
    "special_bessely",
    "special_besseli",
    "special_besselk",
    "special_pbdv",
    "special_pcfd",
    "special_pcfu",
    "special_pcfv",
    "special_pcfw",
)


def test_review_public_imports_remain_clean():
    from certsf import besseli, besselj, besselk, bessely
    from certsf import SFResult as ImportedResult
    from certsf import ai, airy, beta, bi, dawson, erf, erfc, erfcinv, erfcx, erfi, erfinv
    from certsf import gamma, gamma_ratio, loggamma, loggamma_ratio, pochhammer, rgamma
    from certsf import pbdv, pcfd, pcfu, pcfv, pcfw

    imported_functions = (
        gamma,
        gamma_ratio,
        loggamma,
        loggamma_ratio,
        rgamma,
        beta,
        dawson,
        erf,
        erfc,
        erfcinv,
        erfcx,
        erfi,
        erfinv,
        pochhammer,
        airy,
        ai,
        bi,
        besselj,
        bessely,
        besseli,
        besselk,
        pbdv,
        pcfd,
        pcfu,
        pcfv,
        pcfw,
    )
    assert ImportedResult is SFResult
    assert all(callable(function) for function in imported_functions)


def test_package_exports_are_small_and_explicit():
    assert tuple(certsf.__all__) == EXPECTED_PUBLIC_NAMES
    assert certsf.airyai is certsf.ai
    assert certsf.airybi is certsf.bi


def test_sfresult_fields_are_stable():
    assert tuple(field.name for field in dataclasses.fields(SFResult)) == EXPECTED_RESULT_FIELDS


def test_representative_public_calls_return_sfresult():
    cases = [
        (certsf.beta, ("2", "3")),
        (certsf.gamma, ("3.2",)),
        (certsf.gamma_ratio, ("3.2", "1.2")),
        (certsf.loggamma, ("3.2",)),
        (certsf.loggamma_ratio, ("3.2", "1.2")),
        (certsf.pochhammer, ("3", "4")),
        (certsf.dawson, ("1",)),
        (certsf.erf, ("1",)),
        (certsf.erfc, ("1",)),
        (certsf.erfcinv, ("0.5",)),
        (certsf.erfcx, ("1",)),
        (certsf.erfi, ("1",)),
        (certsf.erfinv, ("0.5",)),
        (certsf.rgamma, ("3.2",)),
        (certsf.airy, ("1.0",)),
        (certsf.ai, ("1.0",)),
        (certsf.bi, ("1.0",)),
        (certsf.besselj, ("2", "4.0")),
        (certsf.bessely, ("2", "4.0")),
        (certsf.besseli, ("2", "4.0")),
        (certsf.besselk, ("2", "4.0")),
        (certsf.pbdv, ("2.5", "1.25")),
        (certsf.pcfd, ("2.5", "1.25")),
        (certsf.pcfu, ("2.5", "1.25")),
        (certsf.pcfv, ("2.5", "1.25")),
        (certsf.pcfw, ("2.5", "1.25")),
    ]

    for function, args in cases:
        assert isinstance(function(*args, mode="fast"), SFResult)


def test_mode_semantics_are_stable():
    fast = certsf.gamma("3.2", dps=12, mode="auto")
    high_precision = certsf.gamma("3.2", dps=50, mode="auto")
    certified = certsf.gamma("3.2", dps=50, mode="auto", certify=True)

    assert fast.backend == "scipy"
    assert fast.method == "scipy.special"
    assert fast.certified is False
    assert high_precision.backend == "mpmath"
    assert high_precision.method == "mpmath"
    assert high_precision.certified is False
    assert certified.backend == "python-flint"
    assert certified.diagnostics["mode"] == "certified"


def test_certified_failure_behavior_is_clean_and_non_certified():
    result = certsf.gamma("0", dps=50, mode="certified")

    assert result.certified is False
    assert result.value == ""
    assert result.abs_error_bound is None
    assert result.rel_error_bound is None
    assert result.diagnostics["mode"] == "certified"
    assert "error" in result.diagnostics


def test_python_api_keeps_string_serialization_policy():
    scalar = certsf.gamma("3.2", mode="high_precision")
    airy = certsf.airy("1.0", mode="high_precision")
    pbdv = certsf.pbdv("2.5", "1.25", mode="high_precision")

    assert isinstance(scalar.value, str)
    assert isinstance(airy.value, str)
    assert isinstance(pbdv.value, str)
    assert json.loads(scalar.to_json()) == scalar.to_dict()


def test_python_multi_component_json_payloads_are_stable():
    airy = certsf.airy("1.0", mode="high_precision")
    pbdv = certsf.pbdv("2.5", "1.25", mode="high_precision")

    assert set(airy.value_as_dict()) == {"ai", "aip", "bi", "bip"}
    assert set(pbdv.value_as_dict()) == {"value", "derivative"}


def test_mcp_tool_names_and_nested_payloads_are_stable():
    assert tuple(tool.__name__ for tool in mcp_server._MCP_TOOLS) == EXPECTED_MCP_TOOL_NAMES

    airy_payload = mcp_server.special_airy("1.0", mode="high_precision")
    pbdv_payload = mcp_server.special_pbdv("2.5", "1.25", mode="high_precision")
    assert set(airy_payload["value"]) == {"ai", "aip", "bi", "bip"}
    assert set(pbdv_payload["value"]) == {"value", "derivative"}
