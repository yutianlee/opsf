from pathlib import Path
import subprocess
import sys


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_release_version.py"


def test_release_version_check_accepts_alpha_tag(tmp_path):
    pyproject = _write_pyproject(tmp_path, "0.1.0a2")

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "v0.1.0-alpha.2", "--pyproject", str(pyproject)],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "v0.1.0-alpha.2 -> 0.1.0a2" in result.stdout


def test_release_version_check_accepts_stable_tag_ref(tmp_path):
    pyproject = _write_pyproject(tmp_path, "0.1.0")

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "refs/tags/v0.1.0", "--pyproject", str(pyproject)],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "refs/tags/v0.1.0 -> 0.1.0" in result.stdout


def test_release_version_check_rejects_mismatched_version(tmp_path):
    pyproject = _write_pyproject(tmp_path, "0.1.0a1")

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "v0.1.0-alpha.2", "--pyproject", str(pyproject)],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "pyproject.toml declares '0.1.0a1'" in result.stderr


def _write_pyproject(tmp_path, version):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(f'[project]\nname = "certsf"\nversion = "{version}"\n', encoding="utf-8")
    return pyproject
