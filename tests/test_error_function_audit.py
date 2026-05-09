from pathlib import Path
import json

import pytest

import certsf
from certsf import mcp_server
from certsf.backends import arb_backend
from certsf.dispatcher import REGISTRY


ROOT = Path(__file__).resolve().parents[1]

ERROR_FUNCTIONS = ("erf", "erfc", "erfcx", "erfi", "dawson")
SAMPLE_ARGS = {
    "erf": ("0.5+0.25j",),
    "erfc": ("0.5+0.25j",),
    "erfcx": ("0.5+0.25j",),
    "erfi": ("0.5+0.25j",),
    "dawson": ("0.5+0.25j",),
}
CERTIFIED_SCOPES = {
    "erf": "direct_arb_erf",
    "erfc": "direct_arb_erfc",
    "erfcx": "direct_arb_erfcx|arb_erfcx_formula",
    "erfi": "direct_arb_erfi|arb_erfi_formula",
    "dawson": "direct_arb_dawson|arb_dawson_formula",
}
UNSUPPORTED_CERTIFIED_CASES = (
    ("erf", ("nan",)),
    ("erfc", ("nan",)),
    ("erfcx", ("nan",)),
    ("erfi", ("nan",)),
    ("dawson", ("nan",)),
)
FORBIDDEN_ERROR_FUNCTION_WRAPPERS = (
    "erfinv",
    "erfcinv",
    "faddeeva",
    "plasma_dispersion",
    "plasma_dispersion_function",
    "wofz",
)
DOC_EXPECTATIONS = {
    "README.md": (
        "| `erf`, `erfc`, `erfcx`, `erfi`, `dawson` | alpha-certified, direct Arb error-function primitives plus erfcx, erfi, and dawson identity formulas |",
        "Certified `erf`, `erfc`, and `erfi` use direct Arb error-function primitives",
        "Certified `erfcx` prefers direct Arb `erfcx` when available",
        "Certified `erfi` prefers direct Arb `erfi` when available",
        "Certified `dawson` prefers direct Arb `dawson` when available",
        "`erfc` may evaluate `1 - erf(z)` and records `formula=\"1-erf\"`.",
        "`formula=\"exp(z^2)*erfc(z)\"`.",
        "`formula=\"-i*erf(i*z)\"`.",
        "`formula=\"sqrt(pi)/2*exp(-z^2)*erfi(z)\"`.",
        "No custom asymptotic certification is added.",
        "[`docs/error_function.md`](docs/error_function.md)",
        "[`docs/dawson.md`](docs/dawson.md)",
    ),
    "docs/error_function.md": (
        "erf(z) = 2/sqrt(pi) * integral_0^z exp(-t^2) dt",
        "erfc(z) = 1 - erf(z)",
        "erfcx(z) = exp(z^2) erfc(z)",
        "erfi(z) = -i erf(i z)",
        "dawson(z) = sqrt(pi)/2 * exp(-z^2) * erfi(z)",
        "direct Arb `erf` and `erfc` primitives",
        "record `diagnostics[\"formula\"] == \"1-erf\"`",
        "records `diagnostics[\"formula\"] == \"exp(z^2)*erfc(z)\"`",
        "records `diagnostics[\"formula\"] == \"-i*erf(i*z)\"`",
        "records `diagnostics[\"formula\"] == \"sqrt(pi)/2*exp(-z^2)*erfi(z)\"`",
        "`erfinv`, `erfcinv`, or Faddeeva functions",
        "No Taylor, asymptotic, or custom certification method",
    ),
    "docs/dawson.md": (
        "dawson(z) = sqrt(pi)/2 * exp(-z^2) * erfi(z)",
        "direct Arb `dawson` primitive",
        "`certificate_scope=\"arb_dawson_formula\"`",
        "`certification_claim=\"certified Arb enclosure of sqrt(pi)/2*exp(-z^2)*erfi(z)\"`",
        "`diagnostics[\"formula\"] == \"sqrt(pi)/2*exp(-z^2)*erfi(z)\"`",
    ),
    "docs/audit/error_function.md": (
        "Last reviewed: 2026-05-10.",
        "Direct Arb error-function primitives",
        "`1 - erf(z)` and records `formula=\"1-erf\"`",
        "`erfcx(z) = exp(z^2) erfc(z)`",
        "`formula=\"exp(z^2)*erfc(z)\"`",
        "`erfi(z) = -i erf(i z)`",
        "`formula=\"-i*erf(i*z)\"`",
        "`dawson(z) = sqrt(pi)/2 * exp(-z^2) * erfi(z)`",
        "`formula=\"sqrt(pi)/2*exp(-z^2)*erfi(z)\"`",
        "No `erfinv`, `erfcinv`",
        "Faddeeva wrapper",
        "No custom asymptotic or Taylor certification path",
        "`pypi-smoke.yml` defaults to `0.2.0a8`",
        "certified `special_erf`",
        "`special_erfcx`, `special_erfi`, and",
        "`special_dawson` calls in the MCP-certified",
        "This audit found no implementation inconsistency",
        "Release infrastructure remains unchanged",
        "Current v0.2 audit result:",
        "No public API, dispatcher, backend formula, MCP, or certified-scope",
    ),
    "docs/certification_audit.md": (
        "`direct_arb_erf` | `erf` | `direct_arb_primitive`",
        "`direct_arb_erfc` | `erfc` | `direct_arb_primitive`",
        "`direct_arb_erfcx` | `erfcx` | `direct_arb_primitive`",
        "`arb_erfcx_formula` | `erfcx` | `formula_audited_alpha`",
        "`direct_arb_erfi` | `erfi` | `direct_arb_primitive`",
        "`arb_erfi_formula` | `erfi` | `formula_audited_alpha`",
        "`direct_arb_dawson` | `dawson` | `direct_arb_primitive`",
        "`arb_dawson_formula` | `dawson` | `formula_audited_alpha`",
        "diagnostics record",
        "`formula=\"1-erf\"`",
        "`formula=\"exp(z^2)*erfc(z)\"`",
        "`formula=\"-i*erf(i*z)\"`",
        "`formula=\"sqrt(pi)/2*exp(-z^2)*erfi(z)\"`",
    ),
    "docs/certified_scope_0_2_0.md": (
        "Error-function family | `erf`, `erfc`, `erfcx`, `erfi`, `dawson`",
        "`erf(z)` and `erfc(z)` are the v0.2.0-alpha.5",
        "`erfcx(z)` is the v0.2.0-alpha.6 feature-branch API expansion.",
        "`erfi(z)` is the v0.2.0-alpha.7 feature-branch API expansion.",
        "`dawson(z)` is the v0.2.0-alpha.8 feature-branch API expansion.",
        "certified `erfc` may use `1 - erf(z)` and must record `formula=\"1-erf\"`",
        "otherwise certified `erfcx` may use",
        "otherwise certified `erfi` may use `-i*erf(i*z)`",
        "otherwise certified `dawson` may use `sqrt(pi)/2*exp(-z^2)*erfi(z)`",
        "Custom Taylor, asymptotic, or non-Arb certification methods are outside",
        "Parabolic-cylinder family",
        "experimental certified formula layer",
    ),
    "docs/release_claims.md": (
        "Error-function family | alpha-certified, direct Arb error-function primitives plus erfcx, erfi, and dawson identity formulas",
        "direct Arb `erfc` is preferred",
        "direct Arb `erfcx` is",
        "direct Arb `erfi` is",
        "`dawson` is defined as `sqrt(pi)/2 * exp(-z^2) * erfi(z)`",
        "fallback must be visible in diagnostics",
        "Do not claim `erfinv`, `erfcinv`, Faddeeva",
        "Do not describe the parabolic-cylinder family as certified without the",
    ),
    "docs/release-0.2.0-alpha.7.md": (
        "The release-planning PR was metadata and documentation only.",
        "Before publication, the PyPI smoke workflow continued to target `0.2.0a6`.",
        "After post-release verification, `pypi-smoke.yml` targets `0.2.0a7`",
        "[`post_release_verification.md`](post_release_verification.md)",
    ),
    "docs/release-0.2.0-alpha.8.md": (
        "The release-planning PR is metadata and documentation only.",
        "Before publication, the PyPI smoke workflow continued to target `0.2.0a7`.",
        "After post-release verification, `pypi-smoke.yml` targets `0.2.0a8`",
        "certified MCP `special_dawson` smoke calls",
        "[`post_release_verification.md`](post_release_verification.md)",
    ),
}


