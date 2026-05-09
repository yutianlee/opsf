from pathlib import Path

import certsf
from certsf.dispatcher import available_functions


ROOT = Path(__file__).resolve().parents[1]

FROZEN_0_1_0_FUNCTIONS = (
    "gamma",
    "loggamma",
    "rgamma",
    "airy",
    "ai",
    "bi",
    "besselj",
    "bessely",
    "besseli",
    "besselk",
    "pcfd",
    "pcfu",
    "pcfv",
    "pcfw",
    "pbdv",
)

CURRENT_0_2_0_FUNCTIONS = (
    "gamma",
    "loggamma",
    "rgamma",
    "gamma_ratio",
    "loggamma_ratio",
    "beta",
    "pochhammer",
    "airy",
    "ai",
    "bi",
    "besselj",
    "bessely",
    "besseli",
    "besselk",
    "pcfd",
    "pcfu",
    "pcfv",
    "pcfw",
    "pbdv",
)

FROZEN_0_1_0_STATUS_ROWS = (
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

CURRENT_0_2_0_STATUS_ROWS = (
    (
        "| `gamma`, `loggamma`, `rgamma`, `gamma_ratio`, `loggamma_ratio`, `beta`, `pochhammer` | "
        "alpha-certified, direct Arb gamma primitives and finite products |"
    ),
    "| `airy`, `ai`, `bi` | alpha-certified, direct Arb primitive |",
    (
        "| `besselj`, `bessely`, `besseli`, `besselk` | "
        "alpha-certified where direct Arb primitive works; real-valued order only |"
    ),
    "| `pcfd`, `pcfu`, `pcfv`, `pcfw`, `pbdv` | experimental certified formula layer |",
    "| MCP server | experimental tool interface |",
    "| Custom Taylor/asymptotic methods | not yet |",
)

FROZEN_0_1_0_SCOPE_ROWS = (
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


def test_current_public_certified_function_surface_matches_0_2_0_alpha_scope():
    assert available_functions() == CURRENT_0_2_0_FUNCTIONS

    exported_wrappers = set(certsf.__all__) - {"SFResult", "airyai", "airybi"}
    assert exported_wrappers == set(CURRENT_0_2_0_FUNCTIONS)
    assert certsf.airyai is certsf.ai
    assert certsf.airybi is certsf.bi


def test_0_1_0_scope_document_records_historical_frozen_status_matrix():
    scope_text = _doc_text("docs/certified_scope_0_1_0.md")

    assert "Do not add more public special-function wrappers before 0.1.0" in scope_text
    for function in FROZEN_0_1_0_FUNCTIONS:
        assert function in scope_text
    for row in FROZEN_0_1_0_SCOPE_ROWS:
        assert row in scope_text


def test_0_2_0_scope_document_records_current_status_matrix():
    scope_text = _doc_text("docs/certified_scope_0_2_0.md")

    for function in CURRENT_0_2_0_FUNCTIONS:
        assert function in scope_text
    for row in CURRENT_0_2_0_SCOPE_ROWS:
        assert row in scope_text


def test_readme_and_certification_docs_repeat_release_scope_statuses():
    readme_text = _doc_text("README.md")
    certification_text = _doc_text("docs/certification.md")

    assert "docs/certified_scope_0_1_0.md" in readme_text
    assert "docs/certified_scope_0_2_0.md" in readme_text
    assert "certified_scope_0_1_0.md" in certification_text
    assert "certified_scope_0_2_0.md" in certification_text
    for row in CURRENT_0_2_0_STATUS_ROWS:
        assert row in readme_text
        assert row in certification_text


def _doc_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")
