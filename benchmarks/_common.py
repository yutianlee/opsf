from __future__ import annotations

import json
from time import perf_counter
from typing import Any, Callable


Case = tuple[str, Callable[..., Any], tuple[Any, ...], dict[str, Any]]


def run_cases(cases: list[Case], *, repeats: int = 5) -> None:
    for name, function, args, kwargs in cases:
        best = None
        last = None
        for _ in range(repeats):
            start = perf_counter()
            last = function(*args, **kwargs)
            elapsed = perf_counter() - start
            best = elapsed if best is None else min(best, elapsed)
        assert last is not None
        print(
            json.dumps(
                {
                    "case": name,
                    "function": last.function,
                    "backend": last.backend,
                    "mode": last.diagnostics.get("mode"),
                    "requested_dps": last.requested_dps,
                    "working_dps": last.working_dps,
                    "runtime_seconds_best": best,
                    "certified": last.certified,
                    "abs_error_bound": last.abs_error_bound,
                },
                sort_keys=True,
            )
        )