def test_error_function_public_api_dispatcher_and_mcp_are_in_lockstep():
    mcp_tool_names = {tool.__name__ for tool in mcp_server._MCP_TOOLS}

    for name in ERROR_FUNCTIONS:
        assert hasattr(certsf, name)
        assert name in certsf.__all__
        assert name in REGISTRY
        assert tuple(REGISTRY[name]) == ("fast", "high_precision", "certified")
        assert REGISTRY[name]["certified"].certificate_scope == CERTIFIED_SCOPES[name]
        assert f"special_{name}" in mcp_tool_names
        assert callable(getattr(mcp_server, f"special_{name}"))

    for name in FORBIDDEN_ERROR_FUNCTION_WRAPPERS:
        assert not hasattr(certsf, name)
        assert name not in certsf.__all__
        assert name not in REGISTRY
        assert not hasattr(mcp_server, f"special_{name}")


@pytest.mark.parametrize("name", ERROR_FUNCTIONS)
def test_error_function_mcp_tools_match_python_api(name):
    args = SAMPLE_ARGS[name]
    wrapper = getattr(certsf, name)
    tool = getattr(mcp_server, f"special_{name}")

    assert tool(*args, dps=50, mode="high_precision") == wrapper(
        *args,
        dps=50,
        mode="high_precision",
    ).to_mcp_dict()


