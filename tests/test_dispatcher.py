import pytest

import certsf
from certsf import mcp_server
from certsf.dispatcher import (
    _METHOD_REGISTRY,
    _VALID_FUNCTIONS,
    available_functions,
    available_modes,
    dispatch,
)


def test_dispatcher_method_registry_covers_every_mode():
    expected_modes = {"fast", "high_precision", "certified"}

    assert set(_METHOD_REGISTRY) == expected_modes
    assert _VALID_FUNCTIONS
    for methods in _METHOD_REGISTRY.values():
        assert set(methods) == _VALID_FUNCTIONS
        assert all(callable(method) for method in methods.values())


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
