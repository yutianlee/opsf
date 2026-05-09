from pathlib import Path
import json

import pytest

import certsf
from certsf import mcp_server
from certsf.backends import arb_backend
from certsf.dispatcher import REGISTRY


ROOT = Path(__file__).resolve().parents[1]

ERROR_FUNCTIONS = ("erf", "erfc", "erfcx")
SAMPLE_ARGS = {"erf": ("0.5+0.25j",), "erfc": ("0.5+0.25j",), "erfcx": ("0.5+0.25j",)}
CERTIFIED_SCOPES = {
    "erf": "direct_arb_erf",
    "erfc": "direct_arb_erfc",
    "erfcx": "direct_arb_erfcx|arb_erfcx_formula",
}
UNSUPPORTED_CERTIFIED_CASES = (
    ("erf", ("nan",)),
    ("erfc", ("nan",)),
    ("erfcx", ("nan",)),
)
FORBIDDEN_ERROR_FUNCTION_WRAPPERS = ("erfi", "erfinv", "erfcinv")
DOC_EXPECTATIONS = {
    "README.md": (
        "| `erf`, `erfc`, `erfcx` | alpha-certified, direct Arb error-function primitives plus erfcx identity formula |",
        "Certified `erf` and `erfc` use direct Arb error-function primitives",
        "Certified `erfcx` prefers direct Arb `erfcx` when available",
        "`erfc` may evaluate `1 - erf(z)` and records `formula=\"1-erf\"`.",
        "`formula=\"exp(z^2)*erfc(z)\"`.",
        "No custom asymptotic certification is added.",
        "[`docs/error_function.md`](docs/error_function.md)",
    ),
    "docs/error_function.md": (
        "erf(z) = 2/sqrt(pi) * integral_0^z exp(-t^2) dt",
        "erfc(z) = 1 - erf(z)",
        "erfcx(z) = exp(z^2) erfc(z)",
        "direct Arb `erf` and `erfc` primitives",
        "record `diagnostics[\"formula\"] == \"1-erf\"`",
        "records `diagnostics[\"formula\"] == \"exp(z^2)*erfc(z)\"`",
        "`erfinv`, `erfcinv`, or Faddeeva functions",
        "No Taylor, asymptotic, or custom certification method",
    ),
    "docs/audit/error_function.md": (
        "Direct Arb error-function primitives",
        "`1 - erf(z)` and records `formula=\"1-erf\"`",
        "`erfcx(z) = exp(z^2) erfc(z)`",
        "`formula=\"exp(z^2)*erfc(z)\"`",
        "No `erfi`, `erfinv`, `erfcinv`",
        "Faddeeva wrapper",
        "No custom asymptotic or Taylor certification path",
        "`pypi-smoke.yml` defaults to `0.2.0a5`",
    ),
    "docs/certification_audit.md": (
        "`direct_arb_erf` | `erf` | `direct_arb_primitive`",
        "`direct_arb_erfc` | `erfc` | `direct_arb_primitive`",
        "`arb_erfcx_formula` | `erfcx` | `formula_audited_alpha`",
        "diagnostics record",
        "`formula=\"1-erf\"`",
        "`formula=\"exp(z^2)*erfc(z)\"`",
    ),
    "docs/certified_scope_0_2_0.md": (
        "Error-function family | `erf`, `erfc`, `erfcx`",
        "`erf(z)` and `erfc(z)` are the v0.2.0-alpha.5",
        "`erfcx(z)` is the future v0.2.0-alpha.6 feature-branch API expansion.",
        "certified `erfc` may use `1 - erf(z)` and must record `formula=\"1-erf\"`",
        "otherwise certified `erfcx` may use",
        "Custom Taylor, asymptotic, or non-Arb certification methods are outside",
        "Parabolic-cylinder family",
        "experimental certified formula layer",
    ),
    "docs/release_claims.md": (
        "Error-function family | alpha-certified, direct Arb error-function primitives plus erfcx identity formula",
        "direct Arb `erfc` is preferred",
        "direct Arb `erfcx` is",
        "fallback must be visible in diagnostics",
        "Do not claim `erfi`, `erfinv`, `erfcinv`, or Faddeeva",
        "Do not describe the parabolic-cylinder family as certified without the",
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
    else:
        assert result.diagnostics["certificate_level"] == "direct_arb_primitive"
        assert result.diagnostics["audit_status"] == "audited_direct"
        assert "error-function primitive" in result.diagnostics["certification_claim"]
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


@pytest.mark.parametrize(("path", "expected_fragments"), DOC_EXPECTATIONS.items())
def test_error_function_documentation_uses_current_audit_wording(path, expected_fragments):
    text = _read(path)

    for fragment in expected_fragments:
        assert fragment in text


def test_external_reference_fixture_covers_error_function_surface():
    fixture_dir = ROOT / "tests" / "fixtures" / "external_reference"
    entries = []
    for fixture_name in ("error_function_reference.json", "erfcx_reference.json"):
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
        ("erf", ("0.5+0.25j",)),
        ("erfc", ("0.5+0.25j",)),
        ("erfcx", ("0.5+0.25j",)),
    } <= covered_cases


def test_pypi_smoke_covers_error_function_release_surface():
    text = _read(".github/workflows/pypi-smoke.yml")

    assert 'default: "0.2.0a5"' in text
    assert "inputs.version || '0.2.0a5'" in text
    assert 'erf("1.0", mode="fast"' in text
    assert 'erfc("1.0", mode="fast"' in text
    assert 'erf("1.0", mode="certified"' in text
    assert 'erfc("1.0", mode="certified"' in text
    assert "special_erf" in text
    assert "special_erfc" in text


def test_publish_workflow_artifact_actions_remain_on_v6():
    for path in (".github/workflows/publish-pypi.yml", ".github/workflows/publish-testpypi.yml"):
        text = _read(path)

        assert "actions/upload-artifact@v6" in text
        assert "actions/download-artifact@v6" in text
        assert "actions/upload-artifact@v5" not in text
        assert "actions/download-artifact@v5" not in text


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _backend_is_unavailable(result):
    return not result.certified and "python-flint is not installed" in result.diagnostics.get("error", "")
