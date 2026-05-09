from pathlib import Path

import pytest

import certsf
from certsf.dispatcher import available_methods


ROOT = Path(__file__).resolve().parents[1]
AUDIT_FIELDS = (
    "Function:",
    "Target mathematical definition:",
    "Backend primitive or formula:",
    "Accepted domain:",
    "Excluded domain:",
    "Branch convention:",
    "Singularities:",
    "Validation identities:",
    "Reference equations:",
    "Known numerical risks:",
    "Certification status:",
)
AUDIT_FILES = (
    "gamma.md",
    "airy.md",
    "bessel.md",
    "parabolic_cylinder.md",
)
DIRECT_ARB_CLAIM = "certified Arb enclosure of the documented direct Arb primitive"
DIRECT_ARB_GAMMA_RATIO_CLAIM = (
    "certified Arb enclosure of Gamma(a) * rgamma(b) using direct Arb gamma primitives"
)
DIRECT_ARB_LOGGAMMA_RATIO_CLAIM = (
    "certified Arb enclosure of principal loggamma(a) - principal loggamma(b) using direct Arb gamma primitives"
)
FORMULA_CLAIM = "certified Arb enclosure of the implemented documented formula; formula audit in progress"


@pytest.mark.parametrize(
    ("function", "args"),
    [
        pytest.param(certsf.gamma, ("3.2",), id="gamma"),
        pytest.param(certsf.loggamma, ("3.2",), id="loggamma"),
        pytest.param(certsf.rgamma, ("3.2",), id="rgamma"),
        pytest.param(certsf.airy, ("1.0",), id="airy-real"),
        pytest.param(certsf.airy, ("1.0+0.25j",), id="airy-complex"),
        pytest.param(certsf.besselj, ("2", "4.0"), id="besselj-integer-real"),
        pytest.param(certsf.besselk, ("2.5", "4.0+0.5j"), id="besselk-real-order-complex"),
    ],
)
def test_direct_arb_certified_results_expose_audited_claim(function, args):
    result = function(*args, dps=60, mode="certified")
    if _backend_is_unavailable(result):
        pytest.skip(result.diagnostics["error"])

    assert result.certified is True
    assert result.diagnostics["certificate_level"] == "direct_arb_primitive"
    assert result.diagnostics["audit_status"] == "audited_direct"
    assert result.diagnostics["certification_claim"] == DIRECT_ARB_CLAIM


def test_gamma_ratio_certified_result_exposes_narrow_audited_claim():
    result = certsf.gamma_ratio("3.2", "1.2", dps=60, mode="certified")
    if _backend_is_unavailable(result):
        pytest.skip(result.diagnostics["error"])

    assert result.certified is True
    assert result.diagnostics["certificate_scope"] == "direct_arb_gamma_ratio"
    assert result.diagnostics["certificate_level"] == "direct_arb_primitive"
    assert result.diagnostics["audit_status"] == "audited_direct"
    assert result.diagnostics["certification_claim"] == DIRECT_ARB_GAMMA_RATIO_CLAIM


def test_loggamma_ratio_certified_result_exposes_narrow_audited_claim():
    result = certsf.loggamma_ratio("3.2", "1.2", dps=60, mode="certified")
    if _backend_is_unavailable(result):
        pytest.skip(result.diagnostics["error"])

    assert result.certified is True
    assert result.diagnostics["certificate_scope"] == "direct_arb_loggamma_ratio"
    assert result.diagnostics["certificate_level"] == "direct_arb_primitive"
    assert result.diagnostics["audit_status"] == "audited_direct"
    assert result.diagnostics["certification_claim"] == DIRECT_ARB_LOGGAMMA_RATIO_CLAIM


@pytest.mark.parametrize(
    ("function", "args", "expected_formula"),
    [
        pytest.param(certsf.pbdv, ("2.5", "1.25"), "pcfd_via_pcfu", id="pbdv"),
        pytest.param(certsf.pcfd, ("2.5", "1.25"), "pcfd_via_pcfu", id="pcfd"),
        pytest.param(certsf.pcfu, ("2.5", "1.25"), "pcfu_1f1_global", id="pcfu"),
        pytest.param(certsf.pcfv, ("2.5", "1.25"), "pcfv_dlmf_connection", id="pcfv"),
        pytest.param(certsf.pcfw, ("2.5", "1.25"), "pcfw_dlmf_12_14_real_connection", id="pcfw"),
    ],
)
def test_formula_certified_results_expose_experimental_audit_claim(function, args, expected_formula):
    result = function(*args, dps=60, mode="certified")
    if _backend_is_unavailable(result):
        pytest.skip(result.diagnostics["error"])

    assert result.certified is True
    assert result.diagnostics["formula"] == expected_formula
    assert result.diagnostics["certificate_level"] == "formula_audited_experimental"
    assert result.diagnostics["audit_status"] == "experimental_formula"
    assert result.diagnostics["certification_claim"] == FORMULA_CLAIM


def test_certification_audit_document_covers_dispatcher_certificate_scopes():
    audit_text = _doc_text("certification_audit.md")
    registry_scopes = {
        token
        for method in available_methods()
        if method.certified and method.certificate_scope is not None
        for token in method.certificate_scope.split("|")
    }

    missing = sorted(scope for scope in registry_scopes if f"`{scope}`" not in audit_text)
    assert missing == []


@pytest.mark.parametrize("audit_file", AUDIT_FILES)
def test_family_audit_checklists_use_required_review_template(audit_file):
    audit_text = _audit_doc_text(audit_file)

    missing = [field for field in AUDIT_FIELDS if field not in audit_text]
    assert missing == []


def test_family_audit_checklists_cover_current_public_certified_surface():
    audit_text = "\n".join(_audit_doc_text(name) for name in AUDIT_FILES)
    public_functions = set(certsf.__all__) - {"SFResult", "airyai", "airybi"}

    missing = sorted(function for function in public_functions if f"`{function}" not in audit_text)
    assert missing == []


def test_formula_audit_document_covers_runtime_formula_diagnostics():
    formula_text = _doc_text("formula_audit.md")
    expected_formulas = {
        "pcfd_via_pcfu",
        "pcfu_1f1_global",
        "pcfv_dlmf_connection",
        "pcfw_dlmf_12_14_real_connection",
    }

    missing = sorted(formula for formula in expected_formulas if f"`{formula}`" not in formula_text)
    assert missing == []


def _doc_text(name: str) -> str:
    return (ROOT / "docs" / name).read_text(encoding="utf-8")


def _audit_doc_text(name: str) -> str:
    return (ROOT / "docs" / "audit" / name).read_text(encoding="utf-8")


def _backend_is_unavailable(result):
    return not result.certified and "python-flint is not installed" in result.diagnostics.get("error", "")
