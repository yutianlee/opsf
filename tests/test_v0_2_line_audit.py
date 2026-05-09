from pathlib import Path

import pytest

import certsf
from certsf import mcp_server
from certsf.dispatcher import REGISTRY


ROOT = Path(__file__).resolve().parents[1]

GAMMA_FAMILY = (
    "gamma",
    "loggamma",
    "rgamma",
    "gamma_ratio",
    "loggamma_ratio",
    "beta",
    "pochhammer",
)
SAMPLE_ARGS = {
    "gamma": ("3.2",),
    "loggamma": ("3.2",),
    "rgamma": ("3.2",),
    "gamma_ratio": ("3.2", "1.2"),
    "loggamma_ratio": ("3.2", "1.2"),
    "beta": ("3.2", "1.2"),
    "pochhammer": ("3.2", "4"),
}
CERTIFIED_SCOPES = {
    "gamma": "direct_arb_primitive",
    "loggamma": "direct_arb_primitive",
    "rgamma": "direct_arb_primitive",
    "gamma_ratio": "direct_arb_gamma_ratio",
    "loggamma_ratio": "direct_arb_loggamma_ratio",
    "beta": "direct_arb_beta",
    "pochhammer": "direct_arb_pochhammer_product",
}
UNSUPPORTED_CERTIFIED_CASES = (
    ("gamma", ("0",)),
    ("loggamma", ("0",)),
    ("gamma_ratio", ("0", "3.2")),
    ("gamma_ratio", ("0", "0")),
    ("loggamma_ratio", ("0", "3.2")),
    ("loggamma_ratio", ("3.2", "0")),
    ("loggamma_ratio", ("0", "0")),
    ("beta", ("0", "1.2")),
    ("beta", ("1.2", "0")),
    ("beta", ("0", "0")),
    ("pochhammer", ("3", "2.5")),
    ("pochhammer", ("3", "-1")),
    ("pochhammer", ("-2", "2")),
)
GAMMA_FAMILY_DOC_EXPECTATIONS = {
    "README.md": (
        "`gamma`, `loggamma`, `rgamma`, `gamma_ratio`, `loggamma_ratio`, `beta`, `pochhammer`",
        "Certified `gamma_ratio(a, b)` evaluates `Gamma(a) * rgamma(b)`.",
        "Certified `loggamma_ratio(a, b)` evaluates Arb `lgamma(a) - lgamma(b)`",
        "Certified `beta(a, b)` evaluates `Gamma(a) * Gamma(b) * rgamma(a+b)`",
        "Certified `pochhammer(a, n)` evaluates the finite product",
        "[`docs/pochhammer.md`](docs/pochhammer.md)",
    ),
    "docs/gamma_ratio.md": (
        "Gamma(a) / Gamma(b)",
        "mode=\"certified\"` uses Arb `Gamma(a) * rgamma(b)`",
        "denominator poles can be certified",
        "does not claim a limiting value for simultaneous poles",
    ),
    "docs/loggamma_ratio.md": (
        "principal loggamma(a) - principal loggamma(b)",
        "mode=\"certified\"` uses Arb `lgamma(a) - lgamma(b)`",
        "not necessarily the same value",
        "does not claim simultaneous-pole",
        "limiting values",
    ),
    "docs/beta.md": (
        "B(a,b) = Gamma(a) Gamma(b) / Gamma(a+b)",
        "mode=\"certified\"` uses Arb `Gamma(a) * Gamma(b) * rgamma(a+b)`",
        "poles can be certified",
        "does not claim a limiting value at simultaneous singularities",
    ),
    "docs/pochhammer.md": (
        "(a)_n = Gamma(a+n) / Gamma(a)",
        "mode=\"certified\"` uses Arb ball arithmetic for the finite product only",
        "`n` is an exact integer with `n >= 0`",
        "do not claim",
        "analytic continuation in `n`",
    ),
    "docs/certification_audit.md": (
        "`direct_arb_primitive` | `gamma`, `loggamma`, `rgamma`",
        "`direct_arb_gamma_ratio` | `gamma_ratio`",
        "`direct_arb_loggamma_ratio` | `loggamma_ratio`",
        "`direct_arb_beta` | `beta`",
        "`direct_arb_pochhammer_product` | `pochhammer`",
    ),
    "docs/certified_scope_0_2_0.md": (
        "Gamma family | `gamma`, `loggamma`, `rgamma`, `gamma_ratio`, `loggamma_ratio`, `beta`, `pochhammer`",
        "`pochhammer(a, n)` is the v0.2.0-alpha.4 API expansion.",
        "Parabolic-cylinder family",
        "experimental certified formula layer",
    ),
    "docs/release_claims.md": (
        "The 0.x alpha line should make conservative certification claims.",
        "Say that `pochhammer` is certified only through the finite product",
        "Do not describe the parabolic-cylinder family as certified without the",
    ),
}


