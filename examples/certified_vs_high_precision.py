from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from certsf import SFResult, airy, besselj, gamma, pcfu, rgamma


@dataclass(frozen=True)
class Example:
    name: str
    input_text: str
    evaluate: Callable[[str], SFResult]


EXAMPLES = (
    Example("gamma", 'z="3.2"', lambda mode: gamma("3.2", mode=mode, dps=80)),
    Example("rgamma", 'z="-2"', lambda mode: rgamma("-2", mode=mode, dps=80)),
    Example("airy", 'z="25"', lambda mode: airy("25", mode=mode, dps=80)),
    Example("besselj", 'v="2", z="1e-20"', lambda mode: besselj("2", "1e-20", mode=mode, dps=80)),
    Example("pcfu", 'a="2.5", z="1.25"', lambda mode: pcfu("2.5", "1.25", mode=mode, dps=80)),
)


HEADERS = (
    "function",
    "input",
    "mode",
    "value",
    "certified",
    "abs_error_bound",
    "backend",
    "certificate_scope",
)


def main() -> None:
    rows = []
    for example in EXAMPLES:
        for mode in ("high_precision", "certified"):
            result = example.evaluate(mode)
            rows.append(
                (
                    example.name,
                    example.input_text,
                    mode,
                    _shorten(result.value),
                    str(result.certified),
                    _shorten(result.abs_error_bound or ""),
                    result.backend,
                    str(result.diagnostics.get("certificate_scope", "")),
                )
            )
    _print_table(rows)


def _print_table(rows: list[tuple[str, ...]]) -> None:
    widths = [
        max(len(row[index]) for row in (HEADERS, *rows))
        for index in range(len(HEADERS))
    ]
    print(" | ".join(header.ljust(width) for header, width in zip(HEADERS, widths)))
    print("-+-".join("-" * width for width in widths))
    for row in rows:
        print(" | ".join(value.ljust(width) for value, width in zip(row, widths)))


def _shorten(value: str, limit: int = 42) -> str:
    if len(value) <= limit:
        return value
    return value[: limit - 3] + "..."


if __name__ == "__main__":
    main()
