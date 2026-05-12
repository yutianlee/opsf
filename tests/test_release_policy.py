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
        "first non-prerelease release of a minor line",
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
    publish_text = _read(".github/workflows/publish-pypi.yml")

    assert "Manual staging only." in text
    assert "workflow_dispatch:" in text
    assert "release:" not in text
    assert 'description: "Type publish-testpypi to confirm"' in text
    assert 'if [ "${{ inputs.confirm }}" != "publish-testpypi" ]; then' in text
    assert "Refusing to publish to TestPyPI without confirm=publish-testpypi." in text
    assert "actions/upload-artifact@v6" in text
    assert "actions/download-artifact@v6" in text
    assert 'default: "v0.3.0"' in text
    assert 'default: "v0.3.0"' in publish_text


def test_alpha5_release_plan_records_explicit_rgamma_scope_and_smoke_pin():
    text = _read("docs/release-0.3.0-alpha.5.md")
    smoke_text = _read(".github/workflows/pypi-smoke.yml")

    assert "fifth alpha in the 0.3 line" in text
    assert 'method="stirling_recip"' in text
    assert "finite real `x >= 20`" in text
    assert 'certificate_scope="rgamma_positive_real_stirling_recip"' in text
    assert 'method="stirling_recip_rgamma"' in text
    assert "Default certified `rgamma` remains the direct Arb path." in text
    assert "`method=None` and calls with `method=\"auto\"` remain unchanged" in text
    assert "TestPyPI\nstaging is skipped unless that risk appears during validation" in text
    assert "If a smoke-pin update lands before PyPI publication succeeds" in text
    assert 'default: "0.3.0a5"' in smoke_text
    assert "inputs.version || '0.3.0a5'" in smoke_text


def test_final_release_plan_records_v030_scope_and_testpypi_staging():
    text = _read("docs/release-0.3.0.md")
    checklist = _read("docs/release_checklist.md")
    smoke_text = _read(".github/workflows/pypi-smoke.yml")
    publish_text = _read(".github/workflows/publish-pypi.yml")
    testpypi_text = _read(".github/workflows/publish-testpypi.yml")

    for fragment in (
        "first non-prerelease release of the 0.3 line",
        "already verified `v0.3.0-alpha.1` through `v0.3.0-alpha.5` scope",
        "keeps the 0.2 public wrapper surface",
        'method="stirling"',
        'method="stirling_shifted"',
        'method="certified_auto"',
        'method="stirling_exp"',
        'method="stirling_recip"',
        "Default certified `loggamma`",
        "Default certified `gamma`",
        "Default certified `rgamma`",
        "parabolic-cylinder formula layer beyond `experimental_formula`",
        "TestPyPI staging is required or strongly recommended",
        "`ref=v0.3.0` and `confirm=publish-testpypi`",
    ):
        assert fragment in text

    assert "## v0.3.0 Checklist" in checklist
    assert "`pyproject.toml` version is `0.3.0`" in checklist
    assert "`CITATION.cff` version is `0.3.0`" in checklist
    assert "`CHANGELOG.md` records `0.3.0`" in checklist
    assert "Publish workflow defaults point at `v0.3.0`" in checklist
    assert "PyPI smoke workflow remains pinned to `0.3.0a5`" in checklist
    assert "GitHub release for `v0.3.0` is a normal release, not a prerelease." in checklist
    assert "TestPyPI staging is required or strongly recommended" in checklist
    assert 'default: "0.3.0a5"' in smoke_text
    assert "inputs.version || '0.3.0a5'" in smoke_text
    assert 'default: "0.3.0"' not in smoke_text
    assert 'default: "v0.3.0"' in publish_text
    assert 'default: "v0.3.0"' in testpypi_text
    assert "release:" not in testpypi_text


def test_pypi_smoke_covers_explicit_rgamma_stirling_recip_method():
    smoke_text = _read(".github/workflows/pypi-smoke.yml")

    for fragment in (
        'rgamma("20", mode="certified", method="stirling_recip", dps=50)',
        'rgamma("20", mode="certified", method="stirling_recip", dps=100)',
        'special_rgamma("20", mode="certified", method="stirling_recip", dps=50)',
        'special_rgamma("20", mode="certified", method="stirling_recip", dps=100)',
        'result.function == "rgamma"',
        'result.method == "stirling_recip_rgamma"',
        'result.backend == "certsf+python-flint"',
        'result.diagnostics["selected_method"] == "stirling_recip"',
        'result.diagnostics["certificate_scope"] == "rgamma_positive_real_stirling_recip"',
        'result.diagnostics["certificate_level"] == "custom_asymptotic_bound"',
        'result.diagnostics["audit_status"] == "theorem_documented"',
        'result.diagnostics["loggamma_method_used"] in {"stirling", "stirling_shifted"}',
        "result.abs_error_bound is not None",
        'payload["function"] == "rgamma"',
        'payload["certified"]',
        'payload["method"] == "stirling_recip_rgamma"',
        'payload["backend"] == "certsf+python-flint"',
        'payload["diagnostics"]["selected_method"] == "stirling_recip"',
        'payload["diagnostics"]["certificate_scope"] == "rgamma_positive_real_stirling_recip"',
        'payload["diagnostics"]["certificate_level"] == "custom_asymptotic_bound"',
        'payload["diagnostics"]["audit_status"] == "theorem_documented"',
        'payload["diagnostics"]["loggamma_method_used"] in {"stirling", "stirling_shifted"}',
        'payload["abs_error_bound"] is not None',
    ):
        assert fragment in smoke_text


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _compact(text: str) -> str:
    return " ".join(text.split())
