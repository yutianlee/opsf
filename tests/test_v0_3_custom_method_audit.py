import json
from importlib import import_module
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def test_v0_3_custom_method_audit_exists_and_records_all_paths():
    path = ROOT / "docs" / "v0_3_custom_method_audit.md"
    text = path.read_text(encoding="utf-8")

    assert path.is_file()
    for fragment in (
        'loggamma(method="stirling")',
        'loggamma(method="stirling_shifted")',
        'loggamma(method="certified_auto")',
        'gamma(method="stirling_exp")',
        'certificate_scope="stirling_loggamma_positive_real"',
        'certificate_scope="gamma_positive_real_stirling_exp"',
        "Default certified `loggamma` and default certified `gamma` remain direct Arb",
        "complex `loggamma`",
        "complex `gamma`",
        "reflection formula certification",
        "gamma-ratio asymptotics",
        "beta asymptotics",
        "Parabolic-cylinder wrappers remain `experimental_formula`",
    ):
        assert fragment in text


def test_v0_3_custom_method_audit_records_expected_diagnostics():
    text = _read("docs/v0_3_custom_method_audit.md")

    for fragment in (
        "shift",
        "shifted_argument",
        "shift_policy",
        "guard_digits",
        "effective_dps",
        "coefficient_source",
        "largest_bernoulli_used",
        "tail_bound",
        "auto_selector",
        "auto_selected_method",
        "auto_reason",
        "auto_candidates",
        "preselected",
        "can_certify",
        "estimated_terms_used",
        "loggamma_method_used",
        "loggamma_abs_error_bound",
        "exp_radius",
        "propagated_error_bound",
    ):
        assert fragment in text


def test_gamma_methods_benchmark_schema_is_present():
    path = ROOT / "benchmarks" / "bench_gamma_methods.py"
    text = path.read_text(encoding="utf-8")

    assert path.is_file()
    assert "pass_dps" not in text
    assert 'call_kwargs["dps"] = dps' in text
    assert "gamma(x, **call_kwargs)" in text
    assert 'method": "stirling_exp"' in text
    for field in (
        '"function"',
        '"x"',
        '"dps"',
        '"mode"',
        '"method_requested"',
        '"result_method"',
        '"backend"',
        '"certified"',
        '"elapsed_seconds"',
        '"abs_error_bound"',
        '"rel_error_bound"',
        '"terms_used"',
        '"certificate_scope"',
        '"selected_method"',
        '"loggamma_method_used"',
        '"loggamma_abs_error_bound"',
        '"exp_radius"',
        '"propagated_error_bound"',
        '"error"',
    ):
        assert field in text


def test_gamma_methods_benchmark_passes_requested_dps_for_every_case(monkeypatch):
    benchmark = import_module("benchmarks.bench_gamma_methods")
    calls: list[dict[str, Any]] = []

    class DummyResult:
        function = "gamma"
        method = "dummy_method"
        backend = "dummy_backend"
        certified = True
        abs_error_bound = None
        rel_error_bound = None
        terms_used = None
        diagnostics: dict[str, Any] = {}

    def fake_gamma(x: str, **kwargs: Any) -> DummyResult:
        calls.append({"x": x, **kwargs})
        return DummyResult()

    monkeypatch.setattr(benchmark, "gamma", fake_gamma)

    for mode, method_requested, kwargs in benchmark.METHOD_CASES:
        record = benchmark.run_case(
            x="20",
            dps=100,
            mode=mode,
            method_requested=method_requested,
            kwargs=kwargs,
        )

        assert record["dps"] == 100
        assert calls[-1]["dps"] == 100


def test_gamma_methods_benchmark_sample_is_compact_and_real():
    path = ROOT / "docs" / "benchmark_samples" / "gamma_stirling_exp_sample.jsonl"
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    records = [json.loads(line) for line in lines if line.strip()]

    assert path.is_file()
    assert 0 < len(records) <= 20
    assert {record["x"] for record in records} == {"20", "100"}
    assert {record["dps"] for record in records} == {50, 100}
    assert any(record["method_requested"] == "stirling_exp" for record in records)
    assert any("loggamma_method_used" in record for record in records)
    assert all(record["error"] for record in records if not record["certified"])


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")
