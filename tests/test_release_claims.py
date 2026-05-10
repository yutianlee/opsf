import re
from pathlib import Path

from certsf.dispatcher import available_methods


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_SHORT_SUMMARY = "Alpha special-function wrappers with explicit certification diagnostics."
REQUIRED_CITATION_TITLE = "certsf: Alpha special-function wrappers with explicit certification diagnostics"
RELEASE_CLAIM_DOC = "docs/release_claims.md"
CURRENT_CUSTOM_ASYMPTOTIC_ROW = (
    '| Custom Taylor/asymptotic methods | alpha-certified custom asymptotic bound for positive-real loggamma via '
    'explicit `method="stirling"` or `method="stirling_shifted"`; real `x >= 20`; '
    "not automatic default selection |"
)
HISTORICAL_0_1_0_RELEASE_STATUS_ROWS = (
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
CURRENT_RELEASE_STATUS_ROWS = (
    (
        "| `gamma`, `loggamma`, `rgamma`, `gamma_ratio`, `loggamma_ratio`, `beta`, `pochhammer` | "
        "alpha-certified, direct Arb gamma primitives and finite products |"
    ),
    "| `erf`, `erfc`, `erfcx`, `erfi`, `dawson`, `erfinv`, `erfcinv` | alpha-certified, direct Arb error-function primitives plus erfcx, erfi, and dawson identity formulas; real erfinv on (-1, 1); real erfcinv on (0, 2) |",
    "| `airy`, `ai`, `bi` | alpha-certified, direct Arb primitive |",
    (
        "| `besselj`, `bessely`, `besseli`, `besselk` | "
        "alpha-certified where direct Arb primitive works; real-valued order only |"
    ),
    "| `pcfd`, `pcfu`, `pcfv`, `pcfw`, `pbdv` | experimental certified formula layer |",
    "| MCP server | experimental tool interface |",
    CURRENT_CUSTOM_ASYMPTOTIC_ROW,
)
HISTORICAL_0_1_0_SCOPE_ROWS = (
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
CURRENT_0_2_0_SCOPE_ROWS = (
    (
        "| Gamma family | `gamma`, `loggamma`, `rgamma`, `gamma_ratio`, `loggamma_ratio`, `beta`, "
        "`pochhammer` | alpha-certified, direct Arb gamma primitives and finite products |"
    ),
    "| Error-function family | `erf`, `erfc`, `erfcx`, `erfi`, `dawson`, `erfinv`, `erfcinv` | alpha-certified, direct Arb error-function primitives plus erfcx, erfi, and dawson identity formulas; real erfinv on (-1, 1); real erfcinv on (0, 2) |",
    "| Airy family | `airy`, `ai`, `bi` | alpha-certified, direct Arb primitive |",
    (
        "| Bessel family | `besselj`, `bessely`, `besseli`, `besselk` | "
        "alpha-certified where direct Arb primitive works; real-valued order only |"
    ),
    (
        "| Parabolic-cylinder family | `pcfd`, `pcfu`, `pcfv`, `pcfw`, `pbdv` | "
        "experimental certified formula layer |"
    ),
    "| MCP server | `certsf.mcp_server` tools for the current wrappers | experimental tool interface |",
    "| Custom Taylor/asymptotic methods | none | not yet |",
)
RELEASE_SURFACES = (
    "README.md",
    "CHANGELOG.md",
    "docs/release-0.1.0.md",
    "docs/release-0.3.0.md",
    "docs/release-0.3.0-alpha.1.md",
    "docs/release_checklist.md",
    "docs/certification.md",
    "docs/certification_audit.md",
    "docs/certified_scope_0_1_0.md",
    "docs/certified_scope_0_2_0.md",
    "docs/certified_scope_0_3_0.md",
    "docs/formula_audit.md",
    "docs/stirling_loggamma.md",
    RELEASE_CLAIM_DOC,
)
RELEASE_COPY_SURFACES = tuple(path for path in RELEASE_SURFACES if path != RELEASE_CLAIM_DOC)
FORBIDDEN_CLAIM_PATTERNS = (
    r"\bfully certified\b",
    r"\bfully certified loggamma\b",
    r"\bglobally certified\b",
    r"\bglobal loggamma certification\b",
    r"\bcomplex Stirling certification\b",
    r"\bcomplete certified asymptotic support\b",
    r"\bautomatic Stirling default\b",
    r"\bcertified gamma-ratio asymptotics\b",
    r"\bproduction[- ]certified\b",
    r"\bcertified for every continuation\b",
    r"\bcomplete certified special functions\b",
    r"\bparabolic-cylinder (family|functions?) (is|are) certified\b",
    r"\bparabolic-cylinder (family|functions?) (is|are) broadly certified\b",
    r"\bfully certified parabolic-cylinder\b",
    r"\bproduction[- ]certified parabolic-cylinder\b",
    r"\bcomplete certified parabolic-cylinder support\b",
)
README_SUPPORT_MATRIX = {
    "gamma": (
        "`gamma`, `loggamma`, `rgamma`, `gamma_ratio`, `loggamma_ratio`, `beta`, `pochhammer`",
        "alpha-certified, direct Arb gamma primitives and finite products",
    ),
    "loggamma": (
        "`gamma`, `loggamma`, `rgamma`, `gamma_ratio`, `loggamma_ratio`, `beta`, `pochhammer`",
        "alpha-certified, direct Arb gamma primitives and finite products",
    ),
    "rgamma": (
        "`gamma`, `loggamma`, `rgamma`, `gamma_ratio`, `loggamma_ratio`, `beta`, `pochhammer`",
        "alpha-certified, direct Arb gamma primitives and finite products",
    ),
    "gamma_ratio": (
        "`gamma`, `loggamma`, `rgamma`, `gamma_ratio`, `loggamma_ratio`, `beta`, `pochhammer`",
        "alpha-certified, direct Arb gamma primitives and finite products",
    ),
    "loggamma_ratio": (
        "`gamma`, `loggamma`, `rgamma`, `gamma_ratio`, `loggamma_ratio`, `beta`, `pochhammer`",
        "alpha-certified, direct Arb gamma primitives and finite products",
    ),
    "beta": (
        "`gamma`, `loggamma`, `rgamma`, `gamma_ratio`, `loggamma_ratio`, `beta`, `pochhammer`",
        "alpha-certified, direct Arb gamma primitives and finite products",
    ),
    "pochhammer": (
        "`gamma`, `loggamma`, `rgamma`, `gamma_ratio`, `loggamma_ratio`, `beta`, `pochhammer`",
        "alpha-certified, direct Arb gamma primitives and finite products",
    ),
    "erf": (
        "`erf`, `erfc`, `erfcx`, `erfi`, `dawson`, `erfinv`, `erfcinv`",
        "alpha-certified, direct Arb error-function primitives plus erfcx, erfi, and dawson identity formulas; real erfinv on (-1, 1); real erfcinv on (0, 2)",
    ),
    "erfc": (
        "`erf`, `erfc`, `erfcx`, `erfi`, `dawson`, `erfinv`, `erfcinv`",
        "alpha-certified, direct Arb error-function primitives plus erfcx, erfi, and dawson identity formulas; real erfinv on (-1, 1); real erfcinv on (0, 2)",
    ),
    "erfcx": (
        "`erf`, `erfc`, `erfcx`, `erfi`, `dawson`, `erfinv`, `erfcinv`",
        "alpha-certified, direct Arb error-function primitives plus erfcx, erfi, and dawson identity formulas; real erfinv on (-1, 1); real erfcinv on (0, 2)",
    ),
    "erfi": (
        "`erf`, `erfc`, `erfcx`, `erfi`, `dawson`, `erfinv`, `erfcinv`",
        "alpha-certified, direct Arb error-function primitives plus erfcx, erfi, and dawson identity formulas; real erfinv on (-1, 1); real erfcinv on (0, 2)",
    ),
    "dawson": (
        "`erf`, `erfc`, `erfcx`, `erfi`, `dawson`, `erfinv`, `erfcinv`",
        "alpha-certified, direct Arb error-function primitives plus erfcx, erfi, and dawson identity formulas; real erfinv on (-1, 1); real erfcinv on (0, 2)",
    ),
    "erfinv": (
        "`erf`, `erfc`, `erfcx`, `erfi`, `dawson`, `erfinv`, `erfcinv`",
        "alpha-certified, direct Arb error-function primitives plus erfcx, erfi, and dawson identity formulas; real erfinv on (-1, 1); real erfcinv on (0, 2)",
    ),
    "erfcinv": (
        "`erf`, `erfc`, `erfcx`, `erfi`, `dawson`, `erfinv`, `erfcinv`",
        "alpha-certified, direct Arb error-function primitives plus erfcx, erfi, and dawson identity formulas; real erfinv on (-1, 1); real erfcinv on (0, 2)",
    ),
    "airy": ("`airy`, `ai`, `bi`", "alpha-certified, direct Arb primitive"),
    "ai": ("`airy`, `ai`, `bi`", "alpha-certified, direct Arb primitive"),
    "bi": ("`airy`, `ai`, `bi`", "alpha-certified, direct Arb primitive"),
    "besselj": (
        "`besselj`, `bessely`, `besseli`, `besselk`",
        "alpha-certified where direct Arb primitive works; real-valued order only",
    ),
    "bessely": (
        "`besselj`, `bessely`, `besseli`, `besselk`",
        "alpha-certified where direct Arb primitive works; real-valued order only",
    ),
    "besseli": (
        "`besselj`, `bessely`, `besseli`, `besselk`",
        "alpha-certified where direct Arb primitive works; real-valued order only",
    ),
    "besselk": (
        "`besselj`, `bessely`, `besseli`, `besselk`",
        "alpha-certified where direct Arb primitive works; real-valued order only",
    ),
    "pcfd": ("`pcfd`, `pcfu`, `pcfv`, `pcfw`, `pbdv`", "experimental certified formula layer"),
    "pcfu": ("`pcfd`, `pcfu`, `pcfv`, `pcfw`, `pbdv`", "experimental certified formula layer"),
    "pcfv": ("`pcfd`, `pcfu`, `pcfv`, `pcfw`, `pbdv`", "experimental certified formula layer"),
    "pcfw": ("`pcfd`, `pcfu`, `pcfv`, `pcfw`, `pbdv`", "experimental certified formula layer"),
    "pbdv": ("`pcfd`, `pcfu`, `pcfv`, `pcfw`, `pbdv`", "experimental certified formula layer"),
}


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
    old_scope_text = _read("docs/certified_scope_0_1_0.md")
    current_scope_text = _read("docs/certified_scope_0_2_0.md")

    for row in CURRENT_RELEASE_STATUS_ROWS:
        assert row in readme_text
        assert row in certification_text
    for row in HISTORICAL_0_1_0_RELEASE_STATUS_ROWS:
        assert row in release_notes_text
    for row in HISTORICAL_0_1_0_SCOPE_ROWS:
        assert row in old_scope_text
    for row in CURRENT_0_2_0_SCOPE_ROWS:
        assert row in current_scope_text


def test_readme_support_matrix_matches_dispatcher_certified_methods():
    readme_text = _read("README.md")
    certified_functions = [
        method.function
        for method in available_methods()
        if method.mode == "certified" and method.certified
    ]

    assert set(certified_functions) == set(README_SUPPORT_MATRIX)
    for function in certified_functions:
        wrappers, status = README_SUPPORT_MATRIX[function]
        row = f"| {wrappers} | {status} |"
        assert row in readme_text, f"README support matrix is missing {function}: {row}"


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
