import pytest

import certsf
from certsf import mcp_server
from certsf.dispatcher import (
    METHOD_REGISTRY,
    REGISTRY,
    MethodSpec,
    _VALID_FUNCTIONS,
    available_functions,
    available_methods,
    available_modes,
    dispatch,
)


def test_dispatcher_registry_covers_every_function_and_mode():
    expected_modes = ("fast", "high_precision", "certified")

    assert tuple(REGISTRY) == available_functions()
    assert set(REGISTRY) == _VALID_FUNCTIONS
    for function, methods in REGISTRY.items():
        assert tuple(methods) == expected_modes
        for mode, method in methods.items():
            assert isinstance(method, MethodSpec)
            assert method.function == function
            assert method.mode == mode
            assert method.method_id
            assert method.priority >= 0
            assert callable(method.callable)
            assert method.backend
            assert method.domain
            assert method.applicability_note
            if mode == "certified":
                assert method.certified is True
                assert method.backend == "python-flint"
                assert method.method_id == "arb"
                assert method.certificate_scope is not None
                assert method.certificate_level is not None
                assert method.audit_status is not None
            else:
                assert method.certified is False
                assert method.method_id in {"scipy", "mpmath"}
                assert method.certificate_scope is None
                assert method.certificate_level is None
                assert method.audit_status is None


def test_method_registry_v2_preserves_current_default_methods():
    assert tuple(METHOD_REGISTRY) == available_functions()
    for function, methods_by_mode in REGISTRY.items():
        for mode, method in methods_by_mode.items():
            methods = METHOD_REGISTRY[function][mode]
            assert methods == (method,)
            assert methods[0].priority == 100


def test_loggamma_direct_arb_method_spec_records_audit_metadata():
    method = METHOD_REGISTRY["loggamma"]["certified"][0]

    assert method.method_id == "arb"
    assert method.certificate_scope == "direct_arb_primitive"
    assert method.certificate_level == "direct_arb_primitive"
    assert method.audit_status == "audited_direct"
    assert method.applicability_note == method.domain


def test_stirling_is_not_an_active_registered_method():
    active_method_ids = {method.method_id for method in available_methods() if method.function == "loggamma"}

    assert "stirling" not in active_method_ids


def test_available_methods_exposes_auditable_method_specs_in_dispatch_order():
    methods = available_methods()

    assert len(methods) == len(available_functions()) * 3
    assert methods[0] == REGISTRY["gamma"]["fast"]
    assert methods[1] == REGISTRY["gamma"]["high_precision"]
    assert methods[2] == REGISTRY["gamma"]["certified"]
    assert methods[-1] == REGISTRY["pbdv"]["certified"]


def test_dispatcher_registry_matches_public_api_and_mcp_tools():
    public_wrappers = set(certsf.__all__) - {"SFResult", "airyai", "airybi"}
    mcp_wrappers = {tool.__name__.removeprefix("special_") for tool in mcp_server._MCP_TOOLS}

    assert set(available_functions()) == public_wrappers
    assert set(available_functions()) == mcp_wrappers


def test_dispatcher_exposes_stable_modes_and_functions():
    assert available_modes() == ("auto", "fast", "high_precision", "certified")
    assert available_functions()[0:3] == ("gamma", "loggamma", "rgamma")
    assert available_functions()[-1] == "pbdv"


def test_dispatcher_rejects_unknown_function_before_backend_lookup():
    with pytest.raises(ValueError, match="unknown special function"):
        dispatch("not_a_function", 1, mode="fast")


def test_loggamma_certified_method_none_preserves_old_behavior():
    default = certsf.loggamma("3.2", dps=50, mode="high_precision")
    explicit_none = certsf.loggamma("3.2", dps=50, mode="high_precision", method=None)

    assert explicit_none == default


def test_loggamma_method_auto_preserves_automatic_selection():
    default = certsf.loggamma("3.2", dps=12, mode="auto")
    explicit_auto = certsf.loggamma("3.2", dps=12, mode="auto", method="auto")

    assert explicit_auto == default


def test_loggamma_method_arb_uses_direct_certified_backend():
    default = certsf.loggamma("3.2", dps=50, mode="certified")
    explicit_arb = certsf.loggamma("3.2", dps=50, mode="certified", method="arb")
    if _backend_is_unavailable(default):
        pytest.skip(default.diagnostics["error"])

    assert explicit_arb.certified is True
    assert explicit_arb.backend == default.backend == "python-flint"
    assert explicit_arb.method == default.method == "arb_ball"
    assert explicit_arb.diagnostics["certificate_scope"] == default.diagnostics["certificate_scope"]
    assert explicit_arb.diagnostics["certificate_scope"] == "direct_arb_primitive"


def test_loggamma_auto_certify_method_arb_uses_certified_backend():
    result = certsf.loggamma("3.2", dps=50, mode="auto", certify=True, method="arb")
    if _backend_is_unavailable(result):
        pytest.skip(result.diagnostics["error"])

    assert result.certified is True
    assert result.backend == "python-flint"
    assert result.diagnostics["mode"] == "certified"
    assert result.diagnostics["certificate_scope"] == "direct_arb_primitive"


def test_loggamma_method_arb_is_not_reinterpreted_for_high_precision_mode():
    with pytest.raises(ValueError, match="method 'arb' is not available for 'loggamma' in mode 'high_precision'"):
        certsf.loggamma("3.2", dps=50, mode="high_precision", method="arb")


def test_loggamma_unsupported_method_names_fail_clearly():
    with pytest.raises(ValueError, match="method 'not-a-method' is not available for 'loggamma'"):
        certsf.loggamma("3.2", dps=50, mode="certified", method="not-a-method")


def test_loggamma_stirling_method_is_planned_but_not_implemented():
    with pytest.raises(ValueError, match="method 'stirling'.*planned.*not implemented"):
        certsf.loggamma("50", dps=50, mode="certified", method="stirling")


def test_explicit_certified_arb_method_never_falls_back_to_mpmath():
    result = certsf.loggamma("3.2", dps=50, mode="certified", method="arb")

    assert result.backend == "python-flint"
    assert result.method == "arb_ball"


def test_certified_mode_rejects_mpmath_method_request():
    with pytest.raises(ValueError, match="method 'mpmath' is not available for 'loggamma' in mode 'certified'"):
        certsf.loggamma("3.2", dps=50, mode="certified", method="mpmath")


def _backend_is_unavailable(result):
    return not result.certified and "python-flint is not installed" in result.diagnostics.get("error", "")
