import pytest

import certsf


SUPPORTED_CERTIFIED_CASES = [
    pytest.param(certsf.gamma, ("3.2",), id="gamma"),
    pytest.param(certsf.loggamma, ("3.2",), id="loggamma"),
    pytest.param(certsf.rgamma, ("3.2",), id="rgamma"),
    pytest.param(certsf.gamma_ratio, ("3.2", "1.2"), id="gamma_ratio"),
    pytest.param(certsf.airy, ("1.0",), id="airy"),
    pytest.param(certsf.ai, ("1.0",), id="ai"),
    pytest.param(certsf.bi, ("1.0",), id="bi"),
    pytest.param(certsf.besselj, ("2", "4.0"), id="besselj"),
    pytest.param(certsf.bessely, ("2", "4.0"), id="bessely"),
    pytest.param(certsf.besseli, ("2", "4.0"), id="besseli"),
    pytest.param(certsf.besselk, ("2", "4.0"), id="besselk"),
    pytest.param(certsf.pbdv, ("2.5", "1.25"), id="pbdv"),
    pytest.param(certsf.pcfd, ("2.5", "1.25"), id="pcfd"),
    pytest.param(certsf.pcfu, ("2.5", "1.25"), id="pcfu"),
    pytest.param(certsf.pcfv, ("2.5", "1.25"), id="pcfv"),
    pytest.param(certsf.pcfw, ("2.5", "1.25"), id="pcfw"),
]


UNSUPPORTED_CERTIFIED_CASES = [
    pytest.param(certsf.gamma, ("0",), id="gamma-pole"),
    pytest.param(certsf.gamma_ratio, ("0", "3.2"), id="gamma-ratio-numerator-pole"),
    pytest.param(certsf.gamma_ratio, ("0", "0"), id="gamma-ratio-both-poles"),
    pytest.param(certsf.loggamma, ("-2",), id="loggamma-pole"),
    pytest.param(certsf.bessely, ("2.5+1j", "4.0"), id="bessel-complex-order"),
    pytest.param(certsf.pcfu, ("2.5+1j", "1.25"), id="pcf-complex-parameter"),
    pytest.param(certsf.pcfw, ("2.5", "1.25+0.5j"), id="pcfw-complex-argument"),
]


@pytest.mark.parametrize(("function", "args"), SUPPORTED_CERTIFIED_CASES)
def test_every_certified_result_has_required_claim_metadata(function, args):
    result = function(*args, dps=50, mode="certified")
    if _backend_is_unavailable(result):
        pytest.skip(result.diagnostics["error"])

    assert result.certified is True
    assert result.backend == "python-flint"
    assert result.abs_error_bound is not None
    assert "certificate_scope" in result.diagnostics
    assert "certificate_level" in result.diagnostics
    assert "audit_status" in result.diagnostics
    assert "certification_claim" in result.diagnostics
    assert result.value != ""


@pytest.mark.parametrize(("function", "args"), UNSUPPORTED_CERTIFIED_CASES)
def test_unsupported_certified_domains_are_clean_failures(function, args):
    result = function(*args, dps=50, mode="certified")

    assert result.certified is False
    assert result.value == ""
    assert "error" in result.diagnostics


def test_gamma_family_records_direct_arb_primitive_scope():
    for function in (certsf.gamma, certsf.loggamma, certsf.rgamma):
        result = function("3.2", dps=50, mode="certified")
        if _backend_is_unavailable(result):
            pytest.skip(result.diagnostics["error"])

        assert result.diagnostics["certificate_scope"] == "direct_arb_primitive"


def test_gamma_ratio_records_narrow_direct_arb_scope():
    result = certsf.gamma_ratio("3.2", "1.2", dps=50, mode="certified")
    if _backend_is_unavailable(result):
        pytest.skip(result.diagnostics["error"])

    assert result.diagnostics["certificate_scope"] == "direct_arb_gamma_ratio"
    assert result.diagnostics["certificate_level"] == "direct_arb_primitive"
    assert result.diagnostics["audit_status"] == "audited_direct"


@pytest.mark.parametrize(
    ("function", "expected_formula", "expected_scope"),
    [
        pytest.param(certsf.pbdv, "pcfd_via_pcfu", "phase7_hypergeometric_parabolic_cylinder", id="pbdv"),
        pytest.param(certsf.pcfd, "pcfd_via_pcfu", "phase7_hypergeometric_parabolic_cylinder", id="pcfd"),
        pytest.param(certsf.pcfu, "pcfu_1f1_global", "phase7_hypergeometric_parabolic_cylinder", id="pcfu"),
        pytest.param(certsf.pcfv, "pcfv_dlmf_connection", "phase8_parabolic_cylinder_connections", id="pcfv"),
        pytest.param(certsf.pcfw, "pcfw_dlmf_12_14_real_connection", "phase8_parabolic_cylinder_connections", id="pcfw"),
    ],
)
def test_parabolic_cylinder_certified_results_keep_formula_audit_visible(
    function,
    expected_formula,
    expected_scope,
):
    result = function("2.5", "1.25", dps=50, mode="certified")
    if _backend_is_unavailable(result):
        pytest.skip(result.diagnostics["error"])

    assert result.diagnostics["formula"] == expected_formula
    assert result.diagnostics["certificate_scope"] == expected_scope


def _backend_is_unavailable(result):
    return not result.certified and "python-flint is not installed" in result.diagnostics.get("error", "")
