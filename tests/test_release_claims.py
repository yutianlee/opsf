import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_SHORT_SUMMARY = "Alpha special-function wrappers with explicit certification diagnostics."
REQUIRED_CITATION_TITLE = "certsf: Alpha special-function wrappers with explicit certification diagnostics"
RELEASE_CLAIM_DOC = "docs/release_claims.md"
RELEASE_STATUS_ROWS = (
    "| `gamma`, `loggamma`, `rgamma` | alpha-certified, direct Arb primitive |",
    "| `airy`, `ai`, `bi` | alpha-certified, direct Arb primitive |",
    (
        "| `besselj`, `bessely`, `besseli`, `besselk` | "
        "alpha-certified where direct Arb primitive works; real-valued order only |"
    ),
    "| `pcfd`, `pcfu`, `pcfv`, `pcfw`, `pbdv` | experimental certified formula layer |",
    "| MCP server | experimental tool interface |",
    "| Custom Taylor/asymptotic methods | not yet |",
)
SCOPE_STATUS_ROWS = (
    "| Gamma family | `gamma`, `loggamma`, `rgamma` | alpha-certified, direct Arb primitive |",
    "| Airy family | `airy`, `ai`, `bi` | alpha-certified, direct Arb primitive |",
    (
        "| Bessel family | `besselj`, `bessely`, `besseli`, `besselk` | "
        "alpha-certified where direct Arb primitive works; real-valued order only |"
    ),
    (
        "| Parabolic-cylinder family | `pcfd`, `pcfu`, `pcfv`, `pcfw`, `pbdv` | "
        "experimental certified formula layer |"
    ),
    "| MCP server | `certsf.mcp_server` tools for the frozen wrappers | experimental tool interface |",
    "| Custom Taylor/asymptotic methods | none | not yet |",
)
RELEASE_SURFACES = (
    "README.md",
    "CHANGELOG.md",
    "docs/release-0.1.0.md",
    "docs/release_checklist.md",
    "docs/certification.md",
    "docs/certification_audit.md",
    "docs/certified_scope_0_1_0.md",
    "docs/formula_audit.md",
    RELEASE_CLAIM_DOC,
)
RELEASE_COPY_SURFACES = tuple(path for path in RELEASE_SURFACES if path != RELEASE_CLAIM_DOC)
FORBIDDEN_CLAIM_PATTERNS = (
    r"\bfully certified\b",
    r"\bglobally certified\b",
    r"\bproduction[- ]certified\b",
    r"\bcertified for every continuation\b",
    r"\bparabolic-cylinder (family|functions?) (is|are) certified\b",
    r"\bparabolic-cylinder (family|functions?) (is|are) broadly certified\b",
)


def test_package_and_citation_metadata_use_conservative_alpha_summary():
    pyproject_text = _read("pyproject.toml")
    citation_text = _read("CITATION.cff")

    assert f'description = "{REQUIRED_SHORT_SUMMARY}"' in pyproject_text
    assert f'title: "{REQUIRED_CITATION_TITLE}"' in citation_text
    assert "Certified special-function wrappers with explicit diagnostics" not in pyproject_text
    assert "Certified special-function wrappers with explicit diagnostics" not in citation_text


def test_release_surfaces_link_to_claim_guardrails():
    assert RELEASE_CLAIM_DOC in _read("README.md")
    assert "release_claims.md" in _read("docs/release-0.1.0.md")
    assert "Release-claim guardrails reviewed" in _read("docs/release_checklist.md")


def test_release_status_matrices_keep_conservative_claims():
    readme_text = _read("README.md")
    certification_text = _read("docs/certification.md")
    release_notes_text = _read("docs/release-0.1.0.md")
    scope_text = _read("docs/certified_scope_0_1_0.md")

    for row in RELEASE_STATUS_ROWS:
        assert row in readme_text
        assert row in certification_text
        assert row in release_notes_text
    for row in SCOPE_STATUS_ROWS:
        assert row in scope_text


def test_parabolic_cylinder_release_claim_remains_experimental():
    for path in RELEASE_SURFACES:
        text = _read(path)
        assert "experimental" in text.lower(), path
        assert "formula" in text.lower(), path


def test_release_surfaces_do_not_use_overbroad_certification_claims():
    for path in RELEASE_COPY_SURFACES:
        text = _read(path).lower()
        for pattern in FORBIDDEN_CLAIM_PATTERNS:
            assert re.search(pattern, text) is None, f"{path} uses forbidden claim pattern: {pattern}"


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")
