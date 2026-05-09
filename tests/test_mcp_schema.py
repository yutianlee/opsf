from pathlib import Path
import json

import pytest

from certsf import beta, pochhammer
from certsf import mcp_server


ROOT = Path(__file__).resolve().parents[1]


def test_special_gamma_returns_json_object_payload():
    payload = mcp_server.special_gamma("3.2", dps=50, mode="high_precision")

    assert isinstance(payload, dict)
    assert json.loads(json.dumps(payload)) == payload
    assert payload["function"] == "gamma"
    assert payload["certified"] is False
    assert payload["backend"] == "mpmath"
    assert isinstance(payload["diagnostics"], dict)


def test_special_gamma_ratio_returns_json_object_payload():
    payload = mcp_server.special_gamma_ratio("3.2", "1.2", dps=50, mode="high_precision")

    assert isinstance(payload, dict)
    assert json.loads(json.dumps(payload)) == payload
    assert payload["function"] == "gamma_ratio"
    assert payload["certified"] is False
    assert payload["backend"] == "mpmath"
    assert isinstance(payload["diagnostics"], dict)


def test_special_loggamma_ratio_returns_json_object_payload():
    payload = mcp_server.special_loggamma_ratio("3.2", "1.2", dps=50, mode="high_precision")

    assert isinstance(payload, dict)
    assert json.loads(json.dumps(payload)) == payload
    assert payload["function"] == "loggamma_ratio"
    assert payload["certified"] is False
    assert payload["backend"] == "mpmath"
    assert isinstance(payload["diagnostics"], dict)


def test_special_beta_returns_json_object_payload():
    payload = mcp_server.special_beta("3.2", "1.2", dps=50, mode="high_precision")

    assert isinstance(payload, dict)
    assert json.loads(json.dumps(payload)) == payload
    assert payload == beta("3.2", "1.2", dps=50, mode="high_precision").to_mcp_dict()
    assert payload["function"] == "beta"
    assert payload["certified"] is False
    assert payload["backend"] == "mpmath"
    assert isinstance(payload["diagnostics"], dict)


def test_special_pochhammer_returns_json_object_payload():
    payload = mcp_server.special_pochhammer("3", "4", dps=50, mode="high_precision")

    assert isinstance(payload, dict)
    assert json.loads(json.dumps(payload)) == payload
    assert payload == pochhammer("3", "4", dps=50, mode="high_precision").to_mcp_dict()
    assert payload["function"] == "pochhammer"
    assert payload["certified"] is False
    assert payload["backend"] == "mpmath"
    assert isinstance(payload["diagnostics"], dict)


@pytest.mark.parametrize(
    ("tool", "args", "expected_components"),
    [
        pytest.param(mcp_server.special_airy, ("1.0",), {"ai", "aip", "bi", "bip"}, id="airy"),
        pytest.param(mcp_server.special_pbdv, ("2.5", "1.25"), {"value", "derivative"}, id="pbdv"),
    ],
)
def test_mcp_multi_component_values_are_nested_objects(tool, args, expected_components):
    payload = tool(*args, dps=50, mode="high_precision")

    assert isinstance(payload, dict)
    assert isinstance(payload["value"], dict)
    assert set(payload["value"]) == expected_components
    assert not isinstance(payload["value"], str)
    assert json.loads(json.dumps(payload)) == payload


def test_unsupported_certified_domain_returns_clean_mcp_failure_payload():
    payload = mcp_server.special_gamma("0", dps=50, mode="certified")

    assert isinstance(payload, dict)
    assert payload["function"] == "gamma"
    assert payload["certified"] is False
    assert payload["value"] == ""
    assert payload["abs_error_bound"] is None
    assert payload["rel_error_bound"] is None
    assert payload["diagnostics"]["mode"] == "certified"
    assert "error" in payload["diagnostics"]


def test_invalid_mode_raises_or_returns_clean_mcp_error_payload():
    try:
        payload = mcp_server.special_gamma("3.2", dps=50, mode="not-a-mode")
    except ValueError as exc:
        assert "mode must be one of" in str(exc)
    else:
        assert isinstance(payload, dict)
        assert payload["certified"] is False
        assert payload["diagnostics"]["mode"] == "not-a-mode"
        assert "error" in payload["diagnostics"]


def test_mcp_server_stays_thin_adapter_without_backend_logic():
    source = (ROOT / "src" / "certsf" / "mcp_server.py").read_text(encoding="utf-8")

    assert "from .backends" not in source
    assert "import flint" not in source
    assert "import mpmath" not in source
    assert "import scipy" not in source
    assert "mp.loggamma" not in source
    assert "special.loggamma" not in source
    assert ".rgamma()" not in source
    assert ".to_mcp_dict()" in source
