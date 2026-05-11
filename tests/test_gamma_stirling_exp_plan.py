from pathlib import Path

from certsf.dispatcher import available_methods


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_gamma_stirling_exp_doc_exists_and_records_active_explicit_scope():
    text = _read("docs/gamma_stirling_exp.md")

    assert 'method="stirling_exp"' in text
    assert "active explicit method" in text
    assert "does not change default dispatch" in text
    assert "not automatic default selection" in text


def test_gamma_stirling_exp_doc_freezes_narrow_scope():
    text = _read("docs/gamma_stirling_exp.md")

    assert "Active domain: finite real `x >= 20`." in text
    assert 'certificate_scope="gamma_positive_real_stirling_exp"' in text
    assert 'certificate_level="custom_asymptotic_bound"' in text
    assert 'audit_status="theorem_documented"' in text
    assert 'selected_method="stirling_exp"' in text
    assert "No complex gamma path is in scope." in text
    assert "No reflection formula path is in scope." in text
    assert "No gamma-ratio asymptotics are in scope." in text
    assert "beta asymptotics" in text
    assert "`experimental_formula`" in text


def test_gamma_stirling_exp_diagnostics_are_documented():
    text = _read("docs/gamma_stirling_exp.md")

    for fragment in (
        "loggamma_method_used",
        "loggamma_abs_error_bound",
        "exp_radius",
        "propagated_error_bound",
        "fallback=[]",
    ):
        assert fragment in text


def test_gamma_stirling_exp_is_registered_only_for_certified_gamma():
    method_ids = {
        method.method_id
        for method in available_methods()
        if method.function == "gamma" and method.mode == "certified"
    }
    non_gamma_methods = {
        (method.function, method.mode)
        for method in available_methods()
        if method.method_id == "stirling_exp" and method.function != "gamma"
    }

    assert "stirling_exp" in method_ids
    assert non_gamma_methods == set()


def test_gamma_stirling_exp_surfaces_are_linked():
    scope = _read("docs/certified_scope_0_3_0.md")
    release = _read("docs/release-0.3.0.md")
    changelog = _read("CHANGELOG.md")

    assert "Custom gamma method" in scope
    assert "active explicit method" in scope
    assert "gamma_positive_real_stirling_exp" in scope
    assert "Positive-Real `gamma` via Loggamma Exponentiation" in release
    assert "active explicit method" in release
    assert "gamma_stirling_exp.md" in release
    assert "explicit positive-real `gamma(x)` certificate" in changelog
    assert "method=\"stirling_exp\"" in changelog


def test_pypi_smoke_covers_gamma_stirling_exp_method():
    text = _read(".github/workflows/pypi-smoke.yml")

    for fragment in (
        'gamma("20", mode="certified", method="stirling_exp", dps=50)',
        'gamma("20", mode="certified", method="stirling_exp", dps=100)',
        'special_gamma("20", mode="certified", method="stirling_exp", dps=50)',
        'result.method == "stirling_exp_gamma"',
        'gamma_stirling_payload["method"] == "stirling_exp_gamma"',
        '"selected_method"] == "stirling_exp"',
        '"certificate_scope"] == "gamma_positive_real_stirling_exp"',
        '"loggamma_method_used"] in {"stirling", "stirling_shifted"}',
        '"loggamma_abs_error_bound" in result.diagnostics',
        '"exp_radius" in result.diagnostics',
        '"propagated_error_bound" in result.diagnostics',
        'result.backend != "mpmath"',
    ):
        assert fragment in text