def test_gamma_family_public_api_dispatcher_and_mcp_are_in_lockstep():
    mcp_tool_names = {tool.__name__ for tool in mcp_server._MCP_TOOLS}

    for name in GAMMA_FAMILY:
        assert hasattr(certsf, name)
        assert name in certsf.__all__
        assert name in REGISTRY
        assert tuple(REGISTRY[name]) == ("fast", "high_precision", "certified")
        assert f"special_{name}" in mcp_tool_names
        assert callable(getattr(mcp_server, f"special_{name}"))


@pytest.mark.parametrize("name", GAMMA_FAMILY)
def test_gamma_family_mcp_tools_match_python_api(name):
    args = SAMPLE_ARGS[name]
    wrapper = getattr(certsf, name)
    tool = getattr(mcp_server, f"special_{name}")

    assert tool(*args, dps=50, mode="high_precision") == wrapper(
        *args,
        dps=50,
        mode="high_precision",
    ).to_mcp_dict()


@pytest.mark.parametrize("name", GAMMA_FAMILY)
def test_gamma_family_certified_scopes_match_v0_2_audit(name):
    result = getattr(certsf, name)(*SAMPLE_ARGS[name], dps=50, mode="certified")
    if _backend_is_unavailable(result):
        pytest.skip(result.diagnostics["error"])

    assert result.certified is True
    assert result.backend == "python-flint"
    assert result.method == "arb_ball"
    assert result.diagnostics["certificate_scope"] == CERTIFIED_SCOPES[name]


@pytest.mark.parametrize(("name", "args"), UNSUPPORTED_CERTIFIED_CASES)
def test_unsupported_gamma_family_certified_domains_do_not_fallback_to_mpmath(name, args):
    result = getattr(certsf, name)(*args, dps=50, mode="certified")
    if _backend_is_unavailable(result):
        pytest.skip(result.diagnostics["error"])

    assert result.certified is False
    assert result.value == ""
    assert result.method == "arb_ball"
    assert result.backend == "python-flint"
    assert result.diagnostics["mode"] == "certified"
    assert "error" in result.diagnostics


@pytest.mark.parametrize(("path", "expected_fragments"), GAMMA_FAMILY_DOC_EXPECTATIONS.items())
def test_gamma_family_documentation_uses_current_v0_2_scope_wording(path, expected_fragments):
    text = _read(path)

    for fragment in expected_fragments:
        assert fragment in text


def test_pypi_smoke_covers_current_gamma_family_surface():
    text = _read(".github/workflows/pypi-smoke.yml")

    assert 'default: "0.2.0a4"' in text
    assert "inputs.version || '0.2.0a4'" in text
    for call in (
        'gamma("3.2"',
        'loggamma("3.2"',
        'rgamma("3.2"',
        'gamma_ratio("3.2", "1.2"',
        'loggamma_ratio("3.2", "1.2"',
        'beta("2", "3"',
        'pochhammer("0.5", "3"',
    ):
        assert call in text
    for name in GAMMA_FAMILY:
        assert f"special_{name}" in text


def test_publish_workflows_use_node24_artifact_actions():
    for path in (".github/workflows/publish-pypi.yml", ".github/workflows/publish-testpypi.yml"):
        text = _read(path)

        assert "actions/upload-artifact@v6" in text
        assert "actions/download-artifact@v6" in text
        assert "actions/upload-artifact@v5" not in text
        assert "actions/download-artifact@v5" not in text
        assert "Node.js 20" not in text


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _backend_is_unavailable(result):
    return not result.certified and "python-flint is not installed" in result.diagnostics.get("error", "")
