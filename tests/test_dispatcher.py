import pytest

import certsf
from certsf import mcp_server
from certsf.dispatcher import (
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
            assert callable(method.callable)
            assert method.backend
            assert method.domain
            if mode == "certified":
                assert method.certified is True
                assert method.backend == "python-flint"
                assert method.certificate_scope is not None
            else:
                assert method.certified is False
                assert method.certificate_scope is None


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