@pytest.mark.parametrize("name", ERROR_FUNCTIONS)
@pytest.mark.parametrize("mode", ("fast", "high_precision", "certified", "auto"))
def test_error_function_public_wrappers_return_sfresult_in_every_mode(name, mode):
    result = getattr(certsf, name)("1", dps=40, mode=mode)

    assert isinstance(result, certsf.SFResult)
    assert result.function == name


@pytest.mark.parametrize("name", ERROR_FUNCTIONS)
@pytest.mark.parametrize("mode", ("fast", "high_precision", "certified"))
def test_error_function_mcp_tools_match_python_api_in_every_concrete_mode(name, mode):
    args = SAMPLE_ARGS[name]
    wrapper = getattr(certsf, name)
    tool = getattr(mcp_server, f"special_{name}")
    result = wrapper(*args, dps=50, mode=mode)
    if mode == "certified" and _backend_is_unavailable(result):
        pytest.skip(result.diagnostics["error"])

    assert tool(*args, dps=50, mode=mode) == result.to_mcp_dict()


@pytest.mark.parametrize("name", ERROR_FUNCTIONS)
def test_error_function_certified_scopes_match_audit(name):
    result = getattr(certsf, name)("1", dps=50, mode="certified")
    if _backend_is_unavailable(result):
        pytest.skip(result.diagnostics["error"])

    assert result.certified is True
    assert result.backend == "python-flint"
    assert result.method == "arb_ball"
    assert result.diagnostics["certificate_scope"] in CERTIFIED_SCOPES[name].split("|")
    if result.diagnostics["certificate_scope"] == "arb_erfcx_formula":
        assert result.diagnostics["certificate_level"] == "formula_audited_alpha"
        assert result.diagnostics["audit_status"] == "formula_identity"
        assert result.diagnostics["certification_claim"] == "certified Arb enclosure of exp(z^2)*erfc(z)"
        assert result.diagnostics["formula"] == "exp(z^2)*erfc(z)"
    elif result.diagnostics["certificate_scope"] == "arb_erfi_formula":
        assert result.diagnostics["certificate_level"] == "formula_audited_alpha"
        assert result.diagnostics["audit_status"] == "formula_identity"
        assert result.diagnostics["certification_claim"] == "certified Arb enclosure of -i*erf(i*z)"
        assert result.diagnostics["formula"] == "-i*erf(i*z)"
    elif result.diagnostics["certificate_scope"] == "arb_dawson_formula":
        assert result.diagnostics["certificate_level"] == "formula_audited_alpha"
        assert result.diagnostics["audit_status"] == "formula_identity"
        assert (
            result.diagnostics["certification_claim"]
            == "certified Arb enclosure of sqrt(pi)/2*exp(-z^2)*erfi(z)"
        )
        assert result.diagnostics["formula"] == "sqrt(pi)/2*exp(-z^2)*erfi(z)"
    else:
        assert result.diagnostics["certificate_level"] == "direct_arb_primitive"
        assert result.diagnostics["audit_status"] == "audited_direct"
        assert "error-function primitive" in result.diagnostics["certification_claim"] or name == "dawson"
    if name == "erfc" and "formula" in result.diagnostics:
        assert result.diagnostics["formula"] == "1-erf"


