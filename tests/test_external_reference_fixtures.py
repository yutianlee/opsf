import json
from pathlib import Path

import pytest

import certsf

mp = pytest.importorskip("mpmath")
mp.mp.dps = 100

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "external_reference"
PARABOLIC_CYLINDER_FUNCTIONS = {"pbdv", "pcfd", "pcfu", "pcfv", "pcfw"}
EXPERIMENTAL_LEVEL = "formula_audited_experimental"
EXPERIMENTAL_STATUS = "experimental_formula"
EXPERIMENTAL_CLAIM = "certified Arb enclosure of the implemented documented formula; formula audit in progress"


def _fixture_entries():
    for path in sorted(FIXTURE_DIR.glob("*.json")):
        for entry in json.loads(path.read_text(encoding="utf-8")):
            yield {"fixture_file": path.name, **entry}


def _fixture_id(entry):
    parameters = ",".join(entry["parameters"])
    component = f".{entry['component']}" if "component" in entry else ""
    return f"{entry['fixture_file']}::{entry['function']}({parameters}){component}"


@pytest.mark.parametrize("entry", list(_fixture_entries()), ids=_fixture_id)
def test_certified_results_contain_external_reference_fixture(entry):
    function = getattr(certsf, entry["function"])
    result = function(*entry["parameters"], dps=90, mode="certified")
    if not result.certified:
        pytest.skip(result.diagnostics.get("error", "certified backend unavailable"))

    value, radius = _entry_ball(result, entry)
    reference = _mp_number(entry["expected_value"])
    reference_tolerance = _reference_tolerance(reference, int(entry["digits"]))

    assert abs(value - reference) <= radius + reference_tolerance
    if entry["function"] in PARABOLIC_CYLINDER_FUNCTIONS:
        assert result.diagnostics["certificate_level"] == EXPERIMENTAL_LEVEL
        assert result.diagnostics["audit_status"] == EXPERIMENTAL_STATUS
        assert result.diagnostics["certification_claim"] == EXPERIMENTAL_CLAIM


def _entry_ball(result, entry):
    if "component" not in entry:
        return _mp_number(result.value), _mp_number(result.abs_error_bound)

    values = json.loads(result.value)
    radii = json.loads(result.abs_error_bound)
    component = entry["component"]
    return _mp_number(values[component]), _mp_number(radii[component])


def _reference_tolerance(reference, digits):
    magnitude = max(abs(mp.re(reference)), abs(mp.im(reference)))
    if magnitude == 0:
        return mp.mpf(10) ** (1 - digits)
    exponent = mp.floor(mp.log10(magnitude))
    return 2 * (mp.mpf(10) ** (exponent - digits + 1))


def _mp_number(value):
    text = str(value).strip().strip("()").replace(" ", "").replace("i", "j")
    if "j" not in text.lower():
        return mp.mpf(text)
    real, imag = _split_complex_text(text)
    return mp.mpc(mp.mpf(real), mp.mpf(imag))


def _split_complex_text(text: str) -> tuple[str, str]:
    body = text[:-1]
    if body in {"", "+"}:
        return "0", "1"
    if body == "-":
        return "0", "-1"

    split_at = None
    for index in range(len(body) - 1, 0, -1):
        if body[index] in "+-" and body[index - 1] not in "eE":
            split_at = index
            break
    if split_at is None:
        return "0", _normalize_imaginary_component(body)
    return body[:split_at], _normalize_imaginary_component(body[split_at:])


def _normalize_imaginary_component(value: str) -> str:
    if value in {"", "+"}:
        return "1"
    if value == "-":
        return "-1"
    return value
