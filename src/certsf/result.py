"""Structured result object for special-function evaluation."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
from typing import Any


@dataclass(frozen=True)
class SFResult:
    """Result returned by all public special-function wrappers."""

    value: str
    abs_error_bound: str | None
    rel_error_bound: str | None
    certified: bool
    function: str
    method: str
    backend: str
    requested_dps: int
    working_dps: int
    terms_used: int | None
    diagnostics: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-friendly dictionary."""

        return asdict(self)

    def to_mcp_dict(self) -> dict[str, Any]:
        """Return a JSON-friendly dictionary with nested component payloads."""

        payload = self.to_dict()
        payload["value"] = _json_object_or_original(self.value)
        payload["abs_error_bound"] = _json_object_or_original(self.abs_error_bound)
        payload["rel_error_bound"] = _json_object_or_original(self.rel_error_bound)
        return payload

    def value_as_dict(self) -> dict[str, str]:
        """Decode a multi-component ``value`` JSON string."""

        return _require_json_object(self.value, "value")

    def abs_error_bound_as_dict(self) -> dict[str, str] | None:
        """Decode multi-component absolute error bounds when present."""

        if self.abs_error_bound is None:
            return None
        return _require_json_object(self.abs_error_bound, "abs_error_bound")

    def rel_error_bound_as_dict(self) -> dict[str, str] | None:
        """Decode multi-component relative error bounds when present."""

        if self.rel_error_bound is None:
            return None
        return _require_json_object(self.rel_error_bound, "rel_error_bound")

    def component(self, name: str) -> str:
        """Return one named component from a multi-component value."""

        return self.value_as_dict()[name]

    def to_json(self, **kwargs: Any) -> str:
        """Serialize the result to JSON."""

        options: dict[str, Any] = {"sort_keys": True}
        options.update(kwargs)
        return json.dumps(self.to_dict(), **options)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SFResult":
        """Build an :class:`SFResult` from a dictionary."""

        fields = {
            "value",
            "abs_error_bound",
            "rel_error_bound",
            "certified",
            "function",
            "method",
            "backend",
            "requested_dps",
            "working_dps",
            "terms_used",
            "diagnostics",
        }
        missing = fields.difference(data)
        if missing:
            missing_names = ", ".join(sorted(missing))
            raise ValueError(f"SFResult missing required fields: {missing_names}")
        return cls(
            value=str(data["value"]),
            abs_error_bound=data["abs_error_bound"],
            rel_error_bound=data["rel_error_bound"],
            certified=bool(data["certified"]),
            function=str(data["function"]),
            method=str(data["method"]),
            backend=str(data["backend"]),
            requested_dps=int(data["requested_dps"]),
            working_dps=int(data["working_dps"]),
            terms_used=None if data["terms_used"] is None else int(data["terms_used"]),
            diagnostics=dict(data["diagnostics"]),
        )

    def __repr__(self) -> str:
        return (
            "SFResult("
            f"function={self.function!r}, "
            f"value={self.value!r}, "
            f"certified={self.certified!r}, "
            f"backend={self.backend!r}, "
            f"method={self.method!r})"
        )


def _json_object_or_original(value: str | None) -> Any:
    if value is None:
        return None
    try:
        decoded = json.loads(value)
    except (TypeError, json.JSONDecodeError):
        return value
    return decoded if isinstance(decoded, dict) else value


def _require_json_object(value: str, field: str) -> dict[str, str]:
    try:
        decoded = json.loads(value)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{field} is not a JSON object string") from exc
    if not isinstance(decoded, dict):
        raise ValueError(f"{field} is not a JSON object string")
    return {str(key): str(item) for key, item in decoded.items()}