@pytest.mark.parametrize(("name", "args"), UNSUPPORTED_CERTIFIED_CASES)
def test_unsupported_error_function_certified_domains_do_not_fallback_to_mpmath(name, args):
    result = getattr(certsf, name)(*args, dps=50, mode="certified")
    if _backend_is_unavailable(result):
        pytest.skip(result.diagnostics["error"])

    assert result.certified is False
    assert result.value == ""
    assert result.abs_error_bound is None
    assert result.rel_error_bound is None
    assert result.method == "arb_ball"
    assert result.backend == "python-flint"
    assert result.diagnostics["mode"] == "certified"
    assert result.diagnostics["certificate_scope"] in CERTIFIED_SCOPES[name].split("|")
    assert "error" in result.diagnostics


def test_erfc_fallback_path_records_formula_when_direct_erfc_is_unavailable(monkeypatch):
    flint = pytest.importorskip("flint")

    class ErfOnlyBall:
        def erf(self):
            return flint.acb("0.5").erf()

    monkeypatch.setattr(arb_backend, "_make_ball", lambda _z: ErfOnlyBall())

    result = arb_backend.arb_erfc("0.5", dps=50)

    assert result.certified is True
    assert result.diagnostics["certificate_scope"] == "direct_arb_erfc"
    assert result.diagnostics["certificate_level"] == "direct_arb_primitive"
    assert result.diagnostics["audit_status"] == "audited_direct"
    assert result.diagnostics["formula"] == "1-erf"
    assert result.diagnostics["certification_claim"] == (
        "certified Arb enclosure of 1 - erf(z) using direct Arb error-function primitive"
    )


def test_erfcx_formula_fallback_records_formula_when_direct_erfcx_is_unavailable(monkeypatch):
    flint = pytest.importorskip("flint")

    class ErfcOnlyBall:
        def __init__(self, value):
            self.value = flint.acb(value)

        def __mul__(self, other):
            other_value = other.value if isinstance(other, ErfcOnlyBall) else other
            return self.value * other_value

        def erfc(self):
            return self.value.erfc()

    monkeypatch.setattr(arb_backend, "_make_ball", lambda z: ErfcOnlyBall(z))

    result = arb_backend.arb_erfcx("0.5", dps=50)

    assert result.certified is True
    assert result.diagnostics["certificate_scope"] == "arb_erfcx_formula"
    assert result.diagnostics["certificate_level"] == "formula_audited_alpha"
    assert result.diagnostics["audit_status"] == "formula_identity"
    assert result.diagnostics["formula"] == "exp(z^2)*erfc(z)"
    assert result.diagnostics["certification_claim"] == "certified Arb enclosure of exp(z^2)*erfc(z)"


def test_erfi_formula_fallback_records_formula_when_direct_erfi_is_unavailable(monkeypatch):
    flint = pytest.importorskip("flint")

    class ErfOnlyBall:
        def __init__(self, value):
            self.value = flint.acb(value)

        def __rmul__(self, other):
            return other * self.value

    monkeypatch.setattr(arb_backend, "_make_ball", lambda z: ErfOnlyBall(z))

    result = arb_backend.arb_erfi("0.5", dps=50)

    assert result.certified is True
    assert result.diagnostics["certificate_scope"] == "arb_erfi_formula"
    assert result.diagnostics["certificate_level"] == "formula_audited_alpha"
    assert result.diagnostics["audit_status"] == "formula_identity"
    assert result.diagnostics["formula"] == "-i*erf(i*z)"
    assert result.diagnostics["certification_claim"] == "certified Arb enclosure of -i*erf(i*z)"


@pytest.mark.parametrize(("path", "expected_fragments"), DOC_EXPECTATIONS.items())
def test_error_function_documentation_uses_current_audit_wording(path, expected_fragments):
    text = _read(path)

    for fragment in expected_fragments:
        assert fragment in text


