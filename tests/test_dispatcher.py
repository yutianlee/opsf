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
            assert methods[0] == method
            assert min(registered.priority for registered in methods) == method.priority == 100


def test_loggamma_direct_arb_method_spec_records_audit_metadata():
    method = METHOD_REGISTRY["loggamma"]["certified"][0]

    assert method.method_id == "arb"
    assert method.certificate_scope == "direct_arb_primitive"
    assert method.certificate_level == "direct_arb_primitive"
    assert method.audit_status == "audited_direct"
    assert method.applicability_note == method.domain


def test_gamma_stirling_exp_method_spec_records_custom_asymptotic_metadata():
    method = METHOD_REGISTRY["gamma"]["certified"][1]

    assert method.method_id == "stirling_exp"
    assert method.certificate_scope == "gamma_positive_real_stirling_exp"
    assert method.certificate_level == "custom_asymptotic_bound"
    assert method.audit_status == "theorem_documented"
    assert method.backend == "certsf+python-flint"
    assert "x >= 20" in method.domain
    assert "not automatic default selection" in method.applicability_note
    assert "reflection formulas" in method.applicability_note


def test_rgamma_stirling_recip_method_spec_records_custom_asymptotic_metadata():
    method = METHOD_REGISTRY["rgamma"]["certified"][1]

    assert method.method_id == "stirling_recip"
    assert method.certificate_scope == "rgamma_positive_real_stirling_recip"
    assert method.certificate_level == "custom_asymptotic_bound"
    assert method.audit_status == "theorem_documented"
    assert method.backend == "certsf+python-flint"
    assert "x >= 20" in method.domain
    assert "not automatic default selection" in method.applicability_note
    assert "reflection formulas" in method.applicability_note
    assert "near-pole behavior" in method.applicability_note


def test_loggamma_ratio_stirling_diff_method_spec_records_custom_asymptotic_metadata():
    method = METHOD_REGISTRY["loggamma_ratio"]["certified"][1]

    assert method.method_id == "stirling_diff"
    assert method.certificate_scope == "loggamma_ratio_positive_real_stirling_diff"
    assert method.certificate_level == "custom_asymptotic_bound"
    assert method.audit_status == "theorem_documented"
    assert method.backend == "certsf+python-flint"
    assert "a >= 20" in method.domain
    assert "b >= 20" in method.domain
    assert "not automatic default selection" in method.applicability_note
    assert "reflection formulas" in method.applicability_note
    assert "near-pole behavior" in method.applicability_note


def test_gamma_ratio_stirling_ratio_method_spec_records_custom_asymptotic_metadata():
    method = METHOD_REGISTRY["gamma_ratio"]["certified"][1]

    assert method.method_id == "stirling_ratio"
    assert method.certificate_scope == "gamma_ratio_positive_real_stirling_ratio"
    assert method.certificate_level == "custom_asymptotic_bound"
    assert method.audit_status == "theorem_documented"
    assert method.backend == "certsf+python-flint"
    assert "a >= 20" in method.domain
    assert "b >= 20" in method.domain
    assert "not automatic default selection" in method.applicability_note
    assert "reflection formulas" in method.applicability_note
    assert "near-pole behavior" in method.applicability_note
    assert "beta asymptotics" in method.applicability_note


def test_loggamma_stirling_method_spec_records_custom_asymptotic_metadata():
    method = METHOD_REGISTRY["loggamma"]["certified"][1]

    assert method.method_id == "stirling"
    assert method.certificate_scope == "stirling_loggamma_positive_real"
    assert method.certificate_level == "custom_asymptotic_bound"
    assert method.audit_status == "theorem_documented"
    assert "x >= 20" in method.domain
    assert "not automatic default selection" in method.applicability_note


def test_loggamma_shifted_stirling_method_spec_records_custom_asymptotic_metadata():
    method = METHOD_REGISTRY["loggamma"]["certified"][2]

    assert method.method_id == "stirling_shifted"
    assert method.certificate_scope == "stirling_loggamma_positive_real"
    assert method.certificate_level == "custom_asymptotic_bound"
    assert method.audit_status == "theorem_documented"
    assert "x >= 20" in method.domain
    assert "not automatic default selection" in method.applicability_note


def test_loggamma_certified_auto_method_spec_records_multi_scope_metadata():
    method = METHOD_REGISTRY["loggamma"]["certified"][3]

    assert method.method_id == "certified_auto"
    assert method.certificate_scope == "direct_arb_primitive|stirling_loggamma_positive_real"
    assert method.certificate_level == "direct_arb_primitive|custom_asymptotic_bound"
    assert method.audit_status == "audited_direct|theorem_documented"
    assert method.backend == "certsf+python-flint"
    assert "Explicit method='certified_auto' only" in method.applicability_note
    assert "does not change method=None" in method.applicability_note


