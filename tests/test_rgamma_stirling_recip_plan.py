from pathlib import Path

from certsf.dispatcher import available_methods


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_rgamma_stirling_recip_doc_exists_and_records_planning_scope():
    path = ROOT / "docs" / "rgamma_stirling_recip.md"
    text = path.read_text(encoding="utf-8")

    assert path.is_file()
    assert "planning-only future method" in text
    assert "not active" in text
    assert "not registered" in text
    assert 'method="stirling_recip"' in text
    assert "finite real `x >= 20`" in text
    assert "finite real x >= 20" in text
    assert "rgamma(x) = exp(-loggamma(x))" in text
    assert 'formula="rgamma=exp(-loggamma)"' in text
    assert 'certificate_scope="rgamma_positive_real_stirling_recip"' in text
    assert 'certificate_level="custom_asymptotic_bound"' in text
    assert 'audit_status="theorem_documented"' in text
    assert "stirling_recip_rgamma" in text


def test_rgamma_stirling_recip_doc_excludes_broader_claims():
    text = _read("docs/rgamma_stirling_recip.md")

    for fragment in (
        "complex `rgamma`",
        "No complex rgamma path is in scope.",
        "reflection formula",
        "No reflection formula path is in scope.",
        "near-pole behavior",
        "No near-pole behavior is in scope.",
        "gamma-ratio asymptotics",
        "No gamma-ratio asymptotics are in scope.",
        "beta asymptotics",
        "No beta asymptotics are in scope.",
        "No default dispatch change is planned.",
        "`experimental_formula`",
    ):
        assert fragment in text


def test_rgamma_stirling_recip_planned_diagnostics_are_documented():
    text = _read("docs/rgamma_stirling_recip.md")

    for fragment in (
        'selected_method="stirling_recip"',
        'certificate_scope="rgamma_positive_real_stirling_recip"',
        'certificate_level="custom_asymptotic_bound"',
        'audit_status="theorem_documented"',
        'formula="rgamma=exp(-loggamma)"',
        'domain="positive_real_x_ge_20"',
        "loggamma_method_used",
        "loggamma_abs_error_bound",
        "exp_radius",
        "propagated_error_bound",
        "fallback=[]",
    ):
        assert fragment in text


def test_rgamma_stirling_recip_is_not_registered_for_certified_rgamma():
    method_ids = {
        method.method_id
        for method in available_methods()
        if method.function == "rgamma" and method.mode == "certified"
    }

    assert "stirling_recip" not in method_ids


def test_rgamma_stirling_recip_plan_is_linked_without_active_audit_matrix_entry():
    scope = _read("docs/certified_scope_0_3_0.md")
    release = _read("docs/release-0.3.0.md")
    audit = _read("docs/v0_3_custom_method_audit.md")
    claims = _read("docs/release_claims.md")
    changelog = _read("CHANGELOG.md")

    assert "Planned custom rgamma method" in scope
    assert "planned only, not active until implementation lands" in scope
    assert 'method="stirling_recip"' in scope
    assert "Future Work" in release
    assert "rgamma_stirling_recip.md" in release
    assert "not implemented yet" in release
    assert "No release claim is active yet" in release
    assert "Future Work: Planned `rgamma(method=\"stirling_recip\")`" in audit
    assert "must not be included in the active summary matrix" in audit
    assert "active 0.3 custom methods remain the four currently active paths" in audit
    assert "planned explicit positive-real `rgamma`" in claims
    assert "not active, not registered" in claims
    assert "Planned positive-real `rgamma(x)` custom certificate" in changelog

    summary_matrix = audit.split("## Future Work", maxsplit=1)[0]
    assert "stirling_recip" not in summary_matrix