def test_external_reference_fixture_covers_error_function_surface():
    fixture_dir = ROOT / "tests" / "fixtures" / "external_reference"
    entries = []
    for fixture_name in (
        "error_function_reference.json",
        "erfcx_reference.json",
        "erfi_reference.json",
        "dawson_reference.json",
    ):
        entries.extend(json.loads((fixture_dir / fixture_name).read_text(encoding="utf-8")))
    covered_cases = {(entry["function"], tuple(entry["parameters"])) for entry in entries}

    assert {
        ("erf", ("0",)),
        ("erfc", ("0",)),
        ("erfcx", ("0",)),
        ("erf", ("1",)),
        ("erfc", ("1",)),
        ("erfcx", ("1",)),
        ("erfcx", ("-1",)),
        ("erfi", ("0",)),
        ("erfi", ("1",)),
        ("erfi", ("-1",)),
        ("erf", ("0.5+0.25j",)),
        ("erfc", ("0.5+0.25j",)),
        ("erfcx", ("0.5+0.25j",)),
        ("erfi", ("0.5+0.25j",)),
        ("dawson", ("0",)),
        ("dawson", ("1",)),
        ("dawson", ("-1",)),
        ("dawson", ("0.5+0.25j",)),
    } <= covered_cases


def test_pypi_smoke_covers_error_function_release_surface():
    text = _read(".github/workflows/pypi-smoke.yml")

    assert 'default: "0.2.0a8"' in text
    assert "inputs.version || '0.2.0a8'" in text
    assert 'erf("1.0", mode="fast"' in text
    assert 'erfc("1.0", mode="fast"' in text
    assert 'erfcx("1.0", mode="fast"' in text
    assert 'erfi("1.0", mode="fast"' in text
    assert 'dawson("1.0", mode="fast"' in text
    assert 'erf("1.0", mode="certified"' in text
    assert 'erfc("1.0", mode="certified"' in text
    assert 'erfcx("1.0", mode="certified"' in text
    assert 'erfi("1.0", mode="certified"' in text
    assert 'dawson("1.0", mode="certified"' in text
    assert "special_erf" in text
    assert "special_erfc" in text
    assert "special_erfcx" in text
    assert "special_erfi" in text
    assert "special_dawson" in text
    assert 'special_erf("1.0", mode="certified", dps=50)' in text
    assert 'special_erfc("1.0", mode="certified", dps=50)' in text
    assert 'special_erfcx("1.0", mode="certified", dps=50)' in text
    assert 'special_erfi("1.0", mode="certified", dps=50)' in text
    assert 'special_dawson("1.0", mode="certified", dps=50)' in text
    assert 'assert erf_result["function"] == "erf"' in text
    assert 'assert erfc_result["function"] == "erfc"' in text
    assert 'assert erfcx_result["function"] == "erfcx"' in text
    assert 'assert erfi_result["function"] == "erfi"' in text
    assert 'assert dawson_result["function"] == "dawson"' in text
    assert 'assert erf_result["certified"]' in text
    assert 'assert erfc_result["certified"]' in text
    assert 'assert erfcx_result["certified"]' in text
    assert 'assert erfi_result["certified"]' in text
    assert 'assert dawson_result["certified"]' in text


def test_publish_workflow_artifact_actions_remain_on_v6():
    for path in (".github/workflows/publish-pypi.yml", ".github/workflows/publish-testpypi.yml"):
        text = _read(path)

        assert "actions/upload-artifact@v6" in text
        assert "actions/download-artifact@v6" in text
        assert "actions/upload-artifact@v5" not in text
        assert "actions/download-artifact@v5" not in text


def test_release_policy_and_pypi_smoke_alpha8_guardrails_remain_current():
    smoke = _read(".github/workflows/pypi-smoke.yml")
    policy = _read("docs/release_policy.md")

    assert 'default: "0.2.0a8"' in smoke
    assert "inputs.version || '0.2.0a8'" in smoke
    assert "Routine feature alpha releases may skip TestPyPI" in policy
    assert "The `publish-testpypi` workflow must remain `workflow_dispatch` only." in policy


def test_error_function_release_docs_do_not_keep_pre_publication_alpha7_wording():
    current_scope = _read("docs/certified_scope_0_2_0.md")
    alpha7_release = _read("docs/release-0.2.0-alpha.7.md")

    assert "future v0.2.0-alpha.7" not in current_scope
    assert "should continue to target `0.2.0a6` until" not in alpha7_release


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _backend_is_unavailable(result):
    return not result.certified and "python-flint is not installed" in result.diagnostics.get("error", "")
