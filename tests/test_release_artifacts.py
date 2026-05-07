from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RELEASE_EXAMPLES = (
    "gamma_certified.py",
    "airy_components.py",
    "bessel_complex.py",
    "pcf_experimental.py",
    "mcp_payload.py",
)


def test_release_notes_reference_payload_first_examples():
    release_notes = _read("docs/release-0.1.0.md")

    assert "full payloads instead of just numerical values" in release_notes
    assert "SFResult" in release_notes
    for example in RELEASE_EXAMPLES:
        assert f"examples/{example}" in release_notes


def test_release_examples_print_complete_payloads():
    for example in RELEASE_EXAMPLES:
        source = _read(f"examples/{example}")
        assert "json.dumps" in source
        assert ".value" not in source
        if example == "mcp_payload.py":
            assert "to_dict()" not in source
            assert "special_" in source
        else:
            assert "to_dict()" in source


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")
