import json

import pytest

from certsf import SFResult


def _sample_result():
    return SFResult(
        value="2.0",
        abs_error_bound="1e-50",
        rel_error_bound="5e-51",
        certified=True,
        function="gamma",
        method="arb_ball",
        backend="python-flint",
        requested_dps=50,
        working_dps=59,
        terms_used=None,
        diagnostics={"mode": "certified"},
    )


def test_result_serialization_roundtrip():
    result = _sample_result()
    payload = result.to_dict()
    assert payload["value"] == "2.0"
    assert SFResult.from_dict(payload) == result
    assert SFResult.from_dict(json.loads(result.to_json())) == result


def test_result_repr_is_debuggable():
    text = repr(_sample_result())
    assert "SFResult" in text
    assert "gamma" in text
    assert "python-flint" in text


def test_result_from_dict_requires_all_fields():
    payload = _sample_result().to_dict()
    del payload["value"]
    with pytest.raises(ValueError):
        SFResult.from_dict(payload)


def test_result_component_helpers_decode_json_payloads():
    result = SFResult(
        value='{"ai": "0.1", "bi": "1.2"}',
        abs_error_bound='{"ai": "1e-50", "bi": "2e-50"}',
        rel_error_bound=None,
        certified=True,
        function="airy",
        method="arb_ball",
        backend="python-flint",
        requested_dps=50,
        working_dps=59,
        terms_used=None,
        diagnostics={"mode": "certified"},
    )
    assert result.value_as_dict() == {"ai": "0.1", "bi": "1.2"}
    assert result.abs_error_bound_as_dict() == {"ai": "1e-50", "bi": "2e-50"}
    assert result.rel_error_bound_as_dict() is None
    assert result.component("bi") == "1.2"


def test_result_mcp_dict_uses_nested_objects_when_available():
    result = SFResult(
        value='{"value": "-0.2", "derivative": "1.0"}',
        abs_error_bound='{"value": "1e-40", "derivative": "2e-40"}',
        rel_error_bound=None,
        certified=True,
        function="pbdv",
        method="arb_ball",
        backend="python-flint",
        requested_dps=50,
        working_dps=59,
        terms_used=None,
        diagnostics={"mode": "certified"},
    )
    payload = result.to_mcp_dict()
    assert payload["value"] == {"value": "-0.2", "derivative": "1.0"}
    assert payload["abs_error_bound"] == {"value": "1e-40", "derivative": "2e-40"}


def test_result_component_helpers_reject_scalar_values():
    with pytest.raises(ValueError):
        _sample_result().value_as_dict()
