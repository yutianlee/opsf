from pathlib import Path
import json

import pytest

from certsf import beta, dawson, erf, erfc, erfcinv, erfcx, erfi, erfinv, pochhammer
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


def test_special_gamma_stirling_exp_method_returns_certified_mcp_payload():
    pytest.importorskip("flint")

    payload = mcp_server.special_gamma("20", dps=50, mode="certified", method="stirling_exp")

    assert isinstance(payload, dict)
    assert json.loads(json.dumps(payload)) == payload
    assert payload["function"] == "gamma"
    assert payload["certified"] is True
    assert payload["method"] == "stirling_exp_gamma"
    assert payload["backend"] == "certsf+python-flint"
    assert payload["diagnostics"]["selected_method"] == "stirling_exp"
    assert payload["diagnostics"]["certificate_scope"] == "gamma_positive_real_stirling_exp"


def test_special_rgamma_stirling_recip_method_returns_certified_mcp_payload():
    pytest.importorskip("flint")

    payload = mcp_server.special_rgamma("20", dps=50, mode="certified", method="stirling_recip")

    assert isinstance(payload, dict)
    assert json.loads(json.dumps(payload)) == payload
    assert payload["function"] == "rgamma"
    assert payload["certified"] is True
    assert payload["method"] == "stirling_recip_rgamma"
    assert payload["backend"] == "certsf+python-flint"
    assert payload["diagnostics"]["selected_method"] == "stirling_recip"
    assert payload["diagnostics"]["certificate_scope"] == "rgamma_positive_real_stirling_recip"


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


def test_special_loggamma_stirling_method_returns_certified_mcp_payload():
    pytest.importorskip("flint")

    payload = mcp_server.special_loggamma("50", dps=50, mode="certified", method="stirling")

    assert isinstance(payload, dict)
    assert json.loads(json.dumps(payload)) == payload
    assert payload["certified"] is True
    assert payload["function"] == "loggamma"
    assert payload["method"] == "stirling_loggamma"
    assert payload["backend"] == "certsf+python-flint"
    assert payload["diagnostics"]["selected_method"] == "stirling"
    assert payload["diagnostics"]["certificate_scope"] == "stirling_loggamma_positive_real"


def test_special_loggamma_shifted_stirling_method_returns_certified_mcp_payload():
    pytest.importorskip("flint")

    payload = mcp_server.special_loggamma("20", dps=100, mode="certified", method="stirling_shifted")

    assert isinstance(payload, dict)
    assert json.loads(json.dumps(payload)) == payload
    assert payload["certified"] is True
    assert payload["function"] == "loggamma"
    assert payload["method"] == "stirling_shifted_loggamma"
    assert payload["backend"] == "certsf+python-flint"
    assert payload["diagnostics"]["selected_method"] == "stirling_shifted"
    assert payload["diagnostics"]["shift"] == 18
    assert payload["diagnostics"]["shifted_argument"] == "38"
    assert payload["diagnostics"]["certificate_scope"] == "stirling_loggamma_positive_real"


def test_special_loggamma_certified_auto_method_returns_certified_mcp_payload():
    pytest.importorskip("flint")

    payload = mcp_server.special_loggamma("20", dps=100, mode="certified", method="certified_auto")

    assert isinstance(payload, dict)
    assert json.loads(json.dumps(payload)) == payload
    assert payload["certified"] is True
    assert payload["function"] == "loggamma"
    assert payload["method"] == "stirling_shifted_loggamma"
    assert payload["backend"] == "certsf+python-flint"
    assert payload["diagnostics"]["selected_method"] == "stirling_shifted"
    assert payload["diagnostics"]["auto_selector"] == "certified_auto"
    assert payload["diagnostics"]["auto_selected_method"] == "stirling_shifted"
    assert payload["diagnostics"]["certificate_scope"] == "stirling_loggamma_positive_real"


def test_special_loggamma_arb_method_and_omission_preserve_mcp_payload_behavior():
    explicit = mcp_server.special_loggamma("50", dps=50, mode="certified", method="arb")
    omitted = mcp_server.special_loggamma("50", dps=50, mode="certified")
    if _backend_is_unavailable_payload(explicit):
        pytest.skip(explicit["diagnostics"]["error"])

    assert explicit["certified"] is True
    assert omitted["certified"] is True
    assert explicit["method"] == omitted["method"] == "arb_ball"
    assert explicit["backend"] == omitted["backend"] == "python-flint"
    assert explicit["diagnostics"]["certificate_scope"] == "direct_arb_primitive"
    assert omitted["diagnostics"]["certificate_scope"] == "direct_arb_primitive"


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


def test_special_error_functions_return_json_object_payloads():
    erf_payload = mcp_server.special_erf("1", dps=50, mode="high_precision")
    erfc_payload = mcp_server.special_erfc("1", dps=50, mode="high_precision")
    erfcx_payload = mcp_server.special_erfcx("1", dps=50, mode="high_precision")
    erfi_payload = mcp_server.special_erfi("1", dps=50, mode="high_precision")
    dawson_payload = mcp_server.special_dawson("1", dps=50, mode="high_precision")
    erfinv_payload = mcp_server.special_erfinv("0.5", dps=50, mode="high_precision")
    erfcinv_payload = mcp_server.special_erfcinv("0.5", dps=50, mode="high_precision")

    assert json.loads(json.dumps(erf_payload)) == erf_payload
    assert json.loads(json.dumps(erfc_payload)) == erfc_payload
    assert json.loads(json.dumps(erfcx_payload)) == erfcx_payload
    assert json.loads(json.dumps(erfi_payload)) == erfi_payload
    assert json.loads(json.dumps(dawson_payload)) == dawson_payload
    assert json.loads(json.dumps(erfinv_payload)) == erfinv_payload
    assert json.loads(json.dumps(erfcinv_payload)) == erfcinv_payload
    assert erf_payload == erf("1", dps=50, mode="high_precision").to_mcp_dict()
    assert erfc_payload == erfc("1", dps=50, mode="high_precision").to_mcp_dict()
    assert erfcx_payload == erfcx("1", dps=50, mode="high_precision").to_mcp_dict()
    assert erfi_payload == erfi("1", dps=50, mode="high_precision").to_mcp_dict()
    assert dawson_payload == dawson("1", dps=50, mode="high_precision").to_mcp_dict()
    assert erfinv_payload == erfinv("0.5", dps=50, mode="high_precision").to_mcp_dict()
    assert erfcinv_payload == erfcinv("0.5", dps=50, mode="high_precision").to_mcp_dict()
    assert erf_payload["function"] == "erf"
    assert erfc_payload["function"] == "erfc"
    assert erfcx_payload["function"] == "erfcx"
    assert erfi_payload["function"] == "erfi"
    assert dawson_payload["function"] == "dawson"
    assert erfinv_payload["function"] == "erfinv"
    assert erfcinv_payload["function"] == "erfcinv"
    assert erf_payload["backend"] == "mpmath"
    assert erfc_payload["backend"] == "mpmath"
    assert erfcx_payload["backend"] == "mpmath"
    assert erfi_payload["backend"] == "mpmath"
    assert dawson_payload["backend"] == "mpmath"
    assert erfinv_payload["backend"] == "mpmath"
    assert erfcinv_payload["backend"] == "mpmath"


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


def _backend_is_unavailable_payload(payload):
    return not payload["certified"] and "python-flint is not installed" in payload["diagnostics"].get("error", "")
