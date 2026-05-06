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
