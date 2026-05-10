from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_release_policy_documents_real_pypi_and_testpypi_roles():
    text = _read("docs/release_policy.md")
    compact = _compact(text)

    assert "Public alpha prereleases are published to real PyPI." in text
    assert "GitHub prerelease publication triggers the protected `publish-pypi` workflow." in text
    assert "Real PyPI is the source of truth for install smoke tests." in text
    assert "Each real PyPI prerelease must be followed by:" in compact
    assert "a manual `pypi-smoke` run against the newly published version" in text
    assert "a post-release verification PR" in text
    assert "TestPyPI is manual-only staging." in text
    assert "Do not publish every alpha prerelease to TestPyPI." in compact
    assert "Routine feature alpha releases may skip TestPyPI" in text

    for trigger in (
        "first release of a new minor line",
        "final release candidates",
        "`pyproject.toml` or build-backend changes",
        "extras or dependency changes",
        "Trusted Publishing or environment changes",
        "release workflow changes",
        "prior PyPI packaging failure",
    ):
        assert trigger in text


def test_release_checklist_links_policy_and_keeps_testpypi_manual_only():
    text = _read("docs/release_checklist.md")
    compact = _compact(text)

    assert "[`release_policy.md`](release_policy.md)" in text
    assert "TestPyPI publishing is manual-only through `publish-testpypi`" in text
    assert "Decide whether TestPyPI staging is needed under" in text
    assert "Routine feature alpha releases may skip TestPyPI" in text
    assert "build, `twine check`, tag/version parity, protected PyPI publish, and real PyPI smoke" in compact


def test_publish_testpypi_workflow_requires_manual_confirmation():
    text = _read(".github/workflows/publish-testpypi.yml")

    assert "Manual staging only." in text
    assert "workflow_dispatch:" in text
    assert "release:" not in text
    assert 'description: "Type publish-testpypi to confirm"' in text
    assert 'if [ "${{ inputs.confirm }}" != "publish-testpypi" ]; then' in text
    assert "Refusing to publish to TestPyPI without confirm=publish-testpypi." in text
    assert "actions/upload-artifact@v6" in text
    assert "actions/download-artifact@v6" in text
    assert 'default: "v0.3.0-alpha.1"' in text


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _compact(text: str) -> str:
    return " ".join(text.split())
