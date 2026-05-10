import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_loggamma_auto_analysis_benchmark_schema_is_present():
    path = ROOT / "benchmarks" / "analyze_loggamma_auto.py"
    text = path.read_text(encoding="utf-8")

    assert path.is_file()
    for method in (
        '"arb"',
        '"stirling"',
        '"stirling_shifted"',
        '"certified_auto"',
    ):
        assert method in text
    for field in (
        '"function"',
        '"x"',
        '"dps"',
        '"method_requested"',
        '"result_method"',
        '"backend"',
        '"certified"',
        '"elapsed_seconds"',
        '"abs_error_bound"',
        '"terms_used"',
        '"certificate_scope"',
        '"selected_method"',
        '"auto_selected_method"',
        '"auto_reason"',
        '"shift"',
        '"shifted_argument"',
        '"shift_policy"',
        '"coefficient_source"',
        '"largest_bernoulli_used"',
        '"preselected"',
        '"can_certify"',
        '"estimated_terms_used"',
        '"auto_candidates"',
        '"error"',
    ):
        assert field in text


def test_loggamma_auto_summary_script_summarizes_sample_schema():
    script = ROOT / "benchmarks" / "summarize_loggamma_auto.py"
    sample = ROOT / "docs" / "benchmark_samples" / "loggamma_certified_auto_sample.jsonl"

    completed = subprocess.run(
        [sys.executable, str(script), str(sample)],
        check=True,
        capture_output=True,
        text=True,
    )
    summary = json.loads(completed.stdout)

    assert script.is_file()
    for field in (
        "total_records",
        "methods_seen",
        "certified_counts_by_method",
        "certified_auto_selected_method_counts",
        "fastest_method_by_case",
        "cases_stirling_failed_shifted_succeeded",
    ):
        assert field in summary
    assert "certified_auto" in summary["methods_seen"]
    assert any(
        summary["certified_auto_selected_method_counts"].get(method, 0) > 0
        for method in ("arb", "stirling", "stirling_shifted")
    )


def test_loggamma_auto_decision_docs_are_conservative_and_link_tooling():
    report = _read("docs/loggamma_certified_auto_decision.md")
    readme = _read("README.md")
    release = _read("docs/release-0.3.0.md")

    for text in (report, readme, release):
        assert "benchmarks/analyze_loggamma_auto.py" in text
        assert "benchmarks/summarize_loggamma_auto.py" in text
        assert "loggamma_certified_auto_decision.md" in text
        assert "loggamma_certified_auto_sample_summary.json" in text
    assert "`method=\"certified_auto\"` remains explicit only" in report
    assert "default certified `loggamma` remains the direct Arb path" in report
    assert "does not change runtime behavior" in report
    assert "not sufficient to change the default" in report
    assert "visible behavior change requiring a" in report
    assert "For now, keep direct Arb as the default certified `loggamma` method" in report
    assert "does not recommend changing the default" in report
    assert "no certification for complex Stirling expansions" in report
    assert "no gamma-ratio asymptotics" in report
    assert "no beta asymptotics" in report
    assert "parabolic-cylinder wrappers remain `experimental_formula`" in report


def test_loggamma_auto_sample_stays_compact_and_covers_representative_subset():
    path = ROOT / "docs" / "benchmark_samples" / "loggamma_certified_auto_sample.jsonl"
    lines = path.read_text(encoding="utf-8").splitlines()

    assert path.is_file()
    assert 0 < len(lines) <= 40
    text = "\n".join(lines)
    for fragment in (
        '"x": "3.2"',
        '"x": "20"',
        '"x": "38"',
        '"x": "1000"',
        '"dps": 50',
        '"dps": 100',
        '"method_requested": "arb"',
        '"method_requested": "stirling"',
        '"method_requested": "stirling_shifted"',
        '"method_requested": "certified_auto"',
        '"auto_selected_method"',
        '"auto_reason"',
        '"preselected"',
        '"can_certify"',
        '"estimated_terms_used"',
    ):
        assert fragment in text


def test_loggamma_auto_sample_summary_stays_compact_and_readable():
    path = ROOT / "docs" / "benchmark_samples" / "loggamma_certified_auto_sample_summary.json"
    summary = json.loads(path.read_text(encoding="utf-8"))

    assert path.is_file()
    assert summary["total_records"] == 32
    assert "certified_auto" in summary["methods_seen"]
    assert summary["cases_stirling_failed_shifted_succeeded"]
    assert summary["certified_auto_selected_method_counts"]["arb"] > 0
    assert summary["certified_auto_selected_method_counts"]["stirling"] > 0


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")