def test_stirling_methods_are_active_only_for_explicit_certified_loggamma():
    active_loggamma_methods = [
        method
        for method in available_methods()
        if method.function == "loggamma" and method.mode == "certified"
    ]
    stirling_methods = [
        method
        for method in available_methods()
        if method.method_id == "stirling"
    ]
    shifted_methods = [
        method
        for method in available_methods()
        if method.method_id == "stirling_shifted"
    ]
    certified_auto_methods = [
        method
        for method in available_methods()
        if method.method_id == "certified_auto"
    ]

    assert [method.method_id for method in active_loggamma_methods] == [
        "arb",
        "stirling",
        "stirling_shifted",
        "certified_auto",
    ]
    assert stirling_methods == [METHOD_REGISTRY["loggamma"]["certified"][1]]
    assert shifted_methods == [METHOD_REGISTRY["loggamma"]["certified"][2]]
    assert certified_auto_methods == [METHOD_REGISTRY["loggamma"]["certified"][3]]
    assert METHOD_REGISTRY["loggamma"]["certified"][0] == REGISTRY["loggamma"]["certified"]


def test_stirling_exp_method_is_active_only_for_explicit_certified_gamma():
    active_gamma_methods = [
        method for method in available_methods() if method.function == "gamma" and method.mode == "certified"
    ]
    stirling_exp_methods = [method for method in available_methods() if method.method_id == "stirling_exp"]

    assert [method.method_id for method in active_gamma_methods] == ["arb", "stirling_exp"]
    assert stirling_exp_methods == [METHOD_REGISTRY["gamma"]["certified"][1]]
    assert METHOD_REGISTRY["gamma"]["certified"][0] == REGISTRY["gamma"]["certified"]


def test_stirling_recip_method_is_active_only_for_explicit_certified_rgamma():
    active_rgamma_methods = [
        method for method in available_methods() if method.function == "rgamma" and method.mode == "certified"
    ]
    stirling_recip_methods = [method for method in available_methods() if method.method_id == "stirling_recip"]

    assert [method.method_id for method in active_rgamma_methods] == ["arb", "stirling_recip"]
    assert stirling_recip_methods == [METHOD_REGISTRY["rgamma"]["certified"][1]]
    assert METHOD_REGISTRY["rgamma"]["certified"][0] == REGISTRY["rgamma"]["certified"]


def test_stirling_diff_method_is_active_only_for_explicit_certified_loggamma_ratio():
    active_loggamma_ratio_methods = [
        method
        for method in available_methods()
        if method.function == "loggamma_ratio" and method.mode == "certified"
    ]
    stirling_diff_methods = [method for method in available_methods() if method.method_id == "stirling_diff"]

    assert [method.method_id for method in active_loggamma_ratio_methods] == ["arb", "stirling_diff"]
    assert stirling_diff_methods == [METHOD_REGISTRY["loggamma_ratio"]["certified"][1]]
    assert METHOD_REGISTRY["loggamma_ratio"]["certified"][0] == REGISTRY["loggamma_ratio"]["certified"]


def test_stirling_ratio_method_is_active_only_for_explicit_certified_gamma_ratio():
    active_gamma_ratio_methods = [
        method
        for method in available_methods()
        if method.function == "gamma_ratio" and method.mode == "certified"
    ]
    stirling_ratio_methods = [method for method in available_methods() if method.method_id == "stirling_ratio"]

    assert [method.method_id for method in active_gamma_ratio_methods] == ["arb", "stirling_ratio"]
    assert stirling_ratio_methods == [METHOD_REGISTRY["gamma_ratio"]["certified"][1]]
    assert METHOD_REGISTRY["gamma_ratio"]["certified"][0] == REGISTRY["gamma_ratio"]["certified"]


def test_available_methods_exposes_auditable_method_specs_in_dispatch_order():
    methods = available_methods()

    assert len(methods) == len(available_functions()) * 3 + 7
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


def test_loggamma_stirling_method_is_not_reinterpreted_for_high_precision_mode():
    with pytest.raises(ValueError, match="method 'stirling' is not available for 'loggamma' in mode 'high_precision'"):
        certsf.loggamma("50", dps=50, mode="high_precision", method="stirling")


def test_loggamma_shifted_stirling_method_is_not_reinterpreted_for_high_precision_mode():
    with pytest.raises(
        ValueError,
        match="method 'stirling_shifted' is not available for 'loggamma' in mode 'high_precision'",
    ):
        certsf.loggamma("50", dps=50, mode="high_precision", method="stirling_shifted")


@pytest.mark.parametrize("mode", ["high_precision", "fast"])
def test_loggamma_certified_auto_method_is_certified_mode_only(mode):
    with pytest.raises(ValueError, match=f"method 'certified_auto' is not available for 'loggamma' in mode '{mode}'"):
        certsf.loggamma("50", dps=50, mode=mode, method="certified_auto")


def test_explicit_certified_arb_method_never_falls_back_to_mpmath():
    result = certsf.loggamma("3.2", dps=50, mode="certified", method="arb")

    assert result.backend == "python-flint"
    assert result.method == "arb_ball"


def test_certified_mode_rejects_mpmath_method_request():
    with pytest.raises(ValueError, match="method 'mpmath' is not available for 'loggamma' in mode 'certified'"):
        certsf.loggamma("3.2", dps=50, mode="certified", method="mpmath")


def _backend_is_unavailable(result):
    return not result.certified and "python-flint is not installed" in result.diagnostics.get("error", "")
