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
    "error_function.md",
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
DIRECT_ARB_BETA_CLAIM = (
    "certified Arb enclosure of Gamma(a) * Gamma(b) * rgamma(a+b) using direct Arb gamma primitives"
)
DIRECT_ARB_POCHHAMMER_CLAIM = (
    "certified Arb enclosure of finite product prod_{k=0}^{n-1}(a+k) for nonnegative integer n"
)
DIRECT_ARB_ERF_CLAIM = "certified Arb enclosure of erf(z) using direct Arb error-function primitive"
DIRECT_ARB_ERFC_CLAIM = (
    "certified Arb enclosure of erfc(z) using direct Arb complementary error-function primitive"
)
DIRECT_ARB_ERFCX_CLAIM = (
    "certified Arb enclosure of erfcx(z) using direct Arb scaled complementary error-function primitive"
)
DIRECT_ARB_ERFI_CLAIM = "certified Arb enclosure of erfi(z) using direct Arb imaginary error-function primitive"
DIRECT_ARB_DAWSON_CLAIM = "certified Arb enclosure of dawson(z) using direct Arb Dawson primitive"
DIRECT_ARB_ERFINV_CLAIM = (
    "certified Arb enclosure of real principal erfinv(x) using direct Arb inverse error-function primitive"
)
DIRECT_ARB_ERFCINV_CLAIM = (
    "certified Arb enclosure of real principal erfcinv(x) using direct Arb inverse complementary error-function primitive"
)
ARB_ERFCX_FORMULA_CLAIM = "certified Arb enclosure of exp(z^2)*erfc(z)"
ARB_ERFI_FORMULA_CLAIM = "certified Arb enclosure of -i*erf(i*z)"
ARB_DAWSON_FORMULA_CLAIM = "certified Arb enclosure of sqrt(pi)/2*exp(-z^2)*erfi(z)"
ARB_ERFINV_REAL_ROOT_CLAIM = "certified real root enclosure for erf(y)-x=0 using monotonicity of real erf"
ARB_ERFCINV_VIA_ERFINV_CLAIM = (
    "certified real inverse enclosure for erfcinv(x)=erfinv(1-x) using monotonicity of real erfc"
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


def test_beta_certified_result_exposes_narrow_audited_claim():
    result = certsf.beta("3.2", "1.2", dps=60, mode="certified")
    if _backend_is_unavailable(result):
        pytest.skip(result.diagnostics["error"])

    assert result.certified is True
    assert result.diagnostics["certificate_scope"] == "direct_arb_beta"
    assert result.diagnostics["certificate_level"] == "direct_arb_primitive"
    assert result.diagnostics["audit_status"] == "audited_direct"
    assert result.diagnostics["certification_claim"] == DIRECT_ARB_BETA_CLAIM


def test_pochhammer_certified_result_exposes_narrow_audited_claim():
    result = certsf.pochhammer("3.2", "4", dps=60, mode="certified")
    if _backend_is_unavailable(result):
        pytest.skip(result.diagnostics["error"])

    assert result.certified is True
    assert result.diagnostics["certificate_scope"] == "direct_arb_pochhammer_product"
    assert result.diagnostics["certificate_level"] == "direct_arb_finite_product"
    assert result.diagnostics["audit_status"] == "audited_direct"
    assert result.diagnostics["certification_claim"] == DIRECT_ARB_POCHHAMMER_CLAIM


@pytest.mark.parametrize(
    ("function", "args", "scope", "claim"),
    [
        pytest.param(certsf.erf, ("1",), "direct_arb_erf", DIRECT_ARB_ERF_CLAIM, id="erf"),
        pytest.param(certsf.erfc, ("1",), "direct_arb_erfc", DIRECT_ARB_ERFC_CLAIM, id="erfc"),
    ],
)
def test_error_function_certified_results_expose_narrow_audited_claim(function, args, scope, claim):
    result = function(*args, dps=60, mode="certified")
    if _backend_is_unavailable(result):
        pytest.skip(result.diagnostics["error"])

    assert result.certified is True
    assert result.diagnostics["certificate_scope"] == scope
    assert result.diagnostics["certificate_level"] == "direct_arb_primitive"
    assert result.diagnostics["audit_status"] == "audited_direct"
    assert result.diagnostics["certification_claim"] == claim


@pytest.mark.parametrize(
    ("function", "direct_scope", "direct_claim", "formula_scope", "formula_claim", "formula"),
    [
        pytest.param(
            certsf.erfcx,
            "direct_arb_erfcx",
            DIRECT_ARB_ERFCX_CLAIM,
            "arb_erfcx_formula",
            ARB_ERFCX_FORMULA_CLAIM,
            "exp(z^2)*erfc(z)",
            id="erfcx",
        ),
        pytest.param(
            certsf.erfi,
            "direct_arb_erfi",
            DIRECT_ARB_ERFI_CLAIM,
            "arb_erfi_formula",
            ARB_ERFI_FORMULA_CLAIM,
            "-i*erf(i*z)",
            id="erfi",
        ),
        pytest.param(
            certsf.dawson,
            "direct_arb_dawson",
            DIRECT_ARB_DAWSON_CLAIM,
            "arb_dawson_formula",
            ARB_DAWSON_FORMULA_CLAIM,
            "sqrt(pi)/2*exp(-z^2)*erfi(z)",
            id="dawson",
        ),
    ],
)
def test_error_function_formula_wrappers_expose_direct_or_formula_claim(
    function,
    direct_scope,
    direct_claim,
    formula_scope,
    formula_claim,
    formula,
):
    result = function("1", dps=60, mode="certified")
    if _backend_is_unavailable(result):
        pytest.skip(result.diagnostics["error"])

    assert result.certified is True
    assert result.diagnostics["certificate_scope"] in {direct_scope, formula_scope}
    if result.diagnostics["certificate_scope"] == direct_scope:
        assert result.diagnostics["certificate_level"] == "direct_arb_primitive"
        assert result.diagnostics["audit_status"] == "audited_direct"
        assert result.diagnostics["certification_claim"] == direct_claim
    else:
        assert result.diagnostics["certificate_level"] == "formula_audited_alpha"
        assert result.diagnostics["audit_status"] == "formula_identity"
        assert result.diagnostics["certification_claim"] == formula_claim
        assert result.diagnostics["formula"] == formula


def test_erfinv_certified_result_exposes_narrow_inverse_claim():
    result = certsf.erfinv("0.5", dps=60, mode="certified")
    if _backend_is_unavailable(result):
        pytest.skip(result.diagnostics["error"])

    assert result.certified is True
    assert result.diagnostics["certificate_scope"] in {"direct_arb_erfinv", "arb_erfinv_real_root"}
    assert result.diagnostics["domain"] == "real_x_in_open_interval_minus1_1"
    if result.diagnostics["certificate_scope"] == "direct_arb_erfinv":
        assert result.diagnostics["certificate_level"] == "direct_arb_primitive"
        assert result.diagnostics["audit_status"] == "audited_direct"
        assert result.diagnostics["certification_claim"] == DIRECT_ARB_ERFINV_CLAIM
    else:
        assert result.diagnostics["certificate_level"] == "certified_real_root"
        assert result.diagnostics["audit_status"] == "monotone_real_inverse"
        assert result.diagnostics["certification_claim"] == ARB_ERFINV_REAL_ROOT_CLAIM
        assert result.diagnostics["formula"] == "erf(y)-x=0"


def test_erfcinv_certified_result_exposes_narrow_inverse_claim():
    result = certsf.erfcinv("0.5", dps=60, mode="certified")
    if _backend_is_unavailable(result):
        pytest.skip(result.diagnostics["error"])

    assert result.certified is True
    assert result.diagnostics["certificate_scope"] in {"direct_arb_erfcinv", "arb_erfcinv_via_erfinv"}
    assert result.diagnostics["domain"] == "real_x_in_open_interval_0_2"
    if result.diagnostics["certificate_scope"] == "direct_arb_erfcinv":
        assert result.diagnostics["certificate_level"] == "direct_arb_primitive"
        assert result.diagnostics["audit_status"] == "audited_direct"
        assert result.diagnostics["certification_claim"] == DIRECT_ARB_ERFCINV_CLAIM
    else:
        assert result.diagnostics["certificate_level"] == "certified_real_root"
        assert result.diagnostics["audit_status"] == "monotone_real_inverse"
        assert result.diagnostics["certification_claim"] == ARB_ERFCINV_VIA_ERFINV_CLAIM
        assert result.diagnostics["formula"] == "erfinv(1-x)"


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
