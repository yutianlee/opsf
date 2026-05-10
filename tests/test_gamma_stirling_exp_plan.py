from pathlib import Path

from certsf.dispatcher import available_methods


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_gamma_stirling_exp_planning_doc_exists_and_is_inactive():
    text = _read("docs/gamma_stirling_exp.md")

    assert 'method="stirling_exp"' in text
    assert "planning note only" in text
    assert "planned only" in text
    assert "not active until an implementation" in text
    assert "does not activate a runtime method" in text
    assert "does not change default dispatch" in text


def test_gamma_stirling_exp_planning_doc_freezes_narrow_scope():
    text = _read("docs/gamma_stirling_exp.md")

    assert "Planned domain: real `x >= 20`." in text
    assert 'certificate_scope="gamma_positive_real_stirling_exp"' in text
    assert 'certificate_level="custom_asymptotic_bound"' in text
    assert 'audit_status="theorem_documented"' in text
    assert 'selected_method="stirling_exp"' in text
    assert "No complex gamma path is in scope." in text
    assert "No reflection formula path is in scope." in text
    assert "No gamma-ratio asymptotics are in scope." in text
    assert "beta asymptotics" in text
    assert "`experimental_formula`" in text


def test_gamma_stirling_exp_planned_diagnostics_are_documented():
    text = _read("docs/gamma_stirling_exp.md")

    for fragment in (
        "loggamma_method_used",
        "loggamma_abs_error_bound",
        "exp_radius",
        "propagated_error_bound",
        "fallback=[]",
    ):
        assert fragment in text


def test_gamma_stirling_exp_is_not_registered_yet():
    method_ids = {
        method.method_id
        for method in available_methods()
        if method.function == "gamma" and method.mode == "certified"
    }

    assert "stirling_exp" not in method_ids


def test_gamma_stirling_exp_planning_surfaces_are_linked():
    scope = _read("docs/certified_scope_0_3_0.md")
    release = _read("docs/release-0.3.0.md")
    changelog = _read("CHANGELOG.md")

    assert "Planned custom gamma method" in scope
    assert "planned only, not active until implementation lands" in scope
    assert "gamma_positive_real_stirling_exp" in scope
    assert "Future Work: Positive-Real `gamma`" in release
    assert "not implemented yet" in release
    assert "no release claim is active yet" in release
    assert "gamma_stirling_exp.md" in release
    assert "Planned positive-real `gamma(x)` custom certificate" in changelog
    assert "Documentation only; no runtime behavior" in changelog
